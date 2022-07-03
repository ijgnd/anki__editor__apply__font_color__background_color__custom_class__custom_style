from aqt.qt import QCursor, QMenu, QLabel, QWidgetAction
from aqt.editor import Editor

from ..config_var import getconfig
from ..colors import hex_to_rgb_string

from .apply_categories import apply_categories


"""
Stylesheet for QMenu?
- stylesheet refers not to QAction but to QMenu
- idea for QActionWidget from  https://www.python-forum.de/viewtopic.php?t=42747
- some unanswered questions from 2018 about QAction
  https://stackoverflow.com/questions/49882834/pyqt-setting-background-color-of-individual-qmenu-qaction-objects
  https://stackoverflow.com/questions/50159451/style-sheets-how-can-i-manipulate-a-single-qactions-of-qmenu
"""


def return_stylesheet(editor, e):
    if e["Category"] == "Backcolor (inline)":
        thiscolor = hex_to_rgb_string(e["Setting"])
        line1 = "background-color: rgba({}); ".format(thiscolor)
    elif e["Category"] == "Backcolor (via class)":
        thiscolor = hex_to_rgb_string(e["Text_in_menu_styling"])
        line1 = "background-color: rgba({}); ".format(thiscolor)
    elif e["Category"] == "Forecolor":
        thiscolor = hex_to_rgb_string(e["Setting"])
        line1 = "color: rgba({}); ".format(thiscolor)
    elif e["Category"] == "Forecolor (via class)":
        thiscolor = hex_to_rgb_string(e["Text_in_menu_styling"])
        line1 = "color: rgba({}); ".format(thiscolor)
    else:
        line1 = e["Text_in_menu_styling"]

    stylesheet = """QLabel {{
        {}
        font-size: 15px;
        padding-top: 7px;
        padding-bottom: 7px;
        padding-right: 5px;
        padding-left: 5px;
        }}
    """.format(
        line1
    )
    return stylesheet


Editor.return_stylesheet = return_stylesheet


def my_label_text(editor, _dict, fmt):
    config = getconfig()
    totallength = config["maxname"] + config["maxshortcut"] + 3
    remaining = totallength - len(_dict.get("Hotkey", 0))
    t1 = _dict.get("Text_in_menu", "Variable Text_in_menu missing")
    # ideally hotkey would be right aligned
    # in html I can use:
    #    <span style="text-align:left;">left<span style="float:right;">right</span></span>
    # BUT float is not supported for text in a QLabel/QString
    # https://doc.qt.io/qt-5/richtext-html-subset.html
    # so I would need two QLabels and some container: complicated
    # I don't want to set the shortcut here with
    #       a.setShortcut(QKeySequence(e["Hotkey"]))
    #       a.setShortcutVisibleInContextMenu(True)
    # because I set them globally in a different place
    # and setting the same shortcut multiple times disables them.
    # Also this only works for an unstyled menu and might need to be adjusted for QActionWidget
    if fmt:
        # formatted
        h = _dict.get("Hotkey", "")
        if h:
            out = t1 + "  (" + h + ")"
        else:
            out = t1
    else:
        # unformatted
        out = t1.ljust(remaining) + _dict.get("Hotkey", "")
    return out


Editor.my_label_text = my_label_text


def create_menu_entry(editor, entry, parentmenu):
    text = editor.my_label_text(entry, True)
    label = QLabel(text)
    # https://stackoverflow.com/a/6876509
    label.setAutoFillBackground(True)
    stylesheet = editor.return_stylesheet(entry)
    label.setStyleSheet(stylesheet)
    action = QWidgetAction(parentmenu)
    action.setDefaultWidget(label)
    category = entry["Category"]

    def my_highlight_helper():
        func = apply_categories[category]
        func(editor, entry)

    action.triggered.connect(my_highlight_helper)
    return action


Editor.create_menu_entry = create_menu_entry


def additional_menu_styled(editor):
    # mod of onAdvanced from editor.py
    config = getconfig()
    # QMenu(editor.mw) conflict with persistent editor, 1686259334 I get
    # RuntimeError: super-class __init__() of type AnkiQt was never called
    m = QMenu()
    for e in config["v3"]:
        if e.get("Show_in_menu", False):
            m.addAction(editor.create_menu_entry(e, m))
    m.exec(QCursor.pos())


Editor.additional_menu_styled = additional_menu_styled
