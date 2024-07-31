// src/axios.ts
import axios from 'axios';

const apiClient = axios.create({
<<<<<<< HEAD
  // baseURL: 'http://10.22.63.73:8000', // 后端服务地址
  baseURL: 'http://10.22.3.87:8000', // 后端服务地址
=======
  baseURL: 'http://10.22.61.174:8000', // 后端服务地址
>>>>>>> fe9141ce40a1b9849dfa104074f8e47ecabb31a5
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
