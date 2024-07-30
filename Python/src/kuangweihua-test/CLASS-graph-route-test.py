# -*- coding: utf-8 -*-
"""
说明-20240724
1. 注意 chat_model 在 BuildChainAgent 中的初始化(默认是Ollama,其它情况需要注意 modelchoise)
2. BuildChainAgent 注释的 system prompt(需要个性化定制) 共有两处
    需要调用prompt个性化生成器生成
3. 注意涉及的代码都打包成 Class(不含 modelchoise的 chat_model 加载）
4. 调用时,embedding调用路径确认清楚
"""

"""
这段代码是 TTL-QA1 QA2 伪顺序的图链接构造方式
"""

"""
20240728- 代码跑通！-weihua
调试说明：
涉及的路径：
1. line 213,214 || base_dir,embedding_dir 
2. line 353 || file_path
"""
import os
import json
import operator
import functools
from functools import partial

from typing import Dict, List, TypedDict, Annotated, Any
from langgraph.graph import END, StateGraph, START
from langchain.agents import initialize_agent, AgentType, Tool

from langchain.chains import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage


from langchain_community.chat_models import ChatOllama
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import FAISS, Qdrant
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_community.agent_toolkits.load_tools import load_tools

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

# 禁用并行处理
os.environ["TOKENIZERS_PARALLELISM"] = "false"


class BuildChainAgent:
    """
    注意 chat_model 模型的加载，
    默认使用的是 Ollama 加载方式
    params:
        base_dir 用于构造向量库的文档的目标文件夹
        embeddings 编码模型的加载位置
        role (个性化)角色
        duty (个性化)职责

    """

    def __init__(self, base_dir: str, embedding_dir: str, role: str, duty: str):
        os.environ["SERPAPI_API_KEY"] = (
            "b0b73f4f0f7a24ef9a1cbba1629e6ac5f4221b5dfb491af209a0a1ae6c241338"
        )
        os.environ["USER_AGENT"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
        )
        # os.environ["TOKENIZERS_PARALLELISM"]=True
        self.base_dir = base_dir
        self.embedding_dir = embedding_dir

        self.role = role
        self.duty = duty
        self.chat_model = ChatOllama(model="qwen2")

        self.docs = self.load_documents()
        self.embeddings = self.load_embeddings()
        self.vector_retriever = self.create_vector_retriever()
        self.retriever_chain = self.create_retriever_chain()
        self.chat_history = []

    def load_documents(self):
        docs = []
        for filename in os.listdir(self.base_dir):
            file_path = os.path.join(self.base_dir, filename)
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            elif filename.endswith(".docx"):
                loader = Docx2txtLoader(file_path)
            elif filename.endswith(".txt"):
                loader = TextLoader(file_path)
            else:
                continue
            docs.extend(loader.load())
        return docs

    def load_embeddings(self):
        embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_dir, model_kwargs={"device": "cpu"}
        )
        print("Embedding from huggingface: \n", embeddings)
        return embeddings

    def create_vector_retriever(self):
        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(documents=self.docs)
        vector = Qdrant.from_documents(
            documents=documents,
            embedding=self.embeddings,
            location=":memory:",
            collection_name="Qdrant_vectorstore",
        )
        return vector.as_retriever()

    def create_retriever_chain(self):
        # 历史对话的 Prompt
        history_prompt = ChatPromptTemplate.from_messages(
            messages=[
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", """需求的描述是{input}"""),
                (
                    "user",
                    "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation.",
                ),
            ]
        )
        history_chain = create_history_aware_retriever(
            llm=self.chat_model, prompt=history_prompt, retriever=self.vector_retriever
        )

        # 加载文档处理的内容
        ################## system prompt 1(需要个性化定制)
        doc_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "现在你是多智能体系统中的一个智能体，你的角色是软件开发过程中的:"
                    + self.role
                    + "请在你的指着视角解读你接受到的需求文本如下：{context}",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
            ]
        )
        documents_chain = create_stuff_documents_chain(self.chat_model, doc_prompt)
        chain_first = create_retrieval_chain(history_chain, documents_chain)
        ################# system prompt 2(需要个性化定制)
        template_second = (
            "你的职责是:"
            + self.duty
            + "根据{role_text}的内容，给出你的设计实现方案。保持 json 格式输出"
        )
        prompt_template_second = ChatPromptTemplate.from_template(template_second)

        # 当前 chain 由于 StrOutputParser()的解析，chain.invoke 直接输出 str
        # 如果要保持字典序
        # from langchain.output_parsers import StructuredOutputParser, ResponseSchema
        # # 定义响应架构
        # response_schemas = [
        #     ResponseSchema(name="output", description="The output from the model")
        # ]
        # output_parser = StructuredOutputParser(response_schemas=response_schemas)
        # # 修改 chain_second
        # chain_second = (
        #     {"role_text": chain_first} | prompt_template_second | self.chat_model | output_parser
        # )

        chain_second = (
            {"role_text": chain_first}
            | prompt_template_second
            | self.chat_model
            | StrOutputParser()
        )

        return chain_second

    def retriever_tool(self, query):
        raw_response = self.retriever_chain.invoke(
            {"chat_history": self.chat_history, "input": query}
        )
        return raw_response["output"]

    def initialize_agent(self):
        tools = load_tools(tool_names=["serpapi", "llm-math"], llm=self.chat_model)
        retriever_tool_instance = Tool(
            name="retriever_tool",
            description="This tool handles document retrieval and question answering based on context history.",
            func=self.retriever_tool,
        )
        tools.append(retriever_tool_instance)

        return initialize_agent(
            tools=tools,
            llm=self.chat_model,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
        )


# LangSmith
# os.environ["LANGCHAIN_API_KEY"] = "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"
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_PROJECT"] = "graph-route-0725"
os.environ["TAVILY_API_KEY"] = "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"

base_dir = "kuangweihua/ollama/areaText/areaText_v4/normal"  # 向量库文档文件夹
embedding_dir = "kuangweihua/ollama/models/m3e-base"  # embadding 路径

role = "软件开发人员"
duty = "根据你的分工完成软件开发任务"

agent_builder = BuildChainAgent(base_dir, embedding_dir, role, duty)
role_chain = agent_builder.create_retriever_chain()
chat_history = []


# 0.0 Graph 整体通信类型（之后可以换成 FIPA-ACL）
class AgentState(TypedDict):
    sender: str
    progress: str
    messages: Annotated[List[BaseMessage], operator.add]
    next: str


initial_question = HumanMessage(content="请设计一个银行管理系统")


def save_graph_image(graph, file_path):
    from IPython.display import Image
    from PIL import Image as PILImage
    import io

    try:
        image_data = graph.get_graph(xray=True).draw_mermaid_png()
        image = PILImage.open(io.BytesIO(image_data))
        image.save(file_path)
        print(f"图像已保存为 {file_path}")
    except Exception as e:
        print(f"保存图像失败: {e}")


### 通用 node 处理  - 240725
def func_node(state: AgentState, node_name) -> AgentState:
    last_message = state["messages"][-1]
    prompt = last_message.content
    response = role_chain.invoke({"input": prompt, "chat_history": state["messages"]})
    ai_message_content = response

    result = AIMessage(name=node_name, content=ai_message_content)
    return {
        "sender": node_name,
        "progress": state["progress"],
        "messages": state["messages"] + [result],
    }


def router_concurrent_choice(state: AgentState, members: Dict[str, Any]) -> str:
    visited_members = {message.name for message in state["messages"]}
    for (
        member_key,
        member_value,
    ) in members.items():  # 遍历所有成员，找到第一个未访问过的成员
        if member_value not in visited_members:
            return member_key
    return "Finish"


### supervisor
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


from langchain_community.chat_models import ChatOllama
from langchain_community.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatAnthropic
from langchain_experimental.llms.anthropic_functions import AnthropicFunctions
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser

workflow = StateGraph(AgentState)

# 3-2. 图中加点
role2 = "Tech Leader"
role3 = "Schedule Plan"
role4 = "Code Format"
conditional_map = {"Schedule Plan": role3, "Code Format": role4, "Finish": END}

members = [value for value in conditional_map.values() if value != END]
print("members:", members)

options = ["END"] + members
print("options:", options)
for member in members:
    workflow.add_edge(member, role2)

from langchain_core.prompts import PromptTemplate


def supervisor_chain(state: AgentState):
    system_prompt = (
        " You are a supervisor tasked with managing a conversation between the"
        " following workers(Attetion:Just select one of them):  {members}. Given the following user request,"
        " respond with the worker to act next. Each worker will perform a"
        " task and respond with their results and status. When finished,"
        " respond with FINISH."
        "{format_instruction}"
    )
    response_schema_01 = [
        ResponseSchema(name="next", description="next role to router to members"),
    ]
    output_parser_01 = StructuredOutputParser.from_response_schemas(
        response_schemas=response_schema_01
    )
    format_instruction_01 = output_parser_01.get_format_instructions()
    prompt_template_01 = PromptTemplate.from_template(
        template=system_prompt,
        partial_variables={"format_instruction": format_instruction_01},
    )
    prompt_str_input_01 = prompt_template_01.format(members=members)
    llm = ChatOllama(model="qwen2")
    output_completion_01: AIMessage = llm.invoke(input=prompt_str_input_01)
    print("output_completion:", output_completion_01)
    content_str = output_completion_01.content
    print("content_str:", content_str)
    json_str = content_str.strip("```").replace("json\n", "").strip()
    print("json_str:", json_str)
    json_data = json.loads(json_str)
    print("json_data:", json_data)
    next_value = json_data["next"]
    print("next_value:", next_value)
    next_key = {v: k for k, v in conditional_map.items()}.get(next_value, "Finish")
    return next_key


workflow.add_edge(START, role2)
workflow.add_node(role2, partial(func_node, node_name=role2))
workflow.add_node(role3, partial(func_node, node_name=role3))
workflow.add_node(role4, partial(func_node, node_name=role4))

workflow.add_conditional_edges(
    role2,
    supervisor_chain,
    conditional_map,
)

# 代码运行部分
import datetime

graph = workflow.compile()
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
file_path = f"/home/zhengtinghua/kuangweihua/ollama/LangChain-for-Ollama/workflow-image/workflow_graph_{timestamp}.png"
save_graph_image(graph, file_path)


events = graph.stream(
    {
        "sender": "__start__",
        "progress": "initial",
        "messages": [initial_question],
        "next": "need to check",
    },
    {"recursion_limit": 10},
)

for round in events:
    print("----")
    print(round)
    print("----")
