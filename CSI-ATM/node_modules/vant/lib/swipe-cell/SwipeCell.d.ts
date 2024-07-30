import { type PropType, type ExtractPropTypes } from 'vue';
import { Interceptor } from '../utils';
export declare const swipeCellProps: {
    name: {
        type: (NumberConstructor | StringConstructor)[];
        default: string;
    };
    disabled: BooleanConstructor;
    leftWidth: (NumberConstructor | StringConstructor)[];
    rightWidth: (NumberConstructor | StringConstructor)[];
    beforeClose: PropType<Interceptor>;
    stopPropagation: BooleanConstructor;
};
export type SwipeCellProps = ExtractPropTypes<typeof swipeCellProps>;
declare const _default: import("vue").DefineComponent<{
    name: {
        type: (NumberConstructor | StringConstructor)[];
        default: string;
    };
    disabled: BooleanConstructor;
    leftWidth: (NumberConstructor | StringConstructor)[];
    rightWidth: (NumberConstructor | StringConstructor)[];
    beforeClose: PropType<Interceptor>;
    stopPropagation: BooleanConstructor;
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, ("open" | "click" | "close")[], "open" | "click" | "close", import("vue").PublicProps, Readonly<ExtractPropTypes<{
    name: {
        type: (NumberConstructor | StringConstructor)[];
        default: string;
    };
    disabled: BooleanConstructor;
    leftWidth: (NumberConstructor | StringConstructor)[];
    rightWidth: (NumberConstructor | StringConstructor)[];
    beforeClose: PropType<Interceptor>;
    stopPropagation: BooleanConstructor;
}>> & {
    onClick?: ((...args: any[]) => any) | undefined;
    onOpen?: ((...args: any[]) => any) | undefined;
    onClose?: ((...args: any[]) => any) | undefined;
}, {
    name: string | number;
    disabled: boolean;
    stopPropagation: boolean;
}, {}>;
export default _default;
