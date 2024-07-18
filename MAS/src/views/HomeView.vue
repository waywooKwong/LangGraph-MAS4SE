<template>
  <div class="chat-container">
    <h1>智能对话系统</h1>
    <div class="chat-window" ref="chatWindow">
      <div v-for="(message, index) in messages" :key="index" :class="['message', message.sender]">
        <p>{{ message.text }}</p>
      </div>
    </div>
    <div class="input-area">
      <input v-model="query" @keypress.enter="sendQuery" placeholder="输入你的问题" />
      <button @click="sendQuery">发送</button>
    </div>
    <div class="file-upload-area">
      <input type="file" multiple @change="handleFileUpload" />
      <button @click="uploadFiles">上传文件</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      query: '',
      messages: [],
      files: []
    }
  },
  methods: {
    async sendQuery() {
      if (this.query.trim() === '') return

      // 添加用户消息
      this.messages.push({ text: this.query, sender: 'user' })
      this.scrollToBottom()

      try {
        const res = await axios.post('http://192.168.174.214:8000/ask', {
          query: this.query
        })
        // 添加机器人回复
        this.messages.push({ text: res.data.response, sender: 'bot' })
      } catch (error) {
        console.error(error)
        // 添加错误消息
        this.messages.push({ text: '请求失败，请稍后再试。', sender: 'bot' })
      } finally {
        this.query = ''
        this.scrollToBottom()
      }
    },
    handleFileUpload(event) {
      this.files = event.target.files
    },
    async uploadFiles() {
      if (this.files.length === 0) {
        alert('请选择要上传的文件')
        return
      }

      const formData = new FormData()
      for (let i = 0; i < this.files.length; i++) {
        formData.append('file', this.files[i])
      }

      try {
        const res = await axios.post('http://192.168.174.214:8000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        // 添加上传成功消息
        this.messages.push({ text: '文件上传成功', sender: 'bot' })
      } catch (error) {
        console.error(error)
        // 添加错误消息
        this.messages.push({
          text: `文件上传失败，请稍后再试。错误信息: ${
            error.response ? error.response.data : error.message
          }`,
          sender: 'bot'
        })
      } finally {
        this.scrollToBottom()
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const chatWindow = this.$refs.chatWindow
        chatWindow.scrollTop = chatWindow.scrollHeight
      })
    }
  }
}
</script>

<style scoped>
.chat-container {
  width: 90%;
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.chat-window {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 20px;
  max-height: 400px;
}

.input-area {
  display: flex;
  margin-bottom: 10px;
}

.file-upload-area {
  display: flex;
  align-items: center;
}

input[type='file'] {
  flex: 1;
  margin-right: 10px;
}

input[type='text'] {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 10px;
}

button {
  padding: 10px 20px;
  border: none;
  background-color: #007bff;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.message {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 8px;
  max-width: 80%;
}

.message.user {
  background-color: #007bff;
  color: #fff;
  align-self: flex-end;
}

.message.bot {
  background-color: #e1e1e1;
  color: #333;
  align-self: flex-start;
}
</style>
