<template>
  <div class="container">
    <h1>日志表</h1>
    <el-table
      :data="logs"
      style="width: 100%"
      border
      height="100%"
      :header-cell-style="{ background: '#f2f2f2' }"
      row-class-name="table-row-class"
    >
      <el-table-column
        prop="Log_id"
        label="日志编号"
        width="90"
      ></el-table-column>
      <el-table-column
        prop="timestamp"
        label="流水时间戳"
        width="210"
      ></el-table-column>
      <el-table-column
        prop="event"
        label="流水事件"
        width="100"
      ></el-table-column>
      <el-table-column
        prop="object"
        label="流水对象"
        width="auto"
      ></el-table-column>
      <el-table-column
        prop="balance"
        label="流水金额"
        width="auto"
      ></el-table-column>
      <el-table-column prop="state" label="状态" width="50"></el-table-column>
      <el-table-column
        prop="User_user_id"
        label="对象编号"
        width="90"
      ></el-table-column>
    </el-table>
  </div>
</template>
<script>
import axios from "axios"
export default {
  data() {
    return {
      logs: [],
    }
  },
  created() {
    this.ShowLog()
  },
  methods: {
    ShowLog() {
      axios
        .get("http://localhost:3000/ShowLog")
        .then((response) => {
          this.logs = response.data
        })
        .catch((error) => {
          console.error("获取日志数据失败", error)
        })
    },
  },
}
</script>
<style scoped>
.container {
  position: relative;
  height: 600px;
  width: 1024px;
  border: 2px solid #151414;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
