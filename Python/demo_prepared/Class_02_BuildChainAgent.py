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
import os
from langchain.agents import initialize_agent, AgentType, Tool

from langchain.chains import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder, ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import FAISS, Qdrant
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_community.agent_toolkits.load_tools import load_tools

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from ModelChoise import modelchoise
from Class_01_PromptGenerator import PromptGenerator
from Class_03_WebScratchRoleTxt import WebScratchRoleTxt

# from Python.demo_prepared.Class01_PromptGenerator import PromptGenerator

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def generate_prompt(role: str, duty: str) -> str:
    generator = PromptGenerator()
    description = ""
    for chunk in generator.generate_prompt(role=role, duty=duty):
        description += chunk
        print(chunk, end="", flush=True)
    return description


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

    def __init__(self, role: str, duty: str):
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
        self.chat_model = modelchoise.get_zhipuai_chat_model()
        
        self.docs = self.load_documents()
        
        self.embeddings = self.load_embeddings()
        self.vector_retriever = self.create_vector_retriever()
        self.retriever_chain = self.create_retriever_chain()
        self.chat_history = []
        self.description = generate_prompt(role=self.role, duty=self.duty)
        self.prompt_template_str = """
                    您的描述如下{description}\n
                    您有时候是单独一个人解决用户提出的问题\n
                    (重要)但是，大多数时候，您需要与伙伴合作解决问题\n
                    (非常重要)您需要清楚自身的职责与伙伴的技能与特长，相互提问，获得对方的回答或者提问{input}后，给出相应的提问或者最佳回答\n
                    (最重要!!!)如果你作为提问方:你必须且只能生成要分配的任务问题题干，其他多余的一切回答均不能生成!!!\n
                              如果你作为回答方:不要重复提问方发布的任务，也不要生成分析过程，直接逐个生成解决方案\n
                    (非常重要)您必须时时刻刻明确自身的角色{role},杜绝出现角色错乱的现象发生!!!!!!!!!!!!!!!!!!!!!
                    您能通过分析外界提供的基础信息\n
                    对于用户或者其他角色提出的需求 ‘{input}’ 做出最完美的回答\n
                    格式按需输出，可以是字符串，也可以是jason\n
                    回答均使用中文,回答口吻必须用“我”来回答,生成答案必须按需7换行\n
                    (警告！！！)回答时禁止重复上一轮的答案!!!
                    {format_instructions}"""
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
            partial_variables={"format_instructions": self.format_instructions},
        )

    def detect_encoding(self, file_path):
        import chardet
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)  # 读取文件的一部分来检测编码
        result = chardet.detect(raw_data)
        return result['encoding']
    
    def load_documents(self):
        # !!! 需要定制角色文本的时候再启动这部分代码，因为一直启动速度过慢
        # role_text_generator = WebScratchRoleTxt(role=self.role)
        # # role_text_generator.DuckDuckGo_search()
        # role_text_generator.GoogleSerper_search()
        # role_text_generator.Google_ScrapeUrls()
        # docs = []
        # file_path = role_text_generator.URL_Scraper_txt_path
        docs = []
        file_path = "src/role_txt/SoftwareBasicFlow.txt"
        encoding = self.detect_encoding(file_path)
        loader = TextLoader(file_path,encoding=encoding)
        docs.extend(loader.load())
        print(f"{self.role} role txt generate & load:",file_path)
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

    def invoke(self, user_input: str) -> str:
        # Invoke the retriever chain
        response = self.retriever_chain.invoke(
            {
                "input": user_input,
                "chat_history": self.chat_history,
            }
        )

        # Update chat history
        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=response))

        return response

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
