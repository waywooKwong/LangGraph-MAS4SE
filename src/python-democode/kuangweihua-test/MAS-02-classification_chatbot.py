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



duty_classifier = {
    "Project Manager(PM)",
    "Technology Leader(TTL)",
    "Schedule Planning(QA1)",
    "Coding Standard(QA2)",
}

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
    ResponseSchema(name="reason", description="Reason for the classifier judgement"),
]

classifier_output_parser = StructuredOutputParser.from_response_schemas(
    response_schemas=classifier_response_schema
)

format_instruction = classifier_output_parser.get_format_instructions()

prompt_template_01 = PromptTemplate.from_template(
    template=classifier_prompt_template,
    partial_variables={"format_instruction": format_instruction},
)


def create_messages(input_text):
    duty_descriptions = ",".join(duty_classifier)
    prompt = prompt_template_01.format(
        duty_classifier=duty_descriptions,
        request=input_text,
        format_instruction=format_instruction,
    )
    return [{"role": "user", "content": prompt}]


@traceable(
    run_type="llm",
    name="classifier",
)
def topic_classifier(input_text):
    messages = create_messages(input_text)
    response = chat_model.invoke(input=messages)
    return classifier_output_parser.parse(response.content)


run_id = str(uuid.uuid4())
user_request = "写一个飞机大战的游戏"
classifier_result = topic_classifier(user_request, langsmith_extra={"run_id": run_id})

print("\nclassifier result:", classifier_result["classifier"])
print("reason:", classifier_result["reason"], end="\n\n")
