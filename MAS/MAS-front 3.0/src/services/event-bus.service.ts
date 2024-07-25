/*! JointJS+ v4.0.1 - HTML5 Diagramming Framework - TRIAL VERSION

Copyright (c) 2024 client IO

 2024-07-24 


This Source Code Form is subject to the terms of the JointJS+ Trial License
, v. 2.0. If a copy of the JointJS+ License was not distributed with this
file, You can obtain one at https://www.jointjs.com/license
 or from the JointJS+ archive as was distributed by client IO. See the LICENSE file.*/


import { Observable, Subject, Subscription } from 'rxjs';
import { filter, map } from 'rxjs/operators';
import { mvc } from '@joint/plus';

interface SharedEvent {
    name: string;
    value: any;
}

export class EventBusService implements mvc.Events {

    on: mvc.Events_On<EventBusService>;
    off: mvc.Events_Off<EventBusService>;
    trigger: mvc.Events_Trigger<EventBusService>;
    bind: mvc.Events_On<EventBusService>;
    unbind: mvc.Events_Off<EventBusService>;

    once: mvc.Events_On<EventBusService>;
    listenTo: mvc.Events_Listen<EventBusService>;
    listenToOnce: mvc.Events_Listen<EventBusService>;
    stopListening: mvc.Events_Stop<EventBusService>;

    constructor() {
        Object.assign(this, mvc.Events);
    }

    private _events = new Subject<SharedEvent>();

    events(): Observable<SharedEvent> {
        return this._events.asObservable();
    }

    emit(eventName: string, value?: any): void {
        this._events.next({ name: eventName, value: value });
    }

    subscribe(eventName: string, callback: any): Subscription {
        return this._events.pipe(
            filter(e => e.name === eventName),
            map(e => e.value)
        ).subscribe(callback);
    }
}
