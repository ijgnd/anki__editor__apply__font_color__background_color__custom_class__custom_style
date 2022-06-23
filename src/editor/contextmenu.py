from aqt.qt import QLabel, QWidgetAction

from ..config_var import getconfig
from ..colors import hex_to_rgb_string

from .apply_categories import apply_categories


def return_stylesheet(e):
    if e["Category"] == "Backcolor (inline)":
        thiscolor = hex_to_rgb_string(e["Setting"])
        line1 = f"background-color: rgba({thiscolor}); "
    elif e["Category"] == "Backcolor (via class)":
        thiscolor = hex_to_rgb_string(e["Text_in_menu_styling"])
        line1 = "background-color: rgba({thiscolor}); "
    elif e["Category"] == "Forecolor":
        thiscolor = hex_to_rgb_string(e["Setting"])
        line1 = "color: rgba({thiscolor}); "
    elif e["Category"] == "Forecolor (via class)":
        thiscolor = hex_to_rgb_string(e["Text_in_menu_styling"])
        line1 = "color: rgba({thiscolor}); "
    elif e["Category"] == "text wrapper":
        line1 = ""
    else:
        line1 = e["Text_in_menu_styling"]

    stylesheet = f"""QLabel {{
        {line1}
        font-size: 15px;
        padding-top: 7px;
        padding-bottom: 7px;
        padding-right: 5px;
        padding-left: 5px;
        }}
    """

    # TODO
    if e["Category"] == "font size (via class)":
        stylesheet = """QLabel {{
            font-size: {};
            padding-top: 7px;
            padding-bottom: 7px;
            padding-right: 5px;
            padding-left: 5px;
            }}
        """.format(
            e["Text_in_menu_styling"]
        )
    return stylesheet


def my_label_text(_dict, fmt):
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


def create_menu_entry(view, entry, parentmenu):
    text = my_label_text(entry, True)
    label = QLabel(text)
    # https://stackoverflow.com/a/6876509
    label.setAutoFillBackground(True)
    stylesheet = return_stylesheet(entry)
    label.setStyleSheet(stylesheet)

    action = QWidgetAction(parentmenu)
    action.setDefaultWidget(label)

    category = entry["Category"]

    def callback(_):
        apply_categories[category](view.editor, entry)

    action.triggered.connect(callback)
    return action


def setup_contextmenu(view, menu):
    config = getconfig()

    if config.get("v2_show_in_contextmenu", False):
        return

    menu.addSeparator()
    groups = {}

    for i in config["context_menu_groups"]:
        groups[i] = menu.addMenu(i)

    for entry in config["v3"]:
        if entry.get("Show_in_menu", True):
            if entry["Category"] in ["class (other)", "text wrapper"]:
                if entry["Target group in menu"]:
                    submenu = groups[entry["Target group in menu"]]
                else:
                    submenu = groups[entry["Category"]]
            else:
                submenu = groups[entry["Category"]]

            submenu.addAction(create_menu_entry(view, entry, submenu))
