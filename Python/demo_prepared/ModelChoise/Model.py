#
import os


def os_setenv():
    # sparkllm
    os.environ["IFLYTEK_SPARK_APP_ID"] = "5f26990c"
    os.environ["IFLYTEK_SPARK_API_KEY"] = "50bd51b199b38dbd53884e05deedddc5"
    os.environ["IFLYTEK_SPARK_API_SECRET"] = "YTRhMzBhMTk2ZDQ1MDhjMjc4NGI2Yzdk"
    # 　此处参考：https://www.xfyun.cn/doc/spark/Web.html
    os.environ["IFLYTEK_SPARK_API_URL"] = "wss://spark-api.xf-yun.com/v3.1/chat"
    os.environ["IFLYTEK_SPARK_llm_DOMAIN"] = "generalv3"
    # 获取 serapi google搜索工具的key
    os.environ["SERPAPI_API_KEY"] = "167d7c20554da3e8ff4b429f9bb8ab7ac42ac741b07b220552835b7a90053a28"

    # zhipu
    os.environ["ZHIPUAI_API_KEY"] = "6d7fd536c2a665e8194bdcaa5a582476.PERpvVpORuaGxEZP"

    # WebBaseLoader --BeautifulSoup4
    os.environ[
        "USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"

    #设置TAVILY_API_KEY搜索引擎
    import getpass
    os.environ["TAVILY_API_KEY"] = "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"

    #设置Exa检索
    os.environ["EXA_API_KEY"] = "1fc0b566-fe1e-4145-aeab-05c0f30fdd8e"
    #
    os.environ["STABLE_DIFFUSION_API_KEY"]="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"
    #
def get_zhupuai_model():
    # zhipuai model
    from langchain_community.chat_models import ChatZhipuAI
    zhipuai_chat_model = ChatZhipuAI(model="glm-4")
    return zhipuai_chat_model


def getspark_model():
    # sparkllm model
    from langchain_community.chat_models import ChatSparkLLM

    spark_chat_model = ChatSparkLLM()
    return spark_chat_model
# # https://spark-api.xf-yun.com/v1.1/chat?authorization=YXBpX2tleT0iNGI5Y2MyODYyNDI4OTMyYjU0NjNlY2MxZWJkNTY2ODYiLCBhbGdvcml0aG09ImhtYWMtc2hhMjU2IiwgaGVhZGVycz0iaG9zdCBkYXRlIHJlcXVlc3QtbGluZSIsIHNpZ25hdHVyZT0iRVhWc3BxRFgwSEpjMUZOeXRadWhZMVdxbG5pNWdpc3Q2cVAxS3pSS1ZXND0i&date=Thu%2C+18+Jul+2024+12%3A02%3A43+GMT&host=spark-api.xf-yun.com