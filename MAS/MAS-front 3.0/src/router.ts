import Vue from 'vue';
import VueRouter from 'vue-router';
import ChatView from '@/views/ChatView.vue';
import AgentMap from '@/views/AgentMap.vue';
import StartView from '@/views/StartView.vue';
import { component } from 'vue/types/umd';
import CaseShow from './views/CaseShow.vue';
import CaseShow01 from './views/CaseShow01.vue';
import CaseShow02 from './views/CaseShow02.vue';
import CaseShow03 from './views/CaseShow03.vue';
import CaseShow04 from './views/CaseShow04.vue';

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
    path:'/case-show',
    name: 'CaseShow',
    component:CaseShow,
  },
  {
    path:'/case-show01',
    name: 'CaseShow01',
    component:CaseShow01,
  },
  {
    path:'/case-show02',
    name: 'CaseShow02',
    component:CaseShow02,
  },
  {
    path:'/case-show03',
    name: 'CaseShow03',
    component:CaseShow03,
  },
  {
    path:'/case-show04',
    name: 'CaseShow04',
    component:CaseShow04,
  }




];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
