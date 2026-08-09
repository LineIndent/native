---
title: "Skills"
description: "Give your AI assistant deep knowledge of Buridan UI components, patterns, and best practices."
order: 2
---

# Skills

Buridan Skills give AI assistants project-aware knowledge about Buridan UI.

When installed, your AI assistant understands how to discover, install, compose, and customize Buridan components using the correct APIs and project conventions.

For example, you can ask your AI assistant:

- _"Add a dashboard page with a sidebar and data table."_
- _"Create a login form using Buridan components."_
- _"Add a dark mode theme."_
- _"Install the button and card components."_
- _"Create a new component following Buridan patterns."_

The skill gives your assistant knowledge about your project's configuration, installed components, CLI workflow, theming system, and recommended architecture patterns.

# Using Skills

Buridan Skills are included with the repository and do not require separate installation. They are located in the `.agents/skills/` directory. When working within the project, your AI assistant automatically loads this guidance.

# What's Included

The Buridan skill provides your AI assistant with the following knowledge:

## Component Discovery

Learn how to find, install, and compose Buridan UI components.

Includes:

- Component APIs
- Component dependencies
- Usage patterns
- Composition guidelines
- Recommended component combinations

## CLI Workflow

Guidance for using the Buridan CLI instead of manually copying component code.

Includes:

- Adding components
- Resolving dependencies
- Managing project configuration
- Updating components
- Following the recommended installation workflow

## Theming and Customization

Knowledge of the Buridan design system and customization patterns.

Includes:

- OKLCH color variables
- Theme customization
- Dark mode patterns
- Design tokens
- Component variants

## Framework Patterns

Architecture guidance for building applications with Buridan.

Includes:

- Recommended layouts
- State management patterns
- Component organization
- Routing conventions
- Project structure best practices

# How It Works

- **Project detection**

  The skill identifies your Buridan project configuration and available components.

- **Context injection**

  Your AI assistant receives information about your framework setup, installed components, project structure, and available patterns.

- **Pattern enforcement**

  The assistant follows Buridan conventions when generating new code instead of relying on generic UI patterns.

- **Component assistance**

  The assistant uses Buridan component knowledge and documentation before creating implementations.

# Repository Files

Buridan Skills are powered by repository-level instructions and specialized knowledge modules.

| File                             | Purpose                                                       |
| -------------------------------- | ------------------------------------------------------------- |
| `AGENTS.md`                      | Main instructions for AI assistants working in the repository |
| `.agents/skills/components`      | Component APIs and usage patterns                             |
| `.agents/skills/theming`         | Theme customization and design tokens                         |
| `.agents/skills/getting-started` | Installation and project setup                                |

`AGENTS.md` provides general repository guidance, including project conventions, documentation locations, and available skills.

Individual skills provide specialized knowledge for specific tasks such as building components, customizing themes, or setting up a project.

# Learn More

- [CLI](/docs/getting-started/cli) — Learn how to install and manage Buridan components
- [Components](/docs/components) — Explore available UI components
- [Theming](/docs/resources/theming) — Customize colors, tokens, and appearance
- [Documentation](/docs) — Browse the full Buridan UI documentation
