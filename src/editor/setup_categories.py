import json
from ..config_var import getconfig


def noop(_editor, _entry):
    pass


def setup_span_class(editor, entry):
    print("testo")
    class_name = entry["Setting"]
    key = f"span{class_name}"
    editor.web.eval(
        f"""
customStylesDict[{json.dumps(key)}] = classesAddonWrapSpanHelper({json.dumps(class_name)});
"""
    )


setup_categories_dict = {
    "text wrapper": noop,
    "class (other)": setup_span_class,
    "class (other), wrapped in div": noop,
    "style (inline)": noop,
    "Backcolor (inline)": noop,
    "Backcolor (via class)": setup_span_class,
    "Forecolor (inline)": noop,
    "Forecolor (via class)": setup_span_class,
    "font size (via class)": setup_span_class,
}


def setup_categories(editor):
    config = getconfig()

    # We use this to cache the formatters
    editor.web.eval("const customStylesDict = {}; ")

    for entry in config["v3"]:
        setup_categories_dict[entry["Category"]](editor, entry)
