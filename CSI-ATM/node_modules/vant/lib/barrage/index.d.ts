export declare const Barrage: import("../utils").WithInstall<import("vue").DefineComponent<{
    top: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
    rows: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
    duration: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
    autoPlay: {
        type: BooleanConstructor;
        default: true;
    };
    delay: {
        type: NumberConstructor;
        default: number;
    };
    modelValue: {
        type: import("vue").PropType<import("./Barrage").BarrageItem[]>;
        default: () => never[];
    };
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, "update:modelValue"[], "update:modelValue", import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    top: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
    rows: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
    duration: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
    autoPlay: {
        type: BooleanConstructor;
        default: true;
    };
    delay: {
        type: NumberConstructor;
        default: number;
    };
    modelValue: {
        type: import("vue").PropType<import("./Barrage").BarrageItem[]>;
        default: () => never[];
    };
}>> & {
    "onUpdate:modelValue"?: ((...args: any[]) => any) | undefined;
}, {
    top: string | number;
    modelValue: import("./Barrage").BarrageItem[];
    rows: string | number;
    duration: string | number;
    autoPlay: boolean;
    delay: number;
}, {}>>;
export default Barrage;
export { barrageProps } from './Barrage';
export type { BarrageProps, BarrageItem } from './Barrage';
export type { BarrageInstance, BarrageThemeVars } from './types';
declare module 'vue' {
    interface GlobalComponents {
        VanBarrage: typeof Barrage;
    }
}
