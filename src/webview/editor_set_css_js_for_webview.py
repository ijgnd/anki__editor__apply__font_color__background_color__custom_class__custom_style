import os

from aqt import mw
from aqt.editor import Editor
from aqt.gui_hooks import (
    webview_will_set_content,
    editor_did_init,
)

from ..vars import (
    addon_folder_name,
    css_path,
    css_path_Customize_Editor_Stylesheet,
    js_to_append,
    uses_classes,
)
from ..config_var import getconfig
from ..utils import create_css_for_webviews_from_config


def rangy__create_global_variables_for_later_use():
    jsstring = """var dict = new Object();"""
    # for e in getconfig()["v3"]:
    #     if e["Category"] in uses_classes:
    #         jsstring += f"""\nvar {e["Setting"]}highlighter;"""
    return jsstring


def rangy_higlighters_for_each_class():
    js_str = """
    dict["temporary_highlighter_for_styles"] = rangy.createHighlighter();
    dict["temporary_highlighter_for_styles"].addClassApplier(rangy.createClassApplier('temp_styles_helper'));
"""
    for e in getconfig()["v3"]:
        if e["Category"] in uses_classes:
            classname = e["Setting"]
            js_str += f"""
    dict["{classname}highlighter"] = rangy.createHighlighter();
    dict["{classname}highlighter"].addClassApplier(rangy.createClassApplier('{classname}'));
"""
    return js_str


def append_js_to_Editor(web_content, context):
    if isinstance(context, Editor):
        web_content.head += f"""\n<script>\n{rangy__create_global_variables_for_later_use()}\n</script>\n"""


def append_css_to_Editor(js, note, editor) -> str:
    newjs = js + (
        """
var userStyle = document.createElement("style");
userStyle.rel = "stylesheet";
userStyle.textContent = `USER_STYLE`;
userStyle.id = "customStyles";

forEditorField([], (field) => {
    var sr = field.editingArea.shadowRoot;
    var customStyles = sr.getElementById("customStyles");
    if (customStyles) {
        customStyles.parentElement.replaceChild(userStyle, customStyles)
    }
    else {
        sr.insertBefore(userStyle.cloneNode(true), field.editingArea.editable)
    }
});

""".replace(
            "USER_STYLE", create_css_for_webviews_from_config()
        )
    )

    return newjs


def js_inserter(self):
    # load rangy and create highlighters
    # rangy is inserted/loaded here and not with webview_will_set_content because this didn't work in
    # Windows in 2020-05 for me, also see issue #3/#7. I got
    # JS error /_addons/1899278645/web/rangy-classapplier.js:15 Uncaught TypeError: Cannot read property 'createModule' of undefined
    # JS error /_addons/1899278645/web/rangy-core.js:10 Uncaught Error: required module 'ClassApplier' not found
    # JS error :41 Uncaught TypeError: rangy.createHighlighter is not a function

    jsstring = (
        """
// https://stackoverflow.com/questions/5222814/window-getselection-return-html
async function selectionAsHtml() {
    const input = require("svelte/store").get(require("anki/NoteEditor").instances[0].focusedInput)

    if (!input || input.name !== "richText") {
        return "";
    }

    const element = await input.element;
    const selection =  element.getRootNode().getSelection();

    if (!selection) {
        return "";
    }

    let out = "";

    if (selection.rangeCount) {
        var helper_span = document.createElement("span");
        for (var i = 0, l = selection.rangeCount; i < l; ++i) {
            helper_span.appendChild(selection.getRangeAt(i).cloneContents());
        }
        out = helper_span.innerHTML;
    }

    return out;
}

var classes_addon_wrap = (elemName) => async (surrounding_elem_tag_class) => {
    const input = require("svelte/store").get(require("anki/NoteEditor").instances[0].focusedInput)

    if (!input || input.name !== "richText") {
        return;
    }

    const element = await input.element;
    const selection =  element.getRootNode().getSelection();

    if (!selection) {
        return;
    }

    const range = s.getRangeAt(0);
    const content = range.cloneContents();
    const element = document.createElement(elemName);

    range.deleteContents();

    if (surrounding_elem_tag_class) {
        element.className = surrounding_elem_tag_class;
    }

    element.appendChild(content);
    range.insertNode(elem);
    saveNow(true);
}

var classes_addon_wrap_span_helper = classes_addon_wrap("span")
var classes_addon_wrap_helper = classes_addon_wrap("div")

function injectScript(src) {
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
        console.log('rangy loaded by classes_addon');

        await injectScript("http://127.0.0.1:PORTPORT/_addons/NAMENAME/web/rangy-core.js");
        await injectScript("http://127.0.0.1:PORTPORT/_addons/NAMENAME/web/rangy-classapplier.js");
        await injectScript("http://127.0.0.1:PORTPORT/_addons/NAMENAME/web/rangy-serializer.js");
        await injectScript("http://127.0.0.1:PORTPORT/_addons/NAMENAME/web/rangy-textrange.js");
        await injectScript("http://127.0.0.1:PORTPORT/_addons/NAMENAME/web/rangy-selectionsaverestore.js");
        await injectScript("http://127.0.0.1:PORTPORT/_addons/NAMENAME/web/rangy-highlighter.js");

        rangy.init();
        HIGHLIGHTERS
        MAYBE_HBIR
        focusField(0);
    })();
});
""".replace(
            "PORTPORT", str(mw.mediaServer.getPort())
        )
        .replace("NAMENAME", __name__.split(".", 1)[0])
        .replace("HIGHLIGHTERS", rangy_higlighters_for_each_class())
        .replace(
            "MAYBE_HBIR",
            "hbir_init();" if "1095648795" in mw.addonManager.allAddons() else "",
        )
    )
    # the line above is a workaround for half-baked incremental reading,
    # https://ankiweb.net/shared/info/1095648795
    self.web.eval(jsstring)
