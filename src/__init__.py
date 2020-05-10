# Copyright:  (c) 2019- ignd
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


import os
import re
import pickle
import json
from pprint import pprint as pp

from anki.hooks import wrap, addHook
from anki.utils import json
from aqt import mw
from aqt import editor
from aqt.editor import Editor
from aqt.utils import showInfo, tooltip

from .config import ButtonOptions, get_css_for_editor_from_config
from .colors import hex_to_rgb_tuple, html4colors, css3colors
from .contextmenu import add_to_context
from .editor_apply_styling_functions import setmycategories
from .shortcuts_buttons import setupButtons, SetupShortcuts
from .defaultconfig import defaultconfig
from .vars import (
    css_path,
    picklefile,
    user_files_folder
)
from .oldconfigs import update_config, get_config_from_meta_json
from .editor_set_css_js_for_webview import set_css_js_for_editor


regex = r"(web.*)"
mw.addonManager.setWebExports(__name__, regex)


#### config: on startup load it, then maybe update old version, save on exit
mw.addon_custom_class_config = defaultconfig.copy()


def load_conf_dict():
    conf = mw.addon_custom_class_config
    if os.path.isfile(picklefile):
        with open(picklefile, 'rb') as PO:
            try:
                conf = pickle.load(PO)
            except:
                showInfo("Error. Settings file not readable")
    else:
        # tooltip("Settings file not found")
        conf = get_config_from_meta_json(conf)
    update_style_file_in_media()  # always rewrite the file in case a new profile is used
    conf = update_config(conf)
    if not os.path.exists(user_files_folder):
        os.makedirs(user_files_folder)


def save_conf_dict():
    # prevent error after deleting add-on
    if os.path.exists(user_files_folder):
        with open(picklefile, 'wb') as PO:
            pickle.dump(mw.addon_custom_class_config, PO)


def update_style_file_in_media():
    classes_str = get_css_for_editor_from_config()
    with open(css_path(), "w") as f:
        f.write(classes_str)


def update_all_templates():
    l = """@import url("_editor_button_styles.css");"""
    for m in mw.col.models.all():
        if l not in m['css']:
            model = mw.col.models.get(m['id'])
            model['css'] = l + "\n\n" + model['css']
            mw.col.models.save(model, templates=True)


def onMySettings():
    config = mw.addon_custom_class_config
    # TODO only call settings dialog if Editor or Browser are not active
    # P: User can install "Open the same window multiple times", "Advanced Browser",
    # my "Add and reschedule" so that these are from different classes.
    # tooltip('Close all Browser, Add, Editcurrent windows.')
    dialog = ButtonOptions(config)
    if dialog.exec_():
        config = dialog.config
        config = update_config(config)
        update_style_file_in_media()
        if dialog.update_all_templates:
            update_all_templates()
        l = """@import url("_editor_button_styles.css");"""
        mim = []
        for m in mw.col.models.all():
            if l not in m['css']:
                mim.append(m['name'])
        if not mim:
            msg = ('Restart Anki so that all changes take effect.')
        else:
            msg = ("""Restart Anki so that all changes take effect.\n\n\n"""
                   """Each note type must have the text\n\n"""
                   """  @import url("_editor_button_styles.css");\n\n"""
                   """at the top(!) of """
                   """the "Styling" section in the "Card Types for ..." window.\n\n"""
                   """At the moment the following note types of yours miss this text:"""
                   """\n- %s\nWhen you apply styling with this add-on to notes of these """
                   """types it will show up in the note editor. But it won't be shown """
                   """when you later review cards that belong to these notes.\n\n"""
                   """In other words: There's a good chance that you encounter problems """
                   """in the future because you didn't setup the add-on properly as """
                   """described on the add-on page on Ankiweb.\n\n"""
                   """If you don't want to modify all your note types there's an option"""
                   """"Write Link to CSS into every Template" at the top right of the add-on """
                   """config which should add this line into all your templates. Before you """
                   """use this option make sure to read the section "# Setup" of the add-on """
                   """description.\n\n"""
                   """If you don't know what I mean by """
                   """"Styling" section in the "Card Types for ..." window: """
                   """Watch this video: https://www.youtube.com/watch?v=F1j1Zx0mXME&yt:cc=on """
                   """and see this section of the manual: """
                   """https://apps.ankiweb.net/docs/manual.html#cards-and-templates'""" % 
                   "\n- ".join(mim))
        showInfo(msg, textFormat='plain')  # 'rich')


mw.addonManager.setConfigAction(__name__, onMySettings)


def contextmenu():
    config = mw.addon_custom_class_config
    if config.get("v2_show_in_contextmenu", False):
        addHook("EditorWebView.contextMenuEvent", add_to_context)


addHook("profileLoaded", load_conf_dict)
addHook('unloadProfile', save_conf_dict)

addHook("profileLoaded", contextmenu)
addHook("setupEditorButtons", setupButtons)
addHook("setupEditorShortcuts", SetupShortcuts)
addHook("profileLoaded", lambda: setmycategories(Editor))
addHook("profileLoaded", set_css_js_for_editor)