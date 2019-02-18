# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Copyright:  (c) 2019 ignd
            (c) 2014-2018 Stefan van den Akker
            (c) 2017-2018 Damien Elmes
            (c) 2018 Glutanimate
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Use this at your own risk
"""

from aqt.editor import Editor

from .menu import *
from .functions import *
from .main import config, iconfolder

#######workaround
def makebuttons20(editor,e,func):
    editor._addButton(e['extrabutton_text'],
            lambda c=e['Setting']: func(c),
            text=e['extrabutton_text'], 
            tip="%s (%s)" % (e['extrabutton_tooltip'], e['Hotkey']),
            key=e['Hotkey'])
Editor.makebuttons20 = makebuttons20


def setupButtons20(self):
    for e in config['v2']:
        if e.get('extrabutton_show',False):
            if e['Category'] == 'backcolor':
                self.makebuttons20(e,self.setBackcolor20)
            elif e['Category'] == 'forecolor':
                self.makebuttons20(e,self.setForecolor20)
            elif e['Category'] == 'class':
                self.makebuttons20(e,self.my_apply_span_class)
            elif e['Category'] == 'style':
                self.makebuttons20(e,self.my_apply_style)
        elif e.get("Hotkey",False):
            s = QShortcut(QKeySequence(e["Hotkey"]),self.parentWindow)
            if e['Category'] == 'backcolor':
                s.connect(s, SIGNAL("activated()"), lambda s=e['Setting']: setBackcolor20(self,s))
            elif e['Category'] == 'forecolor':
                s.connect(s, SIGNAL("activated()"), lambda s=e['Setting']: setForecolor20(self,s))
            elif e['Category'] == 'class':
                s.connect(s, SIGNAL("activated()"), lambda s=e['Setting']: my_apply_span_class(self,s))
            elif e['Category'] == 'style':
                s.connect(s, SIGNAL("activated()"), lambda s=e['Setting']: my_apply_style(self,s))

    #collapsible menu
    for e in config['v2']:
        if e['Show_in_menu']:
            show_style_selector_button = True
    if show_style_selector_button:
        if config['v2_menu_styling'] is True:
            func = self.additional_menu_styled
        else:
            func = self.additional_menu_basic
        self._addButton("thename",  
            func, 
            text="|||", 
            tip="advanced styling options",
            size=False if config['v2_wider_button_in_menu'] else True,
            key=config['v2_key_styling_menu'])

#######


# def makebuttons20(editor,e,func):
#     editor._addButton(e['extrabutton_text'],
#             lambda d=editor,c=e['Setting']: func(d,c),
#             text=e['extrabutton_text'], 
#             tip="%s (%s)" % (e['extrabutton_tooltip'], e['Hotkey']),
#             key=e['Hotkey'])
# Editor.makebuttons20 = makebuttons20


# def setupButtons20(editor):
#     for e in config['v2']:
#         f1 = editor.mycategories[e['Category']]
#         if e.get('extrabutton_show',False):    #sets Hotkeys and Button
#             editor.makebuttons20(e,f1)
#         elif e.get("Hotkey",False):
#             s = QShortcut(QKeySequence(e["Hotkey"]),editor.parentWindow)
#             #THIS DOESN'T WORK
#             s.connect(s, SIGNAL("activated()"), lambda d=editor,s=e['Setting']: f1(d,s))

#     #collapsible menu
#     for e in config['v2']:
#         if e['Show_in_menu']:
#             show_style_selector_button = True
#     if show_style_selector_button:
#         if config['v2_menu_styling'] is True:
#             func = editor.additional_menu_styled
#         else:
#             func = editor.additional_menu_basic
#         editor._addButton("thename",  
#             func, 
#             text="|||", 
#             tip="advanced styling options",
#             size=False,
#             key="")