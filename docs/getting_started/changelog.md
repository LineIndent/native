---
title: "Changelog"
description: "Latest updates and announcements."
order: 5
---

# Changelog

Latest updates and announcements.

# July 2026 - Native/Buridan

Under-the-hood layouts can get incredibly messy when they are wrapped in too many heavy React abstractions. In this update, we went back to the drawing board and completely rewrote Buridan's core elements to rely purely on native HTML elements (`rx.el.*`) instead of wrapping everything in heavy, custom third-party components.

By ditching complex client-side libraries like Radix UI and Base UI, we've stripped away massive JavaScript bundles and unnecessary DOM nodes. 

We did this for a couple of really practical reasons that make a huge difference in day-to-day development:

- **Crazy Fast, Lightweight Performance:** Dropping Radix and Base UI means we've eliminated heavy component runtimes. The browser has virtually no bundle bloat to download, parse, or execute. Your site loads instantly, transitions are snappy, and the interactive elements run at native speed.
- **Flawless Event & Focus Propagation:** Standard wrapper divs can swallow click events or break standard form focus paths. By sticking to native elements, browser features work exactly as they should. For example, if you want to click an outer styled card container and have it programmatically trigger an underlying native select dropdown or focus an input field, it works natively without your event bubble getting caught in a messy component hierarchy.
- **Featherlight DOM Overhead:** Stripping out nested wrapper divs means the browser has fewer nodes to paint. Your rendered page markup is incredibly clean, which makes styling adjustments with Tailwind CSS utilities extremely predictable—no more fighting arbitrary class specificity clashes.
- **Predictable 1:1 API mapping:** Native tags are standard. There are no hidden proprietary parameters, undocumented properties, or unexpected behavioral overrides. What you write in your Python code maps 1:1 with what the browser actually renders in the DOM tree.

It’s a simpler, much more robust foundation that keeps your apps lightweight, super-fast, and incredibly responsive.
