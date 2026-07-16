(function () {
  "use strict";

  // Which registry list each field pulls from. Heading/Body share the same
  // sans+serif list; Mono gets its own — both precomputed in Python from
  // the existing FONT_REGISTRY (filtered by category) rather than
  // duplicated here, so shuffle only ever picks fonts that are actually
  // selectable in that field's dropdown.
  var FIELD_REGISTRY = {
    heading: "headingBodyFonts",
    body: "headingBodyFonts",
    mono: "monoFonts",
    measure: "measure",
    size: "size",
    leading: "leading",
    flow: "flow",
  };

  // Named defaults, not index-0 — none of these are first in their actual
  // lists (15px is index 1 in SIZE_OPTIONS, "geist" isn't first in
  // FONT_REGISTRY, etc.), so defaulting to "whatever's first" would
  // silently pick the wrong thing, same trap the theme builder's
  // Color/Chart selects fell into before being fixed.
  var DEFAULTS = {
    heading: "geist",
    body: "geist",
    mono: "geist-mono",
    measure: "80ch",
    size: "15px",
    leading: "regular",
    flow: "regular",
  };

  var state = {
    heading: null,
    body: null,
    mono: null,
    measure: null,
    size: null,
    leading: null,
    flow: null,
  };

  function findById(field, id) {
    var registryKey = FIELD_REGISTRY[field];
    var list = (window.__TYPESET_REGISTRIES__ || {})[registryKey];
    if (!list) return null;
    for (var i = 0; i < list.length; i++) {
      if (list[i].id === id) return list[i];
    }
    return null;
  }

  function ensureDefaults() {
    if (!window.__TYPESET_REGISTRIES__) return false;
    Object.keys(DEFAULTS).forEach(function (field) {
      if (state[field] === null) state[field] = DEFAULTS[field];
    });
    return true;
  }

  function root() {
    return document.querySelector(".typeset-preview");
  }

  function applyFontField(field, cssVar) {
    var entry = findById(field, state[field]);
    var el = root();
    if (!entry || !el) return;
    var fam = entry.vars && entry.vars["--font-family"];
    if (fam) el.style.setProperty(cssVar, fam);
  }

  // Measure is deliberately NOT a --typeset-* custom property — the real
  // stylesheet has no such variable. It's a plain max-width applied
  // directly to the wrapping element, matching shadcn's own usage example
  // (class="typeset typeset-docs max-w-[37em]"). Every other field here
  // IS a genuine CSS custom property; this one alone isn't.
  function applyMeasure() {
    var entry = findById("measure", state.measure);
    var el = root();
    if (!entry || !el) return;
    el.style.maxWidth = entry.value;
  }

  function applySize() {
    var entry = findById("size", state.size);
    var el = root();
    if (!entry || !el) return;
    el.style.setProperty("--typeset-size", entry.value);
  }

  function applyLeading() {
    var entry = findById("leading", state.leading);
    var el = root();
    if (!entry || !el) return;
    el.style.setProperty("--typeset-leading", entry.value);
  }

  function applyFlow() {
    var entry = findById("flow", state.flow);
    var el = root();
    if (!entry || !el) return;
    el.style.setProperty("--typeset-flow", entry.value);
  }

  function applyAll() {
    if (!ensureDefaults()) return;
    applyFontField("heading", "--typeset-font-heading");
    applyFontField("body", "--typeset-font-body");
    applyFontField("mono", "--typeset-font-mono");
    applyMeasure();
    applySize();
    applyLeading();
    applyFlow();
  }

  function syncSelectsToState() {
    Object.keys(FIELD_REGISTRY).forEach(function (field) {
      var el = document.getElementById(field + "-select");
      if (el) el.value = state[field];
    });
  }

  // Mulberry32 — same deterministic PRNG as the theme builder's shuffle.
  function mulberry32(seed) {
    return function () {
      seed |= 0;
      seed = (seed + 0x6d2b79f5) | 0;
      var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function shuffle(seed) {
    var registries = window.__TYPESET_REGISTRIES__;
    if (!registries) return;
    var rng = mulberry32(
      seed === undefined ? (Math.random() * 0xffffffff) >>> 0 : seed,
    );

    function pick(list) {
      return list[Math.floor(rng() * list.length)].id;
    }

    state.heading = pick(registries.headingBodyFonts);
    state.body = pick(registries.headingBodyFonts);
    state.mono = pick(registries.monoFonts);
    state.measure = pick(registries.measure);
    state.size = pick(registries.size);
    state.leading = pick(registries.leading);
    state.flow = pick(registries.flow);

    syncSelectsToState();
    applyAll();
  }

  // Google Fonts import names for next/font/google — NOT derivable from
  // FONT_REGISTRY's id/label alone (e.g. id="playfair" but the real font
  // is "Playfair Display"; id="ibm-plex-mono" needs "IBM" fully
  // capitalized, not title-cased). This is a second source of truth that
  // has to be kept in sync with FONT_REGISTRY by hand — the durable fix is
  // adding a google_import field to FONT_REGISTRY itself so this table
  // isn't needed at all. Until then, any new font added to FONT_REGISTRY
  // needs an entry here too, or its step-2 snippet will be silently wrong.
  var GOOGLE_FONT_IMPORTS = {
    inter: "Inter",
    geist: "Geist",
    roboto: "Roboto",
    outfit: "Outfit",
    "plus-jakarta": "Plus_Jakarta_Sans",
    "public-sans": "Public_Sans",
    playfair: "Playfair_Display",
    merriweather: "Merriweather",
    lora: "Lora",
    "instrument-serif": "Instrument_Serif",
    "fira-code": "Fira_Code",
    "jetbrains-mono": "JetBrains_Mono",
    "geist-mono": "Geist_Mono",
    "ibm-plex-mono": "IBM_Plex_Mono",
  };

  function cssVarNameFor(fontId) {
    return "--font-" + fontId;
  }

  // Deduped by font id — heading/body are very often the same font, and
  // the next/font import block should only load each one once.
  function activeFontEntries() {
    var seen = {};
    var result = [];
    ["heading", "body", "mono"].forEach(function (field) {
      var entry = findById(field, state[field]);
      if (entry && !seen[entry.id]) {
        seen[entry.id] = true;
        result.push(entry);
      }
    });
    return result;
  }

  function deriveFallbackImportName(fontId) {
    // Best-effort only — title-cases each hyphen-separated word, which
    // gets plenty of real Google Font names right (montserrat -> Montserrat)
    // but WILL get acronym casing wrong (ibm-plex-mono -> Ibm_Plex_Mono, not
    // IBM_Plex_Mono). Good enough to produce syntactically safe, non-
    // colliding code; not good enough to trust blindly — callers mark
    // fallback usage explicitly rather than passing it off as verified.
    return fontId
      .split("-")
      .map(function (w) {
        return w.charAt(0).toUpperCase() + w.slice(1);
      })
      .join("_");
  }

  function getFontImportsCode() {
    var fonts = activeFontEntries();
    if (!fonts.length) return "";

    var usedFallback = false;
    var importNames = fonts.map(function (f) {
      if (GOOGLE_FONT_IMPORTS[f.id]) return GOOGLE_FONT_IMPORTS[f.id];
      usedFallback = true;
      return deriveFallbackImportName(f.id);
    });

    var lines = [];
    if (usedFallback) {
      lines.push(
        "// NOTE: one or more font import names below are a best-effort guess",
        "// (not in the known-good list) — double check against next/font/google",
        "// before shipping this.",
      );
    }
    lines.push(
      "// app/layout.tsx",
      "import { " + importNames.join(", ") + ' } from "next/font/google"',
      "",
    );

    fonts.forEach(function (f, i) {
      var constName = importNames[i].toLowerCase();
      lines.push(
        "const " + constName + " = " + importNames[i] + "({",
        '  subsets: ["latin"],',
        '  variable: "' + cssVarNameFor(f.id) + '",',
        "})",
      );
      lines.push("");
    });

    var classNames = fonts
      .map(function (f, i) {
        return "${" + importNames[i].toLowerCase() + ".variable}";
      })
      .join(" ");
    lines.push("<html className={`" + classNames + "`}>");

    return lines.join("\n");
  }

  // The exported theme-tokens block references var(--font-{id}) rather
  // than the literal font-family string the LIVE PREVIEW uses — the real
  // app will have next/font actually defining that variable (via the step-2
  // snippet above), so referencing it is correct there even though the
  // preview (no real next/font loading happening in this browser tool)
  // needs the literal string to render anything at all.
  function getThemeTokensCode(className) {
    var heading = findById("heading", state.heading);
    var body = findById("body", state.body);
    var mono = findById("mono", state.mono);
    var size = findById("size", state.size);
    var leading = findById("leading", state.leading);
    var flow = findById("flow", state.flow);
    if (!heading || !body || !mono || !size || !leading || !flow) return "";

    return (
      "." +
      (className || "typeset-preset") +
      " {\n" +
      "  --typeset-font-body: var(" +
      cssVarNameFor(body.id) +
      ");\n" +
      "  --typeset-font-heading: var(" +
      cssVarNameFor(heading.id) +
      ");\n" +
      "  --typeset-font-mono: var(" +
      cssVarNameFor(mono.id) +
      ");\n" +
      "  --typeset-size: " +
      size.value +
      ";\n" +
      "  --typeset-leading: " +
      leading.value +
      ";\n" +
      "  --typeset-flow: " +
      flow.value +
      ";\n" +
      "}"
    );
  }

  function getUsageCode(className) {
    var measure = findById("measure", state.measure);
    if (!measure) return "";
    return (
      '<div className="typeset ' +
      (className || "typeset-preset") +
      " max-w-[" +
      measure.value +
      ']">\n  {content}\n</div>'
    );
  }

  // Re-populates the step-2/step-3 code blocks and re-runs Prism — called
  // after every state change (select, shuffle, and once on initial load),
  // not just once at mount, since these steps' content is meant to update
  // live as the user changes selections.
  function renderCodeBlocks() {
    var fontsEl = document.getElementById("get-typeset-fonts");
    if (fontsEl) fontsEl.textContent = getFontImportsCode();

    var tokensEl = document.getElementById("get-typeset-tokens");
    if (tokensEl) tokensEl.textContent = getThemeTokensCode();

    if (window.Prism) {
      try {
        Prism.highlightAll();
      } catch (e) {
        /* no-op — Prism not ready yet on very first call, harmless */
      }
    }
  }

  window.typesetPreview = {
    state: state,
    applyAll: applyAll,
    shuffle: shuffle,
    getFontImportsCode: getFontImportsCode,
    getThemeTokensCode: getThemeTokensCode,
    getUsageCode: getUsageCode,
    renderCodeBlocks: renderCodeBlocks,
  };

  document.addEventListener("change", function (e) {
    var id = e.target.id;
    Object.keys(FIELD_REGISTRY).forEach(function (field) {
      if (id === field + "-select") {
        state[field] = e.target.value;
        applyAll();
        renderCodeBlocks();
      }
    });
  });

  document.addEventListener("click", function (e) {
    if (e.target.id === "typeset-shuffle-button") {
      shuffle();
      renderCodeBlocks();
    }
    if (e.target.id === "copy-typeset-fonts") {
      navigator.clipboard.writeText(getFontImportsCode());
    }
    if (e.target.id === "copy-typeset-tokens") {
      navigator.clipboard.writeText(
        getThemeTokensCode() + "\n\n" + getUsageCode(),
      );
    }
  });

  applyAll();
  syncSelectsToState();
  renderCodeBlocks();
})();
