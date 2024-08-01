<template>
  <div :class="['message', sender]">
    <img :src="getAvatar(sender)" class="avatar" />

    <div class="message-bubble">
      {{ text.Sender }}
      <!-- 仅当发送者是机器人时显示按钮 -->
      <div v-if="sender === 'bot'" class="button-container">
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
  },
  // data() {
  //   return {
  //     ws: null, // 保存 WebSocket 实例
  //   };
  // },
  methods: {
    getAvatar(sender) {
      if (sender === "user") {
        return "/icons/用户.png";
      } else {
        return "/icons/Bot.png";
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
    // setupWebSocket() {
    //   this.ws = new WebSocket("ws://localhost:8000/showButton");

    //   this.ws.onmessage = (event) => {
    //     const data = JSON.parse(event.data);
    //     console.log(data);
    //     if (data.label) {
    //       this.showButton = data.label; // 根据实际业务逻辑更新显示状态
    //     }
    //   };

    //   this.ws.onerror = (error) => {
    //     console.error("WebSocket error:", error);
    //   };
    // },
  },
  mounted() {
    this.setupWebSocket();
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

.message .avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin: 0 10px;
}

.message-bubble {
  max-width: 60%;
  padding: 10px;
  border-radius: 10px;
  background-color: #f1f1f1;
}

.message.user .message-bubble {
  background-color: #7853b2;
  color: #fff4f4;
  border-bottom-right-radius: 0;
}

.message.bot .message-bubble {
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
