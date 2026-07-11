"""
Takes a JSON node tree (as the model would produce) and actually calls into
your real component library to build a live rx.Component tree. This is
"real" rendering, not just JSON-shape validation — if the model hallucinates
a component name or a prop that doesn't exist, this raises a genuine error
from your actual library, immediately, with a path to exactly where it
happened in the tree.

Expected node shape:
{
    "component": "card.root",       # dotted path into the registry
    "props": {"class_name": "..."}, # kwargs passed straight to the real fn
    "children": [ <node> | "some text string" ]
}
"""

from dataclasses import dataclass

from registry import build_registry


@dataclass
class RenderError:
    path: str
    message: str


class Renderer:
    def __init__(self):
        self.registry = build_registry()
        self.errors: list[RenderError] = []

    def render(self, node: dict, path: str = "root"):
        if isinstance(node, str):
            return node

        if not isinstance(node, dict) or "component" not in node:
            self.errors.append(
                RenderError(path, f"Expected a node with a 'component' key, got: {node!r}")
            )
            return None

        component_name = node["component"]
        props = node.get("props", {}) or {}
        children_specs = node.get("children", []) or []

        fn = self.registry.get(component_name)
        if fn is None:
            self.errors.append(
                RenderError(
                    path,
                    f"Unknown component '{component_name}'. "
                    f"Not present in the real component registry.",
                )
            )
            return None

        rendered_children = [
            self.render(child, f"{path} > {component_name}[{i}]")
            for i, child in enumerate(children_specs)
        ]
        rendered_children = [c for c in rendered_children if c is not None]

        try:
            return fn(*rendered_children, **props)
        except TypeError as e:
            # This is the payoff: a hallucinated prop or wrong arg shape
            # fails here, against your REAL function signature, not a
            # generic schema check.
            self.errors.append(
                RenderError(
                    path,
                    f"'{component_name}' rejected call — {e}",
                )
            )
            return None
        except Exception as e:
            self.errors.append(
                RenderError(path, f"'{component_name}' raised {type(e).__name__}: {e}")
            )
            return None

    def render_tree(self, tree: dict):
        self.errors = []
        result = self.render(tree)
        return result, self.errors
