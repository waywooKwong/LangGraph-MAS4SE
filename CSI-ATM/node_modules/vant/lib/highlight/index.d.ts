export declare const Highlight: import("../utils").WithInstall<import("vue").DefineComponent<{
    autoEscape: {
        type: BooleanConstructor;
        default: true;
    };
    caseSensitive: BooleanConstructor;
    highlightClass: StringConstructor;
    highlightTag: {
        type: import("vue").PropType<keyof HTMLElementTagNameMap>;
        default: keyof HTMLElementTagNameMap;
    };
    keywords: {
        type: import("vue").PropType<string | string[]>;
        required: true;
    };
    sourceString: {
        type: import("vue").PropType<string>;
        default: string;
    };
    tag: {
        type: import("vue").PropType<keyof HTMLElementTagNameMap>;
        default: keyof HTMLElementTagNameMap;
    };
    unhighlightClass: StringConstructor;
    unhighlightTag: {
        type: import("vue").PropType<keyof HTMLElementTagNameMap>;
        default: keyof HTMLElementTagNameMap;
    };
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, {}, string, import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    autoEscape: {
        type: BooleanConstructor;
        default: true;
    };
    caseSensitive: BooleanConstructor;
    highlightClass: StringConstructor;
    highlightTag: {
        type: import("vue").PropType<keyof HTMLElementTagNameMap>;
        default: keyof HTMLElementTagNameMap;
    };
    keywords: {
        type: import("vue").PropType<string | string[]>;
        required: true;
    };
    sourceString: {
        type: import("vue").PropType<string>;
        default: string;
    };
    tag: {
        type: import("vue").PropType<keyof HTMLElementTagNameMap>;
        default: keyof HTMLElementTagNameMap;
    };
    unhighlightClass: StringConstructor;
    unhighlightTag: {
        type: import("vue").PropType<keyof HTMLElementTagNameMap>;
        default: keyof HTMLElementTagNameMap;
    };
}>>, {
    tag: keyof HTMLElementTagNameMap;
    autoEscape: boolean;
    caseSensitive: boolean;
    highlightTag: keyof HTMLElementTagNameMap;
    sourceString: string;
    unhighlightTag: keyof HTMLElementTagNameMap;
}, {}>>;
export default Highlight;
export { highlightProps } from './Highlight';
export type { HighlightProps } from './Highlight';
export type { HighlightThemeVars } from './types';
declare module 'vue' {
    interface GlobalComponents {
        vanHighlight: typeof Highlight;
    }
}
