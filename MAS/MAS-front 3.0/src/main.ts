/*! JointJS+ v4.0.1 - HTML5 Diagramming Framework - TRIAL VERSION

Copyright (c) 2024 client IO

 2024-07-24 


This Source Code Form is subject to the terms of the JointJS+ Trial License
, v. 2.0. If a copy of the JointJS+ License was not distributed with this
file, You can obtain one at https://www.jointjs.com/license
 or from the JointJS+ archive as was distributed by client IO. See the LICENSE file.*/


import Vue from 'vue';

import App from './App.vue';
import './styles.scss';

import { EventBusService } from './services/event-bus.service';
import batchDirective from './directives/batch.directive';

import router from './router'; // 导入路由配置

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

Vue.use(ElementUI);

Vue.directive('batch', batchDirective);

Vue.prototype.$eventBusService = new EventBusService();

new Vue({
    router, // 注入路由
    render: h => h(App)
}).$mount('#app');
