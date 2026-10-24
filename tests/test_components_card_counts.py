import importlib
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UI = ROOT / "components/ui"
EX = ROOT / "native/lib/components"
DOCS = ROOT / "docs/components"

DEMO_RE = re.compile(r"--DEMO\([^)]*\)--")

EXPECTED_BUTTON_DEMOS = 12
EXPECTED_BUTTON_GROUP_DEMOS = 6
EXPECTED_INPUT_DEMOS = 6
EXPECTED_INPUT_GROUP_DEMOS = 9


def _demo_count(slug: str) -> int:
    md = DOCS / f"{slug.replace('-', '_')}.md"
    return len(DEMO_RE.findall(md.read_text()))


def _entries():
    from native.pages.components import get_component_entries

    return get_component_entries(UI, EX)


def _cards():
    return {slug: count for _, slug, count in _entries()}


def test_card_count_matches_detail_page_demos():
    cards = _cards()
    assert cards, "no component entries found (glob returned nothing)"
    mismatches = []
    for slug, count in cards.items():
        demos = _demo_count(slug)
        if count != demos:
            mismatches.append(f"{slug}: card={count} demos={demos}")
    assert not mismatches, "card counts disagree with detail-page demos:\n" + "\n".join(
        mismatches,
    )


def test_button_card_count_excludes_button_group():
    cards = _cards()
    assert cards["button"] == EXPECTED_BUTTON_DEMOS
    assert cards["button-group"] == EXPECTED_BUTTON_GROUP_DEMOS
    assert cards["button"] != EXPECTED_BUTTON_DEMOS + EXPECTED_BUTTON_GROUP_DEMOS


def test_input_card_count_excludes_input_group():
    cards = _cards()
    assert cards["input"] == EXPECTED_INPUT_DEMOS
    assert cards["input-group"] == EXPECTED_INPUT_GROUP_DEMOS
    assert cards["input"] != EXPECTED_INPUT_DEMOS + EXPECTED_INPUT_GROUP_DEMOS


def test_no_prefixed_sibling_double_counting():
    stems = sorted(p.stem for p in UI.glob("*.py") if p.stem != "__init__")
    cards = _cards()
    for a in stems:
        a_slug = a.replace("_", "-")
        siblings = [s for s in stems if s.startswith(f"{a}_")]
        a_only = sum(
            1
            for p in EX.glob(f"{a}_*.py")
            if not any(p.name.startswith(f"{s}_") for s in siblings)
        )
        assert cards[a_slug] == a_only, (
            f"{a} double-counts sibling files: card={cards[a_slug]} expected={a_only}"
        )
        for b in siblings:
            b_slug = b.replace("_", "-")
            b_files = list(EX.glob(f"{b}_*.py"))
            assert cards[b_slug] == len(b_files), (
                f"{b} card={cards[b_slug]} expected {len(b_files)}"
            )


def test_entries_sorted_by_name_case_insensitive():
    entries = _entries()
    names_lower = [name.lower() for name, _, _ in entries]
    assert names_lower == sorted(names_lower)


def test_get_links_returns_one_card_per_entry():
    from native.pages.components import get_links

    cards = get_links(UI, EX, "/docs/components")
    entries = _entries()
    assert len(cards) == len(entries)
    assert cards
    assert not isinstance(cards[0], tuple)


def test_module_component_links_nonempty_from_repo_root():
    import native.pages.components as page

    cwd = Path.cwd()
    os.chdir(ROOT)
    try:
        importlib.reload(page)
        assert len(page.component_links) > 0, (
            "module-level component_links is empty; import-time relative-path "
            "globs did not resolve from repo root (as `reflex run` does)"
        )
    finally:
        os.chdir(cwd)
