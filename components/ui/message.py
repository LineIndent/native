from typing import Literal

import reflex as rx
from reflex.components.component import ComponentNamespace

from ..core.core import CoreComponent

MessageAlign = Literal["start", "end"]


class ClassNames:
    GROUP = "flex min-w-0 flex-col gap-2"

    ROOT = (
        "group/message relative flex w-full min-w-0 gap-2 text-sm "
        "data-[align=end]:flex-row-reverse"
    )

    AVATAR = (
        "flex w-fit min-w-8 shrink-0 items-center justify-center "
        "self-end overflow-hidden rounded-full bg-muted "
        "group-has-data-[slot=message-footer]/message:-translate-y-8"
    )

    CONTENT = (
        "flex w-full min-w-0 flex-col gap-2.5 break-words "
        "group-data-[align=end]/message:*:data-slot:self-end"
    )

    HEADER = (
        "flex max-w-full min-w-0 items-center px-3 text-xs font-medium "
        "text-muted-foreground "
        "group-has-data-[variant=ghost]/message:px-0"
    )

    FOOTER = (
        "flex max-w-full min-w-0 items-center px-3 text-xs font-medium "
        "text-muted-foreground "
        "group-has-data-[variant=ghost]/message:px-0 "
        "group-data-[align=end]/message:justify-end"
    )


class NativeMessageGroup(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "message-group"
        cls.set_class_name(ClassNames.GROUP, props)
        return rx.el.div(*children, **props)


class NativeMessageRoot(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        align = props.pop("align", "start")
        props["data-slot"] = "message"
        props["data-align"] = align
        cls.set_class_name(ClassNames.ROOT, props)
        return rx.el.div(*children, **props)


class NativeMessageAvatar(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "message-avatar"
        cls.set_class_name(ClassNames.AVATAR, props)
        return rx.el.div(*children, **props)


class NativeMessageContent(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "message-content"
        cls.set_class_name(ClassNames.CONTENT, props)
        return rx.el.div(*children, **props)


class NativeMessageHeader(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "message-header"
        cls.set_class_name(ClassNames.HEADER, props)
        return rx.el.div(*children, **props)


class NativeMessageFooter(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "message-footer"
        cls.set_class_name(ClassNames.FOOTER, props)
        return rx.el.div(*children, **props)


class Message(ComponentNamespace):
    group = staticmethod(NativeMessageGroup.create)
    root = staticmethod(NativeMessageRoot.create)
    avatar = staticmethod(NativeMessageAvatar.create)
    content = staticmethod(NativeMessageContent.create)
    header = staticmethod(NativeMessageHeader.create)
    footer = staticmethod(NativeMessageFooter.create)
    class_names = ClassNames


message = Message()
