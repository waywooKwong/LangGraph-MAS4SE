/*! JointJS+ v4.0.1 - HTML5 Diagramming Framework - TRIAL VERSION

Copyright (c) 2024 client IO

 2024-07-24 


This Source Code Form is subject to the terms of the JointJS+ Trial License
, v. 2.0. If a copy of the JointJS+ License was not distributed with this
file, You can obtain one at https://www.jointjs.com/license
 or from the JointJS+ archive as was distributed by client IO. See the LICENSE file.*/


import {
    CONFIRMATION_ICON,
    ENTITY_ICON,
    MESSAGE_ICON,
    USER_INPUT_ICON
} from '../../theme';

export const stencilConfig = {
    shapes: [{
        name: 'FlowchartStart'
    }, {
        name: 'FlowchartEnd'
    }, {
        name: 'Message',
        attrs: {
            label: { text: 'User action' },
            icon: { xlinkHref: USER_INPUT_ICON }
        }
    }, {
        name: 'Message',
        attrs: {
            label: { text: 'Entity' },
            icon: { xlinkHref: ENTITY_ICON }
        }
    }, {
        name: 'Message',
        attrs: {
            label: { text: 'Message' },
            icon: { xlinkHref: MESSAGE_ICON }
        }
    }, {
        name: 'Message',
        attrs: {
            label: { text: 'Confirmation' },
            icon: { xlinkHref: CONFIRMATION_ICON }
        }
    }]
};
