---
title: "Accordion"
description: "A vertically stacked set of interactive headings that each reveal a section of content."
order: 0
---

--INTRO([Accordion, A vertically stacked set of interactive headings that each reveal a section of content.])--

--USAGE(accordion)--

--SOURCE(accordion)--

# Examples

## Basic

Built on native `<details>`/`<summary>` — expand/collapse, keyboard support, and the chevron rotation all come from the browser and `group-open/accordion-item:rotate-180`, no JS required.

**Props used:** `name` on `accordion.item` (groups items so only one stays open at a time, matching native `<details name="...">` behavior).

--DEMO(accordion_basic)--

# API Reference

## accordion.root

```python
accordion.root(
    accordion.item(...),
    accordion.item(...),
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## accordion.item

Renders a native `<details>`. Give matching items the same `name` to make them mutually exclusive (native `<details name="...">` grouping — opening one closes the others in the group automatically).

```python
accordion.item(
    accordion.trigger("Is it accessible?"),
    accordion.panel("Yes, built on native semantics."),
    name="faq",
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `name`       | `str` |         |
| `class_name` | `str` | `""`    |

## accordion.trigger

Renders a `<summary>` with a chevron icon appended automatically — no need to add one yourself.

```python
accordion.trigger("Is it accessible?")
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## accordion.panel

```python
accordion.panel("Yes. It adheres to the WAI-ARIA design pattern.")
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |
