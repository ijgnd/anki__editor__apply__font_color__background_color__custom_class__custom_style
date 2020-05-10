# Copyright:  (c) 2019- ignd
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from pprint import pprint as pp

from aqt import mw

from . import config_var


def getconfig():
    #return mw.col.get_config("1899278645_config")
    return config_var.myconfig


'''
def rangy_js_str_for_class(classname):
    return f"""
        var {classname}highlighter;
        {classname}highlighter = rangy.createHighlighter();
        {classname}highlighter.addClassApplier(rangy.createClassApplier('{classname}'));
"""

def highlighter_js_code():
    js_str = "rangy.init();"
    for e in getconfig()["v3"]:
        if e["Category"] in  ["class (other)", "Backcolor (via class)"]:
            # class name is e["Setting"]
            js_str += rangy_js_str_for_class(e["Setting"])
    return js_str
'''


uses_classes = [
    "class (other)",
    "Backcolor (via class)",
    "Forecolor (via class)",
    "font size (via class)",
]


def highlighter_js_code():
    # workaround for error with checkExist
    # JS info /_addons/1899278645/web/rangy-core.js:10 Rangy is not supported in this environment. Reason: No body element found

    js_str = ""
    for e in getconfig()["v3"]:
        if e["Category"] in uses_classes:
            js_str += f"""var {e["Setting"]}highlighter;\n"""

    js_str += """
var checkExist = setInterval(function() {
if ($('body').length) {
    rangy.init();
"""

    for e in getconfig()["v3"]:
        if e["Category"] in uses_classes:
            classname = e["Setting"]
            js_str += f"""
{classname}highlighter = rangy.createHighlighter();
{classname}highlighter.addClassApplier(rangy.createClassApplier('{classname}'));
"""

    js_str += """
      clearInterval(checkExist);
   }
}, 30);  // 50ms
"""
    return js_str


def get_css_for_editor_from_config():
    classes_str = ""
    for e in getconfig()["v3"]:
        if e["Category"] in ["class (other)"]:
            classes_str += ("." + str(e["Setting"]) +
                            "{\n" + str(e['Text_in_menu_styling']) +
                            "\n}\n\n"
                            ".nightMode ." + str(e["Setting"]) +
                            "{\n" + str(e['Text_in_menu_styling_nightmode']) +
                            "\n}\n\n"
                            )
        if e["Category"] in ["Backcolor (via class)"]:
            classes_str += ("." + str(e["Setting"]) +
                            "{\nbackground-color: " + str(e['Text_in_menu_styling']) + " !important;" +
                            "\n}\n\n"
                            ".nightMode ." + str(e["Setting"]) +
                            "{\nbackground-color: " + str(e['Text_in_menu_styling_nightmode']) + " !important;" +
                            "\n}\n\n"
                            )
        if e["Category"] in ["Forecolor (via class)"]:
            classes_str += ("." + str(e["Setting"]) +
                            "{\ncolor: " + str(e['Text_in_menu_styling']) + " !important;" +
                            "\n}\n\n"
                            ".nightMode ." + str(e["Setting"]) +
                            "{\ncolor: " + str(e['Text_in_menu_styling_nightmode']) + " !important;" +
                            "\n}\n\n"
                            )
        if e["Category"] in ["font size (via class)"]:
            classes_str += ("." + str(e["Setting"]) +
                            "{\nfont-size: " + str(e['Text_in_menu_styling']) + " !important;" +
                            "\n}\n\n"
                            )
    return classes_str
