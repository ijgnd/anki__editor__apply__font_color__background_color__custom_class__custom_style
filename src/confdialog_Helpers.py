import random

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
)

from aqt.utils import showInfo

from .forms import settings_shortcut


def bg_classname():
    alnum = 'abcdefghijklmnopqrstuvwxyz0123456789'
    id = 'bgCol_'
    for i in range(6):
        id += random.choice(alnum)
    return id


class HotkeySelect(QDialog):
    def __init__(self, parent=None, shortcut=None):
        self.parent = parent
        QDialog.__init__(self, parent, Qt.Window)
        self.dialog = settings_shortcut.Ui_Dialog()
        self.dialog.setupUi(self)
        if shortcut:
            if ("super" or "meta") in shortcut:
                text = ("illegal key name like 'super' or 'meta' in shortcut "
                        "defintion. In the following window make sure to check and "
                        "adjust the line/setting 'Button'."
                        )
                showInfo(text)
            shortcut = shortcut.lower()
            if "ctrl" in shortcut:
                shortcut = shortcut.replace("ctrl+", "")
                self.dialog.cb_ctrl.setChecked(True)
            if "shift" in shortcut:
                shortcut = shortcut.replace("shift+", "")
                self.dialog.cb_shift.setChecked(True)
            if "alt" in shortcut:
                shortcut = shortcut.replace("alt+", "")
                self.dialog.cb_alt.setChecked(True)
            if "meta" in shortcut:
                shortcut = shortcut.replace("meta+", "")
                self.dialog.cb_metasuper.setChecked(True)
            self.dialog.le_key.setText(shortcut)

    def reject(self):
        QDialog.reject(self)

    def accept(self):
        self.hotkey = ""
        if self.dialog.cb_ctrl.isChecked():
            self.hotkey += "Ctrl+"
        if self.dialog.cb_shift.isChecked():
            self.hotkey += "Shift+"
        if self.dialog.cb_alt.isChecked():
            self.hotkey += "Alt+"
        if self.dialog.cb_metasuper.isChecked():
            self.hotkey += "Meta+"
        self.hotkey += self.dialog.le_key.text().upper()
        QDialog.accept(self)
