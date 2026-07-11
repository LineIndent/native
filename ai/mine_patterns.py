"""
Mines native/lib/components/*.py demo files for REAL composition patterns —
which components tend to appear as direct children of which others. This
is how we teach the model idiom (field.label pairs with input, action
buttons go in *.footer) instead of just prop signatures, without having to
hand-write and maintain that list ourselves. As your demo library grows,
re-running this picks up new patterns automatically.
"""

import ast
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

LIBRARY_ROOT = Path(os.environ.get("COMPONENT_LIBRARY_ROOT", "."))
DEMOS_DIR = LIBRARY_ROOT / "native" / "lib" / "components"
OUTPUT_PATH = Path(__file__).parent / "patterns.json"

# Loaded lazily so this file has no hard dependency on the registry unless run directly
def _known_components() -> set[str]:
    from ai.registry import build_registry

    return set(build_registry().keys())


def _dotted_name(node: ast.AST) -> str | None:
    """Resolve a Call's func node to a dotted string like 'card.header', if possible."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted_name(node.value)
        return f"{base}.{node.attr}" if base else None
    return None


class CompositionVisitor(ast.NodeVisitor):
    """
    Walks the AST tracking Call nodes. Whenever a Call whose func resolves to
    a known component name appears as a positional argument of ANOTHER such
    call, that's a direct parent->child composition edge.
    """

    def __init__(self, known: set[str]):
        self.known = known
        self.edges: list[tuple[str, str]] = []  # (parent, child)

    def visit_Call(self, node: ast.Call):
        parent_name = _dotted_name(node.func)
        parent_known = parent_name in self.known

        for arg in node.args:
            if isinstance(arg, ast.Call):
                child_name = _dotted_name(arg.func)
                if parent_known and child_name in self.known:
                    self.edges.append((parent_name, child_name))

        # keyword args (e.g. class_name=...) aren't composition, skip those,
        # but still recurse into everything to find nested calls
        self.generic_visit(node)


def mine_patterns() -> dict:
    if not DEMOS_DIR.exists():
        raise FileNotFoundError(
            f"No native/lib/components/ directory found at {DEMOS_DIR.resolve()}.\n"
            f"Set COMPONENT_LIBRARY_ROOT to the root of your actual Reflex project."
        )

    known = _known_components()
    edge_counts: Counter[tuple[str, str]] = Counter()

    demo_files = sorted(DEMOS_DIR.glob("*.py"))
    for demo_file in demo_files:
        try:
            tree = ast.parse(demo_file.read_text())
        except SyntaxError:
            continue
        visitor = CompositionVisitor(known)
        visitor.visit(tree)
        edge_counts.update(visitor.edges)

    # For each child component, find its most common parent(s)
    child_to_parents: dict[str, Counter] = defaultdict(Counter)
    for (parent, child), count in edge_counts.items():
        child_to_parents[child][parent] += count

    patterns = []
    for child, parent_counts in sorted(child_to_parents.items()):
        total = sum(parent_counts.values())
        top_parent, top_count = parent_counts.most_common(1)[0]
        # Only surface patterns with enough signal to be worth stating as a rule
        if total >= 2 and top_count / total >= 0.6:
            patterns.append(
                {
                    "child": child,
                    "usual_parent": top_parent,
                    "confidence": round(top_count / total, 2),
                    "observed_count": total,
                }
            )

    return {"patterns": patterns, "demo_files_scanned": len(demo_files)}


if __name__ == "__main__":
    result = mine_patterns()
    OUTPUT_PATH.write_text(json.dumps(result, indent=2))
    print(f"Scanned {result['demo_files_scanned']} demo files.")
    print(f"Found {len(result['patterns'])} composition patterns:\n")
    for p in result["patterns"]:
        print(
            f"  {p['child']:25s} usually inside  {p['usual_parent']:20s} "
            f"(seen {p['observed_count']}x, {p['confidence']*100:.0f}% of the time)"
        )
