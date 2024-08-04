import Vue from 'vue';
import VueRouter from 'vue-router';
import ChatView from '@/views/ChatView.vue';
import AgentMap from '@/views/AgentMap.vue';
import StartView from '@/views/StartView.vue';
import LoadPage from '@/views/LoadPage.vue';
import MainSidebar from './components/MainSidebar.vue';

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
  {
    path: '/load',
    name: 'LoadPage',
    component: LoadPage,
  },
  {
    path: '/s',
    name: 'MainSidebar',
    component: MainSidebar,
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
