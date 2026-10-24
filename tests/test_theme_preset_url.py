# ruff: noqa: INP001
"""Regression tests for the /create theme-customizer's first-load ``?preset=<code>``
URL round-trip.

Bug (introduced in a7c0cdb): ``create_page``'s ``on_mount`` unconditionally called
``window.preview.syncAll()``, which seeds registry-default state and rewrites
``?preset=`` to ``"b0"``, silently clobbering any incoming non-default preset
code. The fix reads ``?preset=`` from ``window.location.search`` and routes
through ``window.preview.applyPresetCode(code)`` when present/valid, falling
back to ``window.preview.syncAll()`` otherwise.

What is covered, and why this is the best available coverage:

* ``TestCreatePageOnMountScript`` renders ``create_page()`` and asserts the
  emitted ``on_mount`` JS: populates ``__THEME_REGISTRIES__``, reads
  ``?preset=`` via ``URLSearchParams(...).get("preset")``, calls
  ``applyPresetCode(code)``, falls back to ``syncAll()`` for missing/invalid
  codes, and does NOT use a top-level ``return`` (which would be a swallowed
  ``SyntaxError`` under Reflex's top-level ``eval`` of the script body).

* ``TestThemePreviewSurface`` adds static-source guards on
  ``assets/theme-preview.js`` for the public surface the fix depends on
  (the repo has no JS test runner, so these are the only automated guards
  for the JS side).

* ``TestPresetCodecInterop`` locks the Python codec
  (``cli/preset_codec.decode_seed``, the port of ``theme-preview.js`` used by
  the CLI's ``--preset <ID>``) to the same bit layout as the JS: the
  documented example codes decode the same way, invalid codes are rejected,
  and every index dimension round-trips.
"""

import pathlib
import re
from typing import Any

import pytest  # pyrefly: ignore

import native.pages.create as create_module
from cli.preset_codec import DEFAULT_PRESET_CODE, decode_seed
from native.registry.colors import COLOR_THEMES
from native.registry.fonts import FONT_REGISTRY
from native.registry.radii import RADII_OPTIONS
from native.registry.styles import STYLE_REGISTRY
from native.registry.themes import BASE_THEMES

ROOT_DIR = pathlib.Path(__file__).parent.parent
THEME_PREVIEW_JS = ROOT_DIR / "assets" / "theme-preview.js"

_REGISTRY = {
    "base": BASE_THEMES,
    "color": COLOR_THEMES,
    "style": STYLE_REGISTRY,
    "radii": RADII_OPTIONS,
    "font": FONT_REGISTRY,
}

_MIN_ON_MOUNT_SCRIPTS = 2


def _decode(code: str) -> dict[str, object] | None:
    return decode_seed(
        code,
        _REGISTRY["base"],
        _REGISTRY["color"],
        _REGISTRY["style"],
        _REGISTRY["radii"],
        _REGISTRY["font"],
    )


def _on_mount_scripts(component: Any) -> list[str]:  # noqa: ANN401
    assert "on_mount" in component.event_triggers, (
        "create_page() must wire an on_mount lifecycle hook"
    )
    chain = component.event_triggers["on_mount"]
    scripts: list[str] = []
    for event in chain.events:
        for name_var, val_var in event.args:
            if getattr(name_var, "_js_expr", None) == "javascript_code":
                scripts.append(val_var._var_value)  # noqa: SLF001
                break
    return scripts


_CREATE_SCRIPTS = _on_mount_scripts(create_module.create_page())
_INIT_SCRIPT = _CREATE_SCRIPTS[0]
_JS = THEME_PREVIEW_JS.read_text(encoding="utf-8")


class TestCreatePageOnMountScript:
    def test_registries_are_populated_before_url_read(self) -> None:
        assert "__THEME_REGISTRIES__" in _INIT_SCRIPT
        for key in ("base:", "color:", "radius:", "style:", "font:"):
            assert key in _INIT_SCRIPT, f"registry key {key!r} missing from on_mount"
        assert "URLSearchParams" in _INIT_SCRIPT
        assert _INIT_SCRIPT.index("__THEME_REGISTRIES__") < _INIT_SCRIPT.index(
            "URLSearchParams",
        ), "registries must be populated before reading ?preset="

    def test_reads_preset_from_url_search_params(self) -> None:
        assert re.search(
            r'URLSearchParams\s*\(\s*window\.location\.search\s*\)\.get\s*\(\s*"preset"\s*\)',
            _INIT_SCRIPT,
        ), 'on_mount must read ?preset= via URLSearchParams(...).get("preset")'

    def test_routes_valid_url_code_through_apply_preset_code(self) -> None:
        assert "applyPresetCode" in _INIT_SCRIPT
        assert re.search(
            r"applyPresetCode\s*\(\s*code\s*\)",
            _INIT_SCRIPT,
        ), "on_mount must apply the URL code via window.preview.applyPresetCode(code)"

    def test_falls_back_to_sync_all_for_missing_or_invalid(self) -> None:
        assert re.search(r"syncAll\s*\(\s*\)", _INIT_SCRIPT), (
            "on_mount must call window.preview.syncAll() when no valid URL code present"
        )

    def test_no_top_level_return_after_apply_preset_code(self) -> None:
        # rx.call_script runs the body via top-level eval (no IIFE wrap), so a
        # bare `return;` is a SyntaxError silently swallowed by Reflex's
        # try/catch and the rest of the script never runs. The
        # `applyPresetCode(code)) return` shape looks correct but is broken
        # here; the fix must use if/else instead.
        assert not re.search(
            r"applyPresetCode\s*\([^)]*\)\)\s*return\b",
            _INIT_SCRIPT,
        ), "on_mount must use if/else, not a top-level `return` after applyPresetCode"

    def test_does_not_unconditionally_sync_all_ignoring_url(self) -> None:
        bad = re.search(
            r"__THEME_REGISTRIES__\s*=\s*\{[\s\S]*?\};\s*"
            r"if\s*\(window\.preview\)\s*window\.preview\.syncAll\s*\(\s*\)\s*;",
            _INIT_SCRIPT,
        )
        assert bad is None, (
            "on_mount must not clobber incoming ?preset= via an unconditional syncAll()"
        )

    def test_prism_highlight_remains_wired(self) -> None:
        assert len(_CREATE_SCRIPTS) >= _MIN_ON_MOUNT_SCRIPTS, (
            "second on_mount script (Prism.highlightAll) was dropped"
        )
        assert "Prism.highlightAll" in _CREATE_SCRIPTS[1]


class TestThemePreviewSurface:
    def test_apply_preset_code_defined_with_boolean_contract(self) -> None:
        m = re.search(
            r"applyPresetCode:\s*function\s*\(\s*code\s*\)\s*\{([\s\S]*?)return\s+true\s*;",
            _JS,
        )
        assert m, (
            "window.preview.applyPresetCode must be defined, returning true on success"
        )
        body = m.group(1)
        assert "applyCodeToState" in body
        assert "syncSelectsToState" in body
        assert "applyAll" in body
        assert "afterStateChange" in body
        assert re.search(r"return\s+false", body), (
            "applyPresetCode must return false on an invalid code"
        )

    def test_read_preset_from_url_uses_search_params(self) -> None:
        assert re.search(
            r'function\s+readPresetFromUrl\s*\([^)]*\)\s*\{[\s\S]*?searchParams\.get\s*\(\s*"preset"\s*\)',
            _JS,
        ), "readPresetFromUrl must read ?preset= via searchParams.get"

    def test_update_url_writes_preset_param(self) -> None:
        assert re.search(
            r'function\s+updateUrl\s*\([^)]*\)\s*\{[\s\S]*?searchParams\.set\s*\(\s*"preset"\s*,',
            _JS,
        ), "updateUrl must mirror state into ?preset= via searchParams.set"

    def test_default_preset_code_is_b0(self) -> None:
        assert re.search(r'DEFAULT_PRESET_CODE\s*=\s*"b0"', _JS)
        assert "return DEFAULT_PRESET_CODE" in _JS


def _encode_base62(num: int) -> str:
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    assert num >= 0
    if num == 0:
        return "0"
    out = ""
    while num > 0:
        out = alphabet[num % 62] + out
        num //= 62
    return out


def _encode_v2(
    *,
    font: int = 0,
    color: int = 0,
    chart: int = 0,
    base: int = 0,
    radius: int = 0,
    style: int = 0,
) -> str:
    # Mirrors theme-preview.js comboToCode() bit packing (version 2) so these
    # tests encode independently of the JS encoder and verify the decoder.
    # SHIFT_V2 (JS and Python share it): font=0, color=5, chart=10, base=15,
    # radius=19, style=23.
    if not any([font, color, chart, base, radius, style]):
        return DEFAULT_PRESET_CODE
    packed = (
        (2 << 28)
        | (style << 23)
        | (radius << 19)
        | (base << 15)
        | (chart << 10)
        | (color << 5)
        | (font << 0)
    ) & 0xFFFFFFFF
    return _encode_base62(packed)


class TestPresetCodecInterop:
    def test_non_default_url_example_decodes_to_stone_base(self) -> None:
        result = _decode("aKnAm")
        assert result is not None
        assert result["baseId"] == "stone"
        assert result["baseId"] != BASE_THEMES[0]["id"]
        assert result["colorId"] is None
        assert result["chartId"] is None
        assert result["radius"] is None

    def test_default_preset_code_decodes_to_all_defaults(self) -> None:
        result = _decode(DEFAULT_PRESET_CODE)
        assert result is not None
        assert result["baseId"] == BASE_THEMES[0]["id"] == "neutral"
        assert result["colorId"] is None
        assert result["chartId"] is None
        assert result["radius"] is None
        assert result["styleId"] == STYLE_REGISTRY[0]["id"]
        assert result["fontId"] == FONT_REGISTRY[0]["id"]

    @pytest.mark.parametrize(  # pyright: ignore[reportUntypedFunctionDecorator]
        "code",
        ["ZZZZZ", "", None, "!!!", "gibberish", "none-ish"],
    )
    def test_invalid_or_empty_codes_rejected(self, code: str) -> None:
        assert _decode(code) is None

    @pytest.mark.parametrize(  # pyright: ignore[reportUntypedFunctionDecorator]
        ("combo", "expected"),
        [
            ({"base": 1}, {"baseId": BASE_THEMES[1]["id"]}),
            ({"font": 1}, {"fontId": FONT_REGISTRY[1]["id"]}),
            ({"color": 1}, {"colorId": COLOR_THEMES[0]["id"]}),
            ({"chart": 2}, {"chartId": COLOR_THEMES[1]["id"]}),
            ({"radius": 2}, {"radius": RADII_OPTIONS[1]["value"]}),
            ({"style": 1}, {"styleId": STYLE_REGISTRY[1]["id"]}),
        ],
        ids=["base-stone", "font", "color", "chart", "radius", "style"],
    )
    def test_round_trip_each_index_dimension(
        self,
        combo: dict[str, int],
        expected: dict[str, object],
    ) -> None:
        code = _encode_v2(**combo)
        result = _decode(code)
        assert result is not None, f"decode failed for code {code!r} (combo {combo})"
        for key, val in expected.items():
            assert result[key] == val, (
                f"combo {combo}: expected {key}={val!r}, got {result[key]!r}"
            )

    def test_multi_dimension_round_trip(self) -> None:
        code = _encode_v2(base=3, color=2, chart=2, font=1, style=1, radius=2)
        r = _decode(code)
        assert r is not None
        assert r["baseId"] == BASE_THEMES[3]["id"]
        assert r["colorId"] == COLOR_THEMES[1]["id"]
        assert r["chartId"] == COLOR_THEMES[1]["id"]
        assert r["fontId"] == FONT_REGISTRY[1]["id"]
        assert r["styleId"] == STYLE_REGISTRY[1]["id"]
        assert r["radius"] == RADII_OPTIONS[1]["value"]

    def test_default_combo_short_circuit_equivalence(self) -> None:
        # The JS encoder short-circuits an all-defaults combo to the literal
        # "b0". The decoder must accept both "b0" and the non-short-circuited
        # packed form of the same combo and return identical state.
        assert _encode_v2() == DEFAULT_PRESET_CODE
        packed_default = _encode_base62(0x20000000)
        assert packed_default != DEFAULT_PRESET_CODE
        assert _decode(packed_default) == _decode(DEFAULT_PRESET_CODE)
