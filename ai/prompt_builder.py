"""
Turns manifest.json into the system prompt that grounds the model to your
actual component library. The core discipline here: the model is only ever
shown components/props that genuinely exist, and is told, explicitly and
repeatedly, not to invent anything outside that list.
"""

import json
from pathlib import Path

MANIFEST_PATH = Path(__file__).parent / "manifest.json"
PATTERNS_PATH = Path(__file__).parent / "patterns.json"

SCHEMA_BLOCK = """
Output a single JSON object (no markdown fences, no prose before or after)
matching this shape:

{
  "component": "<dotted path, e.g. 'card.root'>",
  "props": { "<prop_name>": <value>, ... },
  "children": [ <node>, ... ]   // each child is either another node object, or a plain string for text content
}

Rules:
- Use ONLY component names from the reference list below, spelled exactly as shown.
- Use ONLY prop names listed for that specific component. Do not invent props.
- If something the user asked for has no matching component in the list, either
  omit it or approximate it with plain text content — never invent a component name.
- Every node must have "component", "props" (can be {}), and "children" (can be []).
""".strip()

FEW_SHOT = """
Example request: "a button that says Save"
Example output:
{"component": "button", "props": {"variant": "default"}, "children": ["Save"]}

Example request: "a card with a title 'Team' and a description below it"
Example output:
{
  "component": "card.root",
  "props": {},
  "children": [
    {
      "component": "card.header",
      "props": {},
      "children": [
        {"component": "card.title", "props": {}, "children": ["Team"]},
        {"component": "card.description", "props": {}, "children": ["Manage who has access."]}
      ]
    }
  ]
}
""".strip()

# A few situational judgment calls that structural mining genuinely cannot
# derive — mining tells you WHERE a component usually nests, but not WHY,
# so it can't know "these two buttons together are terminal form actions,
# put them in the footer slot" the way it confidently knows "input usually
# goes in field.root." These stay hand-written and few in number on purpose;
# if this list grows large, that's a sign the mining threshold or demo
# coverage needs work instead of patching over it here.
GUIDELINES = """
- If a container has a *.footer slot (card.footer, dialog.footer, message.footer)
  and you're placing action buttons that conclude the section (Save, Cancel,
  Submit, Delete, Close), put them in that footer slot rather than the main
  content area — even if no example explicitly shows your exact combination.
- Form controls (input, textarea, select, checkbox.root) should be paired with
  a field.label via field.root, not left unlabeled, unless the user explicitly
  asks for a bare/unlabeled control.
""".strip()


def format_component_reference(manifest: dict) -> str:
    lines = []
    for entry in manifest["components"]:
        prop_strs = []
        for p in entry["props"]:
            type_str = p["type"].strip("`")
            prop_strs.append(f"{p['name']}: {type_str}")
        props_line = ", ".join(prop_strs) if prop_strs else "(no props)"
        desc = f" — {entry['description']}" if entry["description"] else ""
        lines.append(f"- {entry['component']}({props_line}){desc}")
    return "\n".join(lines)


def format_composition_patterns() -> str:
    if not PATTERNS_PATH.exists():
        return ""
    data = json.loads(PATTERNS_PATH.read_text())
    lines = []
    for p in data["patterns"]:
        lines.append(
            f"- {p['child']} is almost always placed inside {p['usual_parent']} "
            f"(observed in {p['observed_count']} real examples, "
            f"{p['confidence']*100:.0f}% consistent)"
        )
    return "\n".join(lines)


def build_system_prompt() -> str:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(
            f"manifest.json not found at {MANIFEST_PATH}. "
            f"Run build_manifest.py first (or make sure it shipped alongside this script)."
        )
    manifest = json.loads(MANIFEST_PATH.read_text())
    reference = format_component_reference(manifest)
    patterns = format_composition_patterns()
    patterns_block = (
        f"\n# Composition patterns (learned from real usage in this codebase)\n\n{patterns}\n"
        if patterns
        else ""
    )

    return f"""You are a UI layout generator for a specific Python/Reflex component library. \
You do not generate HTML, React, or generic markup — you generate a JSON tree that will be \
rendered using ONLY the components listed below.

{SCHEMA_BLOCK}

# Component reference

{reference}
{patterns_block}
# Additional guidelines

{GUIDELINES}

# Examples

{FEW_SHOT}

Now generate JSON for the user's request. Output ONLY the JSON object."""


if __name__ == "__main__":
    prompt = build_system_prompt()
    print(prompt)
    print(f"\n\n--- prompt length: {len(prompt)} chars (~{len(prompt)//4} tokens) ---")
