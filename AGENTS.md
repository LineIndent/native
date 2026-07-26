# Buridan Native Framework - Agent Guide

## Overview

Native is a framework for building native applications using Python.

This repository contains the framework source code, UI components,
documentation, examples, and supporting tooling.

When working with Native, prefer the repository documentation and existing
patterns over assumptions or general framework knowledge.

## Documentation

The primary documentation lives in:

```text
docs/
```

The public documentation site is:

https://native.buridan.dev/

### Documentation URL Mapping

Repository documentation paths map to public URLs.

Example:

```text
docs/getting_started/introduction.md
```

maps to:

```text
https://native.buridan.dev/docs/getting-started/introduction
```

Rules:

- Underscores in paths become hyphens in URLs.
- Markdown extensions are removed.
- The `/docs/` prefix is preserved.

### Component Documentation

Component documentation lives in:

```text
docs/components/
```

Component URLs follow:

```text
https://native.buridan.dev/components/<component-name>
```

Example:

```text
docs/components/button.md
```

maps to:

```text
https://native.buridan.dev/components/button
```

## Development Principles

When modifying Native:

- Prefer existing components and patterns before creating new ones.
- Follow existing naming conventions.
- Keep APIs consistent with existing components.
- Update documentation when adding user-facing features.
- Match existing architecture and design decisions.
- Avoid introducing unnecessary abstractions.
- Look for similar existing implementations before creating new ones.

## Documentation Priority

When information conflicts, use this priority:

1. Repository documentation
2. Source code implementation
3. Existing project patterns
4. General framework knowledge

The Native documentation and source code are the source of truth.

## Agent Skills

Specialized agent skills are located at:

```text
.agents/skills/
```

Use the most specific skill available for the task.

Available skills:

### getting-started

Covers:

- Installing Native
- Creating a project
- CLI usage
- Development workflow
- Basic configuration

Location:

```text
.agents/skills/getting-started/SKILL.md
```

### components

Covers:

- Native UI components
- Component APIs
- Creating new components
- Component usage patterns

Location:

```text
.agents/skills/components/SKILL.md
```

### theming

Covers:

- Styling
- Themes
- Colors
- Visual customization

Location:

```text
.agents/skills/theming/SKILL.md
```

## Working With Native

Before implementing a feature:

1. Check whether an existing component or pattern already exists.
2. Read the relevant documentation.
3. Follow existing APIs and conventions.
4. Update documentation if the feature is user-facing.
5. Keep changes focused and consistent with the project.

## When Adding New Features

For new components:

- Follow existing component structure.
- Add documentation.
- Add examples when appropriate.
- Ensure the component fits existing design patterns.

For framework changes:

- Understand the existing architecture first.
- Avoid breaking public APIs unless necessary.
- Document important decisions.

## General Guidance

When answering questions about Native:

- Prefer Native-specific examples.
- Use the documented API style.
- Avoid suggesting unsupported patterns.
- Point users toward the relevant documentation.
- Load specialized skills when available.
