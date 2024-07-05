<template>
  <!-- 账号输入框 -->
  <div>
    <div>账号</div>
    <input
      type="number"
      v-model="withdrawAmount"
      placeholder="输入银行卡账号"
      @input="handleAccountChange"
    />
    <div>{{ this.accountError }}</div>
  </div>
  <!-- 密码输入框 -->
  <div>
    <div>密码</div>
    <input
      type="number"
      v-model="withdrawPassword"
      placeholder="输入密码"
      @input="handlePasswordChange"
    />
    <div>{{ this.passwordError }}</div>
  </div>
  <!-- 金额输入框 -->
  <div>
    <div>取款金额</div>
    <input
      type="number"
      v-model="withdrawBalance"
      placeholder="输入取款金额"
      @input="handleBalanceChange"
    />
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
      userData: {},
      withdrawAmount: "", //用户输入的账号
      withdrawPassword: "", //用户输入的密码
      withdrawBalance: "", //用户输入取款金额
      balance: 0, //用户余额
      Lable: 0, //判断弹出类型 0:账户密码均正确 1：账户密码有一个错误 2：取款金额超出限度
      accountError: "", //用于账号错误判断
      passwordError: "", //用于密码错误判断
      timeStamp: 0, //当前时间
      formattedDateTime: "", // 格式化后的日期时间
      nowEvent: "drawMoney", //存款事件
      nowobject: "", //当前用户
      state: 0, //状态
      User_user_id: "", //用户id
    };
  },
  created() {
    this.timeStamp = this.getTimeStamp(); // 获取当前时间戳
    this.formattedDateTime = this.formatDateTime(this.timeStamp); // 转换为指定格式
  },
  methods: {
    //清空所有输入
    Clean() {
      this.withdrawAmount = "";
      this.withdrawBalance = "";
      this.withdrawPassword = "";
    },
    //获取当前时间
    getTimeStamp() {
      return new Date().getTime(); // 获取当前时间戳
    },
    //格式化时间
    formatDateTime(timestamp) {
      let date = new Date(timestamp);
      let year = date.getFullYear();
      let month = String(date.getMonth() + 1).padStart(2, "0");
      let day = String(date.getDate()).padStart(2, "0");
      let hours = String(date.getHours()).padStart(2, "0");
      let minutes = String(date.getMinutes()).padStart(2, "0");
      let seconds = String(date.getSeconds()).padStart(2, "0");
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    },
    // 账号密码错误警示框
    ShowAmountPasswordWarning() {
      showDialog({
        title: "Warning",
        message: "账号密码错误，请重新输入!!!",
        theme: "round-button",
      }).then(() => {
        // on close
        this.Clean();
      });
    },
    //输入金额超限警示框
    ShowBalanceWarning() {
      //如果取款金额超出50000
      showDialog({
        title: "金额超限",
        message: "每日取款金额限度50000元！！！",
        theme: "round-button",
      }).then(() => {
        // on close
        this.Clean();
      });
    },
    //余额不足警示框
    ShowBalanceLackWaring() {
      //如果取款金额超余
      showDialog({
        title: "余额不足",
        message: `余额为${this.balance},请重新输入取款金额!!!`,
        theme: "round-button",
      }).then(() => {
        // on close
        this.Clean();
      });
    },
    // 输入正确弹出框
    ShowDialog() {
      var message = `您的余额为：${this.balance}，请确认取出${this.withdrawBalance}元`;
      showConfirmDialog({
        title: "确认",
        message: message,
      })
        .then(() => {
          // 确认账户、密码、金额输入合法后，数据发送更新请求
          this.updateUserData();
          //更新日志

          this.state = 1;
          console.log(
            "当前时间",
            this.formattedDateTime,
            this.nowEvent,
            this.nowobject,
            this.balance,
            this.state,
            this.User_user_id
          );
          //更新日志
          this.updateLog();
          //显示成功
          showDialog({
            message: `成功取出${this.withdrawBalance}元`,
          }).then(() => {
            // on close
          });
          //清空所有内容
          clean();
        })
        .catch(() => {
          // on cancel
        });
    },
    //点击确认触发事件
    WithDraw() {
      if (this.Lable == 0) {
        this.ShowDialog();
      } else if (this.Lable == 1) {
        this.ShowAmountPasswordWarning();
      } else if (this.Lable == 2) {
        this.ShowBalanceWarning();
      } else {
        this.ShowBalanceLackWaring();
      }
    },
    //// 在这里处理账号输入框变化后的逻辑
    handleAccountChange() {
      console.log("账号输入框变化后的值:", this.withdrawAmount);
      const account = String(this.withdrawAmount);
      console.log("账号长度", account.length);
      // 检查账号长度
      if (account.length > 16) {
        this.withdrawAmount = account.slice(0, 16); // 截取前三个字符
        this.accountError = "账号长度不能超过十六位!!!";
      } else if (account.length < 16) {
        this.accountError = "请输入十六位账号";
      } else {
        this.accountError = ""; // 清空错误提示
      }
      if (typeof account === "string" && account.length === 16) {
        console.log("当前账号长度:", account.length);
        this.fetchData(account);
      }
    },
    //在这里处理密码输入框变化后的逻辑
    handlePasswordChange() {
      const password = String(this.withdrawPassword);
      console.log("密码长度", password.length);
      // 检查密码长度
      if (password.length > 6) {
        this.withdrawPassword = password.slice(0, 6); // 截取前六个字符
        this.passwordError = "密码长度不能超过六位!!!";
      } else if (password.length < 6) {
        this.passwordError = "请输入六位数字密码";
      } else {
        this.passwordError = ""; // 清空错误提示
      }
      if (typeof password === "string" && password.length === 6) {
        console.log("当前密码长度:", password.length);
        if (this.userData && password === this.userData.password) {
          console.log("密码输入正确", password);
          // 进行其他操作，获取用户名
          this.nowobject = this.userData.account;
          this.User_user_id = this.userData.user_id;
        } else {
          console.log("密码错误!!!，请重新输入");
          this.Lable = 1;
        }
      }
    },
    //在这里处理金额输入框变化后的逻辑
    handleBalanceChange() {
      //转换类型
      const money = parseInt(this.withdrawBalance, 10);
      const nowBalance = parseInt(this.balance, 10);
      if (money > 50000) {
        this.Lable = 2;
      } else if (money > nowBalance) {
        this.Lable = 3;
      } else {
        this.Lable = 0;
      }
      //判断账号密码是否正确
      this.handlePasswordChange();
    },

    //获取数据库数据
    fetchData(myAccount) {
      axios
        .get("http://localhost:3000/UserData", {
          params: {
            account: myAccount, // 将账号作为查询参数传递给后端
          },
        })
        .then((response) => {
          this.userData = response.data;
          console.log("获取到的用户数据:", this.userData);
          this.Lable = 0; //账户正确，暂时置零
          this.balance = this.userData.balance;
        })
        .catch((error) => {
          console.error("获取用户数据失败", error);
          this.Lable = 1; //账户错误，置1
        });
    },
    //更改数据库用户表信息
    updateUserData() {
      axios
        .put("http://localhost:3000/outBalance", {
          balance: this.withdrawBalance,
          account: this.withdrawAmount,
        })
        .then((response) => {
          console.log(response.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    //更新日志
    updateLog() {
      // 检查所有必填字段是否已被赋值
      console.log("当前时间");
      axios
        .post("http://localhost:3000/inBalanceInsertLog", {
          timestamp: this.formattedDateTime,
          event: this.nowEvent,
          object: this.nowobject,
          balance: this.withdrawBalance,
          state: this.state,
          User_user_id: this.User_user_id,
        })
        .then((response) => {
          console.log("日志插入成功：", response.data);
        })
        .catch((error) => {
          console.error("日志插入失败：", error);
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
