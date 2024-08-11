import os
import uuid
from langsmith import traceable
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate

class DutyClassifier:
    def __init__(self):
        self.run_id = str(uuid.uuid4())
        
        # LangSmith 内容指定
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        # qiancheng
        os.environ["LANGCHAIN_API_KEY"] = "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"
        os.environ["LANGCHAIN_PROJECT"] = "classifier-chatbot-weihua"

        # ChatModel设定
        self.chat_model = ChatOllama(model="gemma2")

        # Embedding模型
        self.embeddings = HuggingFaceEmbeddings(
            model_name="kuangweihua/ollama/models/m3e-base", model_kwargs={"device": "cpu"}
        )
        print("Embedding: \n", self.embeddings)

        self.duty_classifier = {
            "Project Manager(PM)",
            "Technology Leader(TTL)",
            "Schedule Planning(QA1)",
            "Coding Standard(QA2)",
        }

        # 定义提示模板
        self.classifier_prompt_template = """
        You are now a customer service agent in the software development process,
        responsible for receiving user modification requests and categorizing them to the corresponding software developers.
        The list of developer responsibilities are duty_classfier,
        and classify the type of the request as one of the following duty_classifier: {duty_classifier}.
        User modification request is: {request}

        Please provide the classification and explain the reason for the classification.
        {format_instruction}
        """

        # 构造输出格式
        self.classifier_response_schema = [
            ResponseSchema(
                name="classifier",
                description="Classifier request into a specific type of duty_classifier",
            ),
            ResponseSchema(name="reason", description="Reason for the classifier judgement"),
        ]

        self.classifier_output_parser = StructuredOutputParser.from_response_schemas(
            response_schemas=self.classifier_response_schema
        )

        self.format_instruction = self.classifier_output_parser.get_format_instructions()

        self.prompt_template_01 = PromptTemplate.from_template(
            template=self.classifier_prompt_template,
            partial_variables={"format_instruction": self.format_instruction},
        )

    def create_messages(self, input_text):
        duty_descriptions = ",".join(self.duty_classifier)
        prompt = self.prompt_template_01.format(
            duty_classifier=duty_descriptions,
            request=input_text,
            format_instruction=self.format_instruction,
        )
        return [{"role": "user", "content": prompt}]

    @traceable(
        run_type="llm",
        name="classifier",
    )
    def topic_classifier(self, input_text, langsmith_extra=None):
        messages = self.create_messages(input_text)
        # 将 run_id 添加到 langsmith_extra
        langsmith_extra = langsmith_extra or {}
        langsmith_extra["run_id"] = self.run_id
        response = self.chat_model.invoke(input=messages)
        return self.classifier_output_parser.parse(response.content)


classifier_bot = DutyClassifier()

user_request = "please pull the project to next month"
classifier_result = classifier_bot.topic_classifier(user_request)
print("\n== user request ==:",user_request)
print("== classifier result ==:", classifier_result["classifier"])
print("== judgement reason ==:", classifier_result["reason"], end="\n\n")
