from aqt.gui_hooks import (
    editor_will_load_note,
    editor_will_show_context_menu,
    editor_did_init_buttons,
    editor_did_init_shortcuts,
    editor_did_init,
)

from .contextmenu import setup_contextmenu
from .buttons import setup_extra_buttons, setup_more_button
from .shortcuts import setup_shortcuts
from .setup_categories import setup_categories
from .webview import append_css_to_Editor, eval_base_js


def init_editor():
    editor_will_load_note.append(append_css_to_Editor)
    editor_will_show_context_menu.append(setup_contextmenu)
    editor_did_init_buttons.append(setup_extra_buttons)
    editor_did_init_buttons.append(setup_more_button)
    editor_did_init_shortcuts.append(setup_shortcuts)
    editor_did_init.append(eval_base_js)
    editor_did_init.append(setup_categories)
