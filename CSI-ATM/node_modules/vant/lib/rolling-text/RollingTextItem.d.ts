import { RollingTextDirection } from './types';
export declare const props: {
    figureArr: {
        type: import("vue").PropType<unknown[]>;
        default: () => never[];
    };
    delay: NumberConstructor;
    duration: {
        type: NumberConstructor;
        default: number;
    };
    isStart: BooleanConstructor;
    direction: {
        type: import("vue").PropType<RollingTextDirection>;
        default: RollingTextDirection;
    };
    height: {
        type: NumberConstructor;
        default: number;
    };
};
declare const _default: import("vue").DefineComponent<{
    figureArr: {
        type: import("vue").PropType<unknown[]>;
        default: () => never[];
    };
    delay: NumberConstructor;
    duration: {
        type: NumberConstructor;
        default: number;
    };
    isStart: BooleanConstructor;
    direction: {
        type: import("vue").PropType<RollingTextDirection>;
        default: RollingTextDirection;
    };
    height: {
        type: NumberConstructor;
        default: number;
    };
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, {}, string, import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    figureArr: {
        type: import("vue").PropType<unknown[]>;
        default: () => never[];
    };
    delay: NumberConstructor;
    duration: {
        type: NumberConstructor;
        default: number;
    };
    isStart: BooleanConstructor;
    direction: {
        type: import("vue").PropType<RollingTextDirection>;
        default: RollingTextDirection;
    };
    height: {
        type: NumberConstructor;
        default: number;
    };
}>>, {
    height: number;
    duration: number;
    direction: RollingTextDirection;
    figureArr: unknown[];
    isStart: boolean;
}, {}>;
export default _default;
