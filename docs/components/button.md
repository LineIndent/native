---
title: "Button"
description: "Displays a button or a component that looks like a button."
order: 3
---

--INTRO([Button, Displays a button or a component that looks like a button.])--

--USAGE(button)--

--SOURCE(button)--

# Examples

## Sizes

Use the `size` prop to change the button's size.

**Props used:** `size` on `button`.

--DEMO(button_size)--

## Default

**Props used:** none required — `variant="default"` is the default.

--DEMO(button_default)--

## Secondary

**Props used:** `variant` on `button`.

--DEMO(button_secondary)--

## Outline

**Props used:** `variant` on `button`.

--DEMO(button_outline)--

## Ghost

**Props used:** `variant` on `button`.

--DEMO(button_ghost)--

## Link

**Props used:** `variant` on `button`.

--DEMO(button_link)--

## Destructive

**Props used:** `variant` on `button`.

--DEMO(button_destructive)--

## Icon

**Props used:** `size="icon"` on `button`.

--DEMO(button_icon)--

## With Icon

Add `data-icon="inline-start"` or `data-icon="inline-end"` to the icon child for correct spacing.

**Props used:** `data_icon` on the icon child.

--DEMO(button_with_icon)--

## Rounded

**Props used:** `class_name="rounded-full"` on `button`.

--DEMO(button_rounded)--

## Spinner

Render a `spinner()` inside the button for a loading state, with the same `data-icon` positioning convention as icons.

**Props used:** `data_icon` on the spinner child.

--DEMO(button_loading)--

## As Link

Use `button_variants(...)` to generate the button's classes as a plain `Var`, applied to a real `rx.el.a`. Don't wrap an `<a>` inside `button(...)` — the underlying Base UI `Button` always sets `role="button"`, which overrides the link's semantic role.

**Props used:** `variant`, `size` args on `button_variants(...)`.

--DEMO(button_render)--

# API Reference

## button

```python
button("Click me", variant="outline", size="sm")
```

| Prop      | Type                                                                                      | Default     |
| --------- | ------------------------------------------------------------------------------------------ | ----------- |
| `variant` | `Literal["default", "destructive", "outline", "secondary", "ghost", "link"]`              | `"default"` |
| `size`    | `Literal["default", "xs", "sm", "lg", "icon", "icon-xs", "icon-sm", "icon-lg"]`            | `"default"` |
| `class_name` | `str`                                                                                    | `""`        |

Any other prop accepted by the underlying Base UI `Button` is also passed straight through.

## button_variants

Returns the same classes `button(...)` would apply, as a plain `Var[str]` — for styling a non-button element (like a link) to look like a button, without wrapping it in an actual `<button>`.

```python
rx.el.a(
    "Go to docs",
    href="/docs",
    class_name=button_variants("outline", "sm"),
)
```

| Arg       | Type                                                                            | Default     |
| --------- | --------------------------------------------------------------------------------- | ----------- |
| `variant` | `Literal["default", "destructive", "outline", "secondary", "ghost", "link"]`     | `"default"` |
| `size`    | `Literal["default", "xs", "sm", "lg", "icon", "icon-xs", "icon-sm", "icon-lg"]`   | `"default"` |
