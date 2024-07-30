import { type ExtractPropTypes } from 'vue';
export declare const cellGroupProps: {
    title: StringConstructor;
    inset: BooleanConstructor;
    border: {
        type: BooleanConstructor;
        default: true;
    };
};
export type CellGroupProps = ExtractPropTypes<typeof cellGroupProps>;
declare const _default: import("vue").DefineComponent<{
    title: StringConstructor;
    inset: BooleanConstructor;
    border: {
        type: BooleanConstructor;
        default: true;
    };
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, {}, string, import("vue").PublicProps, Readonly<ExtractPropTypes<{
    title: StringConstructor;
    inset: BooleanConstructor;
    border: {
        type: BooleanConstructor;
        default: true;
    };
}>>, {
    inset: boolean;
    border: boolean;
}, {}>;
export default _default;
