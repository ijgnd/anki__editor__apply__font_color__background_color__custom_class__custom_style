from aqt.gui_hooks import (
    editor_will_show_context_menu,
    editor_did_init_buttons,
    editor_did_init_shortcuts,
)

from .contextmenu import setup_contextmenu
from .buttons import setup_extra_buttons, setup_more_button
from .shortcuts import setup_shortcuts, setup_styling_undo_shortcut


def init_editor():
    editor_will_show_context_menu.append(setup_contextmenu)

    editor_did_init_buttons.append(setup_extra_buttons)
    editor_did_init_buttons.append(setup_more_button)

    editor_did_init_shortcuts.append(setup_shortcuts)
    editor_did_init_shortcuts.append(setup_styling_undo_shortcut)
