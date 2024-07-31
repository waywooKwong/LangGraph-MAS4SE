"""
20240725
收集用户需求进行职责划分,
打包成CSR(客服机器人)类使用
"""

import os
import uuid
from langsmith import traceable
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from demo_prepared.ModelChoise.modelchoise import get_zhipuai_chat_model
# LangSmith 内容指定
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_PROJECT"] = "classifier-chatbot"

# ChatModel设定
chat_model = get_zhipuai_chat_model()




# 定义提示模板
classifier_prompt_template = """
You are now a customer service agent in the software development process,
responsible for receiving user modification requests and categorizing them to the corresponding software developers.
The list of developer responsibilities are duty_classfier,
and classify the type of the request as one of the following duty_classifier: {duty_classifier}.
User modification request is: {request}

Please provide the classification and explain the reason for the classification,answer with Chinese.
{format_instruction}
"""

# 构造输出格式
classifier_response_schema = [
    ResponseSchema(
        name="classifier",
        description="Classifier request into a specific type of duty_classifier",
    ),

]

classifier_output_parser = StructuredOutputParser.from_response_schemas(
    response_schemas=classifier_response_schema
)

format_instruction = classifier_output_parser.get_format_instructions()

prompt_template_01 = PromptTemplate.from_template(
    template=classifier_prompt_template,
    partial_variables={"format_instruction": format_instruction},
)

