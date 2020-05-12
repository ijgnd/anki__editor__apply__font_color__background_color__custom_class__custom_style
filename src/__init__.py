"""
Copyright:  (c) 2019- ignd
            (c) 2014-2018 Stefan van den Akker
            (c) 2017-2018 Damien Elmes
            (c) 2018 Glutanimate


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


This add-on uses "rangy" in the folder "web" which is covered by the following copyright and 
permission notice:

    The MIT License (MIT)

    Copyright (c) 2014 Tim Down

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE. 



"""


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
from aqt.qt import (
    QAction,
)
from aqt.utils import showInfo, tooltip


from .confdialog_MAIN import MainConfDialog
from .config_var import getconfig
from .css_for_webviews import create_css_for_webviews_from_config
from . import config_var
from .colors import hex_to_rgb_tuple, html4colors, css3colors
from .contextmenu import add_to_context
from .editor_apply_styling_functions import setmycategories
from .shortcuts_buttons import setupButtons, SetupShortcuts
from .defaultconfig import defaultconfig
from .vars import (
    addonname,
    css_path,
    picklefile,
    user_files_folder
)
from .adjust_config import (
    autogenerate_config_values_for_menus, 
    read_and_update_old_v2_config_from_meta_json,
    update_config_for_202005,
)
from . import editor_set_css_js_for_webview



regex = r"(web.*)"
mw.addonManager.setWebExports(__name__, regex)


#### config: on startup load it, then maybe update old version, save on exit
config_var.init()


def load_conf_dict():
    config = defaultconfig.copy()
    if os.path.isfile(picklefile):
        with open(picklefile, 'rb') as PO:
            try:
                config = pickle.load(PO)
            except:
                showInfo("Error. Settings file not readable")
    else:
        # tooltip("Settings file not found")
        config = read_and_update_old_v2_config_from_meta_json(config)
    config = update_config_for_202005(config)
    config = autogenerate_config_values_for_menus(config)
    # mw.col.set_config("1899278645_config", config)
    config_var.myconfig = config
    update_style_file_in_media()  # always rewrite the file in case a new profile is used
    if not os.path.exists(user_files_folder):
        os.makedirs(user_files_folder)


def save_conf_dict():
    # prevent error after deleting add-on
    if os.path.exists(user_files_folder):
        with open(picklefile, 'wb') as PO:
            pickle.dump(getconfig(), PO)


def update_style_file_in_media():
    classes_str = create_css_for_webviews_from_config()
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
    # TODO only call settings dialog if Editor or Browser are not active
    # P: User can install "Open the same window multiple times", "Advanced Browser",
    # my "Add and reschedule" so that these are from different classes.
    # tooltip('Close all Browser, Add, Editcurrent windows.')
    dialog = MainConfDialog(getconfig())
    if dialog.exec_():
        new = autogenerate_config_values_for_menus(dialog.config)
        # mw.col.set_config("1899278645_config", new)
        config_var.myconfig = new
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
                   """config which should add this line into all your templates.\n\n"""
                   """If you don't know what I mean by """
                   """"Styling" section in the "Card Types for ..." window: """
                   """Watch this video: https://www.youtube.com/watch?v=F1j1Zx0mXME&yt:cc=on """
                   """and see this section of the manual: """
                   """https://apps.ankiweb.net/docs/manual.html#cards-and-templates'""" % 
                   "\n- ".join(mim))
        showInfo(msg, textFormat='plain')  # 'rich')


mw.addonManager.setConfigAction(__name__, onMySettings)


def contextmenu():
    if getconfig().get("v2_show_in_contextmenu", False):
        addHook("EditorWebView.contextMenuEvent", add_to_context)


action = QAction(mw)
action.setText(f"Configure {addonname}")
mw.form.menuTools.addAction(action)
action.triggered.connect(onMySettings)



addHook("profileLoaded", load_conf_dict)
addHook('unloadProfile', save_conf_dict)

addHook("profileLoaded", contextmenu)
addHook("setupEditorButtons", setupButtons)
addHook("setupEditorShortcuts", SetupShortcuts)
addHook("profileLoaded", lambda: setmycategories(Editor))
