---
title: "components.json"
description: "Configuration and state tracked automatically for your project."
order: 4
---

# components.json

The `components.json` file tracks the components and theme currently installed in your project.

Unlike some other CLI tools, you don't create or edit this file by hand, the `buridan` CLI creates and updates it automatically the first time you run `buridan apply` or `buridan add`. Its main purpose is to give you (and the CLI) a single place to see exactly what's installed, at what version, and under what theme.

**Note:** `components.json` is written to the root of your Reflex project, alongside `rxconfig.py`. It's safe to commit to version control, treat it like a lockfile for your design system.

# Structure

```json
{
  "components": {
    "button": "1.0.0",
    "card": "latest",
    "core": "latest"
  },
  "theme": {
    "preset": "b0",
    "baseId": "neutral",
    "colorId": "blue",
    "chartId": "blue",
    "styleId": "default",
    "fontId": "inter",
    "radius": "0.5rem"
  }
}
```

The two sections are updated independently, running `buridan add` never touches `theme`, and running `buridan apply` never touches `components`.

# components

A map of installed component names to the version installed.

```json
{
  "components": {
    "button": "1.0.0"
  }
}
```

- The key is the component's registry name, without any `@version` suffix.
- The value is either a specific version string (e.g. `"1.0.0"`) if you pinned one with `buridan add button@1.0.0`, or the literal string `"latest"` if you installed it unpinned, or if the component doesn't have multiple published versions.

This section is updated every time you run `buridan add`. See the [CLI docs](/docs/getting-started/cli#versioning) for how version pinning and conflicts are resolved.

# theme

Records the theme preset currently applied to your project.

```json
{
  "theme": {
    "preset": "b0",
    "baseId": "neutral",
    "colorId": "blue",
    "chartId": "blue",
    "styleId": "default",
    "fontId": "inter",
    "radius": "0.5rem"
  }
}
```

This section is written by `buridan apply --preset <ID>` and fully overwritten (not merged) on every subsequent `apply`, it always reflects only the most recently applied preset.

### theme.preset

The raw preset ID from the [theme builder](/docs/getting-started/cli#create), exactly as passed to `--preset`. This is the source of truth for the rest of the fields below, since it fully encodes the theme, it's the most reliable value to reference if you ever need to reconstruct or re-apply the same theme programmatically.

```json
{
  "theme": {
    "preset": "b2D0wqNxT"
  }
}
```

### theme.baseId

The base theme (background, foreground, and neutral tones) the preset is built on.

### theme.colorId

The accent color palette applied on top of the base theme.

### theme.chartId

The color palette used for chart-specific CSS variables (`--chart-1` through `--chart-5`, etc.). This can differ from `colorId` if the preset uses a separate chart palette.

### theme.styleId

The component style variant (e.g. spacing, shadow, and border conventions) the preset applies.

### theme.fontId

The font family applied by the preset.

### theme.radius

The border-radius value applied by the preset, e.g. `"0.5rem"`. Omitted from `components.json` if the preset doesn't override the style's own default radius.

Any field above that wasn't set by a given preset is left out of `components.json` entirely rather than written as `null`, so the file only ever shows what was actually specified.
