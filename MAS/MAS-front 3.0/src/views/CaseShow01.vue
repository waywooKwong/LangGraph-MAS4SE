<!-- 案例模板一 -->
<template>
  <div class="chat-main">
    <!-- 侧边栏 -->
    <div class="side-bar">
      <div class="toggle-bar">
        <!-- 图标，点击后跳转到chatview页面 -->
         <div @click="goToChatView()" class="icon go-to-case " data-tooltip="返回案例选择界面">返回</div>
      </div>
    </div>

    <div class="main-content">
      <!-- 聊天窗口头部 -->
      <div class="chat-header">
        <h2>智能对话客服-案例一-******</h2>
      </div>

      <div class="main-window">
        <!-- 聊天窗口 -->
        <div class="chat-window" ref="chatWindow">
          <!-- 遍历并渲染每条消息/ 排除发送者是 'kuangweihua'(我定义发送修改意见的那个 sender 是 'kuangwiehua' :） ) -->
          <Message v-for="(message, index) in messages"  :key="index" :text="message.text" :sender="message.sender" :status="message.status"  />
          <!-- v-if="(message.sender != 'kuangweihua')" -->
          <!-- 如果 sender 是 'kuangwiehua'， 蹦出来提交修改意见的弹框 :） -->
          <div v-if="messages.length > 0 && messages[messages.length - 1].sender === 'kuangweihua'" class="userRequestDialog">
            <el-input v-model="feedback" placeholder="输入您的修改意见" type="textarea" :rows="1" :autosize="{ minRows: 1, maxRows: 2 }"></el-input>
            <el-button @click="userRequest" class=".sendQueryButton">发送</el-button>
          </div>
        </div>
      </div>
    
    </div>

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
      userRequestDialogVisible: false, //用户反馈意见可见性
      userId: 'QC',// 用户ID
      feedback:''
    };
  },
  mounted() {
    this.loadMessages(); // 加载当前聊天记录
    this.loadHistory(); // 加载聊天历史记录
    this.saveUserId(); // 保存用户ID
  },
  beforeRouteEnter(to, from, next) {
    // 组件实例在导航确认前还没创建好，所以要使用 next 回调
    next(vm => {
      vm.saveUserId();
    });
  },
  methods: {
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
          
          // 获取chatHistory数组中的第一个元素作为messages
          if (this.chatHistory.length > 0) {
            this.messages = this.chatHistory[0].messages;
          }
        } else {
          // 如果没有历史记录，则清空历史记录框
          this.chatHistory = '';
        }

        console.log('用户历史记录:', userDialogs);
        //alert('已加载用户历史记录');
      } catch (error) {
        console.error('Error fetching user history records:', error);
        alert('Error fetching user history records');
      }
    },

    goToChatView() {
      this.$router.push({ name: "CaseSelect" });
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
