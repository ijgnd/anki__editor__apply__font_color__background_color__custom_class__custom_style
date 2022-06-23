from aqt import mw

from ..utils import create_css_for_webviews_from_config


def append_css_to_Editor(js, note, editor) -> str:
    return (
        js
        + f"""
require("anki/RichTextInput").lifecycle.onMount(async ({{ customStyles }}) => {{
    const {{ addStyleTag }} = await customStyles;
    const {{ element: styleTag }} = await addStyleTag('customStyles');
    styleTag.textContent = `{create_css_for_webviews_from_config()}`
}});
"""
    )


def eval_base_js(editor):
    editor.web.eval(
        f"""
const {{ Surrounder }} = require("anki/surround");

let surrounder;
let disabled;
let removeFormats;

let editorResolve;
const editorPromise = new Promise((resolve) => (editorResolve = resolve));

function setupWrapping({{ focusedInput, toolbar }}) {{
    surrounder = Surrounder.make()
    disabled = false;

    focusedInput.subscribe((input) => {{
        if (input && input.name === "rich-text") {{
            surrounder.richText = input;
            disabled = false;
        }} else {{
            surrounder.disable();
            disabled = true;
        }}
    }})

    removeFormats = toolbar.removeFormats;
    editorResolve();
}}

/* This depends on there only being one note editor */
require("anki/NoteEditor").instances.forEach(setupWrapping);
require("anki/NoteEditor").lifecycle.onMount(setupWrapping);

function removeEmptyStyle(element) {{
    if (element.style.cssText.length === 0) {{
        element.removeAttribute("style");
        // Calling `.hasAttribute` right after `.removeAttribute` might return true.
        return true;
    }}

    return false;
}}

function removeStyleProperties(
    element,
) {{
    return removeEmptyStyle(element);
}}

function classesAddonWrap(tagName) {{
    return async (className, label) => {{
       await editorPromise;

       function matcher(
           element,
           match,
       ) {{
           if (
               element.tagName !== tagName
               || !element.classList.contains(className)
           ) {{
               return;
           }}

           match.clear(() => {{
               element.classList.remove(className);

               if (
                   removeStyleProperties(element) &&
                   element.classList.length === 0
               ) {{
                   match.remove();
               }}
           }});
       }}

        function formatter(node) {{
            const extension = node.extensions.find(
                (element) => element.tagName === "SPAN",
            );

            if (extension) {{
                extension.classList.add(className);
                return false;
            }}

            const span = document.createElement("span");
            span.classList.add(className);
            node.range.toDOMRange().surroundContents(span);
            return true;
        }}

        const format = {{
            matcher,
            formatter,
        }};

        const namedFormat = {{
            name: className,
            show: true,
            active: true,
            format,
        }}

        removeFormats.update((formats) => [...formats, namedFormat]);

        return () => surrounder.surround(format);
    }}
}}

const classesAddonWrapSpanHelper = classesAddonWrap("span")
const classesAddonWrapDivHelper = classesAddonWrap("div")

{"hbir_init();" if "1095648795" in mw.addonManager.allAddons() else ""}
// the line above is a workaround for half-baked incremental reading
// https://ankiweb.net/shared/info/1095648795
"""
    )
