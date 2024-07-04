<template>
  <!-- 账号输入框 -->
  <div>
    <div>账号</div>
    <input
      type="number"
      v-model="withdrawAmount"
      placeholder="输入银行卡账号"
    />
  </div>
  <!-- 密码输入框 -->
  <div>
    <div>密码</div>
    <input type="number" v-model="withdrawPassword" placeholder="输入密码" />
  </div>
  <!-- 金额输入框 -->
  <div>
    <div>存入金额</div>
    <input type="number" v-model="withdrawBalance" placeholder="输入取款金额" />
  </div>
  <!-- 确认密码 -->
  <div>
    <button @click="WithDraw">确认</button>
  </div>
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      userData: [],
      withdrawAmount: 0, //用户输入的账号
      withdrawPassword: 0, //用户输入的密码
      withdrawBalance: 0, //用户输入存款金额
      balance: 0, //用户余额
      Lable: 0, //判断弹出类型
    };
  },
  created() {
    //从数据库获取数据
    this.fetchData();
  },
  methods: {
    // 账号密码错误警示框
    ShowAmountPasswordWarning() {
      showDialog({
        title: "Warning",
        message: "账号密码错误，请重新输入!!!",
        theme: "round-button",
      }).then(() => {
        // on close
      });
    },
    // 输入正确弹出框
    ShowDialog() {
      var message = `您的余额为：${this.balance}，请确认存入${this.withdrawBalance}钱`;
      showConfirmDialog({
        title: "确认",
        message: message,
      })
        .then(() => {
          // on confirm
        })
        .catch(() => {
          // on cancel
        });
    },
    //点击确认触发事件
    WithDraw() {
      console.log(this.withdrawAmount);
      console.log(this.withdrawPassword);
      console.log(this.withdrawBalance);
      console.log(this.userData);
      if (this.Lable == 0) {
        this.ShowDialog();
      } else if (this.Lable == 1) {
        this.ShowAmountPasswordWarning();
      }
    },
    //获取数据
    fetchData() {
      axios
        .get("http://localhost:3000/UserData")
        .then((response) => {
          this.userData = response.data;
        })
        .catch((error) => {
          console.error("获取日志数据失败", error);
        });
    },
  },
};
</script>
<style scoped>
#app {
  text-align: center;
  margin-top: 50px;
}

input {
  display: block;
  margin: 10px auto;
  padding: 10px;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #358a70;
}
</style>
