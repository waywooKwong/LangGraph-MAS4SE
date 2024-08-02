<template>
  <div :class="['message', senderClass]">
    <div v-if="avatar === 'text'" class="avatar-text">{{ sender }}</div>
    <img v-else :src="avatar" class="avatar" />
    <div class="message-bubble" :class="bubbleClass">
      {{ text }}
      <!-- 仅当发送者是机器人时显示按钮 -->
      <div
        v-if="sender === '智能客服机器人' && status === 'true'"
        class="button-container"
      >
        <button @click="handleButtonClick" class="action-button">满意</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ChatMessage",
  props: {
    text: String,
    sender: String,
    status: String,
  },
  computed: {
    senderClass() {
      if (this.sender === "user") {
        return "user";
      } else if (this.sender === "智能客服机器人") {
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
      } else {
        return "unknown-bubble"; // 处理未知发送者
      }
    },
    avatar() {
      return this.getAvatar(this.sender);
    },
  },
  methods: {
    getAvatar(sender) {
      if (sender === "user") {
        return "/icons/用户.png";
      } else if (sender === "bot") {
        return "/icons/Bot.png";
      } else {
        return "text"; // 显示发送者文字
      }
    },
    async handleButtonClick() {
      try {
        const response = await fetch("http://localhost:8000/button-clicked", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message: "按钮被点击了" }),
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        console.log("服务器响应:", data);
      } catch (error) {
        console.error("发送请求时发生错误:", error);
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

.message.unknown {
  flex-direction: row;
  text-align: left;
}

.message .avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin: 0 10px;
}

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
  background-color: rgb(126, 18, 110);
  color: #fff4f4;
  border-bottom-right-radius: 0;
}

.bot-bubble {
  background-color: #f6da87;
  color: #07050b;
  border-bottom-left-radius: 0;
}

.unknown-bubble {
  background-color: #f6da87;
  color: #07050b;
  border-bottom-left-radius: 0;
}

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
</style>
