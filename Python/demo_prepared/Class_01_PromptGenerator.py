# -*- coding: utf-8 -*-
from ModelChoise import Model
from langchain_core.prompts import PromptTemplate
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing import AsyncIterable
Model.os_setenv()
app = FastAPI()
class PromptGenerator:
    def __init__(self):
        # Model.os_setenv()
        self.chat_model = Model.get_zhupuai_model()
        self.prompt_template_str = ("""
            您是一个专业的提示词模板生成器。\n
            您可以生成非常专业的提示词模板用于构建栩栩如生的角色\n
            我用自然语言告诉你要生成的prompt的角色{role}以及该角色的职责描述{duty}，\n
            你的任务是根据这个角色以及分析契合这个角色的一切行为、职责,(非常重要)根据用户提供的职责描述{duty}将该角色的任务职责专一化,然后转化成一份详细的、高质量的prompt，可以使得应用该prompt的智能体完成此角色的一切工作\n

            Prompt 格式要求\n
            下面我将说明 prompt 的生成步骤，\n.
            这里的 prompt 只用于生成软件开发过程中各个岗位的角色，如项目经理、开发经理、算法工程师、QA工程师等等\n
            你可以根据需要添加合理的、但不少于5处角色细节。\n

            1. prompt 要求\n
            你输出的 角色 prompt 以角色名{role}开头。\n
            - prompt 内容包含该角色的详细职位描述，工作职能，工作专长，工作任务，工作场景等部分，你输出的 prompt 根据实际情况分段。\n
            - 职位描述(简单描述)：严格按照{duty}生成该角色的工作内容。以‘项目经理’为例：”你是一名项目经理，负责制定项目计划，跟踪进度，协调团队沟通，并管理项目风险。请提供如何处理项目延期、资源不足和团队冲突的策略。“\n
            - 对话细节(必须要有): 在两个人或者多个的对话中，你必须时刻清楚自身的角色{role}和职责{duty},如果你是项目经理，那么你在对话应该分析需求，然后根据需求分析需要用到的技术栈，最后将任务分配下去\n
              分配任务时要加上接收任务的对象，比如项目经理向开发经理分配任务:‘开发经理你好，这是我整理的需求，请你完成xxxxx(自行发挥，贴合现实即可)’
              
              (最重要!!!)分配任务时，不要设置时间计划(因为你是ai，所有任务可以立即完成),而应该设置任务的先后顺序!!!!\n
              如果你作为回答方:不要重复提问方发布的任务，也不要生成分析过程，直接生成解决方案:比如，任务要求生成前端vue架构，那么你直接生成架构即可，再添加一些注释；如果任务要求生成后端接口文档，你直接生成就行!!!剩下的以此类推\n
                    
            - 对话细节(必须要有,接上一条): 对话过程中你必须遵循你的角色设定，明确上下级关系，生成最生动的对话口吻。 \n
            - 最终回答(最最重要，the most important):生成的回答核心点必须围绕 {duty} !!!!!!!!!!! \n
    
            生成的格式必须是字符串类型，并且按需换行。\n
            """
                                    )

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
