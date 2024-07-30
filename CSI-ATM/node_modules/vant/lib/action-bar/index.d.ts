export declare const ActionBar: import("../utils").WithInstall<import("vue").DefineComponent<{
    placeholder: BooleanConstructor;
    safeAreaInsetBottom: {
        type: BooleanConstructor;
        default: true;
    };
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, {}, string, import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    placeholder: BooleanConstructor;
    safeAreaInsetBottom: {
        type: BooleanConstructor;
        default: true;
    };
}>>, {
    placeholder: boolean;
    safeAreaInsetBottom: boolean;
}, {}>>;
export default ActionBar;
export { actionBarProps } from './ActionBar';
export type { ActionBarProps } from './ActionBar';
export type { ActionBarThemeVars } from './types';
declare module 'vue' {
    interface GlobalComponents {
        VanActionBar: typeof ActionBar;
    }
}
