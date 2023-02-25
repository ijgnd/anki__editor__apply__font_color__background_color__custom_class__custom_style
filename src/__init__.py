from aqt.qt import qtmajor
from aqt.utils import tooltip
from .vars import addon_name


if qtmajor == 5:
    msg = f"""The addon "{addon_name}" does not support Anki versions built with pyqt5."""
    print(msg)
    tooltip(msg)
else:
    from aqt import mw


    from .config_var import init_config_var
    from .conf_dict import init_conf_dict
    from .main_window import init_main_window
    from .editor import init_editor


    regex = r"(web[/\\].*)"
    mw.addonManager.setWebExports(__name__, regex)


    # config: on startup load it, then maybe update old version, save on exit
    init_config_var()
    init_conf_dict()
    init_main_window()
    init_editor()
