import itertools
import uuid

import reflex as rx
from reflex.components.component import ComponentNamespace

from .core import CoreComponent, cn

_menu_id_counter = itertools.count()


class ClassNames:
    # Keep <summary> itself as inline-block (NOT flex/grid) — several browser
    # engines tie the native click-to-toggle behavior on <summary> to its
    # special internal `display: list-item` rendering. Overriding it to
    # flex/grid directly can silently break the open/close toggle entirely.
    TRIGGER = "inline-block list-none cursor-pointer [&::-webkit-details-marker]:hidden"
    TRIGGER_INNER = "flex w-fit items-center"
    CONTENT = (
        "absolute z-50 min-w-32 rounded-lg bg-popover p-1 text-popover-foreground "
        "shadow-md ring-1 ring-foreground/10 outline-none"
    )
    ITEM = (
        "group/menu-item relative flex cursor-default items-center gap-1.5 "
        "rounded-lg px-1.5 py-1 text-sm outline-hidden select-none "
        "hover:bg-accent hover:text-accent-foreground "
        "data-[variant=destructive]:text-destructive "
        "data-[variant=destructive]:hover:bg-destructive/10 "
        "data-[variant=destructive]:hover:text-destructive "
        "data-disabled:pointer-events-none data-disabled:opacity-50 "
        "[&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4"
    )
    SEPARATOR = "-mx-1 my-1 h-px bg-border"
    GROUP_LABEL = "px-1.5 py-1 text-xs font-medium text-muted-foreground"
    SHORTCUT = "ml-auto text-xs tracking-widest text-muted-foreground"
    SIDE_OFFSETS = {
        "bottom": "top-full",
        "top": "bottom-full",
        "right": "left-full",
        "left": "right-full",
    }


class MenuRoot(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props.setdefault("id", f"menu-{next(_menu_id_counter)}")
        props["data-slot"] = "menu"
        cls.set_class_name("relative inline-block", props)

        # Attach two document-level listeners exactly once, no matter how
        # many MenuRoots get mounted:
        #   - Escape closes any currently-open menu
        #   - a click outside an open menu's bounds closes it
        # Both query generically by data-slot="menu" rather than a specific
        # id, so a single listener pair handles every menu on the page.
        props["on_mount"] = rx.call_script(
            """
            if (!window.__menuGlobalHandlersAttached) {
                window.__menuGlobalHandlersAttached = true;

                document.addEventListener('keydown', function (e) {
                    if (e.key === 'Escape') {
                        document
                            .querySelectorAll('details[data-slot="menu"][open]')
                            .forEach(function (el) { el.open = false; });
                    }
                });

                document.addEventListener('click', function (e) {
                    document
                        .querySelectorAll('details[data-slot="menu"][open]')
                        .forEach(function (el) {
                            if (!el.contains(e.target)) {
                                el.open = false;
                            }
                        });
                });
            }
            """
        )

        return rx.el.details(*children, **props)


class MenuTrigger(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "menu-trigger"
        cls.set_class_name(ClassNames.TRIGGER, props)
        # Children live in an inner flex wrapper rather than on <summary>
        # itself, so <summary> can stay inline-block (safe for the native
        # toggle) while still visually hugging/aligning its content (e.g.
        # an avatar) with no dead click-zone underneath.
        return rx.el.summary(
            rx.el.div(*children, class_name=ClassNames.TRIGGER_INNER),
            **props,
        )


class MenuContent(CoreComponent):
    @classmethod
    def create(
        cls,
        *children,
        side: str = "bottom",
        side_offset: int = 4,
        align: str = "start",
        **props,
    ) -> rx.Component:
        props["data-slot"] = "menu-content"
        props["data-side"] = side

        margin_key = {
            "bottom": "marginTop",
            "top": "marginBottom",
            "left": "marginRight",
            "right": "marginLeft",
        }.get(side, "marginTop")
        props["style"] = {margin_key: f"{side_offset}px", **props.get("style", {})}

        position_class = ClassNames.SIDE_OFFSETS.get(side, "top-full")
        align_class = {
            "start": "left-0",
            "end": "right-0",
            "center": "left-1/2 -translate-x-1/2",
        }.get(align, "left-0")

        cls.set_class_name(cn(ClassNames.CONTENT, position_class, align_class), props)
        return rx.el.div(*children, **props)


class MenuItem(CoreComponent):
    """
    Note: if rendered inside rx.foreach, the auto-generated uuid is baked in
    once at template-build time and shared across all rendered items. Pass
    an explicit `id` derived from your loop data in that case, e.g.
    id=f"menu-item-{item.id}".
    """

    @classmethod
    def create(cls, *children, close_on_click: bool = True, **props) -> rx.Component:
        props["data-slot"] = "menu-item"
        cls.set_class_name(ClassNames.ITEM, props)

        item_id = props.get("id") or f"menu-item-{uuid.uuid4().hex[:8]}"
        props["id"] = item_id

        # 1. Pop out any existing user on_click triggers (can be None, an event, or a list)
        user_on_click = props.pop("on_click", None)

        # Initialize an empty list to collect all click actions
        click_events = []

        # 2. Append the user's custom event(s) if they provided any
        if user_on_click is not None:
            if isinstance(user_on_click, list):
                click_events.extend(user_on_click)
            else:
                click_events.append(user_on_click)

        # 3. If close_on_click is active, append a script that walks up from
        # this item to its nearest ancestor menu and closes it — no manual
        # menu_id wiring required.
        if close_on_click:
            close_script = rx.call_script(
                f"""
                const item = document.getElementById('{item_id}');
                const root = item ? item.closest('[data-slot="menu"]') : null;
                if (root) root.open = false;
                """
            )
            click_events.append(close_script)

        # 4. Bind the combined chain back to props if there's anything to execute
        if click_events:
            props["on_click"] = click_events

        return rx.el.div(*children, **props)


class MenuClose(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "menu-close"
        props.setdefault("type", "button")

        close_id = props.get("id") or f"menu-close-{uuid.uuid4().hex[:8]}"
        props["id"] = close_id

        props["on_click"] = rx.call_script(
            f"""
            const btn = document.getElementById('{close_id}');
            const root = btn ? btn.closest('[data-slot="menu"]') : null;
            if (root) root.open = false;
            """
        )

        cls.set_class_name(ClassNames.ITEM, props)
        return rx.el.div(*children, **props)


class MenuSeparator(CoreComponent):
    @classmethod
    def create(cls, **props) -> rx.Component:
        props["data-slot"] = "menu-separator"
        cls.set_class_name(ClassNames.SEPARATOR, props)
        return rx.el.div(**props)


class MenuGroupLabel(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "menu-group-label"
        cls.set_class_name(ClassNames.GROUP_LABEL, props)
        return rx.el.div(*children, **props)


class MenuShortcut(CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "menu-shortcut"
        cls.set_class_name(ClassNames.SHORTCUT, props)
        return rx.el.span(*children, **props)


class Menu(ComponentNamespace):
    root = staticmethod(MenuRoot.create)
    trigger = staticmethod(MenuTrigger.create)
    content = staticmethod(MenuContent.create)
    item = staticmethod(MenuItem.create)
    close = staticmethod(MenuClose.create)
    separator = staticmethod(MenuSeparator.create)
    group_label = staticmethod(MenuGroupLabel.create)
    shortcut = staticmethod(MenuShortcut.create)
    class_names = ClassNames


menu = Menu()
