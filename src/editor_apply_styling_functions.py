"""
Copyright:  (c) 2019- ignd
            (c) 2014-2018 Stefan van den Akker
            (c) 2017-2018 Damien Elmes
            (c) 2018 Glutanimate
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Use this at your own risk
"""


import json

from anki.hooks import addHook
from anki.utils import (
    isMac,
    isWin,
)
from aqt.editor import Editor

from .config_var import getconfig
from .vars import unique_string


def setmycategories(editor):
    editor.mycategories = {
        "class (other)": editor.my_apply_span_class,
        "style": editor.my_apply_style,
        "Backcolor (inline)": editor.setBackcolor,
        "Backcolor (via class)": editor.my_apply_span_class,
        "Forecolor": editor.setForecolor,
        "Forecolor (via class)": editor.my_apply_span_class,
        "font size (via class)": editor.my_apply_span_class,
        "text wrapper": editor.my_wrap_helper,
    }


def my_wrap_helper(editor, beforeAfter):
    before, after = beforeAfter.split(unique_string)
    # editor.web.eval(f"wrap('{before}', '{after}');")
    editor.web.eval(f"wrap({json.dumps(before)}, {json.dumps(after)});")
Editor.my_wrap_helper = my_wrap_helper


def setBackcolor(editor, color):
    # from miniformat pack _wrapWithBgColour
    """
    Wrap the selected text in an appropriate tag with a background color.
    """
    # On Linux, the standard 'hiliteColor' method works. On Windows and OSX
    # the formatting seems to get filtered out

    editor.web.eval("""
        if (!setFormat('hiliteColor', '%s')) {
            setFormat('backcolor', '%s');
        }
        """ % (color, color))

    if isWin or isMac:
        # remove all Apple style classes, which is needed for
        # text highlighting on platforms other than Linux
        editor.web.eval("""
            var matches = document.querySelectorAll(".Apple-style-span");
            for (var i = 0; i < matches.length; i++) {
                matches[i].removeAttribute("class");
            }
        """)
Editor.setBackcolor = setBackcolor


def setForecolor(editor, color):
    editor.web.eval("setFormat('forecolor', '%s')" % color)
Editor.setForecolor = setForecolor


def my_apply_style(editor, style):
    # TODO editor.web.selectedText() is text without styling
    selected = editor.web.selectedText()
    styled = "".join(['<span style="{}">'.format(style), selected, '</span>'])
    # TODO use setFormat from editor.js from Anki ?
    editor.web.eval("document.execCommand('inserthtml', false, %s);"
                    % json.dumps(styled))
Editor.my_apply_style = my_apply_style


def my_apply_span_class(editor, _class):
    # TODO there's no undo for this with ctrl+z
    # for undo you apparently should use document.execCommand(insertHTML), see
    # https://stackoverflow.com/questions/28217539/allowing-contenteditable-to-undo-after-dom-modification
    # But insertHTML doesn't help, because rangy by default directly modifies the page and not
    # some variable that I insert. So I'd have to look into rangy. Sounds complicated, very quick
    # search didn't render results.
    # WORKAROUND: use rangy.removeAllHighlights(), see  https://github.com/timdown/rangy/wiki/Highlighter-Module
    editor.web.eval(f"""dict["{_class}highlighter"].highlightSelection('{_class}');""")
    for e in getconfig()['v3']:
        if e["Category"] == "class (other)" and e["Setting"] == _class and e["surround_with_div_tag"]:
            editor.web.eval("classes_addon_wrap_helper();")
            break
Editor.my_apply_span_class = my_apply_span_class
