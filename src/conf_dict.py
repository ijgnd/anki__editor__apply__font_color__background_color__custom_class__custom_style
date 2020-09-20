import os
import pickle

from aqt.utils import askUser, showInfo
from aqt.gui_hooks import (
    profile_did_open,
    profile_will_close,
)

from . import config_var

from .adjust_config import (
    autogenerate_config_values_for_menus, 
    read_and_update_old_v2_config_from_meta_json,
    update_config_for_202005,
)

from .config_var import getconfig
from .defaultconfig import defaultconfig
from .vars import (
    addonname,
    ankiwebpage,
    picklefile,
    user_files_folder
)

from .utils import (
    update_style_file_in_media,
    update_all_templates,
    templates_that_miss_the_import_of_the_styling_file,
    warning_message_about_templates,
)


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


def load_conf_dict():
    config = defaultconfig.copy()
    if os.path.isfile(picklefile):
        with open(picklefile, 'rb') as PO:
            try:
                config = pickle.load(PO)
            except:
                showInfo("Error. Settings file not readable")
    else:
        config = read_and_update_old_v2_config_from_meta_json(config)
    first_after_update_install, config = update_config_for_202005(config)
    config = autogenerate_config_values_for_menus(config)
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


def init_conf_dict():
    profile_did_open.append(load_conf_dict)
    profile_will_close.append(save_conf_dict)
