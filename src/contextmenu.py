"""
Copyright:  (c) 2019 ignd
            (c) Glutanimate 2015-2017
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Use this at your own risk
"""

import os

from aqt.editor import Editor, EditorWebView
from aqt.qt import *


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
    else:
        line1 = ""  # e['Text_in_menu_styling']

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


def co_my_label_text(_dict):
    from .color_style_class_buttons import config
    totallength = config['maxname'] + config['maxshortcut'] + 3
    remaining = totallength - len(_dict.get("Hotkey", 0))
    t1 = _dict.get("Text_in_menu", "Variable Text_in_menu missing")
    return t1.ljust(remaining) + _dict.get("Hotkey", "")


def co_create_menu_entry(view, e, parentmenu):
    t = co_my_label_text(e)
    y = QLabel(t)
    # https://stackoverflow.com/a/6876509
    y.setAutoFillBackground(True)
    stylesheet = co_return_stylesheet(e)
    y.setStyleSheet(stylesheet)

    # font = QFont()
    # #font.setBold(True)
    # y.setFont(font)

    x = QWidgetAction(parentmenu)
    x.setDefaultWidget(y)
    cat = e["Category"]
    se = e.get("Setting", e.get("Category", False))
    x.triggered.connect(lambda _, a=cat, b=se: co_my_highlight_helper(view, a, b))  # ???
    return x


def add_to_context_styled(view, menu):
    from .color_style_class_buttons import config
    selected = view.page().selectedText()
    menu.addSeparator()

    cmbg, cmbgc, cmfc, cmst, cmcl = "", "", "", "", ""
    groups = {
        'Backcolor (inline)': cmbg,
        'Backcolor (via class)': cmbgc,
        'Forecolor': cmfc,
        'style': cmst,
        'class': cmcl,
    }
    for i in config['context_menu_groups']:
        groups[i] = menu.addMenu(i)

    for e in config['v3']:
        if e.get('Show_in_menu', False):
            relevantgroup = groups[e['Category']]
            relevantgroup.addAction(co_create_menu_entry(view, e, relevantgroup))
    # menu.exec_(QCursor.pos())


def add_to_context_unstyled(view, menu):
    from .color_style_class_buttons import config
    selected = view.page().selectedText()
    menu.addSeparator()

    cmbg, cmbgc, cmfc, cmst, cmcl = "", "", "", "", ""
    groups = {
        'Backcolor (inline)': cmbg,
        'Forecolor': cmfc,
        'Backcolor (via class)': cmbgc,
        'style': cmst,
        'class': cmcl,
    }
    for i in config['context_menu_groups']:
        groups[i] = menu.addMenu(i)

    for e in config['v3']:
        if e.get('Show_in_menu', False):
            text = co_my_label_text(e)
            relevantgroup = groups[e['Category']]
            a = relevantgroup.addAction(text)
            cat = e["Category"]
            se = e.get("Setting", e.get("Category", False))
            a.triggered.connect(lambda _, a=cat, b=se: co_my_highlight_helper(view, a, b))


def add_to_context(view, menu):
    from .color_style_class_buttons import config
    if config["v2_menu_styling"]:
        add_to_context_styled(view, menu)
    else:
        add_to_context_unstyled(view, menu)
