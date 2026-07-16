---
title: Bubble
description: Displays conversational content in a message bubble. Supports variants, alignment, grouping, reactions, and collapsible content.
order: 0 
---


## Bubble, Displays Conversational Content In A Message Bubble. Supports Variants, Alignment, Grouping, Reactions, And Collapsible Content.


```python
from components.ui.bubble import Bubble
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
```

Displays conversational content in a message bubble. Supports variants, alignment, grouping, reactions, and collapsible content.

The `Bubble` component displays framed conversational content. Use it for chat text, short structured output, quoted replies, suggestions, and reactions.

For full-featured chat interfaces, use the [`Message`](/docs/components/message) component. `Bubble` is intentionally scoped to the bubble surface. Place avatars, names, timestamps, metadata, and message-level actions in [`Message`](/docs/components/message).


# Features

- Seven visual variants, from a strong primary bubble to unframed ghost content
- Start and end alignment for sender and receiver bubbles
- Reactions that anchor to the bubble edge with configurable side and alignment
- Bubbles size to their content, up to 80% of the container width
- Polymorphic content via `render` for link and button bubbles
- Customizable styling through the `class_name` prop on every part

# Examples

## Variants

Use `variant` to change the visual treatment of the bubble.

**Props used:** `variant` on `bubble.root`.

```python
def bubble_with_variants():
    return rx.el.div(
        bubble.root(
            bubble.content("This is the default primary bubble."),
            variant="default",
        ),
        bubble.root(
            bubble.content("This is the secondary variant."),
            variant="secondary",
            align="end",
        ),
        bubble.root(
            bubble.content(
                "This one is muted. It uses a lower emphasis color for the chat bubble."
            ),
            bubble.reactions(
                rx.el.span("👍"),
                role="img",
                aria_label="Reaction: thumbs up",
            ),
            variant="muted",
        ),
        bubble.root(
            bubble.content(
                "This one is tinted. The tint is a softer color derived from the primary color."
            ),
            variant="tinted",
            align="end",
        ),
        bubble.root(
            bubble.content("We can also use an outlined variant."),
            variant="outline",
        ),
        bubble.root(
            bubble.content("Or a destructive variant with a reaction."),
            bubble.reactions(
                rx.el.span("🔥"),
                role="img",
                aria_label="Reaction: fire",
            ),
            variant="destructive",
            align="end",
        ),
        bubble.root(
            bubble.content(
                rx.html(
                    """
                    Ghost bubbles work for assistant text, **markdown**, and other content that should not be framed.

                    This is perfect for assistant messages that should not have a frame and can take the full width of the container. You can also render `code` in it.

                    Ghost bubbles are full width and can take the full width of the container.
                    """,
                    class_name="docs-prose"
                ),
            ),
            variant="ghost",
        ),
        class_name="flex w-full max-w-sm flex-col gap-12 py-12",
    )
```


| Variant       | Description                                            |
| ------------- | ------------------------------------------------------ |
| `default`     | A strong primary bubble, usually for the current user. |
| `secondary`   | The standard neutral bubble for conversation content.  |
| `muted`       | A lower-emphasis bubble for quiet supporting content.  |
| `tinted`      | A subtle primary-tinted bubble.                        |
| `outline`     | A bordered bubble for secondary or rich content.       |
| `ghost`       | Unframed content for assistant text or rich content.   |
| `destructive` | A destructive bubble for error or failed actions.      |

A bubble sizes to its content, up to 80% of the container width. The `ghost` variant removes the max-width so assistant text and rich content can span the full row.

## Alignment

Use `align` on `bubble.root` to align the bubble to the start or end of the conversation.

**Props used:** `align` on `bubble.root`.

```python
def bubble_alignment_demo():
    return rx.el.div(
        bubble.root(
            bubble.content(
                "This bubble is aligned to the start. This is the default alignment."
            ),
            variant="muted",
            align="start",
        ),
        bubble.root(
            bubble.content(
                "This bubble is aligned to the end. Use this for user messages."
            ),
            align="end",
        ),
        class_name="flex w-full max-w-sm flex-col gap-8 py-12",
    )
```

| align   | Description                                        |
| ------- | -------------------------------------------------- |
| `start` | Align the bubble to the start of the conversation. |
| `end`   | Align the bubble to the end of the conversation.   |

**Note:** When building chat interfaces, you probably want to use alignment on the `Message` component itself, not the `Bubble` component. You can use the `role` prop on the `message.root` component to automatically align the bubble to the start or end of the conversation.

## Bubble Group

Use `bubble.group` to group consecutive bubbles from the same sender. Note the `align` prop should be set on the `bubble.root` component itself, not the `bubble.group` component.

```composition
bubble.group
├── bubble.root
│   └── bubble.content
└── bubble.root
    └── bubble.content
```

**Props used:** `align` on `bubble.root` (set per-bubble, not on `bubble.group`).

```python
def bubble_group_demo():
    return rx.el.div(
        bubble.root(
            bubble.content("Can you tell me what's the issue?"),
            variant="muted",
        ),
        bubble.group(
            bubble.root(
                bubble.content("You tell me!"),
                align="end",
            ),
            bubble.root(
                bubble.content("It worked yesterday. You broke it!"),
                align="end",
            ),
            bubble.root(
                bubble.content("Find the bug and fix it."),
                bubble.reactions(
                    rx.el.span("👀"),
                    aria_label="Reactions: eyes",
                    align="start",
                ),
                align="end",
            ),
        ),
        bubble.root(
            bubble.content(
                "Want me to diff yesterday's you against today's you? "
                "It's a bit embarrassing."
            ),
            variant="muted",
        ),
        class_name="flex w-full max-w-sm flex-col gap-8 py-12",
    )
```

## Links and Buttons

You can turn a bubble into a link or button by using the passing the interactive elements directly into the `bubble.content` slot. The `bubble.content` accepts `*children` so simply placing a button or link will render that component. 

**Props used:** none required — pass a `button`/`rx.el.a` as a child of `bubble.content`.

```python
def bubble_link_button_demo():
    return rx.el.div(
        bubble.root(
            bubble.content("How can I help you today?"),
            variant="muted",
        ),
        bubble.group(
            bubble.root(
                bubble.content(
                    rx.el.button(
                        "I forgot my password",
                        on_click=rx.toast("You clicked forgot password"),
                        class_name="w-full text-left",
                    )
                ),
                variant="tinted",
                align="end",
            ),
            bubble.root(
                bubble.content(
                    rx.el.button(
                        "I need help with my subscription",
                        on_click=rx.toast("You clicked help with subscription"),
                        class_name="w-full text-left",
                    )
                ),
                variant="tinted",
                align="end",
            ),
            bubble.root(
                bubble.content(
                    rx.el.button(
                        "Something else. Talk to a human.",
                        on_click=rx.toast(
                            "You clicked something else. Talk to a human."
                        ),
                        class_name="w-full text-left",
                    )
                ),
                variant="tinted",
                align="end",
            ),
        ),
        class_name="flex w-full max-w-sm flex-col gap-8 py-12",
    )
```

## Reactions

Use `bubble.reactions` for bubble reactions. You can use it to display reactions or quick action buttons. Use `side` and `align` to position the row — `side="top"` anchors it to the upper edge. Reactions overlap the bubble edge, so leave vertical space between rows — the examples below use a larger `gap` for this reason.

**Props used:** `side`, `align` on `bubble.reactions`.

```python
def bubble_reactions_demo():
    return rx.el.div(
        bubble.root(
            bubble.content("I don't need tests, I know my code works."),
            bubble.reactions(
                rx.el.span("👍"),
                rx.el.span("😮"),
                align="start",
                role="img",
                aria_label="Reactions: thumbs up, surprised",
            ),
            variant="muted",
            align="end",
        ),
        bubble.root(
            bubble.content(
                "Bold. Fine I'll add some tests. I'll let you know when they're done."
            ),
            bubble.reactions(
                rx.el.span("👀"),
                rx.el.span("🚀"),
                rx.el.span("+2"),
                role="img",
                aria_label="Reactions: eyes, rocket, and 2 more",
            ),
            variant="muted",
        ),
        bubble.root(
            bubble.content(
                "Tests passed on the first try. All 142 of them. Looking good!"
            ),
            bubble.reactions(
                rx.el.span("🎉"),
                rx.el.span("👏"),
                side="top",
                align="start",
                role="img",
                aria_label="Reactions: party popper, clapping hands",
            ),
            variant="default",
            align="end",
        ),
        bubble.root(
            bubble.content("Are you sure I can run this command?"),
            bubble.reactions(
                rx.el.button(
                    "Yes, run it",
                    on_click=rx.toast.success("You clicked yes, running command..."),
                    class_name="px-2 py-0.5 text-xs hover:bg-accent rounded-md",
                ),
            ),
            variant="destructive",
        ),
        class_name="flex w-full max-w-sm flex-col gap-12 py-12",
    )
```

# Accessibility

`bubble.root` renders the presentational message surface. Keep conversation-level semantics on the surrounding container and follow the guidelines below.

## Labeling Reactions

Reactions render as a row of emoji. A screen reader reads each glyph with no context, and counters like `+8` are announced as "plus eight". Group the row as a single image with a descriptive `aria_label` so it announces once. `role="img"` also hides the individual emoji from assistive tech, so no `aria_hidden` is needed.

```python
bubble.reactions(
    rx.el.span("👍"),
    rx.el.span("🔥"),
    rx.el.span("+8"),
    role="img",
    aria_label="Reactions: thumbs up, fire, and 8 more"
)
```

When reactions are interactive, render buttons instead and give icon-only buttons an `aria_label`.

```python
bubble.reactions(
    button(
        ...,
        aria_label="Thumbs up",
        variant="secondary",
        size="sm"
    )
)
```

## Interactive Bubbles

When a bubble is clickable, render it as a real `<button>` or `<a>`. `bubble.-*` content accept `*children` so simply passing in the interactive component will get rendered. `bubble.content` ships a visible focus ring for interactive elements, and the accessible name comes from the bubble text. No extra label is needed.

```python
bubble.root(
    bubble.content(
        "I forgot my password",
        rx.el.button(type="button", on_click=on_reply)
    ),
    variant="muted",
    align="end"
)
```

## Meaning Beyond Color

Bubble variants signal role and tone with color. Pair them with text, alignment, or icons so meaning is not conveyed by color alone. For a `destructive` bubble, keep the error context in the message text rather than relying on the color treatment.

# API Reference

## bubble.root

The root bubble wrapper.

| Prop        | Type                                                                                       | Default     | Description                                      |
| ----------- | ------------------------------------------------------------------------------------------ | ----------- | ------------------------------------------------ |
| `variant`   | `Literal["default", "secondary", "muted", "tinted", "outline", "ghost", "destructive"]` | `"default"` | The bubble visual treatment.                     |
| `align`     | `Literal["start", "end"]`                                                                         | `"start"`   | The inline alignment of the bubble.              |
| `class_name` | `str`                                                                                   | -           | Additional classes to apply to the root element. |

## bubble.content

The bubble content wrapper.

| Prop        | Type                       | Default | Description                                               |
| ----------- | -------------------------- | ------- | --------------------------------------------------------- |
| `*children`    | `*rx.Component` | -       | Render the content as a different element such as a link. |
| `class_name` | `str`                   | -       | Additional classes to apply to the content element.       |

## bubble.reactions

Displays overlapped reactions for a bubble.

| Prop        | Type                | Default    | Description                                      |
| ----------- | ------------------- | ---------- | ------------------------------------------------ |
| `side`      | `Literal["top", "bottom"]` | `"bottom"` | The side of the bubble to anchor the reactions.  |
| `align`     | `Literal["start", "end"]`  | `"end"`    | The inline alignment of the reactions.           |
| `class_name` | `str`            | -          | Additional classes to apply to the reaction row. |

## bubble.group

Groups consecutive bubbles from the same sender.

| Prop        | Type     | Default | Description                                    |
| ----------- | -------- | ------- | ---------------------------------------------- |
| `class_name` | `str` | -       | Additional classes to apply to the group root. |
