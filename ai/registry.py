"""
Builds a registry mapping dotted component-path strings (as they'll appear
in the model's JSON output, e.g. "card.root", "button") to the *actual*
callables in your component library. This is what makes rendering "real"
instead of just JSON-shape validation — we're calling your real
avatar.root(), card.content(), etc., so a hallucinated prop fails with a
genuine Python error immediately.
"""

import importlib
import os
import sys
from pathlib import Path

from reflex.components.component import ComponentNamespace

# This MUST point at the root of YOUR actual Reflex project — the directory
# that directly contains your real `components/` package. It is NOT meant
# to be a bundled copy; the whole point is that this always reflects your
# live source, so edits to your components show up here with zero syncing.
#
# Override with an env var rather than editing this file every time:
#   export COMPONENT_LIBRARY_ROOT=/path/to/your/reflex/project
LIBRARY_ROOT = Path(os.environ.get("COMPONENT_LIBRARY_ROOT", "."))
COMPONENTS_DIR = LIBRARY_ROOT / "components"

if str(LIBRARY_ROOT) not in sys.path:
    sys.path.insert(0, str(LIBRARY_ROOT))


def build_registry() -> dict:
    if not COMPONENTS_DIR.exists():
        raise FileNotFoundError(
            f"No components/ directory found at {COMPONENTS_DIR.resolve()}.\n"
            f"Set COMPONENT_LIBRARY_ROOT to the root of your actual Reflex "
            f"project (the directory containing your real components/ "
            f"package), e.g.:\n"
            f"  export COMPONENT_LIBRARY_ROOT=/path/to/your/project"
        )

    registry = {}
    category_dirs = [
        d for d in COMPONENTS_DIR.iterdir()
        if d.is_dir() and d.name != "core" and not d.name.startswith(("_", "."))
    ]
    for category_dir in sorted(category_dirs):
        for py_file in sorted(category_dir.glob("*.py")):
            module_name = py_file.stem
            if module_name.startswith("_"):
                continue
            try:
                module = importlib.import_module(
                    f"components.{category_dir.name}.{module_name}"
                )
            except Exception as e:
                print(f"  [registry] skipping {category_dir.name}.{module_name}: {e}")
                continue

            exported = getattr(module, module_name, None)
            if exported is None:
                continue

            if isinstance(exported, ComponentNamespace):
                # Genuine namespace, e.g. card.py -> card.root / card.header /
                # etc. Only these get sub-attribute enumeration — walking dir()
                # on a plain component instance instead picks up unrelated
                # Reflex internals (Var descriptors like "class_name") that
                # aren't real sub-components.
                for attr_name in vars(type(exported)):
                    if attr_name.startswith("_") or attr_name in ("class_names", "class_name"):
                        continue
                    attr = getattr(exported, attr_name)
                    if callable(attr):
                        registry[f"{module_name}.{attr_name}"] = attr
                if callable(exported):
                    # Some namespaces are ALSO directly callable, e.g. select
                    # (NativeSelect.__call__) — register the bare name too.
                    registry[module_name] = exported
            elif callable(exported):
                # Plain directly-callable component, e.g. button(...), input(...)
                registry[module_name] = exported

    if not registry:
        print(
            f"  [registry] WARNING: found {COMPONENTS_DIR} but registered zero "
            f"components. Check the per-module skip messages above — your "
            f"real components/**/*.py files likely failed to import (a "
            f"missing dependency, a broken relative import, etc.)."
        )

    return registry


if __name__ == "__main__":
    registry = build_registry()
    print(f"Registered {len(registry)} component paths:\n")
    for name in sorted(registry):
        print(f"  {name}")
