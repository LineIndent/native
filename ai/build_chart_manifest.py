"""
Chart docs have a genuinely different shape than component docs — frontmatter
title/description, then repeated `## Label` + `--DEMO(function_name)--` pairs,
with no props table at all (there's nothing to parameterize — see
chart_registry.py's docstring for why). This builds a manifest reflecting
that shape instead of forcing chart docs through the component parser, which
would just find no "# API Reference" section and silently produce nothing —
which is exactly the bug that started this.
"""

import json
import os
import re
from pathlib import Path

LIBRARY_ROOT = Path(os.environ.get("COMPONENT_LIBRARY_ROOT", "."))
CHARTS_DOCS_DIR = LIBRARY_ROOT / "docs" / "charts"
OUTPUT_PATH = Path(__file__).parent / "chart_manifest.json"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
FIELD_RE = re.compile(r'^(\w+):\s*"?(.*?)"?\s*$', re.MULTILINE)
VARIANT_RE = re.compile(r"^##\s+(.+?)\s*\n+--DEMO\((\w+)\)--", re.MULTILINE)


def parse_chart_doc(text: str) -> dict:
    fm_match = FRONTMATTER_RE.match(text)
    fields = {}
    if fm_match:
        for m in FIELD_RE.finditer(fm_match.group(1)):
            fields[m.group(1)] = m.group(2)

    variants = [
        {"label": label.strip(), "demo": demo.strip()}
        for label, demo in VARIANT_RE.findall(text)
    ]

    return {
        "title": fields.get("title", ""),
        "description": fields.get("description", ""),
        "variants": variants,
    }


def build_chart_manifest() -> dict:
    if not CHARTS_DOCS_DIR.exists():
        print(f"  [chart_manifest] no docs/charts/ found at {CHARTS_DOCS_DIR.resolve()}, skipping.")
        return {"charts": []}

    charts = []
    for md_file in sorted(CHARTS_DOCS_DIR.glob("*.md")):
        entry = parse_chart_doc(md_file.read_text())
        entry["file"] = md_file.stem
        if entry["variants"]:
            charts.append(entry)

    return {"charts": charts}


if __name__ == "__main__":
    manifest = build_chart_manifest()
    OUTPUT_PATH.write_text(json.dumps(manifest, indent=2))
    total_variants = sum(len(c["variants"]) for c in manifest["charts"])
    print(f"Parsed {len(manifest['charts'])} chart docs, {total_variants} variants -> {OUTPUT_PATH}")
    for c in manifest["charts"]:
        print(f"  {c['file']}: {[v['demo'] for v in c['variants']]}")
