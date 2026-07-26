---
name: theming
description: >
  Buridan Native theming system using CSS variables, semantic tokens, and
  Tailwind v4. Use when customizing appearance, colors, typography, dark mode,
  styling components, creating themes, working with Tailwind classes, or
  modifying design tokens.
---

# Buridan Native Theming

This skill covers the Buridan Native design system and styling approach.

Buridan Native uses:

- CSS variables for theme tokens
- Semantic design tokens
- Tailwind v4 utilities
- Component styling based on shared tokens

The theme system is designed so applications can customize appearance without
rewriting component styles.

The documentation is the source of truth.

---

# Styling Philosophy

Use semantic tokens instead of hardcoded values.

Prefer:

```python
rx.el.div(
    class_name="bg-background text-foreground"
)
```

over:

```python
rx.el.div(
    class_name="bg-white text-black"
)
```

Semantic tokens allow:

- Light/dark mode support
- Consistent design
- Application-wide customization
- Component compatibility

---

# Theme Architecture

The styling stack:

```
CSS Variables
      ↓
Theme Tokens
      ↓
Tailwind v4 @theme inline
      ↓
Tailwind Utilities
      ↓
Buridan Native Components
```

Components consume tokens rather than defining isolated colors.

---

# Tailwind v4

Buridan Native recommends Tailwind v4.

Tailwind v4 exposes CSS variables as utilities through:

```css
@theme inline;
```

Example:

```css
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
}
```

This enables utilities:

```text
bg-background
text-foreground
border-border
rounded-lg
```

inside Reflex components.

Example:

```python
rx.el.div(
    class_name="bg-background text-foreground"
)
```

---

# Theme Tokens

Theme tokens are defined in:

```css
:root;
```

and:

```css
.dark
```

Example:

```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
}
```

Dark mode overrides the same semantic tokens.

---

# Core Tokens

## Background

Controls:

- Application background
- Page surfaces

Usage:

```text
bg-background
```

---

## Foreground

Controls:

- Default text color

Usage:

```text
text-foreground
```

---

## Card

Controls:

- Elevated surfaces
- Panels
- Dashboard sections

Usage:

```text
bg-card text-card-foreground
```

---

## Primary

Controls:

- High emphasis actions
- Brand surfaces
- Active states

Usage:

```text
bg-primary text-primary-foreground
```

---

## Secondary

Controls:

- Supporting actions
- Secondary surfaces

Usage:

```text
bg-secondary
```

---

## Muted

Controls:

- Subtle backgrounds
- Secondary text

Usage:

```text
bg-muted text-muted-foreground
```

---

## Accent

Controls:

- Hover states
- Selected states
- Interactive highlights

---

## Destructive

Controls:

- Errors
- Dangerous actions
- Delete actions

---

## Border

Controls:

- Borders
- Separators
- Component outlines

Usage:

```text
border-border
```

---

## Input

Controls:

- Form controls
- Input surfaces

---

## Ring

Controls:

- Focus states
- Keyboard navigation

---

# Component Styling Rules

When styling Buridan Native components:

1. Use component variants first.
2. Use theme tokens second.
3. Use custom Tailwind classes only when necessary.

Prefer:

```python
native.button(
    "Save",
    variant="primary"
)
```

over manually styling:

```python
rx.el.button(
    "Save",
    class_name="bg-primary text-primary-foreground"
)
```

unless creating custom UI.

---

# Using rx.el.\*

For custom layouts and additional structure:

```python
rx.el.div(
    class_name="bg-background text-foreground"
)
```

Use Tailwind utilities with semantic tokens.

Avoid:

```python
rx.el.div(
    class_name="bg-[#ffffff]"
)
```

because it bypasses the theme system.

---

# Adding New Tokens

When adding a new token:

1. Add the variable in `:root`.
2. Add the dark mode equivalent.
3. Expose it through `@theme inline`.
4. Use the semantic Tailwind utility.

Example:

CSS:

```css
:root {
  --warning: oklch(0.84 0.16 84);
  --warning-foreground: oklch(0.28 0.07 46);
}

.dark {
  --warning: oklch(0.41 0.11 46);
  --warning-foreground: oklch(0.99 0.02 95);
}
```

Expose:

```css
@theme inline {
  --color-warning: var(--warning);
}
```

Use:

```python
rx.el.div(
    class_name="bg-warning text-warning-foreground"
)
```

---

# Tailwind Plugins

Some Tailwind plugins require explicit configuration.

Example:

```python
from reflex.plugins.shared_tailwind import TailwindConfig

config = rx.Config(
    plugins=[
        rx.plugins.TailwindV4Plugin(
            config=TailwindConfig(
                plugins=["@tailwindcss/typography"]
            )
        ),
    ],
)
```

Do not add plugins unless required.

---

# CSS Loading

Ensure global theme CSS is loaded by the application:

```python
app = rx.App(
    stylesheets=["globals.css"]
)
```

---

# Documentation References

Repository:

```text
docs/resources/theming.md
```

Public documentation:

https://native.buridan.dev/docs/resources/theming

---

# When To Use This Skill

Use this skill when asking:

- How do I customize the theme?
- How do colors work?
- How do I add a design token?
- How do I support dark mode?
- How do I style components?
- How do Tailwind classes work with Native?
- How do I customize CSS variables?

---

# Do Not Use This Skill For

Do not use this skill for:

- Choosing components
- Component APIs
- Application state
- Event handling
- Charts
- Framework architecture

Use the specialized skill instead.
