from aqt import mw
from aqt.utils import tooltip
from aqt.operations.notetype import update_notetype_legacy

from .vars import css_path, addon_name, addon_webpage
from .config_var import getconfig


def get_nm_style(configkey):
    e = configkey
    nmsetting = e.get("Text_in_menu_styling_nightmode")
    if nmsetting:
        nmstyle = str(nmsetting)
    else:
        nmstyle = str(e["Text_in_menu_styling"])
    return nmstyle


def create_css_for_webviews_from_config():
    classes_str = ""
    for e in getconfig()["v3"]:
        nmstyle = get_nm_style(e)
        if e["Category"] in ["class (other)", "class (other), wrapped in div"]:
            classes_str += (
                "."
                + str(e["Setting"])
                + "{\n"
                + str(e["Text_in_menu_styling"])
                + "\n}\n\n"
                ".nightMode ." + str(e["Setting"]) + "{\n" + nmstyle + "\n}\n\n"
            )
        if e["Category"] in ["Backcolor (via class)"]:
            classes_str += (
                "."
                + str(e["Setting"])
                + "{\nbackground-color: "
                + str(e["Text_in_menu_styling"])
                + " !important;"
                + "\n}\n\n"
                ".nightMode ."
                + str(e["Setting"])
                + "{\nbackground-color: "
                + nmstyle
                + " !important;"
                + "\n}\n\n"
            )
        if e["Category"] in ["Forecolor (via class)"]:
            classes_str += (
                "."
                + str(e["Setting"])
                + "{\ncolor: "
                + str(e["Text_in_menu_styling"])
                + " !important;"
                + "\n}\n\n"
                ".nightMode ."
                + str(e["Setting"])
                + "{\ncolor: "
                + nmstyle
                + " !important;"
                + "\n}\n\n"
            )
        if e["Category"] in ["font size (via class)"]:
            classes_str += (
                "."
                + str(e["Setting"])
                + "{\nfont-size: "
                + str(e["Text_in_menu_styling"])
                + " !important;"
                + "\n}\n\n"
            )
    return classes_str


def update_style_file_in_media():
    classes_str = create_css_for_webviews_from_config()
    with open(css_path(), "w", encoding="utf-8") as f:
        f.write(classes_str)


def update_all_templates():
    line = """@import url("_editor_button_styles.css");"""
    for model in mw.col.models.all():
        if line not in model["css"]:
            model["css"] = line + "\n\n" + model["css"]
            # mw.col.models.update_dict(model)
            update_notetype_legacy(parent=mw, notetype=model).run_in_background()
    tooltip("Finished updating styling sections")


def templates_that_miss_the_import_of_the_styling_file():
    l = """@import url("_editor_button_styles.css");"""
    mim = []
    for m in mw.col.models.all():
        if l not in m["css"]:
            mim.append(m["name"])
    return mim


def warning_message_about_templates(tmpl_list):
    fmted_list = "SINGLE- ".join(tmpl_list)
    return f"""
You have the add-on "{addon_name}" installed. This add-on will NOT work with these note types:
SINGLE- {fmted_list}SINGLE
Before you continue read the section about "Updating Templates" on ankiweb at {addon_webpage}.SINGLE
Auto update these note types?
""".replace(
        "\n", ""
    ).replace(
        "SINGLE", "\n"
    )
