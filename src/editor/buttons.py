from typing import Optional
from functools import reduce
from os.path import join

from aqt.utils import showInfo

from ..config_var import getconfig
from ..vars import iconfolder

from .menu import additional_menu_basic, additional_menu_styled
from .apply_categories import apply_categories


def generate_button(editor, entry) -> Optional[str]:
    try:
        name = entry["Text_in_menu"]

        func = apply_categories[entry['Category']]
        funct = lambda e=editor, c=entry["Setting"]: func(e, c)

        tip = f'{entry["extrabutton_tooltip"]} {entry["Setting"]} ({entry["Hotkey"]})'
        label = entry["extrabutton_text"]

    except KeyError:
        showInfo("Multi Highlight add-on not configured properly")
        return None

    button = editor.addButton(None, name, funct, tip, label)

    return button

def setup_extra_buttons(buttons, editor):
    config = getconfig()

    # extrabutton
    for entry in filter(lambda entry: entry.get('extrabutton_show', False), config['v3']):
        buttons.append(generate_button(editor, entry))

def setup_more_button(buttons, editor):
    config = getconfig()

    # collapsible menu
    should_show = reduce(lambda accu, entry: accu or entry['Show_in_menu'], config['v3'], False)

    if not should_show:
        return

    icon = join(iconfolder, "more_rotated.png")
    func = additional_menu_styled if config['v2_menu_styling'] else additional_menu_basic

    b = editor.addButton(
        icon,
        "XX",
        func,
        "Apply Custom Styles",
        config['v2_key_styling_menu'],
    )

    buttons.append(b)
