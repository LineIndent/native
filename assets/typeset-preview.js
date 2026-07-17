(function () {
  "use strict";

  var FIELD_REGISTRY = {
    heading: "headingBodyFonts",
    body: "headingBodyFonts",
    mono: "monoFonts",
    measure: "measure",
    size: "size",
    leading: "leading",
    flow: "flow",
  };

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

  function googleFontNameFrom(entry) {
    var m =
      entry.vars &&
      entry.vars["--font-family"] &&
      entry.vars["--font-family"].match(/^"([^"]+)"/);
    return m ? m[1] : entry.label;
  }

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

  function getFontLinkCode() {
    var fonts = activeFontEntries();
    if (!fonts.length) return "";

    var families = fonts
      .map(function (f) {
        return (
          "family=" + googleFontNameFrom(f).replace(/ /g, "+") + ":wght@400;700"
        );
      })
      .join("&");

    var url = "https://fonts.googleapis.com/css2?" + families + "&display=swap";

    return `import reflex as rx

app = rx.App(
    stylesheets=[
        "${url}",
    ],
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin="true"),
    ]
)`;
  }

  // Literal font-family string, same value the live preview already uses
  // — there's no CSS variable to reference with this loading approach.
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
      "  --typeset-font-body: " +
      body.vars["--font-family"] +
      ";\n" +
      "  --typeset-font-heading: " +
      heading.vars["--font-family"] +
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
      "}"
    );
  }

  function getUsageCode(className) {
    var measure = findById("measure", state.measure);
    if (!measure) return "";
    return (
      "rx.el.div(\n" +
      "    ...,\n" +
      '    class_name="typeset ' +
      (className || "typeset-preset") +
      " max-w-[" +
      measure.value +
      ']",\n' +
      ")"
    );
  }

  // Re-populates the step-2/step-3 code blocks and re-runs Prism — called
  // after every state change (select, shuffle, and once on initial load),
  // not just once at mount, since these steps' content is meant to update
  // live as the user changes selections.
  function renderCodeBlocks() {
    var fontsEl = document.getElementById("get-typeset-fonts");
    if (fontsEl) fontsEl.textContent = getFontLinkCode();

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
    getFontLinkCode: getFontLinkCode,
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
      navigator.clipboard.writeText(getFontLinkCode());
      const text = document.getElementById("copy-typeset-fonts");
      if (text) {
        text.innerText = "Copied!";
        setTimeout(() => {
          text.innerText = "Copy";
        }, 1000);
      }
    }
    if (e.target.id === "copy-typeset-tokens") {
      navigator.clipboard.writeText(
        getThemeTokensCode() + "\n\n" + getUsageCode(),
      );
      const text = document.getElementById("copy-typeset-tokens");
      if (text) {
        text.innerText = "Copied!";
        setTimeout(() => {
          text.innerText = "Copy";
        }, 1000);
      }
    }
  });

  applyAll();
  syncSelectsToState();
  renderCodeBlocks();
})();
