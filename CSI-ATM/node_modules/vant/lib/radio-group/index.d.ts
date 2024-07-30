export declare const RadioGroup: import("../utils").WithInstall<import("vue").DefineComponent<{
    shape: import("vue").PropType<import("..").RadioShape>;
    disabled: BooleanConstructor;
    iconSize: (NumberConstructor | StringConstructor)[];
    direction: import("vue").PropType<import("../checkbox/Checker").CheckerDirection>;
    modelValue: import("vue").PropType<unknown>;
    checkedColor: StringConstructor;
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, ("update:modelValue" | "change")[], "update:modelValue" | "change", import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    shape: import("vue").PropType<import("..").RadioShape>;
    disabled: BooleanConstructor;
    iconSize: (NumberConstructor | StringConstructor)[];
    direction: import("vue").PropType<import("../checkbox/Checker").CheckerDirection>;
    modelValue: import("vue").PropType<unknown>;
    checkedColor: StringConstructor;
}>> & {
    onChange?: ((...args: any[]) => any) | undefined;
    "onUpdate:modelValue"?: ((...args: any[]) => any) | undefined;
}, {
    disabled: boolean;
}, {}>>;
export default RadioGroup;
export { radioGroupProps } from './RadioGroup';
export type { RadioGroupProps, RadioGroupDirection } from './RadioGroup';
declare module 'vue' {
    interface GlobalComponents {
        VanRadioGroup: typeof RadioGroup;
    }
}
