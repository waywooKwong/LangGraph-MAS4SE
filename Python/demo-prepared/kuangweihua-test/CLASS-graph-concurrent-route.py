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
import os
import json
import functools
from typing import Dict, List, TypedDict
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


base_dir = "kuangweihua/ollama/areaText/areaText_v4/normal"  # 向量库文档文件夹
embedding_dir = "kuangweihua/ollama/models/m3e-base"  # embadding 路径

role = "软件开发人员"
duty = "根据你的分工完成软件开发任务"

agent_builder = BuildChainAgent(base_dir, embedding_dir, role, duty)
role_chain = agent_builder.create_retriever_chain()
chat_history = []

# 1. 改 Message 类型
# 2. Sequence 链的类实现
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "graph-0725"
os.environ["TAVILY_API_KEY"] = "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"


import functools
import operator
from typing import Annotated, List


# 0.0 Graph 整体通信类型（之后可以换成 FIPA-ACL）
class AgentState(TypedDict):
    sender: str
    progress: str
    messages: Annotated[List[BaseMessage], operator.add]

initial_question = HumanMessage(content="请设计一个银行管理系统")


# 3-5. Graph 生成
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
    
def router(state: AgentState) -> str:
    # 检查 message 中是否包含 'schedule' 和 'code'
    contains_schedule = "Schedule Plan" in state["messages"][-1].content.lower()
    contains_code = "Code Format" in state["messages"][-1].content.lower()

    if not contains_schedule and not contains_code:
        # 如果 message 中既不包含 'schedule' 也不包含 'code'
        return "Schedule Plan"
    elif contains_schedule and not contains_code:
        # 如果 message 中包含 'schedule' 但不包含 'code'
        return "Code Format"
    elif not contains_schedule and contains_code:
        # 如果 message 中不包含 'schedule' 但包含 'code'
        return "Schedule Plan"
    elif contains_schedule and contains_code:
        # 如果 message 中包含 'schedule' 和 'code'
        return "__end__"


# 3. 图构建
# 3-1. 图流实例化
workflow = StateGraph(AgentState)


# 3-2. 图中加点
role2 = "Tech Leader"
role3 = "Schedule Plan"
role4 = "Code Format"
role2_members = [role3, role4]

from typing import List, Dict, Any

def router_concurrent_choice(state: AgentState, members: Dict[str, Any]) -> str:
    # 获取已有的消息中已出现的成员名称
    visited_members = {message.name for message in state["messages"]}
    
    # 遍历所有成员，找到第一个未访问过的成员
    for member_key, member_value in members.items():
        if member_value not in visited_members:
            return member_key  # 返回成员值（即 role3, role4）

    # 如果所有成员都已访问过，则跳转到 'Finish'
    return "Finish"
    
from functools import partial

workflow.add_edge(START, role2)

# 定义角色与下一步节点的映射
role_map = {
    "Schedule Plan": role3,
    "Code Format": role4,
    "Finish": END,
}

workflow.add_node(role2, partial(func_node, node_name=role2))
workflow.add_node(role3, partial(func_node, node_name=role3))
workflow.add_node(role4, partial(func_node, node_name=role4))

workflow.add_edge(role3, role2)
workflow.add_edge(role4, role2)


# 添加条件边
workflow.add_conditional_edges(
    role2,
    lambda state: router_concurrent_choice(state, role_map),
    role_map
)

# 保存图片
import datetime
graph = workflow.compile()
print("graph:", graph)
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
file_path = f"/home/zhengtinghua/kuangweihua/ollama/LangChain-for-Ollama/workflow-image/workflow_graph_{timestamp}.png"
save_graph_image(graph, file_path)

# 4. 运行graph
events = graph.stream(
    {"sender": "__start__", "progress": "initial", "messages": [initial_question]},
    {"recursion_limit": 10},  # 运行迭代步数
)

for round in events:
    print("----")
    print(round)
    print("----")
