# MAS-Vue 3.0

## Project setup

```
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

## Redis

路径：`cd MAS\src\Redis`

版本： redis-x64-5.0.14.1 

环境准备：npm install redis

使用流程：

1. 进入 `cd MAS\src\Redis`

2. `npm install`  更新npm包

3. 新开终端1 `cd MAS\MAS-front 3.0\src\database
   `node server.cjs` 启动 express

   ​	连接成功：Server is running on http://localhost:3000

   ​						Connected to Redis...

4. 新开终端2 `cd MAS\MAS-front 3.0\src\database\Redis`
   `redis-server.exe` 启动 redis

   ​	连接成功：终端打出图形，显示 PORT：6379

insert-test.cjs 测试数据插入

Redis Insight 可视化数据库信息查看
