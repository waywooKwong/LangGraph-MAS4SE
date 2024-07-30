## 运行路径

文件路径为相对路径！

运行时请一定切换到：**cd  \Python\demo_prepared**

## 命名规范

文件夹规范：文件夹命名统一使用 "_" 进行分隔，规避中文命名

文件命名：文件命名可以采用 "-" 进行分隔，Class 类额外注明

## 文件夹说明

src 文件夹：

1. *mydocuments* 存放运行产生的 documents 文件
2. *workflow_graph* 存放 langgraph 运行生成的 graph 图
3. *embedding_models* 存放 embedding 模型

ModelChoise 文件夹：

    modelchoise.py 用来设定ChatModel（ 注意api调用的限制 ）

frontend_json_process 文件夹：

    用来存放处理前端传递的 json 文件
