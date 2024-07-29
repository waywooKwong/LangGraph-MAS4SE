# CSI-ATM

This template should help get you started developing with Vue 3 in Vite.

## 1. Setup

确保你本地已经配置

- Node.js
- MySQL Workbench

```
npm install
```

## 2. Database

 /Server 文件夹下，MySQL 运行 create_and_insert.sql 创建信息存储环境

server.cjs 中配置本地的 MySQL config 信息

```
node server.cjs
```

出现下述语句说明连接成功，其它情况请检查你的服务器配置

```
Server running on http://localhost:3000
MySQL connected...
```

## 3. Run

```
npm run dev
```

