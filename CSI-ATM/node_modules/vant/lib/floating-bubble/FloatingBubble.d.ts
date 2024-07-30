import { PropType, type ExtractPropTypes } from 'vue';
import { FloatingBubbleAxis, FloatingBubbleMagnetic, FloatingBubbleOffset } from './types';
export declare const floatingBubbleProps: {
    gap: {
        type: NumberConstructor;
        default: number;
    };
    icon: StringConstructor;
    axis: {
        type: PropType<FloatingBubbleAxis>;
        default: FloatingBubbleAxis;
    };
    magnetic: PropType<FloatingBubbleMagnetic>;
    offset: {
        type: PropType<FloatingBubbleOffset>;
        default: () => {
            x: number;
            y: number;
        };
    };
    teleport: {
        type: PropType<string | import("vue").RendererElement | null | undefined>;
        default: string;
    };
};
export type FloatingBubbleProps = ExtractPropTypes<typeof floatingBubbleProps>;
declare const _default: import("vue").DefineComponent<{
    gap: {
        type: NumberConstructor;
        default: number;
    };
    icon: StringConstructor;
    axis: {
        type: PropType<FloatingBubbleAxis>;
        default: FloatingBubbleAxis;
    };
    magnetic: PropType<FloatingBubbleMagnetic>;
    offset: {
        type: PropType<FloatingBubbleOffset>;
        default: () => {
            x: number;
            y: number;
        };
    };
    teleport: {
        type: PropType<string | import("vue").RendererElement | null | undefined>;
        default: string;
    };
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, ("click" | "update:offset" | "offsetChange")[], "click" | "update:offset" | "offsetChange", import("vue").PublicProps, Readonly<ExtractPropTypes<{
    gap: {
        type: NumberConstructor;
        default: number;
    };
    icon: StringConstructor;
    axis: {
        type: PropType<FloatingBubbleAxis>;
        default: FloatingBubbleAxis;
    };
    magnetic: PropType<FloatingBubbleMagnetic>;
    offset: {
        type: PropType<FloatingBubbleOffset>;
        default: () => {
            x: number;
            y: number;
        };
    };
    teleport: {
        type: PropType<string | import("vue").RendererElement | null | undefined>;
        default: string;
    };
}>> & {
    onClick?: ((...args: any[]) => any) | undefined;
    "onUpdate:offset"?: ((...args: any[]) => any) | undefined;
    onOffsetChange?: ((...args: any[]) => any) | undefined;
}, {
    offset: FloatingBubbleOffset;
    teleport: string | import("vue").RendererElement | null | undefined;
    gap: number;
    axis: FloatingBubbleAxis;
}, {}>;
export default _default;
