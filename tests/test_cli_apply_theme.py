"""Regression tests for ``cli.main.cmd_apply`` theme-block replacement.

Bug (introduced in a61d7a4, "feature: buridan cli"): ``cmd_apply`` located the
region to replace by matching the first line whose stripped text starts with
the bare string ``":root {"`` and then rewrote the file as
``theme_css + everything_after_the_dark_block``. Two independent defects:

1. The rebuilt file dropped ``lines[0:start_line]``, silently discarding any
   user-authored CSS preceding the matched ``:root {`` line (including
   ``@import`` rules, which the CSS spec requires to precede all other
   rules, custom ``:root`` tokens, ``html { ... }`` blocks, comments).

2. ``":root {"`` cannot distinguish the CLI-generated theme block from any
   user-authored ``:root {`` block — top-level, one-line
   (``:root { --x: 1; }``), or nested inside an at-rule (``@media``). When
   the matched ``:root {`` was nested inside an at-rule, the brace-depth
   scanner started counting at the match line (not the top of the file) and
   could "close" the region at the inner block's ``}``, orphaning the
   at-rule's own closing brace and producing structurally invalid CSS.

The fix delimits the CLI-managed region with sentinel comments (mirroring
``cmd_init``'s utility sentinels) and replaces only the text between them on
re-apply; for files written by older CLIs (no sentinels) it conservatively
locates a top-level adjacent ``:root { ... }`` / ``.dark { ... }`` pair —
rejecting nested and one-line ``:root`` blocks — and replaces only that pair
while preserving the prefix and suffix; otherwise it prepends the new theme
and keeps all existing content intact. No user CSS is ever discarded.

Coverage:

* ``TestManagedThemeBlock`` — sentinel wrapping.
* ``TestJoinCssAroundTheme`` — prefix/theme/suffix join semantics.
* ``TestFindLegacyThemePair`` — the conservative legacy-region detector
  (top-level adjacency, depth-from-top, multi-line blocks only).
* ``TestSpliceThemeBlock`` — the three replacement strategies end-to-end on
  in-memory CSS strings (the four reproduction cases from the bug report).
* ``TestCmdApply`` — full ``cmd_apply`` runs against a temp Reflex project
  (``rxconfig.py`` + ``assets/globals.css``), asserting non-destructive
  re-apply, idempotency, manifest update, and the failure paths.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

import pytest

from cli.main import (
    THEME_END_SENTINEL,
    THEME_START_SENTINEL,
    cmd_apply,
    find_legacy_theme_pair,
    generate_theme_css,
    join_css_around_theme,
    managed_theme_block,
    splice_theme_block,
)

if TYPE_CHECKING:
    from pathlib import Path

PRESET = "b0"
PRESET_ALT = "b1000"


def _theme(preset: str = PRESET) -> str:
    return managed_theme_block(generate_theme_css(preset))


def _raw_theme(preset: str = PRESET) -> str:
    return generate_theme_css(preset)


def _legacy_cli_file(prefix: str = "", suffix: str = "", preset: str = PRESET) -> str:
    """Build a globals.css resembling pre-fix CLI output (no sentinels)."""
    raw = _raw_theme(preset)
    return join_css_around_theme(prefix, raw, suffix)


# ── managed_theme_block ──────────────────────────────────────────────────────


class TestManagedThemeBlock:
    def test_wraps_raw_theme_with_start_and_end_sentinels(self) -> None:
        raw = _raw_theme()
        wrapped = managed_theme_block(raw)
        assert wrapped.startswith(THEME_START_SENTINEL + "\n")
        assert wrapped.endswith("\n" + THEME_END_SENTINEL)
        assert raw in wrapped

    def test_sentinels_flank_raw_theme_on_their_own_lines(self) -> None:
        wrapped = managed_theme_block(
            ":root {\n    --x: 1;\n}\n\n.dark {\n    --x: 2;\n}",
        )
        lines = wrapped.splitlines()
        assert lines[0] == THEME_START_SENTINEL
        assert lines[-1] == THEME_END_SENTINEL
        assert lines[1] == ":root {"


# ── join_css_around_theme ─────────────────────────────────────────────────────


class TestJoinCssAroundTheme:
    def test_joins_all_three_sections_with_blank_line_separators(self) -> None:
        out = join_css_around_theme("@import url(x);", "THEME", ".foo { color: red; }")
        assert out == "@import url(x);\n\nTHEME\n\n.foo { color: red; }"

    def test_drops_empty_prefix(self) -> None:
        assert join_css_around_theme("", "THEME", "SUFFIX") == "THEME\n\nSUFFIX"

    def test_drops_empty_suffix(self) -> None:
        assert join_css_around_theme("PREFIX", "THEME", "") == "PREFIX\n\nTHEME"

    def test_drops_whitespace_only_sections(self) -> None:
        assert join_css_around_theme("\n   \n", "THEME", "\n\n") == "THEME"

    def test_strips_trailing_newlines_from_prefix_and_leading_from_suffix(self) -> None:
        out = join_css_around_theme("PREFIX\n\n\n", "THEME", "\n\nSUFFIX")
        assert out == "PREFIX\n\nTHEME\n\nSUFFIX"

    def test_theme_alone_when_no_user_css(self) -> None:
        assert join_css_around_theme("", "THEME", "") == "THEME"


# ── find_legacy_theme_pair ────────────────────────────────────────────────────


class TestFindLegacyThemePair:
    def test_top_level_adjacent_pair_returns_inclusive_range(self) -> None:
        css = _legacy_cli_file()
        lines = css.splitlines()
        pair = find_legacy_theme_pair(lines)
        assert pair is not None
        start, end = pair
        assert lines[start].strip() == ":root {"
        assert lines[end].strip() == "}"

    def test_pair_located_with_user_prefix(self) -> None:
        prefix = "/* keep me */\n@import url(fonts.css);\nhtml { --mine: 1; }"
        css = _legacy_cli_file(prefix=prefix)
        lines = css.splitlines()
        pair = find_legacy_theme_pair(lines)
        assert pair is not None
        start, _ = pair
        assert lines[start].strip() == ":root {"
        # prefix lines are strictly before the matched :root {
        assert "@import url(fonts.css);" in lines[:start]

    @pytest.mark.parametrize(  # pyright: ignore[reportUntypedFunctionDecorator]
        "one_liner",
        [
            ":root { --my-var: 1; }",
            ":root { --x: 1; --y: 2; }",
        ],
    )
    def test_one_line_root_block_is_skipped_as_region_start(
        self,
        one_liner: str,
    ) -> None:
        # The user's one-line :root precedes the CLI pair. The detector must
        # NOT match the one-liner; it must match the CLI's multi-line :root {.
        css = one_liner + "\n" + _raw_theme()
        lines = css.splitlines()
        pair = find_legacy_theme_pair(lines)
        assert pair is not None
        start, _ = pair
        assert lines[start].strip() == ":root {"
        assert lines[start].count("{") > lines[start].count("}")
        # the one-line user :root is preserved above the matched region
        assert one_liner in "\n".join(lines[:start])

    def test_nested_root_inside_media_is_rejected(self) -> None:
        css = (
            "@media (prefers-color-scheme: dark) {\n"
            "    :root {\n"
            "        --custom: 2;\n"
            "    }\n"
            "}\n"
        )
        assert find_legacy_theme_pair(css.splitlines()) is None

    def test_standalone_root_without_dark_is_rejected(self) -> None:
        css = ":root {\n    --mine: hotpink;\n}\n\n.custom { color: red; }"
        assert find_legacy_theme_pair(css.splitlines()) is None

    def test_standalone_dark_without_root_is_rejected(self) -> None:
        css = ".dark {\n    --mine: hotpink;\n}\n\n.custom { color: red; }"
        assert find_legacy_theme_pair(css.splitlines()) is None

    def test_non_adjacent_root_and_dark_are_rejected(self) -> None:
        # Content between the :root block and .dark block breaks adjacency,
        # so this is not recognized as a CLI-managed pair.
        css = (
            ":root {\n    --a: 1;\n}\n\n"
            "/* user comment in between */\n"
            ".dark {\n    --a: 2;\n}\n"
        )
        assert find_legacy_theme_pair(css.splitlines()) is None

    def test_blank_lines_between_root_and_dark_are_allowed(self) -> None:
        css = ":root {\n    --a: 1;\n}\n\n\n.dark {\n    --a: 2;\n}\n"
        pair = find_legacy_theme_pair(css.splitlines())
        assert pair is not None

    def test_no_root_block_returns_none(self) -> None:
        css = "/* just a comment */\n.custom { color: red; }"
        assert find_legacy_theme_pair(css.splitlines()) is None

    def test_unclosed_root_block_returns_none(self) -> None:
        css = ":root {\n    --a: 1;\n"  # missing closing brace
        assert find_legacy_theme_pair(css.splitlines()) is None

    def test_skips_user_standalone_root_and_finds_later_cli_pair(self) -> None:
        # A user's standalone (multi-line) :root with no .dark must not be
        # mistaken for the CLI region. Scanning must continue and locate
        # the later :root + .dark CLI pair, so the user's block ends up in
        # the prefix (preserved) rather than being overwritten.
        user_root = ":root {\n    --mine: hotpink;\n}"
        css = user_root + "\n\n" + _raw_theme()
        lines = css.splitlines()
        pair = find_legacy_theme_pair(lines)
        assert pair is not None
        start, _ = pair
        # the matched region is the CLI pair, NOT the user's block
        assert lines[start].strip() == ":root {"
        assert start > 1
        assert "--mine: hotpink;" in "\n".join(lines[:start])


# ── splice_theme_block ────────────────────────────────────────────────────────


class TestSpliceThemeBlock:
    def test_sentinel_path_replaces_between_sentinels_preserving_prefix_suffix(
        self,
    ) -> None:
        prefix = '/* mine */\n@import url("https://fonts.example.com/font.css");'
        suffix = ".custom-util {\n    color: red;\n}"
        current = join_css_around_theme(prefix, _theme(), suffix)
        new_theme = _theme(PRESET_ALT)
        out = splice_theme_block(current, new_theme)
        # prefix and suffix are byte-for-byte preserved
        assert out.startswith(prefix + "\n\n")
        assert out.endswith("\n\n" + suffix)
        # the new (alt) theme is between the sentinels, not the old one
        assert THEME_START_SENTINEL in out and THEME_END_SENTINEL in out
        assert generate_theme_css(PRESET_ALT) in out
        assert generate_theme_css(PRESET) not in out
        # exactly one managed region
        assert out.count(THEME_START_SENTINEL) == 1
        assert out.count(THEME_END_SENTINEL) == 1

    def test_sentinel_path_preserves_user_root_block_before_theme(self) -> None:
        user_root = ":root { --my-custom-token: hotpink; }"
        current = join_css_around_theme(user_root, _theme(), ".x { color: red; }")
        out = splice_theme_block(current, _theme(PRESET_ALT))
        assert user_root in out
        assert out.index(user_root) < out.index(THEME_START_SENTINEL)

    def test_sentinel_path_idempotent_when_theme_unchanged(self) -> None:
        current = join_css_around_theme("@import url(x);", _theme(), ".x{color:red}")
        out = splice_theme_block(current, _theme())
        assert out == current

    def test_legacy_path_replaces_pair_preserving_prefix_and_suffix(self) -> None:
        prefix = (
            "/* keep */\n"
            '@import url("https://fonts.example.com/font.css");\n'
            "html { --my-var: 1; }"
        )
        suffix = ".custom-util {\n    color: red;\n}"
        current = _legacy_cli_file(prefix=prefix, suffix=suffix)
        out = splice_theme_block(current, _theme(PRESET_ALT))
        # the bug: prefix used to be dropped. Now it must survive intact.
        assert '@import url("https://fonts.example.com/font.css");' in out
        assert "html { --my-var: 1; }" in out
        assert "/* keep */" in out
        # suffix survives too
        assert ".custom-util {" in out and "color: red;" in out
        # the legacy pair is replaced by the new managed (sentinel'd) theme
        assert THEME_START_SENTINEL in out
        assert generate_theme_css(PRESET_ALT) in out
        # exactly one :root { at top level now (the new theme's)
        assert out.count(":root {") == 1
        # @import remains before the theme block (CSS spec ordering preserved)
        assert out.index("@import") < out.index(THEME_START_SENTINEL)

    def test_legacy_path_preserves_one_line_user_root_in_prefix(self) -> None:
        user_root = ":root { --my-var: 1; }"
        current = user_root + "\n" + _legacy_cli_file()
        out = splice_theme_block(current, _theme(PRESET_ALT))
        # the bug: this one-liner was deleted. Now it must survive in the prefix.
        assert user_root in out
        assert out.index(user_root) < out.index(THEME_START_SENTINEL)

    def test_legacy_path_preserves_multi_line_user_root_in_prefix(self) -> None:
        user_root = ":root {\n    --my-custom-token: hotpink;\n}"
        current = user_root + "\n" + _legacy_cli_file(suffix=".x{color:red}")
        out = splice_theme_block(current, _theme(PRESET_ALT))
        assert "--my-custom-token: hotpink;" in out
        assert out.index("--my-custom-token") < out.index(THEME_START_SENTINEL)
        assert ".x{color:red}" in out

    def test_fallback_prepends_theme_when_no_safe_match_nested_media(self) -> None:
        # The bug-report case that produced structurally invalid CSS:
        # a :root nested inside @media (no CLI .dark present). The fix must
        # prepend the new theme and leave the @media block intact, with no
        # orphaned brace.
        media = (
            "@media (prefers-color-scheme: dark) {\n"
            "    :root {\n"
            "        --custom: 2;\n"
            "    }\n"
            "}\n"
        )
        out = splice_theme_block(media, _theme())
        # the @media block is preserved verbatim (no destruction)
        assert "--custom: 2;" in out
        assert "@media (prefers-color-scheme: dark) {" in out
        # the new managed theme is present
        assert THEME_START_SENTINEL in out
        # the new theme is prepended before the user's @media
        assert out.index(THEME_START_SENTINEL) < out.index("@media")
        # the output is structurally valid CSS: balanced braces
        assert out.count("{") == out.count("}"), (
            f"unbalanced braces in output: {out.count('{')} {{ vs {out.count('}')} }}"
        )

    def test_fallback_prepends_theme_for_unrelated_css(self) -> None:
        current = "/* just a comment and a rule */\n.foo { color: red; }"
        out = splice_theme_block(current, _theme())
        assert THEME_START_SENTINEL in out
        assert "/* just a comment and a rule */" in out
        assert ".foo { color: red; }" in out
        # theme is prepended (before the user content)
        assert out.index(THEME_START_SENTINEL) < out.index("/* just")

    def test_fallback_preserves_empty_file_as_just_theme(self) -> None:
        out = splice_theme_block("", _theme())
        assert out == _theme()

    def test_fallback_preserves_whitespace_only_file_as_just_theme(self) -> None:
        out = splice_theme_block("\n   \n\n", _theme())
        assert out == _theme()

    def test_no_double_sentinel_on_repeated_splices(self) -> None:
        current = _legacy_cli_file(prefix="@import url(x);", suffix=".x{color:red}")
        once = splice_theme_block(current, _theme())
        twice = splice_theme_block(once, _theme(PRESET_ALT))
        assert twice.count(THEME_START_SENTINEL) == 1
        assert twice.count(THEME_END_SENTINEL) == 1
        # prefix and suffix survive two successive splices
        assert "@import url(x);" in twice
        assert ".x{color:red}" in twice

    def test_sentinel_end_before_start_falls_through_safely(self) -> None:
        # A corrupted file with the end sentinel before the start sentinel must
        # not crash (ValueError from str.index); it falls through to the
        # non-destructive fallback that prepends the new theme.
        current = (
            f"{THEME_END_SENTINEL}\n.x {{ color: red; }}\n{THEME_START_SENTINEL}\n"
            ":root { --old: 1; }\n"
        )
        out = splice_theme_block(current, _theme())
        # the new managed theme is present
        assert THEME_START_SENTINEL in out
        assert THEME_END_SENTINEL in out
        # the user CSS survives (non-destructive fallback)
        assert ".x { color: red; }" in out

    def test_sentinel_start_without_end_falls_through_safely(self) -> None:
        # A file with only the start sentinel (end missing) must not crash and
        # must fall through to the non-destructive fallback.
        current = f"{THEME_START_SENTINEL}\n:root {{ --old: 1; }}\n.x {{ color: red; }}"
        out = splice_theme_block(current, _theme())
        assert THEME_START_SENTINEL in out
        assert THEME_END_SENTINEL in out
        assert ".x { color: red; }" in out


# ── cmd_apply (end-to-end against a temp Reflex project) ──────────────────────


@pytest.fixture  # pyright: ignore[reportUntypedFunctionDecorator]
def project_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A minimal Reflex project root the CLI accepts (just rxconfig.py)."""
    (tmp_path / "rxconfig.py").write_text("import reflex as rx\napp = rx.App()\n")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def _globals(project: Path) -> str:
    return (project / "assets" / "globals.css").read_text()


def _manifest(project: Path) -> dict[str, Any]:
    return json.loads((project / "components.json").read_text())


class TestCmdApply:
    def test_first_apply_creates_sentinelled_theme(self, project_dir: Path) -> None:
        cmd_apply(PRESET)
        css = _globals(project_dir)
        assert THEME_START_SENTINEL in css
        assert THEME_END_SENTINEL in css
        assert ":root {" in css and ".dark {" in css
        # exactly one managed region
        assert css.count(THEME_START_SENTINEL) == 1

    def test_first_apply_on_empty_existing_file(self, project_dir: Path) -> None:
        (project_dir / "assets").mkdir(exist_ok=True)
        (project_dir / "assets" / "globals.css").write_text("")
        cmd_apply(PRESET)
        css = _globals(project_dir)
        assert THEME_START_SENTINEL in css
        # an empty file should yield just the theme, no leading blank lines
        assert css.startswith(THEME_START_SENTINEL)

    def test_re_apply_preserves_user_css_before_theme(self, project_dir: Path) -> None:
        # The headline bug: user CSS placed *before* the theme block used to
        # be silently discarded on re-apply. It must now survive intact.
        prefix = (
            "/* keep me */\n"
            '@import url("https://fonts.example.com/font.css");\n'
            "html { --my-var: 1; }"
        )
        assets = project_dir / "assets"
        assets.mkdir(exist_ok=True)
        (assets / "globals.css").write_text(join_css_around_theme(prefix, _theme(), ""))
        cmd_apply(PRESET_ALT)
        css = _globals(project_dir)
        assert "/* keep me */" in css
        assert '@import url("https://fonts.example.com/font.css");' in css
        assert "html { --my-var: 1; }" in css
        # the @import still precedes the theme (CSS spec ordering preserved)
        assert css.index("@import") < css.index(THEME_START_SENTINEL)
        # the new (alt) theme replaced the old one
        assert generate_theme_css(PRESET_ALT) in css
        assert generate_theme_css(PRESET) not in css

    def test_re_apply_preserves_user_root_block_before_theme(
        self,
        project_dir: Path,
    ) -> None:
        user_root = ":root { --my-custom-token: hotpink; }"
        assets = project_dir / "assets"
        assets.mkdir(exist_ok=True)
        (assets / "globals.css").write_text(
            join_css_around_theme(user_root, _theme(), ".x { color: red; }"),
        )
        cmd_apply(PRESET_ALT)
        css = _globals(project_dir)
        assert "--my-custom-token: hotpink;" in css
        assert ".x { color: red; }" in css
        assert css.index("--my-custom-token") < css.index(THEME_START_SENTINEL)
        # exactly one managed region; the user's one-line :root survives in
        # the prefix, so ":root {" legitimately appears twice (user + theme).
        assert css.count(THEME_START_SENTINEL) == 1
        assert css.count(THEME_END_SENTINEL) == 1

    def test_re_apply_on_legacy_cli_output_preserves_prefix(
        self,
        project_dir: Path,
    ) -> None:
        # Backwards compat: a globals.css written by an older CLI (no
        # sentinels) must have only its :root/.dark pair replaced, with the
        # prefix and suffix preserved.
        prefix = "/* keep */\n@import url(x);"
        suffix = ".custom-util {\n    color: red;\n}"
        assets = project_dir / "assets"
        assets.mkdir(exist_ok=True)
        (assets / "globals.css").write_text(
            _legacy_cli_file(prefix=prefix, suffix=suffix),
        )
        cmd_apply(PRESET_ALT)
        css = _globals(project_dir)
        assert "/* keep */" in css
        assert "@import url(x);" in css
        assert ".custom-util {" in css
        assert "color: red;" in css
        assert THEME_START_SENTINEL in css
        assert generate_theme_css(PRESET_ALT) in css
        # exactly one :root { at top level (the new theme's); the old pair
        # is gone, the prefix's other rules survive
        assert css.count(":root {") == 1

    def test_apply_on_nested_media_root_does_not_corrupt_css(
        self,
        project_dir: Path,
    ) -> None:
        # The bug-report case that produced structurally invalid CSS with an
        # orphaned closing brace. The fix must keep the @media block intact
        # and emit balanced braces.
        media = (
            "@media (prefers-color-scheme: dark) {\n"
            "    :root {\n"
            "        --custom: 2;\n"
            "    }\n"
            "}\n"
        )
        assets = project_dir / "assets"
        assets.mkdir(exist_ok=True)
        (assets / "globals.css").write_text(media)
        cmd_apply(PRESET)
        css = _globals(project_dir)
        assert "--custom: 2;" in css
        assert "@media (prefers-color-scheme: dark) {" in css
        assert THEME_START_SENTINEL in css
        assert css.count("{") == css.count("}"), "orphaned brace in output"

    def test_apply_is_idempotent(self, project_dir: Path) -> None:
        cmd_apply(PRESET)
        once = _globals(project_dir)
        cmd_apply(PRESET)
        twice = _globals(project_dir)
        assert once == twice

    def test_apply_preserves_user_suffix_css(self, project_dir: Path) -> None:
        # Baseline happy path (the only case the old code handled): user CSS
        # *after* the theme block must still survive a re-apply.
        suffix = ".my-util {\n    color: rebeccapurple;\n}"
        assets = project_dir / "assets"
        assets.mkdir(exist_ok=True)
        (assets / "globals.css").write_text(join_css_around_theme("", _theme(), suffix))
        cmd_apply(PRESET_ALT)
        css = _globals(project_dir)
        assert ".my-util {" in css
        assert "color: rebeccapurple;" in css

    def test_apply_updates_manifest_theme(self, project_dir: Path) -> None:
        cmd_apply(PRESET)
        manifest = _manifest(project_dir)
        assert manifest["theme"]["preset"] == PRESET

    def test_apply_then_re_apply_updates_manifest_preset(
        self,
        project_dir: Path,
    ) -> None:
        cmd_apply(PRESET)
        cmd_apply(PRESET_ALT)
        manifest = _manifest(project_dir)
        assert manifest["theme"]["preset"] == PRESET_ALT
        # components section is untouched (no components installed here)
        assert manifest["components"] == {}

    def test_apply_creates_assets_dir_if_missing(self, project_dir: Path) -> None:
        assert not (project_dir / "assets").exists()
        cmd_apply(PRESET)
        assert (project_dir / "assets" / "globals.css").exists()

    def test_missing_rxconfig_exits_nonzero(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.chdir(tmp_path)
        with pytest.raises(SystemExit) as exc:
            cmd_apply(PRESET)
        assert exc.value.code == 1
        assert not (tmp_path / "assets" / "globals.css").exists()

    def test_invalid_preset_exits_nonzero(self, project_dir: Path) -> None:
        with pytest.raises(SystemExit) as exc:
            cmd_apply("definitely-not-a-real-preset")
        assert exc.value.code == 1
        # did not create or alter globals.css
        assert not (project_dir / "assets" / "globals.css").exists()

    def test_init_then_apply_workflow_non_destructive(self, project_dir: Path) -> None:
        # The supported CLI workflow: `buridan init` writes utility CSS, then
        # `buridan apply` prepends the theme above it, and re-apply keeps the
        # utilities intact.
        from cli.main import cmd_init

        cmd_init()
        after_init = _globals(project_dir)
        assert "Shimmer utility" in after_init
        assert "Scrollbar utilities" in after_init

        cmd_apply(PRESET)
        after_apply = _globals(project_dir)
        # utilities survive the apply
        assert "Shimmer utility" in after_apply
        assert "Scrollbar utilities" in after_apply
        # theme is present and above the utilities
        assert THEME_START_SENTINEL in after_apply
        assert after_apply.index(THEME_START_SENTINEL) < after_apply.index(
            "Shimmer utility",
        )

        cmd_apply(PRESET_ALT)
        after_re_apply = _globals(project_dir)
        assert "Shimmer utility" in after_re_apply
        assert "Scrollbar utilities" in after_re_apply
        assert generate_theme_css(PRESET_ALT) in after_re_apply
        assert generate_theme_css(PRESET) not in after_re_apply
