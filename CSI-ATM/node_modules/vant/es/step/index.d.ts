export declare const Step: import("../utils").WithInstall<import("vue").DefineComponent<{}, (() => import("vue/jsx-runtime").JSX.Element) | undefined, {}, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, {}, string, import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{}>>, {}, {}>>;
export default Step;
export type { StepThemeVars } from './types';
declare module 'vue' {
    interface GlobalComponents {
        VanStep: typeof Step;
    }
}
