---
name: components
description: >
  Buridan Native UI component system built on Reflex. Use when creating user
  interfaces, selecting Native components, composing layouts, using rx.el.*
  HTML elements, modifying component APIs, adding components, or answering
  questions about UI development.
---

# Buridan Native Components

This skill covers building user interfaces with Buridan Native.

Buridan Native provides reusable UI components built on top of Reflex.

When building UI, prefer:

1. Buridan Native components for common UI patterns.
2. Reflex HTML elements (`rx.el.*`) for custom structure, layouts, and missing pieces.

The documentation is the source of truth.

---

# Component Strategy

## Prefer Buridan Native Components

Use existing Buridan Native components whenever possible.

Native components provide:

- Consistent styling
- Common behavior
- Accessibility patterns
- Reusable APIs
- Framework conventions

Before creating custom UI:

1. Check whether Buridan Native already provides a component.
2. Use the existing component if it matches the use case.
3. Compose components together when possible.

Do not recreate existing Native components using raw HTML.

Examples:

Use:

```python
button(...)
```

instead of:

```python
rx.el.button(...)
```

when a Native button component exists.

Use:

```python
dialog(...)
```

instead of manually creating dialog markup.

---

# Reflex HTML Elements (`rx.el.*`)

Buridan Native is built on Reflex, which provides access to HTML elements through:

```python
rx.el.*
```

Use `rx.el.*` for:

- Page structure
- Semantic HTML
- Custom layouts
- Small UI compositions
- Wrapping Native components
- Elements without a dedicated Native component

Examples:

```python
rx.el.div(
    rx.el.h1("Dashboard"),
    rx.el.p("Welcome back")
)
```

```python
rx.el.section(
    native.card(...)
)
```

```python
rx.el.header(
    rx.el.nav(...)
)
```

Common elements include:

```text
rx.el.div
rx.el.span
rx.el.p
rx.el.h1
rx.el.h2
rx.el.h3
rx.el.a
rx.el.img
rx.el.form
rx.el.input
rx.el.section
rx.el.header
rx.el.footer
rx.el.nav
```

---

# Layouts

For layouts and page composition, prefer `rx.el.*` unless Buridan Native provides a dedicated layout component.

Examples:

```python
rx.el.div(
    sidebar,
    content
)
```

```python
rx.el.section(
    header,
    body
)
```

Use Native layout primitives when they exist.

Do not create unnecessary wrapper components for simple layout.

Prefer:

```python
rx.el.div(
    native.card(...),
    native.button(...)
)
```

over:

```python
DashboardContainer(
    DashboardCard(),
    DashboardButton()
)
```

unless the pattern is reused and has meaningful behavior.

---

# Component Categories

## Actions

Use Native components for:

- Buttons
- Links
- User actions
- Controls

Avoid manually recreating interactive controls with HTML.

---

## Forms

Use Native components for:

- Inputs
- Selectors
- Toggles
- Form controls

Use `rx.el.*` for:

- Form structure
- Labels
- Custom grouping

Example:

```python
rx.el.form(
    native.input(...),
    native.button(...)
)
```

---

## Content

Use Native components for:

- Cards
- Alerts
- Badges
- Tables
- User-facing patterns

Use `rx.el.*` for:

- Text structure
- Semantic grouping
- Custom markup

---

# Creating New Components

Before adding a new Buridan Native component:

1. Confirm the pattern does not already exist.
2. Check similar components.
3. Determine whether composition is enough.
4. Follow existing component conventions.
5. Add documentation.
6. Add examples where appropriate.

Create a new component when it:

- Is reused across applications.
- Has meaningful behavior.
- Has a stable API.
- Represents a common UI pattern.

Do not create components only to wrap simple HTML.

---

# Component Documentation

Component documentation:

https://native.buridan.dev/components/

Repository documentation:

```text
docs/components/
```

URL pattern:

```text
docs/components/<component>.md
```

maps to:

```text
https://native.buridan.dev/components/<component>
```

Example:

```text
docs/components/button.md
```

maps to:

```text
https://native.buridan.dev/components/button
```

---

# When To Use This Skill

Use this skill when:

- Building UI
- Choosing between components
- Creating layouts
- Working with `rx.el.*`
- Adding new components
- Understanding Buridan Native APIs
- Migrating UI code

---

# Do Not Use This Skill For

Do not use this skill for:

- Application state
- Event architecture
- Theming systems
- Chart configuration
- Internal framework architecture

Use the specialized skill instead.
