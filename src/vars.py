import os

from aqt import mw

addon_path = os.path.dirname(__file__)
iconfolder = os.path.join(addon_path, "icons")
# don't use settings/meta.json to make it easier to save multiline values
user_files_folder = os.path.join(addon_path, "user_files")
picklefile = os.path.join(user_files_folder, "settings.pypickle")
mjfile = os.path.join(addon_path, "meta.json")
addonname = "editor: apply font color, background color custom class, custom style"   


# I use a function because mw.col.media.dir() only works after the profile is loaded
def css_path():
    return os.path.join(mw.col.media.dir(), "_editor_button_styles.css")


def css_path_Customize_Editor_Stylesheet():
    return os.path.join(mw.col.media.dir(), "_editor.css")
