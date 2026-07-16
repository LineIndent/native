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

  function getCode() {
    var heading = findById("heading", state.heading);
    var body = findById("body", state.body);
    var mono = findById("mono", state.mono);
    var measure = findById("measure", state.measure);
    var size = findById("size", state.size);
    var leading = findById("leading", state.leading);
    var flow = findById("flow", state.flow);
    if (!heading || !body || !mono || !measure || !size || !leading || !flow)
      return "";

    var css =
      ".typeset-custom {\n" +
      "  --typeset-font-heading: " +
      heading.vars["--font-family"] +
      ";\n" +
      "  --typeset-font-body: " +
      body.vars["--font-family"] +
      ";\n" +
      "  --typeset-font-mono: " +
      mono.vars["--font-family"] +
      ";\n" +
      "  --typeset-size: " +
      size.value +
      ";\n" +
      "  --typeset-leading: " +
      leading.value +
      ";\n" +
      "  --typeset-flow: " +
      flow.value +
      ";\n" +
      "}";

    var usage =
      '<div class="typeset typeset-custom max-w-[' +
      measure.value +
      ']">\n  {content}\n</div>';

    return css + "\n\n" + usage;
  }

  window.typesetPreview = {
    state: state,
    applyAll: applyAll,
    shuffle: shuffle,
    getCode: getCode,
  };

  document.addEventListener("change", function (e) {
    var id = e.target.id;
    Object.keys(FIELD_REGISTRY).forEach(function (field) {
      if (id === field + "-select") {
        state[field] = e.target.value;
        applyAll();
      }
    });
  });

  document.addEventListener("click", function (e) {
    if (e.target.id === "typeset-shuffle-button") {
      shuffle();
    }
    if (e.target.id === "typeset-copy-button") {
      navigator.clipboard.writeText(getCode());
    }
  });

  applyAll();
  syncSelectsToState();
})();
