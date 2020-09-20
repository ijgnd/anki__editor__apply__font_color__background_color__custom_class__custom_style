import os

from aqt import mw


addon_path = os.path.dirname(__file__)
addon_folder_name = os.path.basename(addon_path)
web_absolute = os.path.join(addon_path, "web")
js_to_append = [os.path.basename(f) for f in os.listdir(web_absolute) if f.endswith(".js")]
iconfolder = os.path.join(addon_path, "icons")
# don't use settings/meta.json to make it easier to save multiline values
user_files_folder = os.path.join(addon_path, "user_files")
picklefile = os.path.join(user_files_folder, "settings.pypickle")
mjfile = os.path.join(addon_path, "meta.json")
addonname = mw.addonManager.addonName(addon_folder_name)
ankiwebpage = "https://ankiweb.net/shared/info/1899278645"

unique_string = "91cb101665994f66a728db9aa0a4294a"


uses_classes = [
    "class (other)",
    "class (other), wrapped in div",
    "Backcolor (via class)",
    "Forecolor (via class)",
    "font size (via class)",
]

addable_options = [
    "Backcolor (via class)",
    "Forecolor (via class)",
    "font size (via class)",
    "text wrapper",
    "class (other)",
    "class (other), wrapped in div",
    "style (inline)",
    "Forecolor (inline)",
    "Backcolor (inline)",
]

# I use a function because mw.col.media.dir() only works after the profile is loaded
def css_path():
    return os.path.join(mw.col.media.dir(), "_editor_button_styles.css")


def css_path_Customize_Editor_Stylesheet():
    return os.path.join(mw.col.media.dir(), "_editor.css")
