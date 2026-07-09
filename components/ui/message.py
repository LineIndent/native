from typing import Literal

import reflex as rx
from reflex.components.component import ComponentNamespace

from ..core.core import cn

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


def message_group(*children, class_name: str = "", **props) -> rx.Component:
    ##

    return rx.el.div(
        *children,
        data_slot="message-group",
        class_name=cn(ClassNames.GROUP, class_name),
        **props,
    )


def message_root(
    *children,
    align: MessageAlign = "start",
    class_name: str = "",
    **props,
) -> rx.Component:
    ##

    return rx.el.div(
        *children,
        data_slot="message",
        data_align=align,
        class_name=cn(ClassNames.ROOT, class_name),
        **props,
    )


def message_avatar(*children, class_name: str = "", **props) -> rx.Component:
    ##

    return rx.el.div(
        *children,
        data_slot="message-avatar",
        class_name=cn(ClassNames.AVATAR, class_name),
        **props,
    )


def message_content(*children, class_name: str = "", **props) -> rx.Component:
    ##

    return rx.el.div(
        *children,
        data_slot="message-content",
        class_name=cn(ClassNames.CONTENT, class_name),
        **props,
    )


def message_header(*children, class_name: str = "", **props) -> rx.Component:
    ##

    return rx.el.div(
        *children,
        data_slot="message-header",
        class_name=cn(ClassNames.HEADER, class_name),
        **props,
    )


def message_footer(*children, class_name: str = "", **props) -> rx.Component:
    ##

    return rx.el.div(
        *children,
        data_slot="message-footer",
        class_name=cn(ClassNames.FOOTER, class_name),
        **props,
    )


class Message(ComponentNamespace):
    ##


    group = staticmethod(message_group)
    root = staticmethod(message_root)
    avatar = staticmethod(message_avatar)
    content = staticmethod(message_content)
    header = staticmethod(message_header)
    footer = staticmethod(message_footer)

    class_names = ClassNames


message = Message()
