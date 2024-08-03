from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from Class_01_PromptGenerator import PromptGenerator
from Class_02_BuildChainAgent import BuildChainAgent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的前端源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
prompt = PromptGenerator()

# def generate_prompt(role: str, duty: str) -> str:
#     generator = PromptGenerator()
#     description = ""
#     for chunk in generator.generate_prompt(role=role, duty=duty):
#         description += chunk
#         print(chunk, end="", flush=True)
#     return description
description = ""
roles = ["项目经理", "开发经理", "QA工程师","后端工程师"]
dutys = ["生成需求说明书", "生成软件架构", "生成测试样例","生成后端架构"]

import json
@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # 发送角色数据到前端
    await websocket.send_text(
        json.dumps({"roles": roles}, ensure_ascii=False)
    )
    global description

    # 模拟生成流式数据
    for role, duty in zip(roles, dutys):
        description = ""
        for chunk in prompt.generate_prompt(role=role, duty=duty):
            await asyncio.sleep(0.1)  # 模拟延迟
            description += chunk
            await websocket.send_text(
                json.dumps({"message": chunk, "role": role}, ensure_ascii=False)
            )
        print(description)
        # agent = BuildChainAgent(role=role, duty=duty, description=description)
        # print("角色定制成功！！！")
        # print(agent.process("你好"))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
