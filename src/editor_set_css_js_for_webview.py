# Copyright:  (c) 2019- ignd
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os

from aqt import gui_hooks
from aqt import mw
from aqt.editor import Editor

from .vars import (
    addon_folder_name,
    css_path,
    css_path_Customize_Editor_Stylesheet,
    js_to_append,
)
from .config import get_css_for_editor_from_config, highlighter_js_code


def append_js_to_Editor(web_content, context):
    if isinstance(context, Editor):
        for f in js_to_append:
            if f not in web_content.js:
                web_content.js.append(f"/_addons/{addon_folder_name}/web/{f}")
        web_content.head += f"""\n<script>\n{highlighter_js_code()}\n</script>\n"""


def append_css_to_Editor(web_content, context):
    if isinstance(context, Editor):
        web_content.head += f"""\n<style>\n{get_css_for_editor_from_config()}\n</style>\n"""



gui_hooks.webview_will_set_content.append(append_js_to_Editor)
gui_hooks.webview_will_set_content.append(append_css_to_Editor)
