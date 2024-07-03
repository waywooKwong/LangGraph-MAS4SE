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
    user: 'canteen',
    password: '',
    database: 'dbcanteen' //注意在 SCHEMAS 确认
});

db.connect((err) => {
  if (err) {
    throw err;
  }
  console.log('MySQL connected...');
});

app.use(cors());
app.use(bodyParser.json());


//// 根据需求添加数据库请求 

app.get('/getLog', (req, res) => {
  const { canteen, floor, seat, time } = req.body;
  
  //3. 此处根据需求修改 SQL 语句
  const sql = 'INSERT INTO reservations (id, canteen, floor, seat, time) VALUES (NULL, ?, ?, ?, ?)';
  db.query(sql, [canteen, floor, seat, time], (err, result) => {
    
    if (err) {
      res.status(500).send({ error: 'Failed to save reservation' });
      return;
    }
    res.status(201).send({ message: 'Reservation saved successfully' });
  });
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
