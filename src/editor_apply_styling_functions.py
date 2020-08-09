"""
Copyright:  (c) 2019- ignd
            (c) 2014-2018 Stefan van den Akker
            (c) 2017-2018 Damien Elmes
            (c) 2018 Glutanimate
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Use this at your own risk
"""


import json
import re

from anki.hooks import addHook
from anki.utils import (
    isMac,
    isWin,
)
from aqt.editor import Editor

from .config_var import getconfig
from .vars import unique_string

from .text_wrap_escape_sequences import escape_seqs

def setmycategories(editor):
    editor.mycategories = {
        "class (other)": editor.my_apply_span_class,
        "class (other), wrapped in div": editor.my_wrap_in_class,
        "style (inline)": editor.my_apply_style,
        "Backcolor (inline)": editor.setBackcolor,
        "Backcolor (via class)": editor.my_apply_span_class,
        "Forecolor (inline)": editor.setForecolor,
        "Forecolor (via class)": editor.my_apply_span_class,
        "font size (via class)": editor.my_apply_span_class,
        "text wrapper": editor.my_wrap_helper,
    }


def my_wrap_helper(editor, beforeAfter):
    before, after = beforeAfter.split(unique_string)
    # editor.web.eval(f"wrap('{before}', '{after}');")

    def find_escape_seq(match):
        return escape_seqs[match.group(1)](editor, match) if match.group(1) in escape_seqs else match.group(0)

    before_expanded = re.sub(r'%(.)', find_escape_seq, before)
    after_expanded = re.sub(r'%(.)', find_escape_seq, after)

    editor.web.eval(f"wrap({json.dumps(before_expanded)}, {json.dumps(after_expanded)});")
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
    """.replace("NEWSTYLE", style)
    editor.web.eval(js)
Editor.my_apply_style = my_apply_style


def my_wrap_in_class(editor, _class):
    js = f"classes_addon_wrap_helper('{_class}');"
    editor.web.eval(js)
Editor.my_wrap_in_class = my_wrap_in_class


def my_apply_span_class(editor, _class):
    # TODO there's no undo for this with ctrl+z
    # for undo you apparently should use document.execCommand(insertHTML), see
    # https://stackoverflow.com/questions/28217539/allowing-contenteditable-to-undo-after-dom-modification
    # But insertHTML doesn't help, because rangy by default directly modifies the page and not
    # some variable that I insert. So I'd have to look into rangy. Sounds complicated, very quick
    # search didn't render results.
    # WORKAROUND: use rangy.removeAllHighlights(), see  https://github.com/timdown/rangy/wiki/Highlighter-Module



    # workaround for issue18 "formatting is applied to more than selection"
    js_workaround= """
var cla_sel_str = window.getSelection().toString();
var cla_sel_html = selectionAsHtml();

if (cla_sel_str == cla_sel_html){
    classes_addon_wrap_span_helper('%(CLASS)s');
}
else {
    var action = dict["%(CLASS)shighlighter"];
    action.highlightSelection('%(CLASS)s');
}

"""  % { 
"CLASS": _class,
}
    editor.web.eval(js_workaround)




    
    
    '''
    TODO: maybe only load rangy when command is called the first time?
some js 
"""
var rangy_loaded = None
function highlight_helper(_class){
    if (rangy_loaded){
        dict[`{_class}highlighter`].highlightSelection(_class);
        highlighter, '{_class}');
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
Editor.my_apply_span_class = my_apply_span_class


def classes_addon_rangy_remove_all(editor):
    # this only works on stuff rangy has highlighted before: so it doesn't help in the browser.
    js = """
Object.values(dict).forEach(function (item, index) {
    item.removeAllHighlights();
    console.log(item);
});
"""
    # TODO
    #js = """classes_addon__remove_classes_from_selection();"""
    #editor.web.eval(js)
    
    # at least I can undo the following (which is arguably more important than keeping other formatting)
    text = editor.web.selectedText()
    editor.web.eval("setFormat('inserthtml', %s);" % json.dumps(text))
