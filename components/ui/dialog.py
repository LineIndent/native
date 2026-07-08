import reflex as rx
from reflex.components.component import ComponentNamespace
from reflex_components_core.el import Div

from ..core.core import CoreComponent, cn


class ClassNames:
    POPUP = (
        "hidden open:grid m-auto w-full max-w-[calc(100%-2rem)] gap-4 rounded-xl "
        "bg-popover p-4 text-sm text-popover-foreground ring-1 ring-foreground/10 "
        "outline-hidden sm:max-w-sm "
        "backdrop:bg-black/10 backdrop:supports-backdrop-filter:backdrop-blur-xs"
    )
    HEADER = "flex flex-col gap-2"
    TITLE = "text-base leading-none font-medium text-foreground"
    DESCRIPTION = "text-sm text-muted-foreground"
    FOOTER = (
        "-mx-4 -mb-4 flex flex-col-reverse gap-2 rounded-b-xl border-t "
        "border-foreground/10 bg-muted/50 p-4 sm:flex-row sm:justify-end"
    )
    CLOSE = (
        "rounded-xs opacity-70 transition-opacity hover:opacity-100 "
        "focus:outline-hidden text-muted-foreground"
    )
    CLOSE_ICON = "!absolute !top-2 !right-2"


class DialogTrigger(CoreComponent):
    @classmethod
    def create(cls, *children, dialog_id: str, **props) -> rx.Component:
        props["data-slot"] = "dialog-trigger"
        props.setdefault("type", "button")
        props["on_click"] = rx.call_script(
            f"document.getElementById('{dialog_id}').showModal()"
        )
        return rx.el.div(*children, **props)


class DialogPopup(Div, CoreComponent):
    @classmethod
    def create(
        cls,
        *children,
        dialog_id: str,
        dismissible: bool = True,
        on_open_change: rx.EventHandler | None = None,
        **props,
    ) -> rx.Component:
        props["data-slot"] = "dialog-content"
        props["id"] = dialog_id
        cls.set_class_name(ClassNames.POPUP, props)

        if on_open_change is not None:
            props["on_close"] = lambda: on_open_change(False)
        if not dismissible:
            props["on_cancel"] = rx.prevent_default

        return rx.el.dialog(*children, **props)


class DialogClose(CoreComponent):
    @classmethod
    def create(
        cls, *children, dialog_id: str, variant: str = "default", **props
    ) -> rx.Component:
        props["data-slot"] = "dialog-close"
        props.setdefault("type", "button")
        props["on_click"] = rx.call_script(
            f"document.getElementById('{dialog_id}').close()"
        )

        class_name = ClassNames.CLOSE
        if variant == "icon":
            class_name = cn(class_name, ClassNames.CLOSE_ICON)

        cls.set_class_name(class_name, props)
        return rx.el.div(*children, **props)


class DialogTitle(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "dialog-title"
        cls.set_class_name(ClassNames.TITLE, props)
        return rx.el.h2(*children, **props)


class DialogDescription(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "dialog-description"
        cls.set_class_name(ClassNames.DESCRIPTION, props)
        return rx.el.p(*children, **props)


class DialogHeader(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Div:
        props["data-slot"] = "dialog-header"
        cls.set_class_name(ClassNames.HEADER, props)
        return super().create(*children, **props)


class DialogFooter(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Div:
        props["data-slot"] = "dialog-footer"
        cls.set_class_name(ClassNames.FOOTER, props)
        return super().create(*children, **props)


class Dialog(ComponentNamespace):
    trigger = staticmethod(DialogTrigger.create)
    popup = staticmethod(DialogPopup.create)
    close = staticmethod(DialogClose.create)
    title = staticmethod(DialogTitle.create)
    description = staticmethod(DialogDescription.create)
    header = staticmethod(DialogHeader.create)
    footer = staticmethod(DialogFooter.create)
    class_names = ClassNames


dialog = Dialog()
