from aqt.gui_hooks import (
    profile_did_open,
    editor_did_init_buttons,
    editor_did_init_shortcuts,
    editor_will_show_context_menu,
)

from ..config_var import getconfig

from .contextmenu import add_to_context
from .buttons import setup_extra_buttons, setup_more_button
from .shortcuts import setup_shortcuts


def contextmenu():
    if getconfig().get("v2_show_in_contextmenu", False):
        editor_will_show_context_menu.append(add_to_context)

def init_editor():
    profile_did_open.append(contextmenu)

    editor_did_init_buttons.append(setup_extra_buttons)
    editor_did_init_buttons.append(setup_more_button)

    editor_did_init_shortcuts.append(setup_shortcuts)
