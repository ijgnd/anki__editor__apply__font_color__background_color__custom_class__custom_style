# Copyright:  (c) 2019- ignd
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os

from aqt import gui_hooks
from aqt import mw
from aqt.editor import Editor

from .vars import (
    addon_folder_name,
    css_path,
    css_path_Customize_Editor_Stylesheet,
    js_to_append,
    uses_classes,
)
from .config import (
    getconfig,
)
from .css_for_webviews import create_css_for_webviews_from_config

def rangy__create_global_variables_for_later_use():
    jsstring = ""
    for e in getconfig()["v3"]:
        if e["Category"] in uses_classes:
            jsstring += f"""\nvar {e["Setting"]}highlighter;"""
    return jsstring


def rangy_higlighters_for_each_class():
    js_str = ""
    for e in getconfig()["v3"]:
        if e["Category"] in uses_classes:
            classname = e["Setting"]
            js_str += f"""
    {classname}highlighter = rangy.createHighlighter();
    {classname}highlighter.addClassApplier(rangy.createClassApplier('{classname}'));
"""
    return js_str


def append_js_to_Editor(web_content, context):
    if isinstance(context, Editor):
        web_content.head += f"""\n<script>\n{rangy__create_global_variables_for_later_use()}\n</script>\n"""
gui_hooks.webview_will_set_content.append(append_js_to_Editor)


def append_css_to_Editor(web_content, context):
    if isinstance(context, Editor):
        web_content.head += f"""\n<style>\n{create_css_for_webviews_from_config()}\n</style>\n"""
gui_hooks.webview_will_set_content.append(append_css_to_Editor)


def js_inserter(self):
    # load rangy and create highlighters
    # rangy is inserted/loaded here and not with webview_will_set_content because this didn't work in
    # Windows in 2020-05 for me, also see issue #3/#7. I got
        # JS error /_addons/1899278645/web/rangy-classapplier.js:15 Uncaught TypeError: Cannot read property 'createModule' of undefined
        # JS error /_addons/1899278645/web/rangy-core.js:10 Uncaught Error: required module 'ClassApplier' not found
        # JS error :41 Uncaught TypeError: rangy.createHighlighter is not a function

    jsstring = """
var injectScript = (src) => {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        script.async = true;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
};

$(document).ready(function(){
    (async () => {
        await injectScript("http://127.0.0.1:PORTPORT/_addons/1899278645/web/rangy-core.js");
        await injectScript("http://127.0.0.1:PORTPORT/_addons/1899278645/web/rangy-classapplier.js");
        await injectScript("http://127.0.0.1:PORTPORT/_addons/1899278645/web/rangy-serializer.js");
        await injectScript("http://127.0.0.1:PORTPORT/_addons/1899278645/web/rangy-textrange.js");
        await injectScript("http://127.0.0.1:PORTPORT/_addons/1899278645/web/rangy-selectionsaverestore.js");
        await injectScript("http://127.0.0.1:PORTPORT/_addons/1899278645/web/rangy-highlighter.js");

        rangy.init();
        HIGHLIGHTERS
    })();
});
""".replace("PORTPORT", str(mw.mediaServer.getPort()))\
   .replace("HIGHLIGHTERS", rangy_higlighters_for_each_class())
    self.web.eval(jsstring)
gui_hooks.editor_did_init.append(js_inserter)