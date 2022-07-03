from ..config_var import getconfig

from .apply_categories import apply_categories


def setup_shortcuts(cuts, editor):
    config = getconfig()

    for entry in config["v3"]:
        if entry.get("Hotkey", False):
            # remove already existing shortcuts first
            for match in filter(lambda cut: cut[0] == entry["Hotkey"], cuts):
                cuts.remove(match)

            def callback():
                apply_categories[entry["Category"]](editor, entry)

            cuts.append((entry["Hotkey"], callback))
