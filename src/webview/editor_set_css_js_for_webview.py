from aqt import mw
from aqt.editor import Editor

from ..vars import (
    uses_classes,
)
from ..config_var import getconfig
from ..utils import create_css_for_webviews_from_config


def rangy__create_global_variables_for_later_use():
    return """var dict = new Object();"""
    # for e in getconfig()["v3"]:
    #     if e["Category"] in uses_classes:
    #         jsstring += f"""\nvar {e["Setting"]}highlighter;"""


def rangy_higlighters_for_each_class():
    js_str = "dict['temporary_highlighter_for_styles'] = console.log;"
    for e in getconfig()["v3"]:
        if e["Category"] in uses_classes:
            classname = e["Setting"]
            js_str += f"\ndict['{classname}highlighter'] = console.log;"

    return js_str


def append_js_to_Editor(web_content, context):
    if isinstance(context, Editor):
        web_content.head += f"""\n<script>\n{rangy__create_global_variables_for_later_use()}\n</script>\n"""


def append_css_to_Editor(js, note, editor) -> str:
    return js + (
        """
require("anki/RichTextInput").lifecycle.onMount(async ({ customStyles }) => {
    const { addStyleTag } = await customStyles;
    const { element: styleTag } = await addStyleTag('customStyles');
    styleTag.textContent = `USER_STYLE`
});
""".replace(
            "USER_STYLE", create_css_for_webviews_from_config()
        )
    )


def js_inserter(self):
    # load rangy and create highlighters
    # rangy is inserted/loaded here and not with webview_will_set_content because this didn't work in
    # Windows in 2020-05 for me, also see issue #3/#7. I got
    # JS error /_addons/1899278645/web/rangy-classapplier.js:15 Uncaught TypeError: Cannot read property 'createModule' of undefined
    # JS error /_addons/1899278645/web/rangy-core.js:10 Uncaught Error: required module 'ClassApplier' not found
    # JS error :41 Uncaught TypeError: rangy.createHighlighter is not a function

    jsstring = (
        """
function removeEmptyStyle(element) {
    if (element.style.cssText.length === 0) {
        element.removeAttribute("style");
        // Calling `.hasAttribute` right after `.removeAttribute` might return true.
        return true;
    }

    return false;
}

function removeStyleProperties(
    element,
) {
    return removeEmptyStyle(element);
}

const { Surrounder } = require("anki/surround");

let surrounder;
let disabled;

require("anki/NoteEditor").lifecycle.onMount(({ focusedInput }) => {
    surrounder = Surrounder.make()
    disabled = false;

    focusedInput.subscribe((input) => {
        if (input && input.name === "rich-text") {
            surrounder.richText = input;
            disabled = false;
        } else {
            surrounder.disable();
            disabled = true;
        }
    })
});

function classesAddonWrap(tagName) {
    return async (surroundingElemTagClass) => {
        if (disabled) {
            return;
        }

        function matcher(
            element,
            match,
        ) {
            if (
                element.tagName !== tagName
                || !element.classList.contains(surroundingElemTagClass)
            ) {
                return;
            }

            match.clear(() => {
                element.classList.remove(surroundingElemTagClass);

                if (
                    removeStyleProperties(element) &&
                    element.classList.length === 0
                ) {
                    match.remove();
                }
            });
        }

        function formatter(node) {
            const extension = node.extensions.find(
                (element) => element.tagName === "SPAN",
            );

            if (extension) {
                extension.classList.add(surroundingElemTagClass);
                return false;
            }

            const span = document.createElement("span");
            span.classList.add(surroundingElemTagClass);
            node.range.toDOMRange().surroundContents(span);
            return true;
        }

        const format = {
            matcher,
            formatter,
        };

        surrounder.surround(format);
    }
}

const classesAddonWrapSpanHelper = classesAddonWrap("span")
const classesAddonWrapHelper = classesAddonWrap("div")

HIGHLIGHTERS
MAYBE_HBIR
""".replace(
            "PORTPORT", str(mw.mediaServer.getPort())
        )
        .replace("HIGHLIGHTERS", rangy_higlighters_for_each_class())
        .replace(
            "MAYBE_HBIR",
            "hbir_init();" if "1095648795" in mw.addonManager.allAddons() else "",
        )
    )
    # the line above is a workaround for half-baked incremental reading,
    # https://ankiweb.net/shared/info/1095648795
    self.web.eval(jsstring)
