# -*- coding: utf-8 -*-
"""
说明-20240724
1. 注意 chat_model 在 BuildChainAgent 中的初始化(默认是Ollama,其它情况需要注意 modelchoise)
2. BuildChainAgent 注释的 system prompt(需要个性化定制) 共有两处
    需要调用prompt个性化生成器生成
3. 注意涉及的代码都打包成 Class(不含 modelchoise的 chat_model 加载）
4. 调用时,embedding调用路径确认清楚
5. question node 里还有一个model

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


# def generate_prompt(role: str, duty: str) -> str:
#     generator = PromptGenerator()
#     description = ""
#     for chunk in generator.generate_prompt(role=role, duty=duty):
#         description += chunk
#         print(chunk, end="", flush=True)
#     return description


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

    def __init__(self, role: str, duty: str, description: str):
        os.environ["SERPAPI_API_KEY"] = (
            "b0b73f4f0f7a24ef9a1cbba1629e6ac5f4221b5dfb491af209a0a1ae6c241338"
        )
        os.environ["USER_AGENT"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
        )
        self.base_dir = "src/role_txt"
        self.embedding_dir = "src/embedding_models/m3e-base"

        self.role = role
        self.duty = duty
        self.object = ""
        self.chat_model = Model.get_zhupuai_model()

        self.docs = self.load_documents()

        self.embeddings = self.load_embeddings()
        self.vector_retriever = self.create_vector_retriever()
        self.retriever_chain = self.create_retriever_chain()
        self.chat_history = []
        self.description = description
        self.agent = self.initialize_agent()
        # 下述字符串删除 {format_instructions}
        self.prompt_template_str = """
            您的描述如下{description}。

            ### 角色职责与合作
            - 您通常需要独自解决用户提出的问题，但大多数情况下，您会与伙伴合作解决问题。
            - **非常重要**：明确自身的角色{role}及伙伴的技能和特长。通过提问或回答获取必要的信息，确保您的回答或提问符合角色职责和上下文。
            
            ### 对话规则
            - **最重要**：在一次对话中，您只能扮演（提问方）或（回答方）其中一个角色。确保角色分配清晰，避免角色混乱。
            - **重要**：分点作答时使用Markdown格式中的标题（如##、###）来标注。
            - **重要**：与其他角色对话时，保持现实世界中团队开发交流的口吻，确保语言自然且专业。
            
            ### 任务响应
            - **非常重要**：对外界提供的基础信息进行分析，针对用户或其他角色提出的需求‘{input}’给出最完美的回答。
            - **格式要求**：
              - **Markdown格式**：回答必须按照Markdown格式回复，确保格式清晰且符合标准。
              - **字数要求**：生成内容不少于4000字，最多不超过8000字。
              - **图示要求**：
                - **架构图**：提供系统或项目的目录架构图，展示主要组件及其关系。
                  ```markdown
                  ## 系统架构图
                  - **系统组件 A**
                    - 子组件 A1
                    - 子组件 A2
                  - **系统组件 B**
                    - 子组件 B1
                    - 子组件 B2
                  - **系统组件 C**
                    - 子组件 C1
                    - 子组件 C2
                  ```
                - **流程图**：展示具体的工作流程或系统流程，确保步骤清晰。
                  ```markdown
                  ## 软件开发项目流程图
            
                  ```plaintext
                  +----------------+          +-----------------+          +-----------------+
                  | 需求分析       |          | 设计阶段        |          | 实现阶段        |
                  | (需求调研、     |          | (系统架构设计、  |          | (编码、单元测试)|
                  | 需求定义)       |          | 详细设计)        |          |                 |
                  +----------------+          +-----------------+          +-----------------+
                        |                         |                            |
                        |                         |                            |
                        v                         v                            v
                  +----------------+          +-----------------+          +-----------------+
                  | 需求文档       |          | 设计文档        |          | 代码            |
                  | (编写需求文档)  |          | (编写设计文档)  |          | (编写代码、      |
                  +----------------+          +-----------------+          | 单元测试)        |
                        |                         |                            |
                        |                         |                            |
                        v                         v                            |
                  +----------------+          +-----------------+          +-----------------+
                  | 评审阶段       |          | 实现验收        |          | 集成测试        |
                  | (需求评审、     |          | (代码审查、     |          | (集成测试、      |
                  | 设计评审)       |          | 功能测试)       |          | 系统测试)        |
                  +----------------+          +-----------------+          +-----------------+
                        |                         |                            |
                        |                         |                            |
                        v                         v                            v
                  +----------------+          +-----------------+          +-----------------+
                  | 修订阶段       |          | 整合与修正      |          | 项目交付        |
                  | (修改需求、     |          | (修复缺陷、     |          | (发布、文档)    |
                  | 设计文档)       |          | 系统整合)       |          |                 |
                  +----------------+          +-----------------+          +-----------------+
                        |                         |                            |
                        |                         |                            |
                        v                         v                            v
                  +-------------------------------------------------------------+
                  | 维护阶段                                                   |
                  | (问题修复、更新、    |
                  | 支持)                   |
                  +-------------------------------------------------------------+
                  ```
            
                - **用例图**：展示系统的用例图，明确用户与系统之间的交互，并包含小人图标。
                  ```markdown
                  ## 用例图
            
                  ### 参与者
                  - **用户** ![用户图标](https://example.com/user-icon.png)
                  - **管理员** ![管理员图标](https://example.com/admin-icon.png)
            
                  ### 用例
                  - **用户**
                    - **登录系统**: 用户可以通过提供用户名和密码登录到系统。
                    - **查看账户信息**: 用户可以查看和编辑他们的账户信息。
                    - **提交请求**: 用户可以提交请求或问题给支持团队。
                    
                  - **管理员**
                    - **管理用户**: 管理员可以创建、修改和删除用户账户。
                    - **查看系统报告**: 管理员可以查看系统生成的各种报告和统计数据。
                    - **配置系统设置**: 管理员可以调整系统的配置设置。
            
                  ### 用例图示例
            
                  ```plaintext
                  +----------------+          +------------------+
                  |    用户        |          |    管理员        |
                  |                |          |                 |  
                  +----------------+          +------------------+
                         |                            |
                         |                            |
                         |                            |
                         |                            |
                  +--------------+             +-------------------+
                  | 登录系统     |             | 管理用户          |
                  +--------------+             +-------------------+
                         |                            |
                         |                            |
                         |                            |
                         |                            |
                  +--------------+             +-------------------+
                  | 查看账户信息 |             | 查看系统报告      |
                  +--------------+             +-------------------+
                         |                            |
                         |                            |
                         |                            |
                         |                            |
                  +--------------+             +-------------------+
                  | 提交请求     |             | 配置系统设置      |
                  +--------------+             +-------------------+
                  ```
            
              - **数据库生成**：
                - 必须附上创建数据库的SQL语句，确保语句完整并能够正确创建所需的数据库结构。
              - **关键代码**：
                - 最后一定附上关键代码片段，确保代码示例能够有效支持需求和解决问题。
            
            ### 角色具体要求
            1. **角色明确**：清楚自己在对话中的角色和职责，确保回答符合角色的职能和任务。
            2. **对话细节**：在对话中，始终保持角色一致性，生成生动的对话口吻，确保交流自然流畅。
            3. **任务执行**：根据角色的职责，生成详尽的回答，确保符合软件开发流程，并解决用户的实际需求。
            
            请根据这些要求生成您的回答，并确保所有输出均符合上述规则和格式要求。每个部分都应详细且准确，图示和代码需清晰、易于理解。

                    """
        response_schemas = [
            # ResponseSchema(name="description", description="用户问题"),
            ResponseSchema(
                name="answer", description="根据信息划分任务或者回答另一个角色的问题"
            ),
        ]
        self.output_parser = StructuredOutputParser.from_response_schemas(
            response_schemas=response_schemas
        )
        self.format_instructions = self.output_parser.get_format_instructions()
        self.prompt_template = PromptTemplate.from_template(
            template=self.prompt_template_str,
            # partial_variables={"format_instructions": self.format_instructions},
        )

    def detect_encoding(self, file_path):
        import chardet

        with open(file_path, "rb") as f:
            raw_data = f.read(10000)  # 读取文件的一部分来检测编码
        result = chardet.detect(raw_data)
        return result["encoding"]

    def load_documents(self):
        ### !!! 需要定制角色文本的时候再启动这部分代码，因为一直启动速度过慢
        ## 直接取消下述的注释即可(DuckDuckGo 保持注释)
        # role_text_generator = WebScratchRoleTxt(role=self.role)
        # # role_text_generator.DuckDuckGo_search()
        # role_text_generator.GoogleSerper_search()
        # role_text_generator.Google_ScrapeUrls()
        # docs = []
        # file_path = role_text_generator.URL_Scraper_txt_path
        docs = []
        file_path = "src/role_txt/SoftwareBasicFlow.txt"
        encoding = self.detect_encoding(file_path)
        loader = TextLoader(file_path, encoding=encoding)
        docs.extend(loader.load())
        print(f"{self.role} role txt generate & load:", file_path)
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

    def invoke(self, user_input: str) -> str:
        # Invoke the retriever chain
        response = self.agent.invoke(
            {
                "input": user_input,
                "chat_history": self.chat_history,
            }
        )

        # Update chat history
        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=response["output"]))

        return response["output"]

    def process(self, input: str) -> str:
        prompt_str_input = self.prompt_template.format(
            description=self.description, input=input, role=self.role
        )
        # print("输入的提示词字符串：", prompt_str_input)
        # output_completion: AIMessage = self.chat_model.invoke(input=prompt_str_input)
        # print("chatModel输出内容：", output_completion.content.strip())
        result = self.invoke(user_input=prompt_str_input)
        # print("retriever_chain输出内容：", result.strip())
        # 返回retriever链结果
        return result
