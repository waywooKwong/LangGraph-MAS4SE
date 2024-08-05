const express = require('express');
const { createClient } = require('redis');
const bodyParser = require('body-parser');
const cors = require('cors'); // 引入 cors 中间件

const app = express();
const port = 3000; // Express 服务器的端口

// 创建Redis客户端
const client = createClient();

client.on('error', (err) => console.error('Redis Client Error', err));

(async () => {
  await client.connect();
  console.log('Connected to Redis...');
})();

// 中间件
<<<<<<< HEAD
//app.use(bodyParser.json());
// 配置 body-parser 以处理较大的请求体
app.use(bodyParser.json({ limit: '100mb' })); // 增加请求体大小限制
app.use(bodyParser.urlencoded({ limit: '100mb', extended: true }));



=======
app.use(bodyParser.json());
>>>>>>> 030ff2c91c186cce9e9018e47bd7e8a786f97ae3
app.use(cors()); // 使用 cors 中间件

// 存储对话记录的接口
app.post('/save-dialog', async (req, res) => {
  try {
    const { user, message } = req.body;
    const dialog = { user, message, timestamp: new Date().toISOString() };

    await client.rPush('chat dialog', JSON.stringify(dialog));
    res.status(200).send('Dialog saved');
  } catch (err) {
    res.status(500).send(err.toString());
  }
});

// 获取对话记录的接口
app.get('/dialogs', async (req, res) => {
  // try {
  //   const dialogs = await client.lRange('chat dialog', 0, -1);
  //   res.status(200).json(dialogs.map(JSON.parse));
  // } catch (err) {
  //   res.status(500).send(err.toString());
  // }
  try {
    // 从查询参数中获取用户ID
    const userId = req.query.user;

    // 从Redis中获取所有对话记录
    const dialogs = await client.lRange('chat dialog', 0, -1);

    // 解析对话记录，并根据用户ID进行过滤
    const userDialogs = dialogs
      .map(JSON.parse) // 将字符串转换为对象
      .filter(dialog => dialog.user === userId);

    res.status(200).json(userDialogs);
  } catch (err) {
    res.status(500).send(err.toString());
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
