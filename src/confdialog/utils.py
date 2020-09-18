from aqt.utils import showInfo
from ..vars import addonname

from .cssClass import SettingsForClass
from .fgBgColorClass import SettingsForFgBgColorClass
from .fontsize import SettingsForFont
from .foreBgColor import SettingsForForeBgColor
from .style import SettingsForStyle
from .textwrapper import SettingsForTextWrapper


def gui_dialog(inst, sel=None, config=None):
    if not sel:
        sel = config['Category']
    if sel in ["Backcolor (inline)", "Forecolor (inline)"]:
        return SettingsForForeBgColor(inst, sel, config)
    if sel in ["Backcolor (via class)", "Forecolor (via class)"]:
        return SettingsForFgBgColorClass(inst, sel, config)
    if sel == "font size (via class)":
        return SettingsForFont(inst, sel, config)
    if sel == "style (inline)":
        return SettingsForStyle(inst, config)
    if sel in ["class (other)"]:
        return SettingsForClass(inst, config)
    if sel in ["class (other), wrapped in div"]:
        return SettingsForClass(inst, config, inspan=False)
    if sel == "text wrapper":
        return SettingsForTextWrapper(inst, config)
    else:
        text = (f"Error in config of add-on {addonname}\n\n"
                 "The following part of the config contains an error in"
                 "the setting 'Category': "
                f"\n\n{str(config)}"
                 "\n\nClick Abort/Cancel and maybe delete this entry."
                 "\n\nYou might encounter some error messages after this window."
                )
        showInfo(text)
        return
