---
title: "Frame"
description: "Displays related content in a structured frame."
order: 0
---

--INTRO([Frame, Displays related content in a structured frame.])--

--USAGE(frame)--

--SOURCE(frame)--

# Examples

## Basic Panels

A basic frame with a header and two panels.

**Props used:** none required beyond default `frame.root` composition.

--DEMO(frame_basic)--

## Stacked Panels

Set `stacked=True` to merge panel borders into one continuous block.

**Props used:** `stacked` on `frame.root`.

--DEMO(frame_stacked)--

## Dense Panels

Set `dense=True` for minimal frame padding, edge-to-edge.

**Props used:** `dense` on `frame.root`.

--DEMO(frame_dense)--

## Outer Border

Set `variant="ghost"` to remove the frame's outer border.

**Props used:** `variant` on `frame.root`.

--DEMO(frame_no_border)--

# API Reference

## frame.root

```python
frame.root(
    frame.panel(
        frame.header(frame.title("Overview")),
        "Panel content",
    ),
    variant="default",
    spacing="default",
)
```

| Prop         | Type                                          | Default     | Description                                                                          |
| ------------ | ----------------------------------------------- | ----------- | -------------------------------------------------------------------------------------- |
| `variant`    | `Literal["default", "inverse", "ghost"]`       | `"default"` | Controls the visual style of the frame container.                                     |
| `spacing`    | `Literal["xs", "sm", "default", "lg"]`         | `"default"` | Controls internal padding of panels, headers, and footers via CSS variables.          |
| `stacked`    | `bool`                                          | `False`     | Removes gaps and merges panel borders so they appear as one continuous block.         |
| `dense`      | `bool`                                          | `False`     | Removes all padding/gaps and pulls panels edge-to-edge with negative margins.          |
| `class_name` | `str`                                            | `""`         | Additional classes merged onto the root wrapper.                                       |

## frame.panel

```python
frame.panel("Panel content")
```

| Prop         | Type  | Default | Description                                                          |
| ------------ | ----- | ------- | ------------------------------------------------------------------- |
| `class_name` | `str` | `""`     | Additional classes merged onto the panel — overrides default bg/border/padding. |

## frame.header

```python
frame.header(frame.title("Overview"))
```

| Prop         | Type  | Default | Description                                    |
| ------------ | ----- | ------- | ----------------------------------------------- |
| `class_name` | `str` | `""`     | Additional classes merged onto the header.       |

## frame.title

```python
frame.title("Overview")
```

| Prop         | Type  | Default | Description                                   |
| ------------ | ----- | ------- | ----------------------------------------------- |
| `class_name` | `str` | `""`     | Additional classes merged onto the title.        |

## frame.description

```python
frame.description("A summary of recent activity.")
```

| Prop         | Type  | Default | Description                                        |
| ------------ | ----- | ------- | ----------------------------------------------------- |
| `class_name` | `str` | `""`     | Additional classes merged onto the description.        |

## frame.footer

```python
frame.footer(button("View all", variant="ghost", size="sm"))
```

| Prop         | Type  | Default | Description                                    |
| ------------ | ----- | ------- | ----------------------------------------------- |
| `class_name` | `str` | `""`     | Additional classes merged onto the footer.        |
