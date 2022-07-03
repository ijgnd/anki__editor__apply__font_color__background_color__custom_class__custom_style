import json
import os
from pprint import pprint as pp

from aqt import mw
from aqt.utils import (
    askUser,
    showInfo,
)

from .colors import html4colors, css3colors
from .default_config import default_config
from .vars import addon_name, mjfile, uses_classes


def autogenerate_config_values_for_menus(config):
    config["maxname"] = 0
    config["maxshortcut"] = 0
    config["context_menu_groups"] = []
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
