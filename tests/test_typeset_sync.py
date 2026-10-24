"""Regression: /typeset on_mount must sync remounted selects to persisted state."""

import pathlib
import re

from native.pages.typeset import typeset_page

JS = (pathlib.Path(__file__).parent.parent / "assets" / "typeset-preview.js").read_text(
    encoding="utf-8",
)


def _on_mount_scripts() -> list[str]:
    chain = typeset_page().event_triggers["on_mount"]
    scripts = []
    for event in chain.events:
        for name_var, val_var in event.args:
            if getattr(name_var, "_js_expr", None) == "javascript_code":
                scripts.append(val_var._var_value)
                break
    return scripts


def test_on_mount_calls_sync_all() -> None:
    init = _on_mount_scripts()[0]
    assert "typesetPreview.syncAll()" in init
    assert "typesetPreview.applyAll()" not in init


def test_sync_all_exported_and_syncs_selects() -> None:
    assert re.search(r"window\.typesetPreview\s*=\s*\{[^}]*\bsyncAll:\s*syncAll", JS)
    body = re.search(r"function syncAll\(\)\s*\{(.*?)\n  \}", JS, re.S)
    assert body
    b = body.group(1)
    assert b.index("syncSelectsToState()") < b.index("applyAll()") < b.index("renderCodeBlocks()")
