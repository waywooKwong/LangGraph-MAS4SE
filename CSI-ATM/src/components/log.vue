<template>
  <div class="container">
    <h1>日志表</h1>
    <table>
      <thead>
        <tr>
          <th>日志编号</th>
          <th>流水时间戳</th>
          <th>流水事件</th>
          <th>流水对象</th>
          <th>流水金额</th>
          <th>状态</th>
          <th>对象编号</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in logs" :key="log.Log_id">
          <td>{{ log.Log_id }}</td>
          <td>{{ log.timestamp }}</td>
          <td>{{ log.event }}</td>
          <td>{{ log.object }}</td>
          <td>{{ log.balance }}</td>
          <td>{{ log.state }}</td>
          <td>{{ log.User_user_id }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      logs: [],
    };
  },
  created() {
    this.ShowLog();
  },
  methods: {
    ShowLog() {
      axios
        .get("http://localhost:3000/ShowLog")
        .then((response) => {
          this.logs = response.data;
        })
        .catch((error) => {
          console.error("获取日志数据失败", error);
        });
    },
  },
};
</script>

<!-- 基础的表格大小已经调整合适，需要调整样式使表格居中显示 -->
<style scoped>
.container {
  position: relative;
  height: 600px;
  width: 1024px;
  /* 设置容器高度和宽度 */
  border: 2px solid #151414;
  /* 外框样式，可以根据需要调整颜色和粗细 */
  padding: 20px;
  /* 外框与内容之间的间距 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
table {
  text-align: center;
  width: 100%;
  border-collapse: collapse;
  border-spacing: 20px;
}
th,
td {
  border: 1px solid black;
  padding: 5px;
  width: 20%;
}
th {
  background-color: #f2f2f2;
}
div{
    display: flex;
    justify-content: center;
}
h1{
    width: 100px;
}
</style>
