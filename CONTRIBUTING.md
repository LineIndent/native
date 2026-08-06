# Contributing to Buridan Native

Thank you for your interest in contributing to Buridan Native! We appreciate your help in making this project better.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Development Environment](#development-environment)
- [Project Structure](#project-structure)
- [Workflow & Automation](#workflow--automation)
- [Adding New Components](#adding-new-components)
- [Dependency Management](#dependency-management)
- [Testing](#testing)
- [Style Guidelines](#style-guidelines)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

Please be respectful and helpful to all contributors.

## Development Environment

Buridan Native uses `uv` for dependency management.

1. **Install uv:** If you don't have it, follow the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).
2. **Setup environment:**
   ```bash
   uv sync --group dev
   ```

## Project Structure

- `components/`: UI component definitions.
- `docs/`: Source markdown documentation.
- `native/`: Framework source code, registry, and anatomy definitions.
- `scripts/`: Build and generation scripts.
- `tests/`: Project test suite.

## Workflow & Automation

### Running the App
We use a custom dev script to launch the Reflex application in development mode:
```bash
uv run python dev.py
```
This script allows you to select specific sections or pages to run in development.

## Adding New Components

To contribute a new UI component, follow these steps:

1. **Create Component File:**
   Define your component in `components/ui/<name>.py`. Follow the style and structure of existing components (e.g., `components/ui/button.py`).

2. **Define Anatomy:**
   Create the component's anatomy file at `native/registry/anatomy/<name>.py`. This file defines how the component parts nest, which is critical for documentation and composition.

   Example (`native/registry/anatomy/accordion.py`):
   ```python
   from components.ui.accordion import accordion

   COMPOSITION = accordion.root(
       accordion.item(
           accordion.trigger(),
           accordion.panel(),
       ),
   )
   ```

3. **Add Documentation:**
   Create `docs/components/<name>.md`. Use existing components as templates to include proper frontmatter, description, and demo references using the `--DEMO(...)--` syntax.

4. **Generate & Verify:**
   After adding your component files, run the generation scripts in order to update the registry, documentation assets, and social preview cards:
   ```bash
   # 1. Regenerate registry
   uv run python scripts/generate_registry.py
   
   # 2. Regenerate documentation markdown
   uv run python scripts/generate_markdown.py
   
   # 3. Generate social preview card
   uv run python scripts/generate_preview_cards.py
   ```
   Run the test suite to ensure your component is correctly registered and documented:
   ```bash
   uv run pytest
   ```

## Dependency Management

If your contribution requires new Python packages, please add them to `pyproject.toml` under the `dev` dependency group (if it's a dev tool) or the main project dependencies. After modifying `pyproject.toml`, update your local environment by running:

```bash
uv sync
```

## Testing

We have a comprehensive test suite that verifies documentation, component resolution, and asset generation. Before submitting changes, run the tests to ensure everything is correct:
```bash
uv run pytest
```

## Style Guidelines

We use `ruff` for linting and formatting. Ensure your code complies with our configuration defined in `pyproject.toml`.

## Submitting Changes

1. **Fork the repository** and create a branch for your feature or bug fix.
2. **Make your changes**, keeping them focused and consistent with existing patterns.
3. **Run tests** (`uv run pytest`) to ensure no regressions were introduced.
4. **Submit a Pull Request** describing your changes and referencing any related issues.
