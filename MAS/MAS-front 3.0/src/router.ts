import Vue from 'vue';
import VueRouter from 'vue-router';
import ChatView from '@/views/ChatView.vue';
import AgentMap from '@/views/AgentMap.vue';
import StartView from '@/views/StartView.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'StartView',
    component: StartView,
  },
  {
    path: '/chat',
    name: 'ChatView',
    component: ChatView,
  },
  {
    path: '/agent-map',
    name: 'AgentMap',
    component: AgentMap,
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
