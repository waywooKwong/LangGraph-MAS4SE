<template>
  <div class="hello">
    <h1>智能对话系统</h1>
    <input v-model="query" placeholder="输入你的问题" />
    <button @click="sendQuery">发送</button>
    <p v-if="response">回复: {{ response }}</p>
  </div>
</template>

<script>
import axios from "axios";
const apiClinet = axios.create({
  baseURL: 'http://192.168.147.33:9090',
  headers:{
    'Content-Type':'application/json'
  }
});

export default {
  data() {
    return {
      query: "",
      response: "",
    };
  },
  methods: {
    async sendQuery() {
      try {
        const res = await apiClinet.post("/query", {
          query: this.query,
        });
        this.response = res.data.response;
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
.hello {
  text-align: center;
  margin-top: 50px;
}
input {
  padding: 10px;
  margin-right: 10px;
}
button {
  padding: 10px;
}
</style>
