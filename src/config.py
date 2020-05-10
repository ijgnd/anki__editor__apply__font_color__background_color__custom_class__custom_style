from aqt import mw

config = {}


def getconfig():
    return mw.col.get_config("1899278645_config")


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
        if e["Category"] in  ["class", "Backcolor (via class)"]:
            # class name is e["Setting"]
            js_str += rangy_js_str_for_class(e["Setting"])
    return js_str
'''


def highlighter_js_code():
    # workaround for error with checkExist
    # JS info /_addons/1899278645/web/rangy-core.js:10 Rangy is not supported in this environment. Reason: No body element found

    js_str = ""
    for e in getconfig()["v3"]:
        if e["Category"] in  ["class", "Backcolor (via class)"]:
            js_str += f"""var {e["Setting"]}highlighter;\n"""

    js_str += """
var checkExist = setInterval(function() {
if ($('body').length) {
    rangy.init();
"""

    for e in getconfig()["v3"]:
        if e["Category"] in  ["class", "Backcolor (via class)"]:
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
        if e["Category"] in ["class"]:
            classes_str += ("." + str(e["Setting"]) +
                            "{\n" + str(e['Text_in_menu_styling']) +
                            "\n}\n\n"
                            ".nightMode ." + str(e["Setting"]) +
                            "{\n" + str(e['Text_in_menu_styling_nightmode']) +
                            "\n}\n\n"
                            )
        if e["Category"] == "Backcolor (via class)":
            classes_str += ("." + str(e["Setting"]) +
                            "{\nbackground-color: " + str(e['Text_in_menu_styling']) + " !important;" +
                            "\n}\n\n"
                            ".nightMode ." + str(e["Setting"]) +
                            "{\nbackground-color: " + str(e['Text_in_menu_styling_nightmode']) + " !important;" +
                            "\n}\n\n"
                            )
    return classes_str
