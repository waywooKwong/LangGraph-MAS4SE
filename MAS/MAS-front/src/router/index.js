import { createRouter, createWebHistory } from 'vue-router';
import ChatView from '@/views/ChatView.vue';
import AgentMap from '@/views/AgentMap.vue';

const routes = [
  {
    path: '/',
    name: 'ChatView',
    component: ChatView,
  },
  {
    path: '/agent-map',
    name: 'AgentMap',
    component: AgentMap,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
