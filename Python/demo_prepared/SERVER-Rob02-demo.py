"""
20240801 代码说明-邝伟华

这次我加入 Bot02 进行 Duty_Classfier 的测试，
为了提高测试效率，我暂时注释掉了 Robot001 以及 role_model 的相关生成
请留意
"""

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

# Robot001 与客户经理对接需求文档说明书
from Robot001 import RobotAgent

# Bot2 是第二次与客户对接的 职责分配机器人
from Bot_02_DutyClassifier import DutyClassifier

# 0 - 前端响应传送 json 字符串，保存到文件夹中
from frontend_json_process import CLASS_JointPlus_jsonprocess
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
        self.path = "frontend_json_process/json_simplified_with_bot02.json"
        self.json_file_path = "frontend_json_process/json_simplified_with_bot02.json"
        self.chat_model = Model.get_zhupuai_model()
        self.conversation_finished = True  # 标志对话是否完成
        self.initial_question = HumanMessage(content="请设计一个银行管理系统")

    def set_path(self, new_path):
        self.path = new_path

    def get_path(self):
        return self.path

    def set_conversation_finished(self, finished: bool):
        self.conversation_finished = finished

    def is_conversation_finished(self):
        return self.conversation_finished


class AgentState(TypedDict):
    sender: str
    progress: str
    messages: Annotated[List[BaseMessage], operator.add]


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


# 保存 workflow_image 图像
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


# 结点内部函数
def func_node(state: AgentState, node_name, chat_model) -> AgentState:
    last_message = state["messages"][-1]
    # print("last_message:",last_message)
    # print("type of last_message",type(last_message))
    prompt = last_message.content
    # print("prompt:",prompt)
    # response = chat_model.process(input=prompt)
    # ai_message_content = response
    test_model = default_config.chat_model
    response = test_model.invoke(prompt)
    # print("response:",response)
    ai_message_content = response.content
    print("ai_message_content:", ai_message_content)

    print(node_name, "答案：", ai_message_content)
    result = AIMessage(name=node_name, content=ai_message_content)
    return {
        "sender": node_name,
        "progress": state["progress"],
        "messages": state["messages"] + [result],
    }


# 多边连接顺序遍历的 router 函数
def router_concurrent_choice(state: AgentState, members: Dict[str, Any]) -> str:
    visited_members = {
        message.name for message in state["messages"]
    }  # 获取已有的消息中已出现的成员名称
    member_order = list(members.keys())  # 按照角色顺序定义角色列表
    for member in member_order:  # 查找下一个未处理的成员
        if member not in visited_members:
            return member  # 返回下一个未处理的成员
    return "Finish"  # 如果所有成员都已访问过，则跳转到 'Finish'


# 通用的多边连接多选一 router 选择函数
def supervisor_chain(state: AgentState, conditional_map: Dict[str, Any]):
    print("enter supervisor_chain")
    # sender = state["messages"][-1]
    # sender = sender.name
    sender = state["sender"]
    print("sender before:", sender)
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

    # 创建成员列表，并移除发送者
    members = list(conditional_map.keys())
    # print("members before removing sender:", members)
    if sender in members:
        members.remove(sender)
    print("next members:", members)

    prompt_str_input_01 = prompt_template_01.format(members=members)
    llm = chat_model
    output_completion_01: AIMessage = llm.invoke(input=prompt_str_input_01)
    content_str = output_completion_01.content
    json_str = content_str.strip("```").replace("json\n", "").strip()
    json_data = json.loads(json_str)
    print("json_data:", json_data)
    next_value = json_data["next"]
    print("next value:", next_value)
    next_key = {v: k for k, v in conditional_map.items()}.get(next_value, "Finish")
    print("next key:", next_key)
    return next_key


# 客服机器人 Bot2 特定的结点内部函数
def func_node_Bot02(state: AgentState) -> AgentState:
    result = AIMessage(
        name="Bot02",
        content="您好, 我是客服机器人Bot2, 我已将您的意见反馈, 请等待反馈结果",
    )
    return {
        "sender": "Bot02",
        "progress": state["progress"],
        "messages": state["messages"] + [result],
    }


async def send_message_to_frontend(websocket: WebSocket, message: str):
    await websocket.send_text(json.dumps({"request": message}))


async def get_response_from_frontend(websocket: WebSocket) -> str:
    response = await websocket.receive_text()
    return json.loads(response).get("response", "")


#### 这里需要实现 向前端获取信息！
##### 函数调用的位置: line337 lambda state: supervisor_chain_Bot02(state, conditional_map),(注意参数?)
def supervisor_chain_Bot02(state: AgentState, conditional_map: Dict[str, Any]):
    # members 是分类的目标对象
    print("enter superviosr_chain_Bot02")
    duty_classifier = list(conditional_map.keys())
    duty_description = {}
    json_file_path = default_config.get_path()
    for duty in  duty_classifier:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        for message in data["Message"]:
            if message["label_text"] == duty:
                description_text = message["description_text"]
                duty_description[duty] = description_text
    print("duty description:",duty_description)
                
                

    # 获取前端的 “修改意见”
    # 向前端发送请求消息
    # await send_message_to_frontend(websocket, "请向 Bot2 反馈您的修改意见：")
    # # 等待从前端接收反馈
    # input_request = await get_response_from_frontend(websocket)
    input_request = "请向 Bot2 反馈您的修改意见"
    classifier_bot = DutyClassifier(duty_classifiers=duty_classifier)
    classifier_result = classifier_bot.topic_classifier(input_request)
    next_value = classifier_result["classifier"]
    print("Bot2 router next", next_value)
    next_key = {v: k for k, v in conditional_map.items()}.get(next_value, "Finish")
    print("Bot2 next key:", next_key)
    return next_key
    # return 'QA1'


# 定义 POST 路由来接收 /model 请求，实现选择模型
# 定义请求体模型
class ModelRequest(BaseModel):
    model: str


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


# Global variable to track if the file has been uploaded
file_uploaded = False


def initialize_workflow():
    # if not file_uploaded:
    #     print("No file uploaded yet.")
    #     return

    json_file_path = default_config.get_path()
    print("----")
    print("workflow json 加载路径:", json_file_path)
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    global workflow
    workflow = StateGraph(AgentState)

    # 处理 link 部分信息并添加边
    link_edges = {}
    for link in data["Link"]:
        source_label = link["source_label"]
        target_label = link["target_label"]

        # 统计每个 source_label 对应的 target_label 的数量
        if source_label not in link_edges:
            link_edges[source_label] = []
        link_edges[source_label].append(target_label)

    # 提取 message 部分信息并添加结点
    for message in data["Message"]:
        label_text = message["label_text"]
        description_text = message["description_text"]
        # "start" "end" 特殊处理
        if label_text.lower() != "start" and label_text.lower() != "end":
            role = label_text
            duty = description_text
            # model_role = BuildChainAgent(role=role, duty=duty)
            # 如果 label_text == "Bot2"，构造 conditional_map
            if label_text == "Bot2":
                # 找到 Bot2 对应的 targets
                bot2_targets = link_edges.get(label_text, [])
                print("----")
                print("Bot2 targets:", bot2_targets)
                print("----")
                if bot2_targets:
                    # 构造 conditional_map
                    conditional_map = {target: target for target in bot2_targets}
                    # 如果目标是 "End"，替换为 "Finish":"__end__"
                    if "End" in conditional_map:
                        conditional_map["Finish"] = "__end__"
                        del conditional_map["End"]
                    workflow.add_node("Bot2", func_node_Bot02)
            else:
                workflow.add_node(
                    label_text,
                    partial(func_node, node_name=label_text, chat_model=chat_model),
                )

    for source_label, targets in link_edges.items():

        if source_label.lower() == "start":
            workflow.add_edge(START, targets[0])

        elif len(targets) > 1:
            conditional_map = {target: target for target in targets}
            # 如果目标是 "End"，替换为 "Finish":"__end__"
            if "End" in conditional_map:
                conditional_map["Finish"] = "__end__"
                del conditional_map["End"]

            if source_label == "Bot2":
                print("----")
                print("func_node_Bot2 chain: Bot2")
                print("source label:", source_label)
                print("conditional_map:", conditional_map)
                print("----")
                workflow.add_conditional_edges(
                    source_label,
                    lambda state: supervisor_chain_Bot02(state, conditional_map),
                    conditional_map,
                )
            else:
                # 20240801 含Bot2的示例删除反馈边的添加逻辑
                members = [value for value in conditional_map.values() if value != END]
                # for member in members:
                #     workflow.add_edge(member, source_label)
                print("----")
                print("supervisor chain:", source_label)
                print("source label:", source_label)
                print("conditional_map:", conditional_map)
                print("----")
                workflow.add_conditional_edges(
                    source_label,
                    lambda state: supervisor_chain(state, conditional_map),
                    conditional_map,
                )

        else:
            target_label = targets[0]
            if target_label.lower() == "end":
                workflow.add_edge(source_label, END)
            else:
                workflow.add_edge(source_label, target_label)


@app.websocket("/ws/run_workflow")
async def websocket_run_workflow(websocket: WebSocket):
    await websocket.accept()
    try:
        # if not file_uploaded:
        #     await websocket.send_text(json.dumps({"error": "No file uploaded yet"}))
        #     return

        await run_workflow_and_send_updates(websocket)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        await websocket.send_text(json.dumps({"error": str(e)}))


async def run_workflow_and_send_updates(websocket: WebSocket):
    initialize_workflow()
    graph = workflow.compile()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    workflow_graph_path = f"src/workflow_graph/workflow_graph_{timestamp}.png"
    save_graph_image(graph, workflow_graph_path)
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
        print("here is recent_message")
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


class QueryRequest(BaseModel):
    query: str


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
            default_config.initial_question = HumanMessage(
                content="请项目经理根据以下需求说明文档完成你的职责" + response
            )
            return JSONResponse({"response": "对话已结束，感谢使用！"})

        # 返回正常响应
        return JSONResponse({"response": response})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-agent")
async def upload_agent(file: UploadFile = File(...)):
    if not default_config.is_conversation_finished():
        return JSONResponse(
            content={"error": "Conversation is not finished yet"}, status_code=400
        )

    global file_uploaded
    try:
        file_content = await file.read()
        data = json.loads(file_content)
        print("Received JSON data:", data)
        simplified_json_path = (
            CLASS_JointPlus_jsonprocess.extract_data_to_simplified_json(data)
        )
        default_config.set_path(simplified_json_path)
        file_uploaded = True
        print("成功解析为json:", default_config.get_path())

        # Initialize the workflow and run it
        return JSONResponse(content={"message": "JSON received successfully"})
    except Exception as e:
        print("Error:", e)
        return JSONResponse(content={"error": "An error occurred"}, status_code=500)


# 备用测试 websocket 连通的响应函数
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
