---
title: "Avatar"
description: "An image element with a fallback for representing the user."
order: 1
---

--INTRO([Avatar, An easily stylable avatar component that displays a user's profile picture, initials, or fallback icon.])--

--USAGE(avatar)--

--SOURCE(avatar)--

# Examples

## Basic

A basic avatar with an image and a fallback. The fallback is shown automatically if the image fails to load.

**Props used:** `src` on `avatar.image`; no props required on `avatar.fallback`.

--DEMO(avatar_basic)--

## Badge

Use `avatar.badge` to add a badge to the avatar. It's positioned at the bottom right by default.

**Props used:** none required — pass content as children.

--DEMO(avatar_with_badge)--

Use `class_name` to customize the badge's colors, size, etc.

```python
avatar.badge(class_name="bg-green-600 dark:bg-green-800")
```

## Badge with Icon

You can also render an icon inside `avatar.badge`.

**Props used:** none required — pass an icon as a child.

--DEMO(avatar_badge_icon)--

## Avatar Group

Use `avatar.group` to render a group of overlapping avatars.

**Props used:** none required on `avatar.group` — wraps multiple `avatar.root` children.

--DEMO(avatar_as_group)--

## Avatar Group Count

Use `avatar.group_count` to show a "+N" count at the end of a group.

**Props used:** none required — pass the count text as a child.

--DEMO(avatar_with_group_count)--

## Avatar Group with Icon

You can also render an icon inside `avatar.group_count`.

**Props used:** none required — pass an icon as a child.

--DEMO(avatar_group_count_icon)--

## Sizes

Use the `size` prop to change the avatar's size.

**Props used:** `size` on `avatar.root`.

--DEMO(avatar_sizes)--

## Dropdown

`avatar.root` can be used as a trigger for a dropdown menu.

**Props used:** `size` on `avatar.root`; see the [Menu](/docs/components/menu) docs for menu-specific props.

--DEMO(avatar_dropdown_menu)--

# API Reference

## avatar.root

The root component that wraps the avatar image and fallback.

```python
avatar.root(
    avatar.image(src="/avatars/01.png"),
    avatar.fallback("RD"),
)
```

| Prop         | Type                                       | Default     |
| ------------ | ------------------------------------------ | ----------- |
| `size`       | `Literal["default", "sm", "lg", "xl"]`     | `"default"` |
| `class_name` | `str`                                       | `""`        |

## avatar.image

Renders the `<img>` and probes its `src` client-side on mount — if it fails to load, it hides itself and reveals the sibling `avatar.fallback` automatically. No `fallback_id` wiring needed.

```python
avatar.image(src="/avatars/01.png", custom_attrs={"alt": "@shadcn"})
```

| Prop         | Type  | Default             |
| ------------ | ----- | ------------------- |
| `src`        | `str` |                      |
| `id`         | `str` | auto-generated       |
| `class_name` | `str` | `""`                 |

Any other prop accepted by a native `<img>` is also passed straight through.

## avatar.fallback

Shown automatically when `avatar.image` fails to load.

```python
avatar.fallback("RD")
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## avatar.badge

Displays a badge indicator on the avatar, positioned at the bottom right by default.

```python
avatar.badge(hi("BadgeCheck01Icon"))
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## avatar.group

Displays a group of avatars with overlapping styling.

```python
avatar.group(
    avatar.root(...),
    avatar.root(...),
)
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |

## avatar.group_count

Displays a count indicator at the end of an avatar group.

```python
avatar.group_count("+3")
```

| Prop         | Type  | Default |
| ------------ | ----- | ------- |
| `class_name` | `str` | `""`    |
