"""
通过 "关键词" 提取网页链接，爬取网页内容
参考网址: https://python.langchain.com/v0.2/docs/integrations/tools/
注意需要找的工具是 Return Data 中包含 "Snippet" 的项

1. 最好不要 URL + BeatuifulSoup  
    ->  Google Serper 有 WebSearch 的选项爬取网页内容，具体看代码部分的注释网址
2. 直接得到 content 然后加入生成文本中，
    ->  文本路径: web_down_file_path = f"src/exa/exa_txt/{input_keyword}.txt"
"""

import os
import pprint

import json
import requests
from bs4 import BeautifulSoup

### 关键词输入
keyword = "Project Manager"

# Tool 1 : EXA
# def EXA_search(input_keyword):
#     # 0. EXA (Agent tool) 工具爬取使用
#     exa_api_url = "https://api.exa.ai/search"
#     exa_payload = {"query": input_keyword}
#     exa_headers = {
#         "accept": "application/json",
#         "content-type": "application/json",
#         "x-api-key": "8388973f-cd9c-4452-bfea-c860c263fbba",
#     }
#     exa_response = requests.post(exa_api_url, json=exa_payload, headers=exa_headers)
#     exa_response_json = exa_response.json()

#     # 1. 将获取的信息保存为json文件
#     exa_json_file_path = f"src/exa/exa_json/{input_keyword}.json"
#     with open(exa_json_file_path, "w", encoding="utf-8") as json_file:
#         json.dump(exa_response_json, json_file, ensure_ascii=False, indent=4)
#     print(f"1. exa json 文件保存到 {exa_json_file_path}")

#     # 2. 读取并提取 json 文件中的 url
#     with open(exa_json_file_path, "r", encoding="utf-8") as json_file:
#         exa_data = json.load(json_file)
#     urls = [result["url"] for result in exa_data["results"]]
#     print("2. URL 爬取到 (urls[0]) :",urls[0])

#     # 3. 从URL抓取网页内容并保存到文件
#     web_down_file_path = f"src/exa/exa_txt/{input_keyword}.txt"
#     with open(web_down_file_path, "a", encoding="utf-8") as file: # 'a' 模型, 追写模式
#         for url in urls:
#             try:
#                 response = requests.get(url)
#                 response.raise_for_status()
#                 soup = BeautifulSoup(response.content, "html.parser")
#                 text = soup.get_text().replace("\n", " ").replace("\r", "")
#                 file.write(f"web 内容来自 URL: {url}\n\n")
#                 file.write(text)
#                 file.write("\n\n" + "=" * 80 + "\n\n")
#             except requests.RequestException as e:
#                 print(f"获取时出错: {url}, error: {e}")
#             except Exception as e:
#                 print(f"处理内容时出错: {url}, error: {e}")
#     print(f"URL 内容全部写入到: {web_down_file_path}")
# EXA_search(keyword)


# Tool 2 : DuckDuckGo (false)
def DuckDuckGo_search(input_keyword):
    from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults

    # DuckDuckGo_search = DuckDuckGoSearchRun()
    DuckDuckGo_search = DuckDuckGoSearchResults()
    results = DuckDuckGo_search._run(input_keyword)
    print("DuckDuckGo response", results)


DuckDuckGo_search(keyword)


# Tool 3 : Google Serper
# 官网: https://serper.dev/
# LangChain: https://python.langchain.com/v0.2/docs/integrations/tools/google_serper/
# 可以获取原始数据，也可以进行 Google 图片搜索 / Google 新闻 / Google 地理位置
# !!! 这个也有 URL 的爬取，可以结合 EXA 得到的 URL？
def GoogleSerper_search(input_keyword):
    from langchain_community.utilities import GoogleSerperAPIWrapper

    # 进 GoogleSerperAPIWrapper 中，有直接拼接 Snippet 的函数
    os.environ["SERPER_API_KEY"] = "0b33d1ee4053a32b93f6d029f66aa149599d7c91"
    GoogleSerper_search = GoogleSerperAPIWrapper()
    response = GoogleSerper_search.run(input_keyword)
    print("GoogleSerper response:", response)


GoogleSerper_search(keyword)
