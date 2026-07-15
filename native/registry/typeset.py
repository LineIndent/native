"""
Registries for the Typeset builder. Measure/Size/Leading/Flow are new here.
Heading/Body/Mono reuse the EXISTING FONT_REGISTRY (same source as the
theme builder's Font select) filtered by category, rather than duplicating
font data in a second place where it could drift out of sync.
"""

from native.registry.fonts import FONT_REGISTRY

# ---------------------------------------------------------------------------
# Line length (measure) — classic typographic convention: ~45-90 characters
# per line is the readability sweet spot, so a small fixed set of common
# values makes more sense here than a free-form/continuous control.
# ---------------------------------------------------------------------------
MEASURE_OPTIONS = [
    {"id": "60ch", "label": "60ch", "value": "60ch"},
    {"id": "65ch", "label": "65ch", "value": "65ch"},
    {"id": "70ch", "label": "70ch", "value": "70ch"},
    {"id": "75ch", "label": "75ch", "value": "75ch"},
    {"id": "80ch", "label": "80ch", "value": "80ch"},
    {"id": "90ch", "label": "90ch", "value": "90ch"},
]

# ---------------------------------------------------------------------------
# Base font size
# ---------------------------------------------------------------------------
SIZE_OPTIONS = [
    {"id": "14px", "label": "14px", "value": "14px"},
    {"id": "15px", "label": "15px", "value": "15px"},
    {"id": "16px", "label": "16px", "value": "16px"},
    {"id": "17px", "label": "17px", "value": "17px"},
    {"id": "18px", "label": "18px", "value": "18px"},
]

# ---------------------------------------------------------------------------
# Line height (leading)
# ---------------------------------------------------------------------------
LEADING_OPTIONS = [
    {"id": "tight", "label": "Tight (1.5)", "value": "1.5"},
    {"id": "regular", "label": "Regular (1.75)", "value": "1.75"},
    {"id": "relaxed", "label": "Relaxed (2)", "value": "2"},
    {"id": "loose", "label": "Loose (2.25)", "value": "2.25"},
]

# ---------------------------------------------------------------------------
# Vertical rhythm — spacing between flow elements (paragraphs, headings,
# lists, etc. via a "* + * { margin-top: var(--flow) }"-style pattern).
# ---------------------------------------------------------------------------
FLOW_OPTIONS = [
    {"id": "tight", "label": "Tight (1em)", "value": "1em"},
    {"id": "regular", "label": "Regular (1.25em)", "value": "1.25em"},
    {"id": "relaxed", "label": "Relaxed (1.5em)", "value": "1.5em"},
    {"id": "loose", "label": "Loose (1.75em)", "value": "1.75em"},
]

# ---------------------------------------------------------------------------
# Fonts — reuse FONT_REGISTRY wholesale, just filtered by category.
# Heading/Body draw from the same pool (sans + serif); Mono is restricted
# to genuinely monospace faces, matching the screenshot ("Geist Mono").
# ---------------------------------------------------------------------------
HEADING_BODY_FONTS = [f for f in FONT_REGISTRY if f["category"] in ("sans", "serif")]
MONO_FONTS = [f for f in FONT_REGISTRY if f["category"] == "mono"]
