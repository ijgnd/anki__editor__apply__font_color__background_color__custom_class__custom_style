import re

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
)

from aqt.utils import showInfo

from .forms import settings_class


class SettingsForClass(QDialog):
    def __init__(self, parent=None, config=None, inspan=True):
        self.parent = parent
        self.config = config
        QDialog.__init__(self, parent, Qt.Window)
        self.dialog = settings_class.Ui_Dialog()
        self.dialog.setupUi(self)

        self.menuentry = ""
        if config:
            if config["Hotkey"]:
                self.dialog.hotkey.setKeySequence(config["Hotkey"])
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
            if config.get("surround_with_div_tag"):
                self.dialog.cb_surround_with_div.setChecked(config["surround_with_div_tag"])
        if not inspan:
            self.dialog.cb_surround_with_div.setParent(None)

    def reject(self):
        QDialog.reject(self)

    def accept(self):
        classname = self.dialog.le_classname.text()
        o = re.match(r"""^(?!-\d)[a-zA-Z-_][a-zA-Z0-9_][a-zA-Z0-9-_]*$""", classname)
        if not o:
            t = ("Illegal character in classname.\n"
                 "the name can contain only the characters [a-zA-Z0-9], the hyphen (-), the "
                 "underscore (_); it may not start with a digit, two hyphens, or a "
                 "hyphen followed by a digit. It must be at least 2 characters long."
                )
            showInfo(t)
            return
        self.newsetting = {
            "Category": "",  # if new I add in the category in the parent
            "Hotkey": self.dialog.hotkey.keySequence().toString(),
            "Setting": self.dialog.le_classname.text(),
            "Show_in_menu": self.dialog.cb_contextmenu_show.isChecked(),
            "Target group in menu": self.dialog.le_menu_group.text(),
            "Text_in_menu":  self.dialog.le_contextmenu_text.text(),
            "Text_in_menu_styling": self.dialog.pte_style.toPlainText(),
            "Text_in_menu_styling_nightmode": self.dialog.pte_style_nm.toPlainText(),
            "surround_with_div_tag": self.dialog.cb_surround_with_div.isChecked(),            
            "extrabutton_show": self.dialog.cb_extrabutton_show.isChecked(),
            "extrabutton_text":  self.dialog.le_extrabutton_text.text(),
            "extrabutton_tooltip":  self.dialog.le_tooltip_text.text(),
        }
        if self.config:   # new entries don't have this entry yet
            if "Category" in self.config:
                self.newsetting["Category"] = self.config["Category"]
        QDialog.accept(self)
