from components.ui.tabs import tabs

DEMO_MODULES = {
    "basic": ("native.lib.components.tabs_basic", "tabs_basic"),
    "disabled": ("native.lib.components.tabs_disabled", "tabs_disabled"),
    "icons": ("native.lib.components.tabs_icons", "tabs_icons"),
    "line": ("native.lib.components.tabs_line_variant", "tabs_line"),
    "vertical": ("native.lib.components.tabs_vertical", "tabs_vertical"),
}

GUARD_SUBSTRING = "closest('[data-slot=\"tabs\"]') !== root"


def _walk_components(comp):
    yield comp
    for child in getattr(comp, "children", []) or []:
        if hasattr(child, "custom_attrs") or hasattr(child, "event_triggers"):
            yield from _walk_components(child)


def _extract_on_click_js(comp):
    out = []
    for node in _walk_components(comp):
        et = getattr(node, "event_triggers", {}) or {}
        spec = et.get("on_click")
        if spec is None:
            continue
        events = getattr(spec, "events", None) or [spec]
        for ev in events:
            stack = list(getattr(ev, "args", None) or ())
            while stack:
                item = stack.pop()
                if isinstance(item, (tuple, list)):
                    stack.extend(item)
                    continue
                value = getattr(item, "_var_value", None)
                if isinstance(value, str) and "querySelectorAll" in value:
                    out.append(value)
    return out


def _build_nested_tree(default_inner="profile"):
    return tabs.root(
        tabs.list(
            tabs.trigger("Home", value="home", id="outer-home"),
            tabs.trigger("Settings", value="settings", id="outer-settings"),
        ),
        tabs.content(
            tabs.root(
                tabs.list(
                    tabs.trigger("Profile", value="profile", id="inner-prof"),
                    tabs.trigger("Security", value="security", id="inner-sec"),
                ),
                tabs.content("Profile panel", value="profile"),
                tabs.content("Security panel", value="security"),
                default_value=default_inner,
            ),
            value="settings",
        ),
        default_value="settings",
    )


def _dom_tree(comp):
    ca = getattr(comp, "custom_attrs", {}) or {}
    return {
        "slot": ca.get("data-slot"),
        "value": ca.get("data-value"),
        "id": getattr(comp, "id", None),
        "active": None,
        "children": [
            _dom_tree(child)
            for child in (getattr(comp, "children", []) or [])
            if hasattr(child, "custom_attrs") or hasattr(child, "event_triggers")
        ],
    }


def _index_parents(node, parent=None, mapping=None):
    if mapping is None:
        mapping = {}
    mapping[id(node)] = parent
    for child in node["children"]:
        _index_parents(child, node, mapping)
    return mapping


def _closest(node, slot, parents):
    cur = node
    while cur is not None:
        if cur.get("slot") == slot:
            return cur
        cur = parents.get(id(cur))
    return None


def _descendants_with_slot(node, slot):
    out = []
    for child in node["children"]:
        if child.get("slot") == slot:
            out.append(child)
        out.extend(_descendants_with_slot(child, slot))
    return out


def _find_by_id(node, node_id):
    if node.get("id") == node_id:
        return node
    for child in node["children"]:
        found = _find_by_id(child, node_id)
        if found:
            return found
    return None


def _all_triggers(node):
    out = []
    for child in node["children"]:
        if child.get("slot") == "tabs-trigger":
            out.append(child)
        out.extend(_all_triggers(child))
    return out


def _simulate_mount(root):
    parents = _index_parents(root)
    for trigger in _all_triggers(root):
        group = _closest(trigger, "tabs", parents)
        trigger["active"] = (
            "true" if group and group.get("value") == trigger.get("value") else "false"
        )


def _simulate_click(root, trigger_node, with_guard):
    parents = _index_parents(root)
    group = _closest(trigger_node, "tabs", parents)
    if group is None:
        return
    clicked_value = trigger_node.get("value")
    group["value"] = clicked_value
    for target in _descendants_with_slot(group, "tabs-trigger"):
        own_group = _closest(target, "tabs", parents)
        if with_guard and own_group is not group:
            continue
        target["active"] = "true" if target.get("value") == clicked_value else "false"


def test_on_click_handler_contains_scope_guard():
    trigger = tabs.trigger("Home", value="home", id="t1")
    handlers = _extract_on_click_js(trigger)
    assert len(handlers) == 1
    assert GUARD_SUBSTRING in handlers[0]


def test_guard_preserves_nested_highlight_after_outer_click():
    nested = _build_nested_tree(default_inner="profile")
    dom = _dom_tree(nested)
    _simulate_mount(dom)
    outer_home = _find_by_id(dom, "outer-home")
    inner_prof = _find_by_id(dom, "inner-prof")
    inner_sec = _find_by_id(dom, "inner-sec")
    assert outer_home is not None
    assert inner_prof is not None
    assert inner_sec is not None
    assert inner_prof["active"] == "true"
    assert inner_sec["active"] == "false"
    _simulate_click(dom, outer_home, with_guard=True)
    assert outer_home["active"] == "true"
    outer_settings = _find_by_id(dom, "outer-settings")
    assert outer_settings is not None
    assert outer_settings["active"] == "false"
    assert inner_prof["active"] == "true", (
        "outer click must not clobber inner highlight"
    )
    assert inner_sec["active"] == "false"
    inner_root = _closest(inner_prof, "tabs", _index_parents(dom))
    assert inner_root is not None
    assert inner_root["value"] == "profile", (
        "outer click must not change inner root value"
    )


def test_nested_inner_group_remains_independently_switchable_with_guard():
    nested = _build_nested_tree(default_inner="profile")
    dom = _dom_tree(nested)
    _simulate_mount(dom)
    outer_settings = _find_by_id(dom, "outer-settings")
    assert outer_settings is not None
    _simulate_click(dom, outer_settings, with_guard=True)
    inner_sec = _find_by_id(dom, "inner-sec")
    inner_prof = _find_by_id(dom, "inner-prof")
    assert inner_sec is not None
    assert inner_prof is not None
    assert inner_prof["active"] == "true"
    _simulate_click(dom, inner_sec, with_guard=True)
    assert inner_sec["active"] == "true"
    assert inner_prof["active"] == "false"
    outer_root = _closest(outer_settings, "tabs", _index_parents(dom))
    assert outer_root is not None
    assert outer_root["value"] == "settings"


def test_flat_demo_guard_is_noop_for_outer_only_group():
    import importlib

    for label, (module_path, fn_name) in DEMO_MODULES.items():
        mod = importlib.import_module(module_path)
        comp = getattr(mod, fn_name)()
        dom = _dom_tree(comp)
        _simulate_mount(dom)
        triggers = _all_triggers(dom)
        for trigger in triggers:
            _simulate_click(dom, trigger, with_guard=True)
            expected = {
                t["id"]: ("true" if t["value"] == trigger["value"] else "false")
                for t in triggers
            }
            snapshot_after = {t["id"]: t["active"] for t in triggers}
            assert snapshot_after == expected, (
                f"{label}: click {trigger['id']} did not yield a single active trigger"
            )
            assert trigger["active"] == "true"
