import json
import re

from anki.utils import (
    isMac,
    isWin,
)

from ..config_var import getconfig
from ..vars import unique_string

from .text_wrap_escape_sequences import escape_seqs


def wrap_text(editor, beforeAfter):
    before, after = beforeAfter.split(unique_string)

    def find_escape_seq(match):
        return (
            escape_seqs[match.group(1)](editor, match)
            if match.group(1) in escape_seqs
            else match.group(0)
        )

    before_expanded = re.sub(r"%(.)", find_escape_seq, before)
    after_expanded = re.sub(r"%(.)", find_escape_seq, after)

    editor.web.eval(
        f"wrap({json.dumps(before_expanded)}, {json.dumps(after_expanded)});"
    )


def set_backcolor(editor, color):
    # from miniformat pack _wrapWithBgColour
    """
    Wrap the selected text in an appropriate tag with a background color.
    """
    # On Linux, the standard 'hiliteColor' method works. On Windows and OSX
    # the formatting seems to get filtered out

    editor.web.eval(
        """
        if (!setFormat('hiliteColor', '%s')) {
            setFormat('backcolor', '%s');
        }
        """
        % (color, color)
    )

    if isWin or isMac:
        # remove all Apple style classes, which is needed for
        # text highlighting on platforms other than Linux
        editor.web.eval(
            """
            var matches = document.querySelectorAll(".Apple-style-span");
            for (var i = 0; i < matches.length; i++) {
                matches[i].removeAttribute("class");
            }
        """
        )


def set_forecolor(editor, color):
    editor.web.eval("setFormat('forecolor', '%s')" % color)


def apply_style(editor, style):
    editor.web.eval(
        """dict["temporary_highlighter_for_styles"].highlightSelection('temp_styles_helper');"""
    )
    js = """
const matches = document.querySelectorAll(".temp_styles_helper");

for (var i = 0; i < matches.length; i++) {
    matches[i].classList.remove("temp_styles_helper");
    matches[i].removeAttribute("style (inline)");  // delete old styling, https://stackoverflow.com/a/18691728
    matches[i].style.cssText = "NEWSTYLE"; // set new style, https://stackoverflow.com/a/3968772
                                            // might only work if all other styling is removed
}
""".replace(
        "NEWSTYLE", style.replace("\n", " ")
    )
    editor.web.eval(js)


def apply_div_class(editor, class_name):
    key = f"div{class_name}"
    editor.web.eval(
        f"""
if (!({json.dumps(key)} in customStylesDict)) {{
    customStylesDict[{json.dumps(key)}] = classesAddonWrapDivHelper({json.dumps(class_name)});
}}

customStylesDict[{json.dumps(key)}].then((surrounder) => surrounder());
"""
    )


def apply_span_class(editor, class_name):
    key = f"span{class_name}"
    editor.web.eval(
        f"""
if (!({json.dumps(key)} in customStylesDict)) {{
    customStylesDict[{json.dumps(key)}] = classesAddonWrapSpanHelper({json.dumps(class_name)});
}}

customStylesDict[{json.dumps(key)}].then((surrounder) => surrounder());
"""
    )

    for e in getconfig()["v3"]:
        if (
            e["Category"] == "class (other)"
            and e["Setting"] == class_name
            and e.get("surround_with_div_tag")
        ):
            editor.web.eval("classesAddonWrapDivHelper();")
            break


apply_categories = {
    "text wrapper": wrap_text,
    "class (other)": apply_span_class,
    "class (other), wrapped in div": apply_div_class,
    "style (inline)": apply_style,
    "Backcolor (inline)": set_backcolor,
    "Backcolor (via class)": apply_span_class,
    "Forecolor (inline)": set_forecolor,
    "Forecolor (via class)": apply_span_class,
    "font size (via class)": apply_span_class,
}
