---
title: "Collapsible"
description: "An interactive component which expands/collapses a panel."
order: 0
---

--INTRO([Collapsible, An interactive component which expands/collapses a panel. ])--

--USAGE(collapsible)--

--SOURCE(collapsible)--

# Examples

## Basic

Built on native `<details>`/`<summary>`, expand/collapse and keyboard support come from the browser, no JS required. The chevron rotation and open-state highlight use a structural selector (`[details[open]>&]`) rather than Tailwind's `group-open:`, since `group-open:` matches _any_ open ancestor rather than the nearest one — harmless here, but matters once collapsibles nest (see below).

**Props used:** `default_open` on `collapsible.root` (starts the panel expanded).

--DEMO(collapsible_basic)--

## Nested

Collapsibles nest freely, each `<details>` is fully independent, so there's no coordination needed between levels (multiple folders can be open at once). The one thing that _does_ need care when nesting: chevron/highlight styling must use the structural `[details[open]>...]` selector, not `group-open:`. `group-open:` would match an open ancestor several folders up, which makes every icon inside it look rotated even if that specific folder is still closed.

**Props used:** none beyond `collapsible.root` / `collapsible.trigger` / `collapsible.panel` — the tree is just `folder_item` calling itself recursively.

--DEMO(collapsible_nested)--

# API Reference

## collapsible.root

Renders a native `<details>` element. `default_open` sets the initial `open` attribute on first render. Since it's a real `<details>`, controlled usage also works without any extra plumbing — pass `open=State.is_open` and `on_toggle=State.handle_toggle` to drive or react to it from Reflex state, same as any other native attribute/event.

```python
collapsible.root(
    collapsible.trigger(...),
    collapsible.panel(...),
    default_open=False,
)
```

| Prop           | Type           | Default |
| -------------- | -------------- | ------- |
| `default_open` | `bool`         | `False` |
| `open`         | `bool`         | `None`  |
| `on_toggle`    | `EventHandler` | `None`  |
| `class_name`   | `str`          | `""`    |

## collapsible.trigger

Renders a `<summary>`. Unlike a typical accordion trigger, it doesn't append a chevron for you — pass your own icon (and any other trigger content) as children, and drive its rotation off the parent's open state yourself.

```python
collapsible.trigger(
    rx.el.p("How do I update my billing information?"),
    hi("ArrowDown01Icon", class_name="[details[open]>summary_&]:rotate-180"),
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## collapsible.panel

```python
collapsible.panel(
    "You can update your card details directly inside your account settings dashboard.",
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## Styling based on open state

`collapsible.root` renders the actual `<details>`, so any open-state styling on the trigger or its children should key off that element directly rather than a Tailwind `group`:

| Target                                      | Selector                               |
| ------------------------------------------- | -------------------------------------- |
| The trigger itself (e.g. a highlight)       | `[details[open]>&]:bg-muted/50`        |
| Something inside the trigger (e.g. an icon) | `[details[open]>summary_&]:rotate-180` |

Both are scoped to _that_ collapsible's own `<details>` — never a distant open ancestor — which is what makes them safe to reuse inside recursively nested collapsibles like the file-tree example above.
