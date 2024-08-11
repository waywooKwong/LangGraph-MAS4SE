/*! JointJS+ v4.0.1 - HTML5 Diagramming Framework - TRIAL VERSION

Copyright (c) 2024 client IO

 2024-07-24 


This Source Code Form is subject to the terms of the JointJS+ Trial License
, v. 2.0. If a copy of the JointJS+ License was not distributed with this
file, You can obtain one at https://www.jointjs.com/license
 or from the JointJS+ archive as was distributed by client IO. See the LICENSE file.*/


import Vue from 'vue';
import { Prop, Watch } from 'vue-property-decorator';
import Component from 'vue-class-component';
import { dia } from '@joint/plus';

export interface Properties {
    [property: string]: dia.Path;
}

@Component({} as any)
export abstract class BaseInspector extends Vue {

    @Prop() cell: dia.Cell;

    public props: Properties;

    @Watch('cell')
    onPropertyChanged(currentValue: dia.Cell, previousValue: dia.Cell): void {
        this.removeCellListener(previousValue);
        this.addCellListener(currentValue);
        this.assignFormFields();
    }

    public mounted(): void {
        this.addCellListener(this.cell);
        this.assignFormFields();
    }

    public beforeDestroy(): void {
        this.removeCellListener(this.cell);
    }

    public changeCellProp(path: dia.Path, value: any): void {
        this.cell.prop(path, value);
    }

    protected abstract assignFormFields(): void;

    private addCellListener(cell: dia.Cell): void {
        cell.on('change', () => this.assignFormFields(), this);
    }

    private removeCellListener(cell: dia.Cell): void {
        cell.off(null, null, this);
    }
}

