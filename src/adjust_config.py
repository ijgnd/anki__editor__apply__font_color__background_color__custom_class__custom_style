import json
import os
from pprint import pprint as pp

from aqt import mw
from aqt.utils import (
    askUser,
    showInfo,
)

from .colors import html4colors, css3colors
from .defaultconfig import defaultconfig
from .vars import addonname, mjfile, uses_classes


def autogenerate_config_values_for_menus(config):
    config["maxname"] = 0
    config["maxshortcut"] = 0
    config["context_menu_groups"] = []
    config["maxname"] = 0
    config["maxshortcut"] = 0
    for e in config["v3"]:
        if e["Category"] in uses_classes:
            if not "Target group in menu" in e:
                e["Target group in menu"] = ""
                e["surround_with_div_tag"] = False
        if e["Show_in_menu"]:
            if e.get("Text_in_menu", False):
                config["maxname"] = max(config["maxname"], len(e["Text_in_menu"]))
                if e["Category"] == "class (other)" and e["Target group in menu"]:
                    thisgroup = e["Target group in menu"]
                elif e["Category"] == "text wrapper" and e["Target group in menu"]:
                    thisgroup = e["Target group in menu"]
                else:
                    thisgroup = e["Category"]
                if thisgroup not in config["context_menu_groups"]:
                    config["context_menu_groups"].append(thisgroup)
            if e.get("Hotkey", False):
                config["maxshortcut"] = max(config["maxshortcut"], len(e["Hotkey"]))
    return config


def uses_most_recent_config(config, level):
    if not "update_level" in config:
        return False
    current = config["update_level"]
    try:
        current = int(current)
    except:
        return False
    else:
        if current > level:
            return True
        else:
            return False


def update_config_for_202005(config):
    if "v3" not in config:
        # something's broken in the config??
        # just rest it?
        config["v3"] = defaultconfig.copy()["v3"]
    for e in config["v3"]:
        if not "Text_in_menu_styling" in e:
            e["Text_in_menu_styling"] = ""
        if not "Text_in_menu_styling_nightmode" in e:
            e["Text_in_menu_styling_nightmode"] = ""
    if not "v3_inactive" in config:
        config["v3_inactive"] = []
    first_after_update_install = False
    if not uses_most_recent_config(config, 1589114109):
        first_after_update_install = True
        if not "v2_key_styling_undo" in config:
            config["v2_key_styling_undo"] = ""
        oldv3 = config["v3"][:]
        config["v3"] = []
        for row in oldv3:
            if (
                row["Category"] in ["class", "class (other)"]
                and "surround_with_div_tag" not in row
            ):
                row["surround_with_div_tag"] = False
            if row["Category"] == "class":
                row["Category"] = "class (other)"
            if row["Category"] == "style":
                row["Category"] = "style (inline)"
            if row["Category"] == "Forecolor":
                row["Category"] = "Forecolor (inline)"
            config["v3"].append(row)
        config["update_level"] = 1589114110
    return first_after_update_install, config
