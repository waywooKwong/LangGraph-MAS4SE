import { type InjectionKey, type ExtractPropTypes } from 'vue';
export type SidebarProvide = {
    getActive: () => number;
    setActive: (value: number) => void;
};
export declare const SIDEBAR_KEY: InjectionKey<SidebarProvide>;
export declare const sidebarProps: {
    modelValue: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
};
export type SidebarProps = ExtractPropTypes<typeof sidebarProps>;
declare const _default: import("vue").DefineComponent<{
    modelValue: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, ("update:modelValue" | "change")[], "update:modelValue" | "change", import("vue").PublicProps, Readonly<ExtractPropTypes<{
    modelValue: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
}>> & {
    onChange?: ((...args: any[]) => any) | undefined;
    "onUpdate:modelValue"?: ((...args: any[]) => any) | undefined;
}, {
    modelValue: string | number;
}, {}>;
export default _default;
