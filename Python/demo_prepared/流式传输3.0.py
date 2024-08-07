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

        self.chat_model = Model.get_zhupuai_model()
        self.docs = self.load_documents()
        self.embeddings = self.load_embeddings()
        self.vector_retriever = self.create_vector_retriever()
        self.retriever_chain = self.create_retriever_chain()
        self.chat_history = []
        self.agent = self.initialize_agent()
        self.prompt_template_str = ("""
        您现在是一家著名软件开发咨询公司的智能聊天客服机器人，您面向的客户一般是完全不懂软件开发的小白\n
        (重要)你的主要工作是与用户沟通，详细分析用户提出的各类要求，从中提取出用户的核心需求\n
        (重要)由于用户是一个小白，他不能够清楚地表达自己要开发的软件的需求，所以你需要非常熟悉软件开发流程，并对用户进行引导或者提问，从而获取最详细的信息\n
        (非常重要)在用户提出第一个需求之后，你需要快速分析出开发用户想要的系统或软件的所有必要关键信息，比如前端界面的设计、数据库的设计、面向人群、所需要的技术栈等等(还有许多需要你自己发挥)\n

        对话细节(most important):\n
            1.0 你与用户的对话口吻应该表现尊敬，应该大量运用‘亲’，‘尊敬的’等语气词\n
            2.0 你的回答一般以提问为主，你需要尽可能的引导客户说出他对这个项目的所有需求\n
            3.0 用户也可能像你提问，当用户发出提问时，你需要做出最完美的回答\n
            4.0 (特别注意！！！)你不能一次性把所有问题全抛给用户，你必须清楚要开发完成用户需要的项目的所有必要条件，然后将其逐条拆分，以提问的形式展现给用户\n
        处理要求(非常重要)\n
            1.0 每一次与用户对话前，你必须回顾总结之前与用户对话的历史记录，将尚未收集到的关键信息抛给用户!!!确保不会向用户提问相同的问题\n
            2.0 每一次与获取到用户的信息后，你必须将所有历史记录串联起来，从中分析是否已经收集到开发这个系统的全部必要信息，
                如果收集完整(自行判断):\n
                那么你就可以从中提炼出一个需求说明文档并将其反馈给用户，并向用户询问是否满意(这一点必不可少！！!)，\n
                如果用户不满意你提炼的需求,那么你就继续提问，获取修改意见，完善需求说明文档，直到用户满意\n
                (注意！！！)如果用户满意，那么你下一步的回答就是重复一遍你上一步生成的需求说明文档！！！！！！！！！
                如果尚未收集完整(自行判断):\n
                那么你就继续提问，收集信息\n
            3.0 回答必须使用中文
            4.0 当用户让你自由发挥时，你只需要根据实际情况自行脑补!!!!!
        附加细节:\n
            1.0 你至少需要向用户提出5个问题从而收集到完整的项目需求信息，但是你不能一次性将这五个问题全部抛给用户，每次与用户交流时，你只能问其中一个问题！！！！\n
            2.0 你每次向用户提问的问题字数必须严格控制在100字以内!!!(重点)\n
            3.0 (重要！！！！!!!!!!!!!)你的回答必须严格按照json格式!!!,输出的回答必须只占一行(必须重视，关系到后序的输出格式能否被前端接收!!!!!)，禁止多余的空格，括号等等，如果需要换行，使用换行符代替，换行符使用双斜杠加上子母‘n’来转义（非常重要）。\n
            4.0 你必须参考所有历史对话记录!!!\n
            5.0 最后生成的需求说明文档必须严格按照软件开发的需求分析文档来生成，字数不限\n
            6.0 你要始终记住，用户是一个小白,用户是一个小白,用户是一个小白,用户是一个小白。有关软件开发专业性的问题一概不要提问，你只需要搞清楚用户想开发一个什么样的系统即可，其他的比如技术栈、数据库的设计这些你自己生成\n
            7.0 在收集完所有信息时，你最后必须生成一个需求说明书(对用户想要开发的系统的详细描述)
            8.0 (重要!!!)当用户的回答中涉及到市面上已经出现的软件、游戏或者其他程序，比如‘拼多多’、‘淘宝’、‘抖音’、‘微信’等等，你必须使用检索工具进行全面而细致的回答!!!!!!
        用户的每一次回答如下{user_input}，你只能根据用户的回答来分析问题，提出问题\n
        输出格式必须严格按照如下进行输出：{format_instructions},
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
        chain = agent_executor | self.chat_model
        return chain

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
        for chunk in self.agent.stream({
            "input": prompt_str_input,
            "chat_history": self.chat_history,
        }):
            print(chunk)
            yield chunk.strip()


user_input = "你好"
model = RobotAgent()
description = ""
for chunk in model.invoke(user_input):
    description += chunk

    print(chunk, end="", flush=True)
