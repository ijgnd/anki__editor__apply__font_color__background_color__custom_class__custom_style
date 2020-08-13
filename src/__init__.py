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

import io
import os
import re
import pickle
import json
from pprint import pprint as pp

from anki.utils import json

from aqt import mw
from aqt import editor
from aqt.editor import Editor
from aqt.qt import (
    QAction,
)
from aqt.utils import askUser, showInfo, tooltip
from aqt.gui_hooks import (
    profile_did_open,
    profile_will_close,

    editor_did_init_shortcuts,
    editor_did_init_buttons,
    editor_will_show_context_menu,
)

from .adjust_config import (
    autogenerate_config_values_for_menus, 
    read_and_update_old_v2_config_from_meta_json,
    update_config_for_202005,
)
from .confdialog import MainConfDialog
from . import config_var
from .config_var import getconfig
from .css_for_webviews import create_css_for_webviews_from_config
from .contextmenu import add_to_context
from .defaultconfig import defaultconfig
from .editor_set_css_js_for_webview import set_css_js_for_webview
from .shortcuts_buttons import setupButtons, SetupShortcuts
from .vars import (
    addonname,
    ankiwebpage,
    css_path,
    picklefile,
    user_files_folder
)

regex = r"(web[/\\].*)"
mw.addonManager.setWebExports(__name__, regex)



msg_restart_required = """
Restart Anki (or at leat close all Add, Browser, or EditCurrent windows) so that all changes 
take effect.
""".replace("\n", "")


def warning_message_about_templates(tmpl_list):
    fmted_list = "SINGLE- ".join(tmpl_list)
    return f"""
You have the add-on "{addonname}" installed. This add-on will NOT work with these note types:
SINGLE- {fmted_list}SINGLE
Before you continue read the section about "Updating Templates" on ankiweb at {ankiwebpage}.SINGLE
Auto update these note types?
""".replace("\n", "").replace("SINGLE","\n")


first_start = f"""
This is an infobox from the add-on "{addonname}". It's shown one time because you either 
installed it for the first time or just upgraded. 
The most recent version of this add-on contains a better default config. If you don't use a 
custom config you should consider resetting the config of this add-on to it's default so that 
you get the new config: It's in the upper right corner of the config dialog behind the "more" button. 
DOUBLE
This add-on has some quirks/limitations for technical reasons: You either know some 
background about the anki editor and how to work around these or you will run into some problems 
like disappearing markup or not being able to clear the formatting. If you can't live with 
these limitations don't use this add-on. Just uninstall it. For details see the description 
on ankiweb, {ankiwebpage}.
DOUBLE
This add-on only works if "@import url("_editor_button_styles.css");" is ontop (!) 
the styling section of all your note types. I (addon-creator) have had many "bug" reports because 
people didn't do this. So this add-on offers to automatically add this line to all your note types.
DOUBLE
If something went wrong there would be a lot of damage so that most likely only a backup would help. 
The code that automatically updates your templates has been downloaded thousands of times and I 
haven't heard a complaint. But better safe than sorry: So make sure to have backups and know 
how to restore them. Read the section "Setup" on ankiweb, {ankiwebpage}.
DOUBLE
If you don't update the templates now this add-on offers to auto-update your note types whenever 
you change the add-on config.
DOUBLE
DOUBLE
I have read the description on ankiweb and confirm to have a backup that I know how to restore.
DOUBLE
I want to auto-adjust the styling section of my note types if necessary now.
""".replace("\n", "").replace("DOUBLE", "\n\n")


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
    first_after_update_install, config = update_config_for_202005(config)
    config = autogenerate_config_values_for_menus(config)
    # mw.col.set_config("1899278645_config", config)
    config_var.myconfig = config
    update_style_file_in_media()  # always rewrite the file in case a new profile is used
    if not os.path.exists(user_files_folder):
        os.makedirs(user_files_folder)
    if first_after_update_install:
        if askUser(first_start):
            update_all_templates()
    else:
        missing = templates_that_miss_the_import_of_the_styling_file()
        if missing:
            if askUser(warning_message_about_templates(missing)):
                update_all_templates()
        

def save_conf_dict():
    # prevent error after deleting add-on
    if os.path.exists(user_files_folder):
        with open(picklefile, 'wb') as PO:
            cnf = getconfig()
            if "v3" not in cnf:  # sanity check
                return
            pickle.dump(getconfig(), PO)


def update_style_file_in_media():
    classes_str = create_css_for_webviews_from_config()
    with io.open(css_path(), 'w', encoding='utf-8') as f:
        f.write(classes_str)


def update_all_templates():
    mw.progress.start(immediate=True)
    line = """@import url("_editor_button_styles.css");"""
    # in the additional card fields add-on I use:
    # for mid in mw.col.models.ids():  # but in 2.1.28 method "ids" is labelled as "legacy"
    #     model = mw.col.models.get(mid)
    for model in mw.col.models.all():
        if line not in model['css']:
            model['css'] = line + "\n\n" + model['css']
            # templates=True no longer used in 2.1.28 or later; maybe not needed anyway since
            # the the css/styling section shouldn't affect card generation? But it shouldn't hurt.
            mw.col.models.save(model, templates=True)
    mw.col.models.flush()  # no longer used in 2.1.28 or later
    mw.progress.finish()
    tooltip("Finished updating styling sections")


def templates_that_miss_the_import_of_the_styling_file():
    l = """@import url("_editor_button_styles.css");"""
    mim = []
    for m in mw.col.models.all():
        if l not in m['css']:
            mim.append(m['name'])
    return mim


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
        missing = templates_that_miss_the_import_of_the_styling_file()
        if not missing:
            showInfo(msg_restart_required)
        else:
            msg = msg_restart_required + "\n\n" + warning_message_about_templates(missing)
            if askUser(msg):
                update_all_templates()
mw.addonManager.setConfigAction(__name__, onMySettings)


def contextmenu():
    if getconfig().get("v2_show_in_contextmenu", False):
        editor_will_show_context_menu.append(add_to_context)


action = QAction(mw)
action.setText(f"Adjust config for {addonname}")
mw.form.menuTools.addAction(action)
action.triggered.connect(onMySettings)

set_css_js_for_webview()

profile_did_open.append(load_conf_dict)
profile_did_open.append(contextmenu)
profile_will_close.append(save_conf_dict)

editor_did_init_buttons.append(setupButtons)
editor_did_init_shortcuts.append(SetupShortcuts)
