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

       

        <!-- 用户ID输入对话框 -->
        <el-dialog
          title="输入用户ID"
          :visible.sync="userIdDialogVisible"
          >
          <el-input v-model="userId" placeholder="请输入用户ID"></el-input>
          <span slot="footer" class="dialog-footer">
            <el-button @click="userIdDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveUserId()">保存</el-button>
          </span>
        </el-dialog>

        <!-- 打开抽屉按钮 -->
        <el-tooltip effect="dark" content="打开历史记录" placement="bottom">
          <el-button :disabled="isSending" class="drawer-button" type="text" @click="toggleDrawer">
            历史记录
          </el-button>
        </el-tooltip>
        <!--  下拉选择模型菜单 -->
        <el-dropdown @command="selectOllamaModel" class="model-select-bottom-dropdown">
          <el-button type="primary" class="model-select-bottom">
            Ollama Custom-Made: {{ ModelSelectText }}<i class="model-select"></i>
          </el-button>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="gemma2">gemma2</el-dropdown-item>
            <el-dropdown-item command="llama3.1">llama3.1</el-dropdown-item>
            <el-dropdown-item command="llama3">llama3</el-dropdown-item>
            <el-dropdown-item command="qwen2">qwen2</el-dropdown-item>
            <el-dropdown-item command="glm4">glm4</el-dropdown-item>
            <el-dropdown-item command="phi3">phi3</el-dropdown-item>
            <el-dropdown-item command="yi">yi</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
 
        <!-- 头像按钮，点击后弹出用户ID输入框 -->
        <el-tooltip effect="dark" content="输入用户ID" placement="bottom">
          <el-button :disabled="isSending" class="avatar-button" type="text" @click="openUserIdDialog">
            <i class="el-icon-user">user</i>user
          </el-button>
        </el-tooltip>
        <!-- "关于"按钮，点击后跳转到GitHub -->
        <el-tooltip effect="dark" content="跳转到 GitHub 页面" placement="bottom">
          <el-button :disabled="isSending" class="about-button" type="text" @click="goToGithub">
            Github
          </el-button>
        </el-tooltip>
      </div>

      <div class="main-window">
        <!-- 聊天窗口 -->
        <div class="chat-window" ref="chatWindow">
          <!-- 遍历并渲染每条消息/ 排除发送者是 'kuangweihua'(我定义发送修改意见的那个 sender 是 'kuangwiehua' :） ) -->
          <Message v-for="(message, index) in messages" v-if="!(index === messages.length - 1 && message.sender === 'kuangweihua')"  :key="index" :text="message.text" :sender="message.sender" :status="message.status" />
          <!-- v-if="(message.sender != 'kuangweihua')" -->
          <!-- 如果 sender 是 'kuangwiehua'， 蹦出来提交修改意见的弹框 :） -->
          <div v-if="messages.length > 0 && messages[messages.length - 1].sender === 'kuangweihua'" class="userRequestDialog">
            <el-input v-model="feedback" placeholder="输入您的修改意见" type="textarea" :rows="1" :autosize="{ minRows: 1, maxRows: 2 }"></el-input>
            <el-button @click="userRequest" class=".sendQueryButton">发送</el-button>
          </div>
        </div>
      </div>
      <el-footer class="footer">
        <!-- 文件上传组件 -->
        <el-upload class="upload-demo" ref="upload" action="" :file-list="fileList" :show-file-list="false"
          :before-upload="handleFileUpload" :disabled="isSending" multiple>
          <!-- 自定义上传按钮 -->
          <template v-slot:trigger>
            <el-tooltip effect="dark" content="选择文件" placement="top">
              <el-button :disabled="isSending" class="selectFilesButton">
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
        <el-input v-model="query" placeholder="Type a message" @keyup.enter.native="sendQuery" :disabled="isSending"
          type="textarea" :rows="1" :autosize="{ minRows: 1, maxRows: 2 }"></el-input>
        <!-- 发送按钮 -->
        <el-button @click="sendQuery" :disabled="isSending" class="sendQueryButton">发送</el-button>
        <!-- 上传文件按钮 -->
        <el-button @click="uploadFiles" :disabled="isSending || files.length === 0"
          class="uploadFilesButton">上传文件</el-button>

      </el-footer>
    </div>

    <!-- 抽屉组件 -->
    <el-drawer class="history-drawer-contain"
      title="历史记录"
      :visible.sync="drawerVisible"
      direction="ltr"
      size="20%">
      <div class="history-contain">
        <div class="history-header">
        
          <button @click="saveDialog">上传数据库</button>
          <!-- 新建聊天按钮 -->
          <button class="new-chat-button" @click="createNewChat">新建对话</button>
          <!-- 手动保存历史记录按钮 -->
          <button :disabled="messages.length === 0" class="save-history-button" @click="saveHistory">保存对话</button>
          <!-- 清除历史记录按钮 -->
          <button class="clear-history-button" @click="clearHistory">清除记录</button>
        </div>
        <!-- 历史聊天记录 -->
        <div class="chat-history">
          <div v-for="(history, index) in chatHistory" :key="index" class="chat-history-message"
            @click="continueChat(history)">
            <span>{{ history.summary }}</span>
          </div>
        </div>
      </div>
    </el-drawer>
  </div> 
</template>

<script>
import Message from '@/components/Message.vue';
import apiClient from '@/axios';
import axios from 'axios';


export default {
  components: {
    Message,
  },
  data() {
    return {
      query: "", // 用户输入的消息
      messages: [], // 消息列表
      isSending: false, // 是否正在发送消息或上传文件
      files: [], // 待上传的文件列表
      chatHistory: [], // 聊天历史记录
      drawerVisible: false, // 抽屉是否可见
      client: null, // WebSocket 客户端实例 1
      clientUserRequest: null, // WebSocket 客户端实例 2: 专用于处理用户反馈修改信息
      ModelSelectText: 'None', // 当前选择的模型文本
      userIdDialogVisible: false, // 用户ID输入对话框可见性
      userRequestDialogVisible: false, //用户反馈意见可见性
      userId: '',// 用户ID
      feedback:''
    };
  },
  mounted() {
    this.loadMessages(); // 加载当前聊天记录
    this.loadHistory(); // 加载聊天历史记录
    this.initWebSocket(); // 初始化 WebSocket 连接
  },
  methods: {
    async saveDialog() {
      try {
        const response = await axios.post('http://localhost:3000/save-dialog', {
          user: this.userId,
          message: this.chatHistory,
        });
        console.log(response.data);
        alert("Message saved successfully");
      } catch (error) {
        console.error("Error saving message:", error);
        alert("Error saving message");
      }
    },

     // 保存用户ID
    async saveUserId() {
      console.log('用户ID:', this.userId);
      this.userIdDialogVisible = false;
      // 在这里进一步处理用户ID的逻辑，连接数据库，检查用户id下是否含有历史记录，如果有历史记录，则取出放到历史记录框中
         try {
        // 发送请求以获取用户ID下的历史记录
        const response = await axios.get(`http://localhost:3000/dialogs?user=${this.userId}`);
        const userDialogs = response.data;

        if (userDialogs.length > 0) {
          // 按时间戳排序，获取最新的历史记录
          const latestDialog = userDialogs.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))[0];
          
          // 将最新的历史记录里的消息放到历史记录框中
          this.chatHistory = latestDialog.message;
        } else {
          // 如果没有历史记录，则清空历史记录框
          this.chatHistory = '';
        }

        console.log('用户历史记录:', userDialogs);
      } catch (error) {
        console.error('Error fetching user history records:', error);
        alert('Error fetching user history records');
      }
    },
    initWebSocket() {
      this.client = new WebSocket("ws://localhost:8000/ws/run_workflow");

      this.client.onmessage = (event) => {
        const message = JSON.parse(event.data);

        if (message.message) {
            this.messages.push({ text: message.message, sender: message.sender, status: message.progress });
            this.userRequestDialogVisible = false
            if(message.sender=='kuangweihua')
              this.userRequestDialogVisible = true
        } else {
          console.log("Received JSON without message field:", message);
          this.messages.push({
            text: JSON.stringify(message, null, 2),
            sender: "bot",
            status: "false"
          });
        }
        this.saveMessages();
        this.scrollToBottom();

        this.isSending = true;

        this.client.onerror = (error) => {
          console.error("WebSocket Client Error", error);
        };
      };

      // 初始化 userRequest WebSocket
      this.clientUserRequest = new WebSocket("ws://localhost:8000/ws/userRequest");
      this.clientUserRequest.onopen = () => {
        console.log('WebSocket connection for userRequest established');
      };
      this.clientUserRequest.onmessage = (event) => {
        console.log('Message from server (userRequest):', event.data);
      };
      this.clientUserRequest.onclose = () => {
        console.log('WebSocket connection for userRequest closed');
      };
      this.clientUserRequest.onerror = (error) => {
        console.error('WebSocket error (userRequest):', error);
      };
    },
    
    userRequest() {
      if (this.clientUserRequest && this.clientUserRequest.readyState === WebSocket.OPEN) {
        this.clientUserRequest.send(this.feedback);
        this.feedback = '已提交完成'; // 清空输入框
      }
    },
  
    // 打开用户ID输入对话框
    openUserIdDialog() {
      this.userIdDialogVisible = true;
    },

   
    
    toggleDrawer() {
      this.drawerVisible = !this.drawerVisible;
    },
    handleFileUpload(file) {
      this.files.push(file);
      return false; // 阻止默认上传行为
    },
    removeFile(index) {
      this.files.splice(index, 1);
    },
    // 与客服机器人对话
    async sendQuery() {
      if (this.query.trim() === "") return;

      this.messages.push({ text: this.query, sender: "user" ,status:"false"});
      this.scrollToBottom();

      this.isSending = true;

      try {
        const res = await apiClient.post("/ask", {
          query: this.query,
        });
        const response = res.data;
        console.log(response.message)
        console.log(response.sender)
        console.log(response.progress)
        if (response.message) {
          this.messages.push({
            text: response.message,
            sender: response.sender,
            status: String(response.progress)
            
          });
        } else {
          this.messages.push({
            text: JSON.stringify(response, null, 2),
            sender: "bot",
            status: "false"
          });
        }
        // this.messages.push({ text: response, sender: response.sender });
      } catch (error) {
        console.error(error);
        this.messages.push({ text: "请求失败，请稍后再试。", sender: "bot" ,status:"false"});
      } finally {
        this.saveMessages();
        this.query = "";
        this.isSending = false;
        this.scrollToBottom();
      }
    },
    // 上传文件
    async uploadFiles() {
      if (this.files.length === 0) {
        alert("请选择要上传的文件");
        return;
      }

      this.isSending = true;

      const formData = new FormData();
      for (let i = 0; i < this.files.length; i++) {
        formData.append("file", this.files[i]);
      }

      try {
        await apiClient.post("/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        this.messages.push({ text: "文件上传成功", sender: "bot" ,status:"false"});
        this.files = [];
      } catch (error) {
        console.error(error);
        this.messages.push({
          text: `文件上传失败，请稍后再试。错误信息: ${
            error.response ? error.response.data : error.message
          }`,
          sender: "bot",
          status:"false"
        });
      } finally {
        this.isSending = false;
        this.scrollToBottom();
      }
    },
    saveMessages() {
      localStorage.setItem("chatMessages", JSON.stringify(this.messages));
    },
    loadMessages() {
      const savedMessages = localStorage.getItem("chatMessages");
      if (savedMessages) {
        this.messages = JSON.parse(savedMessages);
      }
    },
    saveHistory() {
      this.chatHistory.push({
        summary: this.messages.map((msg) => msg.text).join(" | "),
        messages: this.messages,
      });
      localStorage.setItem("chatHistory", JSON.stringify(this.chatHistory));
    },
    loadHistory() {
      const savedHistory = localStorage.getItem("chatHistory");
      if (savedHistory) {
        this.chatHistory = JSON.parse(savedHistory);
      }
    },
    clearHistory() {
      this.chatHistory = [];
      localStorage.removeItem("chatHistory");
    },
    createNewChat() {
      this.messages = [];
      this.saveMessages();
    },
    continueChat(history) {
      this.messages = history.messages;
      this.saveMessages();
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const chatWindow = this.$refs.chatWindow;
        chatWindow.scrollTop = chatWindow.scrollHeight;
      });
    },
    goToAgentMap() {
      this.$router.push({ name: "AgentMap" });
    },
    goToGithub() {
      window.open(
        "https://github.com/waywooKwong/CSI-LangChain-LLM-Chatbot",
        "_blank"
      );
    },
    async selectOllamaModel(command) {
      try {
        const res = await apiClient.post("/OllamaMade", { model: command });
        this.$message("已选择 " + command +" 进行模型层级 ( Model SystemPrompt ) 的角色定制");
        this.ModelSelectText = command;
      } catch (error) {
        this.$message.error("请求失败: " + error.message);
      }
    },
  },
};
</script>


<style lang="scss" scoped>
@import "@/assets/fonts/index";

.chat-main {
  display: flex;
  height: 100%;
}

.avatar-button{
 color: #000;
}
.main-content {
  display: flex;
  flex: 1;
  flex-direction: column;
  // margin-bottom: 40px; /* 预留空间给 footer */
}

.chat-header {
  height: 60px;
  padding: 0 10px;
  // background-color: #7853B2;
  // background-image: url('@/background/hback2.png');
  // border-bottom: 1px solid #f4f4f4;
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

  .model-select-bottom-dropdown {
    position: absolute;
    left: 90px;
    top: 50%;
    transform: translateY(-50%);

    .model-select-bottom {
      font-size: 14px;
      width: auto;
      height: 30px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #394398;
      // background-color: #222222;
      border: rgb(251, 248, 248);
      background-color: #dce2fa;
    }

    .model-select {
      font-size: 12px;
    }
  }

  .drawer-button {
    position: absolute;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
    width: 70px;
    /* 自动宽度适应文字 */
    height: 30px;
    /* 自动高度适应文字 */
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #dce2fa;
    color: #394398;
    padding: 0;
  }

  .about-button {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    width: 60px;
    /* 自动宽度适应文字 */
    height: 30px;
    /* 自动高度适应文字 */
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #dce2fa;
    color: #394398;
    padding: 0;
  }
}

.main-window {
  display: flex;
  flex: 1;
  overflow: hidden;
  /* 避免整个窗口的滚动条 */
  justify-content: center;
 
  background-size: cover;
  background-position: center;
}

// .main-window::after {
//   content: '';
//   position: absolute;
//   top: 0;
//   left: 0;
//   width: 100%;
//   height: 100%;
//   background-image: url('@/background/bluebackground.jpg');
//   background-size: cover;
//   background-position: center;
//   opacity: 0.5; /* 设置透明度，范围是 0 到 1 */
//   z-index: -1; /* 使背景图片在内容下方 */
// }
.main-window::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1; /* 使背景图片在内容下方 */
  background-image: linear-gradient(-225deg, #231557 0%, #44107A 29%, #FF1361 67%, #FFF800 100%);
}

.chat-window {
  width: 63%;
  // flex: 1;
  overflow-y: auto;
  /* 仅对话信息框可以滚动 */
  padding: 10px;
  border-bottom: 1px solid #dcdfe6;

  /* 自定义滚动条样式 */
  &::-webkit-scrollbar {
    width: 12px;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
    /* 滚动条轨道背景透明 */
  }

  &::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.2);
    /* 滚动条颜色 */
    border-radius: 10px;
    border: 3px solid transparent;
    /* 为滚动条添加间距 */
    background-clip: content-box;
  }

  &::-webkit-scrollbar-thumb:hover {
    background-color: rgba(0, 0, 0, 0.4);
    /* 悬停时滚动条颜色 */
  }
}

.footer {
  height: 80px;
  display: flex;
  // padding: 10px;
  background-color: #dce2fa;
  align-items: center;
  /* 底部水平对齐 */

  .selectFilesButton {
    height: 30px;
    width: 30px;
    align-items: center;
    justify-content: center;
    display: flex;
  }

  .el-input {
    flex: 1;
    margin-right: 10px;
    display: flex;
    align-items: center;
    top: 10%;
  }

  .sendQueryButton {
    margin-left: 10px;
    background-color: #dbd3e4;
    color: #000;
    font-weight: bold;
  }

  .uploadFilesButton {
    background-color: #dbd3e4;
    color: #000;
    font-weight: bold;
  }

  .wstestButton {
    background-color: #dbd3e4;
    color: #000;
    font-weight: bold;
  }
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
      color: #ffffff;
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
        transform: translateY(-50%) translateX(10px);
        /* 右侧显示并略微偏移 */
        background: #333;
        color: #fff;
        padding: 5px 10px;
        border-radius: 4px;
        white-space: nowrap;
        font-size: 12px;
        /* 缩小字体 */
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
        content: "\E8AF";
        /* 请确保这个内容与您的字体图标设置相匹配 */
      }
    }

    .disabled-icon {
      opacity: 0.35;
    }
  }
}
::v-deep .el-drawer {
  background-image: url('@/background/floral-6475479_1920.png');
  background-size: cover;
  background-position: center;
}

.history-contain {
  padding: 10px; /* 增加内边距 */
  
  h3 {
    text-align: center;
    margin-bottom: 10px;
    /* 增加下边距 */
    color: #333;
  }

  .history-header {
    display: flex;
    flex-direction: column;
    /* 垂直排列按钮 */
    align-items: center;
    /* 居中对齐 */
    margin-bottom: 10px;
    /* 增加下边距 */

    button {
      margin: 5px 0;
      /* 增加上下间距 */
      padding: 5px 10px;
      /* 增加内边距 */
      width: 100%;
      /* 按钮宽度为100% */
      box-sizing: border-box;
      /* 包括内边距和边框在内的宽度和高度 */
    }
  }

  .chat-history {
    display: flex;
    flex-direction: column;
    /* 垂直排列历史记录 */
    gap: 5px;
    /* 增加历史记录之间的间距 */
  }

  .chat-history-message {
    background-color: #fff;
    padding: 5px;
    border-radius: 5px; /* 圆角边框 */

    cursor: pointer;
    transition: background-color 0.3s;
    white-space: nowrap; /* 防止换行 */
    overflow: hidden; /* 隐藏溢出内容 */
    text-overflow: ellipsis; /* 使用省略号表示溢出的文本 */
    &:hover {
      background-color: #f5f5f5;
    }
  }
}

.el-drawer__wrapper {
  .el-drawer__container {
    margin-left: 50px;
    /* 从侧边栏展开 */
  }
}

.userRequestDialog {
    display: flex;
    align-items: center;

  }
  .userRequestDialog input {
    flex: 1;
    margin-top: 15px;
    margin-right: 20px; /* 使按钮和输入框之间有间距 */
    height: 40px;
  }
  .userRequestDialog button {
    font-size: 16px; 
    height: 40px;
    width: 88px;
    margin-left: 10px;
    background-color: #dbd3e4;
    color: #000;
    font-weight: bold;
  }
</style>
