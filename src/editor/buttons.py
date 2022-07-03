from typing import Optional
from functools import reduce
from os.path import join

from aqt.utils import shortcut

from ..config_var import getconfig
from ..vars import iconfolder

from .menu import additional_menu_styled
from .apply_categories import apply_categories


def generate_button(editor, entry) -> Optional[str]:
    name = entry["Text_in_menu"]
    category = entry["Category"]

    def callback(_):
        apply_categories[category](editor, entry)

    tip = (
        f'{entry["extrabutton_tooltip"]} '
        f'{entry["Setting"]} '
        f'({shortcut(entry["Hotkey"])})'
    )
    label = entry["extrabutton_text"]

    return editor.addButton(
        None,
        name,
        callback,
        tip,
        label,
    )


def setup_extra_buttons(buttons, editor):
    config = getconfig()

    # extrabutton
    for entry in filter(
        lambda entry: entry.get("extrabutton_show", False), config["v3"]
    ):
        buttons.append(generate_button(editor, entry))


def setup_more_button(buttons, editor):
    config = getconfig()

    # collapsible menu
    if not reduce(
        lambda accu, entry: accu or entry["Show_in_menu"],
        config["v3"],
        False,
    ):
        return

    icon = join(iconfolder, "more_rotated.png")
    key = config["v2_key_styling_menu"]

    buttons.append(
        editor.addButton(
            icon,
            "customStylesMore",
            additional_menu_styled,
            "Apply Custom Styles",
            keys=key,
        )
    )
