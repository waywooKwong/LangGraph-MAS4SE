import requests
from bs4 import BeautifulSoup

def search_baidu_baike(keyword):
    search_url = f"https://baike.baidu.com/search/word?word={keyword}"
    print(f"Initial search URL: {search_url}")
    
    try:
        response = requests.get(search_url, allow_redirects=True)
        response.raise_for_status()  # 检查请求是否成功
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None
    
    # 检查最终的URL
    final_url = response.url
    if "baike.baidu.com/item" in final_url:
        return final_url
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        result_link = soup.find('a', {'target': '_blank', 'href': True})
        if result_link and 'item' in result_link['href']:
            return 'https://baike.baidu.com' + result_link['href']
        else:
            return None

keyword = "抖音"
baidu_url = search_baidu_baike(keyword)
if baidu_url:
    print(f"Final URL: {baidu_url}")
else:
    print(f"No results found for keyword: {keyword}")
