from typing import Literal

import reflex as rx
from reflex.components.component import ComponentNamespace

from ..core.core import CoreComponent, cn
from ..ui.button import button

AttachmentOrientation = Literal["horizontal", "vertical"]
AttachmentSize = Literal["default", "sm", "xs"]
AttachmentState = Literal["idle", "uploading", "processing", "error", "done"]
AttachmentMediaVariant = Literal["icon", "image"]


class ClassNames:
    ROOT_BASE = (
        "group/attachment relative flex w-full max-w-full min-w-0 shrink-0 flex-wrap "
        "rounded-2xl border border-input bg-card text-card-foreground transition-colors "
        "focus-within:ring-1 focus-within:ring-ring/30 "
        "has-[>a,>button]:hover:bg-muted/50 "
        "data-[state=error]:border-destructive/30 "
        "data-[state=idle]:border-dashed"
    )

    SIZES = {
        "default": (
            "gap-2 text-sm "
            "has-data-[slot=attachment-content]:px-2.5 "
            "has-data-[slot=attachment-content]:py-2 "
            "has-data-[slot=attachment-media]:p-2"
        ),
        "sm": (
            "gap-2.5 text-xs "
            "has-data-[slot=attachment-content]:px-2 "
            "has-data-[slot=attachment-content]:py-1.5 "
            "has-data-[slot=attachment-media]:p-1.5"
        ),
        "xs": (
            "gap-1.5 rounded-xl text-xs "
            "has-data-[slot=attachment-content]:px-1.5 "
            "has-data-[slot=attachment-content]:py-1 "
            "has-data-[slot=attachment-media]:p-1"
        ),
    }

    ORIENTATIONS = {
        "horizontal": "min-w-40 items-center",
        "vertical": "w-24 flex-col has-data-[slot=attachment-content]:w-30",
    }

    MEDIA_BASE = (
        "relative flex aspect-square w-10 shrink-0 items-center justify-center "
        "overflow-hidden rounded-lg bg-muted text-foreground "
        "group-data-[orientation=vertical]/attachment:w-full "
        "group-data-[size=sm]/attachment:w-8 "
        "group-data-[size=xs]/attachment:w-7 "
        "group-data-[size=xs]/attachment:rounded-md "
        "group-data-[state=error]/attachment:bg-destructive/10 "
        "group-data-[state=error]/attachment:text-destructive "
        "[&_svg]:pointer-events-none "
        "[&_svg:not([class*='size-'])]:size-4 "
        "group-data-[orientation=vertical]/attachment:[&_svg:not([class*='size-'])]:size-6 "
        "group-data-[size=xs]/attachment:[&_svg:not([class*='size-'])]:size-3.5"
    )

    MEDIA_VARIANTS = {
        "icon": "",
        "image": (
            "opacity-60 "
            "group-data-[state=done]/attachment:opacity-100 "
            "group-data-[state=idle]/attachment:opacity-100 "
            "*:[img]:aspect-square *:[img]:w-full *:[img]:object-cover"
        ),
    }

    CONTENT = (
        "max-w-full min-w-0 flex-1 leading-tight "
        "group-data-[orientation=vertical]/attachment:px-1"
    )

    TITLE = (
        "block max-w-full min-w-0 truncate font-medium "
        "group-data-[state=processing]/attachment:shimmer "
        "group-data-[state=uploading]/attachment:shimmer"
    )

    DESCRIPTION = (
        "mt-0.5 block min-w-0 max-w-full truncate text-xs text-muted-foreground "
        "group-data-[state=error]/attachment:text-destructive/80"
    )

    ACTIONS = (
        "relative z-20 flex shrink-0 items-center "
        "group-data-[orientation=vertical]/attachment:absolute "
        "group-data-[orientation=vertical]/attachment:top-3 "
        "group-data-[orientation=vertical]/attachment:right-3 "
        "group-data-[orientation=vertical]/attachment:gap-1"
    )

    TRIGGER = "absolute inset-0 z-10 outline-none"

    GROUP = (
        "flex scroll-fade-x min-w-0 snap-x snap-mandatory scroll-px-1 scrollbar-none gap-3 "
        "overflow-x-auto overscroll-x-contain py-1 "
        "*:data-[slot=attachment]:flex-none "
        "*:data-[slot=attachment]:snap-start"
    )


class NativeAttachmentRoot(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        orientation: AttachmentOrientation = props.pop("orientation", "horizontal")
        size: AttachmentSize = props.pop("size", "default")
        state: AttachmentState = props.pop("state", "done")

        props["data-slot"] = "attachment"
        props["data-state"] = state
        props["data-size"] = size
        props["data-orientation"] = orientation

        cls.set_class_name(
            cn(
                ClassNames.ROOT_BASE,
                ClassNames.SIZES.get(size, ""),
                ClassNames.ORIENTATIONS.get(orientation, ""),
            ),
            props,
        )
        return rx.el.div(*children, **props)


class NativeAttachmentMedia(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        variant: AttachmentMediaVariant = props.pop("variant", "icon")

        props["data-slot"] = "attachment-media"
        props["data-variant"] = variant

        cls.set_class_name(
            cn(
                ClassNames.MEDIA_BASE,
                ClassNames.MEDIA_VARIANTS.get(variant, ""),
            ),
            props,
        )
        return rx.el.div(*children, **props)


class NativeAttachmentContent(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "attachment-content"
        cls.set_class_name(ClassNames.CONTENT, props)
        return rx.el.div(*children, **props)


class NativeAttachmentTitle(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "attachment-title"
        cls.set_class_name(ClassNames.TITLE, props)
        return rx.el.span(*children, **props)


class NativeAttachmentDescription(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "attachment-description"
        cls.set_class_name(ClassNames.DESCRIPTION, props)
        return rx.el.span(*children, **props)


class NativeAttachmentActions(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "attachment-actions"
        cls.set_class_name(ClassNames.ACTIONS, props)
        return rx.el.div(*children, **props)


class NativeAttachmentAction(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props.setdefault("variant", "ghost")
        props.setdefault("size", "icon-xs")
        props["data-slot"] = "attachment-action"
        return button(*children, **props)


class NativeAttachmentTrigger(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        link: bool = props.pop("link", False)
        component_fn = rx.el.a if link else rx.el.button

        props["data-slot"] = "attachment-trigger"
        cls.set_class_name(ClassNames.TRIGGER, props)

        if not link:
            props.setdefault("type", "button")

        return component_fn(*children, **props)


class NativeAttachmentGroup(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "attachment-group"
        cls.set_class_name(ClassNames.GROUP, props)
        return rx.el.div(*children, **props)


class Attachment(ComponentNamespace):
    root = staticmethod(NativeAttachmentRoot.create)
    media = staticmethod(NativeAttachmentMedia.create)
    content = staticmethod(NativeAttachmentContent.create)
    title = staticmethod(NativeAttachmentTitle.create)
    description = staticmethod(NativeAttachmentDescription.create)
    actions = staticmethod(NativeAttachmentActions.create)
    action = staticmethod(NativeAttachmentAction.create)
    trigger = staticmethod(NativeAttachmentTrigger.create)
    group = staticmethod(NativeAttachmentGroup.create)
    class_names = ClassNames


attachment = Attachment()
