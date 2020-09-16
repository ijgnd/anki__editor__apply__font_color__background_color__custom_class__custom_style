from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
)

from .forms import settings_style


class SettingsForStyle(QDialog):
    def __init__(self, parent=None, config=None):
        self.parent = parent
        self.config = config
        QDialog.__init__(self, parent, Qt.Window)
        self.dialog = settings_style.Ui_Dialog()
        self.dialog.setupUi(self)
        self.color = ""
        if config:
            if config["Hotkey"]:
                self.dialog.hotkey.setKeySequence(config["Hotkey"])
            if config["Setting"]:
                self.dialog.pte_style.insertPlainText(config["Setting"])
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

    def reject(self):
        QDialog.reject(self)

    def accept(self):
        self.newsetting = {
            "Category": "",  # if new I add in the category in the parent
            "Hotkey": self.dialog.hotkey.keySequence().toString(),
            "Setting": self.dialog.pte_style.toPlainText(),
            "Show_in_menu": self.dialog.cb_contextmenu_show.isChecked(),
            "Text_in_menu":  self.dialog.le_contextmenu_text.text(),
            "Text_in_menu_styling": self.dialog.pte_style.toPlainText(),
            "Text_in_menu_styling_nightmode": "",
            "extrabutton_show": self.dialog.cb_extrabutton_show.isChecked(),
            "extrabutton_text":  self.dialog.le_extrabutton_text.text(),
            "extrabutton_tooltip":  self.dialog.le_tooltip_text.text(),
        }
        if self.config:   # new entries don't have this entry yet
            if "Category" in self.config:
                self.newsetting["Category"] = self.config["Category"]
        QDialog.accept(self)
