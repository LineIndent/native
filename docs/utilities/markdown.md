---
title: "Markdown"
description: "A lightweight, dependency-free way to render markdown in Reflex using Tailwind Typography."
order: 0
---

# Markdown

A lightweight, dependency-free way to render markdown in Reflex using Tailwind Typography.

Most component libraries, Radix included, ship a `Markdown` component that parses and renders markdown on the client, in the browser, on every render. That's a reasonable default, but it also means shipping a parser to the client and mapping every markdown token to a component.

This page shows a different pattern: parse markdown to HTML once, on the server, with Python's `markdown` library, then hand the raw HTML to `rx.html` with a Tailwind Typography class attached. There's no client-side parser and no component-per-token mapping, just HTML and CSS.

This isn't a component with an API to learn. It's a small utility function plus a CSS class, both of which you're expected to copy in and adapt.

# How it works

Three pieces work together:

1. **`markdown`** is a Python library that converts a markdown string into an HTML string.
2. **A prose class**, built on `@tailwindcss/typography`, styles raw HTML elements (`h1`, `p`, `table`, `blockquote`, etc.) to match your UI.
3. **`rx.html`** renders a raw HTML string as a component, with the prose class applied.

```python
def render_markdown(text: str) -> rx.Component:
    if not text.strip():
        return rx.el.div()

    html = markdown.markdown(text, extensions=["fenced_code", "tables"])
    return rx.html(html, class_name="prose-content")
```

That's the whole pattern. Everything past this point, including which extensions to enable, how to style the class, and whether to post-process the HTML at all, is optional and up to your project.

# Setup

## Install markdown

```bash
pip install markdown
```

Extensions worth knowing about:

| Extension     | Purpose                                                   |
| ------------- | --------------------------------------------------------- |
| `fenced_code` | Enables triple-backtick code blocks                       |
| `tables`      | Enables GitHub-style pipe tables                          |
| `toc`         | Adds `id` attributes to headings, useful for anchor links |

Full list in the [Python-Markdown extension docs](https://python-markdown.github.io/extensions/).

## Add Tailwind Typography

Because `@tailwindcss/typography` gets processed as a JavaScript file, it should be added directly to `rxconfig.py` plugins.

```python
import reflex as rx
from reflex.plugins.shared_tailwind import TailwindConfig

config = rx.Config(
    ...,
    plugins=[
        rx.plugins.TailwindV4Plugin(
            config=TailwindConfig(plugins=["@tailwindcss/typography"])
        ),
    ],
)
```

## Write a prose class

The `prose` class from Typography is unstyled but structured on its own; most projects add a class on top of it to bring in their own theme. Below is one example. Treat the class name, colors, and spacing as placeholders, not requirements.

Two rules are worth keeping regardless of theme, since they fix rendering quirks rather than express a style opinion:

- Resetting `::before`/`::after` content on `code` and `blockquote`. Typography adds decorative quote marks by default, which most non-editorial UIs don't want.
- Resetting `pre > code` padding and background. Without it you get double backgrounds, since both `pre` and the `code` inside it are styled.

```css
@layer components {
  /* name and theme this however fits your project */
  .prose-content {
    @apply prose dark:prose-invert max-w-none w-full;

    /* fixes double-styling on code blocks */
    @apply prose-pre:p-0
            prose-pre:overflow-x-auto
            prose-pre:before:content-none
            prose-pre:after:content-none
            prose-code:before:content-none
            prose-code:after:content-none;

    /* everything below is a styling choice, not a requirement */
    @apply prose-code:rounded-md
            prose-code:bg-muted
            prose-code:px-1.5
            prose-code:py-0.5
            prose-code:text-sm
            prose-pre:rounded-lg
            prose-pre:bg-muted
            prose-pre:border;
  }
}
```

## Put it together

```python
from components.markdown import render_markdown

def page() -> rx.Component:
    return render_markdown("""
# Welcome

Some **markdown** content, rendered straight to HTML.
""")
```

# What markdown elements look like

Everything below is real markdown, run through `render_markdown`, styled with this site's own prose class. It's one possible look, not the only one.

## Headings

Typography styles `h1`–`h6` out of the box. Override with `prose-h1:*` / `prose-h2:*` modifiers as needed.

```md
# Page title

## Section heading
```

## Text formatting

Bold, italic, and inline code markers map straight to their HTML equivalents.

You can use **bold text**, _italic text_, or `inline code` inside a normal paragraph.

```md
You can use **bold text**, _italic text_, or `inline code`.
```

## Lists

- List markers can be restyled with `prose-li:marker:*`
- Ordered and unordered lists both inherit standard Typography spacing
- Nested lists work out of the box

```md
- First item
- Second item
  - Nested item
```

## Links

[Links](#) inherit Typography's default underline-on-hover treatment. Restyle with `prose-a:*`.

## Code blocks

Fenced code blocks come from the `fenced_code` extension. Typography wraps them in a `pre > code` pair, and the double-styling fix from the CSS above keeps that pairing clean.

```python
def hello(name: str) -> str:
    return f"Hello, {name}!"
```

## Blockquotes

Typography's default blockquote is an italic left border. Some projects prefer a bordered callout instead. Both are reasonable; restyle with `prose-blockquote:*`.

> A blockquote, styled however fits your content.

```md
> A blockquote, styled however fits your content.
```

# Optional: handling table overflow

Markdown tables render as plain `<table>` elements, which can overflow their container on narrow screens or long content. This isn't specific to this rendering approach; it's a general HTML table problem. But it's common enough with markdown-sourced tables that it's worth a note.

One way to handle it is to post-process the generated HTML and wrap each `<table>` in a scrollable container before it reaches `rx.html`. This is one option among several. You could just as easily reach for an `overflow-x-auto` utility on a parent element, a CSS container query, or leave tables unwrapped if your content never has wide ones.

```python
from bs4 import BeautifulSoup

def wrap_tables(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for table in soup.find_all("table"):
        wrapper = soup.new_tag("div")
        wrapper["class"] = "w-full overflow-x-auto"
        table.wrap(wrapper)

    return str(soup)
```

```md
| Column A | Column B |
| -------- | -------- |
| Value 1  | Value 2  |
```

If you go this route, it requires `beautifulsoup4`:

```bash
pip install beautifulsoup4
```

```python
def render_markdown(text: str) -> rx.Component:
    if not text.strip():
        return rx.el.div()

    html = markdown.markdown(text, extensions=["fenced_code", "tables"])
    html = wrap_tables(html)  # optional
    return rx.html(html, class_name="prose-content")
```
