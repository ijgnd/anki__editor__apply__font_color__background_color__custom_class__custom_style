# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# License AGPLv3

import os, io
from aqt import mw
from aqt.editor import Editor
from anki.utils import json
from anki.hooks import wrap, addHook
from aqt.utils import showInfo
from anki import version

ANKI21 = version.startswith("2.1.")


###############BEGIN USER CONFIG FPR ANKI 2.0####################
#config for 2.1 is set via the config dialog of 2.1
#config for 2.0 is set in the file config.json
####################END USER CONFIG##############################


def load_config(conf):
    global config
    config=conf

if ANKI21:
    load_config(mw.addonManager.getConfig(__name__))
    mw.addonManager.setConfigUpdatedAction(__name__,load_config) 
else:
    moduleDir, _ = os.path.split(__file__)
    path = os.path.join(moduleDir, 'config.json')
    if os.path.exists(path):
        with io.open(path, 'r', encoding='utf-8') as f:
            data=f.read()
        load_config(json.loads(data))


def hilight(self,color):
    hilighted = "".join(['<span style="background-color:' + color + '">',
                            self.web.selectedText(),
                            '</span>'])
    self.web.eval("document.execCommand('inserthtml', false, %s);"
                % json.dumps(hilighted))
Editor.hilight = hilight


#from anki aqt/editor.py which is
    # Copyright: Damien Elmes <anki@ichi2.net>
    # License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
def _wrapWithColour(self, colour):
    self.web.eval("setFormat('forecolor', '%s')" % colour)


def setupButtons20(self):
    try: 
        config['background']
    except:
        pass
    else:
        for i in config['background']:
            b = self._addButton(i['name'],
                                lambda c=i['color']: self.hilight(c), 
                                text=i['buttontext'], 
                                tip="%s (%s)" % (i['tooltip'], i['hotkey']),
                                key=i['hotkey'])
    try: 
        config['fontcolor']
    except:
        pass
    else:
        for i in config['fontcolor']:
            b = self._addButton(i['name'], 
                                lambda c=i['color']: self._wrapWithColour(c), 
                                text=i['buttontext'],
                                tip="%s (%s)" % (i['tooltip'], i['hotkey']), 
                                key=i['hotkey'])


#adjusted from Mini Format Pack (https://ankiweb.net/shared/info/295889520) which is
    #     Copyright: (c) 2014-2018 Stefan van den Akker <neftas@protonmail.com>
    #                (c) 2017-2018 Damien Elmes <http://ichi2.net/contact.html>
    #                (c) 2018 Glutanimate <https://glutanimate.com/>
    #    License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
def setupButtons21(buttons, editor):
    """Add buttons to Editor for Anki 2.1.x"""
    if config['background']:   
        for action in config['background']:
            try:
                name = action["name"]
                tooltip = action["tooltip"]
                label = action["buttontext"]
                hotkey = action["hotkey"]
                function = lambda editor,c=action["color"]: hilight(editor,c) 
            except KeyError:
                showInfo ("Multi Highlight add-on not configured properly:")
                continue
            b = editor.addButton(
                    icon=None, 
                    cmd=name, 
                    func=function,
                    tip="{} ({})".format(tooltip, hotkey),
                    label=label,
                    keys=hotkey,
                    )
            buttons.append(b)
    if config['fontcolor']:
        for action in config['fontcolor']:
            try:
                name = action["name"]
                tooltip = action["tooltip"]
                label = action["buttontext"]
                hotkey = action["hotkey"]
                function = lambda editor,c=action["color"]: _wrapWithColour(editor,c)
            except KeyError:
                showInfo ("Multi Highlight add-on not configured properly:")
                continue
            b = editor.addButton(
                    icon=None, 
                    cmd=name, 
                    func=function,
                    tip="{} ({})".format(tooltip, hotkey),
                    label=label,
                    keys=hotkey,
                    )
            buttons.append(b)
    return buttons


if ANKI21:   
    addHook("setupEditorButtons", setupButtons21)
else:
    addHook("setupEditorButtons", setupButtons20)
