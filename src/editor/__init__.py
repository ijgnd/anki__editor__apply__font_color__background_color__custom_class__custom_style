from aqt.gui_hooks import (
    profile_did_open,
    editor_did_init_buttons,
    editor_did_init_shortcuts,
    editor_will_show_context_menu,
)

from ..config_var import getconfig

from .shortcuts_buttons import setupButtons, SetupShortcuts
from .contextmenu import add_to_context


def contextmenu():
    if getconfig().get("v2_show_in_contextmenu", False):
        editor_will_show_context_menu.append(add_to_context)


def init_editor():
    profile_did_open.append(contextmenu)
    editor_did_init_buttons.append(setupButtons)
    editor_did_init_shortcuts.append(SetupShortcuts)
