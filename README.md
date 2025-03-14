## News

new generation from 15/03/2025,

mainly based on stable version of LangGraph & LangChain,

ensembling MCP from Anthropic and Browser use.

## Project Name

Muiti-Agents System Workflow for Software Engineering

![function_structure](src/fuction_structure.png)

## Members

Origin version: Weihua Kuang (邝伟华)、Pu Wang (王璞)、Cheng Qian (钱程)、Wenxiang Yu (余文祥)

This repository is maintained by Weihua Kuang (@**waywooKwong**).

## How to run

Please ensure you have the following environments :

- Python 3.9 + LangChain + LangGraph
- Node.js + Vue3
- Ollama
- Redis

![basic workflow](src/basic_workflow.png)

1. Clone this repo

   ```
   git clone https://github.com/waywooKwong/CSI-LangChain-LLM-Chatbot.git
   ```
2. run Web UI

   ```
   cd MAS4SE-frontend
   npm run serve
   ```
3. run backend function server

   ```
   cd MAS4SE-backend
   python run.py
   ```
4. run database server

   ```
   cd MAS4SE-frontend/src/database
   cd Redis redis-server.exe
   node server.cjs
   ```

Attention：

1. embedding_models:  m3e-base needs to be downloaded local.

```
MAS4SE-backend/src/embedding_models/m3e-base
```

2. Interaction between frontend & backend

```
前端 JointUI 向后端传递连接结点关系
MAS4SE-backend/frontend_json_process/json_simplified
工作流运行完成后生成的文本
MessageSum
```

## Thanks

We use JointJS+ to implement the interactive workflow part of Web UI.

https://www.jointjs.com/demos/chatbot

## Contact us

Push issues under this repo, or eamil Weihua Kuang by weihua.kwong@mai.nankai.edu.cn
