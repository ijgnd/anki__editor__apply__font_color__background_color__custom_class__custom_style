import os
import json

from pprint import pprint as pp
from collections import OrderedDict

from aqt import mw

from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QCursor,
)
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QAbstractScrollArea,
    QDialog,
    QHeaderView,
    QMenu,
    QTableView,
    QTableWidgetItem,
)

from aqt.utils import (
    askUser,
    getFile,
    getSaveFile,
    restoreGeom,
    saveGeom,
    showInfo,
    tooltip,
)

from ..defaultconfig import defaultconfig
from ..vars import addonname, addable_options, unique_string

from .forms import settings_main_widgets
from .addEntry import AddEntry
from .utils import gui_dialog


class MainConfDialog(QDialog):
    def __init__(self, c):
        parent = mw.app.activeWindow()
        QDialog.__init__(self, parent)
        self.config = c
        self.bo = settings_main_widgets.Ui_Dialog()
        self.bo.setupUi(self)
        self.bo.cb_classes_to_styling.setParent(None)  # maybe ask user more prominently
        self.bo.cb_global_contextmenu_with_styling.setParent(None)  # To make the add-on less complex I removed the option for an unstyled context menu.
        restoreGeom(self, "class_custom_style_config_gui")
        self.setWindowTitle("Anki: Change Options for Add-on 'Buttons for Color and Style'")
        self.init_tables()
        self.init_buttons()

    def init_buttons(self):
        self.set_check_state_buttons()
        self.bo.pb_modify_active.clicked.connect(
            lambda _, w=self.bo.tw_active: self.process_row(w, "modify"))
        self.bo.pb_modify_inactive.clicked.connect(
            lambda _, w=self.bo.tw_inactive: self.process_row(w, "modify"))
        self.bo.pb_add.clicked.connect(self.onAdd)
        self.bo.pb_deactivate.clicked.connect(
            lambda _, w=self.bo.tw_active: self.process_row(w, "switch"))
        self.bo.pb_activate.clicked.connect(
            lambda _, w=self.bo.tw_inactive: self.process_row(w, "switch"))
        self.bo.pb_delete_from_active.clicked.connect(
            lambda _, w=self.bo.tw_active: self.process_row(w, "del"))
        self.bo.pb_delete_from_inactive.clicked.connect(
            lambda _, w=self.bo.tw_inactive: self.process_row(w, "del"))
        self.bo.cb_classes_to_styling.toggled.connect(self.onClassesToStyling)

        self.bo.multi_button_shortcut.setKeySequence(self.config["v2_key_styling_menu"])
        self.bo.remove_formatting_shortcut.setKeySequence(self.config["v2_key_styling_undo"])

        self.bo.pb_more.clicked.connect(self.onMore)

    def set_check_state_buttons(self):
        if self.config["v2_show_in_contextmenu"]:
            self.bo.cb_global_contextmenu_show.setChecked(True)
        if self.config["v2_menu_styling"]:
            self.bo.cb_global_contextmenu_with_styling.setChecked(True)
        if "write_classes_to_templates" in self.config:
            if self.config["write_classes_to_templates"]:
                self.bo.cb_classes_to_styling.setChecked(True)

    def onMore(self):
        m = QMenu(mw)
        a = m.addAction("Restore default config")
        a.triggered.connect(self.restoreDefault)
        a = m.addAction("Export Button Config to json")
        a.triggered.connect(self.onExport)
        a = m.addAction("Import Button Config from json")
        a.triggered.connect(self.onImport)
        m.exec_(QCursor.pos())

    def restoreDefault(self):
        text = "Delete your setup and restore default buttons config?"
        if askUser(text, defaultno=False):
            self.config["v3"] = defaultconfig["v3"][:]
            self.config["v3_inactive"] = [][:]
            self.active = self.config["v3"]
            self.inactive = self.config["v3_inactive"]
            self.bo.tw_active.setRowCount(0)
            self.bo.tw_inactive.setRowCount(0)
            self.set_table(self.bo.tw_active, self.active)
            self.set_table(self.bo.tw_inactive, self.inactive)

    def onExport(self):
        o = getSaveFile(mw, title="Anki - Select file for export",
                        dir_description="jsonbuttons",
                        key=".json",
                        ext=".json",
                        fname="anki_addon_styling_buttons_config.json"
                        )
        if o:
            self.updateConfig()
            with open(o, 'w') as fp:
                json.dump(self.config, fp)

    def onImport(self):
        o = getFile(self, 
                    title="Anki - Select file for import ", 
                    cb=None, 
                    filter="*.json", 
                    dir=None,
                    key=".json",
                    multi=False)
        if o:
            try:
                with open(o, 'r') as fp:
                    c = json.load(fp)
            except:
                showInfo("Aborting. Error while reading file.")
            try:
                self.config = c
            except:
                showInfo("Aborting. Error in file.")
            self.set_check_state_buttons()
            self.active = self.config["v3"]
            self.inactive = self.config["v3_inactive"]
            self.bo.tw_active.setRowCount(0)
            self.bo.tw_inactive.setRowCount(0)
            self.set_table(self.bo.tw_active, self.active)
            self.set_table(self.bo.tw_inactive, self.inactive)

    def onClassesToStyling(self):
        text = ""
        showInfo(text)

    def onAdd(self):
        e = AddEntry(self)
        if e.exec_():
            self.active.append(e.newsetting)
            self.active = sorted(self.active, key=lambda k: k['Category'])
            self.set_table(self.bo.tw_active, self.active)

    def process_row(self, activewidget, action):
        if activewidget == self.bo.tw_active:
            thisli = self.active
            otherli = self.inactive
            otherwidget = self.bo.tw_inactive
        else:
            thisli = self.inactive
            otherli = self.active
            otherwidget = self.bo.tw_active
        try:
            row = activewidget.currentRow()
        except:
            tooltip("No row selected.")
        else:
            if row != -1:
                if action == "modify":
                    config = thisli[row]
                    a = gui_dialog(self, sel=None, config=config)
                    if a.exec_():
                        thisli[row] = a.newsetting
                        self.set_table(activewidget, thisli)
                if action == "del":
                    text = "Delete row number %s" % str(row+1)
                    if askUser(text, defaultno=True):
                        del thisli[row]
                        self.set_table(activewidget, thisli)
                elif action == "switch":
                    text = "Toggle state row number %s" % str(row+1)
                    if askUser(text, defaultno=True):
                        otherli.append(thisli[row])
                        del thisli[row]
                        thisli = sorted(thisli, key=lambda k: k['Category'])
                        otherli = sorted(otherli, key=lambda k: k['Category'])
                        self.set_table(activewidget, thisli)
                        self.set_table(otherwidget, otherli)
            else:
                tooltip('no row selected.')

    def init_tables(self):
        headers = [("Category", "Category"),
                   ("Hotkey", "Hotkey"),
                   ("Setting", "class (other)"),
                   ("Text_in_menu_styling", "Styling"),
                   ("Text_in_menu_styling_nightmode", "Styling\n(night mode)"),
                   ("Show_in_menu", "Show in\nmenu"),
                   ("Text_in_menu", "Text in\nmenu"),
                   ("extrabutton_show", "extra\nbutton\nshow"),
                   ("extrabutton_text", "extra\nbutton\ntext"),
                   ("extrabutton_tooltip", "extra\nbutton\ntooltip"),
                   ]
        self.tableHeaders = OrderedDict(headers)

        self.active = self.config["v3"]
        if "v3_inactive" in self.config:
            self.inactive = self.config["v3_inactive"]
        else:
            self.inactive = []
        self.active = sorted(self.active, key=lambda k: k['Category'])
        self.inactive = sorted(self.inactive, key=lambda k: k['Category'])
        self.set_table(self.bo.tw_active, self.active)
        self.bo.tw_active.itemDoubleClicked.connect(self.ondoubleclick)
        self.set_table(self.bo.tw_inactive, self.inactive)
        self.bo.tw_inactive.itemDoubleClicked.connect(self.ondoubleclick)

    def set_table(self, widget, li):
        widget.setSelectionBehavior(QTableView.SelectRows)
        widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        widget.setRowCount(len(li))
        widget.setColumnCount(len(self.tableHeaders))
        widget.setHorizontalHeaderLabels(self.tableHeaders.values())
        # widget.verticalHeader().setVisible(False)
        widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        widget.resizeColumnsToContents()
        widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # stretch all to resize
        widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # Stretch
        # per column https://stackoverflow.com/q/38098763
        widget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        widget.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        # widget.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)
        # widget.horizontalHeader().setSectionResizeMode(9, QHeaderView.Stretch)

        # workaround for QTableWidget: add empty strings to all fields to make them clickable
        for i in range(len(li)):
            for j in range(len(self.tableHeaders)):
                newitem = QTableWidgetItem(str(" "))
                widget.setItem(j, i, newitem)

        for rowidx, rowdict in enumerate(li):
            if rowdict["Category"] == "text wrapper":
                rowdict["Setting"] = ""  # this will be fixed when closing the main gui 
                                         # with text_wrapper_workaround
            for k, v in rowdict.items():
                try:
                    index = list(self.tableHeaders.keys()).index(k)
                    if rowdict["Category"] in ["Backcolor (via class)", "Forecolor (via class)", "class (other)"]:
                        if k == "Setting":
                            index = 2
                except ValueError:
                    # field "active" and ugly fix for class styling in Text_in_menu_styling
                    if rowdict["Category"] in ["Backcolor (via class)", "Forecolor (via class)", "class (other)"]:
                        if k == "Text_in_menu_styling":
                            index = 3
                            newitem = QTableWidgetItem(str(v))
                            widget.setItem(rowidx, index, newitem)
                else:
                    newitem = QTableWidgetItem(str(v))
                    widget.setItem(rowidx, index, newitem)

    def ondoubleclick(self, item):
        row = item.row()
        w = item.tableWidget()
        if w == self.bo.tw_active:
            li = self.active
        else:
            li = self.inactive
        config = li[row]
        a = gui_dialog(self, sel=None, config=config)
        if a.exec_():
            li[row] = a.newsetting
            self.set_table(w, li)

    def text_wrapper_workaround(self, list_):
        for row in list_:
            if row["Category"] == "text wrapper":
                before = row["Text_in_menu_styling"]
                after = row["Text_in_menu_styling_nightmode"]
                row["Setting"] = before + unique_string + after
        return list_

    def updateConfig(self):
        self.active = self.text_wrapper_workaround(self.active)
        self.inactive = self.text_wrapper_workaround(self.inactive)
        self.config["v3"] = self.active
        self.config["v3_inactive"] = self.inactive

        self.config["v2_key_styling_menu"] = self.bo.multi_button_shortcut.keySequence().toString()
        self.config["v2_key_styling_undo"] = self.bo.remove_formatting_shortcut.keySequence().toString()

        if self.bo.cb_classes_to_styling.isChecked():
            self.update_all_templates = True
        else:
            self.update_all_templates = False

        if self.bo.cb_global_contextmenu_show.isChecked():
            self.config["v2_show_in_contextmenu"] = True
        else:
            self.config["v2_show_in_contextmenu"] = False

        if self.bo.cb_global_contextmenu_with_styling.isChecked():
            self.config["v2_menu_styling"] = True
        else:
            self.config["v2_menu_styling"] = False

        media_dir = mw.col.media.dir()
        fpath = os.path.join(media_dir, "syncdummy.txt")
        if not os.path.isfile(fpath):
            with open(fpath, "w") as f:
                f.write("anki sync dummy")
        os.remove(fpath)

    def accept(self):
        self.updateConfig()
        saveGeom(self, "class_custom_style_config_gui")
        QDialog.accept(self)

    def reject(self):
        saveGeom(self, "class_custom_style_config_gui")
        QDialog.reject(self)
