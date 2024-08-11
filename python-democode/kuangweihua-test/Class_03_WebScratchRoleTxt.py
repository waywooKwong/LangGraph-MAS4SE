"""
通过 "关键词" 提取网页链接，爬取网页内容
参考网址: https://python.langchain.com/v0.2/docs/integrations/tools/
注意需要找的工具是 Return Data 中包含 "Snippet" 的项

1. 最好不要 URL + BeatuifulSoup  
    ->  Google Serper 有 WebSearch 的选项爬取网页内容，具体看代码部分的注释网址
2. 直接得到 content 然后加入生成文本中，
    ->  文本路径: web_down_file_path = f"src/exa/exa_txt/{input_keyword}.txt"
"""
"""
20240731 - finished
用了两个工具：
1. DuckDuckGo 得到的输出是 <list>, 所以 snippet 直接写入文本, link 加入 url 列表
2. Google Serper: 得到输出是 <json>, 所以先存为 json 再进行解析

基础代码由 余文祥 实现
代码架构以及功能的调教整理, 由邝伟华完成
"""

import os
import json
import requests


### 关键词输入
keyword = "算法工程师"
key_word_txt_folder = f"src/exa/exa_txt/{keyword}"
os.makedirs(key_word_txt_folder, exist_ok=True)
# Google 得到的 json 文件
json_file_path = f"src/exa/exa_json/{keyword}.json"
# 存储所有涉及到的 url
urls = []
# Google Serper 从 url 提取到的文本
URL_Scraper_txt_path = f"src/exa/exa_txt/{keyword}/URL_Scarper.txt"



# # Tool 2 : DuckDuckGo (false)
# def DuckDuckGo_search(input_keyword):
#     from langchain_community.tools import DuckDuckGoSearchResults
#     from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
#     import urllib.request

#     # DuckDuckGo 有限制, 设置使用代理访问
#     proxy = "127.0.0.1:7890"
#     proxy_handler = urllib.request.ProxyHandler(
#         {"http": "http://" + proxy, "https": "http://" + proxy}
#     )
#     opener = urllib.request.build_opener(proxy_handler)
#     urllib.request.install_opener(opener)

#     # 参数文档: https://pypi.org/project/duckduckgo-search/#regions
#     # region:"cn-zh" for china
#     wrapper = DuckDuckGoSearchAPIWrapper(region="wt-wt", time="y", source="text")
#     DDG_response = wrapper.results(query=input_keyword, max_results=3)
#     print("DuckDuckGo response", DDG_response)
#     # 初始化 urls 列表

#     DDG_snippet_path = f"src/exa/exa_txt/{input_keyword}/DDG_snippet_path.txt"
#     # 将每个 snippet 写入 a.txt 文件，并将每个 link 添加到 urls 列表中
#     with open(DDG_snippet_path, 'a') as file:
#         for result in DDG_response:
#             snippet = result.get('snippet')
#             link = result.get('link')
#             file.write(snippet + '\n')
#             urls.append(link)
# DuckDuckGo_search(keyword)


# Tool 3 : Google Serper
# 官网: https://serper.dev/
# LangChain: https://python.langchain.com/v0.2/docs/integrations/tools/google_serper/
# 可以获取原始数据，也可以进行 Google 图片搜索 / Google 新闻 / Google 地理位置

# 1. 获取搜索反馈的 json
def GoogleSerper_search(input_keyword):
    from langchain_community.utilities import GoogleSerperAPIWrapper
    os.environ["SERPER_API_KEY"] = "0b33d1ee4053a32b93f6d029f66aa149599d7c91"

    # 1. 搜索, 进 GoogleSerperAPIWrapper 中，有直接拼接 Snippet 的函数
    GoogleSerper_search = GoogleSerperAPIWrapper(k=3, type="search")
    response = GoogleSerper_search.results(input_keyword)
    print("GoogleSerper response:", response)
    with open(json_file_path, "w") as file:
        json.dump(response, file, indent=4)
    print(f"Google Serper- Json 保存到{json_file_path}")
    
    with open(json_file_path, "r") as file:
        data = json.load(file)
    GoogleSerper_urls = [item["link"] for item in data.get("organic", [])]
    urls.extend(GoogleSerper_urls)
    print('urls(after add GoogleSerper URL):',urls)


    # 2. snippets 拼接写入
    snippets = [item["snippet"] for item in response["organic"]]
    GoogleSerper_snippet_path =  f"src/exa/exa_txt/{keyword}/Google_snippet.txt"
    with open(GoogleSerper_snippet_path, "w") as file:
        file.write("Snippets:\n")
        file.write("\n".join(snippets))
    print(f"GoogleSerper snippet - txt 保存到 {GoogleSerper_snippet_path}")
GoogleSerper_search(keyword)
print('urls:',urls)


def Google_ScrapeUrls(urls, output_file):
    url = "https://scrape.serper.dev"
    GoogleSerper_api_key = "ed86bb07558520108083d454996e405afa715db1"
    with open(output_file, "w", encoding="utf-8") as file:
        for target_url in urls:
            payload = json.dumps({"url": target_url})
            headers = {"X-API-KEY": GoogleSerper_api_key, "Content-Type": "application/json"}
            response = requests.request("POST", url, headers=headers, data=payload)
            print("response.text:",response.text)
            # value = response.text
            # print(value["text"])
            file.write(response.text + "\n")
    print(f"Google Serper URL 解析文本已经保存： {output_file}")
Google_ScrapeUrls(urls, URL_Scraper_txt_path)


# ========================= Code not used =====================#
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
