# Copyright:  (c) 2019- ignd
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os
from pprint import pprint as pp

from PyQt5.QtWidgets import (
    QLabel,
    QWidgetAction,
)

from aqt import mw
from aqt.editor import Editor, EditorWebView

from .config_var import getconfig
from .editor_apply_styling_functions import classes_addon_rangy_remove_all


def co_my_highlight_helper(view, category, setting):
    func = view.editor.mycategories[category]
    func(view.editor, setting)


def co_hex_to_rgb(color):
    # https://stackoverflow.com/a/29643643
    c = color.lstrip('#')
    red = int(c[0:2], 16)
    green = int(c[2:4], 16)
    blue = int(c[4:6], 16)
    alpha = 128
    values = "{}, {}, {}, {}".format(red, green, blue, alpha)
    return values


def co_return_stylesheet(e):
    if e['Category'] == 'Backcolor (inline)':
        thiscolor = co_hex_to_rgb(e['Setting'])
        line1 = "background-color: rgba({}); ".format(thiscolor)
    elif e['Category'] == 'Backcolor (via class)':
        thiscolor = co_hex_to_rgb(e['Text_in_menu_styling'])
        line1 = "background-color: rgba({}); ".format(thiscolor)
    elif e['Category'] == 'Forecolor':
        thiscolor = co_hex_to_rgb(e['Setting'])
        line1 = "color: rgba({}); ".format(thiscolor)
    elif e['Category'] == 'Forecolor (via class)':
        thiscolor = co_hex_to_rgb(e['Text_in_menu_styling'])
        line1 = "color: rgba({}); ".format(thiscolor)
    elif e['Category'] == 'text wrapper':
        line1 = ""
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

    # TODO
    if e['Category'] == 'font size (via class)':
        stylesheet = """QLabel {{
            font-size: {};
            padding-top: 7px;
            padding-bottom: 7px;
            padding-right: 5px;
            padding-left: 5px;
            }}
        """.format(e['Text_in_menu_styling'])
    return stylesheet


def co_my_label_text(_dict, fmt):
    config = getconfig()
    totallength = config['maxname'] + config['maxshortcut'] + 3
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


def co_create_menu_entry(view, e, parentmenu):
    t = co_my_label_text(e, True)
    y = QLabel(t)
    # https://stackoverflow.com/a/6876509
    y.setAutoFillBackground(True)
    stylesheet = co_return_stylesheet(e)
    y.setStyleSheet(stylesheet)
    x = QWidgetAction(parentmenu)
    x.setDefaultWidget(y)
    cat = e["Category"]
    se = e.get("Setting", e.get("Category", False))
    x.triggered.connect(lambda _, a=cat, b=se: co_my_highlight_helper(view, a, b))  # ???
    return x


def add_to_context_styled(view, menu):
    config = getconfig()
    menu.addSeparator()
    a = menu.addAction("Clear more formatting (Classes, etc.)")
    a.triggered.connect(lambda _: classes_addon_rangy_remove_all(view.editor))
    menu.addSeparator()
    groups = {}
    for i in config['context_menu_groups']:
        groups[i] = menu.addMenu(i)
    for row in config['v3']:
        if row.get('Show_in_menu', True):
            if row['Category'] in ["class (other)", "text wrapper"]:
                if row["Target group in menu"]:
                    submenu = groups[row['Target group in menu']]
                else:
                    submenu = groups[row['Category']]
            else:
                submenu = groups[row['Category']]
            submenu.addAction(co_create_menu_entry(view, row, submenu))


def add_to_context(view, menu):
    add_to_context_styled(view, menu)
