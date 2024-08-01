// src/axios.ts
import axios from 'axios';

const apiClient = axios.create({
<<<<<<< HEAD
  // baseURL: 'http://10.22.63.73:8000', // 后端服务地址
  baseURL: 'http://10.22.3.87:8000', // 后端服务地址
=======
  baseURL: 'http://10.22.64.78:8000', // 后端服务地址
>>>>>>> e35378e538dbd2c386e735f26065b3b09618cddc
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
