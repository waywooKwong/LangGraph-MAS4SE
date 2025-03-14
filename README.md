## News

new generation from 15/03/2025,

mainly based on stable version of LangGraph & LangChain,

ensembling MCP from Anthropic and Browser use.

## Project Name

Muiti-Agents System Workflow for Software Engineering

![function_structure](src/fuction_structure.png)

## Members

邝伟华、王璞、钱程、余文祥

## Log

1. 项目名称：MAS4SE Multi-Agent System for Software Engineering
2. 项目简介：LangGraph 框架搭建的可视化多智能体工作流系统，LangChain+Ollama
3. 确保你的本地已配置：

- Python 3.9 + LangChain + LangGraph
- Node.js + Vue3
- Ollama
- Redis

![basic workflow](src/basic_workflow.png)

### How to run

1. 保存仓库至本地

   ```
   git clone https://github.com/waywooKwong/CSI-LangChain-LLM-Chatbot.git
   ```
2. 前端启动

   ```
   cd MAS4SE-frontend
   npm run serve
   ```
3. 后端启动

   ```
   cd MAS4SE-backend
   python run.py
   ```
4. 数据库启动

   ```
   cd MAS4SE-frontend/src/database
   cd Redis redis-server.exe
   node server.cjs
   ```

注意：

1. embedding_models 编码模型 m3e-base 需要本地配置

```
MAS4SE-backend/src/embedding_models/m3e-base
```

2. 前后端交互

```
前端 JointUI 向后端传递连接结点关系
MAS4SE-backend/frontend_json_process/json_simplified
工作流运行完成后生成的文本
MessageSum
```

## Thanks

致谢：我们使用 Jointjs+来实现WebUI的交互连接部分，https://www.jointjs.com/demos/chatbot

## Contact us

通过 Github 或者邮箱 2211992@mail.nankai.edu.cn 与我们联系
