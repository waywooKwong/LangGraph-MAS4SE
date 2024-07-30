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
from ModelChoise import modelchoise
from Class_02_BuildChainAgent import BuildChainAgent

chat_model = modelchoise.get_zhipuai_chat_model()
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "wangpu_test"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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"

from pydantic import BaseModel
from fastapi import (
    FastAPI,
    HTTPException,
    File,
    UploadFile,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")


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
    print(node_name, "答案：", ai_message_content)
    result = AIMessage(name=node_name, content=ai_message_content)
    return {
        "sender": node_name,
        "progress": state["progress"],
        "messages": state["messages"] + [result],
    }


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


#
# workflow = StateGraph(AgentState)
# conditional_map = {role2: role2, role3: role3, "Finish": END}
# members = [value for value in conditional_map.values() if value != END]
# print("members:", members)
# options = ["END"] + members
# print("options:", options)
#
# # 只允许从项目经理到开发工程师的单向边
# workflow.add_edge(START, role1)
# workflow.add_edge(role1, role2)  # 项目经理 -> 开发工程师1
# workflow.add_edge(role1, role3)  # 项目经理 -> 开发工程师2
#
# # 不允许开发工程师返回到项目经理
# # workflow.add_edge(role2, role1)  # 这行代码应被删除
# # workflow.add_edge(role3, role1)  # 这行代码应被删除
#
# # 设置节点及条件边
# workflow.add_node(role1, partial(func_node, node_name=role1, chat_model=model_role1))
# workflow.add_node(role2, partial(func_node, node_name=role2, chat_model=model_role2))
# workflow.add_node(role3, partial(func_node, node_name=role3, chat_model=model_role3))
# workflow.add_conditional_edges(role1, supervisor_chain, conditional_map)
#
# # 代码运行部分
# graph = workflow.compile()
# timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# file_path = f"workflow_graph_{timestamp}.png"
# save_graph_image(graph, file_path)
#
# events = graph.stream(
#     {
#         "sender": "__start__",
#         "progress": "initial",
#         "messages": [initial_question],
#         "next": "need to check",
#     },
#     {"recursion_limit": 10},
# )
#
# for round in events:
#     print("----")
#     print(round)
#     print("----")
#
json_file_path = "frontend_json_process/frontend-0729_simpified.json"
with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

workflow = StateGraph(AgentState)

# 提取 message 部分信息并添加结点
for message in data["Message"]:
    label_text = message["label_text"]
    description_text = message["description_text"]
    # "start" "end" 特殊处理
    if label_text.lower() != "start" and label_text.lower() != "end":
        role = label_text
        duty = description_text
        model_role = BuildChainAgent(role=role, duty=duty)
        workflow.add_node(
            label_text, partial(func_node, node_name=label_text, chat_model=model_role)
        )

# 处理 link 部分信息并添加边
link_edges = {}
for link in data["Link"]:
    source_label = link["source_label"]
    target_label = link["target_label"]

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
        # conditional_map["Finish"] = END
        print("----")
        print("conditional_map:", conditional_map)
        print("----")
        # members = [value for value in conditional_map.values() if value != END]
        # for member in members:
        #     workflow.add_edge(member, source_label)

        workflow.add_conditional_edges(
            source_label,
            lambda state: router_concurrent_choice(state, conditional_map),
            conditional_map,
        )

    else:
        target_label = targets[0]
        if target_label.lower() == "end":
            workflow.add_edge(source_label, END)
        else:
            workflow.add_edge(source_label, target_label)

import datetime


async def run_workflow_and_send_updates(websocket: WebSocket):
    graph = workflow.compile()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"src/workflow_graph/workflow_graph_{timestamp}.png"
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
        await websocket.send_text(json.dumps(round))


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
# graph = workflow.compile()
# timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# file_path = f"src/workflow_graph/workflow_graph_{timestamp}.png"
# save_graph_image(graph, file_path)

# # # 代码运行部分
# events = graph.stream(
#     {
#         "sender": "__start__",
#         "progress": "initial",
#         "messages": [initial_question],
#         "next": "need to check",
#     },
#     {"recursion_limit": 10},
# )

# for round in events:
#     print("----")
#     print(round)
#     print("----")
