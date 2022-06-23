from aqt.gui_hooks import (
    editor_did_init,
    editor_will_load_note,
    webview_will_set_content,
)

from .editor_set_css_js_for_webview import (
    eval_base_js,
    append_css_to_Editor,
)


def init_webview():
    editor_did_init.append(eval_base_js)
    editor_will_load_note.append(append_css_to_Editor)
