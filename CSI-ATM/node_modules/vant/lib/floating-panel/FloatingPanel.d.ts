import { type ExtractPropTypes } from 'vue';
export declare const floatingPanelProps: {
    height: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
    anchors: {
        type: import("vue").PropType<number[]>;
        default: () => never[];
    };
    duration: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
    contentDraggable: {
        type: BooleanConstructor;
        default: true;
    };
    lockScroll: BooleanConstructor;
    safeAreaInsetBottom: {
        type: BooleanConstructor;
        default: true;
    };
};
export type FloatingPanelProps = ExtractPropTypes<typeof floatingPanelProps>;
declare const _default: import("vue").DefineComponent<{
    height: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
    anchors: {
        type: import("vue").PropType<number[]>;
        default: () => never[];
    };
    duration: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
    contentDraggable: {
        type: BooleanConstructor;
        default: true;
    };
    lockScroll: BooleanConstructor;
    safeAreaInsetBottom: {
        type: BooleanConstructor;
        default: true;
    };
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, ("heightChange" | "update:height")[], "heightChange" | "update:height", import("vue").PublicProps, Readonly<ExtractPropTypes<{
    height: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
    anchors: {
        type: import("vue").PropType<number[]>;
        default: () => never[];
    };
    duration: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
    contentDraggable: {
        type: BooleanConstructor;
        default: true;
    };
    lockScroll: BooleanConstructor;
    safeAreaInsetBottom: {
        type: BooleanConstructor;
        default: true;
    };
}>> & {
    onHeightChange?: ((...args: any[]) => any) | undefined;
    "onUpdate:height"?: ((...args: any[]) => any) | undefined;
}, {
    height: string | number;
    safeAreaInsetBottom: boolean;
    duration: string | number;
    lockScroll: boolean;
    anchors: number[];
    contentDraggable: boolean;
}, {}>;
export default _default;
