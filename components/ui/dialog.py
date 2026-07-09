# import uuid

# import reflex as rx
# from reflex.components.component import ComponentNamespace
# from reflex_components_core.el import Div

# from ..core.core import CoreComponent, cn


# class ClassNames:
#     POPUP = (
#         "hidden open:grid m-auto w-full max-w-[calc(100%-2rem)] gap-4 rounded-xl "
#         "bg-popover p-4 text-sm text-popover-foreground ring-1 ring-foreground/10 "
#         "outline-hidden sm:max-w-sm "
#         "backdrop:bg-black/10 backdrop:supports-backdrop-filter:backdrop-blur-xs"
#     )
#     HEADER = "flex flex-col gap-2"
#     TITLE = "text-base leading-none font-medium text-foreground"
#     DESCRIPTION = "text-sm text-muted-foreground"
#     FOOTER = (
#         "-mx-4 -mb-4 flex flex-col-reverse gap-2 rounded-b-xl border-t "
#         "border-foreground/10 bg-muted/50 p-4 sm:flex-row sm:justify-end"
#     )
#     CLOSE = (
#         "rounded-xs opacity-70 transition-opacity hover:opacity-100 "
#         "focus:outline-hidden text-muted-foreground"
#     )
#     CLOSE_ICON = "!absolute !top-2 !right-2"


# class DialogRoot(CoreComponent):
#     """
#     Non-visual scoping wrapper. Trigger/close resolve their target <dialog>
#     via `closest('[data-slot="dialog-root"]')` + a scoped querySelector, the
#     same pattern Menu uses for `[data-slot="menu"]` — no manual id threading,
#     and multiple independent dialog instances on the same page (e.g. a
#     per-row "Share" dialog in a table) never cross-target each other.

#     class_name="contents" so this wrapper never introduces an extra box in
#     the layout — e.g. nesting a dialog trigger inside a button_group still
#     sees the trigger's rendered child as if it were a direct child, avoiding
#     the same nesting-depth issue that showed up with the menu trigger.
#     """

#     @classmethod
#     def create(cls, *children, **props) -> rx.Component:
#         props["data-slot"] = "dialog-root"
#         cls.set_class_name("contents", props)
#         return rx.el.div(*children, **props)


# class DialogTrigger(CoreComponent):
#     """
#     Wraps its child(ren) — typically a `button(...)` — with no visual box of
#     its own (display: contents) and attaches a CAPTURING click listener.
#     Capture-phase fires top-down before any descendant's own click handler
#     runs, so this reliably opens the dialog even if the nested Button calls
#     stopPropagation() internally (the same class of issue found with the
#     menu trigger + nested Button).
#     """

#     @classmethod
#     def create(cls, *children, **props) -> rx.Component:
#         custom_classes = props.pop("class_name", "")
#         props["data-slot"] = "dialog-trigger"

#         trigger_id = props.get("id") or f"dialog-trigger-{uuid.uuid4().hex[:8]}"
#         props["id"] = trigger_id

#         cls.set_class_name(cn("contents", custom_classes), props)

#         props["on_mount"] = rx.call_script(
#             f"""
#             (function() {{
#                 var trigger = document.getElementById('{trigger_id}');
#                 if (!trigger || trigger.__dialogTriggerAttached) return;
#                 trigger.__dialogTriggerAttached = true;
#                 trigger.addEventListener('click', function (e) {{
#                     var root = trigger.closest('[data-slot="dialog-root"]');
#                     var dlg = root
#                         ? root.querySelector('dialog[data-slot="dialog-content"]')
#                         : null;
#                     if (dlg) dlg.showModal();
#                 }}, true);
#             }})()
#             """
#         )
#         return rx.el.div(*children, **props)


# class DialogPopup(Div, CoreComponent):
#     @classmethod
#     def create(
#         cls,
#         *children,
#         dismissible: bool = True,
#         on_open_change: rx.EventHandler | None = None,
#         **props,
#     ) -> rx.Component:
#         props["data-slot"] = "dialog-content"
#         cls.set_class_name(ClassNames.POPUP, props)

#         if on_open_change is not None:
#             props["on_close"] = lambda: on_open_change(False)
#         if not dismissible:
#             props["on_cancel"] = rx.prevent_default

#         return rx.el.dialog(*children, **props)


# class DialogClose(CoreComponent):
#     """
#     Same "contents"-wrapper + capture-listener behavior as DialogTrigger, but
#     calls `.close()` instead of `.showModal()`. Purely behavioral — it has no
#     default visual styling of its own, so it never fights with whatever
#     you're wrapping. Apply `dialog.class_names.CLOSE` /
#     `dialog.class_names.CLOSE_ICON` directly to the child you pass in when
#     you want the default close-button look (see examples).
#     """

#     @classmethod
#     def create(cls, *children, **props) -> rx.Component:
#         custom_classes = props.pop("class_name", "")
#         props["data-slot"] = "dialog-close"

#         close_id = props.get("id") or f"dialog-close-{uuid.uuid4().hex[:8]}"
#         props["id"] = close_id

#         cls.set_class_name(cn("contents", custom_classes), props)

#         props["on_mount"] = rx.call_script(
#             f"""
#             (function() {{
#                 var closer = document.getElementById('{close_id}');
#                 if (!closer || closer.__dialogCloseAttached) return;
#                 closer.__dialogCloseAttached = true;
#                 closer.addEventListener('click', function (e) {{
#                     var root = closer.closest('[data-slot="dialog-root"]');
#                     var dlg = root
#                         ? root.querySelector('dialog[data-slot="dialog-content"]')
#                         : null;
#                     if (dlg) dlg.close();
#                 }}, true);
#             }})()
#             """
#         )
#         return rx.el.div(*children, **props)


# class DialogTitle(CoreComponent):
#     @classmethod
#     def create(cls, *children, **props) -> rx.Component:
#         props["data-slot"] = "dialog-title"
#         cls.set_class_name(ClassNames.TITLE, props)
#         return rx.el.h2(*children, **props)


# class DialogDescription(CoreComponent):
#     @classmethod
#     def create(cls, *children, **props) -> rx.Component:
#         props["data-slot"] = "dialog-description"
#         cls.set_class_name(ClassNames.DESCRIPTION, props)
#         return rx.el.p(*children, **props)


# class DialogHeader(Div, CoreComponent):
#     @classmethod
#     def create(cls, *children, **props) -> Div:
#         props["data-slot"] = "dialog-header"
#         cls.set_class_name(ClassNames.HEADER, props)
#         return super().create(*children, **props)


# class DialogFooter(Div, CoreComponent):
#     @classmethod
#     def create(cls, *children, **props) -> Div:
#         props["data-slot"] = "dialog-footer"
#         cls.set_class_name(ClassNames.FOOTER, props)
#         return super().create(*children, **props)


# class Dialog(ComponentNamespace):
#     root = staticmethod(DialogRoot.create)
#     trigger = staticmethod(DialogTrigger.create)
#     popup = staticmethod(DialogPopup.create)
#     close = staticmethod(DialogClose.create)
#     title = staticmethod(DialogTitle.create)
#     description = staticmethod(DialogDescription.create)
#     header = staticmethod(DialogHeader.create)
#     footer = staticmethod(DialogFooter.create)
#     class_names = ClassNames


# dialog = Dialog()

import uuid

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


class DialogRoot(CoreComponent):
    """
    Non-visual scoping wrapper. Trigger/close resolve their target <dialog>
    via `closest('[data-slot="dialog-root"]')` + a scoped querySelector, the
    same pattern Menu uses for `[data-slot="menu"]` — no manual id threading,
    and multiple independent dialog instances on the same page (e.g. a
    per-row "Share" dialog in a table) never cross-target each other.

    class_name="contents" so this wrapper never introduces an extra box in
    the layout — e.g. nesting a dialog trigger inside a button_group still
    sees the trigger's rendered child as if it were a direct child, avoiding
    the same nesting-depth issue that showed up with the menu trigger.
    """

    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "dialog-root"
        cls.set_class_name("contents", props)
        return rx.el.div(*children, **props)


class DialogTrigger(CoreComponent):
    """
    Wraps its child(ren) — typically a `button(...)` — with no visual box of
    its own (display: contents) and attaches a CAPTURING click listener.
    Capture-phase fires top-down before any descendant's own click handler
    runs, so this reliably opens the dialog even if the nested Button calls
    stopPropagation() internally (the same class of issue found with the
    menu trigger + nested Button).
    """

    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        custom_classes = props.pop("class_name", "")
        props["data-slot"] = "dialog-trigger"

        trigger_id = props.get("id") or f"dialog-trigger-{uuid.uuid4().hex[:8]}"
        props["id"] = trigger_id

        cls.set_class_name(cn("contents", custom_classes), props)

        props["on_mount"] = rx.call_script(
            f"""
            (function() {{
                var trigger = document.getElementById('{trigger_id}');
                if (!trigger || trigger.__dialogTriggerAttached) return;
                trigger.__dialogTriggerAttached = true;
                trigger.addEventListener('click', function (e) {{
                    var root = trigger.closest('[data-slot="dialog-root"]');
                    var dlg = root
                        ? root.querySelector('dialog[data-slot="dialog-content"]')
                        : null;
                    if (dlg) dlg.showModal();
                }}, true);
            }})()
            """
        )
        return rx.el.div(*children, **props)


class DialogPopup(Div, CoreComponent):
    @classmethod
    def create(
        cls,
        *children,
        dismissible: bool = True,
        on_open_change: rx.EventHandler | None = None,
        **props,
    ) -> rx.Component:
        props["data-slot"] = "dialog-content"
        cls.set_class_name(ClassNames.POPUP, props)

        if on_open_change is not None:
            props["on_close"] = lambda: on_open_change(False)
        if not dismissible:
            props["on_cancel"] = rx.prevent_default

        if dismissible:
            popup_id = props.get("id") or f"dialog-content-{uuid.uuid4().hex[:8]}"
            props["id"] = popup_id

            # A modal <dialog>'s own box fills the viewport (UA default) —
            # the visible "card" is just the dialog element sized/centered
            # via m-auto/max-w-*. So a click in the dimmed area around the
            # card lands ON the <dialog> element itself, just not on any of
            # its children — checking event.target === dlg reliably tells
            # "clicked the backdrop" apart from "clicked inside the card."
            existing_on_mount = props.pop("on_mount", None)
            close_on_backdrop_script = rx.call_script(
                f"""
                (function() {{
                    var dlg = document.getElementById('{popup_id}');
                    if (!dlg || dlg.__dialogBackdropAttached) return;
                    dlg.__dialogBackdropAttached = true;
                    dlg.addEventListener('click', function (e) {{
                        if (e.target === dlg) dlg.close();
                    }});
                }})()
                """
            )
            if existing_on_mount is not None:
                events = (
                    existing_on_mount
                    if isinstance(existing_on_mount, list)
                    else [existing_on_mount]
                )
                props["on_mount"] = [*events, close_on_backdrop_script]
            else:
                props["on_mount"] = close_on_backdrop_script

        return rx.el.dialog(*children, **props)


class DialogClose(CoreComponent):
    """
    Same "contents"-wrapper + capture-listener behavior as DialogTrigger, but
    calls `.close()` instead of `.showModal()`. Purely behavioral — it has no
    default visual styling of its own, so it never fights with whatever
    you're wrapping. Apply `dialog.class_names.CLOSE` /
    `dialog.class_names.CLOSE_ICON` directly to the child you pass in when
    you want the default close-button look (see examples).
    """

    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        custom_classes = props.pop("class_name", "")
        props["data-slot"] = "dialog-close"

        close_id = props.get("id") or f"dialog-close-{uuid.uuid4().hex[:8]}"
        props["id"] = close_id

        cls.set_class_name(cn("contents", custom_classes), props)

        props["on_mount"] = rx.call_script(
            f"""
            (function() {{
                var closer = document.getElementById('{close_id}');
                if (!closer || closer.__dialogCloseAttached) return;
                closer.__dialogCloseAttached = true;
                closer.addEventListener('click', function (e) {{
                    var root = closer.closest('[data-slot="dialog-root"]');
                    var dlg = root
                        ? root.querySelector('dialog[data-slot="dialog-content"]')
                        : null;
                    if (dlg) dlg.close();
                }}, true);
            }})()
            """
        )
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
    root = staticmethod(DialogRoot.create)
    trigger = staticmethod(DialogTrigger.create)
    popup = staticmethod(DialogPopup.create)
    close = staticmethod(DialogClose.create)
    title = staticmethod(DialogTitle.create)
    description = staticmethod(DialogDescription.create)
    header = staticmethod(DialogHeader.create)
    footer = staticmethod(DialogFooter.create)
    class_names = ClassNames


dialog = Dialog()
