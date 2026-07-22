---
title: "Input Group"
description: "Add addons, buttons, and helper content to inputs."
order: 0
---


## Input Group, Add Addons, Buttons, And Helper Content To Inputs.



> Component `input_group` not found


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
from typing import Literal

from reflex.vars.base import Var
from reflex_components_core.el import Button as BaseButton

from ..core.core import CoreComponent, cn

LiteralButtonVariant = Literal[
    "default",
    "destructive",
    "outline",
    "secondary",
    "ghost",
    "link",
]
LiteralButtonSize = Literal[
    "default",
    "xs",
    "sm",
    "lg",
    "icon",
    "icon-xs",
    "icon-sm",
    "icon-lg",
]

DEFAULT_CLASS_NAME = (
    "group/button inline-flex shrink-0 items-center justify-center "
    "rounded-lg border border-transparent bg-clip-padding "
    "text-sm font-medium whitespace-nowrap outline-none select-none "
    "focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50 "
    "active:not-aria-[haspopup]:translate-y-px "
    "disabled:pointer-events-none disabled:opacity-50 "
    "aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20 "
    "dark:aria-invalid:border-destructive/50 dark:aria-invalid:ring-destructive/40 "
    "[&_svg]:pointer-events-none [&_svg]:shrink-0 "
    "[&_svg:not([class*='size-'])]:size-4"
)

BUTTON_VARIANTS = {
    "variant": {
        "default": ("bg-primary text-primary-foreground hover:bg-primary/80"),
        "outline": (
            "border-border bg-background hover:bg-muted hover:text-foreground "
            "aria-expanded:bg-muted aria-expanded:text-foreground "
            "dark:border-input dark:bg-input/30 dark:hover:bg-input/50"
        ),
        "secondary": (
            "bg-secondary text-secondary-foreground "
            "hover:bg-[color-mix(in_oklch,var(--secondary),var(--foreground)_5%)] "
            "aria-expanded:bg-secondary aria-expanded:text-secondary-foreground"
        ),
        "ghost": (
            "hover:bg-muted hover:text-foreground "
            "aria-expanded:bg-muted aria-expanded:text-foreground "
            "dark:hover:bg-muted/50"
        ),
        "destructive": (
            "bg-destructive/10 text-destructive hover:bg-destructive/20 "
            "focus-visible:border-destructive/40 focus-visible:ring-destructive/20 "
            "dark:bg-destructive/20 dark:hover:bg-destructive/30 "
            "dark:focus-visible:ring-destructive/40"
        ),
        "link": "text-primary underline-offset-4 hover:underline",
    },
    "size": {
        "default": (
            "h-8 gap-1.5 px-2.5 "
            "has-data-[icon=inline-end]:pr-2 "
            "has-data-[icon=inline-start]:pl-2"
        ),
        "xs": (
            "h-6 gap-1 rounded-[min(var(--radius-md),10px)] px-2 text-xs "
            "in-data-[slot=button-group]:rounded-lg "
            "has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 "
            "[&_svg:not([class*='size-'])]:size-3"
        ),
        "sm": (
            "h-7 gap-1 rounded-[min(var(--radius-md),12px)] px-2.5 text-[0.8rem] "
            "in-data-[slot=button-group]:rounded-lg "
            "has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 "
            "[&_svg:not([class*='size-'])]:size-3.5"
        ),
        "lg": (
            "h-9 gap-1.5 px-2.5 "
            "has-data-[icon=inline-end]:pr-2 "
            "has-data-[icon=inline-start]:pl-2"
        ),
        "icon": "size-8",
        "icon-xs": (
            "size-6 rounded-[min(var(--radius-md),10px)] "
            "in-data-[slot=button-group]:rounded-lg "
            "[&_svg:not([class*='size-'])]:size-3"
        ),
        "icon-sm": (
            "size-7 rounded-[min(var(--radius-md),12px)] "
            "in-data-[slot=button-group]:rounded-lg"
        ),
        "icon-lg": "size-9",
    },
}


class Button(BaseButton, CoreComponent):
    variant: Var[LiteralButtonVariant]
    size: Var[LiteralButtonSize]

    @classmethod
    def create(cls, *children, **props) -> BaseButton:
        variant = props.pop("variant", "default")
        size = props.pop("size", "default")
        custom_classes = props.pop("class_name", "")
        data_slot = props.pop("data_slot", "button")

        return super().create(
            *children,
            data_slot=data_slot,
            class_name=cn(
                DEFAULT_CLASS_NAME,
                BUTTON_VARIANTS["variant"].get(variant, ""),
                BUTTON_VARIANTS["size"].get(size, ""),
                custom_classes,
            ),
            **props,
        )

    def _exclude_props(self) -> list[str]:
        return [*super()._exclude_props(), "size", "variant"]


def button_variants(variant: str = "default", size: str = "default") -> Var:
    return cn(
        DEFAULT_CLASS_NAME,
        BUTTON_VARIANTS["variant"].get(variant, ""),
        BUTTON_VARIANTS["size"].get(size, ""),
    )


button = Button.create
```

```python
from reflex.components.component import ComponentNamespace
from reflex_components_core.el import Input as BaseInput

from ..core.core import CoreComponent, cn


class ClassNames:
    INPUT = (
        "w-full file:text-foreground placeholder:text-muted-foreground "
        "selection:bg-primary selection:text-primary-foreground "
        "dark:bg-input/30 border-input "
        "h-8 w-full min-w-0 rounded-lg border bg-transparent px-3 py-1 text-base "
        "outline-none "
        "file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium "
        "disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 "
        "md:text-sm "
        "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] "
        "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 "
        "aria-invalid:border-destructive"
    )


class InputComponent(BaseInput, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> BaseInput:

        existing_class = props.get("class_name", "")

        props["class_name"] = cn(ClassNames.INPUT, existing_class)

        props.setdefault("data_slot", "input")

        if "type" not in props:
            props["type"] = "text"

        return super().create(*children, **props)


class Input(ComponentNamespace):
    __call__ = staticmethod(InputComponent.create)
    class_name = ClassNames


input = Input()
```

```python
from reflex_components_core.el import Textarea

from ..core.core import CoreComponent


class ClassNames:
    ROOT = (
        "flex field-sizing-content min-h-16 w-full rounded-lg border border-input bg-transparent "
        "px-2.5 py-2 text-base transition-colors outline-none placeholder:text-muted-foreground "
        "focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50 disabled:cursor-not-allowed "
        "disabled:bg-input/50 disabled:opacity-50 aria-invalid:border-destructive aria-invalid:ring-3 "
        "aria-invalid:ring-destructive/20 md:text-sm dark:bg-input/30 dark:disabled:bg-input/80 "
        "dark:aria-invalid:border-destructive/50 dark:aria-invalid:ring-destructive/40"
    )


class TextAreaComponent(Textarea, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> Textarea:
        props.setdefault(
            "custom_attrs",
            {
                "autoComplete": "off",
                "autoCapitalize": "none",
                "autoCorrect": "off",
                "spellCheck": "false",
            },
        )
        props.setdefault("data_slot", "textarea")
        cls.set_class_name(ClassNames.ROOT, props)
        return super().create(*children, **props)


textarea = TextAreaComponent.create
```

```python
from typing import Literal

from reflex.components.component import ComponentNamespace
from reflex_components_core.el import Div as ElDiv
from reflex_components_core.el import Span as ElSpan

from ..core.core import CoreComponent, cn
from .button import button
from .input import input
from .textarea import textarea

LiteralAlign = Literal["inline-start", "inline-end", "block-start", "block-end"]
LiteralSize = Literal["xs", "sm", "icon-xs", "icon-sm"]


class ClassNames:
    ROOT = (
        "group/input-group relative flex h-8 w-full min-w-0 items-center rounded-lg border border-input "
        "outline-none in-data-[slot=combobox-content]:focus-within:border-inherit "
        "in-data-[slot=combobox-content]:focus-within:ring-0 has-disabled:bg-input/50 has-disabled:opacity-50 "
        "has-[[data-slot=input-group-control]:focus-visible]:border-ring has-[[data-slot=input-group-control]:focus-visible]:ring-3 "
        "has-[[data-slot=input-group-control]:focus-visible]:ring-ring/50 has-[[data-slot][aria-invalid=true]]:border-destructive "
        "has-[[data-slot][aria-invalid=true]]:ring-3 has-[[data-slot][aria-invalid=true]]:ring-destructive/20 "
        "has-[>[data-align=block-end]]:h-auto has-[>[data-align=block-end]]:flex-col has-[>[data-align=block-start]]:h-auto "
        "has-[>[data-align=block-start]]:flex-col has-[>textarea]:h-auto dark:bg-input/30 dark:has-disabled:bg-input/80 "
        "dark:has-[[data-slot][aria-invalid=true]]:ring-destructive/40 has-[>[data-align=block-end]]:[&>input]:pt-3 "
        "has-[>[data-align=block-start]]:[&>input]:pb-3 has-[>[data-align=inline-end]]:[&>input]:pr-1.5 "
        "has-[>[data-align=inline-start]]:[&>input]:pl-1.5"
    )

    ADDON = (
        "flex h-auto cursor-text items-center justify-center gap-2 py-1.5 text-sm font-medium text-muted-foreground "
        "select-none group-data-[disabled=true]/input-group:opacity-50 [&>kbd]:rounded-[calc(var(--radius)-5px)] "
        "[&>svg:not([class*='size-'])]:size-4"
    )

    TEXT = "flex items-center gap-2 text-sm text-muted-foreground [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4"

    CONTROL_INPUT = (
        "flex-1 rounded-none border-0 bg-transparent shadow-none ring-0 focus-visible:ring-0 "
        "disabled:bg-transparent aria-invalid:ring-0 dark:bg-transparent dark:disabled:bg-transparent"
    )

    CONTROL_TEXTAREA = (
        "flex-1 resize-none rounded-none border-0 bg-transparent py-2 shadow-none ring-0 focus-visible:ring-0 "
        "disabled:bg-transparent aria-invalid:ring-0 dark:bg-transparent dark:disabled:bg-transparent"
    )

    @classmethod
    def get_addon_align(cls, align: str) -> str:
        variants = {
            "inline-start": "order-first pl-2 has-[>button]:ml-[-0.3rem] has-[>kbd]:ml-[-0.15rem]",
            "inline-end": "order-last pr-2 has-[>button]:mr-[-0.3rem] has-[>kbd]:mr-[-0.15rem]",
            "block-start": "order-first w-full justify-start px-2.5 pt-2 group-has-[>input]/input-group:pt-2 [.border-b]:pb-2",
            "block-end": "order-last w-full justify-start px-2.5 pb-2 group-has-[>input]/input-group:pb-2 [.border-t]:pt-2",
        }
        return variants.get(align, variants["inline-start"])

    @classmethod
    def get_button_size(cls, size: str) -> str:
        variants = {
            "xs": "h-6 gap-1 rounded-[calc(var(--radius)-3px)] px-1.5 [&>svg:not([class*='size-'])]:size-3.5",
            "sm": "",
            "icon-xs": "size-6 rounded-[calc(var(--radius)-3px)] p-0 has-[>svg]:p-0",
            "icon-sm": "size-8 p-0 has-[>svg]:p-0",
        }
        return variants.get(size, variants["xs"])


class InputGroupRoot(ElDiv, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> ElDiv:
        props["role"] = "group"
        props["data_slot"] = "input-group"

        cls.set_class_name(ClassNames.ROOT, props)
        return super().create(*children, **props)


class InputGroupAddon(ElDiv, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> ElDiv:
        props["role"] = "group"
        props["data_slot"] = "input-group-addon"

        align = props.pop("align", "inline-start")
        props["data_align"] = align

        addon_defaults = cn(ClassNames.ADDON, ClassNames.get_addon_align(align))

        cls.set_class_name(addon_defaults, props)
        return super().create(*children, **props)

    def add_custom_code(self) -> list[str]:

        focus_script = """
        if (typeof window !== "undefined") {
            const bindInputGroupAddons = () => {
                document.querySelectorAll('[data-slot="input-group-addon"]').forEach(addon => {
                    if (!addon.onclick) {
                        addon.onclick = (e) => {
                            if (!e.target.closest('button')) {
                                addon.parentElement?.querySelector('input')?.focus();
                            }
                        };
                    }
                });
            };

            // Run immediately if DOM is already cooked
            if (document.readyState === "loading") {
                document.addEventListener("DOMContentLoaded", bindInputGroupAddons);
            } else {
                bindInputGroupAddons();
            }

            // Keep it active across single-page transitions or dynamic updates
            const observer = new MutationObserver(bindInputGroupAddons);
            observer.observe(document.body, { childList: true, subtree: true });
        }
        """
        return [focus_script]


class InputGroupText(ElSpan, CoreComponent):
    @classmethod
    def create(cls, *children, **props) -> ElSpan:
        cls.set_class_name(ClassNames.TEXT, props)
        return super().create(*children, **props)


class InputGroupButton(CoreComponent):
    @classmethod
    def create(cls, *children, **props):
        props.setdefault("type", "button")
        props.setdefault("variant", "ghost")

        size = props.pop("size", "xs")
        props["data_size"] = size

        props["class_name"] = cn(
            "flex items-center gap-2 text-sm shadow-none",
            ClassNames.get_button_size(size),
            props.get("class_name", ""),
        )

        return button(*children, **props)


class InputGroupInput(CoreComponent):
    @classmethod
    def create(cls, *children, **props):
        props.setdefault("type", "text")
        props["data_slot"] = "input-group-control"
        props["class_name"] = cn(
            ClassNames.CONTROL_INPUT,
            props.get("class_name", ""),
        )

        return input(*children, **props)


class InputGroupTextarea(CoreComponent):
    @classmethod
    def create(cls, *children, **props):
        props["data_slot"] = "input-group-control"
        props["class_name"] = cn(
            ClassNames.CONTROL_TEXTAREA, props.get("class_name", "")
        )

        return textarea(*children, **props)


class InputGroupNamespace(ComponentNamespace):
    root = staticmethod(InputGroupRoot.create)
    addon = staticmethod(InputGroupAddon.create)
    button = staticmethod(InputGroupButton.create)
    text = staticmethod(InputGroupText.create)
    input = staticmethod(InputGroupInput.create)
    textarea = staticmethod(InputGroupTextarea.create)
    class_names = ClassNames


input_group = InputGroupNamespace()
```

# Align

Use `align` on `input_group.addon` to position it relative to the input.

> For proper focus management, `input_group.addon` should always be placed **after** `input_group.input` or `input_group.textarea` in the DOM. Use `align` to visually position it instead of reordering the DOM.

## inline-start

The default — positions the addon at the start of the input.

**Props used:** `align="inline-start"` on `input_group.addon`.

```python
def input_group_inline_start() -> rx.Component:
    return input_group.root(
        input_group.input(
            id="inline-start-input",
            placeholder="Search...",
        ),
        input_group.addon(
            hi("SearchIcon", class_name="text-muted-foreground"),
            align="inline-start",
        ),
        class_name="max-w-sm",
    )
```

## inline-end

**Props used:** `align="inline-end"` on `input_group.addon`.

```python
def input_group_inline_end() -> rx.Component:
    return input_group.root(
        input_group.input(
            id="inline-end-input",
            type="password",
            placeholder="Enter password",
        ),
        input_group.addon(
            hi("EyeOffIcon", class_name="text-muted-foreground"),
            align="inline-end",
        ),
        class_name="max-w-sm",
    )
```

## block-start

Positions the addon above the input — typically used with `input_group.textarea`.

**Props used:** `align="block-start"` on `input_group.addon`.

```python
def input_group_block_start() -> rx.Component:
    return rx.el.div(
        field.root(
            field.label("Input", html_for="block-start-input"),
            field.content(
                input_group.root(
                    input_group.input(
                        id="block-start-input",
                        placeholder="Enter your name",
                    ),
                    input_group.addon(
                        input_group.text("Full Name"),
                        align="block-start",
                    ),
                    class_name="h-auto",
                )
            ),
            field.description("Header positioned above the input."),
            orientation="vertical",
        ),
        field.root(
            field.label("Textarea", html_for="block-start-textarea"),
            field.content(
                input_group.root(
                    input_group.textarea(
                        id="block-start-textarea",
                        placeholder="console.log('Hello, world!');",
                        class_name="font-mono text-sm",
                    ),
                    input_group.addon(
                        hi("FileCodeIcon", class_name="text-muted-foreground"),
                        input_group.text("script.py", class_name="font-mono"),
                        input_group.button(
                            hi("CopyIcon"),
                            rx.el.span("Copy", class_name="sr-only"),
                            size="icon-xs",
                            class_name="ml-auto",
                        ),
                        align="block-start",
                    ),
                )
            ),
            field.description("Header positioned above the textarea."),
            orientation="vertical",
        ),
        class_name="flex flex-col gap-y-6 max-w-sm w-full",
    )
```

## block-end

**Props used:** `align="block-end"` on `input_group.addon`.

```python
def input_group_block_end() -> rx.Component:
    return rx.el.div(
        field.root(
            field.label("Input", html_for="block-end-input"),
            field.content(
                input_group.root(
                    input_group.input(
                        id="block-end-input",
                        placeholder="Enter amount",
                    ),
                    input_group.addon(
                        input_group.text("USD"),
                        align="block-end",
                    ),
                    class_name="h-auto",
                )
            ),
            field.description("Footer positioned below the input."),
            orientation="vertical",
        ),
        field.root(
            field.label("Textarea", html_for="block-end-textarea"),
            field.content(
                input_group.root(
                    input_group.textarea(
                        id="block-end-textarea",
                        placeholder="Write a comment...",
                    ),
                    input_group.addon(
                        input_group.text("0/280"),
                        input_group.button(
                            "Post",
                            variant="default",
                            size="sm",
                            class_name="ml-auto",
                        ),
                        align="block-end",
                    ),
                )
            ),
            field.description("Footer positioned below the textarea."),
            orientation="vertical",
        ),
        class_name="flex flex-col gap-y-6 max-w-sm w-full",
    )
```

# Examples

## Icons

**Props used:** `align` on `input_group.addon`.

```python
def input_group_icons() -> rx.Component:
    return rx.el.div(
        input_group.root(
            input_group.input(placeholder="Search..."),
            input_group.addon(
                hi("Search01Icon", class_name="text-muted-foreground"),
                align="inline-start",
            ),
        ),
        input_group.root(
            input_group.input(type="email", placeholder="Enter your email"),
            input_group.addon(
                hi("Mail01Icon", class_name="text-muted-foreground"),
                align="inline-start",
            ),
        ),
        input_group.root(
            input_group.input(placeholder="Card number"),
            input_group.addon(
                hi("CreditCardIcon", class_name="text-muted-foreground"),
                align="inline-start",
            ),
            input_group.addon(
                hi("Tick02Icon", class_name="text-muted-foreground"),
                align="inline-end",
            ),
        ),
        input_group.root(
            input_group.input(placeholder="Card number"),
            input_group.addon(
                hi("StarIcon", class_name="text-muted-foreground"),
                hi("InformationCircleIcon", class_name="text-muted-foreground"),
                align="inline-end",
            ),
        ),
        class_name="grid w-full max-w-sm gap-6",
    )
```

## Text

**Props used:** none required beyond default `input_group.text` composition.

```python
def input_group_text() -> rx.Component:
    return rx.el.div(
        input_group.root(
            input_group.addon(
                input_group.text("$"),
                align="inline-start",
            ),
            input_group.input(placeholder="0.00"),
            input_group.addon(
                input_group.text("USD"),
                align="inline-end",
            ),
        ),
        input_group.root(
            input_group.addon(
                input_group.text("https://"),
                align="inline-start",
            ),
            input_group.input(
                placeholder="example.com",
                class_name="!pl-0.5",
            ),
            input_group.addon(
                input_group.text(".com"),
                align="inline-end",
            ),
        ),
        input_group.root(
            input_group.input(placeholder="Enter your username"),
            input_group.addon(
                input_group.text("@company.com"),
                align="inline-end",
            ),
        ),
        input_group.root(
            input_group.textarea(placeholder="Enter your message"),
            input_group.addon(
                input_group.text(
                    "120 characters left",
                    class_name="text-xs text-muted-foreground",
                ),
                align="block-end",
            ),
        ),
        class_name="grid w-full max-w-sm gap-6",
    )
```

## Button

**Props used:** `size` on `input_group.button`.

```python
def input_group_button() -> rx.Component:
    return rx.el.div(
        input_group.root(
            input_group.input(
                placeholder="https://ui.buridan.dev/",
                read_only=True,
            ),
            input_group.addon(
                input_group.button(
                    rx.cond(
                        _input_copy.value,
                        hi("Tick02Icon"),
                        hi("Copy01Icon"),
                    ),
                    aria_label="Copy",
                    title="Copy",
                    size="icon-xs",
                    on_click=[
                        _input_copy.set_value(True),
                        rx.set_clipboard("https://ui.buridan.dev/"),
                    ],
                    on_mouse_down=rx.call_function(
                        _input_copy.set_value(False)
                    ).debounce(1500),
                ),
                align="inline-end",
            ),
        ),
        input_group.root(
            input_group.addon(
                input_group.button(
                    hi("InformationCircleIcon"),
                    variant="secondary",
                    size="icon-xs",
                ),
                align="inline-start",
            ),
            input_group.addon(
                "https://",
                class_name="pl-1.5 text-muted-foreground",
                align="inline-start",
            ),
            input_group.input(id="input-secure-19"),
            input_group.addon(
                input_group.button(
                    hi(
                        "StarIcon",
                        class_name=rx.cond(
                            _input_star.value,
                            "text-blue-600 fill-blue-600",
                            "",
                        ),
                    ),
                    size="icon-xs",
                    on_click=_input_star.set_value(~_input_star.value),
                ),
                align="inline-end",
            ),
            class_name="[--radius:9999px]",
        ),
        input_group.root(
            input_group.input(placeholder="Type to search..."),
            input_group.addon(
                input_group.button(
                    "Search",
                    variant="secondary",
                ),
                align="inline-end",
            ),
        ),
        class_name="grid w-full max-w-sm gap-6",
    )
```

## Spinner

**Props used:** `align` on `input_group.addon`.

```python
def input_group_spinner() -> rx.Component:
    return rx.el.div(
        input_group.root(
            input_group.input(placeholder="Searching..."),
            input_group.addon(
                spinner(),
                align="inline-end",
            ),
        ),
        input_group.root(
            input_group.input(placeholder="Processing..."),
            input_group.addon(
                spinner(),
                align="inline-start",
            ),
        ),
        input_group.root(
            input_group.input(placeholder="Saving changes..."),
            input_group.addon(
                input_group.text("Saving..."),
                spinner(),
                align="inline-end",
            ),
        ),
        input_group.root(
            input_group.input(placeholder="Refreshing data..."),
            input_group.addon(
                spinner(),
                align="inline-start",
            ),
            input_group.addon(
                input_group.text(
                    "Please wait...",
                    class_name="text-muted-foreground",
                ),
                align="inline-end",
            ),
        ),
        class_name="grid w-full max-w-sm gap-4",
    )
```

## Dropdown

**Props used:** see the [Menu](/docs/components/menu) docs for menu-specific props.

```python
def input_group_dropdown() -> rx.Component:
    return rx.el.div(
        input_group.root(
            input_group.input(placeholder="Enter file name"),
            input_group.addon(
                menu.root(
                    menu.trigger(
                        hi("MoreHorizontal"),
                    ),
                    menu.content(
                        menu.item("Settings"),
                        menu.item("Copy path"),
                        menu.item("Open location"),
                    ),
                ),
                align="inline-end",
            ),
        ),
        input_group.root(
            input_group.input(placeholder="Enter search query"),
            input_group.addon(
                menu.root(
                    menu.trigger(
                        "Search In... ",
                        hi("ChevronDownIcon", class_name="size-3 ml-1 inline"),
                        class_name="!pr-1.5 text-xs",
                    ),
                    menu.content(
                        menu.item("Documentation"),
                        menu.item("Blog Posts"),
                        menu.item("Changelog"),
                    ),
                ),
                align="inline-end",
            ),
        ),
        class_name="grid w-full max-w-sm gap-4",
    )
```

# API Reference

## input_group.root

The main wrapper around inputs and addons.

```python
input_group.root(
    input_group.addon(hi("Search01Icon")),
    input_group.input(placeholder="Search..."),
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## input_group.addon

Displays icons, text, buttons, or other content alongside the input. Can contain multiple `input_group.button`s.

```python
input_group.addon(hi("Search01Icon"), align="inline-start")
```

| Prop         | Type                                                                     | Default          |
| ------------ | --------------------------------------------------------------------------| ---------------- |
| `align`      | `Literal["inline-start", "inline-end", "block-start", "block-end"]`      | `"inline-start"` |
| `class_name` | `str`                                                                     | `""`              |

Use `inline-start`/`inline-end` with `input_group.input`, and `block-start`/`block-end` with `input_group.textarea`.

## input_group.button

A `button` pre-styled for input group contexts. See the [Button](/docs/components/button) docs for the rest of `button`'s props.

```python
input_group.addon(
    input_group.button(hi("X01Icon"), aria_label="Clear"),
    align="inline-end",
)
```

| Prop         | Type                                                                          | Default   |
| ------------ | -------------------------------------------------------------------------------| --------- |
| `size`       | `Literal["xs", "icon-xs", "sm", "icon-sm"]`                                   | `"xs"`    |
| `variant`    | `Literal["default", "destructive", "outline", "secondary", "ghost", "link"]` | `"ghost"` |
| `class_name` | `str`                                                                          | `""`      |

## input_group.input

Drop-in replacement for `input()` inside an input group — pre-styled and tagged with the shared `data-slot="input-group-control"` used for group-wide focus states.

```python
input_group.input(placeholder="Search...")
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

Any other prop accepted by `input()` is passed straight through.

## input_group.textarea

Drop-in replacement for `textarea()` inside an input group — same `data-slot="input-group-control"` convention as `input_group.input`.

```python
input_group.textarea(placeholder="Leave a comment...")
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

Any other prop accepted by `textarea()` is passed straight through.
