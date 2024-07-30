export declare const NavBar: import("../utils").WithInstall<import("vue").DefineComponent<{
    title: StringConstructor;
    fixed: BooleanConstructor;
    zIndex: (NumberConstructor | StringConstructor)[];
    border: {
        type: BooleanConstructor;
        default: true;
    };
    leftText: StringConstructor;
    rightText: StringConstructor;
    leftDisabled: BooleanConstructor;
    rightDisabled: BooleanConstructor;
    leftArrow: BooleanConstructor;
    placeholder: BooleanConstructor;
    safeAreaInsetTop: BooleanConstructor;
    clickable: {
        type: BooleanConstructor;
        default: true;
    };
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, ("clickLeft" | "clickRight")[], "clickLeft" | "clickRight", import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    title: StringConstructor;
    fixed: BooleanConstructor;
    zIndex: (NumberConstructor | StringConstructor)[];
    border: {
        type: BooleanConstructor;
        default: true;
    };
    leftText: StringConstructor;
    rightText: StringConstructor;
    leftDisabled: BooleanConstructor;
    rightDisabled: BooleanConstructor;
    leftArrow: BooleanConstructor;
    placeholder: BooleanConstructor;
    safeAreaInsetTop: BooleanConstructor;
    clickable: {
        type: BooleanConstructor;
        default: true;
    };
}>> & {
    onClickLeft?: ((...args: any[]) => any) | undefined;
    onClickRight?: ((...args: any[]) => any) | undefined;
}, {
    fixed: boolean;
    border: boolean;
    clickable: boolean;
    placeholder: boolean;
    safeAreaInsetTop: boolean;
    leftDisabled: boolean;
    rightDisabled: boolean;
    leftArrow: boolean;
}, {}>>;
export default NavBar;
export { navBarProps } from './NavBar';
export type { NavBarProps } from './NavBar';
export type { NavBarThemeVars } from './types';
declare module 'vue' {
    interface GlobalComponents {
        VanNavBar: typeof NavBar;
    }
}
