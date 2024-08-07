<template>
  <div :class="['message', senderClass]">
    <div v-if="avatar === 'text'" class="avatar-text">{{ sender }}</div>
    <div v-else class="avatar-container">
      <img :src="avatar" class="avatar" />
    </div>
    <div class="message-content">
      <div class="sender-name">{{ sender }}</div>
      <div class="message-bubble" :class="bubbleClass">
        <div>
          <!-- 如果是 Markdown 文本，则渲染为 HTML，否则显示错误消息 -->
          <vue-markdown :source="text"></vue-markdown>
        </div>
        <div id="app">
          <LoadingSpinner v-if="text === ' ' && sender === '智能客服机器人'" />
          <!-- 其他内容 -->
        </div>
        <div
          v-if="sender === '智能客服机器人' && status === 'true'"
          class="button-container"
        >
          <el-button type="text" @click="open"
            >如果您对这个方案满意，请点击此处</el-button
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VueMarkdown from "vue-markdown";
import apiClient from "@/axios";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

export default {
  name: "ChatMessage",
  components: {
    LoadingSpinner,
    VueMarkdown,
  },
  props: {
    text: String,
    sender: String,
    status: String,
  },
  data() {
    return {
      showModal: false,
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
      } else if (this.sender === "CodeFormat_QA1") {
        return "qa1";
      } else if (this.sender === "SchedulePlan_QA2") {
        return "qa2";
      } else if (this.sender === "Bot02") {
        return "bot02";
      } else if (this.sender === "bot") {
        return "bot";
      } else {
        return "unknown";
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
      } else if (this.sender === "CodeFormat_QA1") {
        return "qa1-bubble";
      } else if (this.sender === "SchedulePlan_QA2") {
        return "qa2-bubble";
      } else if (this.sender === "Bot02") {
        return "bot02-bubble";
      } else if (this.sender === "bot") {
        return "bot-bubble";
      } else {
        return "unknown-bubble";
      }
    },
    avatar() {
      return this.getAvatar(this.sender);
    },
  },
  methods: {
    checkIfMarkdown(text) {
      // 简单的 Markdown 检测规则
      const markdownPatterns = [
        /#\s/, // 标题
        /\*\*/, // 粗体
        /```\n/, // 代码块
        /!\[.*\]\(.*\)/, // 图片
      ];
      return markdownPatterns.some((pattern) => pattern.test(text));
    },
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
          this.$emit('disable-dropdown');
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
      } else if (sender === "CodeFormat_QA1") {
        return "/icons/QA1.png";
      } else if (sender === "SchedulePlan_QA2") {
        return "/icons/QA2.png";
      } else if (sender === "Bot02") {
        return "/icons/Bot02.png";
      } else if (sender === "bot") {
        return "/icons/Bot.png";
      } else {
        return "/icons/默认.png";
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
      }
    },
  },
};
</script>

<style scoped>
.message {
  display: flex;
  align-items: flex-start; /* 将消息对齐到上边 */
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
}

.message.user {
  flex-direction: row-reverse;
  text-align: right;
}

.message.bot,
.message.project-manager,
.message.tech-leader,
.message.qa1,
.message.qa2,
.message.bot02,
.message.unknown {
  flex-direction: row;
  text-align: left;
}

.avatar-container {
  display: flex;
  align-items: flex-start; /* 将头像对齐到上边 */
  margin-right: 10px;
}

.message .avatar {
  width: 30px;
  height: 30px;
}

.message-content {
  display: flex;
  flex-direction: column;
}

.message .sender-name {
  font-size: 12px;
  color: #ffffff;
  margin-bottom: 5px;
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
  padding: 10px;
  border-radius: 10px;
  word-wrap: break-word;
  word-break: break-all;
}

.user-bubble {
  background-color: rgb(126, 18, 110);
  color: #fff4f4;
  border-bottom-right-radius: 0;
}

.bot-bubble,
.project-manager-bubble,
.tech-leader-bubble,
.qa1-bubble,
.qa2-bubble,
.bot02-bubble,
.unknown-bubble {
  background-color: #f6da87;
  color: #07050b;
  border-bottom-left-radius: 0;
}

.project-manager-bubble {
  background-color: #646e78;
  color: #07050b;
  border-bottom-left-radius: 0;
}

.tech-leader-bubble {
  background-color: #8d98a7;
  color: #07050b;
  border-bottom-left-radius: 0;
}

.qa1-bubble {
  background-color: #dcccbb;
  color: #07050b;
  border-bottom-left-radius: 0;
}

.qa2-bubble {
  background-color: #a7754d;
  color: #07050b;
  border-bottom-left-radius: 0;
}

.bot02-bubble {
  background-color: #eab464;
  color: #07050b;
  border-bottom-left-radius: 0;
}

.unknown-bubble {
  background-color: #e0e0e0;
  color: #07050b;
  border-bottom-left-radius: 0;
}

.button-container {
  margin-top: 10px;
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
</style>
