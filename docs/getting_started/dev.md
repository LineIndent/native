---
title: "dev"
description: "Interactive and command-line tool for selecting and running Buridan documentation pages locally."
order: 4
---

# dev

The `dev` command is a CLI tool used to control which documentation pages are loaded during local development.

It replaces manual environment variable setup and makes it easier to selectively run parts of the documentation site while developing. Pages can be picked interactively through a fuzzy search prompt, or loaded directly by name.

# Requirements

This tool uses [questionary](https://github.com/tmbo/questionary) for the environment/confirm prompts, and [InquirerPy](https://github.com/kazhala/InquirerPy) for fuzzy-searchable page selection. Both are declared in the `dev` dependency group, so they're installed automatically.

```bash
uv sync
```

This also registers the `dev` command itself, via the `[project.scripts]` entry in `pyproject.toml`:

```pyproject.toml
[project.scripts]
dev = "cli.dev:main"
```

# Usage

Run the command from your project root:

```bash
uv run dev
```

With no arguments, this starts the interactive flow: choose an environment, then fuzzy-search and multi-select pages.

To skip the prompts entirely, pass pages, sections, or a mode directly as arguments — see below.

# Command Reference

```text
uv run dev [pages...] [--section SECTION [SECTION ...]] [--prod]
```

| Argument          | Description                                                                                   |
| ----------------- | --------------------------------------------------------------------------------------------- |
| `pages`           | Page names (e.g. `button`) or full paths (e.g. `components/button`) to load, space-separated. |
| `--section`, `-s` | Load every page in the given section(s). Accepts one or more section names.                   |
| `--prod`          | Run in prod mode, loading the full site. Same as passing `prod` as the only argument.         |

If any pages or sections are passed on the command line, `dev` runs immediately in dev mode with those pages — no prompts, no confirmation step.

If nothing is passed, `dev` falls back to the interactive flow (environment select → fuzzy page search).

## Examples

Interactive picker (no arguments):

```bash
uv run dev
```

Load specific pages by name:

```bash
uv run dev button input
```

Load a page by its full `section/page` path — useful if a page name exists in more than one section:

```bash
uv run dev components/button
```

Load an entire section:

```bash
uv run dev --section components
```

Load multiple sections at once:

```bash
uv run dev --section components auth
```

Mix individual pages and whole sections in one command:

```bash
uv run dev button --section auth
```

Run the full site in prod mode, skipping all prompts:

```bash
uv run dev prod
```

```bash
uv run dev --prod
```

# Page Name Resolution

When you pass a bare page name (e.g. `button`), `dev` looks it up across every section:

- **Unique match** — resolves automatically to its full path (e.g. `components/button`).
- **Ambiguous match** — if the same page name exists in more than one section, `dev` prints an error listing every match and asks you to use the full `section/page` path instead of guessing.
- **No match** — prints an error naming the page that couldn't be found. Nothing is launched if any requested page or section fails to resolve.

# Environment

## Dev

Development mode allows you to work on specific parts of the documentation without loading the entire site. It's the default mode whenever pages or sections are provided, or when you're using the interactive picker.

Use this mode when:

- Working on specific documentation pages
- Debugging content structure
- Speeding up local development

## Prod

Production mode runs the full documentation site without any filtering. Trigger it with `uv run dev prod`, `uv run dev --prod`, or by selecting **prod** in the interactive picker.

# Interactive Page Selection

When no arguments are passed, page selection happens through a single fuzzy-searchable, multi-select prompt:

- Type to filter the list by page name or section name
- Press `Tab` to select multiple entries
- Press `Enter` to confirm your selection

Each section also has a virtual **"(entire section)"** entry at the top of its group, letting you pull in every page in that section with one selection instead of picking them individually. You can mix and match — for example, select an entire section plus a couple of individual pages from other sections in the same pass.

If no pages are selected, the CLI exits without launching Reflex. When pages are selected interactively, you'll be asked to confirm before Reflex starts; this confirmation step is skipped when pages are passed directly as command-line arguments.
