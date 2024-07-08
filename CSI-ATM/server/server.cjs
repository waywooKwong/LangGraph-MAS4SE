const express = require('express');
const mysql = require('mysql');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const port = 3000; // 这是固定的端口，最好不要修改

// 1. 此处修改数据库的相关配置
// 2. 根据需求 create table
const db = mysql.createConnection({
  host: 'localhost',
  user: 'myuser',
  password: 'qmyyb763',
  database: 'atm' //注意在 SCHEMAS 确认
});


db.connect((err) => {
  if (err) {
    throw err;
  }
  console.log('MySQL connected...');
});

app.use(cors());
app.use(bodyParser.json());
// 管理员登录
app.get('/AdminLogin', (req, res) => {
  const sql = 'SELECT * FROM Admin WHERE account = ? AND password = ?';
  const newData = req.query;
  const values = [newData.account, newData.password];

  db.query(sql, values, (err, results) => {
    if (err) {
      console.error(err);
      res.status(500).json('false');
    } else {
      if (results.length === 1) {
        // 找到匹配的管理员账号和密码
        res.json('true');
      } else {
        // 未找到匹配的管理员账号和密码
        res.status(404).json('false');
      }
    }
  });
});
//// 获取日志的请求
app.get('/ShowLog', (req, res) => {
  const sql = 'SELECT * FROM Log';
  //3. 此处根据需求修改 SQL 语句
  db.query(sql, (err, results) => {
    if (err) {
      res.status(500).send({ error: 'Failed to access Log' });
      return;
    }
    res.json(results);
  });
});

//// 存款服务的请求
app.put('/inBalance', (req, res) => {
  const newData = req.body;
  const sql = 'UPDATE User SET balance = balance + ? WHERE account = ?';
  const values = [newData.balance, newData.account];

  db.query(sql, values, (err, results) => {
    if (err) {
      res.status(500).send({ error: 'Failed to update User' });
      return;
    }
    if (results.affectedRows === 0) {
      res.status(404).send({ error: 'User table not found' });
      return;
    }
    res.send({ success: 'inBalance updated successfully' });
  });
});
//取款服务请求、更新用户账户
app.put('/outBalance', (req, res) => {
  const newData = req.body;
  const sql = 'UPDATE User SET balance = balance - ? WHERE account = ?';
  const values = [newData.balance, newData.account];

  db.query(sql, values, (err, results) => {
    if (err) {
      res.status(500).send({ error: 'Failed to update User' });
      return;
    }
    if (results.affectedRows === 0) {
      res.status(404).send({ error: 'User table not found' });
      return;
    }
    res.send({ success: 'inBalance updated successfully' });
  });
});
//存款服务更新日志
app.post('/inBalanceInsertLog', (req, res) => {
  const newData = req.body;
  const sql = 'INSERT INTO Log (timestamp, event, object, balance, state, User_user_id) VALUES (?,?,?,?,?,?)';
  const values = [newData.timestamp, newData.event, newData.object, newData.balance, newData.state, newData.User_user_id];

  db.query(sql, values, (err, results) => {
    if (err) {
      console.error('日志插入失败: ', err); // 打印错误信息
      res.status(500).send({ error: 'Failed to update Log' });
      return;
    }
    res.send({ success: 'inBalance updated successfully' });
  });
});

//// 转账服务的请求
app.put('/transBalance', (req, res) => {
  const { balance, account, targetAccount } = req.body;

  // 第一个更新语句
  const sql1 = 'UPDATE User SET balance = balance - ? WHERE account = ?';
  const values1 = [balance, account];

  db.query({ sql: sql1, values: values1, multipleStatements: false }, (err, result1) => {
    if (err) {
      res.status(500).send({ error: 'Failed to update User balance' });
      return;
    }

    if (result1.affectedRows === 0) {
      res.status(404).send({ error: 'Source User not found' });
      return;
    }

    // 第二个更新语句
    const sql2 = 'UPDATE User SET balance = balance + ? WHERE account = ?';
    const values2 = [balance, targetAccount];

    db.query({ sql: sql2, values: values2, multipleStatements: false }, (err, result2) => {
      if (err) {
        res.status(500).send({ error: 'Failed to update User balance' });
        return;
      }

      if (result2.affectedRows === 0) {
        res.status(404).send({ error: 'Target User not found' });
        return;
      }

      res.send({ success: 'Balance updated successfully' });
    });
  });
});


//// 转账服务更新日志
app.post('/transBalanceInsertLog', (req, res) => {
  const newData = req.body;
  const sql = 'INSERT INTO Log (timestamp, event, object, balance, state, User_user_id) VALUES (?,?,?,?,?,?)';
  const values = [newData.timestamp, newData.event, newData.object, newData.balance, newData.state, newData.User_user_id];

  db.query(sql, values, (err, results) => {
    if (err) {
      console.error('日志插入失败: ', err); // 打印错误信息
      res.status(500).send({ error: 'Failed to update Log' });
      return;
    }
    res.send({ success: 'transBalance Log insert successfully' });
  });
});


// GET 请求处理，根据账号 ID 查询用户数据
app.get('/UserData', (req, res) => {
  const account = req.query.account; // 从查询参数中获取账号 ID
  const sql = 'SELECT * FROM User WHERE account = ?'; // 根据账号 ID 查询用户数据的 SQL 语句

  // 执行 SQL 查询
  db.query(sql, [account], (err, results) => {
    if (err) {
      console.error('数据库查询错误:', err);
      res.status(500).json({ error: 'Failed to fetch user data' });
      return;
    }

    if (results.length === 0) {
      res.status(404).json({ error: 'User not found' });
      return;
    }

    // 查询成功，返回查询到的用户数据
    res.json(results[0]); // 假设只返回第一个匹配的用户数据
  });
});


app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
