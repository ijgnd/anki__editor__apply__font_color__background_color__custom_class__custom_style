from __future__ import unicode_literals

"""
Copyright:  (c) 2019 ignd
            (c) Glutanimate 2015-2017
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Use this at your own risk
"""

import os

from aqt.editor import Editor
from aqt.qt import *
from anki.hooks import addHook

from .colors import hex_to_rgb_string
from .contextmenu import co_hex_to_rgb


def my_highlight_helper(editor, category, setting):
    func = editor.mycategories[category]
    func(editor, setting)
Editor.my_highlight_helper = my_highlight_helper


"""
Stylesheet for QMenu?
- stylesheet refers not to QAction but to QMenu
- idea for QActionWidget from  https://www.python-forum.de/viewtopic.php?t=42747
- some unanswered questions from 2018 about QAction
  https://stackoverflow.com/questions/49882834/pyqt-setting-background-color-of-individual-qmenu-qaction-objects
  https://stackoverflow.com/questions/50159451/style-sheets-how-can-i-manipulate-a-single-qactions-of-qmenu
"""


def return_stylesheet(editor, e):
    if e['Category'] == 'Backcolor (inline)':
        thiscolor = hex_to_rgb_string(e['Setting'])
        line1 = "background-color: rgba({}); ".format(thiscolor)
    elif e['Category'] == 'Backcolor (via class)':
        thiscolor = co_hex_to_rgb(e['Text_in_menu_styling'])
        line1 = "background-color: rgba({}); ".format(thiscolor)
    elif e['Category'] == 'Forecolor':
        thiscolor = hex_to_rgb_string(e['Setting'])
        line1 = "color: rgba({}); ".format(thiscolor)
    else:
        line1 = e['Text_in_menu_styling']

    stylesheet = """QLabel {{
        {}
        font-size: 15px;
        padding-top: 7px;
        padding-bottom: 7px;
        padding-right: 5px;
        padding-left: 5px;
        }}
    """.format(line1)
    return stylesheet
Editor.return_stylesheet = return_stylesheet


def my_label_text(editor, _dict):
    from .color_style_class_buttons import config
    totallength = config['maxname'] + config['maxshortcut'] + 3
    remaining = totallength - len(_dict.get("Hotkey", 0))
    t1 = _dict.get("Text_in_menu", "Variable Text_in_menu missing")
    out = t1.ljust(remaining) + _dict.get("Hotkey", "")
    return out
Editor.my_label_text = my_label_text


def create_menu_entry(editor, e, parentmenu):
    # e.get('Icon_in_menu',False) doesn't work???
    # maybe show icons with settings like:
            # {
            #     "Category":"justifyCenter",
            #     "Hotkey": "ctrl+shift+alt+s",
            #     "Show_in_menu": true,
            #     "IconInMenu": "justifyCenter.png"
            # }
    # But small icons look really strange.
    if e.get('IconInMenu', False):
        y = QLabel()
        path = os.path.join(icon_path, e['IconInMenu'])
        pixmap = QPixmap(path)
        y.setPixmap(pixmap)
    else:
        t = editor.my_label_text(e)
        y = QLabel(t)
    # https://stackoverflow.com/a/6876509
    y.setAutoFillBackground(True)
    stylesheet = editor.return_stylesheet(e)
    y.setStyleSheet(stylesheet)

    # font = QFont()
    # #font.setBold(True)
    # y.setFont(font)

    x = QWidgetAction(parentmenu)
    x.setDefaultWidget(y)
    cat = e["Category"]
    se = e.get("Setting", e.get("Category", False))
    x.triggered.connect(lambda _, a=cat, b=se: my_highlight_helper(editor, a, b))
    return x
Editor.create_menu_entry = create_menu_entry


def additional_menu_styled(editor):
    # mod of onAdvanced from editor.py
    from .color_style_class_buttons import config
    m = QMenu(editor.mw)
    for e in config['v3']:
        if e.get('Show_in_menu', False):
            m.addAction(editor.create_menu_entry(e, m))
    m.exec_(QCursor.pos())
Editor.additional_menu_styled = additional_menu_styled


basic_stylesheet = """
QMenu::item {
    padding-top: 5px;
    padding-bottom: 5px;
    padding-right: 5px;
    padding-left: 5px;
    font-family: Roboto Mono;
}
QMenu::item:selected {
    color: black;
    background-color: #D9CD6D;
}
"""


def additional_menu_basic(editor):
    from .color_style_class_buttons import config
    # mod of onAdvanced from editor.py
    m = QMenu(editor.mw)
    # m.setStyleSheet(basic_stylesheet)
    m.setFont(QFont('Courier New', 9))
    for e in config['v3']:
        if e.get('Show_in_menu', False):
            text = editor.my_label_text(e)
            a = m.addAction(text)
            cat = e["Category"]
            se = e.get("Setting", e.get("Category", False))
            a.triggered.connect(lambda _, a=cat, b=se: my_highlight_helper(editor, a, b))
            # a.setShortcut(QKeySequence(e.get("Hotkey","")))   #hotkey is not shown in 2.1.8
    m.exec_(QCursor.pos())
Editor.additional_menu_basic = additional_menu_basic
