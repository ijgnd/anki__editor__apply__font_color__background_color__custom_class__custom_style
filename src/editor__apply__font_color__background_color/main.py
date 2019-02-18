# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Copyright:  (c) 2019 ignd
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Use this at your own risk
"""

###############BEGIN USER CONFIG FOR ANKI 2.0####################
#config for 2.1 is set via the config dialog of 2.1
#config for 2.0 is set in the file config.json
####################END USER CONFIG##############################


import sys, os, io, pprint

from aqt import mw
from aqt.qt import *
from aqt.editor import Editor
from anki.hooks import wrap, addHook
from anki.utils import json
from aqt.utils import showInfo
from anki import version

ANKI21 = version.startswith("2.1.")

sys_encoding = sys.getfilesystemencoding()
if ANKI21:
    addon_path = os.path.dirname(__file__)
else:
    addon_path = os.path.dirname(__file__).decode(sys_encoding)
iconfolder = os.path.join(addon_path, "icons")


def dbg(text):
    pprint.pprint(text)
    

config = "empty"
def load_config(conf):
    global config
    config=conf

    # width of entries
    config['maxname'] = 0
    config['maxshortcut'] = 0
    config['context_menu_groups'] = []
    for e in config['v2']:
        if e['Show_in_menu']:
            config['maxname'] = 0
            config['maxshortcut'] = 0
            if e.get('Text_in_menu',False):
                config['maxname']=max(config['maxname'],len(e["Text_in_menu"]))
                if e['Category'] not in config['context_menu_groups']:
                    config['context_menu_groups'].append(e['Category'])
            if e.get('Hotkey',False):
                config['maxshortcut']=max(config['maxshortcut'],len(e["Hotkey"]))
            
    

if ANKI21:
    load_config(mw.addonManager.getConfig(__name__))
    mw.addonManager.setConfigUpdatedAction(__name__,load_config)

    from .shortcuts_buttons_21 import setmycategories,setupButtons21,SetupShortcuts21
    addHook("profileLoaded", lambda: setmycategories(Editor)) 
    addHook("setupEditorButtons", setupButtons21)
    addHook("setupEditorShortcuts", SetupShortcuts21)

    if config.get("v2_show_in_contextmenu",False):
        from .contextmenu import add_to_context
        addHook("EditorWebView.contextMenuEvent", add_to_context)


if not ANKI21:
    moduleDir, _ = os.path.split(__file__)
    path = os.path.join(moduleDir, 'config.json')
    if os.path.exists(path):
        with io.open(path, 'r', encoding='utf-8') as f:
            data=f.read()
        load_config(json.loads(data))

    from .shortcuts_buttons_20 import setmycategories,setupButtons20
    addHook("profileLoaded", lambda: setmycategories(Editor)) 
    addHook("setupEditorButtons", setupButtons20)

    if config.get("v2_show_in_contextmenu",False):  
        from .contextmenu import add_to_context
        addHook("EditorWebView.contextMenuEvent", add_to_context)