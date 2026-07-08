from pathlib import Path

BASE_PATH = Path("docs")


def slugify(name: str) -> str:
    return name.strip().lower().replace(" ", "-")


def generate_template(title: str) -> str:
    return f"""---
title: {title}
description:
order:
---

# Usage

## Installation

## Basic Usage

## Anatomy


# Examples


# API Reference

"""


def main():
    name = input("Component name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    folder = input("Folder inside docs/ (example: components/): ").strip()

    folder_path = BASE_PATH / folder
    file_path = folder_path / f"{slugify(name)}.md"

    if file_path.exists():
        print(f"File already exists: {file_path}")
        return

    folder_path.mkdir(parents=True, exist_ok=True)

    file_path.write_text(
        generate_template(name.title()),
        encoding="utf-8",
    )

    print(f"Created: {file_path}")


if __name__ == "__main__":
    main()
