// (function () {
//   "use strict";

//   function findById(name, id) {
//     var list = (window.__THEME_REGISTRIES__ || {})[name];
//     if (!list) return null;
//     for (var i = 0; i < list.length; i++) {
//       if (list[i].id === id) return list[i];
//     }
//     return null;
//   }

//   var DEFAULT_RADIUS_VALUE = "__default__";
//   var MATCH_BASE_VALUE = "__match_base__";

//   // --- preset codec ---------------------------------------------------
//   // Each dimension gets a FIXED, generously-oversized bit width — larger
//   // than the registry's current length on purpose, so new entries can be
//   // appended at the end later without shifting indices and silently
//   // corrupting every preset code issued before that change. Registry
//   // entries must only ever be appended, never inserted/reordered.
//   var PRESET_VERSION = 1;
//   var BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
//   var DEFAULT_PRESET_CODE = "b0";
//   var BITS = { font: 5, color: 5, base: 4, radius: 4, style: 4 };
//   var SHIFT = (function () {
//     var s = {}, offset = 0;
//     ["font", "color", "base", "radius", "style"].forEach(function (name) {
//       s[name] = offset;
//       offset += BITS[name];
//     });
//     return s;
//   })();

//   function encodeBase62(num) {
//     if (num === 0) return "0";
//     var out = "";
//     while (num > 0) {
//       out = BASE62_ALPHABET[num % 62] + out;
//       num = Math.floor(num / 62);
//     }
//     return out;
//   }

//   function decodeBase62(str) {
//     var num = 0;
//     for (var i = 0; i < str.length; i++) {
//       var idx = BASE62_ALPHABET.indexOf(str[i]);
//       if (idx === -1) return null;
//       num = num * 62 + idx;
//     }
//     return num;
//   }

//   // Mulberry32 — deterministic PRNG for the shuffle button. Same seed
//   // always produces the same sequence of draws.
//   function mulberry32(seed) {
//     return function () {
//       seed |= 0;
//       seed = (seed + 0x6d2b79f5) | 0;
//       var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
//       t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
//       return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
//     };
//   }

//   function plainIndex(name, id) {
//     var list = (window.__THEME_REGISTRIES__ || {})[name];
//     if (!list) return 0;
//     for (var i = 0; i < list.length; i++) {
//       if (list[i].id === id) return i;
//     }
//     return 0;
//   }

//   // +1 reserves index 0 to mean "inherit" (match-base / style-default)
//   function inheritableIndex(name, id) {
//     var list = (window.__THEME_REGISTRIES__ || {})[name];
//     if (!list) return 0;
//     for (var i = 0; i < list.length; i++) {
//       if (list[i].id === id) return i + 1;
//     }
//     return 0;
//   }

//   function comboToCode() {
//     var styleIdx = plainIndex("style", state.style);
//     var baseIdx = plainIndex("base", state.base);
//     var fontIdx = plainIndex("font", state.font);
//     var colorIdx = state.color === MATCH_BASE_VALUE ? 0 : inheritableIndex("color", state.color);
//     var radiusIdx = state.radius === DEFAULT_RADIUS_VALUE ? 0 : inheritableIndex("radius", state.radius);

//     if (styleIdx === 0 && radiusIdx === 0 && baseIdx === 0 && colorIdx === 0 && fontIdx === 0) {
//       return DEFAULT_PRESET_CODE;
//     }

//     var packed =
//       ((PRESET_VERSION << 28) |
//         (styleIdx << SHIFT.style) |
//         (radiusIdx << SHIFT.radius) |
//         (baseIdx << SHIFT.base) |
//         (colorIdx << SHIFT.color) |
//         (fontIdx << SHIFT.font)) >>>
//       0;

//     return encodeBase62(packed);
//   }

//   // Returns true/false rather than throwing — callers (paste box, URL
//   // param) both need to handle "that wasn't a valid code" gracefully,
//   // not crash the page.
//   function applyCodeToState(code) {
//     if (!ensureDefaults()) return false;

//     var packed;
//     if (code === DEFAULT_PRESET_CODE) {
//       packed = (PRESET_VERSION << 28) >>> 0;
//     } else {
//       packed = decodeBase62(code);
//       if (packed === null) return false;
//     }

//     var version = (packed >>> 28) & 0xf;
//     if (version !== PRESET_VERSION) return false;

//     var styleIdx = (packed >>> SHIFT.style) & ((1 << BITS.style) - 1);
//     var radiusIdx = (packed >>> SHIFT.radius) & ((1 << BITS.radius) - 1);
//     var baseIdx = (packed >>> SHIFT.base) & ((1 << BITS.base) - 1);
//     var colorIdx = (packed >>> SHIFT.color) & ((1 << BITS.color) - 1);
//     var fontIdx = (packed >>> SHIFT.font) & ((1 << BITS.font) - 1);

//     var registries = window.__THEME_REGISTRIES__;
//     var styleEntry = registries.style[styleIdx];
//     var baseEntry = registries.base[baseIdx];
//     var fontEntry = registries.font[fontIdx];
//     if (!styleEntry || !baseEntry || !fontEntry) return false;

//     state.style = styleEntry.id;
//     state.base = baseEntry.id;
//     state.font = fontEntry.id;

//     if (colorIdx === 0) {
//       state.color = MATCH_BASE_VALUE;
//     } else {
//       var colorEntry = registries.color[colorIdx - 1];
//       if (!colorEntry) return false;
//       state.color = colorEntry.id;
//     }

//     if (radiusIdx === 0) {
//       state.radius = DEFAULT_RADIUS_VALUE;
//     } else {
//       var radiusEntry = registries.radius[radiusIdx - 1];
//       if (!radiusEntry) return false;
//       state.radius = radiusEntry.id;
//     }

//     return true;
//   }

//   function syncSelectsToState() {
//     var styleSelect = document.getElementById("style-select");
//     var baseSelect = document.getElementById("base-theme-select");
//     var colorSelect = document.getElementById("color-theme-select");
//     var radiusSelect = document.getElementById("radius-select");
//     var fontSelect = document.getElementById("font-select");

//     if (styleSelect) styleSelect.value = state.style;
//     if (baseSelect) baseSelect.value = state.base;
//     if (fontSelect) fontSelect.value = state.font;

//     var baseEntry = findById("base", state.base);
//     if (colorSelect) {
//       upsertSyntheticOption(colorSelect, MATCH_BASE_VALUE, baseEntry ? baseEntry.label : "Match base");
//       colorSelect.value = state.color;
//     }
//     if (radiusSelect) {
//       upsertSyntheticOption(radiusSelect, DEFAULT_RADIUS_VALUE, "Default");
//       radiusSelect.value = state.radius;
//     }
//   }

//   function updateUrl(code) {
//     try {
//       var url = new URL(window.location.href);
//       url.searchParams.set("preset", code);
//       window.history.replaceState({}, "", url);
//     } catch (e) {
//       /* no-op if URL isn't available (e.g. non-browser context) */
//     }
//   }

//   function readPresetFromUrl() {
//     try {
//       var url = new URL(window.location.href);
//       return url.searchParams.get("preset");
//     } catch (e) {
//       return null;
//     }
//   }

//   function afterStateChange() {
//     updateUrl(comboToCode());
//     var codeDisplay = document.getElementById("preset-code-display");
//     if (codeDisplay) codeDisplay.value = comboToCode();
//   }


//   var state = {
//     base: null,
//     color: MATCH_BASE_VALUE,
//     style: null,
//     radius: DEFAULT_RADIUS_VALUE,
//     font: null,
//   };

//   function ensureDefaults() {
//     var registries = window.__THEME_REGISTRIES__;
//     if (!registries) return false;
//     if (state.base === null) state.base = registries.base[0].id;
//     if (state.style === null) state.style = registries.style[0].id;
//     if (state.font === null) state.font = registries.font[0].id;
//     return true;
//   }

//   function root() {
//     return document.querySelector(".preview-theme");
//   }

//   // --- shared helper for preset -> dependent-select synthetic options -----
//   // Style resets Radius to a "Default" option (fixed label, meaning "use
//   // whatever --radius the current style defines"). Base resets Color to a
//   // synthetic option labeled with the base's own name (meaning "don't
//   // overlay a separate color theme, use the base's own primary/chart
//   // colors as-is"). Both are the same mechanism: create-if-missing, update
//   // label, select it — reused here instead of duplicated per-select.
//   function upsertSyntheticOption(selectEl, value, label) {
//     if (!selectEl) return null;
//     var opt = selectEl.querySelector('option[value="' + value + '"]');
//     if (!opt) {
//       opt = document.createElement("option");
//       opt.value = value;
//       selectEl.insertBefore(opt, selectEl.firstChild);
//     }
//     opt.textContent = label;
//     return opt;
//   }

//   function applyBase() {
//     var entry = findById("base", state.base);
//     var el = root();
//     if (!entry || !el) return;
//     var isDark = document.documentElement.classList.contains("dark");
//     var values = isDark ? entry.dark : entry.light;
//     Object.keys(values).forEach(function (key) {
//       el.style.setProperty("--" + key, values[key]);
//     });
//   }

//   function applyColorOverlay() {
//     if (state.color === MATCH_BASE_VALUE) return; // base's own colors stand as-is
//     var entry = findById("color", state.color);
//     var el = root();
//     if (!entry || !el) return;
//     var isDark = document.documentElement.classList.contains("dark");
//     var values = isDark ? entry.dark : entry.light;
//     Object.keys(values).forEach(function (key) {
//       el.style.setProperty("--" + key, values[key]);
//     });
//   }

//   function applyStyle() {
//     var entry = findById("style", state.style);
//     var el = root();
//     if (!entry || !el) return;
//     Object.keys(entry.vars).forEach(function (key) {
//       el.style.setProperty(key, entry.vars[key]);
//     });
//     // Radius is part of the style's own vars bag (applied above), but it's
//     // ALSO independently overridable via the Radius select — so if the
//     // user has explicitly picked something other than "Default", that
//     // explicit choice takes precedence over what the style just set.
//     if (state.radius !== DEFAULT_RADIUS_VALUE) {
//       applyRadiusOverride();
//     }
//   }

//   function applyRadiusOverride() {
//     var entry = findById("radius", state.radius);
//     var el = root();
//     if (!entry || !el) return;
//     el.style.setProperty("--radius", entry.value);
//   }

//   function applyFont() {
//     var entry = findById("font", state.font);
//     var el = root();
//     if (!entry || !el) return;
//     Object.keys(entry.vars).forEach(function (key) {
//       el.style.setProperty(key, entry.vars[key]);
//     });
//   }

//   function applyAll() {
//     if (!ensureDefaults()) return;
//     applyBase();
//     applyColorOverlay();
//     applyStyle(); // sets --radius from style, then re-applies an explicit radius override on top if one is active
//     applyFont();
//   }

//   function getThemeCSS() {
//     var base = findById("base", state.base);
//     var color = state.color === MATCH_BASE_VALUE ? null : findById("color", state.color);
//     var style = findById("style", state.style);
//     var font = findById("font", state.font);
//     if (!base || !style || !font) return "";

//     var radiusValue = style.vars["--radius"];
//     if (state.radius !== DEFAULT_RADIUS_VALUE) {
//       var radiusEntry = findById("radius", state.radius);
//       if (radiusEntry) radiusValue = radiusEntry.value;
//     }

//     var light = Object.assign({}, base.light, color ? color.light : {}, style.vars, font.vars, {
//       "--radius": radiusValue,
//     });
//     var dark = Object.assign({}, base.dark, color ? color.dark : {}, style.vars, font.vars, {
//       "--radius": radiusValue,
//     });

//     function serialize(values) {
//       return Object.keys(values)
//         .map(function (key) {
//           var cssKey = key.indexOf("--") === 0 ? key : "--" + key;
//           return "  " + cssKey + ": " + values[key] + ";";
//         })
//         .join("\n");
//     }

//     return ":root {\n" + serialize(light) + "\n}\n\n.dark {\n" + serialize(dark) + "\n}";
//   }

//   window.preview = {
//     state: state,

//     setBase: function (id) {
//       state.base = id;
//       var baseEntry = findById("base", id);
//       var colorSelect = document.getElementById("color-theme-select");
//       upsertSyntheticOption(
//         colorSelect,
//         MATCH_BASE_VALUE,
//         baseEntry ? baseEntry.label : "Match base"
//       );
//       // Only keep the select showing "match base" if the user hasn't
//       // manually overridden it — an explicit color choice persists across
//       // base changes, it just now overlays on top of the NEW base.
//       if (state.color === MATCH_BASE_VALUE && colorSelect) {
//         colorSelect.value = MATCH_BASE_VALUE;
//       }
//       applyBase();
//       applyColorOverlay();
//       afterStateChange();
//     },

//     setColor: function (id) {
//       state.color = id;
//       applyColorOverlay();
//       afterStateChange();
//     },

//     setStyle: function (id) {
//       state.style = id;
//       var radiusSelect = document.getElementById("radius-select");
//       upsertSyntheticOption(radiusSelect, DEFAULT_RADIUS_VALUE, "Default");
//       // Only keep the select showing "Default" if the user hasn't manually
//       // picked an explicit radius — an explicit pick persists across style
//       // changes (applyStyle() re-applies it on top automatically).
//       if (state.radius === DEFAULT_RADIUS_VALUE && radiusSelect) {
//         radiusSelect.value = DEFAULT_RADIUS_VALUE;
//       }
//       applyStyle();
//       afterStateChange();
//     },

//     setRadius: function (id) {
//       state.radius = id;
//       if (id === DEFAULT_RADIUS_VALUE) {
//         applyStyle(); // re-derive --radius from the current style
//       } else {
//         applyRadiusOverride();
//       }
//       afterStateChange();
//     },

//     setFont: function (id) {
//       state.font = id;
//       applyFont();
//       afterStateChange();
//     },

//     // Random combo via Mulberry32 — deterministic given a seed, so the
//     // resulting combo can always be re-derived from that seed alone. Not
//     // used for encoding the SHARE code though (see comboToCode) — a PRNG
//     // is one-way by design (seed -> output), there's no efficient way to
//     // go from an arbitrary target combo back to "which seed produces
//     // this", so shuffle and the share-code codec are deliberately separate
//     // mechanisms rather than one trying to do both jobs.
//     shuffle: function (seed) {
//       var registries = window.__THEME_REGISTRIES__;
//       if (!registries) return;
//       var rng = mulberry32(seed === undefined ? (Math.random() * 0xffffffff) >>> 0 : seed);

//       state.style = registries.style[Math.floor(rng() * registries.style.length)].id;
//       state.base = registries.base[Math.floor(rng() * registries.base.length)].id;
//       state.font = registries.font[Math.floor(rng() * registries.font.length)].id;
//       state.color =
//         rng() < 0.5
//           ? MATCH_BASE_VALUE
//           : registries.color[Math.floor(rng() * registries.color.length)].id;
//       state.radius =
//         rng() < 0.5
//           ? DEFAULT_RADIUS_VALUE
//           : registries.radius[Math.floor(rng() * registries.radius.length)].id;

//       syncSelectsToState();
//       applyAll();
//       afterStateChange();
//     },

//     // Returns true/false — callers (paste box) need to show an error for
//     // an invalid code rather than have this throw.
//     applyPresetCode: function (code) {
//       var ok = applyCodeToState(code);
//       if (!ok) return false;
//       syncSelectsToState();
//       applyAll();
//       afterStateChange();
//       return true;
//     },

//     getPresetCode: comboToCode,
//     reset: function () {
//       window.preview.applyPresetCode(DEFAULT_PRESET_CODE);
//     },
//     applyAll: applyAll,
//     getThemeCSS: getThemeCSS,
//   };

//   document.addEventListener("change", function (e) {
//     var id = e.target.id;
//     if (id === "base-theme-select") window.preview.setBase(e.target.value);
//     if (id === "color-theme-select") window.preview.setColor(e.target.value);
//     if (id === "style-select") window.preview.setStyle(e.target.value);
//     if (id === "radius-select") window.preview.setRadius(e.target.value);
//     if (id === "font-select") window.preview.setFont(e.target.value);
//   });

//   document.addEventListener("click", function (e) {
//     if (e.target.id === "copy-theme-button") {
//       navigator.clipboard.writeText(getThemeCSS());
//     }
//     if (e.target.id === "shuffle-button") {
//       window.preview.shuffle();
//     }
//     if (e.target.id === "reset-preset-button") {
//       window.preview.reset();
//     }
//     if (e.target.id === "apply-preset-button") {
//       var input = document.getElementById("preset-input");
//       if (!input) return;
//       var ok = window.preview.applyPresetCode(input.value.trim());
//       input.setAttribute("aria-invalid", ok ? "false" : "true");
//     }
//   });

//   new MutationObserver(function (mutations) {
//     for (var i = 0; i < mutations.length; i++) {
//       if (mutations[i].attributeName === "class") {
//         applyBase();
//         applyColorOverlay();
//         break;
//       }
//     }
//   }).observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });

//   // On first load: if the URL has a valid ?preset= code, apply it.
//   // Otherwise fall back to plain defaults (and write "b0" to the URL so
//   // the default state is itself shareable from the very first load).
//   var urlCode = readPresetFromUrl();
//   var appliedFromUrl = urlCode ? applyCodeToState(urlCode) : false;

//   applyAll();

//   // Seed the synthetic options on first load too, not just on future
//   // change events — otherwise "Default"/"<Base label>" wouldn't appear
//   // until the user touched Style or Base at least once.
//   if (ensureDefaults()) {
//     var baseEntry = findById("base", state.base);
//     upsertSyntheticOption(
//       document.getElementById("color-theme-select"),
//       MATCH_BASE_VALUE,
//       baseEntry ? baseEntry.label : "Match base"
//     );
//     upsertSyntheticOption(document.getElementById("radius-select"), DEFAULT_RADIUS_VALUE, "Default");
//     syncSelectsToState();
//     afterStateChange();
//   }
// })();


(function () {
  "use strict";

  function findById(name, id) {
    var list = (window.__THEME_REGISTRIES__ || {})[name];
    if (!list) return null;
    for (var i = 0; i < list.length; i++) {
      if (list[i].id === id) return list[i];
    }
    return null;
  }

  var DEFAULT_RADIUS_VALUE = "__default__";
  var MATCH_BASE_VALUE = "__match_base__";
  var MATCH_COLOR_VALUE = "__match_color__";

  // --- preset codec ---------------------------------------------------
  // Each dimension gets a FIXED, generously-oversized bit width — larger
  // than the registry's current length on purpose, so new entries can be
  // appended at the end later without shifting indices and silently
  // corrupting every preset code issued before that change. Registry
  // entries must only ever be appended, never inserted/reordered.
  //
  // v1 -> v2 added the "chart" dimension. The bit layout changed, so v1 is
  // kept exactly as originally shipped, purely for decoding old codes that
  // are already out in the world (e.g. bookmarked/shared URLs) — encoding
  // always uses the current version. A v1 code has no chart information,
  // so it decodes with chart defaulting to "Auto". An unrecognized future
  // version is rejected outright rather than guessed at.
  var PRESET_VERSION = 2;
  var BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
  var DEFAULT_PRESET_CODE = "b0";

  var BITS_V1 = { font: 5, color: 5, base: 4, radius: 4, style: 4 };
  var SHIFT_V1 = (function () {
    var s = {}, offset = 0;
    ["font", "color", "base", "radius", "style"].forEach(function (name) {
      s[name] = offset;
      offset += BITS_V1[name];
    });
    return s;
  })();

  var BITS_V2 = { font: 5, color: 5, chart: 5, base: 4, radius: 4, style: 4 };
  var SHIFT_V2 = (function () {
    var s = {}, offset = 0;
    ["font", "color", "chart", "base", "radius", "style"].forEach(function (name) {
      s[name] = offset;
      offset += BITS_V2[name];
    });
    return s;
  })();

  function encodeBase62(num) {
    if (num === 0) return "0";
    var out = "";
    while (num > 0) {
      out = BASE62_ALPHABET[num % 62] + out;
      num = Math.floor(num / 62);
    }
    return out;
  }

  function decodeBase62(str) {
    var num = 0;
    for (var i = 0; i < str.length; i++) {
      var idx = BASE62_ALPHABET.indexOf(str[i]);
      if (idx === -1) return null;
      num = num * 62 + idx;
    }
    return num;
  }

  // Mulberry32 — deterministic PRNG for the shuffle button. Same seed
  // always produces the same sequence of draws.
  function mulberry32(seed) {
    return function () {
      seed |= 0;
      seed = (seed + 0x6d2b79f5) | 0;
      var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function plainIndex(name, id) {
    var list = (window.__THEME_REGISTRIES__ || {})[name];
    if (!list) return 0;
    for (var i = 0; i < list.length; i++) {
      if (list[i].id === id) return i;
    }
    return 0;
  }

  // +1 reserves index 0 to mean "inherit" (match-base / style-default)
  function inheritableIndex(name, id) {
    var list = (window.__THEME_REGISTRIES__ || {})[name];
    if (!list) return 0;
    for (var i = 0; i < list.length; i++) {
      if (list[i].id === id) return i + 1;
    }
    return 0;
  }

  function comboToCode() {
    var styleIdx = plainIndex("style", state.style);
    var baseIdx = plainIndex("base", state.base);
    var fontIdx = plainIndex("font", state.font);
    var colorIdx = state.color === MATCH_BASE_VALUE ? 0 : inheritableIndex("color", state.color);
    var radiusIdx = state.radius === DEFAULT_RADIUS_VALUE ? 0 : inheritableIndex("radius", state.radius);
    var chartIdx = state.chart === MATCH_COLOR_VALUE ? 0 : inheritableIndex("color", state.chart);

    if (styleIdx === 0 && radiusIdx === 0 && baseIdx === 0 && colorIdx === 0 && chartIdx === 0 && fontIdx === 0) {
      return DEFAULT_PRESET_CODE;
    }

    var packed =
      ((PRESET_VERSION << 28) |
        (styleIdx << SHIFT_V2.style) |
        (radiusIdx << SHIFT_V2.radius) |
        (baseIdx << SHIFT_V2.base) |
        (colorIdx << SHIFT_V2.color) |
        (chartIdx << SHIFT_V2.chart) |
        (fontIdx << SHIFT_V2.font)) >>>
      0;

    return encodeBase62(packed);
  }

  // Returns true/false rather than throwing — callers (paste box, URL
  // param) both need to handle "that wasn't a valid code" gracefully,
  // not crash the page.
  function applyCodeToState(code) {
    if (!ensureDefaults()) return false;

    var packed;
    if (code === DEFAULT_PRESET_CODE) {
      packed = (PRESET_VERSION << 28) >>> 0;
    } else {
      packed = decodeBase62(code);
      if (packed === null) return false;
    }

    var version = (packed >>> 28) & 0xf;
    var styleIdx, radiusIdx, baseIdx, colorIdx, fontIdx, chartIdx;

    if (version === 1) {
      // Legacy format — no chart dimension existed yet, defaults to "Auto".
      styleIdx = (packed >>> SHIFT_V1.style) & ((1 << BITS_V1.style) - 1);
      radiusIdx = (packed >>> SHIFT_V1.radius) & ((1 << BITS_V1.radius) - 1);
      baseIdx = (packed >>> SHIFT_V1.base) & ((1 << BITS_V1.base) - 1);
      colorIdx = (packed >>> SHIFT_V1.color) & ((1 << BITS_V1.color) - 1);
      fontIdx = (packed >>> SHIFT_V1.font) & ((1 << BITS_V1.font) - 1);
      chartIdx = 0;
    } else if (version === 2) {
      styleIdx = (packed >>> SHIFT_V2.style) & ((1 << BITS_V2.style) - 1);
      radiusIdx = (packed >>> SHIFT_V2.radius) & ((1 << BITS_V2.radius) - 1);
      baseIdx = (packed >>> SHIFT_V2.base) & ((1 << BITS_V2.base) - 1);
      colorIdx = (packed >>> SHIFT_V2.color) & ((1 << BITS_V2.color) - 1);
      chartIdx = (packed >>> SHIFT_V2.chart) & ((1 << BITS_V2.chart) - 1);
      fontIdx = (packed >>> SHIFT_V2.font) & ((1 << BITS_V2.font) - 1);
    } else {
      return false; // unknown future version — reject rather than misread
    }

    var registries = window.__THEME_REGISTRIES__;
    var styleEntry = registries.style[styleIdx];
    var baseEntry = registries.base[baseIdx];
    var fontEntry = registries.font[fontIdx];
    if (!styleEntry || !baseEntry || !fontEntry) return false;

    state.style = styleEntry.id;
    state.base = baseEntry.id;
    state.font = fontEntry.id;

    if (colorIdx === 0) {
      state.color = MATCH_BASE_VALUE;
    } else {
      var colorEntry = registries.color[colorIdx - 1];
      if (!colorEntry) return false;
      state.color = colorEntry.id;
    }

    if (chartIdx === 0) {
      state.chart = MATCH_COLOR_VALUE;
    } else {
      var chartEntry = registries.color[chartIdx - 1];
      if (!chartEntry) return false;
      state.chart = chartEntry.id;
    }

    if (radiusIdx === 0) {
      state.radius = DEFAULT_RADIUS_VALUE;
    } else {
      var radiusEntry = registries.radius[radiusIdx - 1];
      if (!radiusEntry) return false;
      state.radius = radiusEntry.id;
    }

    return true;
  }

  function syncSelectsToState() {
    var styleSelect = document.getElementById("style-select");
    var baseSelect = document.getElementById("base-theme-select");
    var colorSelect = document.getElementById("color-theme-select");
    var chartSelect = document.getElementById("chart-color-select");
    var radiusSelect = document.getElementById("radius-select");
    var fontSelect = document.getElementById("font-select");

    if (styleSelect) styleSelect.value = state.style;
    if (baseSelect) baseSelect.value = state.base;
    if (fontSelect) fontSelect.value = state.font;

    var baseEntry = findById("base", state.base);
    if (colorSelect) {
      upsertSyntheticOption(colorSelect, MATCH_BASE_VALUE, baseEntry ? baseEntry.label : "Match base");
      colorSelect.value = state.color;
    }
    if (chartSelect) {
      upsertSyntheticOption(chartSelect, MATCH_COLOR_VALUE, "Auto");
      chartSelect.value = state.chart;
    }
    if (radiusSelect) {
      upsertSyntheticOption(radiusSelect, DEFAULT_RADIUS_VALUE, "Default");
      radiusSelect.value = state.radius;
    }
  }

  function updateUrl(code) {
    try {
      var url = new URL(window.location.href);
      url.searchParams.set("preset", code);
      window.history.replaceState({}, "", url);
    } catch (e) {
      /* no-op if URL isn't available (e.g. non-browser context) */
    }
  }

  function readPresetFromUrl() {
    try {
      var url = new URL(window.location.href);
      return url.searchParams.get("preset");
    } catch (e) {
      return null;
    }
  }

  function afterStateChange() {
    updateUrl(comboToCode());
    var codeDisplay = document.getElementById("preset-code-display");
    if (codeDisplay) codeDisplay.value = comboToCode();
  }


  var state = {
    base: null,
    color: MATCH_BASE_VALUE,
    chart: MATCH_COLOR_VALUE,
    style: null,
    radius: DEFAULT_RADIUS_VALUE,
    font: null,
  };

  function ensureDefaults() {
    var registries = window.__THEME_REGISTRIES__;
    if (!registries) return false;
    if (state.base === null) state.base = registries.base[0].id;
    if (state.style === null) state.style = registries.style[0].id;
    if (state.font === null) state.font = registries.font[0].id;
    return true;
  }

  function root() {
    return document.querySelector(".preview-theme");
  }

  // --- shared helper for preset -> dependent-select synthetic options -----
  // Style resets Radius to a "Default" option (fixed label, meaning "use
  // whatever --radius the current style defines"). Base resets Color to a
  // synthetic option labeled with the base's own name (meaning "don't
  // overlay a separate color theme, use the base's own primary/chart
  // colors as-is"). Both are the same mechanism: create-if-missing, update
  // label, select it — reused here instead of duplicated per-select.
  function upsertSyntheticOption(selectEl, value, label) {
    if (!selectEl) return null;
    var opt = selectEl.querySelector('option[value="' + value + '"]');
    if (!opt) {
      opt = document.createElement("option");
      opt.value = value;
      selectEl.insertBefore(opt, selectEl.firstChild);
    }
    opt.textContent = label;
    return opt;
  }

  function applyBase() {
    var entry = findById("base", state.base);
    var el = root();
    if (!entry || !el) return;
    var isDark = document.documentElement.classList.contains("dark");
    var values = isDark ? entry.dark : entry.light;
    Object.keys(values).forEach(function (key) {
      el.style.setProperty("--" + key, values[key]);
    });
  }

  var CHART_KEYS = ["chart-1", "chart-2", "chart-3", "chart-4", "chart-5"];

  function applyColorOverlay() {
    if (state.color === MATCH_BASE_VALUE) return; // base's own colors stand as-is
    var entry = findById("color", state.color);
    var el = root();
    if (!entry || !el) return;
    var isDark = document.documentElement.classList.contains("dark");
    var values = isDark ? entry.dark : entry.light;
    // chart-* is governed exclusively by applyChartOverlay — excluded here
    // so the two don't fight over the same keys depending on call order.
    Object.keys(values).forEach(function (key) {
      if (CHART_KEYS.indexOf(key) === -1) {
        el.style.setProperty("--" + key, values[key]);
      }
    });
  }

  // What chart-1..5 WOULD be if Chart is left on "Auto" — mirrors whatever
  // the Color select currently resolves to (an explicit color theme's own
  // chart-*, or the base's own chart-* if Color is also on "match base").
  function effectiveChartValues(isDark) {
    if (state.color !== MATCH_BASE_VALUE) {
      var c = findById("color", state.color);
      if (c) return isDark ? c.dark : c.light;
    }
    var b = findById("base", state.base);
    return b ? (isDark ? b.dark : b.light) : {};
  }

  function applyChartOverlay() {
    var el = root();
    if (!el) return;
    var isDark = document.documentElement.classList.contains("dark");
    var values;
    if (state.chart === MATCH_COLOR_VALUE) {
      values = effectiveChartValues(isDark);
    } else {
      var entry = findById("color", state.chart); // chart reuses COLOR_THEMES as its source list
      if (!entry) return;
      values = isDark ? entry.dark : entry.light;
    }
    CHART_KEYS.forEach(function (key) {
      if (values[key] !== undefined) el.style.setProperty("--" + key, values[key]);
    });
  }

  function applyStyle() {
    var entry = findById("style", state.style);
    var el = root();
    if (!entry || !el) return;
    Object.keys(entry.vars).forEach(function (key) {
      el.style.setProperty(key, entry.vars[key]);
    });
    // Radius is part of the style's own vars bag (applied above), but it's
    // ALSO independently overridable via the Radius select — so if the
    // user has explicitly picked something other than "Default", that
    // explicit choice takes precedence over what the style just set.
    if (state.radius !== DEFAULT_RADIUS_VALUE) {
      applyRadiusOverride();
    }
  }

  function applyRadiusOverride() {
    var entry = findById("radius", state.radius);
    var el = root();
    if (!entry || !el) return;
    el.style.setProperty("--radius", entry.value);
  }

  function applyFont() {
    var entry = findById("font", state.font);
    var el = root();
    if (!entry || !el) return;
    Object.keys(entry.vars).forEach(function (key) {
      el.style.setProperty(key, entry.vars[key]);
    });
  }

  function applyAll() {
    if (!ensureDefaults()) return;
    applyBase();
    applyColorOverlay();
    applyChartOverlay();
    applyStyle(); // sets --radius from style, then re-applies an explicit radius override on top if one is active
    applyFont();
    syncSwatches();
  }

  // Reads live CSS values back from the actual applied state (state object
  // + registries), rather than re-deriving colors independently — so
  // swatches can never drift out of sync with what's really applied.
  function syncSwatches() {
    var isDark = document.documentElement.classList.contains("dark");

    var baseEntry = findById("base", state.base);
    var baseSwatch = document.getElementById("base-theme-select-swatch");
    if (baseSwatch && baseEntry) {
      var bv = isDark ? baseEntry.dark : baseEntry.light;
      baseSwatch.style.backgroundColor = bv.primary;
    }

    var colorSwatch = document.getElementById("color-theme-select-swatch");
    if (colorSwatch) {
      var effectiveColor =
        state.color === MATCH_BASE_VALUE
          ? baseEntry && (isDark ? baseEntry.dark.primary : baseEntry.light.primary)
          : (function () {
              var c = findById("color", state.color);
              return c && (isDark ? c.dark.primary : c.light.primary);
            })();
      if (effectiveColor) colorSwatch.style.backgroundColor = effectiveColor;
    }

    var chartValues = effectiveChartValues(isDark);
    if (state.chart !== MATCH_COLOR_VALUE) {
      var explicitChart = findById("color", state.chart);
      if (explicitChart) chartValues = isDark ? explicitChart.dark : explicitChart.light;
    }
    CHART_KEYS.forEach(function (key, i) {
      var dot = document.getElementById("chart-color-select-swatch-" + (i + 1));
      if (dot && chartValues[key]) dot.style.backgroundColor = chartValues[key];
    });
  }

  function getThemeCSS() {
    var base = findById("base", state.base);
    var color = state.color === MATCH_BASE_VALUE ? null : findById("color", state.color);
    var style = findById("style", state.style);
    var font = findById("font", state.font);
    if (!base || !style || !font) return "";

    var radiusValue = style.vars["--radius"];
    if (state.radius !== DEFAULT_RADIUS_VALUE) {
      var radiusEntry = findById("radius", state.radius);
      if (radiusEntry) radiusValue = radiusEntry.value;
    }

    // Chart resolution mirrors applyChartOverlay's precedence, computed for
    // both modes at once since the exported CSS needs both :root and .dark
    // blocks simultaneously (unlike the live apply path, which only ever
    // cares about whichever mode is currently active).
    var chartSource = state.chart === MATCH_COLOR_VALUE ? color || base : findById("color", state.chart);
    var chartLight = {}, chartDark = {};
    if (chartSource) {
      CHART_KEYS.forEach(function (key) {
        if (chartSource.light[key] !== undefined) chartLight[key] = chartSource.light[key];
        if (chartSource.dark[key] !== undefined) chartDark[key] = chartSource.dark[key];
      });
    }

    var light = Object.assign({}, base.light, color ? color.light : {}, chartLight, style.vars, font.vars, {
      "--radius": radiusValue,
    });
    var dark = Object.assign({}, base.dark, color ? color.dark : {}, chartDark, style.vars, font.vars, {
      "--radius": radiusValue,
    });

    function serialize(values) {
      return Object.keys(values)
        .map(function (key) {
          var cssKey = key.indexOf("--") === 0 ? key : "--" + key;
          return "  " + cssKey + ": " + values[key] + ";";
        })
        .join("\n");
    }

    return ":root {\n" + serialize(light) + "\n}\n\n.dark {\n" + serialize(dark) + "\n}";
  }

  window.preview = {
    state: state,

    setBase: function (id) {
      state.base = id;
      var baseEntry = findById("base", id);
      var colorSelect = document.getElementById("color-theme-select");
      upsertSyntheticOption(
        colorSelect,
        MATCH_BASE_VALUE,
        baseEntry ? baseEntry.label : "Match base"
      );
      // Only keep the select showing "match base" if the user hasn't
      // manually overridden it — an explicit color choice persists across
      // base changes, it just now overlays on top of the NEW base.
      if (state.color === MATCH_BASE_VALUE && colorSelect) {
        colorSelect.value = MATCH_BASE_VALUE;
      }
      applyBase();
      applyColorOverlay();
      applyChartOverlay(); // keeps Chart's "Auto" tracking live if it's not explicitly overridden
      syncSwatches();
      afterStateChange();
    },

    setColor: function (id) {
      state.color = id;
      applyColorOverlay();
      applyChartOverlay(); // same — Auto chart tracks whichever color is now effective
      syncSwatches();
      afterStateChange();
    },

    setChart: function (id) {
      state.chart = id;
      applyChartOverlay();
      syncSwatches();
      afterStateChange();
    },

    setStyle: function (id) {
      state.style = id;
      var radiusSelect = document.getElementById("radius-select");
      upsertSyntheticOption(radiusSelect, DEFAULT_RADIUS_VALUE, "Default");
      // Only keep the select showing "Default" if the user hasn't manually
      // picked an explicit radius — an explicit pick persists across style
      // changes (applyStyle() re-applies it on top automatically).
      if (state.radius === DEFAULT_RADIUS_VALUE && radiusSelect) {
        radiusSelect.value = DEFAULT_RADIUS_VALUE;
      }
      applyStyle();
      afterStateChange();
    },

    setRadius: function (id) {
      state.radius = id;
      if (id === DEFAULT_RADIUS_VALUE) {
        applyStyle(); // re-derive --radius from the current style
      } else {
        applyRadiusOverride();
      }
      afterStateChange();
    },

    setFont: function (id) {
      state.font = id;
      applyFont();
      afterStateChange();
    },

    // Random combo via Mulberry32 — deterministic given a seed, so the
    // resulting combo can always be re-derived from that seed alone. Not
    // used for encoding the SHARE code though (see comboToCode) — a PRNG
    // is one-way by design (seed -> output), there's no efficient way to
    // go from an arbitrary target combo back to "which seed produces
    // this", so shuffle and the share-code codec are deliberately separate
    // mechanisms rather than one trying to do both jobs.
    shuffle: function (seed) {
      var registries = window.__THEME_REGISTRIES__;
      if (!registries) return;
      var rng = mulberry32(seed === undefined ? (Math.random() * 0xffffffff) >>> 0 : seed);

      state.style = registries.style[Math.floor(rng() * registries.style.length)].id;
      state.base = registries.base[Math.floor(rng() * registries.base.length)].id;
      state.font = registries.font[Math.floor(rng() * registries.font.length)].id;
      state.color =
        rng() < 0.5
          ? MATCH_BASE_VALUE
          : registries.color[Math.floor(rng() * registries.color.length)].id;
      state.chart =
        rng() < 0.5
          ? MATCH_COLOR_VALUE
          : registries.color[Math.floor(rng() * registries.color.length)].id;
      state.radius =
        rng() < 0.5
          ? DEFAULT_RADIUS_VALUE
          : registries.radius[Math.floor(rng() * registries.radius.length)].id;

      syncSelectsToState();
      applyAll();
      afterStateChange();
    },

    // Returns true/false — callers (paste box) need to show an error for
    // an invalid code rather than have this throw.
    applyPresetCode: function (code) {
      var ok = applyCodeToState(code);
      if (!ok) return false;
      syncSelectsToState();
      applyAll();
      afterStateChange();
      return true;
    },

    getPresetCode: comboToCode,
    reset: function () {
      window.preview.applyPresetCode(DEFAULT_PRESET_CODE);
    },
    applyAll: applyAll,
    getThemeCSS: getThemeCSS,
  };

  document.addEventListener("change", function (e) {
    var id = e.target.id;
    if (id === "base-theme-select") window.preview.setBase(e.target.value);
    if (id === "color-theme-select") window.preview.setColor(e.target.value);
    if (id === "chart-color-select") window.preview.setChart(e.target.value);
    if (id === "style-select") window.preview.setStyle(e.target.value);
    if (id === "radius-select") window.preview.setRadius(e.target.value);
    if (id === "font-select") window.preview.setFont(e.target.value);
  });

  document.addEventListener("click", function (e) {
    if (e.target.id === "copy-theme-button") {
      var target = document.getElementById("get-css-theme");
      target.textContent = getThemeCSS();
      navigator.clipboard.writeText(getThemeCSS());
    }
    if (e.target.id === "shuffle-button") {
      window.preview.shuffle();
    }
    if (e.target.id === "reset-preset-button") {
      window.preview.reset();
    }
    if (e.target.id === "apply-preset-button") {
      var input = document.getElementById("preset-input");
      if (!input) return;
      var ok = window.preview.applyPresetCode(input.value.trim());
      input.setAttribute("aria-invalid", ok ? "false" : "true");
    }
  });

  new MutationObserver(function (mutations) {
    for (var i = 0; i < mutations.length; i++) {
      if (mutations[i].attributeName === "class") {
        applyBase();
        applyColorOverlay();
        applyChartOverlay();
        syncSwatches();
        break;
      }
    }
  }).observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });


  // On first load: if the URL has a valid ?preset= code, apply it.
  // Otherwise fall back to plain defaults (and write "b0" to the URL so
  // the default state is itself shareable from the very first load).
  var urlCode = readPresetFromUrl();
  var appliedFromUrl = urlCode ? applyCodeToState(urlCode) : false;

  applyAll();

  // Seed the synthetic options on first load too, not just on future
  // change events — otherwise "Default"/"<Base label>" wouldn't appear
  // until the user touched Style or Base at least once.
  if (ensureDefaults()) {
    var baseEntry = findById("base", state.base);
    upsertSyntheticOption(
      document.getElementById("color-theme-select"),
      MATCH_BASE_VALUE,
      baseEntry ? baseEntry.label : "Match base"
    );
    upsertSyntheticOption(document.getElementById("radius-select"), DEFAULT_RADIUS_VALUE, "Default");
    syncSelectsToState();
    afterStateChange();
  }
})();
