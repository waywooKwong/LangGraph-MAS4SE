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
        # 查找推荐的相关词条
        related_links = soup.find_all('a', {'target': '_blank', 'href': True})
        for link in related_links:
            return 'https://baike.baidu.com' + link['href']
        
        # 如果没有找到确切的结果和推荐的相关词条，返回页面中下一个出现的推荐词条链接
        first_link = soup.find('a', {'class': 'result-title'})
        if first_link:
            return 'https://baike.baidu.com' + first_link['href']
        
        return None

# 测试关键词
keyword = "项目用例"
baidu_url = search_baidu_baike(keyword)
if baidu_url:
    print(f"Final URL: {baidu_url}")
else:
    print(f"No exact results found for keyword: {keyword}. Trying to find related entries.")
    # 可以在这里添加更多处理逻辑，例如返回相关词条列表或进一步的处理
