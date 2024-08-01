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
from Robot001 import RobotAgent

from ModelChoise import Model

Model.os_setenv()


class default_config:
    """
    函数运行的默认参数类
    在类中设定，然后根据实例化调用，
    解决了一些参数在函数中得到，但没法应用在类外的尴尬
    """

    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "wangpu_test"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] = (
        "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"
    )

    def __init__(self):
        self.path = None
        self.json_file_path = (
            "frontend_json_process/json_simplified/frontend-0729_simpified.json"
        )
        self.chat_model = Model.get_zhupuai_model()
        self.conversation_finished = False  # 标志对话是否完成
        self.initial_question = initial_question = HumanMessage(content="")

    def set_path(self, new_path):
        self.path = new_path

    def get_path(self):
        return self.path

    def set_conversation_finished(self, finished: bool):
        self.conversation_finished = finished

    def is_conversation_finished(self):
        return self.conversation_finished


default_config = default_config()
chat_model = default_config.chat_model

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


class AgentState(TypedDict):
    sender: str
    progress: str
    messages: Annotated[List[BaseMessage], operator.add]





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


# 节点内部函数
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
    visited_members = {
        message.name for message in state["messages"]
    }  # 获取已有的消息中已出现的成员名称
    member_order = list(members.keys())  # 按照角色顺序定义角色列表
    for member in member_order:  # 查找下一个未处理的成员
        if member not in visited_members:
            return member  # 返回下一个未处理的成员
    return "Finish"  # 如果所有成员都已访问过，则跳转到 'Finish'


# 定义请求体模型
class ModelRequest(BaseModel):
    model: str


# 定义 POST 路由来接收 /model 请求，实现选择模型
@app.post("/model")
async def receive_model(request: ModelRequest):
    try:
        # 从请求体中提取 model 数据
        model_data = request.model
        print("Received model:", model_data)

        # 处理 model 数据（这里可以根据需要进行处理）
        # ...

        # 返回响应给前端
        return JSONResponse(
            content={"message": "Model received successfully", "model": model_data}
        )
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="An error occurred")


##### 0 - 前端响应传送 json 字符串，保存到文件夹中
from frontend_json_process import CLASS_JointPlus_jsonprocess

# Global variable to track if the file has been uploaded
file_uploaded = False

agent = RobotAgent()


@app.post("/ask")
async def ask(request: QueryRequest):
    try:
        response = agent.invoke(input=request.query)
        print(response)

        # 检查对话是否结束
        if request.query == "满意":
            # 返回最后一次响应后，设置对话已结束标志
            print("满意")
            default_config.set_conversation_finished(True)
            default_config.initial_question = HumanMessage(content="请项目经理根据以下需求说明文档完成你的职责" + response)
            return JSONResponse({"response": "对话已结束，感谢使用！"})

        # 返回正常响应
        return JSONResponse({"response": response})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-agent")
async def upload_agent(file: UploadFile = File(...)):
    if not default_config.is_conversation_finished():
        return JSONResponse(content={"error": "Conversation is not finished yet"}, status_code=400)

    global file_uploaded
    try:
        file_content = await file.read()
        data = json.loads(file_content)
        print("Received JSON data:", data)
        simplified_json_path = CLASS_JointPlus_jsonprocess.extract_data_to_simplified_json(data)
        default_config.set_path(simplified_json_path)
        file_uploaded = True
        print("成功解析为json:", default_config.get_path())
        # Initialize the workflow and run it

        return JSONResponse(content={"message": "JSON received successfully"})
    except Exception as e:
        print("Error:", e)
        return JSONResponse(content={"error": "An error occurred"}, status_code=500)


def initialize_workflow():
    if not file_uploaded:
        print("No file uploaded yet.")
        return

    json_file_path = default_config.get_path()
    print("jason路径:", json_file_path)
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    global workflow
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
            conditional_map["Finish"] = END
            print("----")
            print("conditional_map:", conditional_map)
            print("----")
            members = [value for value in conditional_map.values() if value != END]
            for member in members:
                workflow.add_edge(member, source_label)

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


async def run_workflow_and_send_updates(websocket: WebSocket):
    initialize_workflow()
    graph = workflow.compile()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"demo_prepared\frontend_json_process\json_simplified\workflow_graph_{timestamp}.png"
    save_graph_image(graph, file_path)
    events = graph.stream(
        {
            "sender": "__start__",
            "progress": "initial",
            "messages": [default_config.initial_question],
            "next": "need to check",
        },
        {"recursion_limit": 10},
    )
    for round in events:
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
        await websocket.send_text(json.dumps(serialized_round, ensure_ascii=False))
        print("----")


@app.websocket("/ws/run_workflow")
async def websocket_run_workflow(websocket: WebSocket):
    await websocket.accept()
    try:
        if not file_uploaded:
            await websocket.send_text(json.dumps({"error": "No file uploaded yet"}))
            return

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
            data = await websocket.receive_text()  # 获取前端文本
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
