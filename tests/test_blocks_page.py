"""Regression guard for the /blocks showcase page (``native/pages/blocks.py``).

``BLOCK_GROUPS`` is a hardcoded allowlist that drives which block categories
are rendered on the showcase page. When a new block category is added under
``native/lib/blocks/`` but the matching ``BLOCK_GROUPS`` entry is forgotten,
the category is silently dropped from the page (no error, no missing-button
warning). This test asserts the allowlist stays in sync with what is on disk
so that drift is caught automatically — the original bug omitted ``line_chart``
while four ``line_chart_*.py`` files existed on disk.
"""

from __future__ import annotations

import re

from native.pages import blocks


def _disk_prefixes():
    """Block prefixes discoverable on disk, matching the loader's
    ``<prefix>_<digits>.py`` naming convention (excludes ``__init__.py``)."""
    prefixes = set()
    pattern = re.compile(r"^([a-z_]+)_(\d+)\.py$")
    for path in blocks.BLOCKS_PATH.glob("*.py"):
        match = pattern.match(path.name)
        if match:
            prefixes.add(match.group(1))
    return prefixes


def test_block_groups_match_block_prefixes_on_disk():
    """Every block prefix present on disk must be declared in
    ``BLOCK_GROUPS`` (and vice versa) so every block category is rendered on
    the showcase page."""
    assert _disk_prefixes() == {group[0] for group in blocks.BLOCK_GROUPS}
