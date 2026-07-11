"""
Charts are NOT parameterized components like card/button — each demo
function (e.g. area_chart_basic_type) is a complete, bespoke composition,
mostly built from Reflex's own rx.recharts.* primitives, with only
chart_tooltip/chart_tooltip_content coming from your actual library. There's
no prop surface to expose — the whole function IS the reusable unit. So
charts get looked up and called wholesale, with zero args, rather than
reconstructed prop-by-prop the way regular components are.

Unlike components/ui/*.py, chart demo files don't follow the "module name
== exported variable name" convention (v1.py defines area_chart_basic_type,
not something called v1) — so this scans every top-level function actually
DEFINED in each module (not imported into it) and registers it by its real
function name.
"""

import importlib.util
import os
import sys
from pathlib import Path

LIBRARY_ROOT = Path(os.environ.get("COMPONENT_LIBRARY_ROOT", "."))
CHARTS_DIR = LIBRARY_ROOT / "native" / "lib" / "charts"

if str(LIBRARY_ROOT) not in sys.path:
    sys.path.insert(0, str(LIBRARY_ROOT))


def build_chart_registry() -> dict:
    if not CHARTS_DIR.exists():
        print(f"  [chart_registry] no native/lib/charts/ found at {CHARTS_DIR.resolve()}, skipping.")
        return {}

    registry = {}
    chart_files = sorted(p for p in CHARTS_DIR.rglob("*.py") if "__pycache__" not in p.parts)

    for py_file in chart_files:
        # e.g. native/lib/charts/area/v1.py -> module path "native.lib.charts.area.v1"
        rel = py_file.relative_to(LIBRARY_ROOT).with_suffix("")
        module_path = ".".join(rel.parts)
        try:
            module = importlib.import_module(module_path)
        except Exception as e:
            print(f"  [chart_registry] skipping {module_path}: {e}")
            continue

        for name, obj in vars(module).items():
            if (
                callable(obj)
                and getattr(obj, "__module__", None) == module.__name__
                and not name.startswith("_")
            ):
                registry[name] = obj

    if not registry and CHARTS_DIR.exists():
        print(
            f"  [chart_registry] WARNING: found {CHARTS_DIR} but registered "
            f"zero chart functions — check the skip messages above."
        )

    return registry


if __name__ == "__main__":
    registry = build_chart_registry()
    print(f"Registered {len(registry)} chart functions:\n")
    for name in sorted(registry):
        print(f"  {name}")
