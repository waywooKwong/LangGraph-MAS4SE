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
import LoadPage from '@/views/LoadPage.vue';
import LoadPageTest from './views/LoadPageTest.vue';
import MainSidebar from './components/MainSidebar.vue';
import CaseSelect from './views/CaseSelect.vue';
import AnimationBackground from './components/AnimationBackground.vue';

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
    path: '/CaseSelect',
    name: 'CaseSelect',
    component: CaseSelect,
  },
  {
    path: '/lt',
    name: 'LoadPageTest',
    component: LoadPageTest,
  },
  {
    path: '/AB',
    name: 'AnimationBackground',
    component: AnimationBackground,
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
