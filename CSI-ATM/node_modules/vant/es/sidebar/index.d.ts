export declare const Sidebar: import("../utils").WithInstall<import("vue").DefineComponent<{
    modelValue: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, ("update:modelValue" | "change")[], "update:modelValue" | "change", import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    modelValue: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
}>> & {
    onChange?: ((...args: any[]) => any) | undefined;
    "onUpdate:modelValue"?: ((...args: any[]) => any) | undefined;
}, {
    modelValue: string | number;
}, {}>>;
export default Sidebar;
export { sidebarProps } from './Sidebar';
export type { SidebarProps } from './Sidebar';
export type { SidebarThemeVars } from './types';
declare module 'vue' {
    interface GlobalComponents {
        VanSidebar: typeof Sidebar;
    }
}
