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
//   function ensureSyntheticOption(selectEl, value, label) {
//     if (!selectEl) return;
//     var opt = selectEl.querySelector('option[value="' + value + '"]');
//     if (!opt) {
//       opt = document.createElement("option");
//       opt.value = value;
//       selectEl.insertBefore(opt, selectEl.firstChild);
//     }
//     opt.textContent = label;
//     selectEl.value = value;
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
//       state.color = MATCH_BASE_VALUE; // new base resets color back to "match base"
//       var baseEntry = findById("base", id);
//       ensureSyntheticOption(
//         document.getElementById("color-theme-select"),
//         MATCH_BASE_VALUE,
//         baseEntry ? baseEntry.label : "Match base"
//       );
//       applyBase();
//       applyColorOverlay();
//     },

//     setColor: function (id) {
//       state.color = id;
//       applyColorOverlay();
//     },

//     setStyle: function (id) {
//       state.style = id;
//       state.radius = DEFAULT_RADIUS_VALUE; // new style resets radius back to "Default"
//       ensureSyntheticOption(
//         document.getElementById("radius-select"),
//         DEFAULT_RADIUS_VALUE,
//         "Default"
//       );
//       applyStyle();
//     },

//     setRadius: function (id) {
//       state.radius = id;
//       if (id === DEFAULT_RADIUS_VALUE) {
//         applyStyle(); // re-derive --radius from the current style
//       } else {
//         applyRadiusOverride();
//       }
//     },

//     setFont: function (id) {
//       state.font = id;
//       applyFont();
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

//   applyAll();

//   // Seed the synthetic options on first load too, not just on future
//   // change events — otherwise "Default"/"<Base label>" wouldn't appear
//   // until the user touched Style or Base at least once.
//   if (ensureDefaults()) {
//     var baseEntry = findById("base", state.base);
//     ensureSyntheticOption(
//       document.getElementById("color-theme-select"),
//       MATCH_BASE_VALUE,
//       baseEntry ? baseEntry.label : "Match base"
//     );
//     ensureSyntheticOption(
//       document.getElementById("radius-select"),
//       DEFAULT_RADIUS_VALUE,
//       "Default"
//     );
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

  var state = {
    base: null,
    color: MATCH_BASE_VALUE,
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

  function applyColorOverlay() {
    if (state.color === MATCH_BASE_VALUE) return; // base's own colors stand as-is
    var entry = findById("color", state.color);
    var el = root();
    if (!entry || !el) return;
    var isDark = document.documentElement.classList.contains("dark");
    var values = isDark ? entry.dark : entry.light;
    Object.keys(values).forEach(function (key) {
      el.style.setProperty("--" + key, values[key]);
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
    applyStyle(); // sets --radius from style, then re-applies an explicit radius override on top if one is active
    applyFont();
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

    var light = Object.assign({}, base.light, color ? color.light : {}, style.vars, font.vars, {
      "--radius": radiusValue,
    });
    var dark = Object.assign({}, base.dark, color ? color.dark : {}, style.vars, font.vars, {
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
    },

    setColor: function (id) {
      state.color = id;
      applyColorOverlay();
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
    },

    setRadius: function (id) {
      state.radius = id;
      if (id === DEFAULT_RADIUS_VALUE) {
        applyStyle(); // re-derive --radius from the current style
      } else {
        applyRadiusOverride();
      }
    },

    setFont: function (id) {
      state.font = id;
      applyFont();
    },

    applyAll: applyAll,
    getThemeCSS: getThemeCSS,
  };

  document.addEventListener("change", function (e) {
    var id = e.target.id;
    if (id === "base-theme-select") window.preview.setBase(e.target.value);
    if (id === "color-theme-select") window.preview.setColor(e.target.value);
    if (id === "style-select") window.preview.setStyle(e.target.value);
    if (id === "radius-select") window.preview.setRadius(e.target.value);
    if (id === "font-select") window.preview.setFont(e.target.value);
  });

  document.addEventListener("click", function (e) {
    if (e.target.id === "copy-theme-button") {
      navigator.clipboard.writeText(getThemeCSS());
    }
  });

  new MutationObserver(function (mutations) {
    for (var i = 0; i < mutations.length; i++) {
      if (mutations[i].attributeName === "class") {
        applyBase();
        applyColorOverlay();
        break;
      }
    }
  }).observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });

  applyAll();

  // Seed the synthetic options on first load too, not just on future
  // change events — otherwise "Default"/"<Base label>" wouldn't appear
  // until the user touched Style or Base at least once.
  if (ensureDefaults()) {
    var baseEntry = findById("base", state.base);
    var colorSelect = document.getElementById("color-theme-select");
    var radiusSelect = document.getElementById("radius-select");
    upsertSyntheticOption(colorSelect, MATCH_BASE_VALUE, baseEntry ? baseEntry.label : "Match base");
    upsertSyntheticOption(radiusSelect, DEFAULT_RADIUS_VALUE, "Default");
    if (colorSelect) colorSelect.value = MATCH_BASE_VALUE;
    if (radiusSelect) radiusSelect.value = DEFAULT_RADIUS_VALUE;
  }
})();
