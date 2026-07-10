---
title: "Dialog"
description: "A window overlaid on either the primary window or another dialog window, rendering the content underneath inert."
order: 8
---

--INTRO([Dialog, A window overlaid on either the primary window or another dialog window, rendering the content underneath inert.])--

--USAGE(dialog)--

--SOURCE(dialog)--

# Examples

## Custom Close Button

Replace the default close control with your own button. Apply `dialog.class_names.CLOSE_ICON` to it for correct top-right positioning.

**Props used:** `class_name` on the button passed to `dialog.close`.

--DEMO(dialog_close_button)--

## No Close Button

To omit the top-right close icon, simply don't render a `dialog.close(...)` for it — every other close mechanism (Escape, backdrop click, a footer button) still works.

**Props used:** none required — omit the icon `dialog.close(...)` call.

--DEMO(dialog_no_close_button)--

## Sticky Footer

Keep actions visible while the content scrolls, using `dialog.footer`.

**Props used:** none required beyond standard `dialog.footer` composition.

--DEMO(dialog_sticky_footer)--

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
