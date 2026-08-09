---
title: "CLI"
description: "Learn how to use the Buridan UI Command Line Interface to manage components and themes."
order: 3
---

# buridan

Use the buridan CLI to add components, apply themes, and manage your Buridan UI project.

All commands must be run from your Reflex project root, where `rxconfig.py` is located.

# Installation

Add `buridan` to your `pyproject.toml`:

```toml
dependencies = ["buridan=={current version}"]
```

Then sync your environment with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

See the [Installation](/docs/getting-started/installation) page for the full setup guide.

# create

Open the Buridan UI theme builder in your browser. Use it to customize your design system and generate a unique preset ID.

```bash
buridan create
```

# init

Initialize Buridan UI in your project. This command sets up CSS utilities (shimmer, scrollbar) in `assets/globals.css` and updates `rxconfig.py` with the required Tailwind configuration.

```bash
buridan init
```

# apply

Apply a theme preset to your project. Generates `:root` and `.dark` CSS variable blocks in `assets/globals.css` based on the preset ID from the theme builder, and records the applied theme in [`components.json`](/docs/components-json).

```bash
buridan apply --preset <ID>
```

Arguments:

- `--preset`: The theme preset ID from the Buridan UI theme builder. Use `b0` for the default theme.

Example:

```bash
buridan apply --preset b0
buridan apply --preset b2D0wqNxT
```

Re-running `buridan apply` with a different preset overwrites the theme section of `components.json` and the generated CSS variables — it does not touch any components you've already added.

# add

Add components and their dependencies to your project.

```bash
buridan add <name>
```

You can add multiple components at once:

```bash
buridan add button input select
```

Blocks (charts, dashboards, etc.) can be added the same way:

```bash
buridan add line_chart_01
```

Components are placed in `components/`, blocks in `blocks/`. Dependencies are resolved and added automatically. Every install updates the `components` section of [`components.json`](/docs/components-json) with the name and version of each installed component.

> **Note:** Components require a theme to render correctly. Run `buridan apply` before using components.

## Versioning

Some components have more than one published version. By default, `add` installs the latest available version:

```bash
buridan add button
```

To pin a specific version, append `@<version>` to the component name:

```bash
buridan add button@1.0.0
```

Version pins you specify explicitly always take priority over versions pulled in automatically by another component's dependencies. For example, if you run:

```bash
buridan add card button@1.0.0
```

and `card` normally depends on the latest `button`, your explicit `button@1.0.0` pin wins — `card` will be installed against `button@1.0.0`, not whatever the latest version happens to be.

If you pin the same component to two different versions in one command (or the CLI otherwise detects a genuine conflict it can't resolve), it prints a warning and keeps the first version it resolved:

```bash
buridan add button@1.0.0 button@2.0.0
# Warning: 'button' requested at both 1.0.0 and 2.0.0; keeping 1.0.0.
```

# list

Display all available components and blocks. If a component has multiple published versions, each version is listed separately (e.g. `button@1.0.0`, `button@2.0.0`).

```bash
buridan list
```

# Recommended workflow

```bash
buridan create
buridan init
buridan apply --preset <ID>
buridan add button input select
```
