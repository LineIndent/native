"""Regression coverage for the dialog popup crash when ``dismissible=False``
or ``on_open_change=...`` was passed to ``dialog.popup(...)``.

Both options previously raised at component-construction time:

    ValueError: The Dialog does not take in an 'on_cancel' event trigger
    ValueError: The Dialog does not take in an 'on_close' event trigger

because ``DialogPopup`` wired ``on_cancel`` / ``on_close`` into ``props`` and
passed them to ``rx.el.dialog(...)``, whose underlying element does not declare
those triggers. The tests pin the four contracts the fix restored:
``DialogPopup`` declares ``on_close`` / ``on_cancel`` as class-level triggers,
the popup renders a native ``<dialog>`` with ``data-slot="dialog-content"``,
``dismissible=False`` wires ``on_cancel`` only, and ``on_open_change=`` wires
``on_close`` only. See bug #4 and PR #23.
"""

import reflex as rx
from reflex_components_core.el.elements.other import Dialog

from components.ui.dialog import DialogPopup, dialog


class _DialogState(rx.State):  # pyright: ignore [reportUntypedBaseClass]
    open: bool = True

    def set_open(self, *, value: bool) -> None:
        self.open = value


def test_dialog_popup_declares_on_close_and_on_cancel_triggers():
    triggers = DialogPopup.get_event_triggers()
    assert "on_close" in triggers
    assert "on_cancel" in triggers


def test_popup_is_a_dialog_element_with_data_slot():
    popup = dialog.popup(dialog.title("title"), dismissible=False)
    assert isinstance(popup, Dialog)
    assert popup.tag == "dialog"
    assert popup.custom_attrs.get("data-slot") == "dialog-content"


def test_dismissible_false_wires_on_cancel():
    popup = dialog.popup(dialog.title("title"), dismissible=False)
    assert "on_cancel" in popup.event_triggers
    assert "on_close" not in popup.event_triggers


def test_on_open_change_wires_on_close():
    popup = dialog.popup(dialog.title("title"), on_open_change=_DialogState.set_open)
    assert "on_close" in popup.event_triggers
    assert "on_cancel" not in popup.event_triggers
