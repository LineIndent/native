---
title: "Switch"
description: "A control that allows the user to toggle between checked and not checked."
order: 0
---

--INTRO([Switch, A control that allows the user to toggle between checked and not checked.])--

--USAGE(switch)--

--SOURCE(switch)--

# Examples

## Basic

A simple switch rendering an internal semantic label using the inline `label_text` argument.

**Props used:** `label_text` as the first argument in `switch.root`.

--DEMO(switch_basic)--


## Choice Card

Card-style premium selection where `field.label` wraps the entire layout block. Clicking anywhere on the card container natively triggers the nested switch checkbox.

**Props used:** `id` on `switch.root`; `html_for` on `field.label`.

--DEMO(switch_with_label)--

## Sizes

Two size variants available side by side—`sm` for tight, compact toolbars or layouts, and the `default` size for normal structural form elements.

**Props used:** `size` on `switch.root`; `orientation="horizontal"` on `field.root`.

--DEMO(switch_sizes)--

## Invalid

An invalid or error state signaling form validation failures. The switch track highlights structural errors through `aria-invalid`, and the parent `field.root` dynamically updates text styling to the system's destructive state.

**Props used:** `invalid` on `switch.root`; `data-invalid="true"` on `field.root`.

--DEMO(switch_invalid)--

## Disabled

A disabled switch control with interaction constraints. Disabling cascades visually and functionally down to the control via structural `group-has-[:disabled]` selectors, lowering control opacity and locking out all user inputs.

**Props used:** `disabled` on `switch.root`; `data-disabled="true"` on `field.root`.

--DEMO(switch_disabled)--

# API Reference

## switch.root

The main switch control component. Renders an accessible, zero-latency toggle using a native hidden checkbox input element wrapped in a clickable semantic label layout block.

```python
switch.root("Enable notifications", id="notify", size="default")
```

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `label_text` | `str` | `""` | Optional descriptive label string inserted directly alongside the switch. |
| `size` | `Literal["default", "sm"]` | `"default"` | Sets the physical width/height scaling of the track and thumb elements. |
| `invalid` | `bool` | `False` | Sets `aria-invalid="true"` to trigger error styling. |
| `disabled` | `bool` | `False` | Disables interaction and drops opacity. |
| `checked` | `bool` |  | Controlled component state binding. |
| `default_checked` | `bool` |  | Uncontrolled default initial state setting. |
| `track_class_name` | `str` | `""` | Fine-grain custom Tailwind class overrides directly injected onto the track. |
| `thumb_class_name` | `str` | `""` | Fine-grain custom Tailwind class overrides directly injected onto the thumb. |
| `id` | `str` |  | Unique identifier assigned directly to the inner hidden input peer. |
| `name` | `str` |  | Form submission parameter identifier. |
| `on_change` | `EventHandler` |  | Fired instantly as soon as the switch toggle changes state. |

Any other attribute accepted by a standard HTML `<input type="checkbox">` (`required`, `value`, etc.) will pass straight through to the inner input control peer.
