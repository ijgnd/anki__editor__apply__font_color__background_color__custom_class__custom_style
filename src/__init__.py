from aqt import mw

from .config_var import init_config_var
from .conf_dict import init_conf_dict
from .main_window import init_main_window
from .editor import init_editor
from .webview import init_webview


regex = r"(web[/\\].*)"
mw.addonManager.setWebExports(__name__, regex)


#### config: on startup load it, then maybe update old version, save on exit
init_config_var()
init_conf_dict()
init_main_window()
init_editor()
init_webview()
