// src/axios.ts
import axios from 'axios';

const apiClient = axios.create({
<<<<<<< HEAD
  baseURL: 'http://10.22.188.216:8000', // 后端服务地址
=======
  // baseURL: 'http://10.22.63.73:8000', // 后端服务地址
  baseURL: 'http://10.22.3.87:8000', // 后端服务地址
>>>>>>> 030ff2c91c186cce9e9018e47bd7e8a786f97ae3
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
