'''
通过 "关键词" 提取网页链接，爬取网页内容
基础功能代码由 余文祥 实现
调整代码结构由 邝伟华 完成
'''
import os
import requests
import json
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from dataclasses import dataclass
from typing import List


@dataclass
class Document:
    page_content: str
    metadata: dict


def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


# 获取当前脚本文件所在的目录, 构建模型的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "models", "m3e-base")

embeddings = HuggingFaceEmbeddings(
    model_name=model_path,
    model_kwargs={"device": "cpu"},
)
print(embeddings)
# 获取用户输入
input_keyword = "nankai"

# 通过Exa API获取关键词相关的链接
exa_api_url = "https://api.exa.ai/search"
exa_payload = {"query": input_keyword}
exa_headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": "8388973f-cd9c-4452-bfea-c860c263fbba",
}
exa_response = requests.post(exa_api_url, json=exa_payload, headers=exa_headers)
exa_response_json = exa_response.json()

# 将获取的信息保存为json文件
exa_json_dir = os.path.join(
    "langchain-demo", "MAS", "Qdrant", "documents", "myExaJsons"
)
ensure_dir_exists(exa_json_dir)
exa_json_file_path = os.path.join(exa_json_dir, f"{input_keyword}.json")
with open(exa_json_file_path, "w", encoding="utf-8") as json_file:
    json.dump(exa_response_json, json_file, ensure_ascii=False, indent=4)
print(f"数据已保存到 {exa_json_file_path}")

# 读取并提取JSON文件中的URL
with open(exa_json_file_path, "r", encoding="utf-8") as json_file:
    exa_data = json.load(json_file)
urls = [result["url"] for result in exa_data["results"]]

# 从URL抓取网页内容并保存到文件
base_dir = os.path.join("langchain-demo", "MAS", "Qdrant", "documents", "mytxt")
down_folder_path = os.path.join(base_dir, input_keyword)
ensure_dir_exists(down_folder_path)
web_down_file_path = os.path.join(down_folder_path, f"webs_{input_keyword}.txt")
with open(web_down_file_path, "w", encoding="utf-8") as file:
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.get_text().replace("\n", " ").replace("\r", "")
            file.write(f"内容来自网址: {url}\n\n")
            file.write(text)
            file.write("\n\n" + "=" * 80 + "\n\n")
        except requests.RequestException as e:
            print(f"获取网址内容时出错: {url}，错误信息: {e}")
        except Exception as e:
            print(f"处理网址内容时出错: {url}，错误信息: {e}")
print(f"所有网址的内容已经保存到文件: {web_down_file_path}")

# 整合所有TXT文件为一个文件
vector_path = base_dir
vector_folder_path = os.path.join(vector_path, f"combine_{input_keyword}")
ensure_dir_exists(vector_folder_path)
combine_files_path = os.path.join(vector_folder_path, f"combine_{input_keyword}.txt")

with open(combine_files_path, "w", encoding="utf-8") as output_file:
    for filename in os.listdir(down_folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(down_folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as input_file:
                content = input_file.read().replace("\n", " ")
                output_file.write(content.strip() + " ")
print(f"所有TXT文件已成功合并到 {combine_files_path}")

# 将整合后的内容保存到向量数据库中
documents: List[Document] = []
with open(combine_files_path, "r", encoding="utf-8") as file:
    text = file.read()
    document = Document(page_content=text, metadata={"filename": input_keyword})
    documents.append(document)

print(f"读取了 {len(documents)} 个文档。")
if documents:
    print(
        f"第一个文档内容预览：\n文件名: {documents[0].metadata['filename']}\n内容: {documents[0].page_content[:200]}..."
    )

# 文档切分
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=10)
chunked_documents = text_splitter.split_documents(documents=documents)
for chunk in chunked_documents:
    print(chunk)


# vectorstore = Qdrant.from_documents(
#     documents=chunked_documents,
#     embedding=embeddings,
#     location=":memory:",
#     collection_name="my_documents",
# )
# 定义存储位置的路径
vectorstore_dir = os.path.join("langchain-demo", "MAS", "Qdrant", "documents", "qdrant_stroage")
ensure_dir_exists(vectorstore_dir)
print("vectorstore_path:",vectorstore_dir)

vectorstore = Qdrant.from_documents(
    documents=chunked_documents,
    embedding=embeddings,
    location="http://localhost:6333",
    collection_name="qdrant-test-0725-docker",
)

print("文档已成功嵌入到Qdrant向量数据库中并存储到本地文件系统。")
