export declare const FloatingBubble: import("../utils").WithInstall<import("vue").DefineComponent<{
    gap: {
        type: NumberConstructor;
        default: number;
    };
    icon: StringConstructor;
    axis: {
        type: import("vue").PropType<import("./types").FloatingBubbleAxis>;
        default: import("./types").FloatingBubbleAxis;
    };
    magnetic: import("vue").PropType<import("./types").FloatingBubbleMagnetic>;
    offset: {
        type: import("vue").PropType<import("./types").FloatingBubbleOffset>;
        default: () => {
            x: number;
            y: number;
        };
    };
    teleport: {
        type: import("vue").PropType<string | import("vue").RendererElement | null | undefined>;
        default: string;
    };
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, ("click" | "update:offset" | "offsetChange")[], "click" | "update:offset" | "offsetChange", import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    gap: {
        type: NumberConstructor;
        default: number;
    };
    icon: StringConstructor;
    axis: {
        type: import("vue").PropType<import("./types").FloatingBubbleAxis>;
        default: import("./types").FloatingBubbleAxis;
    };
    magnetic: import("vue").PropType<import("./types").FloatingBubbleMagnetic>;
    offset: {
        type: import("vue").PropType<import("./types").FloatingBubbleOffset>;
        default: () => {
            x: number;
            y: number;
        };
    };
    teleport: {
        type: import("vue").PropType<string | import("vue").RendererElement | null | undefined>;
        default: string;
    };
}>> & {
    onClick?: ((...args: any[]) => any) | undefined;
    "onUpdate:offset"?: ((...args: any[]) => any) | undefined;
    onOffsetChange?: ((...args: any[]) => any) | undefined;
}, {
    offset: import("./types").FloatingBubbleOffset;
    teleport: string | import("vue").RendererElement | null | undefined;
    gap: number;
    axis: import("./types").FloatingBubbleAxis;
}, {}>>;
export default FloatingBubble;
export { floatingBubbleProps } from './FloatingBubble';
export type { FloatingBubbleProps } from './FloatingBubble';
export type { FloatingBubbleThemeVars, FloatingBubbleAxis, FloatingBubbleMagnetic, FloatingBubbleOffset, } from './types';
declare module 'vue' {
    interface GlobalComponents {
        VanFloatingBubble: typeof FloatingBubble;
    }
}
