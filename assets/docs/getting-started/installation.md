---
title: "Installation"
description: "Steps to install and start using Buridan in your project."
order: 1
---

# Installation

How to install dependencies and structure your app.

> Recommended for new projects: Use [buridan/create](/create) to build your preset visually and generate the right setup command for your framework.

# Use buridan/create

Build your preset visually, preview your choices, and generate a framework-specific setup command. You can use your final theme system locally or pipe-lined to Reflex Build. Start with the default preset [Neutral](/create?preset=b0)

# Prerequisites

Python 3.10+ (required by Reflex)

# Local Environment

It's recommended to use the [uv](https://docs.astral.sh/uv/) package manager when working with Reflex apps.

The following page provides a step-by-step [installation](https://reflex.dev/docs/getting-started/installation/) guide for Reflex apps. Buridan is installed into an existing Reflex project, so make sure you have a project with an `rxconfig.py` at its root before continuing. Every `buridan` command needs to be run from that project root.

After setting up your Reflex environment, you can install the `buridan` package by adding it to your `pyproject.toml` file.

```toml
dependencies = ["buridan=={current version}"]
```

You can find the latest published version on [PyPI](https://pypi.org/project/buridan/).

After adding the package, sync your environment with uv:

```bash
uv sync
```

Installing it will give access to the full [CLI](/docs/getting-started/cli) tool. To confirm everything is set up correctly, run:

```bash
buridan init
```

This sets up the CSS utilities and Tailwind configuration Buridan needs, and confirms the CLI is installed and working. From here, see the [CLI docs](/docs/getting-started/cli) for the recommended workflow to apply a theme and start adding components.

# Troubleshooting

If `uv sync` or a manual `pip install` fails with `error: externally-managed-environment`, you're likely installing against your system Python rather than a project-scoped environment. Using `uv sync` inside a Reflex project set up per the guide above avoids this. If you're not using uv, make sure you've activated a virtual environment first (`python3 -m venv .venv && source .venv/bin/activate`) before installing.
