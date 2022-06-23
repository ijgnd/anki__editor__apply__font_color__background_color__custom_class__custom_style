from ..config_var import getconfig

from .apply_categories import apply_categories


def setup_shortcuts(cuts, editor):
    config = getconfig()
    for e in config["v3"]:
        if e.get("Hotkey", False):  # and not config["v2_show_in_contextmenu"]:
            func = apply_categories[e["Category"]]

            # remove already existing shortcuts first
            for match in filter(lambda v: v[0] == e["Hotkey"], cuts):
                cuts.remove(match)

            cuts.append((e["Hotkey"], lambda s=e["Setting"], f=func: f(editor, s)))
