<template>
  <div>
    <h1>实时消息流</h1>
    <div class="message-container">
      <!-- 添加 ref 属性 -->
      <div ref="messageBox" class="message-box">{{ messages }}</div>
    </div>
    <!-- <button @click="startWebSocket">开始 WebSocket 连接</button> -->

    <div class="progress">
      <div v-for="(step, index) in roles" :key="index" class="step-wrapper">
        <div class="circle" :class="{
          done: stepCompleted[index],
          active: index === currentStep - 1,
        }">
          <span class="label">{{ index + 1 }}</span>
          <span class="title">{{ step }}</span>
        </div>
        <!-- 进度条 -->
        <span v-if="index < roles.length - 1" class="bar" :class="{
          done: index < currentStep - 1,
          active: index === currentStep - 2,
        }"></span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      messages: "", // 用于存储和显示流式消息
      socket: null, // WebSocket 实例
      roles: [], // 角色列表
      stepCompleted: [], // 记录每个步骤是否完成
      currentStep: 0, // 当前步骤索引
      stepCheckInterval: null,
      graph_success: false,
    };
  },
  mounted() {
    this.startWebSocket();
    this.startStepCheck();
  },
  beforeDestroy() {
    this.stopStepCheck();
  },
  methods: {
    startStepCheck() {
      this.intervalId = setInterval(() => {
        if (this.graph_success === true) {
          if (this.$route.path !== "/chat") {
            this.stopStepCheck(); // 条件满足时停止定时器
            this.$router.push({ path: "/chat", name: "ChatView" });
          }

        }
      }, 1000); // 每秒检查一次
    },
    stopStepCheck() {
      if (this.intervalId) {
        clearInterval(this.intervalId);
        this.intervalId = null;
      }
    },
    startWebSocket() {
      this.socket = new WebSocket("ws://localhost:8000/ws/stream");

      this.socket.onmessage = (event) => {
        try {
          // 解析 JSON 数据
          const data = JSON.parse(event.data);

          if (data.roles) {
            // 处理角色数据
            this.roles = data.roles;
            this.stepCompleted = new Array(this.roles.length).fill(false);
          } else if (data.message) {
            // 处理消息数据
            this.messages += data.message;

            // 更新步骤条状态
            const roleIndex = this.roles.indexOf(data.role);
            if (roleIndex >= 0 && roleIndex === this.currentStep) {
              this.stepCompleted[this.currentStep] = true;
              this.currentStep++;
            }

            // 自动滚动到最底部
            this.$nextTick(() => {
              const messageBox = this.$refs.messageBox;
              if (messageBox) {
                messageBox.scrollTop = messageBox.scrollHeight;
              }
            });
          } else {
            this.graph_success = data.success;
          }
        } catch (error) {
          console.error("处理消息时发生错误", error);
        }
      };

      this.socket.onopen = () => {
        console.log("WebSocket 连接已打开");
      };

      this.socket.onclose = () => {
        console.log("WebSocket 连接已关闭");
      };

      this.socket.onerror = (error) => {
        console.error("WebSocket 错误", error);
      };
    },
  },
};
</script>

<style scoped>
*,
*:after,
*:before {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Open Sans";
}

/* Progress Steps */
.progress {
  width: 1000px;
  margin: 20px auto;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}

.step-wrapper {
  display: flex;
  align-items: center;
}

.circle,
.bar {
  display: inline-block;
  background: #fff;
}

.circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid #d5d5da;
  position: relative;


}

.bar {
  width: 130px;
  height: 6px;
  margin: 0 -5px;
  border: none;
  border-radius: 0;
  background: #f7f7f7;
  /* 底色黄色 */
}

.circle .label {
  margin-top: 3px;
  display: inline-block;
  width: 32px;
  height: 32px;
  line-height: 32px;
  border-radius: 50%;
  color: #b5b5ba;
  font-size: 17px;
}

.circle .title {
  color: #b5b5ba;
  font-size: 13px;
  line-height: 30px;
  margin-left: -5px;
}

/* Done / Active */
.bar.done,
.circle.done {
  background: #f0f0f0;
  /* 浅黄色 */
}

.bar.active {
  background: linear-gradient(to right,
      #f0f0d6 40%,
      /* 黄色渐变 */
      #f7f7c8 60%);
}

.circle.done .label {
  color: #fff;
  background: #00ff11;
  box-shadow: inset 0 0 2px rgba(0, 0, 0, 0.2);
}

.circle.done .title {
  color: #444;
}

.circle.active .label {
  color: #fff;
  background: #ffa500;
  /* 橙黄色 */
  box-shadow: inset 0 0 2px rgba(0, 0, 0, 0.2);
}

.circle.active .title {
  color: #ffa500;
  /* 橙黄色 */
}

/* Message Container */
.message-container {
  width: 100%;
  height: 300px;
  /* 你可以根据需要调整高度 */
  overflow-y: auto;
  /* 启用垂直滚动条 */
  border: 1px solid #ddd;
  padding: 10px;
  background-color: #f9f9f9;
}

.message-box {
  white-space: pre-wrap;
  /* 保留空格和换行 */
  word-break: break-word;
}
</style>
