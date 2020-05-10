import os

from aqt import mw
from aqt.editor import Editor


from .vars import (
    addon_folder_name,
    css_path,
    css_path_Customize_Editor_Stylesheet,
    js_to_append,
    old_anki,
)
from .config import get_css_for_editor_from_config, highlighter_js_code


# before 2.1.22
def prepareEditorStylesheet():
    css1 = ""
    if os.path.isfile(css_path()):
        with open(css_path(), "r") as css_file:
            css1 = css_file.read()
    css2 = ""
    if os.path.isfile(css_path_Customize_Editor_Stylesheet()):
        with open(css_path_Customize_Editor_Stylesheet(), "r") as css_file:
            css2 = css_file.read()
    # TODO adjust height of buttons, maybe add option to make wider, see
    # https://www.reddit.com/r/Anki/comments/ce9wk7/bigger_edit_icons/
    # css2 first in case it contains @import url
    css = css2 + "\n" + css1
    editor_style = "<style>\n{}\n</style>".format(css.replace("%", "%%"))
    editor._html = editor_style + editor._html





def append_js_to_Editor(web_content, context):
    if isinstance(context, Editor):
        for f in js_to_append:
            if f not in web_content.js:
                web_content.js.append(f"/_addons/{addon_folder_name}/web/{f}")
        web_content.head += f"""
<script>
{highlighter_js_code()}
</script>
"""


def append_css_to_Editor(web_content, context):
    if isinstance(context, Editor):
        web_content.head += f"""\n<style>\n{get_css_for_editor_from_config()}\n</style>\n"""
        




# def on_webview_will_set_content(web_content: WebContent, context):
#     if not isinstance(context, Editor):
#         return
#     web_content.js.append(f"/_addons/{foldername}/web/js.js")
# gui_hooks.webview_will_set_content.append(on_webview_will_set_conten


def set_css_js_for_editor():
    if old_anki:
        from aqt import editor
        from anki.hooks import addHook
        addHook("profileLoaded", prepareEditorStylesheet)
    else:
        from aqt import gui_hooks
        gui_hooks.webview_will_set_content.append(append_js_to_Editor)
        gui_hooks.webview_will_set_content.append(append_css_to_Editor)
