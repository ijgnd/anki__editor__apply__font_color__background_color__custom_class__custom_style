from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
)

from .confdialog_Helpers import HotkeySelect
from .forms import settings_textwrapper


class SettingsForTextWrapper(QDialog):
    def __init__(self, parent=None, config=None):
        self.parent = parent
        self.config = config
        QDialog.__init__(self, parent, Qt.Window)
        self.dialog = settings_textwrapper.Ui_Dialog()
        self.dialog.setupUi(self)
        self.dialog.pb_hotkeyset.clicked.connect(self.onHotkey)
        self.hotkey = ""
        self.menuentry = ""
        if config:
            if config["Hotkey"]:
                self.hotkey = config["Hotkey"]
                self.dialog.pb_hotkeyset.setText(self.hotkey)
            if config["Target group in menu"]:
                self.dialog.le_menu_group.setText(config["Target group in menu"])
            if config["Text_in_menu_styling"]:
                self.dialog.pte_before.insertPlainText(config["Text_in_menu_styling"])
            if config["Text_in_menu_styling_nightmode"]:
                self.dialog.pte_after.insertPlainText(config["Text_in_menu_styling_nightmode"])
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
        # originally "Setting" was used for the foreground or background color. The value for 
        # "Setting" is used when clicking a menu/button or shortcut. So before/after must be
        # in "Setting"
        # But only set this when closing the dialog so that the unique string is not shown
        # to the user. That workaround is a consequence of reading the config from the 
        # QTableWidget directly ....
        bef = self.dialog.pte_before.toPlainText()
        aft = self.dialog.pte_after.toPlainText()
        self.newsetting = {
            "Category": "text wrapper",
            "Hotkey": self.hotkey,
            "Setting": "", # bef + unique_string + aft, 
            "Show_in_menu": self.dialog.cb_contextmenu_show.isChecked(),
            "Target group in menu": self.dialog.le_menu_group.text(),
            "Text_in_menu":  self.dialog.le_contextmenu_text.text(),
            "Text_in_menu_styling": bef,
            "Text_in_menu_styling_nightmode": aft,
            "extrabutton_show": self.dialog.cb_extrabutton_show.isChecked(),
            "extrabutton_text":  self.dialog.le_extrabutton_text.text(),
            "extrabutton_tooltip":  self.dialog.le_tooltip_text.text(),
        }
        if self.config:   # new entries don't have this entry yet
            if "Category" in self.config:
                self.newsetting["Category"] = self.config["Category"]
        QDialog.accept(self)
