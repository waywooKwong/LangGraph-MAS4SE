import { type PropType } from 'vue';
export type KeyType = '' | 'delete' | 'extra' | 'close';
declare const _default: import("vue").DefineComponent<{
    type: PropType<KeyType>;
    text: (NumberConstructor | StringConstructor)[];
    color: StringConstructor;
    wider: BooleanConstructor;
    large: BooleanConstructor;
    loading: BooleanConstructor;
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, "press"[], "press", import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    type: PropType<KeyType>;
    text: (NumberConstructor | StringConstructor)[];
    color: StringConstructor;
    wider: BooleanConstructor;
    large: BooleanConstructor;
    loading: BooleanConstructor;
}>> & {
    onPress?: ((...args: any[]) => any) | undefined;
}, {
    large: boolean;
    loading: boolean;
    wider: boolean;
}, {}>;
export default _default;
