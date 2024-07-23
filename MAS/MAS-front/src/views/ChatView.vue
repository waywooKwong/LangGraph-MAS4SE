<template>
  <div class="chat-main">
    <div class="chat-window" ref="chatWindow">
      <Message
        v-for="(message, index) in messages"
        :key="index"
        :text="message.text"
        :sender="message.sender"
      />
    </div>
    <el-footer class="footer">
      <el-upload
        class="upload-demo"
        ref="upload"
        action=""
        :file-list="fileList"
        :show-file-list="false"
        :before-upload="handleFileUpload"
        :disabled="isSending"
        multiple
      >
        <template v-slot:trigger>
          <el-button size="small" :disabled="isSending">
            <el-icon><Plus /></el-icon>
          </el-button>
        </template>
      </el-upload>
      <ul class="file-list">
        <li v-for="(file, index) in files" :key="index">
          {{ file.name }}
          <el-button type="text" @click="removeFile(index)">删除</el-button>
        </li>
      </ul>
      <el-input
        v-model="query"
        placeholder="Type a message"
        @keyup.enter="sendQuery"
        :disabled="isSending"
      ></el-input>
      <el-button
        type="primary"
        @click="sendQuery"
        :disabled="isSending"
      >Send</el-button>
      <el-button
        type="success"
        @click="uploadFiles"
        :disabled="isSending || files.length === 0"
      >Upload Files</el-button>
    </el-footer>
  </div>
</template>

<script>
import { Plus } from '@element-plus/icons-vue';
import Message from '@/components/Message.vue';
import apiClient from '@/axios';

export default {
  components: {
    Plus,
    Message,
  },
  data() {
    return {
      query: '',
      response: '',
      messages: [],
      isSending: false,
      files: [],
    };
  },
  methods: {
    handleFileUpload(file) {
      this.files.push(file);
      return false; // Prevent default upload behavior
    },
    removeFile(index) {
      this.files.splice(index, 1);
    },
    async sendQuery() {
      if (this.query.trim() === '') return;

      this.messages.push({ text: this.query, sender: 'user' });
      this.scrollToBottom();

      this.isSending = true;

      try {
        const res = await apiClient.post('/ask', {
          query: this.query,
        });
        this.messages.push({ text: res.data.response, sender: 'bot' });
      } catch (error) {
        console.error(error);
        this.messages.push({ text: '请求失败，请稍后再试。', sender: 'bot' });
      } finally {
        this.query = '';
        this.isSending = false;
        this.scrollToBottom();
      }
    },
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
        await apiClient.post('/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        this.messages.push({ text: '文件上传成功', sender: 'bot' });
        this.files = [];
      } catch (error) {
        console.error(error);
        this.messages.push({
          text: `文件上传失败，请稍后再试。错误信息: ${
            error.response ? error.response.data : error.message
          }`,
          sender: 'bot',
        });
      } finally {
        this.isSending = false;
        this.scrollToBottom();
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const chatWindow = this.$refs.chatWindow;
        chatWindow.scrollTop = chatWindow.scrollHeight;
      });
    },
  },
};
</script>

<style scoped>
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
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
</style>
