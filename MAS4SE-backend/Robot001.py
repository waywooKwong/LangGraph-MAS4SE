# -*- coding: utf-8 -*-
"""
说明-20240724
1. 注意 chat_model 在 BuildChainAgent 中的初始化(默认是Ollama,其它情况需要注意 modelchoise)
2. BuildChainAgent 注释的 system prompt(需要个性化定制) 共有两处
    需要调用prompt个性化生成器生成
3. 注意涉及的代码都打包成 Class(不含 modelchoise的 chat_model 加载）
4. 调用时,embedding调用路径确认清楚
5. question node 里还有一个model
6.83/84行改相对路径
"""
"""
说明20240807晚上
在提示词部分稍作修改
"""
import os
import json
import functools
from typing import Dict, List, TypedDict
from langgraph.graph import END, StateGraph, START
from langchain.agents import initialize_agent, AgentType, Tool
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain import hub
from langchain.agents import (
    create_openai_functions_agent,
    initialize_agent,
    AgentType,
    AgentExecutor,
)

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
from ModelChoise import Model
from ModelChoise.modelchoise import get_tongyi_chat_model
from Class_01_PromptGenerator import PromptGenerator
from langchain_core.prompts import PromptTemplate
from typing import Dict, Any

# 禁用并行处理
os.environ["TOKENIZERS_PARALLELISM"] = "false"
Model.os_setenv()


def generate_prompt(role: str, duty: str) -> str:
    generator = PromptGenerator()
    description = ""
    for chunk in generator.generate_prompt(role=role, duty=duty):
        description += chunk
        print(chunk, end="", flush=True)
    return description


class RobotAgent:
    """
    注意 chat_model 模型的加载，
    默认使用的是 Ollama 加载方式
    params:
        base_dir 用于构造向量库的文档的目标文件夹
        embeddings 编码模型的加载位置
        role (个性化)角色
        duty (个性化)职责

    """

    def __init__(self):
        os.environ["SERPAPI_API_KEY"] = "b0b73f4f0f7a24ef9a1cbba1629e6ac5f4221b5dfb491af209a0a1ae6c241338"
        os.environ[
            "USER_AGENT"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0")
        # os.environ["TOKENIZERS_PARALLELISM"]=True
        self.base_dir = "src/role_txt"
        self.embedding_dir = "src/embedding_models/m3e-base"

        # self.chat_model = Model.get_zhupuai_model()
        self.chat_model = ChatOllama(model="qwen2")
        self.docs = self.load_documents()
        self.embeddings = self.load_embeddings()
        self.vector_retriever = self.create_vector_retriever()
        self.retriever_chain = self.create_retriever_chain()
        self.chat_history = []
        self.agent = self.initialize_agent()
        self.prompt_template_str = ("""
        您现在是一家著名软件开发咨询公司的智能聊天客服机器人，您的主要任务是满足用户的需求，详细分析用户的要求，并提取出核心需求。

        1. **核心任务**：
           - 提供详尽的需求收集，确保每个问题都针对用户的实际需求。
           - 与用户沟通时，深入分析并提取用户的核心需求，避免遗漏关键点。
        
        2. **提问要求**：
           - (非常重要)每次只提出一个问题，引导用户详细描述需求。
           - (非常重要)避免一次性抛出多个问题，以免让用户感到困惑。
           - 每次提问时，确保问题紧密围绕软件的核心功能，避免无关问题干扰。
        
        3. **用户提问环节**：
           - **接收提问**：用户可以随时向您提问。当遇到用户提问时，运用您的知识或搜索工具，提供最准确的回答。
           - **回答要求**：
             - 回答必须使用严格的Markdown格式。
             - 字数尽可能多，至少1000字，确保回答详尽、准确，并能全面解答用户的疑问。
             - **避免重复**：回顾历史对话，确保不重复回答相同问题。
             - **提供网址**：如果回答需要引用外部网址（例如官网），请在回答中附上准确的网址，并明确说明网址的用途，以便用户方便查找相关信息。
        
        4. **信息收集与整理**：
           - 每次对话前，回顾历史记录，避免重复提问。
           - 将历史记录串联起来，确保需求说明文档的完整性和一致性。
        
        5. **需求说明文档**：
           - 包含系统的功能需求、非功能需求、界面设计、技术栈等详细信息。
           - 每部分描述必须详细，使用Markdown格式进行排版，确保用户理解。
           - Markdown格式示例（以下仅为示例，实际生成要更加详细）：
             - **功能需求**：
               - 列出所有功能需求
               - 对每项功能需求进行详细描述，说明其用途和实现方式
             - **非功能需求**：
               - 列出所有非功能需求
               - 对每项非功能需求进行详细描述，说明其对系统性能、可靠性等的影响
             - **界面设计**：
               - 描述界面的设计需求
               - 提供界面设计的示意图（如适用），说明每个界面的布局和功能
             - **技术栈**：
               - 列出所使用的技术栈
               - 说明每种技术的选择理由，包括技术的优势和适用场景
        
        6. **格式和规范**：
           - 输出必须符合JSON格式，并使用转义符处理换行。
           - 避免多余的空格和括号，保持格式简洁。
        
        7. **用户知识水平**：
           - 避免提问过于专业的问题，确保问题适合用户的知识水平。
           - 根据用户的回答和专业知识，调整需求说明文档的细节，以符合用户的实际需求。
        
        用户的每次回答如下{user_input}。请根据用户的回答和历史对话来分析问题并提问。同时，当用户提出问题时，请提供详细解答，并确保回答符合上述格式和规范要求。
        
        **输出格式**：{format_instructions}

                    """
                                    )
        response_schemas = [
            # ResponseSchema(name="description", description="用户问题"),
            ResponseSchema(name="sender", description="发送者，对你来说就是‘智能客服机器人’"),
            ResponseSchema(name="progress",
                           description="状态判断，如果需求说明书已经生成那么返回‘true’,否则返回‘false’"),
            ResponseSchema(name="answer", description="与用户对话的内容"),
        ]
        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas=response_schemas)
        self.format_instructions = self.output_parser.get_format_instructions()
        self.prompt_template = PromptTemplate.from_template(
            template=self.prompt_template_str,
            partial_variables={"format_instructions": self.format_instructions}
        )
    def detect_encoding(self, file_path):
        import chardet
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)  # 读取文件的一部分来检测编码
        result = chardet.detect(raw_data)
        return result['encoding']
    def load_documents(self):
        docs = []
        for filename in os.listdir(self.base_dir):
            file_path = f"{self.base_dir}/{filename}"
            print("file_path:", file_path)
            encoding = self.detect_encoding(file_path)
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(file_path, encoding=encoding)
            elif filename.endswith(".docx"):
                loader = Docx2txtLoader(file_path, encoding=encoding)
            elif filename.endswith(".txt"):
                loader = TextLoader(file_path, encoding=encoding)
            else:
                continue
            docs.extend(loader.load())
        return docs

    def create_vector_retriever(self):
        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(documents=self.docs)
        vector = Qdrant.from_documents(
            documents=documents,
            embedding=self.embeddings,
            location=":memory:",
            collection_name="Qdrant_vectorstore"
        )
        return vector.as_retriever()

    def create_retriever_chain(self):
        # 历史对话的 Prompt
        history_prompt = ChatPromptTemplate.from_messages(
            messages=[
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", """需求的描述是{input}"""),
                ("user",
                 "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation.")
            ]
        )
        history_chain = create_history_aware_retriever(llm=self.chat_model, prompt=history_prompt,
                                                       retriever=self.vector_retriever)

        # 加载文档处理的内容
        ################## system prompt 1(需要个性化定制)
        doc_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "你现在是一家著名软件开发咨询公司的智能聊天客服机器人,请在你的指着视角解读你接受到的需求文本如下：{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}")
        ])
        documents_chain = create_stuff_documents_chain(self.chat_model, doc_prompt)
        chain_first = create_retrieval_chain(history_chain, documents_chain)
        ################# system prompt 2(需要个性化定制)
        template_second = "你的职责是与用户进行多轮沟通 ，根据{role_text}的内容，给出你的设计实现方案。保持 json 格式输出"
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
                {"role_text": chain_first} | prompt_template_second | self.chat_model | StrOutputParser()
        )

        return chain_second

    def retriever_tool(self, query):
        raw_response = self.retriever_chain.invoke({
            "chat_history": self.chat_history,
            "input": query
        })
        return raw_response["output"]

    def initialize_agent(self):
        tools = load_tools(tool_names=["serpapi", "llm-math"], llm=self.chat_model)
        retriever_tool_instance = Tool(
            name="retriever_tool",
            description="This tool handles document retrieval and question answering based on context history.",
            func=self.retriever_tool,
        )
        prompt = hub.pull("hwchase17/openai-functions-agent")
        tools.append(retriever_tool_instance)
        agent = create_openai_functions_agent(self.chat_model, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        # return initialize_agent(
        #     tools=tools,
        #     llm=self.chat_model,
        #     agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        #     verbose=True,
        #     handle_parsing_errors=True
        # )
        return agent_executor

    def load_embeddings(self):
        embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_dir,
            model_kwargs={'device': 'cpu'}
        )
        print("Embedding from huggingface: \n", embeddings)
        return embeddings

    def invoke(self, input: str) -> str:
        # Invoke the retriever chain
        prompt_str_input = self.prompt_template.format(user_input=input)
        response = self.agent.invoke({
            "input": prompt_str_input,
            "chat_history": self.chat_history,
        })
        print("Response:", response)
        # Update chat history
        self.chat_history.append(HumanMessage(content=prompt_str_input))
        self.chat_history.append(AIMessage(content=response["output"]))

        return response["output"]
