export declare const CellGroup: import("../utils").WithInstall<import("vue").DefineComponent<{
    title: StringConstructor;
    inset: BooleanConstructor;
    border: {
        type: BooleanConstructor;
        default: true;
    };
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, {}, string, import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    title: StringConstructor;
    inset: BooleanConstructor;
    border: {
        type: BooleanConstructor;
        default: true;
    };
}>>, {
    inset: boolean;
    border: boolean;
}, {}>>;
export default CellGroup;
export { cellGroupProps } from './CellGroup';
export type { CellGroupProps } from './CellGroup';
export type { CellGroupThemeVars } from './types';
declare module 'vue' {
    interface GlobalComponents {
        VanCellGroup: typeof CellGroup;
    }
}
