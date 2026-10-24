import reflex as rx

GUARD_SUBSTRING = "closest('[data-slot=\"tabs\"]') !== root"

from components.ui.tabs import GLOBAL_HANDLERS_JS, tabs


def _walk(comp):
    yield comp
    for child in getattr(comp, "children", []) or []:
        if hasattr(child, "event_triggers"):
            yield from _walk(child)


def _js(comp, trigger):
    out = []
    for node in _walk(comp):
        spec = (getattr(node, "event_triggers", {}) or {}).get(trigger)
        if spec is None:
            continue
        stack = list(getattr(spec, "events", None) or [spec])
        while stack:
            item = stack.pop()
            if isinstance(item, (list, tuple)):
                stack.extend(item)
                continue
            if isinstance(item, rx.event.EventSpec):
                stack.extend(item.args)
                continue
            try:
                value = item._var_value
            except Exception:
                continue
            if isinstance(value, str):
                out.append(value)
    return out


def _root(**kw):
    return tabs.root(
        tabs.list(tabs.trigger("Home", value="home")),
        tabs.content("p", value="home"),
        default_value="home",
        **kw,
    )


def test_trigger_bakes_no_id_or_highlight_js():
    t = tabs.trigger("Home", value="home")
    assert getattr(t, "id", None) is None
    assert _js(t, "on_click") == []
    assert _js(t, "on_mount") == []
    assert getattr(tabs.trigger("H", value="h", id="x"), "id", None) == "x"


def test_root_attaches_delegated_runtime_handler():
    js = [j for j in _js(_root(), "on_mount") if "addEventListener" in j]
    assert len(js) == 1
    assert js[0] == GLOBAL_HANDLERS_JS
    for bad in ("getElementById", "{value}", "{trigger_id}", "=== '", "dataset.value = '"):
        assert bad not in GLOBAL_HANDLERS_JS
    assert "getAttribute('data-value')" in GLOBAL_HANDLERS_JS


def test_user_handlers_preserved():
    blocks = _js(_root(on_mount=rx.call_script("mark_mount")), "on_mount")
    assert any("mark_mount" in b for b in blocks)
    assert any("addEventListener" in b for b in blocks)
    t = tabs.trigger("H", value="h", on_click=rx.call_script("mark_click"))
    assert any("mark_click" in b for b in _js(t, "on_click"))


def test_delegated_listener_scopes_to_clicked_tabs_group():
    from components.ui.tabs import GLOBAL_HANDLERS_JS

    assert GUARD_SUBSTRING in GLOBAL_HANDLERS_JS
