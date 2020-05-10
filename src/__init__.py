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

from .config import ButtonOptions
from .colors import hex_to_rgb_tuple, html4colors, css3colors
from .contextmenu import add_to_context
from .shortcuts_buttons_21 import setmycategories, setupButtons21, SetupShortcuts21
from .defaultconfig import defaultconfig
from .vars import *
from .oldconfigs import update_config, get_config_from_meta_json


config = defaultconfig.copy()


def loaddict():
    global config
    if os.path.isfile(picklefile):
        with open(picklefile, 'rb') as PO:
            try:
                config = pickle.load(PO)
            except:
                showInfo("Error. Settings file not readable")
    else:
        # tooltip("Settings file not found")
        config = get_config_from_meta_json(config)
    update_style_file_in_media()  # always rewrite the file in case a new profile is used
    config = update_config(config)
    if not os.path.exists(user_files_folder):
        os.makedirs(user_files_folder)


def savedict():
    # prevent error after deleting add-on
    if os.path.exists(user_files_folder):
        with open(picklefile, 'wb') as PO:
            pickle.dump(config, PO)


media_dir = None
css_path = None


def setCssPath():
    global media_dir
    global css_path
    global css_path_Customize_Editor_Stylesheet
    media_dir = mw.col.media.dir()
    css_path = os.path.join(media_dir, "_editor_button_styles.css")
    css_path_Customize_Editor_Stylesheet = os.path.join(media_dir, "_editor.css")


def prepareEditorStylesheet():
    global config
    global css_path
    global css_path_Customize_Editor_Stylesheet
    css1 = ""
    if os.path.isfile(css_path):
        with open(css_path, "r") as css_file:
            css1 = css_file.read()
    css2 = ""
    if os.path.isfile(css_path_Customize_Editor_Stylesheet):
        with open(css_path_Customize_Editor_Stylesheet, "r") as css_file:
            css2 = css_file.read()
    # TODO adjust height of buttons, maybe add option to make wider, see
    # https://www.reddit.com/r/Anki/comments/ce9wk7/bigger_edit_icons/
    # css2 first in case it contains @import url
    css = css2 + "\n" + css1
    editor_style = "<style>\n{}\n</style>".format(css.replace("%", "%%"))
    editor._html = editor_style + editor._html


def onEditorInit(self, *args, **kwargs):
    """Apply modified Editor HTML"""
    # TODO night mode
    pass


def update_style_file_in_media():
    global config
    global css_path
    classes_str = ""
    for e in config["v3"]:
        if e["Category"] in ["class"]:
            classes_str += ("." + str(e["Setting"]) +
                            "{\n" + str(e['Text_in_menu_styling']) +
                            "\n}\n\n"
                            )
        if e["Category"] == "Backcolor (via class)":
            classes_str += ("." + str(e["Setting"]) +
                            "{\nbackground-color: " + str(e['Text_in_menu_styling']) + ";" +
                            "\n}\n\n"
                            )
    with open(css_path, "w") as f:
        f.write(classes_str)


def update_all_templates():
    l = """@import url("_editor_button_styles.css");"""
    for m in mw.col.models.all():
        if l not in m['css']:
            model = mw.col.models.get(m['id'])
            model['css'] = l + "\n\n" + model['css']
            mw.col.models.save(model, templates=True)


def onMySettings():
    global config
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
    global config
    if config.get("v2_show_in_contextmenu", False):
        addHook("EditorWebView.contextMenuEvent", add_to_context)

addHook("profileLoaded", setCssPath)
addHook("profileLoaded", loaddict)
addHook('unloadProfile', savedict)
addHook("profileLoaded", lambda: setmycategories(Editor))
addHook("profileLoaded", contextmenu)
addHook("setupEditorButtons", setupButtons21)
addHook("setupEditorShortcuts", SetupShortcuts21)

addHook("profileLoaded", prepareEditorStylesheet)
# Editor.__init__ = wrap(Editor.__init__, onEditorInit, "after")
