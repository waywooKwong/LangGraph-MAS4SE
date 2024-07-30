import { type ExtractPropTypes } from 'vue';
declare const imagePreviewItemProps: {
    src: StringConstructor;
    show: BooleanConstructor;
    active: NumberConstructor;
    minZoom: {
        type: (NumberConstructor | StringConstructor)[];
        required: true;
    };
    maxZoom: {
        type: (NumberConstructor | StringConstructor)[];
        required: true;
    };
    rootWidth: {
        type: NumberConstructor;
        required: true;
    };
    rootHeight: {
        type: NumberConstructor;
        required: true;
    };
    disableZoom: BooleanConstructor;
    doubleScale: BooleanConstructor;
    closeOnClickImage: BooleanConstructor;
    closeOnClickOverlay: BooleanConstructor;
    vertical: BooleanConstructor;
};
export type ImagePreviewItemProps = ExtractPropTypes<typeof imagePreviewItemProps>;
declare const _default: import("vue").DefineComponent<{
    src: StringConstructor;
    show: BooleanConstructor;
    active: NumberConstructor;
    minZoom: {
        type: (NumberConstructor | StringConstructor)[];
        required: true;
    };
    maxZoom: {
        type: (NumberConstructor | StringConstructor)[];
        required: true;
    };
    rootWidth: {
        type: NumberConstructor;
        required: true;
    };
    rootHeight: {
        type: NumberConstructor;
        required: true;
    };
    disableZoom: BooleanConstructor;
    doubleScale: BooleanConstructor;
    closeOnClickImage: BooleanConstructor;
    closeOnClickOverlay: BooleanConstructor;
    vertical: BooleanConstructor;
}, () => import("vue/jsx-runtime").JSX.Element, unknown, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, ("close" | "scale" | "longPress")[], "close" | "scale" | "longPress", import("vue").PublicProps, Readonly<ExtractPropTypes<{
    src: StringConstructor;
    show: BooleanConstructor;
    active: NumberConstructor;
    minZoom: {
        type: (NumberConstructor | StringConstructor)[];
        required: true;
    };
    maxZoom: {
        type: (NumberConstructor | StringConstructor)[];
        required: true;
    };
    rootWidth: {
        type: NumberConstructor;
        required: true;
    };
    rootHeight: {
        type: NumberConstructor;
        required: true;
    };
    disableZoom: BooleanConstructor;
    doubleScale: BooleanConstructor;
    closeOnClickImage: BooleanConstructor;
    closeOnClickOverlay: BooleanConstructor;
    vertical: BooleanConstructor;
}>> & {
    onClose?: ((...args: any[]) => any) | undefined;
    onScale?: ((...args: any[]) => any) | undefined;
    onLongPress?: ((...args: any[]) => any) | undefined;
}, {
    show: boolean;
    vertical: boolean;
    closeOnClickOverlay: boolean;
    disableZoom: boolean;
    doubleScale: boolean;
    closeOnClickImage: boolean;
}, {}>;
export default _default;
