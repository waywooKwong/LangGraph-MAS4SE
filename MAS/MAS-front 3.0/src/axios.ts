// src/axios.ts
import axios from 'axios';

const apiClient = axios.create({
  // baseURL: 'http://192.168.174.214:8000', // 后端服务地址
  baseURL: 'http://192.168.0.33:8000', // 后端服务地址
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
