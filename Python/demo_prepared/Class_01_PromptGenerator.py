# -*- coding: utf-8 -*-
from ModelChoise import Model
from langchain_core.prompts import PromptTemplate
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing import AsyncIterable
"""
说明20240807晚上
在提示词部分稍作修改
"""
Model.os_setenv()
app = FastAPI()
class PromptGenerator:
    def __init__(self):
        # Model.os_setenv()
        self.chat_model = Model.get_zhupuai_model()
        self.prompt_template_str = ("""
        您是一个专业的提示词模板生成器。

        您的任务是根据我提供的角色{role}和职责描述{duty}，生成一份详细、高质量的prompt。这份prompt将用于构建角色在特定应用中的行为模型，使智能体能够准确完成该角色的工作任务。

        **Prompt格式要求：**

        1. **角色介绍**
           - 以角色名{role}开头。
           - 提供该角色的详细职位描述、工作职能、工作专长、工作任务、工作场景等。内容需要清晰分段，并根据实际情况进行详细描述。

        2. **职位描述**
           - 根据提供的职责描述{duty}生成该角色的工作内容。例如，对于‘项目经理’，描述可能是：“你是一名项目经理，负责制定项目计划、跟踪进度、协调团队沟通并管理项目风险。请提供如何处理项目延期、资源不足和团队冲突的策略。”

        3. **对话细节**
           - 在对话中，角色{role}和职责{duty}必须清晰明确。如果你是项目经理，那么在对话中应分析需求，选择合适的技术栈，并将任务分配给相关人员。
           - 分配任务时，明确接收任务的对象，比如：“开发经理，你好，这是我整理的需求，请完成以下任务：xxxxx（根据实际情况编写）。任务分配时不需要设置时间计划，而应设置任务的优先顺序。”

        4. **解决方案**
           - 当作为回答方时，直接提供解决方案，不重复提问者的任务，也不生成分析过程。例如，如果任务要求生成前端 Vue 架构，则直接生成架构和注释；如果任务要求生成后端接口文档，则直接生成文档。

        5. **对话口吻**
           - 对话过程中必须遵循角色设定，明确上下级关系，生成生动的对话口吻。

        6. **最终回答**
           - 生成的回答核心点必须围绕职责描述{duty}，并确保结果是中文。

        生成的prompt必须是字符串类型，并按需换行，以保持格式的清晰性。
        """)

    def generate_prompt(self, role: str, duty: str):
        prompt_template = PromptTemplate.from_template(template=self.prompt_template_str)
        prompt_str_input = prompt_template.format(role=role, duty=duty)

        # 使用流式输出
        for chunk in self.chat_model.stream(prompt_str_input):
            # print(chunk.content, end="|", flush=True)
            # print(chunk.content.strip())
            yield chunk.content.strip()


# agent=PromptGenerator()
#
# @app.get("/stream")
# async def stream_response():
#     return StreamingResponse(agent.generate_prompt(role="项目经理",duty="向下属分配任务"), media_type='text/plain')
#
# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host="0.0.0.0", port=8000)
