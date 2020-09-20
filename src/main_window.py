from aqt import mw
from aqt.qt import QAction
from aqt.utils import askUser, showInfo, tooltip
from anki.hooks import addHook

from .confdialog import MainConfDialog
from .config_var import getconfig

from .adjust_config import (
    autogenerate_config_values_for_menus, 
    read_and_update_old_v2_config_from_meta_json,
    update_config_for_202005,
)

from . import config_var
from .config_var import getconfig

from .utils import (
    update_style_file_in_media,
    update_all_templates,
    templates_that_miss_the_import_of_the_styling_file,
    warning_message_about_templates,
)

msg_restart_required = """
Restart Anki (or at leat close all Add, Browser, or EditCurrent windows) so that all changes 
take effect.
""".replace("\n", "")

def on_settings():
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

def init_menu_option():
    action = QAction(mw)
    action.setText("Custom Styles Options...")

    mw.form.menuTools.addAction(action)
    action.triggered.connect(on_settings)

def init_main_window():
    mw.addonManager.setConfigAction(__name__, on_settings)
    addHook('profileLoaded', init_menu_option)
