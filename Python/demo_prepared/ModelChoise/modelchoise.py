import os


# 环境变量设置 def os_setenv():
def get_ollama():
    from langchain_community.chat_models import ChatOllama

    ollama_chat_model = ChatOllama(model="llama3")
    return ollama_chat_model


def get_openai_chat_model():
    # from langchain_openai import ChatOpenAI
    from langchain_community.chat_models import ChatOpenAI

    gpt_chat_model = ChatOpenAI(
        base_url="https://p33279i881.vicp.fun/v1/",
        api_key="sk-JKuWXQZ4WEaNQEYi72A72304075742E2B2D805C6936293E5",
    )
    return gpt_chat_model


def get_qianfan_chat_model():
    from langchain_community.chat_models import QianfanChatEndpoint

    os.environ["QIANFAN_AK"] = "QZuS6bjsMNYIviveGTu3ZbKj"
    os.environ["QIANFAN_SK"] = "AfMleAQMS2fI4yGl9M8iU2ikBGVlKQOJ"
    qianfan_chat_model = QianfanChatEndpoint(
        temperature=0, model="ernie-bot-turbo", verbose=True
    )
    return qianfan_chat_model


def get_tongyi_chat_model():
    os.environ["DASHSCOPE_API_KEY"] = "sk-8a7c3ac35b84410e8435116a8b3630ef"
    from langchain_community.chat_models import ChatTongyi

    tongyi_chat_model = ChatTongyi()
    return tongyi_chat_model


def get_spark_chat_model():
    os.environ["IFLYTEK_SPARK_APP_ID"] = "2e921bde"
    os.environ["IFLYTEK_SPARK_API_SECRET"] = "ZjJhZTkyOGQzNzA4N2U5MWI2MjhhM2Qz"
    os.environ["IFLYTEK_SPARK_API_KEY"] = "e77f9a737eee9d91e710e1f743ed46dd"
    os.environ["IFLYTEK_SPARK_API_URL"] = "wss://spark-api.xf-yun.com/v3.5/chat"
    os.environ["IFLYTEK_SPARK_llm_DOMAIN"] = "generalv3.5"
    from langchain_community.chat_models import ChatSparkLLM

    spark_chat_model = ChatSparkLLM()
    return spark_chat_model


def get_zhipuai_chat_model():
    os.environ["ZHIPUAI_API_KEY"] = "72fea15b5fce38e0a81b2bb01e4903dd.wkhUuC4oAO5otOmY"
    # 20240731 20:55 weihua
    # new key: "6ac43a47c3fed6a70433a55108033202.OMB8LBLcgcz60x3q"
    # old key: "43c5d0cda6ab08302d6db046469d7c6b.eCF9cwVy1tadDU1q"
    # qiancheng: "72fea15b5fce38e0a81b2bb01e4903dd.wkhUuC4oAO5otOmY"
    from langchain_community.chat_models import ChatZhipuAI

    zhipuai_chat_model = ChatZhipuAI(model="glm-4")
    return zhipuai_chat_model
