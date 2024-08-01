const { createClient } = require('redis');

// 创建Redis客户端
const client = createClient();

client.on('error', (err) => console.error('Redis Client Error', err));

(async () => {
  await client.connect();
  console.log('Connected to Redis...');

  // 插入消息
  async function saveMessage(user, message) {
    try {
      const dialog = { user, message, timestamp: new Date().toISOString() };
      await client.rPush('chat dialog 0801', JSON.stringify(dialog));
      console.log('Dialog saved:', dialog);
    } catch (err) {
      console.error('Error saving dialog:', err);
    }
  }

  // 测试插入消息
  await saveMessage('Alice', 'Hello, how are you?');
  await saveMessage('Bob', 'Hi Alice!');
  await saveMessage('Alice', 'I\'m good, thank you!');

  // 关闭Redis客户端
  await client.disconnect();
})();
