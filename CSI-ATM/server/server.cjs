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

// //// 更新日志的请求
// app.put('/', (req, res) => {
//   const logId = req.params.id;
//   const newData = req.body;

//   const sql = 'UPDATE Log SET balance = balance - ?, timestamp = ? WHERE id = ?';
//   const values = [newData.message, newData.timestamp, logId];

//   db.query(sql, values, (err, results) => {
//     if (err) {
//       res.status(500).send({ error: 'Failed to update Log' });
//       return;
//     }
//     if (results.affectedRows === 0) {
//       res.status(404).send({ error: 'Log not found' });
//       return;
//     }
//     res.send({ success: 'Log updated successfully' });
//   });
// });


app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
