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
from anki.utils import json
from .main import ANKI21

def setmycategories(editor):
    editor.mycategories = {
        'class': editor.my_apply_span_class,
        'style': editor.my_apply_style,
        #'backcolor': editor.setBackcolor,
        #'forecolor': editor.setForecolor,
    }
    # I can set the styling in four ways: dedicated button,
    # shortcut, menu and context menu. 
    # I run into this problem for some of these:
    # contextmenu in 2.0 requires this workaroudn
    # commented out buttons in shortcuts_functions_20, too:
    # setBackcolor/setForecolor don't persist in 2.0: They are shown but if e.g.
    # I press ctrl+shift+x in a different field to edit its html contents the
    # markup disappears. I don't have this problem in 2.1. 
    # This is a workaround since the exact function setForecolor is built into
    # Anki 2.0 and works well in it
    if ANKI21:
        editor.mycategories['backcolor'] = editor.setBackcolor
        editor.mycategories['forecolor'] = editor.setForecolor
    else:
        editor.mycategories['backcolor'] = editor.setBackcolor20
        editor.mycategories['forecolor'] = editor.setForecolor20
Editor.setmycategories = setmycategories


def setBackcolor20(editor,c):
    hilighted = "".join(['<span style="background-color:' + c + '">',
                            editor.web.selectedText(),
                            '</span>'])
    editor.web.eval("document.execCommand('inserthtml', false, %s);"
                % json.dumps(hilighted))
Editor.setBackcolor20 = setBackcolor20


def setForecolor20(editor,c):
    hilighted = "".join(['<span style="color:' + c + '">',
                            editor.web.selectedText(),
                            '</span>'])
    editor.web.eval("document.execCommand('inserthtml', false, %s);"
                % json.dumps(hilighted))
Editor.setForecolor20 = setForecolor20


def setBackcolor(editor,colour):
    editor.web.eval("setFormat('backcolor', '%s')" % colour)
Editor.setBackcolor = setBackcolor


def setForecolor(editor, colour):
    editor.web.eval("setFormat('forecolor', '%s')" % colour)
Editor.setForecolor = setForecolor


def my_apply_style(editor,style):
    selected = editor.web.selectedText()
    styled = "".join(['<span style="{}">'.format(style),selected,'</span>'])
    editor.web.eval("document.execCommand('inserthtml', false, %s);"
                % json.dumps(styled))
Editor.my_apply_style = my_apply_style


def my_apply_span_class(editor,_class):
    selected = editor.web.selectedText()
    styled = "".join(['<span class="{}">'.format(_class),selected,'</span>'])
    editor.web.eval("document.execCommand('inserthtml', false, %s);"
                % json.dumps(styled))
Editor.my_apply_span_class = my_apply_span_class
