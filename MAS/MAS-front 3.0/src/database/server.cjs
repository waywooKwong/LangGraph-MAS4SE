const express = require('express');
const { createClient } = require('redis');
const bodyParser = require('body-parser');

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
app.use(bodyParser.json());

// 存储对话记录的接口
app.post('/save-dialog', async (req, res) => {
  try {
    const { user, message } = req.body;
    const dialog = { user, message, timestamp: new Date().toISOString() };

    await client.rPush('dialogs', JSON.stringify(dialog));
    res.status(200).send('Dialog saved');
  } catch (err) {
    res.status(500).send(err.toString());
  }
});

// 获取对话记录的接口
app.get('/dialogs', async (req, res) => {
  try {
    const dialogs = await client.lRange('dialogs', 0, -1);
    res.status(200).json(dialogs.map(JSON.parse));
  } catch (err) {
    res.status(500).send(err.toString());
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

