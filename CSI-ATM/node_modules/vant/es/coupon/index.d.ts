export declare const Coupon: import("../utils").WithInstall<import("vue").DefineComponent<{
    chosen: BooleanConstructor;
    coupon: {
        type: import("vue").PropType<import("./Coupon").CouponInfo>;
        required: true;
    };
    disabled: BooleanConstructor;
    currency: {
        type: import("vue").PropType<string>;
        default: string;
    };
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, {}, string, import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    chosen: BooleanConstructor;
    coupon: {
        type: import("vue").PropType<import("./Coupon").CouponInfo>;
        required: true;
    };
    disabled: BooleanConstructor;
    currency: {
        type: import("vue").PropType<string>;
        default: string;
    };
}>>, {
    disabled: boolean;
    currency: string;
    chosen: boolean;
}, {}>>;
export default Coupon;
export type { CouponInfo } from './Coupon';
export type { CouponThemeVars } from './types';
declare module 'vue' {
    interface GlobalComponents {
        VanCoupon: typeof Coupon;
    }
}
