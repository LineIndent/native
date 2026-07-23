---
title: "Card"
description: "Displays a card with header, content, and footer."
order: 0
---

--INTRO([Card, Displays a card with header, content, and footer.])--

--USAGE(card)--

--SOURCE(card)--

# Examples

## Size

Use `size="sm"` for tighter spacing throughout the card.

**Props used:** `size` on `card.root`.

--DEMO(card_small)--

## Spacing

Beyond `size`, use the `--card-padding` and `--card-gap` CSS variables directly to control the card's inset and section spacing. `--card-padding` sets the padding inside the card (and each section's horizontal inset); `--card-gap` sets the space between header, content, and footer.

**Props used:** `class_name` (setting `--card-padding` and `--card-gap` inline) on `card.root`.

--DEMO(card_spacing)--

Use negative margins with `-mx-(--card-padding)` to let content go edge-to-edge while staying aligned with the card's inset. When edge-to-edge content sits above a footer, add `-mb-(--card-gap)` on `card.content` to remove the section gap.

--DEMO(card_edge_to_edge)--

## Image

Add an image before `card.header` to create a card with a cover image — corner radii adjust automatically for first/last-child images.

**Props used:** none required — place `rx.el.img(...)` as the first child of `card.root`.

--DEMO(card_image)--

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
