from ModelChoise import modelchoise
# chat_model = modelchoise.get_spark_chat_model()
from langchain_community.chat_models import ChatOllama
chat_model = ChatOllama(model = "qwen2")
response = chat_model.invoke("introduce yourself")
print("response:",response)