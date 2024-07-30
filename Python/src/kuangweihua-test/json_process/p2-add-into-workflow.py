import json
from functools import partial

json_file_path = "frontend-0729_simpified.json"
with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)
    
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from typing import Dict, List, TypedDict, Annotated, Any
import operator
# 0.0 Graph 整体通信类型（之后可以换成 FIPA-ACL）
class AgentState(TypedDict):
    sender: str
    progress: str
    messages: Annotated[List[BaseMessage], operator.add]
    next: str
    
# 定义函数
def func_node(node_name):
    print(f"Node: {node_name}")
    
from langgraph.graph import END, StateGraph, START
# 初始化图
workflow = StateGraph(AgentState)

# 提取 message 部分信息并添加结点
for message in data['Message']:
    label_text = message['label_text']
    workflow.add_node(label_text, partial(func_node, node_name=label_text))

# 处理 link 部分信息并添加边
link_edges = {}
for link in data['Link']:
    source_label = link['source_label']
    target_label = link['target_label']

    # 统计每个 source_label 对应的 target_label 的数量
    if source_label not in link_edges:
        link_edges[source_label] = []
    link_edges[source_label].append(target_label)


# 添加边
for source_label, targets in link_edges.items():
    if len(targets) > 1:
        conditional_map = {target: target for target in targets}
        conditional_map["Finish"] = "End"
        print("----")
        print("conditional_map:",conditional_map)
        print("----")
        workflow.add_conditional_edges(source_label, partial(func_node, node_name=source_label), conditional_map)
    else:
        workflow.add_edge(source_label, targets[0])
    

# 测试打印结果
print("Nodes:", workflow.nodes)
print("Edges:", workflow.edges)