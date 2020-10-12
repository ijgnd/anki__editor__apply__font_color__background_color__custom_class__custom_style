from aqt.gui_hooks import editor_will_show_context_menu
from aqt.qt import QLabel, QWidgetAction
from aqt.editor import Editor

from ..config_var import getconfig
from ..colors import hex_to_rgb_string

from .rangy_helpers import classes_addon_rangy_remove_all
from .apply_categories import apply_categories


def my_highlight_helper(view, category, setting):
    func = apply_categories[category]
    func(view.editor, setting)

def return_stylesheet(e):
    if e['Category'] == 'Backcolor (inline)':
        thiscolor = hex_to_rgb_string(e['Setting'])
        line1 = "background-color: rgba({}); ".format(thiscolor)
    elif e['Category'] == 'Backcolor (via class)':
        thiscolor = hex_to_rgb_string(e['Text_in_menu_styling'])
        line1 = "background-color: rgba({}); ".format(thiscolor)
    elif e['Category'] == 'Forecolor':
        thiscolor = hex_to_rgb_string(e['Setting'])
        line1 = "color: rgba({}); ".format(thiscolor)
    elif e['Category'] == 'Forecolor (via class)':
        thiscolor = hex_to_rgb_string(e['Text_in_menu_styling'])
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

def my_label_text(_dict, fmt):
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

def create_menu_entry(view, e, parentmenu):
    t = my_label_text(e, True)
    y = QLabel(t)
    # https://stackoverflow.com/a/6876509
    y.setAutoFillBackground(True)
    stylesheet = return_stylesheet(e)
    y.setStyleSheet(stylesheet)
    x = QWidgetAction(parentmenu)
    x.setDefaultWidget(y)
    cat = e["Category"]
    se = e.get("Setting", e.get("Category", False))
    x.triggered.connect(lambda _, a=cat, b=se: my_highlight_helper(view, a, b))  # ???
    return x

def setup_contextmenu(view, menu):
    config = getconfig()

    if config.get("v2_show_in_contextmenu", False):
        return

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

            submenu.addAction(create_menu_entry(view, row, submenu))
