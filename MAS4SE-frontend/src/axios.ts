// src/axios.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://192.168.137.1:8000', // 后端服务地址
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
