export declare const TextEllipsis: import("../utils").WithInstall<import("vue").DefineComponent<{
    rows: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
    dots: {
        type: import("vue").PropType<string>;
        default: string;
    };
    content: {
        type: import("vue").PropType<string>;
        default: string;
    };
    expandText: {
        type: import("vue").PropType<string>;
        default: string;
    };
    collapseText: {
        type: import("vue").PropType<string>;
        default: string;
    };
    position: {
        type: import("vue").PropType<string>;
        default: string;
    };
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, "clickAction"[], "clickAction", import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    rows: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
    dots: {
        type: import("vue").PropType<string>;
        default: string;
    };
    content: {
        type: import("vue").PropType<string>;
        default: string;
    };
    expandText: {
        type: import("vue").PropType<string>;
        default: string;
    };
    collapseText: {
        type: import("vue").PropType<string>;
        default: string;
    };
    position: {
        type: import("vue").PropType<string>;
        default: string;
    };
}>> & {
    onClickAction?: ((...args: any[]) => any) | undefined;
}, {
    content: string;
    position: string;
    rows: string | number;
    dots: string;
    expandText: string;
    collapseText: string;
}, {}>>;
export default TextEllipsis;
export { textEllipsisProps } from './TextEllipsis';
export type { TextEllipsisProps } from './TextEllipsis';
export type { TextEllipsisInstance, TextEllipsisThemeVars } from './types';
declare module 'vue' {
    interface GlobalComponents {
        VanTextEllipsis: typeof TextEllipsis;
    }
}
