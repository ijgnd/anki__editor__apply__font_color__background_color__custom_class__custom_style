import json
import re

from anki.utils import (
    isMac,
    isWin,
)
from aqt.editor import Editor

from ..config_var import getconfig
from ..vars import unique_string

from .text_wrap_escape_sequences import escape_seqs


def my_wrap_helper(editor, beforeAfter):
    before, after = beforeAfter.split(unique_string)
    # editor.web.eval(f"wrap('{before}', '{after}');")

    def find_escape_seq(match):
        return escape_seqs[match.group(1)](editor, match) if match.group(1) in escape_seqs else match.group(0)

    before_expanded = re.sub(r'%(.)', find_escape_seq, before)
    after_expanded = re.sub(r'%(.)', find_escape_seq, after)

    editor.web.eval(f"wrap({json.dumps(before_expanded)}, {json.dumps(after_expanded)});")


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


def setForecolor(editor, color):
    editor.web.eval("setFormat('forecolor', '%s')" % color)


def my_apply_style(editor, style):
    """
    # TODO editor.web.selectedText() is text without styling
    selected = editor.web.selectedText()
    styled = "".join(['<span style="{}">'.format(style), selected, '</span>'])
    # TODO use setFormat from editor.js from Anki ?
    editor.web.eval("document.execCommand('inserthtml', false, %s);"
                    % json.dumps(styled))
    """
    editor.web.eval(f"""dict["temporary_highlighter_for_styles"].highlightSelection('temp_styles_helper');""")
    js = """
        var matches = document.querySelectorAll(".temp_styles_helper");
        for (var i = 0; i < matches.length; i++) {
            matches[i].classList.remove("temp_styles_helper");
            matches[i].removeAttribute("style (inline)");  // delete old styling, https://stackoverflow.com/a/18691728
            matches[i].style.cssText = "NEWSTYLE"; // set new style, https://stackoverflow.com/a/3968772
                                                    // might only work if all other styling is removed
            }
    """.replace("NEWSTYLE", style.replace("\n", " "))
    editor.web.eval(js)


def my_wrap_in_class(editor, _class):
    js = f"classes_addon_wrap_helper('{_class}');"
    editor.web.eval(js)


def my_apply_span_class(editor, _class):
    # TODO there's no undo for this with ctrl+z
    # for undo you apparently should use document.execCommand(insertHTML), see
    # https://stackoverflow.com/questions/28217539/allowing-contenteditable-to-undo-after-dom-modification
    # But insertHTML doesn't help, because rangy by default directly modifies the page and not
    # some variable that I insert. So I'd have to look into rangy. Sounds complicated, very quick
    # search didn't render results.
    # WORKAROUND: use rangy.removeAllHighlights(), see  https://github.com/timdown/rangy/wiki/Highlighter-Module

    # workaround for issue18 "formatting is applied to more than selection"
    js_workaround = "classes_addon_wrap_span_helper(`%(CLASS)s`); "  % { "CLASS": _class }
    editor.web.eval(js_workaround)


    '''
    TODO: maybe only load rangy when command is called the first time?
some js 
"""
var rangy_loaded = None
function highlight_helper(_class){
    if (rangy_loaded) {
        dict[`{_class}highlighter`].highlightSelection(_class);
        highlighter, `{_class}`);
    }
}
"""
P: I'm losing focus when loading rangy: I use  focusField(0); in my "$(document).ready(function(){" function ...
   so how would I highlight a selection ...
   maybe pycmd so that I can use self.editor.web.setFocus() from QWebEngine ...?
    js =   f"""    highlight_helper('{_class}');   """
'''
    # js = f"""    dict["{_class}highlighter"].highlightSelection('{_class}');   """
    # editor.web.eval(js)
    for e in getconfig()['v3']:
        if e["Category"] == "class (other)" and e["Setting"] == _class and e.get("surround_with_div_tag"):
            editor.web.eval("classes_addon_wrap_helper();")
            break


apply_categories = {
    "class (other)": my_apply_span_class,
    "class (other), wrapped in div": my_wrap_in_class,
    "style (inline)": my_apply_style,
    "Backcolor (inline)": setBackcolor,
    "Backcolor (via class)": my_apply_span_class,
    "Forecolor (inline)": setForecolor,
    "Forecolor (via class)": my_apply_span_class,
    "font size (via class)": my_apply_span_class,
    "text wrapper": my_wrap_helper,
}
