/*! JointJS+ v4.0.1 - HTML5 Diagramming Framework - TRIAL VERSION

Copyright (c) 2024 client IO

 2024-07-24 


This Source Code Form is subject to the terms of the JointJS+ Trial License
, v. 2.0. If a copy of the JointJS+ License was not distributed with this
file, You can obtain one at https://www.jointjs.com/license
 or from the JointJS+ archive as was distributed by client IO. See the LICENSE file.*/


import { dia, elementTools } from '@joint/plus';

export const RemoveTool = elementTools.Remove.extend({
    options: {
        useModelGeometry: true,
        action: (evt: dia.Event, cellView: dia.CellView): void => {
            cellView.notify('cell:tool:remove', evt);
        },
        markup: [{
            tagName: 'circle',
            selector: 'button',
            attributes: {
                'r': 10,
                'fill': '#FD0B88',
                'cursor': 'pointer',
                'data-tooltip': 'Remove <i>(Del)</i>',
                'data-tooltip-position': 'bottom'
            }
        }, {
            tagName: 'path',
            selector: 'icon',
            attributes: {
                'd': 'M -4 -4 4 4 M -4 4 4 -4',
                'fill': 'none',
                'stroke': '#FFFFFF',
                'stroke-width': 2,
                'pointer-events': 'none'
            }
        }]
    }
});
