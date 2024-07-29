<!-- 智能客服聊天页面 v- 1.0-->
<template>
  <div class="chat-main">
    <!-- 侧边栏 -->
    <div class="side-bar">
      <div class="toggle-bar">
        <!-- 图标，点击后跳转到AgentMap页面 -->
        <div @click="goToAgentMap()" class="icon go-to-agent" data-tooltip="Go to AgentMap"></div>
      </div>
    </div>

    <div class="main-content">
      <!-- 聊天窗口头部 -->
      <div class="chat-header">
        <h2>智能对话客服</h2>
        <!-- "关于"按钮，点击后跳转到GitHub -->
        <el-tooltip effect="dark" content="跳转到 GitHub 页面" placement="bottom">
          <el-button :disabled="isSending" class="about-button" type="text" @click="goToGithub">
            Github
          </el-button>
        </el-tooltip>
      </div>

      <div class="main-window">
        <!-- 历史记录窗口 -->
        <div class="history-contain">
          <div class="history-header">
            <h3>历史记录</h3>
            <!-- 新建聊天按钮 -->
            <button class="new-chat-button" @click="createNewChat">New Chat</button>
            <!-- 手动保存历史记录按钮 -->
            <button class="save-history-button" @click="saveHistory">Save Chat to History</button>
          </div>
          <!-- 历史聊天记录 -->
          <div class="chat-history">
            <h3>Chat History</h3>
            <div v-for="(history, index) in chatHistory" :key="index" class="chat-history-message"
              @click="continueChat(history)">
              <span>{{ history.summary }}</span>
            </div>
          </div>

        </div>

        <!-- 聊天窗口 -->
        <div class="chat-window" ref="chatWindow">
          <!-- 遍历并渲染每条消息 -->
          <Message v-for="(message, index) in messages" :key="index" :text="message.text" :sender="message.sender" />

        </div>

        <!-- 底部区域，包括输入框、上传按钮和发送按钮 -->


      </div>

      <el-footer class="footer">
        <!-- 文件上传组件 -->
        <el-upload class="upload-demo" ref="upload" action="" :file-list="fileList" :show-file-list="false"
          :before-upload="handleFileUpload" :disabled="isSending" multiple>
          <!-- 自定义上传按钮 -->
          <template v-slot:trigger>
            <el-tooltip effect="dark" content="选择文件" placement="top">
              <el-button :disabled="isSending">
                <i class="el-icon-paperclip" size: small></i>
              </el-button>
            </el-tooltip>
          </template>
        </el-upload>
        <!-- 文件列表 -->
        <ul class="file-list">
          <li v-for="(file, index) in files" :key="index">
            {{ file.name }}
            <el-button type="text" @click="removeFile(index)">删除</el-button>
          </li>
        </ul>
        <!-- 消息输入框 -->
        <el-input v-model="query" placeholder="Type a message" @keyup.enter="sendQuery"
          :disabled="isSending"></el-input>
        <!-- 发送按钮 -->
        <el-button type="primary" @click="sendQuery" :disabled="isSending">发送</el-button>
        <!-- 上传文件按钮 -->
        <el-button type="success" @click="uploadFiles" :disabled="isSending || files.length === 0">上传文件</el-button>
      </el-footer>
    </div>
  </div>
</template>

<script>
import Message from '@/components/Message.vue';
import apiClient from '@/axios';

export default {
  components: {
    Message,
  },
  data() {
    return {
      query: '', // 用户输入的消息
      response: '', // 服务器响应
      messages: [], // 消息列表
      isSending: false, // 是否正在发送消息或上传文件
      files: [], // 待上传的文件列表
      chatHistory: []      // 聊天历史记录
    };
  },
  mounted() {
    this.loadMessages();  // 加载当前聊天记录
    this.loadHistory();   // 加载聊天历史记录
  },
  methods: {
    // 处理文件上传，防止默认上传行为
    handleFileUpload(file) {
      this.files.push(file);
      return false; // 阻止默认上传行为
    },
    // 删除指定索引的文件
    removeFile(index) {
      this.files.splice(index, 1);
    },
    // 发送用户输入的消息
    async sendQuery() {
      if (this.query.trim() === '') return;

      // 添加用户消息到消息列表
      this.messages.push({ text: this.query, sender: 'user' });
      this.scrollToBottom();

      this.isSending = true;

      try {
        // 发送请求到服务器
        const res = await apiClient.post('/ask', {
          query: this.query,
        });
        // 添加服务器响应到消息列表
        this.messages.push({ text: res.data.response, sender: 'bot' });
      } catch (error) {
        console.error(error);
        this.messages.push({ text: '请求失败，请稍后再试。', sender: 'bot' });
      } finally {
        // 清空输入框并重置发送状态
        this.saveMessages();
        this.query = '';
        this.isSending = false;
        this.scrollToBottom();
      }
    },
    // 上传文件
    async uploadFiles() {
      if (this.files.length === 0) {
        alert('请选择要上传的文件');
        return;
      }

      this.isSending = true;

      const formData = new FormData();
      for (let i = 0; i < this.files.length; i++) {
        formData.append('file', this.files[i]);
      }

      try {
        // 发送文件上传请求
        await apiClient.post('/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        // 上传成功消息
        this.messages.push({ text: '文件上传成功', sender: 'bot' });
        this.files = [];
      } catch (error) {
        console.error(error)
        this.messages.push({
          text: `文件上传失败，请稍后再试。错误信息: ${error.response ? error.response.data : error.message
            }`,
          sender: 'bot'
        })
      } finally {
        this.isSending = false
        this.scrollToBottom()
      }
    },
    // 保存当前聊天记录到 localStorage
    saveMessages() {
      // 保存当前聊天记录到 localStorage
      localStorage.setItem('chatMessages', JSON.stringify(this.messages));
    },
    loadMessages() {
      // 从 localStorage 加载当前聊天记录
      const savedMessages = localStorage.getItem('chatMessages');
      if (savedMessages) {
        this.messages = JSON.parse(savedMessages);
      }
    },
    saveHistory() {
      // 保存当前聊天记录到聊天历史记录中，并存储到 localStorage
      this.chatHistory.push({ summary: this.messages.map(msg => msg.text).join(' | '), messages: this.messages });
      localStorage.setItem('chatHistory', JSON.stringify(this.chatHistory));
    },
    loadHistory() {
      // 从 localStorage 加载聊天历史记录
      const savedHistory = localStorage.getItem('chatHistory');
      if (savedHistory) {
        this.chatHistory = JSON.parse(savedHistory);
      }
    },
    createNewChat() {
      // 清空当前聊天记录
      this.messages = [];
      this.saveMessages();
    },
    continueChat(history) {
      // 点击历史记录条目时，将其加载为当前聊天记录
      this.messages = history.messages;
      this.saveMessages();
    },
    handleFileUpload(event) {
      // 处理文件上传
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const content = e.target.result;
          this.messages.push({ sender: 'user', text: content });
          this.saveMessages();
        };
        reader.readAsText(file);
      }
    },

    // 滚动到聊天窗口底部
    scrollToBottom() {
      this.$nextTick(() => {
        const chatWindow = this.$refs.chatWindow;
        chatWindow.scrollTop = chatWindow.scrollHeight;
      });
    },
    // 路由跳转到 AgentMap
    goToAgentMap() {
      this.$router.push({ name: 'AgentMap' });
    },
    // 跳转到 GitHub 页面
    goToGithub() {
      window.open('https://github.com/waywooKwong/CSI-LangChain-LLM-Chatbot', '_blank');
    }
  },
};
</script>

<style lang="scss" scoped>
@import "@/assets/fonts/index";

.chat-main {
  display: flex;
  height: 100%;
}

.main-content {
  display: flex;
  flex: 1;
  flex-direction: column;
}

.chat-header {
  height: 60px;
  padding: 0 10px;
  background-color: rgb(126,18,110);
  border-bottom: 1px solid #f4f4f4;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  color: white;

  h2 {
    margin: 0;
    flex: 1;
    text-align: center;
  }

  .about-button {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    // border-radius: 20%;
    width: 10px; /* 设置按钮宽度 */
    height: 40px; /* 设置按钮高度 */
    display: flex;
    align-items: center;
    justify-content: center;
    background-color:#006bde;
    
    padding: 0;
  }
}

.main-window{
  display: flex;
  height: 100%;
}

.history-contain{
  background-color: #bdbdbd;
  width: 20%;
  h3{
    text-align: center;
  }
}

.chat-window {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  border-bottom: 1px solid #dcdfe6;
}

.footer {
  display: flex;
  padding: 10px;
  background-color: #fff;
}

.footer .el-input {
  flex: 1;
  margin-right: 10px;
}

.upload-demo {
  margin-right: 10px;
}

.file-list {
  list-style: none;
  padding: 0;
  margin: 0 10px 10px 0;
  
}

.file-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f9f9f9;
  padding: 5px;
  border-radius: 3px;
  margin-bottom: 5px;
}

.side-bar {
  height: 100%;
  max-width: 250px;
  z-index: 2;
  background: none;
  display: flex;

  .toggle-bar {
    height: 100%;
    width: 50px;
    background: #222222;
    z-index: 2;
    display: flex;
    flex-flow: column;
    align-items: center;
    padding: 13px;

    .icon {
      margin-bottom: 26px;
      font-size: 24px;
      color: #FFFFFF;
      cursor: pointer;
      position: relative;

      &:before {
        @include icon;
      }

      /* Tooltip styling */
      &::after {
        content: attr(data-tooltip);
        position: absolute;
        top: 50%;
        left: 100%;
        transform: translateY(-50%) translateX(10px); /* 右侧显示并略微偏移 */
        background: #333;
        color: #fff;
        padding: 5px 10px;
        border-radius: 4px;
        white-space: nowrap;
        font-size: 12px; /* 缩小字体 */
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.3s, visibility 0.3s;
        z-index: 10;
      }

      &:hover::after {
        opacity: 1;
        visibility: visible;
      }
    }

    .go-to-agent {
      &:before {
        content: '\E8AF'; /* 请确保这个内容与您的字体图标设置相匹配 */
      }
    }

    .disabled-icon {
      opacity: 0.35;
    }
  }
}
</style>