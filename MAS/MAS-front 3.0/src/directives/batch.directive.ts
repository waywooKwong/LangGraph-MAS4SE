/*! JointJS+ v4.0.1 - HTML5 Diagramming Framework - TRIAL VERSION

Copyright (c) 2024 client IO

 2024-07-24 


This Source Code Form is subject to the terms of the JointJS+ Trial License
, v. 2.0. If a copy of the JointJS+ License was not distributed with this
file, You can obtain one at https://www.jointjs.com/license
 or from the JointJS+ archive as was distributed by client IO. See the LICENSE file.*/


import { ObjectDirective } from 'vue';

import { SharedEvents } from '../joint-plus/controller';

const BATCH_NAME = 'inspector-input';

const batchDirective: ObjectDirective = {

    bind(element, binding, vNode): void {
        element.addEventListener('focus', onFocus);
        element.addEventListener('focusout', onFocusOut);

        function onFocus() {
            vNode.context.$eventBusService.emit(SharedEvents.GRAPH_START_BATCH, BATCH_NAME);
        }
        function onFocusOut() {
            vNode.context.$eventBusService.emit(SharedEvents.GRAPH_STOP_BATCH, BATCH_NAME);
        }
    }
};

export default batchDirective;
