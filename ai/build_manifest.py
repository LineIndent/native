"""
Builds a structured manifest of every component + prop from the Markdown
docs. This is the grounding context fed to the model — instead of letting
it guess at your API, it only ever sees components/props that genuinely
exist in your library.
"""

import json
import os
import re
from pathlib import Path

LIBRARY_ROOT = Path(os.environ.get("COMPONENT_LIBRARY_ROOT", "."))
DOCS_DIR = LIBRARY_ROOT / "docs"
OUTPUT_PATH = Path(__file__).parent / "manifest.json"

# Matches "## component.subcomponent" headers under the "# API Reference" section
API_HEADER_RE = re.compile(r"^## (.+)$", re.MULTILINE)
# Matches a markdown table row: | `prop` | `Type` | `default` |
TABLE_ROW_RE = re.compile(
    r"^\|\s*`?([\w./]+)`?\s*\|\s*(.+?)\s*\|\s*(.*?)\s*\|.*$", re.MULTILINE
)
CODE_BLOCK_RE = re.compile(r"```python\n(.*?)\n```", re.DOTALL)


def extract_api_reference(text: str) -> str:
    marker = "# API Reference"
    idx = text.find(marker)
    return text[idx:] if idx != -1 else ""


def parse_component_sections(api_text: str) -> list[dict]:
    sections = []
    headers = list(API_HEADER_RE.finditer(api_text))
    for i, match in enumerate(headers):
        name = match.group(1).strip()
        start = match.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(api_text)
        body = api_text[start:end]

        code_match = CODE_BLOCK_RE.search(body)
        example = code_match.group(1).strip() if code_match else None

        props = []
        for row in TABLE_ROW_RE.finditer(body):
            prop_name, prop_type, default = row.groups()
            # skip the header separator row and the "Prop | Type | Default" header itself
            if prop_name.strip("-") == "" or prop_name.lower() == "prop":
                continue
            props.append(
                {
                    "name": prop_name.strip(),
                    "type": prop_type.strip(),
                    "default": default.strip() or None,
                }
            )

        # first prose line of body — properly skip the whole code block
        # (not just lines *starting* with ``` — lines *inside* the block
        # don't start with backticks either, and were leaking through as
        # a fake "description" whenever a section had no prose before its
        # code example, e.g. accordion.root / accordion.panel)
        description = ""
        in_code_block = False
        for line in body.strip().splitlines():
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            if stripped and not stripped.startswith(("|", "#")):
                description = stripped
                break

        sections.append(
            {
                "component": name,
                "description": description,
                "props": props,
                "example": example,
            }
        )
    return sections


def build_manifest() -> dict:
    if not DOCS_DIR.exists():
        raise FileNotFoundError(
            f"No docs/ directory found at {DOCS_DIR.resolve()}. "
            f"Set COMPONENT_LIBRARY_ROOT to the root of your actual Reflex project."
        )

    manifest = {"components": []}
    category_dirs = [d for d in DOCS_DIR.iterdir() if d.is_dir()]
    for category_dir in sorted(category_dirs):
        for md_file in sorted(category_dir.glob("*.md")):
            text = md_file.read_text()
            api_text = extract_api_reference(text)
            if not api_text:
                continue
            sections = parse_component_sections(api_text)
            for s in sections:
                s["category"] = category_dir.name
            manifest["components"].extend(sections)
    return manifest


if __name__ == "__main__":
    manifest = build_manifest()
    OUTPUT_PATH.write_text(json.dumps(manifest, indent=2))
    from collections import Counter

    by_category = Counter(c.get("category", "?") for c in manifest["components"])
    print(f"Parsed {len(manifest['components'])} component entries -> {OUTPUT_PATH}")
    for cat, count in sorted(by_category.items()):
        print(f"  {cat}: {count}")
