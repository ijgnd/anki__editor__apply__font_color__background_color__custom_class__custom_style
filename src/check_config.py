import json
import os
from pprint import pprint as pp

from aqt.utils import showInfo

from .colors import html4colors, css3colors
from .vars import addonname, mjfile


updatetext = (f'This is a warning message generated by the add-on {addonname} '
               'This message is only shown once after the update/installation of this '
               'add-on or if you use a different profile for the first time.'
               '\n\nThis add-on got a big update in 2019-08 which brings a new config '
               'dialog. The add-on tries to import the old config. '
               "\n\nIf your version of this add-on is from before 2019-02-19 "
               "your old config will be ignored."
               "\n\nIf your version of this add-on is newer there still might "
               "be some unforseeable problems. This new version won't "
               "change your old-config. Your old config is still in "
               "the file 'meta.json' which is in the folder of this add-on. "
               "\n\nTo view your 'meta.json' go to the add-on manager, select this "
               "add-on and click 'View Files'."
               "\n\nIf you run into a problem you can report this on"
               "\nhttps://github.com/ijgnd/anki__quick_highlight_fontcolor_background/issues"
              )




def read_and_update_old_v2_config_from_meta_json(config):
    """update old v2 config that was used before 2019-08-06"""
    mjconfig = ""
    if os.path.exists(mjfile):
        with open(mjfile, "r") as mjf:
            mj = json.load(mjf)
            if "config" in mj:
                mjconfig = mj['config']
    if mjconfig:
        # check for illegal entries and abort
        v2_entries_bool = ["v2_configwarning",
                           "v2_menu_styling",
                           "v2_show_in_contextmenu",
                           "v2_wider_button_in_menu",
                           ]
        v2_entries_str = ["v2_key_styling_menu"]
        v2_entries_list = ["v2"]
        v2_all = v2_entries_bool + v2_entries_str + v2_entries_list
        v2_contents_bool = ["Show_in_menu",
                            "extrabutton_show",
                            "extrabutton_width",
                            ]
        v2_contents_str = ["Category",
                           "Hotkey",
                           "Setting",
                           "Text_in_menu",
                           "Text_in_menu_styling",
                           "extrabutton_text",
                           "extrabutton_tooltip",
                           ]
        v2_contents_all = v2_contents_bool + v2_contents_str
        for k, v in mjconfig.items():
            if k not in v2_all:
                text = ('Error while reading old config of the add-on "editor: apply '
                        'font color, background color custom class, custom style". '
                        '\n\n Unknown value "%s" detected in config. Ignoring old config.'
                        % str(k)
                        )
                showInfo(text)
                return
            error = False
            if k in v2_entries_bool and not isinstance(v, bool):
                error = True
            if k in v2_entries_str and not isinstance(v, str):
                error = True
            if k in v2_entries_list and not isinstance(v, list):
                error = True
            if error:
                text = ('Error while reading old config of the add-on "editor: apply '
                        'font color, background color custom class, custom style". '
                        '\n\n Illegal value "%s" detected in option %s config. Ignoring old config.'
                        % (str(v), str(k))
                        )
                showInfo(text)
                return
            error = False
            for e in mjconfig['v2']:
                if not isinstance(e, dict):
                    text = ('Error while reading old config of the add-on "editor: apply '
                            'font color, background color custom class, custom style". '
                            '\n\n In "v2" there is an entry that is not a dictionary. '
                            'Ignoring old config.'
                            )
                    showInfo(text)
                    return
                for k, v in e.items():
                    if k not in v2_contents_all:
                        error = (k, "")
                    if k in v2_contents_str and not isinstance(v, str):
                        error = (k, v)
                    if k in v2_contents_bool and not isinstance(v, bool):
                        error = (k, v)
                if error:
                    text = ('Error while reading old config of the add-on "editor: apply '
                            'font color, background color custom class, custom style". '
                            '\n\n Illegal value "%s", "%s" detected in option "v2" config.'
                            'Ignoring old config.'
                            % (str(error[0]), str(error[1]))
                            )
                    showInfo(text)
                    return
        showInfo(updatetext)
        config = mjconfig
        v2 = config['v2']
        # adjust old config
        for i, e in enumerate(v2):
            e["Hotkey"] = e["Hotkey"].lower()
            # convert colors
            if e["Category"] in ["forecolor", "backcolor"]:
                for k, v in html4colors.items():
                    if k == e["Setting"]:
                        e["Setting"] = v
                for k, v in css3colors.items():
                    if k == e["Setting"]:
                        e["Setting"] = v
            # uppercase forecolor, backcolor so that they are sorted together
            for v, k in e.items():
                if v == "Category" and k == "backcolor":
                    v2[i]["Category"] = "Backcolor (inline)"
                if v == "Category" and k == "forecolor":
                    v2[i]["Category"] = "Forecolor"
        config['v3'] = v2
    return config


def autogenerate_config_values_for_menus(config):
    config['maxname'] = 0
    config['maxshortcut'] = 0
    config['context_menu_groups'] = []
    config['maxname'] = 0
    config['maxshortcut'] = 0
    for e in config['v3']:
        if e['Show_in_menu']:
            if e.get('Text_in_menu', False):
                config['maxname'] = max(config['maxname'], len(e["Text_in_menu"]))
                if e['Category'] not in config['context_menu_groups']:
                    config['context_menu_groups'].append(e['Category'])
            if e.get('Hotkey', False):
                config['maxshortcut'] = max(config['maxshortcut'], len(e["Hotkey"]))
    return config
