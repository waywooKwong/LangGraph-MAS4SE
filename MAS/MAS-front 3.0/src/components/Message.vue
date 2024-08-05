<template>
  <div :class="['message', senderClass]">
    <div v-if="avatar === 'text'" class="avatar-text">{{ sender }}</div>
<<<<<<< HEAD
    <div v-else class="avatar-container">
      <img :src="avatar" class="avatar" />
      <div class="sender-name">{{ sender }}</div>
    </div>
    <div class="message-bubble" :class="bubbleClass">
      {{ text }}
      <!-- 仅当发送者是智能客服机器人时显示按钮 -->
      <div
        v-if="sender === '智能客服机器人' && status === 'true'"
        class="button-container"
      >
        <!-- <button @click="handleButtonClick" class="action-button">满意</button> -->
        <!-- 弹窗 -->
        <el-button type="text" @click="open"
          >如果您对这个方案满意，请点击此处</el-button
        >
      </div>
    </div>
=======
    <img v-else :src="avatar" class="avatar" />

    <div class="message-bubble" :class="bubbleClass">{{ text }}</div>
>>>>>>> 030ff2c91c186cce9e9018e47bd7e8a786f97ae3
  </div>
</template>

<script>
<<<<<<< HEAD
import { MessageBox } from "element-ui";
export default {
  name: "ChatMessage",
  props: {
    text: String,
    sender: String,
    status: String,
  },
  data() {
    return {
      showModal: false, // 控制弹窗显示与隐藏
    };
  },
  computed: {
    senderClass() {
      if (this.sender === "user") {
        return "user";
      } else if (this.sender === "智能客服机器人") {
        return "bot";
      } else if (this.sender === "ProjectManager") {
        return "project-manager";
      } else if (this.sender === "TechLeader") {
        return "tech-leader";
      } else if (this.sender === "QA1") {
        return "qa1";
      } else if (this.sender === "QA2") {
        return "qa2";
      } else if (this.sender === "Bot02") {
        return "bot02";
      } else if (this.sender === "bot") {
        return "bot";
      } else {
        return "unknown"; // 处理未知发送者
      }
    },
    bubbleClass() {
      if (this.sender === "user") {
        return "user-bubble";
      } else if (this.sender === "智能客服机器人") {
        return "bot-bubble";
      } else if (this.sender === "ProjectManager") {
        return "project-manager-bubble";
      } else if (this.sender === "TechLeader") {
        return "tech-leader-bubble";
      } else if (this.sender === "QA1") {
        return "qa1-bubble";
      } else if (this.sender === "QA2") {
        return "qa2-bubble";
      } else if (this.sender === "Bot02") {
        return "bot02-bubble";
      } else if (this.sender === "bot") {
        return "bot-bubble";
      } else {
        return "unknown-bubble"; // 处理未知发送者
=======
export default {
  name: 'ChatMessage',
  props: {
    text: String,
    sender: String,
  },
  computed: {
    senderClass() {
      if (this.sender === 'user') {
        return 'user';
      } else if (this.sender === 'bot') {
        return 'bot';
      } else {
        return 'unknown'; // 处理未知发送者
      }
    },
    bubbleClass() {
      if (this.sender === 'user') {
        return 'user-bubble';
      } else if (this.sender === 'bot') {
        return 'bot-bubble';
      } else {
        return 'unknown-bubble'; // 处理未知发送者
>>>>>>> 030ff2c91c186cce9e9018e47bd7e8a786f97ae3
      }
    },
    avatar() {
      return this.getAvatar(this.sender);
<<<<<<< HEAD
    },
  },
  methods: {
    open() {
      this.$confirm(
        "此操作将跳转到定制角色界面，你可以私人定制你的开发团队，是否继续?",
        "提示",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
          center: true,
        }
      )
        .then(() => {
          console.log("跳转成功");

          this.$router.push({ name: "AgentMap" });

          this.handleButtonClick();
          this.$message({
            type: "success",
            message: "跳转成功!",
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消",
          });
        });
    },
    getAvatar(sender) {
      if (sender === "user") {
        return "/icons/用户.png";
      } else if (sender === "智能客服机器人") {
        return "/icons/智能客服机器人.png";
      } else if (sender === "ProjectManager") {
        return "/icons/ProjectManager.png";
      } else if (sender === "TechLeader") {
        return "/icons/TechLeader.png";
      } else if (sender === "QA1") {
        return "/icons/QA1.png";
      } else if (sender === "QA2") {
        return "/icons/QA2.png";
      } else if (sender === "Bot02") {
        return "/icons/Bot02.png";
      } else if (sender === "bot") {
        return "/icons/Bot.png";
      } else {
        return "text"; // 显示发送者文字
      }
    },
    async handleButtonClick() {
      try {
        const response = await apiClient.post("/button-clicked", {
          message: "按钮被点击了",
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        console.log("服务器响应:", data);
      } catch (error) {
        console.error("发送请求时发生错误:", error);
=======
    }
  },
  methods: {
    getAvatar(sender) {
      if (sender === 'user') {
        return '/icons/用户.png';
      } else if (sender === 'bot') {
        return '/icons/Bot.png';
      } else {
        return 'text'; // 显示发送者文字
>>>>>>> 030ff2c91c186cce9e9018e47bd7e8a786f97ae3
      }
    },
  },
};
</script>

<style scoped>
.message {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
}

.message.user {
  flex-direction: row-reverse;
  text-align: right;
}

.message.bot {
  flex-direction: row;
  text-align: left;
}

<<<<<<< HEAD
.message.project-manager {
  flex-direction: row;
  text-align: left;
}

.message.tech-leader {
  flex-direction: row;
  text-align: left;
}

.message.qa1 {
  flex-direction: row;
  text-align: left;
}

.message.qa2 {
  flex-direction: row;
  text-align: left;
}

.message.bot02 {
  flex-direction: row;
  text-align: left;
}

=======
>>>>>>> 030ff2c91c186cce9e9018e47bd7e8a786f97ae3
.message.unknown {
  flex-direction: row;
  text-align: left;
}

<<<<<<< HEAD
.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

=======
>>>>>>> 030ff2c91c186cce9e9018e47bd7e8a786f97ae3
.message .avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin: 0 10px;
}

<<<<<<< HEAD
.message .sender-name {
  
  font-size: 12px;
  color: #ffffff;
  text-align: center;
}

=======
>>>>>>> 030ff2c91c186cce9e9018e47bd7e8a786f97ae3
.message .avatar-text {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin: 0 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ccc;
  color: #fff;
  font-size: 12px;
  text-align: center;
}

.message-bubble {
  max-width: 60%;
  padding: 10px;
  border-radius: 10px;
}

.user-bubble {
<<<<<<< HEAD
  background-color: rgb(126, 18, 110);
=======
  background-color: #7853B2;
>>>>>>> 030ff2c91c186cce9e9018e47bd7e8a786f97ae3
  color: #fff4f4;
  border-bottom-right-radius: 0;
}

.bot-bubble {
  background-color: #f6da87;
  color: #07050b;
  border-bottom-left-radius: 0;
}

<<<<<<< HEAD
.project-manager-bubble {
  background-color: #87f6da;
  color: #07050b;
  border-bottom-left-radius: 0;
}

.tech-leader-bubble {
  background-color: #da87f6;
  color: #07050b;
  border-bottom-left-radius: 0;
}

.qa1-bubble {
  background-color: #f687da;
  color: #07050b;
  border-bottom-left-radius: 0;
}

.qa2-bubble {
  background-color: #87daf6;
  color: #07050b;
  border-bottom-left-radius: 0;
}

.bot02-bubble {
  background-color: #87f6da;
  color: #07050b;
  border-bottom-left-radius: 0;
}

=======
>>>>>>> 030ff2c91c186cce9e9018e47bd7e8a786f97ae3
.unknown-bubble {
  background-color: #f6da87;
  color: #07050b;
  border-bottom-left-radius: 0;
}
<<<<<<< HEAD

.button-container {
  margin-top: 10px; /* 给按钮一个上边距 */
}

.action-button {
  padding: 5px 10px;
  font-size: 14px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.action-button:hover {
  background-color: #0056b3;
}

.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  background: white;
  border: 1px solid #ccc;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
=======
>>>>>>> 030ff2c91c186cce9e9018e47bd7e8a786f97ae3
</style>
