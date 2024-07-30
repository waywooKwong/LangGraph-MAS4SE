import { type ExtractPropTypes } from 'vue';
export declare const signatureProps: {
    tips: StringConstructor;
    type: {
        type: import("vue").PropType<string>;
        default: string;
    };
    penColor: {
        type: import("vue").PropType<string>;
        default: string;
    };
    lineWidth: {
        type: NumberConstructor;
        default: number;
    };
    clearButtonText: StringConstructor;
    backgroundColor: {
        type: import("vue").PropType<string>;
        default: string;
    };
    confirmButtonText: StringConstructor;
};
export type SignatureProps = ExtractPropTypes<typeof signatureProps>;
declare const _default: import("vue").DefineComponent<{
    tips: StringConstructor;
    type: {
        type: import("vue").PropType<string>;
        default: string;
    };
    penColor: {
        type: import("vue").PropType<string>;
        default: string;
    };
    lineWidth: {
        type: NumberConstructor;
        default: number;
    };
    clearButtonText: StringConstructor;
    backgroundColor: {
        type: import("vue").PropType<string>;
        default: string;
    };
    confirmButtonText: StringConstructor;
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, ("submit" | "clear" | "start" | "end" | "signing")[], "submit" | "clear" | "start" | "end" | "signing", import("vue").PublicProps, Readonly<ExtractPropTypes<{
    tips: StringConstructor;
    type: {
        type: import("vue").PropType<string>;
        default: string;
    };
    penColor: {
        type: import("vue").PropType<string>;
        default: string;
    };
    lineWidth: {
        type: NumberConstructor;
        default: number;
    };
    clearButtonText: StringConstructor;
    backgroundColor: {
        type: import("vue").PropType<string>;
        default: string;
    };
    confirmButtonText: StringConstructor;
}>> & {
    onSubmit?: ((...args: any[]) => any) | undefined;
    onClear?: ((...args: any[]) => any) | undefined;
    onStart?: ((...args: any[]) => any) | undefined;
    onEnd?: ((...args: any[]) => any) | undefined;
    onSigning?: ((...args: any[]) => any) | undefined;
}, {
    type: string;
    backgroundColor: string;
    lineWidth: number;
    penColor: string;
}, {}>;
export default _default;
