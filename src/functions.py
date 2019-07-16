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


def setmycategories(editor):
    editor.mycategories = {
        'class': editor.my_apply_span_class,
        'style': editor.my_apply_style,
        'Backcolor (inline)': editor.setBackcolor,
        'Backcolor (via class)': editor.my_apply_span_class,
        'Forecolor': editor.setForecolor,
    }
Editor.setmycategories = setmycategories


def setBackcolor(editor, color):
    editor.web.eval("setFormat('backcolor', '%s')" % color)
Editor.setBackcolor = setBackcolor


def setForecolor(editor, color):
    editor.web.eval("setFormat('forecolor', '%s')" % color)
Editor.setForecolor = setForecolor


def my_apply_style(editor, style):
    selected = editor.web.selectedText()
    styled = "".join(['<span style="{}">'.format(style), selected, '</span>'])
    editor.web.eval("document.execCommand('inserthtml', false, %s);"
                    % json.dumps(styled))
Editor.my_apply_style = my_apply_style


def my_apply_span_class(editor, _class):
    selected = editor.web.selectedText()
    styled = "".join(['<span class="{}">'.format(_class), selected, '</span>'])
    editor.web.eval("document.execCommand('inserthtml', false, %s);"
                    % json.dumps(styled))
Editor.my_apply_span_class = my_apply_span_class
