export declare const Image: import("../utils").WithInstall<import("vue").DefineComponent<{
    src: StringConstructor;
    alt: StringConstructor;
    fit: import("vue").PropType<import("csstype").Property.ObjectFit | undefined>;
    position: import("vue").PropType<import("csstype").Property.ObjectPosition<string | number> | undefined>;
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
        type: import("vue").PropType<string>;
        default: string;
    };
    iconPrefix: StringConstructor;
    showLoading: {
        type: BooleanConstructor;
        default: true;
    };
    loadingIcon: {
        type: import("vue").PropType<string>;
        default: string;
    };
    crossorigin: import("vue").PropType<"" | "anonymous" | "use-credentials" | undefined>;
    referrerpolicy: import("vue").PropType<("" | "no-referrer" | "no-referrer-when-downgrade" | "origin" | "origin-when-cross-origin" | "same-origin" | "strict-origin" | "strict-origin-when-cross-origin" | "unsafe-url") | undefined>;
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, ("error" | "load")[], "error" | "load", import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    src: StringConstructor;
    alt: StringConstructor;
    fit: import("vue").PropType<import("csstype").Property.ObjectFit | undefined>;
    position: import("vue").PropType<import("csstype").Property.ObjectPosition<string | number> | undefined>;
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
        type: import("vue").PropType<string>;
        default: string;
    };
    iconPrefix: StringConstructor;
    showLoading: {
        type: BooleanConstructor;
        default: true;
    };
    loadingIcon: {
        type: import("vue").PropType<string>;
        default: string;
    };
    crossorigin: import("vue").PropType<"" | "anonymous" | "use-credentials" | undefined>;
    referrerpolicy: import("vue").PropType<("" | "no-referrer" | "no-referrer-when-downgrade" | "origin" | "origin-when-cross-origin" | "same-origin" | "strict-origin" | "strict-origin-when-cross-origin" | "unsafe-url") | undefined>;
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
}, {}>>;
export default Image;
export { imageProps } from './Image';
export type { ImageProps } from './Image';
export type { ImageFit, ImagePosition, ImageThemeVars } from './types';
declare module 'vue' {
    interface GlobalComponents {
        VanImage: typeof Image;
    }
}
