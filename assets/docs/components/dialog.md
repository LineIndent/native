---
title: "Dialog"
description: "A window overlaid on either the primary window or another dialog window, rendering the content underneath inert."
order: 8
---


## Dialog, A Window Overlaid On Either The Primary Window Or Another Dialog Window, Rendering The Content Underneath Inert.


```python
from components.ui.dialog import Dialog
```

```python
from typing import Any

from reflex.components.component import Component
from reflex.utils.imports import ImportVar
from reflex.vars import FunctionVar, Var
from reflex.vars.base import VarData

PACKAGE_CN = "clsx-for-tailwind@1.0.0"
CN = Var(
    "cn",
    _var_data=VarData(
        imports={
            PACKAGE_CN: ImportVar(tag="cn"),
        },
    ),
).to(FunctionVar)


class CoreComponent(Component):
    unstyled: Var[bool]

    @classmethod
    def set_class_name(
        cls, default_class_name: str | Var[str], props: dict[str, Any]
    ) -> None:

        if "render_" in props:
            return

        props_class_name = props.get("class_name", "")

        if props.pop("unstyled", False):
            props["class_name"] = props_class_name
            return

        props["class_name"] = cn(default_class_name, props_class_name)

    def _exclude_props(self) -> list[str]:
        return [
            *super()._exclude_props(),
            "unstyled",
        ]


def cn(*classes: Var | str | tuple | list | None) -> Var:
    return CN.call(*classes).to(str)
```

```python
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
    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        props["data-slot"] = "dialog-root"
        cls.set_class_name("contents", props)
        return rx.el.div(*children, **props)


class DialogTrigger(CoreComponent):
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

        custom_classes = props.pop("class_name", "")

        cls.set_class_name(cn(ClassNames.POPUP, custom_classes), props)

        if on_open_change is not None:
            props["on_close"] = lambda: on_open_change(False)
        if not dismissible:
            props["on_cancel"] = rx.prevent_default

        if dismissible:
            popup_id = props.get("id") or f"dialog-content-{uuid.uuid4().hex[:8]}"
            props["id"] = popup_id

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
```

# Examples

## Custom Close Button

Replace the default close control with your own button. Apply `dialog.class_names.CLOSE_ICON` to it for correct top-right positioning.

**Props used:** `class_name` on the button passed to `dialog.close`.

```python
def dialog_close_button() -> rx.Component:
    return dialog.root(
        dialog.trigger(button("Share", variant="outline")),
        dialog.popup(
            dialog.header(
                dialog.title("Share link"),
                dialog.description(
                    "Anyone who has this link will be able to view this."
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label("Link", html_for="link", class_name="sr-only"),
                    input(
                        id="link",
                        default_value="https://ui.buridan.com/docs/getting-started/installation",
                        read_only=True,
                    ),
                    class_name="grid flex-1 gap-2",
                ),
                class_name="flex items-center gap-2",
            ),
            dialog.footer(
                dialog.close(button("Close", type="button")),
                class_name="sm:justify-start",
            ),
            dialog.close(
                button(
                    hi("Cancel01Icon", class_name="size-4"),
                    variant="ghost",
                    size="icon-sm",
                    class_name=dialog.class_names.CLOSE_ICON,
                )
            ),
            class_name="sm:max-w-md",
        ),
    )
```

## No Close Button

To omit the top-right close icon, simply don't render a `dialog.close(...)` for it — every other close mechanism (Escape, backdrop click, a footer button) still works.

**Props used:** none required — omit the icon `dialog.close(...)` call.

```python
def dialog_no_close_button() -> rx.Component:
    return dialog.root(
        dialog.trigger(button("No Close Button", variant="outline")),
        dialog.popup(
            dialog.header(
                dialog.title("No Close Button"),
                dialog.description(
                    "This dialog doesn't have a close button in the top-right corner."
                ),
            ),
        ),
    )
```

## Sticky Footer

Keep actions visible while the content scrolls, using `dialog.footer`.

**Props used:** none required beyond standard `dialog.footer` composition.

```python
def dialog_sticky_footer() -> rx.Component:
    return dialog.root(
        dialog.trigger(button("Sticky Footer", variant="outline")),
        dialog.popup(
            dialog.header(
                dialog.title("Sticky Footer"),
                dialog.description(
                    "This dialog has a sticky footer that stays visible while the content scrolls."
                ),
            ),
            rx.el.div(
                *[
                    rx.el.p(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do "
                        "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut "
                        "enim ad minim veniam, quis nostrud exercitation ullamco laboris "
                        "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in "
                        "reprehenderit in voluptate velit esse cillum dolore eu fugiat "
                        "nulla pariatur. Excepteur sint occaecat cupidatat non proident, "
                        "sunt in culpa qui officia deserunt mollit anim id est laborum.",
                        class_name="mb-4 leading-normal",
                    )
                    for _ in range(10)
                ],
                class_name="-mx-4 no-scrollbar max-h-[50vh] overflow-y-auto px-4",
            ),
            dialog.footer(
                dialog.close(button("Close", variant="outline")),
            ),
            dialog.close(
                button(
                    hi("Cancel01Icon", class_name="size-4"),
                    variant="ghost",
                    size="icon-sm",
                    class_name=dialog.class_names.CLOSE_ICON,
                )
            ),
        ),
    )
```

# API Reference

## dialog.root

Non-visual scoping wrapper (`display: contents`, adds no layout box). Trigger and close resolve their target `<dialog>` by walking up to the nearest `dialog.root` — no manual id threading, and multiple independent dialogs on the same page (e.g. a per-row "Share" dialog) never cross-target each other.

```python
dialog.root(
    dialog.trigger(button("Share", variant="outline")),
    dialog.popup(...),
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## dialog.trigger

Wraps its child (typically a `button(...)`) with a capturing click listener that calls `.showModal()` on the nearest `dialog.popup`. No visual box of its own, so nesting a styled button inside doesn't add extra layout depth.

```python
dialog.trigger(button("Share", variant="outline"))
```

| Prop         | Type  | Default          |
| ------------ | ----- | ---------------- |
| `id`         | `str` | auto-generated    |
| `class_name` | `str` | `""`              |

## dialog.popup

Renders the native `<dialog>`. Escape and backdrop clicks both close it when `dismissible=True` (the default).

```python
dialog.popup(
    dialog.header(dialog.title("Share link")),
    ...,
)
```

| Prop              | Type                        | Default |
| ----------------- | ---------------------------- | ------- |
| `dismissible`      | `bool`                       | `True`  |
| `on_open_change`   | `EventHandler[[bool]] \| None` | `None`  |
| `class_name`       | `str`                        | `""`    |

When `dismissible=False`, both Escape and backdrop-click are disabled — only an explicit `dialog.close(...)` can close it.

## dialog.close

Same behavioral wrapper as `dialog.trigger`, but calls `.close()`. Has no default visual styling of its own — apply `dialog.class_names.CLOSE` / `dialog.class_names.CLOSE_ICON` to whatever you pass in.

```python
dialog.close(button("Close", type="button"))

dialog.close(
    button(
        hi("Cancel01Icon", class_name="size-4"),
        variant="ghost",
        size="icon-sm",
        class_name=dialog.class_names.CLOSE_ICON,
    )
)
```

| Prop         | Type  | Default          |
| ------------ | ----- | ---------------- |
| `id`         | `str` | auto-generated    |
| `class_name` | `str` | `""`              |

## dialog.title

```python
dialog.title("Share link")
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## dialog.description

```python
dialog.description("Anyone who has this link will be able to view this.")
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## dialog.header

```python
dialog.header(
    dialog.title("Share link"),
    dialog.description("..."),
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## dialog.footer

```python
dialog.footer(dialog.close(button("Close", type="button")))
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |
