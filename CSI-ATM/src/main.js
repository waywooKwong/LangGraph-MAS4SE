import './assets/main.css'

import { createApp } from 'vue'


import App from './App.vue'
import router from './router'

// 引入 ElementPlus , 管理员登录界面的对话框
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';


const app = createApp(App)
app.use(router)

app.use(ElementPlus);
app.mount('#app')
