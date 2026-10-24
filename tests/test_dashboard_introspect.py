"""Tests for native.registry.dashboard_introspect.

The introspect module powers the "Dependencies" badge row on the /dashboards
page: it walks each dashboard file's ``from X import Y`` statements, buckets
the imported names by module prefix via ``DEPENDENCY_BUCKETS``, and returns
``{"components": [...], "blocks": [...]}``.

Charts live under ``native/lib/charts/`` which the codebase consumes via the
Components surface (``native/pages/components.py``), while blocks live under
``native/lib/blocks/`` consumed via the Blocks surface. The bucket map
routes each lib prefix to the matching bucket. These tests lock in that
routing and the extractor's invariants so a chart import cannot silently
fall through to ``None`` again, and a bad bucket value cannot cause a silent
``KeyError`` with an empty deps map.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from native.registry.dashboard_introspect import (
    DEPENDENCY_BUCKETS,
    _classify_import,  # pyright: ignore[reportPrivateUsage]
    _extract_dependencies,  # pyright: ignore[reportPrivateUsage]
    load_dashboard_example,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DASHBOARDS_DIR = REPO_ROOT / "native" / "lib" / "dashboards"


def _read_dashboard_source(dashboard_id: str) -> str:
    return (DASHBOARDS_DIR / f"{dashboard_id}.py").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# DEPENDENCY_BUCKETS integrity
# ---------------------------------------------------------------------------


def test_dependency_buckets_only_use_known_bucket_names():
    """``_extract_dependencies`` initialises its deps dict with only the
    ``components`` and ``blocks`` keys; any bucket value in
    ``DEPENDENCY_BUCKETS`` must be one of those or the lookup would raise
    ``KeyError`` and silently drop the import."""
    assert set(DEPENDENCY_BUCKETS.values()) <= {"components", "blocks"}


# ---------------------------------------------------------------------------
# _classify_import
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(  # pyright: ignore[reportUntypedFunctionDecorator]
    "case",
    [
        # Charts route to components (the fix; previously returned None).
        ("native.lib.charts.area.v8", "components"),
        ("native.lib.charts.bar.v1", "components"),
        ("native.lib.charts.area.v8.sub", "components"),
        # No regression for the existing tracked prefixes.
        ("components.ui.avatar", "components"),
        ("components.core.hugeicon", "components"),
        ("native.lib.blocks.kpi_card_01", "blocks"),
        ("native.lib.blocks.bar_chart_02", "blocks"),
        # External / untracked modules still fall through to None.
        ("reflex", None),
        ("reflex_components_core.el", None),
    ],
    ids=lambda case: f"{case[0]}->{case[1]}",  # pyright: ignore[reportUnknownLambdaType]
)
def test_classify_import(case: tuple[str, str | None]):
    module_path, expected = case
    assert _classify_import(module_path) == expected


# ---------------------------------------------------------------------------
# _extract_dependencies (pure function; cwd-independent)
# ---------------------------------------------------------------------------


def test_extract_dependencies_buckets_mixed_imports():
    """Charts, blocks, UI/core components, and untracked externals are all
    classified together without cross-contamination."""
    source = (
        "import reflex as rx\n"
        "from components.ui.avatar import avatar\n"
        "from components.core.hugeicon import hi\n"
        "from native.lib.blocks.kpi_card_01 import kpi_card_01\n"
        "from native.lib.charts.area.v8 import area_chart_with_gradient\n"
        "from reflex_components_core.el import div\n"
    )
    assert _extract_dependencies(source) == {
        "components": ["avatar", "hi", "area_chart_with_gradient"],
        "blocks": ["kpi_card_01"],
    }


def test_extract_dependencies_dedupes_and_uses_asname():
    """The same imported name from two chart modules is recorded once, and
    ``from x import a as b`` records the alias ``b`` (mirrors the
    ``alias.asname or alias.name`` logic in the extractor)."""
    source = (
        "from native.lib.charts.area.v8 import area_chart_with_gradient\n"
        "from native.lib.charts.bar.v1 import area_chart_with_gradient\n"
        "from components.ui.avatar import avatar as av\n"
    )
    deps = _extract_dependencies(source)
    assert deps["components"] == ["area_chart_with_gradient", "av"]


def test_extract_dependencies_ignores_plain_import_statements():
    """``_extract_dependencies`` only inspects ``from ... import ...``
    (ast.ImportFrom); bare ``import X`` statements must not be bucketed."""
    source = (
        "import reflex\n"
        "import native.lib.charts.area.v8\n"
        "from native.lib.charts.area.v8 import area_chart_with_gradient\n"
    )
    assert _extract_dependencies(source) == {
        "components": ["area_chart_with_gradient"],
        "blocks": [],
    }


# ---------------------------------------------------------------------------
# Routing against the real dashboard files on disk
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("dashboard_id", ["dashboard_02", "dashboard_03"])  # pyright: ignore[reportUntypedFunctionDecorator]
def test_dashboards_02_03_chart_routes_to_components(dashboard_id: str):
    """``area_chart_with_gradient`` lives under ``native/lib/charts/`` and is
    the central rendered element of dashboards 02 and 03, so it must appear in
    their ``components`` bucket (the user-visible badge fix) and not in
    ``blocks``."""
    deps = _extract_dependencies(_read_dashboard_source(dashboard_id))
    assert "area_chart_with_gradient" in deps["components"], (
        f"{dashboard_id} should list area_chart_with_gradient under components"
    )
    assert "area_chart_with_gradient" not in deps["blocks"]


def test_dashboard_01_chart_stays_in_blocks_not_components():
    """``bar_chart_02`` lives under ``native/lib/blocks/``, so it remains in the
    ``blocks`` bucket even though charts now route to ``components``. Locks in
    the file-tree-derived asymmetric routing (each chart is bucketed by the lib
    directory it lives in) and guards against a too-broad charts prefix."""
    deps = _extract_dependencies(_read_dashboard_source("dashboard_01"))
    assert "bar_chart_02" in deps["blocks"]
    assert "bar_chart_02" not in deps["components"]
    assert "area_chart_with_gradient" not in deps["components"]
    assert "area_chart_with_gradient" not in deps["blocks"]


# ---------------------------------------------------------------------------
# Public API: load_dashboard_example (cwd-relative)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("dashboard_id", ["dashboard_02", "dashboard_03"])  # pyright: ignore[reportUntypedFunctionDecorator]
def test_load_dashboard_example_includes_chart_badge(dashboard_id: str, monkeypatch):
    """End-to-end guard for the user-visible defect: the public API consumed
    by ``native/templates/_dashboard_example.py`` must surface
    ``area_chart_with_gradient`` in ``components`` for the dashboards whose
    central element is that chart."""
    monkeypatch.chdir(REPO_ROOT)
    example = load_dashboard_example(dashboard_id)
    assert "area_chart_with_gradient" in example["dependencies"]["components"], (
        f"{dashboard_id} dependency badges must include area_chart_with_gradient"
    )
    assert "area_chart_with_gradient" not in example["dependencies"]["blocks"]
