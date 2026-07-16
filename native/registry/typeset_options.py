# ---------------------------------------------------------------------------
# TYPESET OPTIONS
# Matches the real --typeset-* custom properties from shadcn/typeset's
# stylesheet exactly (names, units, and defaults) — see typeset.css:
#   --typeset-size: 1em (this app overrides to a px value, e.g. 15px)
#   --typeset-leading: 1.75   (unitless line-height)
#   --typeset-flow: 1.25em    (vertical rhythm between elements)
#
# Measure is deliberately NOT a --typeset-* variable — the real stylesheet
# has no such property. It's applied as a plain max-width directly on the
# wrapping element (e.g. class="typeset typeset-docs max-w-[37em]" in
# shadcn's own usage example). Keep that in mind when wiring this into the
# live preview: Measure needs a different application path (direct
# style.maxWidth) than the other four, which really are CSS custom
# properties on .typeset.
#
# Heading/Body/Mono font options are NOT defined here — they reuse the
# existing FONT_REGISTRY (native/registry/fonts.py), filtered by category
# in the page itself, rather than duplicating font data in two registries.
# ---------------------------------------------------------------------------

from native.registry.fonts import FONT_REGISTRY

# Heading/Body draw from the same pool (sans + serif); Mono is restricted
# to genuinely monospace faces, matching the screenshot ("Geist Mono").
# Computed here once rather than in the page, so there's a single source
# of truth for "which fonts are selectable for which field."
HEADING_BODY_FONTS = [f for f in FONT_REGISTRY if f["category"] in ("sans", "serif")]
MONO_FONTS = [f for f in FONT_REGISTRY if f["category"] == "mono"]

MEASURE_OPTIONS = [
    {"id": "60ch", "label": "60ch", "value": "60ch"},
    {"id": "65ch", "label": "65ch", "value": "65ch"},
    {"id": "70ch", "label": "70ch", "value": "70ch"},
    {"id": "75ch", "label": "75ch", "value": "75ch"},
    {"id": "80ch", "label": "80ch", "value": "80ch"},
    {"id": "90ch", "label": "90ch", "value": "90ch"},
]

SIZE_OPTIONS = [
    {"id": "14px", "label": "14px", "value": "14px"},
    {"id": "15px", "label": "15px", "value": "15px"},
    {"id": "16px", "label": "16px", "value": "16px"},
    {"id": "17px", "label": "17px", "value": "17px"},
    {"id": "18px", "label": "18px", "value": "18px"},
]

LEADING_OPTIONS = [
    {"id": "tight", "label": "Tight (1.5)", "value": "1.5"},
    {"id": "regular", "label": "Regular (1.75)", "value": "1.75"},
    {"id": "relaxed", "label": "Relaxed (2)", "value": "2"},
    {"id": "loose", "label": "Loose (2.25)", "value": "2.25"},
]

FLOW_OPTIONS = [
    {"id": "tight", "label": "Tight (1em)", "value": "1em"},
    {"id": "regular", "label": "Regular (1.25em)", "value": "1.25em"},
    {"id": "relaxed", "label": "Relaxed (1.5em)", "value": "1.5em"},
    {"id": "loose", "label": "Loose (1.75em)", "value": "1.75em"},
]

# Defaults match the real stylesheet's own built-in defaults (and your
# screenshot) exactly, not arbitrary picks: 80ch, 15px, 1.75, 1.25em.
DEFAULT_MEASURE_ID = "80ch"
DEFAULT_SIZE_ID = "15px"
DEFAULT_LEADING_ID = "regular"
DEFAULT_FLOW_ID = "regular"

# Font defaults reference native/registry/fonts.py's real ids — "geist" for
# heading/body, "geist-mono" for mono, matching the screenshot exactly.
# Not index-0 lookups on purpose: FONT_REGISTRY's first entry is "inter",
# not "geist" — same trap that bit the theme builder's Color/Chart selects
# defaulting to whatever happened to be list-first instead of the intended
# default. Every default in this file is resolved by id, never by position.
DEFAULT_HEADING_FONT_ID = "geist"
DEFAULT_BODY_FONT_ID = "geist"
DEFAULT_MONO_FONT_ID = "geist-mono"
