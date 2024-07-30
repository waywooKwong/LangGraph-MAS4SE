export declare const Divider: import("../utils").WithInstall<import("vue").DefineComponent<{
    dashed: BooleanConstructor;
    hairline: {
        type: BooleanConstructor;
        default: true;
    };
    vertical: BooleanConstructor;
    contentPosition: {
        type: import("vue").PropType<import("./Divider").DividerContentPosition>;
        default: import("./Divider").DividerContentPosition;
    };
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, {}, string, import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    dashed: BooleanConstructor;
    hairline: {
        type: BooleanConstructor;
        default: true;
    };
    vertical: BooleanConstructor;
    contentPosition: {
        type: import("vue").PropType<import("./Divider").DividerContentPosition>;
        default: import("./Divider").DividerContentPosition;
    };
}>>, {
    dashed: boolean;
    vertical: boolean;
    hairline: boolean;
    contentPosition: import("./Divider").DividerContentPosition;
}, {}>>;
export default Divider;
export { dividerProps } from './Divider';
export type { DividerProps, DividerContentPosition } from './Divider';
export type { DividerThemeVars } from './types';
declare module 'vue' {
    interface GlobalComponents {
        VanDivider: typeof Divider;
    }
}
