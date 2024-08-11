"""
20240803 代码说明: weihua
这里是我从 LangChain 官方文档看到的 ChatOllama 中 MultiModel
url: https://python.langchain.com/v0.2/docs/integrations/chat/ollama/

注意使用需要先在 ollama 中 ollama pull bakllava, 使用的是 bakllava 模型

PNG -> base74 -> llm_bakllava
"""

"""
测试案例1: 分析一张具体的甘特图, 效果并不好

image_path = "src/pic_test/CSI-ATM.png"
text_input = "Please describe the contents of the project Gantt chart below"
"""
"""
测试案例2: 分析抖音界面截图

概要性内容设计的总结还比较全面

image_path = "src/pic_test/douyin.png"
text_input = "Detailed describe the UI structure shown in the picture"
"""
"""
测试案例3: 解读 workflow 图片
效果其实不错, prompt 需要提得更细节一些

image_path = "src/workflow_graph/workflow_graph_20240801_121243.png"
text_input = "Detailedly introduce the workflow in picture, describe each node and edge relationship"

The image displays a chart or diagram depicting a workflow,
with each box representing a specific step in the process. 
The workflow appears to be related to software development, 
as it includes a Start block and a Tech Leader block. 
There are also blocks for testing and deployment.
"""
import base64
from PIL import Image
from io import BytesIO
from langchain_core.messages import HumanMessage
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser


class ImageChain:
    def __init__(self):
        self.llm_bakllava = ChatOllama(
            model="bakllava", temperature=0
        )  # 使用 bakllava 模型, temperature=0 活跃性最低
        self.image_chain = self.image_prompt | self.llm_bakllava | StrOutputParser()

    def convert_to_base64(self, image_path, image_format="PNG"):
        """
        Convert PIL images to Base64 encoded strings

        :param pil_image: PIL image
        :return: Re-sized Base64 string
        """
        pil_image = Image.open(image_path)
        buffered = BytesIO()
        pil_image.save(buffered, format=image_format)  # 默认 image_format, 也可调整参数
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str

    def image_prompt(self, data):
        # 获取的原始输入
        text = data["text"]
        image = data["image"]

        # 原始输入调整成模型输入格式
        image_part = {
            "type": "image_url",
            "image_url": f"data:image/jpeg;base64,{image}",
        }
        text_part = {"type": "text", "text": text}

        content_parts = []
        content_parts.append(image_part)
        content_parts.append(text_part)
        return [HumanMessage(content=content_parts)]

    def image_invoke(
        self,
        image_path="src/pic_test/douyin.png",
        text_request="What is picture content?",
        image_format="PNG",
    ):
        """
        调用该函数,传入 1.图片路径 和 2. 文本需求描述
        得到 image_chain 分析得到的结果
        """
        print("enter the ImageChain...")
        image_input = self.convert_to_base64(image_path, image_format)
        response = self.image_chain.invoke({"text": text_request, "image": image_input})
        return response


image_path = "src/workflow_graph/workflow_graph_20240801_121243.png"
text_input = "Detailedly introduce the workflow in picture, describe each node and edge relationship"

imageChain = ImageChain()
print(
    "image chain response:",
    imageChain.image_invoke(image_path=image_path, text_request=text_input),
)
