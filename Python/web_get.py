import requests
from bs4 import BeautifulSoup
import urllib.parse

def save_page_text(url, filename):
    response = requests.get(url)
    response.encoding = 'utf-8'  # 确保正确的编码
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # 提取纯文本
        text = soup.get_text(separator='\n')
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text content saved to {filename}")
    else:
        print(f"Failed to retrieve content from {url}")

def search_and_save(keyword):
    # 百度百科
    baidu_base_url = 'https://baike.baidu.com/item/'
    baidu_search_url = baidu_base_url + urllib.parse.quote(keyword)
    baidu_filename = f"{keyword}_baidu.txt"
    save_page_text(baidu_search_url, baidu_filename)

    # # 维基百科
    # wiki_base_url = 'https://en.wikipedia.org/wiki/'
    # wiki_search_url = wiki_base_url + urllib.parse.quote(keyword)
    # wiki_filename = f"{keyword}_wiki.txt"
    # save_page_text(wiki_search_url, wiki_filename)

# 示例用法
search_and_save('余华')

