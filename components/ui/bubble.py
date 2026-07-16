from typing import Literal

import reflex as rx
from reflex.components.component import ComponentNamespace

from ..core.core import CoreComponent, cn

BubbleVariant = Literal[
    "default", "secondary", "muted", "tinted", "outline", "ghost", "destructive"
]
BubbleAlign = Literal["start", "end"]
BubbleSide = Literal["top", "bottom"]


class ClassNames:
    GROUP = "flex min-w-0 flex-col gap-2"

    VARIANTS: dict[str, str] = {
        "default": (
            "*:data-[slot=bubble-content]:bg-primary "
            "*:data-[slot=bubble-content]:text-primary-foreground"
        ),
        "secondary": (
            "*:data-[slot=bubble-content]:bg-secondary "
            "*:data-[slot=bubble-content]:text-secondary-foreground"
        ),
        "muted": "*:data-[slot=bubble-content]:bg-muted",
        "tinted": (
            "*:data-[slot=bubble-content]:bg-[oklch(from_var(--primary)_0.93_calc(c*0.4)_h)] "
            "*:data-[slot=bubble-content]:text-foreground "
            "dark:*:data-[slot=bubble-content]:bg-[oklch(from_var(--primary)_0.3_calc(c*0.4)_h)]"
        ),
        "outline": (
            "*:data-[slot=bubble-content]:border-border "
            "*:data-[slot=bubble-content]:bg-background"
        ),
        "ghost": (
            "border-none "
            "*:data-[slot=bubble-content]:rounded-none "
            "*:data-[slot=bubble-content]:bg-transparent "
            "*:data-[slot=bubble-content]:p-0"
        ),
        "destructive": (
            "*:data-[slot=bubble-content]:bg-destructive/10 "
            "*:data-[slot=bubble-content]:text-destructive "
            "dark:*:data-[slot=bubble-content]:bg-destructive/20"
        ),
    }

    ROOT = (
        "group/bubble relative flex w-fit max-w-[80%] min-w-0 flex-col gap-1 "
        "group-data-[align=end]/message:self-end "
        "data-[align=end]:self-end "
        "data-[variant=ghost]:max-w-full"
    )

    CONTENT = (
        "w-fit max-w-full min-w-0 overflow-hidden rounded-3xl border border-transparent "
        "px-3 py-2.5 text-sm leading-relaxed break-words "
        "group-data-[align=end]/bubble:self-end"
    )

    REACTIONS_BASE = (
        "absolute z-10 flex w-fit shrink-0 items-center justify-center gap-1 "
        "rounded-full bg-muted px-1.5 py-0.5 text-sm ring-3 ring-card has-[button]:p-0"
    )

    REACTIONS_SIDE: dict[str, str] = {
        "top": "top-0 -translate-y-3/4",
        "bottom": "bottom-0 translate-y-3/4",
    }

    REACTIONS_ALIGN: dict[str, str] = {
        "start": "left-3",
        "end": "right-3",
    }


class NativeBubbleGroup(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "bubble-group"
        cls.set_class_name(ClassNames.GROUP, props)
        return rx.el.div(*children, **props)


class NativeBubbleRoot(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        variant: BubbleVariant = props.pop("variant", "default")
        align: BubbleAlign = props.pop("align", "start")

        props["data-slot"] = "bubble"
        props["data-variant"] = variant
        props["data-align"] = align

        cls.set_class_name(
            cn(
                ClassNames.ROOT,
                ClassNames.VARIANTS.get(variant, ""),
            ),
            props,
        )
        return rx.el.div(*children, **props)


class NativeBubbleContent(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "bubble-content"
        cls.set_class_name(ClassNames.CONTENT, props)
        return rx.el.div(*children, **props)


class NativeBubbleReactions(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        side: BubbleSide = props.pop("side", "bottom")
        align: BubbleAlign = props.pop("align", "end")

        props["data-slot"] = "bubble-reactions"
        props["data-align"] = align
        props["data-side"] = side

        cls.set_class_name(
            cn(
                ClassNames.REACTIONS_BASE,
                ClassNames.REACTIONS_SIDE.get(side, ""),
                ClassNames.REACTIONS_ALIGN.get(align, ""),
            ),
            props,
        )
        return rx.el.div(*children, **props)


class Bubble(ComponentNamespace):
    group = staticmethod(NativeBubbleGroup.create)
    root = staticmethod(NativeBubbleRoot.create)
    content = staticmethod(NativeBubbleContent.create)
    reactions = staticmethod(NativeBubbleReactions.create)
    class_names = ClassNames


bubble = Bubble()
