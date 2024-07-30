export declare const IndexAnchor: import("../utils").WithInstall<import("vue").DefineComponent<{
    index: (NumberConstructor | StringConstructor)[];
}, (() => import("vue/jsx-runtime").JSX.Element) | undefined, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, {}, string, import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    index: (NumberConstructor | StringConstructor)[];
}>>, {}, {}>>;
export default IndexAnchor;
export { indexAnchorProps } from './IndexAnchor';
export type { IndexAnchorProps } from './IndexAnchor';
export type { IndexAnchorThemeVars } from './types';
declare module 'vue' {
    interface GlobalComponents {
        VanIndexAnchor: typeof IndexAnchor;
    }
}
