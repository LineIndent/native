import ast
import importlib
from pathlib import Path

DASHBOARDS_DIR = Path("native/lib/dashboards")

DEPENDENCY_BUCKETS = {
    "components.ui.": "components",
    "components.core.": "components",
    "native.lib.blocks.": "blocks",
}


def _classify_import(module_path: str) -> str | None:
    for prefix, bucket in DEPENDENCY_BUCKETS.items():
        if module_path.startswith(prefix):
            return bucket
    return None  # e.g. "reflex", "reflex_components_core.el" — not tracked


def _extract_dependencies(source: str) -> dict[str, list[str]]:
    """Walks `from X import a, b` statements and buckets the imported
    names (not the module path) by what X starts with. So:
        from components.ui.avatar import avatar   -> components: ["avatar"]
        from native.lib.blocks.kpi_card_01 import kpi_card_01
                                                    -> blocks: ["kpi_card_01"]
    """
    tree = ast.parse(source)
    deps: dict[str, list[str]] = {"components": [], "blocks": []}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            bucket = _classify_import(node.module)
            if bucket is None:
                continue
            for alias in node.names:
                name = alias.asname or alias.name
                if name not in deps[bucket]:
                    deps[bucket].append(name)
    return deps


def list_dashboard_ids() -> list[str]:
    """e.g. ["dashboard_01", "dashboard_02", ...] from files on disk."""
    return sorted(p.stem for p in DASHBOARDS_DIR.glob("dashboard_*.py"))


def load_dashboard_example(dashboard_id: str) -> dict:
    """dashboard_id="dashboard_01" -> reads
    native/lib/dashboards/dashboard_01.py, imports it, and grabs the
    top-level dashboard_01() function (same-name convention you're using)."""
    file_path = DASHBOARDS_DIR / f"{dashboard_id}.py"
    source = file_path.read_text()

    module = importlib.import_module(f"native.lib.dashboards.{dashboard_id}")
    component_fn = getattr(module, dashboard_id)

    return {
        "id": dashboard_id,
        "source": source,
        "component_fn": component_fn,
        "dependencies": _extract_dependencies(source),
    }
