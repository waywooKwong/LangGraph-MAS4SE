import { type InjectionKey, type ExtractPropTypes } from 'vue';
export type PickerGroupProvide = Record<string, string>;
export declare const PICKER_GROUP_KEY: InjectionKey<PickerGroupProvide>;
export declare const pickerGroupProps: {
    tabs: {
        type: import("vue").PropType<string[]>;
        default: () => never[];
    };
    activeTab: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
    nextStepText: StringConstructor;
    showToolbar: {
        type: BooleanConstructor;
        default: true;
    };
} & {
    title: StringConstructor;
    cancelButtonText: StringConstructor;
    confirmButtonText: StringConstructor;
};
export type PickerGroupProps = ExtractPropTypes<typeof pickerGroupProps>;
declare const _default: import("vue").DefineComponent<{
    tabs: {
        type: import("vue").PropType<string[]>;
        default: () => never[];
    };
    activeTab: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
    nextStepText: StringConstructor;
    showToolbar: {
        type: BooleanConstructor;
        default: true;
    };
} & {
    title: StringConstructor;
    cancelButtonText: StringConstructor;
    confirmButtonText: StringConstructor;
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, ("cancel" | "confirm" | "update:activeTab")[], "cancel" | "confirm" | "update:activeTab", import("vue").PublicProps, Readonly<ExtractPropTypes<{
    tabs: {
        type: import("vue").PropType<string[]>;
        default: () => never[];
    };
    activeTab: {
        type: (NumberConstructor | StringConstructor)[];
        default: number;
    };
    nextStepText: StringConstructor;
    showToolbar: {
        type: BooleanConstructor;
        default: true;
    };
} & {
    title: StringConstructor;
    cancelButtonText: StringConstructor;
    confirmButtonText: StringConstructor;
}>> & {
    onCancel?: ((...args: any[]) => any) | undefined;
    onConfirm?: ((...args: any[]) => any) | undefined;
    "onUpdate:activeTab"?: ((...args: any[]) => any) | undefined;
}, {
    showToolbar: boolean;
    tabs: string[];
    activeTab: string | number;
}, {}>;
export default _default;
