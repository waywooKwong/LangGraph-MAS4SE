"""
20240801 代码说明-邝伟华

这次我加入 Bot02 进行 Duty_Classfier 的测试，
为了提高测试效率，我暂时注释掉了 Robot001 以及 model_role 的相关生成
请留意
"""

"""
20240802 代码说明-邝伟华
手动将 Bot02 代码合并
有关 Bot02 的代码我尽量都标注了 Bot02

注意此处我们定义的 
-Robot01: 获取项目需求说明书
-Bot02: 对话一轮结束后根据用户反馈进行职责划分
"""
"""
20240807 王璞
添加to_strict_json和convert_newline_escape规范json格式的函数
在/ask中添加一条语句     answer = convert_newline_escape(answer)保证markdown格式可以正确传入前端
"""
import asyncio
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

# Ollama model 接入
from langchain_community.chat_models import ChatOllama
from Class_04_OllamaCustomMade import OllamaCustomMade

# 文档总结
from Class_06_MessagesSum import MessagesSum

# Robot001 与客户经理对接需求文档说明书
from Robot001 import RobotAgent

# Bot2 是第二次与客户对接的 职责分配机器人
from Bot_02_DutyClassifier import DutyClassifier

# 0 - 前端响应传送 json 字符串，保存到文件夹中
from frontend_json_process import CLASS_JointPlus_jsonprocess
from ModelChoise import Model
from fastapi.responses import StreamingResponse
from typing import AsyncIterable
from Class_01_PromptGenerator import PromptGenerator
import json

Model.os_setenv()


class AgentState(TypedDict):
    sender: str
    progress: str
    messages: Annotated[List[BaseMessage], operator.add]


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
        # Ollama 角色定制是否启动, 图节点对于角色定制的添加
        ## 关联line: model_role = BuildChainAgent(role=role, duty=duty)
        self.OllamaCustomMade = False
        self.OllamaModelName = None

        # 将提示词生成器单独导出
        self.prompt_creatation = PromptGenerator()
        self.conversation_finished = False  # 标志对话是否完成
        self.initial_question = HumanMessage(content="", name="user")
        # self.showButton = False
        # self.user_is_satisfy = False
        self.file_uploaded = False
        # 客服机器人的回答
        self.answer = ""
        # 是否完成角色创建
        self.is_role = False

        # Rob02: hasRequest, userRequest
        self.hasRequest = False
        self.userRequest = "我的需求已满足, 请直接退出, 返回 'Finish'"

        # 收集最终的 state 总结获得文档(.md)
        self.final_state: AgentState = None
        # 文件保存
        self.messageSum = MessagesSum()

        # 角色定制模板
        self.promptList = []

        self.agent = RobotAgent()

    def set_path(self, new_path):
        self.path = new_path

    def get_path(self):
        return self.path

    def set_conversation_finished(self, finished: bool):
        self.conversation_finished = finished

    def is_conversation_finished(self):
        return self.conversation_finished

    ### Bot02
    def set_hasRequest(self, tnf: bool):
        self.hasRequest = tnf

    def hasRequest(self, tnf: bool):
        return self.hasRequest

    def set_userRequest(self, request):
        self.userRequest = request

    ###

    def is_OllamaCustonMade(self) -> bool:
        return self.OllamaCustomMade

    def set_OllamaCustomMade(self, tnf: bool):
        self.OllamaCustomMade = tnf

    def set_OllamaModelName(self, target_model):
        self.OllamaModelName = target_model

    #   为生成最终的文本
    def set_state(self, state: AgentState):
        self.final_state = state

    def set_state(self, state: AgentState):
        self.final_state = state


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
    ### Bot02 反馈进来之后, 模型的生成效果 - 20240806 - weihua
    if state["sender"] == "Bot2":
        prompt = f"""请根据用户反馈的修改意见:{default_config.userRequest}, 
                    修改你最近的一次反馈内容:{state["messages"]}"""
        print("prompt 是根据用户的反馈内容对最近一次反馈进行修改")
    ###
    else:
        prompt = last_message.content
        print("prompt:", prompt)

    ### 两种构建的选择
    if default_config.is_OllamaCustonMade() == True:
        response = chat_model.invoke(prompt)
        response = response.content
    else:
        response = chat_model.process(input=prompt)
    ai_message_content = response
    ### Rob02
    # test_model = default_config.chat_model
    # response = test_model.invoke(prompt)
    ###
    # print("response:",response)
    # ai_message_content = response.content
    # print("ai_message_content:", ai_message_content)

    print(node_name, "func_node answer:", ai_message_content)
    result = AIMessage(name=node_name, content=ai_message_content)
    # fun_node 中及时存储 state
    state: AgentState = {
        "sender": node_name,
        "progress": state["progress"],
        "messages": state["messages"] + [result],
    }
    default_config.set_state(state=state)
    return state


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
    ### 20240806 LangGraph 底层逻辑的缺陷？自动补齐
    members = list(conditional_map.keys())
    if "ProjectManager" in members:
        members.remove("ProjectManager")
    if sender in members:
        members.remove(sender)
    print("next members:", members)

    ### Bot02
    duty_description = {}
    json_file_path = default_config.get_path()
    for duty in members:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        for message in data["Message"]:
            if message["label_text"] == duty:
                description_text = message["description_text"]
                duty_description[duty] = description_text
    print("duty description:\n", duty_description)
    ### Bot02

    prompt_str_input_01 = prompt_template_01.format(members=members)
    llm = chat_model
    output_completion_01: AIMessage = llm.invoke(input=prompt_str_input_01)
    content_str = output_completion_01.content
    json_str = content_str.strip("```").replace("json\n", "").strip()
    json_data = json.loads(json_str)
    # print("json_data:", json_data)
    next_value = json_data["next"]
    print("next value:", next_value)
    if next_value in conditional_map.values():
        next_key = list(conditional_map.keys())[list(conditional_map.values()).index(next_value)]
    else:
        next_key = "Finish"
    print("next key:", next_key)
    return next_key


# 客服机器人 Bot2 特定的结点内部函数
def func_node_Bot02(state: AgentState) -> AgentState:
    result = AIMessage(
        name="Bot02",
        content="您好, 我是客服机器人Bot2, 我已将您的意见反馈, 请等待反馈结果",
    )
    # 及时存储 state
    state: AgentState = {
        "sender": "Bot02",
        "progress": state["progress"],
        "messages": state["messages"] + [result],
    }
    default_config.set_state(state=state)
    return state


# 前端定义 ChatView 中定义的新的 clientUserRequest
# 这里在最终 graph 的流式输出中留有 10s 间隔释放给用户输入
@app.websocket("/ws/userRequest")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            print("/ws/userRequest is for Bot02-userRequest!")
            request = await websocket.receive_text()
            response = {"message": f"User request received: {request}"}
            default_config.set_userRequest(request)
            default_config.set_hasRequest(tnf=True)
            print("ws/userRequest 接收到用户修改意见\n", default_config.userRequest)
            await websocket.send_text(json.dumps(response))  # 发送响应回前端
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")


def supervisor_chain_Bot02(state: AgentState, conditional_map: Dict[str, Any]):
    print("enter superviosr_chain_Bot02")
    duty_classifier = list(conditional_map.keys())
    print("duty classifier:\n", duty_classifier)
    duty_description = {}
    json_file_path = default_config.get_path()
    for duty in duty_classifier:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        for message in data["Message"]:
            if message["label_text"] == duty:
                description_text = message["description_text"]
                duty_description[duty] = description_text
    print("duty description:\n", duty_description)

    import time

    if not default_config.hasRequest:
        print("Bot02 没有接收到反馈, while continue")
        time.sleep(3)

    input_request = default_config.userRequest
    print("get userRequest:", input_request)
    # input_request = "请调整一下 QA2 的工作"
    classifier_bot = DutyClassifier(
        duty_classifiers=duty_classifier, duty_description=duty_description
    )
    classifier_result = classifier_bot.topic_classifier(input_request)
    next_value = classifier_result["classifier"]
    if next_value in conditional_map.values():
        next_key = list(conditional_map.keys())[list(conditional_map.values()).index(next_value)]
    else:
        next_key = "Finish"
    print("Bot2 next key:", next_key)
    # 恢复默认
    default_config.set_userRequest("我的需求已满足, 请直接退出, 返回 'Finish'")
    default_config.set_hasRequest(tnf=False)
    return next_key


class QueryRequest(BaseModel):
    query: str


import re


# 处理部分json格式解析错误
def to_strict_json(json_str):
    json_str = json_str.strip()
    json_str = json_str.strip("`")
    json_str = json_str.strip("json")
    # 替换换行符和回车符为 JSON 兼容的转义字符
    json_str = json_str.replace('\r\n', "\\n").replace('\n', "\\n")
    json_str = json_str.strip("\\n")
    json_str = json_str.strip("{")
    json_str = json_str.strip("}")
    json_str = json_str.strip("\\n")
    json_str = json_str.strip()
    json_str = f"{{{json_str}}}"
    json_str = json_str.replace('\\', "\\\\")
    json_str = re.sub(r'\\\\n', '\\n', json_str, count=2)

    # 确保 JSON 字符串有效

    # 转换为严格的 JSON 格式
    return json_str


def convert_newline_escape(json_str):
    """将字符串中的 '\\n' 转换为实际的换行符 '\n'"""
    # 替换字符串中的 '\\n' 为 '\n'
    return json_str.replace('\\n', '\n')


# 多模态对话
@app.post("/ask")
async def ask(request: QueryRequest):
    try:
        response = default_config.agent.invoke(input=request.query)
        print(response)
        cleaned_json_string = to_strict_json(response)

        response_dict = json.loads(cleaned_json_string)
        sender = response_dict.get("sender", "字段不存在")
        progress = response_dict.get("progress", "字段不存在")
        answer = response_dict.get("answer", "字段不存在")
        answer = convert_newline_escape(answer)
        default_config.answer = answer
        print("\n解析结果:")
        print(f"sender: {sender}")
        print(f"progress: {progress}")
        print(f"answer: {answer}")

        # 返回正常响应
        return JSONResponse({"sender": sender, "progress": progress, "message": answer})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 接收json
@app.post("/upload-agent")
async def upload_agent(file: UploadFile = File(...)):
    if not default_config.is_conversation_finished():
        return JSONResponse(
            content={"error": "Conversation is not finished yet"}, status_code=400
        )

    try:
        file_content = await file.read()
        data = json.loads(file_content)
        print("Received JSON data:", data)
        simplified_json_path = (
            CLASS_JointPlus_jsonprocess.extract_data_to_simplified_json(data)
        )
        default_config.set_path(simplified_json_path)
        # 将判断json文件是否上传置为true
        default_config.file_uploaded = True
        print("成功解析为json:", default_config.get_path())
        # Initialize the workflow and run it

        return JSONResponse(content={"message": "JSON received successfully"})
    except Exception as e:
        print("Error:", e)
        return JSONResponse(content={"error": "An error occurred"}, status_code=500)


# 定义 POST 路由来接收 /OllamaMade 请求，实现选择定制Ollama模型
class ModelRequest(BaseModel):
    model: str


@app.post("/OllamaMade")
async def receive_model(request: ModelRequest):
    try:
        model_name = request.model
        default_config.set_OllamaCustomMade(tnf=True)
        default_config.set_OllamaModelName(target_model=model_name)
        print("config OllamaCustomMade:", default_config.OllamaCustomMade)
        print("config OllamaModelName:", default_config.OllamaModelName)
        print("====")
        print("notice: 请确保已经启动 ollama serve !")

        # 返回响应给前端
        return JSONResponse(
            content={"message": "Model received successfully", "model": model_name}
        )
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="An error occurred")


@app.websocket("/ws/stream")
async def initialize_workflow(websocket: WebSocket):
    await websocket.accept()
    # 如果json文件没有上传
    if not default_config.file_uploaded:
        print("No json uploaded yet.")
        return

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
    roles = []
    for message in data["Message"]:
        label_text = message["label_text"]
        if (
                label_text != "Bot2"
                and label_text.lower() != "start"
                and label_text.lower() != "end"
        ):
            roles.append(label_text)

    await websocket.send_text(json.dumps({"roles": roles}, ensure_ascii=False))
    # 提取 message 部分信息并添加结点
    for message in data["Message"]:
        label_text = message["label_text"]
        description_text = message["description_text"]
        # "start" "end" 特殊处理
        if label_text.lower() != "start" and label_text.lower() != "end":

            # 如果 label_text == "Bot2"，构造 conditional_map
            if label_text == "Bot2" or label_text == "Bot02":
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
                role = label_text
                duty = description_text
                print("OllamaCustonMade? ", default_config.is_OllamaCustonMade())

                ### 角色定制逻辑在这里实现:
                ## 1. Ollama 直接 model system prompt 进行模型级的定制
                if default_config.is_OllamaCustonMade() == True:
                    # "/OllamaMade" 响应触发 Ollama 定制运行
                    # 01. 这是从零生成 定制 Ollama 开源模型
                    # OllamaBuild = OllamaCustomMade(
                    #     model_name=default_config.OllamaModelName, role=role, duty=duty
                    # )
                    # model_role = OllamaBuild.get_ChatOllama()
                    
                    # 02. 这是已经生成好 Ollama 直接拿模型运行的规程
                    custom_model_name = role + '-' + default_config.OllamaModelName
                    print(f"make sure custom model:{custom_model_name} exists")
                    model_role = ChatOllama(model=custom_model_name)
                    #
                    ollama_message = f"Ollama is auto-generating {role} by {default_config.OllamaModelName}, please waiting ~"
                    await websocket.send_text(
                        json.dumps(
                            {"message": ollama_message, "role": role},
                            ensure_ascii=False,
                        )
                    )
                else:
                    ## 2. BuildChainAgent 常规流程
                    # 注意: 类 BuildChainAgent 中查看 load_documents 文件爬取角色文本为提高加载效率默认关闭
                    description = ""
                    for chunk in default_config.prompt_creatation.generate_prompt(
                            role=role, duty=duty
                    ):
                        await asyncio.sleep(0.1)  # 模拟延迟
                        description += chunk
                        await websocket.send_text(
                            json.dumps(
                                {"message": chunk, "role": role}, ensure_ascii=False
                            )
                        )
                    # print(description)
                    default_config.promptList.append(description)

                    model_role = BuildChainAgent(
                        role=role, duty=duty, description=description
                    )
                ###
                print(f"{role} for model_role:\n{model_role}")
                workflow.add_node(
                    role,
                    partial(func_node, node_name=role, chat_model=model_role),
                )

    for source_label, targets in link_edges.items():
        print("====")
        print('source_label: ', source_label)
        print('targets: ', targets)
        print('====')
        if source_label.lower() == "start":
            print(f"add edge: START, {targets[0]}")
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
                print("Bot2 conditional_map:", conditional_map)
                print("----")
                workflow.add_conditional_edges(
                    source_label,
                    lambda state: supervisor_chain_Bot02(state, conditional_map),
                    conditional_map,
                )
                print("Bot2 conditional_map(after):", conditional_map)
            else:
                # 20240801 含Bot2的示例删除反馈边的添加逻辑
                # members = [value for value in conditional_map.values() if value != END]
                # for member in members:
                #     workflow.add_edge(member, source_label)
                print("----")
                print("supervisor chain:", source_label)
                print("source label:", source_label)
                print("supervisor chain conditional_map:", conditional_map)
                print("----")
                workflow.add_conditional_edges(
                    source_label,
                    lambda state: supervisor_chain(state, conditional_map),
                    conditional_map,
                )
                print("supervisor chain conditional_map(after):", conditional_map)

        else:
            target_label = targets[0]
            if target_label.lower() == "end":
                workflow.add_edge(source_label, END)
                print(f"add edge: {source_label}, END")
            else:
                workflow.add_edge(source_label, target_label)
                print(f"add edge:{source_label}, {target_label}")

    # 将default_config.file_uploaded复原
    print("图创建成功!!!!!!!!!!!!!!!")
    default_config.file_uploaded = False
    default_config.is_role = True
    await websocket.send_text(
        json.dumps({"success": default_config.is_role}, ensure_ascii=False)
    )
    print("default_config.is_role:", default_config.is_role)
    print("initial_workflow 角色生成完成")
    # 保存模板
    default_config.messageSum.sum_prompt_to_file(default_config.promptList)
    print("模板保存成功")


@app.websocket("/ws/run_workflow")
async def websocket_run_workflow(websocket: WebSocket):
    await websocket.accept()
    print("如果需要 Ollama 定制, 请使用按钮选择源模型")
    try:
        # 如果所有角色没有创建成功
        if not default_config.is_role:
            print("角色尚未创建成功")
            # await websocket.send_text(json.dumps({"error": "No json uploaded yet"}))
            return

        await run_workflow_and_send_updates(websocket)
        final_state = default_config.final_state
        final_state_messages = final_state["messages"]

        default_config.messageSum.sum_message_to_file(messages=final_state_messages)
        print("workflow run end!")
        await websocket.send_text(
            json.dumps(
                {"message": "Work Finished! Please checkout ", "role": "Bot2"}, ensure_ascii=False
            )
        )

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        await websocket.send_text(json.dumps({"error": str(e)}))


async def run_workflow_and_send_updates(websocket: WebSocket):
    # initialize_workflow()
    graph = workflow.compile()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    workflow_graph_path = f"src/workflow_graph/workflow_graph_{timestamp}.png"
    save_graph_image(graph, workflow_graph_path)
    print("需求说明书：", default_config.initial_question)
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

        ### Bot02: 留下释放的时间, 给用户进行输入
        await websocket.send_text(
            json.dumps(
                {
                    "sender": "kuangweihua",
                    "progress": "userRequest",
                    "message": "随时提出修改意见",
                },
                ensure_ascii=False,
            )
        )
        await asyncio.sleep(10)  # Add 3-second delay


class ButtonClick(BaseModel):
    message: str


# 用户确认
@app.post("/button-clicked")
async def handle_button_click(button_click: ButtonClick):
    try:
        # 打印接收到的消息
        print(f"/button-clicked Received message from client: {button_click.message}")

        # 可以根据需要进行更多处理
        default_config.conversation_finished = True

        default_config.initial_question = HumanMessage(
            content="请你根据以下需求说明书完成你的工作并向下属分配工作"
                    + default_config.answer,
            name="bot",
        )
        print(default_config.initial_question)

        # 返回成功的响应
        return {"status": "success", "received_message": button_click.message}
    except Exception as e:
        # 捕获异常并返回错误响应
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


class NewChat(BaseModel):
    message: str


# 新建对话
@app.post("/create_newChat")
async def handle_button_click(create_newchat: NewChat):
    try:
        # 打印接收到的消息
        print(f"/create_newChat Received message from client: {create_newchat.message}")

        # 可以根据需要进行更多处理
        default_config.OllamaCustomMade = False
        default_config.OllamaModelName = None
        default_config.conversation_finished = False  # 标志对话是否完成
        default_config.initial_question = HumanMessage(content="", name="user")
        # self.showButton = False
        # self.user_is_satisfy = False
        default_config.file_uploaded = False
        # 客服机器人的回答
        default_config.answer = ""
        # 是否完成角色创建
        default_config.is_role = False

        # Rob02: hasRequest, userRequest
        default_config.hasRequest = False
        default_config.userRequest = "我的需求已满足, 请直接退出, 返回 'Finish'"

        # 收集最终的 state 总结获得文档(.md)
        default_config.final_state = None
        # 文件保存
        default_config.messageSum = MessagesSum()

        default_config.agent = RobotAgent()

        # 角色定制模板
        default_config.promptList = []
        print("=====================================================")
        print("新建对话成功!!!!!")

        # 返回成功的响应
        return {"status": "success", "received_message": create_newchat.message}
    except Exception as e:
        # 捕获异常并返回错误响应
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
