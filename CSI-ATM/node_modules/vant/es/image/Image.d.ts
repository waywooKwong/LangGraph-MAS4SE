import { type PropType, type ExtractPropTypes } from 'vue';
export declare const imageProps: {
    src: StringConstructor;
    alt: StringConstructor;
    fit: PropType<import("csstype").Property.ObjectFit | undefined>;
    position: PropType<import("csstype").Property.ObjectPosition<string | number> | undefined>;
    round: BooleanConstructor;
    block: BooleanConstructor;
    width: (NumberConstructor | StringConstructor)[];
    height: (NumberConstructor | StringConstructor)[];
    radius: (NumberConstructor | StringConstructor)[];
    lazyLoad: BooleanConstructor;
    iconSize: (NumberConstructor | StringConstructor)[];
    showError: {
        type: BooleanConstructor;
        default: true;
    };
    errorIcon: {
        type: PropType<string>;
        default: string;
    };
    iconPrefix: StringConstructor;
    showLoading: {
        type: BooleanConstructor;
        default: true;
    };
    loadingIcon: {
        type: PropType<string>;
        default: string;
    };
    crossorigin: PropType<"" | "anonymous" | "use-credentials" | undefined>;
    referrerpolicy: PropType<("" | "no-referrer" | "no-referrer-when-downgrade" | "origin" | "origin-when-cross-origin" | "same-origin" | "strict-origin" | "strict-origin-when-cross-origin" | "unsafe-url") | undefined>;
};
export type ImageProps = ExtractPropTypes<typeof imageProps>;
declare const _default: import("vue").DefineComponent<{
    src: StringConstructor;
    alt: StringConstructor;
    fit: PropType<import("csstype").Property.ObjectFit | undefined>;
    position: PropType<import("csstype").Property.ObjectPosition<string | number> | undefined>;
    round: BooleanConstructor;
    block: BooleanConstructor;
    width: (NumberConstructor | StringConstructor)[];
    height: (NumberConstructor | StringConstructor)[];
    radius: (NumberConstructor | StringConstructor)[];
    lazyLoad: BooleanConstructor;
    iconSize: (NumberConstructor | StringConstructor)[];
    showError: {
        type: BooleanConstructor;
        default: true;
    };
    errorIcon: {
        type: PropType<string>;
        default: string;
    };
    iconPrefix: StringConstructor;
    showLoading: {
        type: BooleanConstructor;
        default: true;
    };
    loadingIcon: {
        type: PropType<string>;
        default: string;
    };
    crossorigin: PropType<"" | "anonymous" | "use-credentials" | undefined>;
    referrerpolicy: PropType<("" | "no-referrer" | "no-referrer-when-downgrade" | "origin" | "origin-when-cross-origin" | "same-origin" | "strict-origin" | "strict-origin-when-cross-origin" | "unsafe-url") | undefined>;
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, ("error" | "load")[], "error" | "load", import("vue").PublicProps, Readonly<ExtractPropTypes<{
    src: StringConstructor;
    alt: StringConstructor;
    fit: PropType<import("csstype").Property.ObjectFit | undefined>;
    position: PropType<import("csstype").Property.ObjectPosition<string | number> | undefined>;
    round: BooleanConstructor;
    block: BooleanConstructor;
    width: (NumberConstructor | StringConstructor)[];
    height: (NumberConstructor | StringConstructor)[];
    radius: (NumberConstructor | StringConstructor)[];
    lazyLoad: BooleanConstructor;
    iconSize: (NumberConstructor | StringConstructor)[];
    showError: {
        type: BooleanConstructor;
        default: true;
    };
    errorIcon: {
        type: PropType<string>;
        default: string;
    };
    iconPrefix: StringConstructor;
    showLoading: {
        type: BooleanConstructor;
        default: true;
    };
    loadingIcon: {
        type: PropType<string>;
        default: string;
    };
    crossorigin: PropType<"" | "anonymous" | "use-credentials" | undefined>;
    referrerpolicy: PropType<("" | "no-referrer" | "no-referrer-when-downgrade" | "origin" | "origin-when-cross-origin" | "same-origin" | "strict-origin" | "strict-origin-when-cross-origin" | "unsafe-url") | undefined>;
}>> & {
    onLoad?: ((...args: any[]) => any) | undefined;
    onError?: ((...args: any[]) => any) | undefined;
}, {
    round: boolean;
    block: boolean;
    showError: boolean;
    lazyLoad: boolean;
    errorIcon: string;
    showLoading: boolean;
    loadingIcon: string;
}, {}>;
export default _default;
