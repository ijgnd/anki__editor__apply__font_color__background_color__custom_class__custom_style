from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QColor,
) 
from PyQt5.QtWidgets import (
    QColorDialog,
    QDialog,
)

from .helpers import bg_classname
from .forms import settings_forecolor_bgcolor_class


class SettingsForFgBgColorClass(QDialog):
    def __init__(self, parent=None, category=None, config=None):
        self.category = category
        self.config = config
        self.parent = parent
        QDialog.__init__(self, parent, Qt.Window)
        self.dialog = settings_forecolor_bgcolor_class.Ui_Dialog()
        self.dialog.setupUi(self)

        self.color = ""
        self.color_nightmode = ""
        self.thisclass = bg_classname()
        if config:
            if "Hotkey" in config:
                self.dialog.hotkey.setKeySequence(config["Hotkey"])
            if "Setting" in config:
                if config["Setting"]:
                    self.thisclass = config["Setting"]
            if "Text_in_menu_styling" in config:
                self.color = config["Text_in_menu_styling"]
                self.dialog.pb_color.setText(str(self.color))
            if "Text_in_menu_styling_nightmode" in config:
                self.color_nightmode = config["Text_in_menu_styling_nightmode"]
                self.dialog.pb_color_nm.setText(str(self.color_nightmode))
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
        self.dialog.pb_color_nm.clicked.connect(self.getColor_nm)

    def getColor(self):
        new = QColorDialog.getColor(QColor(self.color), None)
        if new.isValid():
            self.color = new.name()
        self.dialog.pb_color.setText(str(self.color))

    def getColor_nm(self):
        new = QColorDialog.getColor(QColor(self.color_nightmode), None)
        if new.isValid():
            self.color_nightmode = new.name()
        self.dialog.pb_color_nm.setText(str(self.color_nightmode))

    def reject(self):
        QDialog.reject(self)

    def accept(self):
        self.newsetting = {
            "Category": self.category if self.category else "",
            "Hotkey": self.dialog.hotkey.keySequence().toString(),
            "Setting": self.thisclass,
            "Show_in_menu": self.dialog.cb_contextmenu_show.isChecked(),
            "Text_in_menu":  self.dialog.le_contextmenu_text.text(),
            "Text_in_menu_styling": self.color,
            "Text_in_menu_styling_nightmode": self.color_nightmode,
            "extrabutton_show": self.dialog.cb_extrabutton_show.isChecked(),
            "extrabutton_text":  self.dialog.le_extrabutton_text.text(),
            "extrabutton_tooltip":  self.dialog.le_tooltip_text.text(),
        }
        QDialog.accept(self)
