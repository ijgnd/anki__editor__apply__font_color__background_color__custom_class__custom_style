from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QColor,
) 
from PyQt5.QtWidgets import (
    QColorDialog,
    QDialog,
)

from .helpers import HotkeySelect
from .forms import settings_forecolor_bgcolor


class SettingsForForeBgColor(QDialog):
    def __init__(self, parent=None, category=None, config=None):
        self.category = category
        self.config = config
        self.parent = parent
        QDialog.__init__(self, parent, Qt.Window)
        self.dialog = settings_forecolor_bgcolor.Ui_Dialog()
        self.dialog.setupUi(self)
        self.dialog.pb_hotkeyset.clicked.connect(self.onHotkey)
        self.hotkey = ""
        self.color = ""
        if config:
            if "Hotkey" in config:
                self.hotkey = config["Hotkey"]
                self.dialog.pb_hotkeyset.setText(self.hotkey)
            if "Setting" in config:
                self.color = config["Setting"]  # .replace("background-color: ","").replace(";","")
                self.dialog.pb_color.setText(str(self.color))
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
        self.dialog.pb_color.clicked.connect(self.getColor)

    def onHotkey(self):
        h = HotkeySelect(self, self.hotkey)
        if h.exec_():
            self.hotkey = h.hotkey
            self.dialog.pb_hotkeyset.setText(self.hotkey)

    def getColor(self):
        new = QColorDialog.getColor(QColor(self.color), None)
        if new.isValid():
            self.color = new.name()
        self.dialog.pb_color.setText(str(self.color))

    def reject(self):
        QDialog.reject(self)

    def accept(self):
        self.newsetting = {
            "Category": self.category if self.category else "",
            "Hotkey": self.hotkey,
            "Setting": self.color,  # "background-color: " + self.color + ";",
            "Show_in_menu": self.dialog.cb_contextmenu_show.isChecked(),
            "Text_in_menu":  self.dialog.le_contextmenu_text.text(),
            "Text_in_menu_styling": "",
            "extrabutton_show": self.dialog.cb_extrabutton_show.isChecked(),
            "extrabutton_text":  self.dialog.le_extrabutton_text.text(),
            "extrabutton_tooltip":  self.dialog.le_tooltip_text.text(),
        }
        QDialog.accept(self)
