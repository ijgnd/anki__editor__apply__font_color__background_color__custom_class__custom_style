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
)

from .config_var import getconfig
from .default_config import default_config
from .vars import addon_name, addon_webpage, pickle_file, user_files_folder

from .utils import (
    update_style_file_in_media,
    update_all_templates,
    templates_that_miss_the_import_of_the_styling_file,
    warning_message_about_templates,
)


def load_conf_dict():
    config = default_config.copy()
    if os.path.isfile(pickle_file):
        with open(pickle_file, "rb") as PO:
            try:
                config = pickle.load(PO)
            except:
                showInfo("Error. Settings file not readable")
    config = autogenerate_config_values_for_menus(config)
    config_var.myconfig = config
    update_style_file_in_media()  # always rewrite the file in case a new profile is used
    if not os.path.exists(user_files_folder):
        os.makedirs(user_files_folder)
    missing = templates_that_miss_the_import_of_the_styling_file()
    if missing:
        if askUser(warning_message_about_templates(missing)):
            update_all_templates()


def save_conf_dict():
    # prevent error after deleting add-on
    if os.path.exists(user_files_folder):
        with open(pickle_file, "wb") as PO:
            cnf = getconfig()
            if "v3" not in cnf:  # sanity check
                return
            pickle.dump(getconfig(), PO)


def init_conf_dict():
    profile_did_open.append(load_conf_dict)
    profile_will_close.append(save_conf_dict)
