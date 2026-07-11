"""
Terminal prototype: prompt -> JSON -> render, checked against your REAL
component library at every step.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...   (or OPENAI_API_KEY / GEMINI_API_KEY)
    python3 cli.py [anthropic|openai|gemini]
"""

import json
import sys

from llm_client import generate_ui_json, PROVIDER_FNS
from renderer import Renderer


def print_tree(node, indent=0):
    pad = "  " * indent
    if isinstance(node, str):
        print(f'{pad}"{node}"')
        return
    if not isinstance(node, dict):
        return
    props = node.get("props", {})
    props_str = f" {props}" if props else ""
    print(f"{pad}{node.get('component', '???')}{props_str}")
    for child in node.get("children", []):
        print_tree(child, indent + 1)


def main():
    provider = "anthropic"
    if len(sys.argv) > 1 and sys.argv[1] in PROVIDER_FNS:
        provider = sys.argv[1]

    renderer = Renderer()
    print(f"[provider: {provider}] Loaded {len(renderer.registry)} real components. Type a UI request (or 'quit').\n")

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input or user_input.lower() in ("quit", "exit"):
            break

        try:
            tree = generate_ui_json(user_input, provider=provider)
        except Exception as e:
            print(f"[generation failed] {e}\n")
            continue

        print("\n--- JSON tree ---")
        print(json.dumps(tree, indent=2))

        print("\n--- Tree structure ---")
        print_tree(tree)

        result, errors = renderer.render_tree(tree)

        if errors:
            print("\n--- Render errors ---")
            for e in errors:
                print(f"  [{e.path}] {e.message}")
        else:
            print("\n--- Rendered cleanly, zero errors ---")

        print()


if __name__ == "__main__":
    main()
