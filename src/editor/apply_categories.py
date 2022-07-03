import json
import re

from anki.utils import (
    is_mac,
    is_win,
)

from ..vars import unique_string

from .text_wrap_escape_sequences import escape_seqs


def wrap_text(editor, entry):
    beforeAfter = entry["Setting"]
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


def set_backcolor(editor, entry):
    color = entry["Setting"]
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

    if is_win or is_mac:
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


def set_forecolor(editor, entry):
    color = entry["Setting"]
    editor.web.eval("setFormat('forecolor', '%s')" % color)


def apply_style(editor, entry):
    style = entry["Setting"]
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


def apply_div_class(editor, entry):
    class_name = entry["Setting"]
    key = f"div{class_name}"
    editor.web.eval(
        f"""
if (!({json.dumps(key)} in customStylesDict)) {{
    customStylesDict[{json.dumps(key)}] = classesAddonWrapDivHelper({json.dumps(class_name)});
}}

customStylesDict[{json.dumps(key)}].then((surrounder) => surrounder());
"""
    )


def apply_span_class(editor, entry):
    class_name = entry["Setting"]
    key = f"span{class_name}"
    editor.web.eval(
        f"""
customStylesDict[{json.dumps(key)}].then((surrounder) => surrounder());
"""
    )

    if entry["Category"] == "class (other)" and entry.get("surround_with_div_tag"):
        editor.web.eval("classesAddonWrapDivHelper();")


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
