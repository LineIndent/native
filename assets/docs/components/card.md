---
title: "Card"
description: "Displays a card with header, content, and footer."
order: 0
---


## Card, Displays A Card With Header, Content, And Footer.


```python
from components.ui.card import Card
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
from reflex.components.component import ComponentNamespace
from reflex.vars.base import Var
from reflex_components_core.el import Div

from ..core.core import CoreComponent


class ClassNames:
    ROOT = (
        "group/card flex flex-col gap-(--card-gap) overflow-hidden rounded-xl bg-card "
        "py-(--card-padding) text-sm text-card-foreground ring-1 ring-foreground/10 "
        "has-data-[slot=card-footer]:pb-0 "
        "has-[>img:first-child]:pt-0 "
        "*:[img:first-child]:rounded-t-xl *:[img:last-child]:rounded-b-xl"
    )

    HEADER = (
        "group/card-header @container/card-header grid auto-rows-min items-start gap-1 "
        "rounded-t-xl px-(--card-padding) "
        "has-data-[slot=card-action]:grid-cols-[1fr_auto] "
        "has-data-[slot=card-description]:grid-rows-[auto_auto] "
        "[.border-b]:pb-(--card-padding)"
    )

    TITLE = (
        "cn-font-heading text-base leading-snug font-medium "
        "group-data-[size=sm]/card:text-sm"
    )

    DESCRIPTION = "text-sm text-muted-foreground"

    ACTION = "col-start-2 row-span-2 row-start-1 self-start justify-self-end"

    CONTENT = "px-(--card-padding)"

    FOOTER = (
        "flex items-center rounded-b-xl border-t border-input "
        "bg-muted/50 p-(--card-padding)"
    )


class CardRoot(Div, CoreComponent):
    size: Var[str]

    @classmethod
    def create(cls, *children, **props):
        props["data-slot"] = "card"
        if "size" in props:
            props["data-size"] = props.pop("size")
        cls.set_class_name(ClassNames.ROOT, props)
        return super().create(*children, **props)


class CardHeader(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props):
        props["data-slot"] = "card-header"
        cls.set_class_name(ClassNames.HEADER, props)
        return super().create(*children, **props)


class CardTitle(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props):
        props["data-slot"] = "card-title"
        cls.set_class_name(ClassNames.TITLE, props)
        return super().create(*children, **props)


class CardDescription(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props):
        props["data-slot"] = "card-description"
        cls.set_class_name(ClassNames.DESCRIPTION, props)
        return super().create(*children, **props)


class CardAction(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props):
        props["data-slot"] = "card-action"
        cls.set_class_name(ClassNames.ACTION, props)
        return super().create(*children, **props)


class CardContent(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props):
        props["data-slot"] = "card-content"
        cls.set_class_name(ClassNames.CONTENT, props)
        return super().create(*children, **props)


class CardFooter(Div, CoreComponent):
    @classmethod
    def create(cls, *children, **props):
        props["data-slot"] = "card-footer"
        cls.set_class_name(ClassNames.FOOTER, props)
        return super().create(*children, **props)


class Card(ComponentNamespace):
    root = staticmethod(CardRoot.create)
    header = staticmethod(CardHeader.create)
    title = staticmethod(CardTitle.create)
    description = staticmethod(CardDescription.create)
    action = staticmethod(CardAction.create)
    content = staticmethod(CardContent.create)
    footer = staticmethod(CardFooter.create)
    class_names = ClassNames


card = Card()
```

# Examples

## Size

Use `size="sm"` for tighter spacing throughout the card.

**Props used:** `size` on `card.root`.

```python
def card_small() -> rx.Component:
    feature_name = "Scheduled reports"

    return card.root(
        card.header(
            card.title(feature_name),
            card.description("Weekly snapshots. No more manual exports."),
        ),
        card.content(
            rx.el.ul(
                rx.el.li(
                    hi(
                        "ArrowRight01Icon",
                        class_name="mt-0.5 size-4 shrink-0 text-muted-foreground",
                    ),
                    rx.el.span("Choose a schedule (daily, or weekly)."),
                    class_name="flex gap-2",
                ),
                rx.el.li(
                    hi(
                        "ArrowRight01Icon",
                        class_name="mt-0.5 size-4 shrink-0 text-muted-foreground",
                    ),
                    rx.el.span("Send to channels or specific teammates."),
                    class_name="flex gap-2",
                ),
                rx.el.li(
                    hi(
                        "ArrowRight01Icon",
                        class_name="mt-0.5 size-4 shrink-0 text-muted-foreground",
                    ),
                    rx.el.span("Include charts, tables, and key metrics."),
                    class_name="flex gap-2",
                ),
                class_name="grid gap-2 py-2 text-sm",
            )
        ),
        card.footer(
            button(
                "Set up scheduled reports",
                size="sm",
                class_name="w-full",
            ),
            button(
                "See what's new",
                variant="outline",
                size="sm",
                class_name="w-full",
            ),
            class_name="flex-col gap-2",
        ),
        size="sm",
        class_name="mx-auto w-full max-w-xs my-10",
    )
```

## Spacing

Beyond `size`, use the `--card-padding` and `--card-gap` CSS variables directly to control the card's inset and section spacing. `--card-padding` sets the padding inside the card (and each section's horizontal inset); `--card-gap` sets the space between header, content, and footer.

**Props used:** `class_name` (setting `--card-padding` and `--card-gap` inline) on `card.root`.

```python
def card_spacing() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            *[
                button(
                    item["label"],
                    variant="outline",
                    size="sm",
                    class_name=rx.cond(
                        selected_card_spacing.value == item["value"], "!bg-muted", ""
                    ),
                    on_click=selected_card_spacing.set_value(item["value"]),
                )
                for item in spacing_options
            ],
            class_name="flex gap-1 justify-start items-center w-full",
        ),
        card.root(
            card.header(
                card.title("Login to your account"),
                card.description("Enter your email below to login to your account"),
                card.action(
                    button("Sign Up", variant="link"),
                ),
            ),
            card.content(
                rx.el.form(
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Email",
                                html_for="email-spacing",
                                class_name="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
                            ),
                            rx.el.input(
                                id="email-spacing",
                                type="email",
                                placeholder="m@example.com",
                                required=True,
                                class_name="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-xs transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium text-foreground placeholder:text-muted-foreground focus-visible:outline-hidden focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
                            ),
                            class_name="grid gap-2",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Password",
                                    html_for="password-spacing",
                                    class_name="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
                                ),
                                rx.el.a(
                                    "Forgot your password?",
                                    href="#",
                                    class_name="ml-auto inline-block text-sm underline-offset-4 hover:underline",
                                ),
                                class_name="flex items-center",
                            ),
                            rx.el.input(
                                id="password-spacing",
                                type="password",
                                required=True,
                                class_name="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-xs transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium text-foreground placeholder:text-muted-foreground focus-visible:outline-hidden focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
                            ),
                            class_name="grid gap-2",
                        ),
                        class_name="flex flex-col gap-6",
                    )
                )
            ),
            card.footer(
                button("Login", type="submit", class_name="w-full"),
                button("Login with Google", variant="outline", class_name="w-full"),
                class_name="flex-col gap-2",
            ),
            class_name=(
                f"[--card-padding:--spacing({selected_card_spacing.value})] "
                f"[--card-gap:--spacing({selected_card_spacing.value})]"
            ),
        ),
        class_name="mx-auto grid w-full max-w-sm gap-4 my-10",
    )
```

Use negative margins with `-mx-(--card-padding)` to let content go edge-to-edge while staying aligned with the card's inset. When edge-to-edge content sits above a footer, add `-mb-(--card-gap)` on `card.content` to remove the section gap.

```python
def card_edge_to_edge() -> rx.Component:
    return card.root(
        card.header(
            card.title("Terms of Service"),
            card.description("Review the terms before accepting the agreement."),
        ),
        card.content(
            rx.el.div(
                rx.el.p(
                    "These terms govern your use of the workspace, including access to shared documents, project files, and collaboration tools."
                ),
                rx.el.p(
                    "You are responsible for the content you upload and for ensuring that your team has the appropriate permissions to view or edit it."
                ),
                rx.el.p(
                    "We may update features or limits as the service evolves. When those changes materially affect your workflow, we will notify your workspace administrators."
                ),
                rx.el.p(
                    "By continuing, you agree to keep your account credentials secure and to follow your organization's acceptable use policies."
                ),
                class_name="-mx-(--card-padding) max-h-48 space-y-4 overflow-y-scroll border-input border-t bg-muted/50 px-(--card-padding) py-4 text-sm leading-relaxed",
            ),
            class_name="-mb-(--card-gap)",
        ),
        card.footer(
            button("Decline", variant="outline"),
            button("Accept"),
            class_name="justify-end gap-2",
        ),
        class_name="mx-auto w-full max-w-sm",
    )
```

## Image

Add an image before `card.header` to create a card with a cover image — corner radii adjust automatically for first/last-child images.

**Props used:** none required — place `rx.el.img(...)` as the first child of `card.root`.

```python
def card_image() -> rx.Component:
    return card.root(
        rx.el.div(
            class_name="absolute inset-0 z-30 aspect-video bg-black/35",
        ),
        rx.el.img(
            src="https://avatar.vercel.sh/shadcn1",
            alt="Event cover",
            class_name="relative z-20 aspect-video w-full object-cover brightness-60 grayscale dark:brightness-40",
        ),
        card.header(
            card.action(
                badge("Featured", variant="secondary"),
            ),
            card.title("Design systems meetup"),
            card.description(
                "A practical talk on component APIs, accessibility, and shipping faster."
            ),
        ),
        card.footer(
            button("View Event", class_name="w-full"),
        ),
        class_name="relative mx-auto w-full max-w-sm pt-0",
    )
```

# API Reference

## card.root

```python
card.root(
    card.header(card.title("Team members")),
    card.content("..."),
    size="sm",
)
```

| Prop         | Type                       | Default     |
| ------------ | -------------------------- | ----------- |
| `size`       | `Literal["default", "sm"]` | `"default"` |
| `class_name` | `str`                      | `""`        |

## card.header

For a title, description, and optional action.

```python
card.header(
    card.title("Team members"),
    card.description("Manage who has access."),
    card.action(button("Invite", size="sm")),
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## card.title

```python
card.title("Team members")
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## card.description

```python
card.description("Manage who has access to this project.")
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## card.action

Places content in the top-right of the header (a button, badge, etc.).

```python
card.action(button("Invite", size="sm"))
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## card.content

```python
card.content("Main card body content.")
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## card.footer

```python
card.footer(button("Cancel", variant="ghost"), button("Save"))
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |
