from typing import Literal

import reflex as rx
from reflex.components.component import ComponentNamespace

from ..core.core import CoreComponent, cn

LiteralVariant = Literal["default", "inverse", "ghost"]
LiteralSpacing = Literal["xs", "sm", "default", "lg"]


class ClassNames:
    ROOT = "relative flex flex-col bg-muted/50 gap-0.75 p-0.75 rounded-xl"
    ROOT_VARIANT_DEFAULT = "border border-border bg-clip-padding"
    ROOT_VARIANT_INVERSE = "border border-border bg-background bg-clip-padding"
    ROOT_VARIANT_GHOST = ""
    PANEL = "relative grow overflow-hidden rounded-xl border border-border bg-card bg-clip-padding shadow-xs p-(--frame-panel-p)"
    HEADER = "flex flex-col px-(--frame-panel-header-px) py-(--frame-panel-header-py)"
    TITLE = "text-sm font-semibold"
    DESCRIPTION = "text-muted-foreground text-sm"
    FOOTER = (
        "flex flex-col gap-1 px-(--frame-panel-footer-px) py-(--frame-panel-footer-py)"
    )


VARIANT_CLASSES: dict[str, str] = {
    "default": ClassNames.ROOT_VARIANT_DEFAULT,
    "inverse": ClassNames.ROOT_VARIANT_INVERSE,
    "ghost": ClassNames.ROOT_VARIANT_GHOST,
}

SPACING_CLASSES: dict[str, str] = {
    "xs": "[--frame-panel-p:--spacing(2)] [--frame-panel-header-px:--spacing(2)] [--frame-panel-header-py:--spacing(1)] [--frame-panel-footer-px:--spacing(2)] [--frame-panel-footer-py:--spacing(1)]",
    "sm": "[--frame-panel-p:--spacing(3)] [--frame-panel-header-px:--spacing(3)] [--frame-panel-header-py:--spacing(2)] [--frame-panel-footer-px:--spacing(3)] [--frame-panel-footer-py:--spacing(2)]",
    "default": "[--frame-panel-p:--spacing(4)] [--frame-panel-header-px:--spacing(4)] [--frame-panel-header-py:--spacing(3)] [--frame-panel-footer-px:--spacing(4)] [--frame-panel-footer-py:--spacing(3)]",
    "lg": "[--frame-panel-p:--spacing(5)] [--frame-panel-header-px:--spacing(5)] [--frame-panel-header-py:--spacing(4)] [--frame-panel-footer-px:--spacing(5)] [--frame-panel-footer-py:--spacing(4)]",
}


class FrameRoot(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        variant: LiteralVariant = props.pop("variant", "default")
        spacing: LiteralSpacing = props.pop("spacing", "default")
        stacked: bool = props.pop("stacked", False)
        dense: bool = props.pop("dense", False)
        class_name: str = props.pop("class_name", "")

        stacked_class = (
            "gap-0 *:has-[+[data-slot=frame-panel]]:rounded-b-none *:[[data-slot=frame-panel]+[data-slot=frame-panel]]:rounded-t-none *:[[data-slot=frame-panel]+[data-slot=frame-panel]]:border-t-0"
            if stacked
            else ""
        )

        dense_class = (
            "p-0 gap-0 [&_[data-slot=frame-panel]]:-mx-px [&_[data-slot=frame-panel]]:before:hidden [&_[data-slot=frame-panel]:last-child]:-mb-px"
            if dense
            else ""
        )

        props["data-slot"] = "frame"
        props["data-spacing"] = spacing

        return rx.el.div(
            *children,
            class_name=cn(
                ClassNames.ROOT,
                VARIANT_CLASSES.get(variant, ""),
                SPACING_CLASSES.get(spacing, ""),
                stacked_class,
                dense_class,
                class_name,
            ),
            **props,
        )


class FramePanel(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        class_name: str = props.pop("class_name", "")
        props["data-slot"] = "frame-panel"
        return rx.el.div(
            *children,
            class_name=cn(ClassNames.PANEL, class_name),
            **props,
        )


class FrameHeader(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        class_name: str = props.pop("class_name", "")
        props["data-slot"] = "frame-panel-header"
        return rx.el.header(
            *children,
            class_name=cn(ClassNames.HEADER, class_name),
            **props,
        )


class FrameTitle(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        class_name: str = props.pop("class_name", "")
        props["data-slot"] = "frame-panel-title"
        return rx.el.div(
            *children,
            class_name=cn(ClassNames.TITLE, class_name),
            **props,
        )


class FrameDescription(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        class_name: str = props.pop("class_name", "")
        props["data-slot"] = "frame-panel-description"
        return rx.el.div(
            *children,
            class_name=cn(ClassNames.DESCRIPTION, class_name),
            **props,
        )


class FrameFooter(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        class_name: str = props.pop("class_name", "")
        props["data-slot"] = "frame-panel-footer"
        return rx.el.footer(
            *children,
            class_name=cn(ClassNames.FOOTER, class_name),
            **props,
        )


class Frame(ComponentNamespace):
    root = staticmethod(FrameRoot.create)
    panel = staticmethod(FramePanel.create)
    header = staticmethod(FrameHeader.create)
    title = staticmethod(FrameTitle.create)
    description = staticmethod(FrameDescription.create)
    footer = staticmethod(FrameFooter.create)
    __call__ = staticmethod(FrameRoot.create)
    class_names = ClassNames


frame = Frame()
