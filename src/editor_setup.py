import os

from aqt import editor
from aqt import mw

from .vars import (
    css_path,
    css_path_Customize_Editor_Stylesheet,
)

def prepareEditorStylesheet():
    config = mw.addon_custom_class_config
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


def onEditorInit(self, *args, **kwargs):
    """Apply modified Editor HTML"""
    # TODO night mode
    pass


# Editor.__init__ = wrap(Editor.__init__, onEditorInit, "after")