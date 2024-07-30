from diffusers import StableDiffusionPipeline
import torch
from fastapi import FastAPI, HTTPException, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains.retrieval_qa.base import RetrievalQA
from demo_prepared.ModelChoise.modelchoise import get_zhipuai_chat_model

from typing import List
from fastapi.responses import StreamingResponse
from io import BytesIO
import os
from fastapi.responses import StreamingResponse, JSONResponse

# Initialize Stable Diffusion pipeline
model_id = "D:\\MyMOdel\\stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

# Initialize FastAPI app
app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# System variable settings



# Define request model
class QueryRequest(BaseModel):
    query: str


# Define request model for image generation
class ImageRequest(BaseModel):
    prompt: str
    num_images: int = 1


# Load documents
def process_uploaded_file(file_path: str):
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        return loader.load()
    elif file_path.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
        return loader.load()
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
        return loader.load()
    else:
        raise HTTPException(status_code=400, detail="文件类型不支持！！！")


base_dir = 'D:/WorkSpace/Pycharm/Langchain_Final/Python/demo_prepared/src/mydocuments'
documents = []
for filename in os.listdir(base_dir):
    file_path = os.path.join(base_dir, filename)
    try:
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
            documents.extend(loader.load())
        elif filename.endswith(".txt"):
            loader = TextLoader(file_path)
            documents.extend(loader.load())
    except Exception as e:
        print(f"Error loading {filename}: {e}")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"../mydocuments/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    # Process the uploaded file
    try:
        new_documents = process_uploaded_file(file_location)
        documents.clear()  # Clear existing documents
        documents.extend(new_documents)
        # print(documents)
        chunked_new_documents = text_splitter.split_documents(documents=new_documents)

        # Recreate the vector store with new documents
        global vectorstore
        vectorstore = Qdrant.from_documents(
            documents=chunked_new_documents,
            embedding=embeddings,
            location=":memory:",
            collection_name="my_documents"
        )

        return {"filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Document splitting
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=1)
chunked_documents = text_splitter.split_documents(documents=documents)

# Vector database storage
EMBEDDING_DEVICE = "cpu"
embeddings = HuggingFaceEmbeddings(model_name="D:/WorkSpace/Pycharm/pythonProject/m3e-base",
                                   model_kwargs={'device': EMBEDDING_DEVICE})
vectorstore = Qdrant.from_documents(
    documents=chunked_documents,
    embedding=embeddings,
    location=":memory:",
    collection_name="my_documents"
)

from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate

# Generate LLM chat model
chat_model = get_zhipuai_chat_model()
retriever = vectorstore.as_retriever()
# Generate ChatModel session prompt messages
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user",
     "Given the above conversation, generate a search query to look up in order to get information relevant to the "
     "conversation.")
])
retriever_chain = create_history_aware_retriever(chat_model, retriever, prompt)
# Continue retrieval, remember retrieved documents, etc.
prompt = ChatPromptTemplate.from_messages([
    ("system", "Please prioritize the provided document information when answering the user's questions:\n\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

documents_chain = create_stuff_documents_chain(chat_model, prompt)
retriever_chain = create_retrieval_chain(retriever_chain, documents_chain)
from langchain_core.messages import HumanMessage, AIMessage

from langchain_community.agent_toolkits.load_tools import load_tools
from langchain import hub
from langchain.agents import (
    create_openai_functions_agent,
    initialize_agent,
    AgentType,
    AgentExecutor,
)

# Initialize custom tool
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import Tool


class RetrieverTool(Tool):
    def __init__(self, chain):
        self.chain = chain

    def run(self, query):
        response = self.chain.invoke(query)
        return response["answer"]


def retriever_tool_instance(query):
    return retriever_chain.invoke({
        "chat_history": chat_history,
        "input": query,
    })["answer"]


retriever_tool = Tool(
    name="retriever_chain",
    description="这个工具是专门分析用户上传文件的，当用户问到上传文档相关问题是，必须使用此工具！！！",
    func=retriever_tool_instance,
)

# Simulate a historical session record
chat_history = [
    HumanMessage(content="《让子弹飞》是什么时候在大陆上映的"),
    AIMessage(content="《让子弹飞》的大陆上映时间是2010年12月16日")
]

# Select the main tool as Tavily - a search engine.
from langchain_community.tools.tavily_search import TavilySearchResults

search = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    # include_domains = []
    # exclude_domains = []
    # include_answer = False
    # include_raw_content = False
    # include_images = True
)
tool = load_tools(tool_names=["llm-math"], llm=chat_model)

# If we want, we can create other tools.
# Once we have all the tools we want, we can put them in a list that we will reference later.

# Initialize Agent
tools = [retriever_tool, search] + tool
agent = initialize_agent(
    tools=tools,
    llm=chat_model,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True

)


# instructions = """You are an assistant,You must always use the provided tool to answer any question."""
# base_prompt = hub.pull("langchain-ai/openai-functions-template")
# prompt = base_prompt.partial(instructions=instructions)
#
# agent = create_openai_functions_agent(chat_model, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
@app.post('/upload-agent')
async def upload_agent(request: Request):
    try:
        # 获取 JSON 数据
        data = await request.json()

        # 打印接收到的 JSON 数据
        print('Received JSON data:', data)

        # 返回成功响应
        return JSONResponse(content={'message': 'JSON received successfully'})
    except Exception as e:
        # 打印错误并返回错误响应
        print('Error:', e)
        return JSONResponse(content={'error': 'An error occurred'}, status_code=500)


@app.post("/ask")
async def ask(request: QueryRequest):
    try:
        response = agent.invoke({
            "input": request.query,
            "chat_history": chat_history,
        })
        chat_history.append(HumanMessage(content=request.query))
        chat_history.append(AIMessage(content=response["output"]))
        print(response["output"])
        return JSONResponse({"response": response["output"]})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate_image")
async def generate_image(request: ImageRequest):
    try:
        # Generate images using Stable Diffusion
        image_urls = []
        for i in range(request.num_images):
            image = pipe(request.prompt).images[0]
            image_io = BytesIO()
            image.save(image_io, format="PNG")
            image_io.seek(0)
            image_id = f"generated_image_{i + 1}"
            app.state.images[image_id] = image_io
            image_urls.append(f"/images/{image_id}")
        return {"image_urls": image_urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/images/{image_id}")
async def get_image(image_id: str):
    image_io = app.state.images.get(image_id)
    if not image_io:
        raise HTTPException(status_code=404, detail="Image not found")
    return StreamingResponse(image_io, media_type="image/png")


@app.on_event("startup")
async def startup_event():
    app.state.images = {}


@app.on_event("shutdown")
async def shutdown_event():
    app.state.images.clear()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
