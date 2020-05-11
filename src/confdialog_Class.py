import re

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
)

from aqt.utils import showInfo

from .confdialog_Helpers import HotkeySelect
from .forms import settings_class


class SettingsForClass(QDialog):
    def __init__(self, parent=None, config=None):
        self.parent = parent
        self.config = config
        QDialog.__init__(self, parent, Qt.Window)
        self.dialog = settings_class.Ui_Dialog()
        self.dialog.setupUi(self)
        self.dialog.pb_hotkeyset.clicked.connect(self.onHotkey)
        self.hotkey = ""
        self.menuentry = ""
        if config:
            if config["Hotkey"]:
                self.hotkey = config["Hotkey"]
                self.dialog.pb_hotkeyset.setText(self.hotkey)
            if config["Setting"]:
                self.dialog.le_classname.setText(config["Setting"])
            if config["Target group in menu"]:
                self.dialog.le_menu_group.setText(config["Target group in menu"])
            if config["Text_in_menu_styling"]:
                self.dialog.pte_style.insertPlainText(config["Text_in_menu_styling"])
            if config["Text_in_menu_styling_nightmode"]:
                self.dialog.pte_style_nm.insertPlainText(config["Text_in_menu_styling_nightmode"])
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

    def accept(self):
        classname = self.dialog.le_classname.text()
        o = re.match("""-?[_a-zA-Z]+[_a-zA-Z0-9-]*""", classname)
        if not o:
            t = ("Illegal character in classname. "
                 "the name must begin with an underscore (_), a hyphen (-), or a letter(a–z), "
                 "followed by any number of hyphens, underscores, letters, or numbers. "
                 "If the first character is a hyphen, the second character must be a letter"
                 "or underscore, and the name must be at least 2 characters long."
                )
            showInfo(t)
            return
        self.newsetting = {
            "Category": "",  # if new I add in the category in the parent
            "Hotkey": self.hotkey,
            "Setting": self.dialog.le_classname.text(),
            "Show_in_menu": self.dialog.cb_contextmenu_show.isChecked(),
            "Target group in menu": self.dialog.le_menu_group.text(),
            "Text_in_menu":  self.dialog.le_contextmenu_text.text(),
            "Text_in_menu_styling": self.dialog.pte_style.toPlainText(),
            "Text_in_menu_styling_nightmode": self.dialog.pte_style_nm.toPlainText(),
            "extrabutton_show": self.dialog.cb_extrabutton_show.isChecked(),
            "extrabutton_text":  self.dialog.le_extrabutton_text.text(),
            "extrabutton_tooltip":  self.dialog.le_tooltip_text.text(),
        }
        if self.config:   # new entries don't have this entry yet
            if "Category" in self.config:
                self.newsetting["Category"] = self.config["Category"]
        QDialog.accept(self)
