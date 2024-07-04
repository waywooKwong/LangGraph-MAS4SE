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
    password: 'america1',
    database: 'dbsclab2018' //注意在 SCHEMAS 确认
});

db.connect((err) => {
  if (err) {
    throw err;
  }
  console.log('MySQL connected...');
});

app.use(cors());
app.use(bodyParser.json());


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


app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
