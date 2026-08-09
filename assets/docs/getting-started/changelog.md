---
title: "Changelog"
description: "Latest updates and announcements."
order: 5
---

# Changelog

Latest updates and announcements.

# August 2026 - Component Versioning & components.json

As Buridan UI's component library has grown, we've run into a familiar problem: components change over time, and sometimes those changes aren't backward compatible. Until now, updating a component in the registry meant every project pulling that component got the new version, whether it was ready for it or not. This update fixes that.

Components can now publish multiple versions side by side, and the CLI lets you choose exactly which one you want.

- **Version pinning:** Install a specific version of any component with `buridan add button@1.0.0`, or leave off the version to get the latest one automatically. Your project stays exactly as you set it up, even as new versions get published to the registry.
- **Smart dependency resolution:** If a component you're adding depends on another versioned component, the CLI resolves it sensibly. An explicit version you pin always takes priority over whatever a dependency would otherwise pull in, so you're never surprised by a version swap you didn't ask for.
- **A new components.json manifest:** Every `buridan add` and `buridan apply` now records what's actually installed in your project, including each component's version and your currently applied theme preset. It's a simple, readable log of your project's setup, not something you need to edit by hand, but useful to have around when you're checking what's installed or diffing changes over time.
- **Clear conflict handling:** If two different versions of the same component end up requested at once, the CLI warns you about it instead of quietly picking one and leaving you to find out later.

None of this changes how components look or behave today. It just means your project can move at its own pace as the registry evolves underneath it.

# July 2026 - Native/Buridan

Under-the-hood layouts can get incredibly messy when they are wrapped in too many heavy React abstractions. In this update, we went back to the drawing board and completely rewrote Buridan's core elements to rely purely on native HTML elements (`rx.el.*`) instead of wrapping everything in heavy, custom third-party components.

By ditching complex client-side libraries like Radix UI and Base UI, we've stripped away massive JavaScript bundles and unnecessary DOM nodes.

We did this for a couple of really practical reasons that make a huge difference in day-to-day development:

- **Crazy Fast, Lightweight Performance:** Dropping Radix and Base UI means we've eliminated heavy component runtimes. The browser has virtually no bundle bloat to download, parse, or execute. Your site loads instantly, transitions are snappy, and the interactive elements run at native speed.
- **Flawless Event & Focus Propagation:** Standard wrapper divs can swallow click events or break standard form focus paths. By sticking to native elements, browser features work exactly as they should. For example, if you want to click an outer styled card container and have it programmatically trigger an underlying native select dropdown or focus an input field, it works natively without your event bubble getting caught in a messy component hierarchy.
- **Featherlight DOM Overhead:** Stripping out nested wrapper divs means the browser has fewer nodes to paint. Your rendered page markup is incredibly clean, which makes styling adjustments with Tailwind CSS utilities extremely predictable—no more fighting arbitrary class specificity clashes.
- **Predictable 1:1 API mapping:** Native tags are standard. There are no hidden proprietary parameters, undocumented properties, or unexpected behavioral overrides. What you write in your Python code maps 1:1 with what the browser actually renders in the DOM tree.

It's a simpler, much more robust foundation that keeps your apps lightweight, super-fast, and incredibly responsive.
