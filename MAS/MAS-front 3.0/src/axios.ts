// src/axios.ts
import axios from 'axios';

const apiClient = axios.create({
<<<<<<< HEAD
  // baseURL: 'http://10.22.63.73:8000', // 后端服务地址
  baseURL: 'http://10.22.3.87:8000', // 后端服务地址
=======
  baseURL: 'http://10.22.61.174:8000', // 后端服务地址
>>>>>>> 346caec9d158b794f1aa0b030c392b2e49ff8f32
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
