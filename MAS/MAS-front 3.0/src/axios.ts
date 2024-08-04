// src/axios.ts
import axios from 'axios';

const apiClient = axios.create({
<<<<<<< HEAD
  baseURL: 'http://10.22.140.233:8000', // 后端服务地址
=======
  baseURL: 'http://10.22.190.184:8000', // 后端服务地址
>>>>>>> 400682c1743a4fab6d3c46d3a7e89eef681885c5
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
