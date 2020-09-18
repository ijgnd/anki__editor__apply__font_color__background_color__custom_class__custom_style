import json

def classes_addon_rangy_remove_all(editor):
    # this only works on stuff rangy has highlighted before: so it doesn't help in the browser.
    js = """
Object.values(dict).forEach(function (item, index) {
    item.removeAllHighlights();
    console.log(item);
});
"""
    # TODO
    #js = """classes_addon__remove_classes_from_selection();"""
    #editor.web.eval(js)

    # at least I can undo the following (which is arguably more important than keeping other formatting)
    text = editor.web.selectedText()
    editor.web.eval("setFormat('inserthtml', %s);" % json.dumps(text))
