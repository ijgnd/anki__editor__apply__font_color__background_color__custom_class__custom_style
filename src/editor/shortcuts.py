from ..config_var import getconfig

from .apply_categories import apply_categories


def setup_shortcuts(cuts, editor):
    config = getconfig()

    for entry in config["v3"]:
        if entry.get("Hotkey", False):
            # remove already existing shortcuts first
            for match in filter(lambda cut: cut[0] == entry["Hotkey"], cuts):
                cuts.remove(match)

            cuts.append((entry["Hotkey"], lambda ed=editor, ent=entry, cat=entry["Category"]: apply_categories[cat](ed, ent)))
