import { type PropType, type ComputedRef, type InjectionKey, type ExtractPropTypes } from 'vue';
export type RowSpaces = {
    left?: number;
    right: number;
}[];
export type VerticalSpaces = {
    bottom?: number;
}[];
export type RowProvide = {
    spaces: ComputedRef<RowSpaces>;
    verticalSpaces: ComputedRef<VerticalSpaces>;
};
export declare const ROW_KEY: InjectionKey<RowProvide>;
export type RowAlign = 'top' | 'center' | 'bottom';
export type RowJustify = 'start' | 'end' | 'center' | 'space-around' | 'space-between';
export declare const rowProps: {
    tag: {
        type: PropType<keyof HTMLElementTagNameMap>;
        default: keyof HTMLElementTagNameMap;
    };
    wrap: {
        type: BooleanConstructor;
        default: true;
    };
    align: PropType<RowAlign>;
    gutter: {
        type: PropType<string | number | (string | number)[]>;
        default: number;
    };
    justify: PropType<RowJustify>;
};
export type RowProps = ExtractPropTypes<typeof rowProps>;
declare const _default: import("vue").DefineComponent<{
    tag: {
        type: PropType<keyof HTMLElementTagNameMap>;
        default: keyof HTMLElementTagNameMap;
    };
    wrap: {
        type: BooleanConstructor;
        default: true;
    };
    align: PropType<RowAlign>;
    gutter: {
        type: PropType<string | number | (string | number)[]>;
        default: number;
    };
    justify: PropType<RowJustify>;
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, {}, string, import("vue").PublicProps, Readonly<ExtractPropTypes<{
    tag: {
        type: PropType<keyof HTMLElementTagNameMap>;
        default: keyof HTMLElementTagNameMap;
    };
    wrap: {
        type: BooleanConstructor;
        default: true;
    };
    align: PropType<RowAlign>;
    gutter: {
        type: PropType<string | number | (string | number)[]>;
        default: number;
    };
    justify: PropType<RowJustify>;
}>>, {
    tag: keyof HTMLElementTagNameMap;
    wrap: boolean;
    gutter: string | number | (string | number)[];
}, {}>;
export default _default;
