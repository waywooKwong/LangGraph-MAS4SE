import Vue from 'vue';
import Router from 'vue-router';
import ChatView from '@/views/ChatView.vue'; 
import AgentMap from '@/views/AgentMap.vue'; 

Vue.use(Router);

const routes = [
    { path: '/', name: 'ChatView', component: ChatView },  // 添加 name
    { path: '/agent-map', name: 'AgentMap', component: AgentMap }  // 添加 name
];

const router = new Router({
    mode: 'history', // 使用 HTML5 历史模式
    routes
});

export default router;
