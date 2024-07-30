import { type PropType } from 'vue';
import { type Numeric } from '../utils';
import type { RadioShape } from '../radio';
export type CheckerShape = 'square' | 'round';
export type CheckerDirection = 'horizontal' | 'vertical';
export type CheckerLabelPosition = 'left' | 'right';
export type CheckerParent = {
    props: {
        max?: Numeric;
        shape?: CheckerShape | RadioShape;
        disabled?: boolean;
        iconSize?: Numeric;
        direction?: CheckerDirection;
        modelValue?: unknown | unknown[];
        checkedColor?: string;
    };
};
export declare const checkerProps: {
    name: PropType<unknown>;
    disabled: BooleanConstructor;
    iconSize: (NumberConstructor | StringConstructor)[];
    modelValue: PropType<unknown>;
    checkedColor: StringConstructor;
    labelPosition: PropType<CheckerLabelPosition>;
    labelDisabled: BooleanConstructor;
};
declare const _default: import("vue").DefineComponent<{
    name: PropType<unknown>;
    disabled: BooleanConstructor;
    iconSize: (NumberConstructor | StringConstructor)[];
    modelValue: PropType<unknown>;
    checkedColor: StringConstructor;
    labelPosition: PropType<CheckerLabelPosition>;
    labelDisabled: BooleanConstructor;
} & {
    bem: {
        type: FunctionConstructor;
        required: true;
    };
    role: StringConstructor;
    shape: PropType<"dot" | "round" | "square">;
    parent: PropType<CheckerParent | null>;
    checked: BooleanConstructor;
    bindGroup: {
        type: BooleanConstructor;
        default: true;
    };
    indeterminate: {
        type: PropType<boolean | null>;
        default: null;
    };
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, ("click" | "toggle")[], "click" | "toggle", import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    name: PropType<unknown>;
    disabled: BooleanConstructor;
    iconSize: (NumberConstructor | StringConstructor)[];
    modelValue: PropType<unknown>;
    checkedColor: StringConstructor;
    labelPosition: PropType<CheckerLabelPosition>;
    labelDisabled: BooleanConstructor;
} & {
    bem: {
        type: FunctionConstructor;
        required: true;
    };
    role: StringConstructor;
    shape: PropType<"dot" | "round" | "square">;
    parent: PropType<CheckerParent | null>;
    checked: BooleanConstructor;
    bindGroup: {
        type: BooleanConstructor;
        default: true;
    };
    indeterminate: {
        type: PropType<boolean | null>;
        default: null;
    };
}>> & {
    onClick?: ((...args: any[]) => any) | undefined;
    onToggle?: ((...args: any[]) => any) | undefined;
}, {
    checked: boolean;
    disabled: boolean;
    labelDisabled: boolean;
    bindGroup: boolean;
    indeterminate: boolean | null;
}, {}>;
export default _default;
