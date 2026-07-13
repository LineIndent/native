---
title: "Attachment"
description: "Displays a file or image attachment with media, metadata, upload state, and actions."
order: 0
---


## Attachment, Displays A File Or Image Attachment With Media, Metadata, Upload State, And Actions.


```python
from components.ui.attachment import Attachment
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
from typing import Literal

import reflex as rx
from reflex.components.component import ComponentNamespace

from ..ui.button import button
from ..core.core import cn

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


def attachment_root(
    *children,
    orientation: AttachmentOrientation = "horizontal",
    size: AttachmentSize = "default",
    state: AttachmentState = "done",
    class_name: str = "",
    **props,
) -> rx.Component:

    return rx.el.div(
        *children,
        data_slot="attachment",
        data_state=state,
        data_size=size,
        data_orientation=orientation,
        class_name=cn(
            ClassNames.ROOT_BASE,
            ClassNames.SIZES.get(size, ""),
            ClassNames.ORIENTATIONS.get(orientation, ""),
            class_name,
        ),
        **props,
    )


def attachment_media(
    *children,
    variant: AttachmentMediaVariant = "icon",
    class_name: str = "",
    **props,
) -> rx.Component:

    return rx.el.div(
        *children,
        data_slot="attachment-media",
        data_variant=variant,
        class_name=cn(
            ClassNames.MEDIA_BASE,
            ClassNames.MEDIA_VARIANTS.get(variant, ""),
            class_name,
        ),
        **props,
    )


def attachment_content(*children, class_name: str = "", **props) -> rx.Component:

    return rx.el.div(
        *children,
        data_slot="attachment-content",
        class_name=cn(ClassNames.CONTENT, class_name),
        **props,
    )


def attachment_title(*children, class_name: str = "", **props) -> rx.Component:

    return rx.el.span(
        *children,
        data_slot="attachment-title",
        class_name=cn(ClassNames.TITLE, class_name),
        **props,
    )


def attachment_description(*children, class_name: str = "", **props) -> rx.Component:

    return rx.el.span(
        *children,
        data_slot="attachment-description",
        class_name=cn(ClassNames.DESCRIPTION, class_name),
        **props,
    )


def attachment_actions(*children, class_name: str = "", **props) -> rx.Component:

    return rx.el.div(
        *children,
        data_slot="attachment-actions",
        class_name=cn(ClassNames.ACTIONS, class_name),
        **props,
    )


def attachment_action(*children, class_name: str = "", **props) -> rx.Component:
    props.setdefault("variant", "ghost")

    props.setdefault("size", "icon-xs")

    return button(
        *children,
        data_slot="attachment-action",
        class_name=cn(class_name),
        **props,
    )


def attachment_trigger(
    *children, link: bool = False, class_name: str = "", **props
) -> rx.Component:

    component_fn = rx.el.a if link else rx.el.button

    props.setdefault("data-slot", "attachment-trigger")
    props.setdefault("class_name", cn(ClassNames.TRIGGER, class_name))

    if not link:
        props.setdefault("type", "button")

    return component_fn(*children, **props)


def attachment_group(*children, class_name: str = "", **props) -> rx.Component:

    return rx.el.div(
        *children,
        data_slot="attachment-group",
        class_name=cn(ClassNames.GROUP, class_name),
        **props,
    )


class Attachment(ComponentNamespace):
    root = staticmethod(attachment_root)
    media = staticmethod(attachment_media)
    content = staticmethod(attachment_content)
    title = staticmethod(attachment_title)
    description = staticmethod(attachment_description)
    actions = staticmethod(attachment_actions)
    action = staticmethod(attachment_action)
    trigger = staticmethod(attachment_trigger)
    group = staticmethod(attachment_group)

    class_names = ClassNames


attachment = Attachment()
```

# Features

- Icon and image media through `attachment.media`
- Upload states: `idle`, `uploading`, `processing`, `error`, and `done` with built-in styling and a shimmer while in progress
- Three sizes and horizontal or vertical orientation
- A full-card `attachment.trigger` that opens a link or dialog while the actions stay independently clickable
- Scrollable, snapping `attachment.group` with an edge fade
- Customizable styling through the `class_name` prop on every part

# Examples

## Image

Set `variant="image"` on `attachment.media` and render an `rx.el.img()` inside it. Use `orientation="vertical"` to stack the media above the content.

```python
def attachment_image_demo():
    return rx.el.div(
        attachment.group(
            # rx.foreach(
            #     images,
            #     lambda image: attachment.root(
            #         attachment.trigger(
            #             link=True,
            #             href=image["src"],
            #             target="_blank",
            #             rel="noreferrer",
            #             aria_label=f"Open {image['name']}",
            #         ),
            #         attachment.media(
            #             rx.el.img(src=image["src"], alt=image["alt"]),
            #             variant="image",
            #         ),
            #         attachment.content(
            #             attachment.title(image["name"]),
            #             attachment.description(image["meta"]),
            #         ),
            #         attachment.actions(
            #             attachment.action(
            #                 hi("Cancel01Icon"),
            #                 aria_label=f"Remove {image['name']}",
            #             )
            #         ),
            #         orientation="vertical",
            #     ),
            # ),
            [
                attachment.root(
                    attachment.trigger(
                        link=True,
                        href=image["src"],
                        target="_blank",
                        rel="noreferrer",
                        aria_label=f"Open {image['name']}",
                    ),
                    attachment.media(
                        rx.el.img(src=image["src"], alt=image["alt"]),
                        variant="image",
                    ),
                    attachment.content(
                        attachment.title(image["name"]),
                        attachment.description(image["meta"]),
                    ),
                    attachment.actions(
                        attachment.action(
                            hi("Cancel01Icon"),
                            aria_label=f"Remove {image['name']}",
                        )
                    ),
                    orientation="vertical",
                )
                for image in images
            ],
            class_name="w-full",
        ),
        class_name="mx-auto w-full max-w-sm py-12",
    )
```

## States

Set `state` to reflect the upload lifecycle. `uploading` and `processing` shimmer the title, and `error` switches to a destructive treatment.

```python
def attachment_states_demo():
    return rx.el.div(
        attachment.root(
            attachment.media(hi("Clock01Icon")),
            attachment.content(
                attachment.title("selected-file.pdf"),
                attachment.description("Ready to upload"),
            ),
            attachment.actions(
                attachment.action(
                    hi("Cancel01Icon"), aria_label="Remove selected-file.pdf"
                )
            ),
            state="idle",
        ),
        attachment.root(
            attachment.media(spinner()),
            attachment.content(
                attachment.title(
                    "design-system.zip",
                    class_name="shimmer",
                ),
                attachment.description("Uploading · 64%"),
            ),
            attachment.actions(
                attachment.action(hi("Cancel01Icon"), aria_label="Cancel upload")
            ),
            state="uploading",
        ),
        attachment.root(
            attachment.media(hi("File02Icon")),
            attachment.content(
                attachment.title("market-research.pdf"),
                attachment.description("Processing document"),
            ),
            attachment.actions(
                attachment.action(
                    hi("Cancel01Icon"), aria_label="Remove market-research.pdf"
                )
            ),
            state="processing",
        ),
        attachment.root(
            attachment.media(hi("FileExclamationPointIcon")),
            attachment.content(
                attachment.title("financial-model.xlsx"),
                attachment.description("Upload failed. Try again."),
            ),
            attachment.actions(
                attachment.action(hi("RefreshIcon"), aria_label="Retry upload"),
                attachment.action(
                    hi("Cancel01Icon"), aria_label="Remove financial-model.xlsx"
                ),
            ),
            state="error",
        ),
        attachment.root(
            attachment.media(hi("Tick02Icon")),
            attachment.content(
                attachment.title("uploaded-report.pdf"),
                attachment.description("Uploaded · 1.8 MB"),
            ),
            attachment.actions(
                attachment.action(
                    hi("Cancel01Icon"), aria_label="Remove uploaded-report.pdf"
                )
            ),
            state="done",
        ),
        class_name="w-full mx-auto max-w-sm py-12 flex flex-col gap-y-4",
    )
```


## Sizes

Use `size` to switch between `default`, `sm`, and `xs`.

```python
def attachment_sizes_demo():
    return rx.el.div(
        attachment.root(
            attachment.media(hi("File02Icon")),
            attachment.content(
                attachment.title("Default attachment"),
                attachment.description("PDF · 2.4 MB"),
            ),
            size="default",
        ),
        attachment.root(
            attachment.media(hi("File02Icon")),
            attachment.content(
                attachment.title("Small attachment"),
                attachment.description("PDF · 2.4 MB"),
            ),
            size="sm",
        ),
        attachment.root(
            attachment.media(hi("File02Icon")),
            attachment.content(
                attachment.title("Extra small attachment"),
            ),
            size="xs",
        ),
        class_name="mx-auto w-full max-w-sm py-12 flex flex-col gap-y-4",
    )
```

## Group

Wrap attachments in `attachment.group` to lay them out in a horizontally scrollable, snapping row with an edge fade.

```python
def attachment_group_demo():
    return rx.el.div(
        attachment.group(
            # rx.foreach(
            #     items,
            #     lambda item: attachment.root(
            #         rx.cond(
            #             item["type"] == "image",
            #             attachment.media(
            #                 rx.el.img(src=item["src"], alt=item["name"]),
            #                 variant="image",
            #             ),
            #             attachment.media(hi("File02Icon")),
            #         ),
            #         attachment.content(
            #             attachment.title(item["name"]),
            #             attachment.description(item["meta"]),
            #         ),
            #         attachment.actions(
            #             attachment.action(
            #                 hi("Cancel01Icon"), aria_label=f"Remove {item['name']}"
            #             )
            #         ),
            #         class_name="w-64",
            #     ),
            # ),
            [
                attachment.root(
                    attachment.media(
                        rx.el.img(src=item["src"], alt=item["name"]),
                        variant="image",
                    )
                    if item["type"] == "image"
                    else attachment.media(hi("File02Icon")),
                    attachment.content(
                        attachment.title(item["name"]),
                        attachment.description(item["meta"]),
                    ),
                    attachment.actions(
                        attachment.action(
                            hi("Cancel01Icon"),
                            aria_label=f"Remove {item['name']}"
                        )
                    ),
                    class_name="w-64",
                )
                for item in items
            ],
            class_name="full",
        ),
        class_name="mx-auto w-full max-w-sm py-12",
    )
```

## Trigger

Add an `attachment.trigger` to make the whole card open a link or dialog. It fills the card behind the actions, so the actions stay clickable.

```python
def attachment_trigger_dialog_demo():
    return rx.el.div(
        dialog.root(
            attachment.root(
                attachment.media(hi("File01Icon")),
                attachment.content(
                    attachment.title("research-summary.pdf"),
                    attachment.description("Open preview dialog"),
                ),
                attachment.actions(
                    attachment.action(hi("Copy01Icon"), aria_label="Copy link"),
                    attachment.action(
                        hi("Cancel01Icon"), aria_label="Remove research-summary.pdf"
                    ),
                ),
                dialog.trigger(attachment.trigger(link=False)),
                class_name="w-full",
            ),
            dialog.popup(
                dialog.title("research-summary.pdf"),
                dialog.description(
                    "The attachment trigger fills the card and opens the dialog, "
                    "while the actions stay independently clickable above it."
                ),
                class_name="max-w-md rounded-2xl",
            ),
        ),
        class_name="mx-auto w-full max-w-sm py-12",
    )
```


# Accessibility

`attachment.action` renders a `Button`, and `attachment.trigger` renders either a real `rx.el.button()` or a `rx.el.a()` if the `link` prop is set to `True`. Follow the guidance below so both are operable and announced.

## Label icon-only actions

`attachment.action` is usually icon-only, so give each one an `aria-label` describing the action and its target.

```python
attachment.action(
    hi("Cancel01Icon"), aria_label="Remove market-research.pdf"
)
```

## Label the trigger

`attachment.trigger` overlays the entire attachment with a clickable surface.

Use `aria_label` to describe what activating the attachment does. This is required when the trigger has no visible text.

### Link trigger (opens a URL)

```python
attachment.trigger(
    link=True,
    href=url,
    target="_blank",
    rel="noreferrer",
    aria_label="Open workspace.png",
)
```

### Button trigger (interactive action)

```python
attachment.trigger(
    on_click=handle_open,
    aria_label="Open attachment preview",
)
```


The trigger sits behind the actions in the stacking order, so an `attachment.action` and the `attachment.trigger` never trap each other — both remain separately focusable and clickable.

## Keyboard scrolling

An `attachment.group` scrolls horizontally. When its attachments are interactive: a trigger or actions, keyboard users reach off-screen items by tabbing to them. For a row of presentational attachments, make the group itself focusable and scrollable by adding `tabIndex={0}`, `role="group"`, and an `aria-label`.

## Meaning beyond color

The `error` state uses a destructive color. Keep the failure reason in `attachment.description` so the state is not conveyed by color alone.

# API Reference

## attachment.root

The root attachment container.

| Prop          | Type                                                         | Default        | Description                                       |
| ------------- | ------------------------------------------------------------ | -------------- | ------------------------------------------------- |
| `state`       | `"idle" \| "uploading" \| "processing" \| "error" \| "done"` | `"done"`       | The upload state. Drives styling and the shimmer. |
| `size`        | `"default" \| "sm" \| "xs"`                                  | `"default"`    | The attachment size.                              |
| `orientation` | `"horizontal" \| "vertical"`                                 | `"horizontal"` | Lay the media beside or above the content.        |
| `class_name`   | `string`                                                     | -              | Additional classes to apply to the root element.  |

## attachment.media

The media slot for an icon or image preview.

| Prop        | Type                | Default  | Description                                    |
| ----------- | ------------------- | -------- | ---------------------------------------------- |
| `variant`   | `"icon" \| "image"` | `"icon"` | Whether the media holds an icon or an `<img>`. |
| `class_name` | `string`            | -        | Additional classes to apply to the media slot. |

## attachment.content

Wraps the title and description.

| Prop        | Type     | Default | Description                                      |
| ----------- | -------- | ------- | ------------------------------------------------ |
| `class_name` | `string` | -       | Additional classes to apply to the content slot. |

## attachment.title

The attachment name. Shimmers while the attachment is `uploading` or `processing`.

| Prop        | Type     | Default | Description                               |
| ----------- | -------- | ------- | ----------------------------------------- |
| `class_name` | `string` | -       | Additional classes to apply to the title. |

## attachment.description

Secondary metadata such as the file type, size, or upload status.

| Prop        | Type     | Default | Description                                     |
| ----------- | -------- | ------- | ----------------------------------------------- |
| `class_name` | `string` | -       | Additional classes to apply to the description. |

## attachment.actions

A container for one or more actions, aligned to the end of the attachment.

| Prop        | Type     | Default | Description                                 |
| ----------- | -------- | ------- | ------------------------------------------- |
| `class_name` | `string` | -       | Additional classes to apply to the actions. |

## attachment.action

An action button. Renders a [`Button`](/docs/components/button) and accepts all of its props.

| Prop       | Type                                  | Default     | Description                              |
| ---------- | ------------------------------------- | ----------- | ---------------------------------------- |
| `size`     | `Button["size"]`                      | `"icon-xs"` | The button size.                         |
| `class_name` | `string` | -       | Additional classes to apply to the actions. |

## attachment.trigger

A full-card overlay that activates the attachment. Renders a `rx.el.button` by default or a `rx.el.a` when `link=True`.

| Prop         | Type                  | Default | Description                                                                   |
| ------------ | --------------------- | ------- | ----------------------------------------------------------------------------- |
| `link`       | `bool`         | `False`  | If set, renders an anchor (`rx.el.a`) instead of a button.                        |
| `aria_label` | `str \| None`         | `None`  | Accessibility label for screen readers. Required when no visible text exists. |
| `class_name` | `str`                 | `""`    | Additional CSS classes applied to the trigger.                                |


## attachment.group

Lays out attachments in a horizontally scrollable, snapping row.

| Prop        | Type     | Default | Description                               |
| ----------- | -------- | ------- | ----------------------------------------- |
| `class_name` | `string` | -       | Additional classes to apply to the group. |
