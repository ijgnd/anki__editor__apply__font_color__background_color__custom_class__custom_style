from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
)

from .confdialog_Helpers import HotkeySelect, bg_classname
from .forms import settings_fontsize


class SettingsForFont(QDialog):
    def __init__(self, parent=None, category=None, config=None):
        self.category = category
        self.config = config
        self.parent = parent
        QDialog.__init__(self, parent, Qt.Window)
        self.dialog = settings_fontsize.Ui_Dialog()
        self.dialog.setupUi(self)
        self.dialog.pb_hotkeyset.clicked.connect(self.onHotkey)
        self.hotkey = ""
        self.Text_in_menu_styling_nightmode = ""  # unused
        self.thisclass = bg_classname()
        if config:
            if "Hotkey" in config:
                self.hotkey = config["Hotkey"]
                self.dialog.pb_hotkeyset.setText(self.hotkey)
            if "Setting" in config:
                if config["Setting"]:
                    self.thisclass = config["Setting"]
            if "Text_in_menu_styling" in config:
                self.dialog.le_fontsize.setText(str(config["Text_in_menu_styling"]))
            if config["Show_in_menu"]:
                self.dialog.cb_contextmenu_show.setChecked(True)
            if config["Text_in_menu"]:
                self.dialog.le_contextmenu_text.setText(config["Text_in_menu"])
            if config["extrabutton_show"]:
                self.dialog.cb_extrabutton_show.setChecked(True)
            if config["extrabutton_text"]:
                self.dialog.le_extrabutton_text.setText(config["extrabutton_text"])
            if config["extrabutton_tooltip"]:
                self.dialog.le_tooltip_text.setText(config["extrabutton_tooltip"])

    def onHotkey(self):
        h = HotkeySelect(self, self.hotkey)
        if h.exec_():
            self.hotkey = h.hotkey
            self.dialog.pb_hotkeyset.setText(self.hotkey)

    def reject(self):
        QDialog.reject(self)

    def return_font_size(self):
        font = self.dialog.le_fontsize.text(),  #"font-size:" + self.dialog.le_fontsize.text() + ";",
        return font.rstrip(";").lstrip("font-size:")

    def accept(self):
        self.newsetting = {
            "Category": self.category if self.category else "",
            "Hotkey": self.hotkey,
            "Setting": self.thisclass,
            "Show_in_menu": self.dialog.cb_contextmenu_show.isChecked(),
            "Text_in_menu": self.dialog.le_contextmenu_text.text(),
            "Text_in_menu_styling": self.return_font_size(),
            "Text_in_menu_styling_nightmode": self.Text_in_menu_styling_nightmode,
            "extrabutton_show": self.dialog.cb_extrabutton_show.isChecked(),
            "extrabutton_text":  self.dialog.le_extrabutton_text.text(),
            "extrabutton_tooltip":  self.dialog.le_tooltip_text.text(),
        }
        QDialog.accept(self)
