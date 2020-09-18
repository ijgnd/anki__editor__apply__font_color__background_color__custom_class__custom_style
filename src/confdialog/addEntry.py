from aqt.qt import QDialog, Qt
from aqt.utils import askUser

from .forms import settings_select_category
from .utils import gui_dialog

from ..vars import addonname, addable_options, unique_string


inlinewarning = """
In Anki 2.1 when you copy text from one field to another Anki will remove the background color 
and styles.DOUBLEThis is not just a limitation of this add-on. The same applies e.g. to the 
background color function of the add-on 'Mini Format Pack'.DOUBLEContinue?
""".replace("\n", "").replace("DOUBLE","\n")


classeswarning = """
Applying a class can't be undone with Ctrl/Cmd+Z and the regular Ctrl/Cmd+R doesn't remove the 
classes. Instead this add-on offers a custom shortcut for removing all formatting from selected 
text.DOUBLENote: If you insert unformatted text into a html paragraph that already has some 
formatting the inserted text will also show this formatting. So the remove all formatting" options 
only works as expected if you have unformatted text before your selection.
DOUBLEContinue?
""".replace("\n", "").replace("DOUBLE","\n")


class AddEntry(QDialog):
    def __init__(self, parent=None):
        self.parent = parent
        QDialog.__init__(self, parent, Qt.Window)
        self.dialog = settings_select_category.Ui_Dialog()
        self.dialog.setupUi(self)
        self.dialog.list_categories.addItems(addable_options)
        self.dialog.list_categories.itemDoubleClicked.connect(self.accept)

    def reject(self):
        QDialog.reject(self)

    def accept(self):
        sel = self.dialog.list_categories.currentItem().text()
        if sel in ["Backcolor (inline)", "style (inline)"]:
            if not askUser(inlinewarning):
                return
        if sel in ["class (other)", "Backcolor (via class)", "Forecolor (via class)", "font size (via class)", "class (other), wrapped in div"]:
            if not askUser(classeswarning):
                return
        a = gui_dialog(self, sel=sel, config=None)
        if a.exec_():
            self.newsetting = a.newsetting
            self.newsetting['Category'] = sel
            QDialog.accept(self)
        else:
            QDialog.reject(self)
