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


class WebScratchRoleTxt:
    def __init__(self, role: str):
        self.keyword = role
        self.keyword_txt_folder = f"src/exa/exa_txt/{self.keyword}"
        os.makedirs(self.keyword_txt_folder, exist_ok=True)
        # Google 得到的 json 文件
        self.json_file_path = f"src/exa/exa_json/{self.keyword}.json"
        # 存储所有涉及到的 url
        self.urls = []
        # Google Serper 从 url 提取到的文本
        self.URL_Scraper_txt_path = f"src/exa/exa_txt/{self.keyword}/URL_Scarper.txt"

    # Tool 2 : DuckDuckGo (false)
    def DuckDuckGo_search(self):
        from langchain_community.tools import DuckDuckGoSearchResults
        from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
        import urllib.request

        # DuckDuckGo 有限制, 设置使用代理访问
        proxy = "127.0.0.1:7890"
        proxy_handler = urllib.request.ProxyHandler(
            {"http": "http://" + proxy, "https": "http://" + proxy}
        )
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)

        # 参数文档: https://pypi.org/project/duckduckgo-search/#regions
        # region:"cn-zh" for china
        wrapper = DuckDuckGoSearchAPIWrapper(region="wt-wt", time="y", source="text")
        DDG_response = wrapper.results(query=self.keyword, max_results=3)
        print("\nDuckDuckGo response", DDG_response)
        # 初始化 urls 列表

        DDG_snippet_path = f"src/exa/exa_txt/{self.keyword}/DDG_snippet_path.txt"
        with open(DDG_snippet_path, "a", encoding="utf-8") as file:
            for result in DDG_response:
                snippet = result.get("snippet")
                link = result.get("link")
                file.write(snippet + "\n")
                self.urls.append(link)

    # Tool 3 : Google Serper
    # 官网: https://serper.dev/
    # LangChain: https://python.langchain.com/v0.2/docs/integrations/tools/google_serper/
    # 可以获取原始数据，也可以进行 Google 图片搜索 / Google 新闻 / Google 地理位置

    # 1. 获取搜索反馈的 json
    def GoogleSerper_search(self):
        from langchain_community.utilities import GoogleSerperAPIWrapper

        os.environ["SERPER_API_KEY"] = "0b33d1ee4053a32b93f6d029f66aa149599d7c91"

        # 1. 搜索, 进 GoogleSerperAPIWrapper 中，有直接拼接 Snippet 的函数
        GoogleSerper_search = GoogleSerperAPIWrapper(k=3, type="search")
        response = GoogleSerper_search.results(self.keyword)
        # print("\nGoogleSerper response:", response)
        with open(self.json_file_path, "w") as file:
            json.dump(response, file, indent=4)
        print(f"\nGoogle Serper- Json 保存到{self.json_file_path}")

        with open(self.json_file_path, "r") as file:
            data = json.load(file)
        GoogleSerper_urls = [item["link"] for item in data.get("organic", [])]
        self.urls.extend(GoogleSerper_urls)
        # print("\nurls(after add GoogleSerper URL):", self.urls)

        # 2. snippets 拼接写入
        snippets = [item["snippet"] for item in response["organic"]]
        GoogleSerper_snippet_path = f"src/exa/exa_txt/{self.keyword}/Google_snippet.txt"
        with open(GoogleSerper_snippet_path, "w", encoding="utf-8") as file:
            file.write("Snippets:\n")
            file.write("\n".join(snippets))
        print(f"\nGoogleSerper snippet - txt 保存到 {GoogleSerper_snippet_path}")
        # print("\nurls:", self.urls)

    def Google_ScrapeUrls(self):
        url = "https://scrape.serper.dev"
        GoogleSerper_api_key = "ed86bb07558520108083d454996e405afa715db1"
        with open(self.URL_Scraper_txt_path, "w", encoding="utf-8") as file:
            for target_url in self.urls:
                payload = json.dumps({"url": target_url})
                headers = {
                    "X-API-KEY": GoogleSerper_api_key,
                    "Content-Type": "application/json",
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                # print("\nresponse.text:", response.text)
                # value = response.text
                # print(value["text"])
                file.write(response.text + "\n")
        print(f"\nGoogle Serper URL 解析文本已经保存： {self.URL_Scraper_txt_path}")


# role_text_generator = WebScratchRoleTxt(role="辅导员")
# role_text_generator.DuckDuckGo_search()
# role_text_generator.GoogleSerper_search()
# role_text_generator.Google_ScrapeUrls()
