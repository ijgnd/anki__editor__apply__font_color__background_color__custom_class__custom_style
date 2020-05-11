# Copyright:  (c) 2019- ignd
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from pprint import pprint as pp

import aqt
from aqt import mw

from . import config_var


def getconfig():
    #return mw.col.get_config("1899278645_config")
    return config_var.myconfig


# This code doesn't work on my main machine: In the js debug console I get
#    JS info /_addons/1899278645/web/rangy-core.js:10 Rangy is not supported in this 
#    environment.  Reason: No body element found
# def rangy_js_str_for_class(classname):
#     return f"""
#         var {classname}highlighter;
#         {classname}highlighter = rangy.createHighlighter();
#         {classname}highlighter.addClassApplier(rangy.createClassApplier('{classname}'));
# """
#
# def highlighter_js_code():
#     js_str = "rangy.init();"
#     for e in getconfig()["v3"]:
#         if e["Category"] in  ["class (other)", "Backcolor (via class)"]:
#             # class name is e["Setting"]
#             js_str += rangy_js_str_for_class(e["Setting"])
#     return js_str



uses_classes = [
    "class (other)",
    "Backcolor (via class)",
    "Forecolor (via class)",
    "font size (via class)",
]



# highlighter_js_code in combination with editor_set_css_js_for_webview.append_js_to_Editor
# works on my main machine but not in Window in 2020-05-11.
# So I made the workaround below with var_script_load_template, var_rangyfiles, and
# add_js_to_editor_html. I also added the css/styling into this function so that I no longer
# require the gui_hook from 2.1.22
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
}, 1500);  // 1.5 seconds
"""
    return js_str


# https://stackoverflow.com/questions/3857874/how-to-dynamically-insert-a-script-tag-via-jquery-after-page-load
var_script_load_template = """
<script type="text/javascript">
$(document).ready(function() 
{
    var s = document.createElement("script");
    s.type = "text/javascript";
    s.src = "LOCATION";
    $("head").append(s);
});
</script>
"""


var_rangyfiles = [
    "http://127.0.0.1:PORTPORT/_addons/1899278645/web/rangy-core.js",
    "http://127.0.0.1:PORTPORT/_addons/1899278645/web/rangy-serializer.js",
    "http://127.0.0.1:PORTPORT/_addons/1899278645/web/rangy-textrange.js",
    "http://127.0.0.1:PORTPORT/_addons/1899278645/web/rangy-highlighter.js",
    "http://127.0.0.1:PORTPORT/_addons/1899278645/web/rangy-selectionsaverestore.js",
    "http://127.0.0.1:PORTPORT/_addons/1899278645/web/rangy-classapplier.js",
]


def extend_editor_html_variable_with_js_and_css():
    # this modifies editor._html. Before editor._html is used included placeholders are filled
    # by using c-style replacements. So everything with % gets replaced. To keep "%" I need to 
    # double them
    s = ""
    for f in var_rangyfiles:
        fmted = f.replace("PORTPORT", str(mw.mediaServer.getPort()))
        s +=  var_script_load_template.replace("LOCATION", fmted).replace("%", "%%")
    s += "\n<script>\n" + highlighter_js_code() +  "\n</script>\n".replace("%", "%%")
    s += f"""\n<style>\n{get_css_for_editor_from_config()}\n</style>\n""".replace("%", "%%")
    aqt.editor._html = s + aqt.editor._html


def get_nm_style(configkey):
    e = configkey
    nmsetting = e['Text_in_menu_styling_nightmode']
    if nmsetting:
        nmstyle = str(nmsetting)
    else:
        nmstyle = str(e['Text_in_menu_styling'])
    return nmstyle


def get_css_for_editor_from_config():
    classes_str = ""
    for e in getconfig()["v3"]:
        nmstyle = get_nm_style(e)
        if e["Category"] in ["class (other)"]:
            classes_str += ("." + str(e["Setting"]) +
                            "{\n" + str(e['Text_in_menu_styling']) +
                            "\n}\n\n"
                            ".nightMode ." + str(e["Setting"]) +
                            "{\n" + nmstyle +
                            "\n}\n\n"
                            )
        if e["Category"] in ["Backcolor (via class)"]:
            classes_str += ("." + str(e["Setting"]) +
                            "{\nbackground-color: " + str(e['Text_in_menu_styling']) + " !important;" +
                            "\n}\n\n"
                            ".nightMode ." + str(e["Setting"]) +
                            "{\nbackground-color: " + nmstyle + " !important;" +
                            "\n}\n\n"
                            )
        if e["Category"] in ["Forecolor (via class)"]:
            classes_str += ("." + str(e["Setting"]) +
                            "{\ncolor: " + str(e['Text_in_menu_styling']) + " !important;" +
                            "\n}\n\n"
                            ".nightMode ." + str(e["Setting"]) +
                            "{\ncolor: " + nmstyle + " !important;" +
                            "\n}\n\n"
                            )
        if e["Category"] in ["font size (via class)"]:
            classes_str += ("." + str(e["Setting"]) +
                            "{\nfont-size: " + str(e['Text_in_menu_styling']) + " !important;" +
                            "\n}\n\n"
                            )
    return classes_str
