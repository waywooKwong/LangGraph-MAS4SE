import operator
import os
import json
import datetime
from functools import partial
from typing import Dict, List, Annotated, Any, TypedDict
from langgraph.graph import END, StateGraph, START
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_core.prompts import PromptTemplate
from starlette.websockets import WebSocketDisconnect, WebSocket

from demo_prepared.ModelChoise.modelchoise import get_zhipuai_chat_model

from 用户定制001 import BuildChainAgent
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

# 设置模型和环境变量

chat_model = get_zhipuai_chat_model()
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "wangpu_test"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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"

# 初始化角色
# role1 = "项目经理"
# role2 = "开发工程师1"
# role3 = "开发工程师2"
# duty1 = f"分析用户需求，向{role2}和{role3}分配任务"
# duty2 = f"完成{role1}分配的任务中属于自己的那一部分,生成详细的前后端架构图，前端采用vue架构"
# duty3 = f"完成{role1}分配的任务中属于自己的那一部分,生成数据库的设计，与sql代码"
# model_role1 = BuildChainAgent(role=role1, duty=duty1)
# model_role2 = BuildChainAgent(role=role2, duty=duty2)
# model_role3 = BuildChainAgent(role=role3, duty=duty3)
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


class QueryRequest(BaseModel):
    query: str


class AgentState(TypedDict):
    sender: str
    progress: str
    messages: Annotated[List[BaseMessage], operator.add]


initial_question = HumanMessage(content="请设计一个银行管理系统")


def save_graph_image(graph, file_path):
    from PIL import Image as PILImage
    import io
    try:
        image_data = graph.get_graph(xray=True).draw_mermaid_png()
        image = PILImage.open(io.BytesIO(image_data))
        image.save(file_path)
        print(f"图像已保存为 {file_path}")
    except Exception as e:
        print(f"保存图像失败: {e}")


def func_node(state: AgentState, node_name, chat_model) -> AgentState:
    last_message = state["messages"][-1]
    prompt = last_message.content
    response = chat_model.process(input=prompt)
    ai_message_content = response
    # print(node_name, "答案：", ai_message_content)
    result = AIMessage(name=node_name, content=ai_message_content)
    return {
        "sender": node_name,
        "progress": state["progress"],
        "messages": state["messages"] + [result],
    }


import httpx


def router_concurrent_choice(state: AgentState, members: Dict[str, Any]) -> str:
    # 获取已有的消息中已出现的成员名称
    visited_members = {message.name for message in state["messages"]}

    # 按照角色顺序定义角色列表
    member_order = list(members.keys())

    # 查找下一个未处理的成员
    for member in member_order:
        if member not in visited_members:
            return member  # 返回下一个未处理的成员

    # 如果所有成员都已访问过，则跳转到 'Finish'
    return "Finish"


# def process_technology(state: AgentState, members: Dict[str, Any]) -> AgentState:
#     # 发送消息到 QA1 和 QA2
#     for member in members.keys():
#         state["messages"].append(HumanMessage(content=f"发送消息到 {member}"))
#     return state
json_file_path = ("D:/WorkSpace/Pycharm/Langchain_Final/Python/demo_prepared/frontend_json_process/frontend"
                  "-0729_simpified.json")
with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

workflow = StateGraph(AgentState)

# 提取 message 部分信息并添加结点
for message in data['Message']:
    label_text = message['label_text']
    description_text = message['description_text']
    # "start" "end" 特殊处理
    if label_text.lower() != "start" and label_text.lower() != "end":
        role = label_text
        duty = description_text
        model_role = BuildChainAgent(role=role, duty=duty)
        workflow.add_node(label_text, partial(func_node, node_name=label_text, chat_model=model_role))

# 处理 link 部分信息并添加边
link_edges = {}
for link in data['Link']:
    source_label = link['source_label']
    target_label = link['target_label']

    # 统计每个 source_label 对应的 target_label 的数量
    if source_label not in link_edges:
        link_edges[source_label] = []
    link_edges[source_label].append(target_label)

# 添加边

for source_label, targets in link_edges.items():

    if source_label.lower() == "start":
        workflow.add_edge(START, targets[0])

    elif len(targets) > 1:
        conditional_map = {target: target for target in targets}
        conditional_map["Finish"] = END
        print("----")
        print("conditional_map:", conditional_map)
        print("----")
        members = [value for value in conditional_map.values() if value != END]
        for member in members:
            workflow.add_edge(member, source_label)

        workflow.add_conditional_edges(source_label,
                                       lambda state: router_concurrent_choice(state, conditional_map),
                                       conditional_map)

    else:
        target_label = targets[0]
        if target_label.lower() == "end":
            workflow.add_edge(source_label, END)
        else:
            workflow.add_edge(source_label, target_label)

import datetime

graph = workflow.compile()
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
file_path = f"D:/WorkSpace/Pycharm/Langchain_Final/Python/demo_prepared/src/workflow_graph/workflow_graph_{timestamp}.png"
save_graph_image(graph, file_path)


# def serialize_initial_question() -> Dict[str, str]:
#     return {
#         "sender": "user",
#         "content": initial_question.content,
#     }
#
#
# # 使用时
# messages = [serialize_initial_question()]
#
#
def serialize_message(message: BaseMessage) -> Dict[str, str]:
    return {
        "sender": message.name,
        "content": message.content,
    }

import datetime

graph = workflow.compile()
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
file_path = f"src/workflow_graph/workflow_graph_{timestamp}.png"
save_graph_image(graph, file_path)
async def run_workflow_and_send_updates(websocket: WebSocket):

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
        # print("----")
        # print(round)
        # key = list(round.keys())
        # value = round.get(key[0])
        # print("----")
        # serialized_messages = [serialize_message(msg) for msg in value['messages']]
        # value['messages'] = serialized_messages
        # json_string = json.dumps(value, ensure_ascii=False, indent=2)
        # print("json_string:",json_string)
        # await websocket.send_text(json_string)
        print("----")
        keys = list(round.keys())
        first_key = keys[0]
        round_data = round[first_key]
        round_data_message = round_data["messages"]
        recent_message = round_data_message[-1]
        recent_content = recent_message.content
        print("content to front end:", recent_message.content)
        serialized_round = {
            "sender": round_data["sender"],
            "progress": round_data["progress"],
            "message": recent_content,
        }
        print("serialized_round:", json.dumps(serialized_round))
        await websocket.send_text(json.dumps(serialized_round,ensure_ascii=False))
        print("----")

# WebSocket endpoint for running the workflow
@app.websocket("/ws/run_workflow")
async def websocket_run_workflow(websocket: WebSocket):
    await websocket.accept()
    try:
        await run_workflow_and_send_updates(websocket)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        await websocket.send_text(json.dumps({"error": str(e)}))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
