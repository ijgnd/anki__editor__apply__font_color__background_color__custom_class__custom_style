from .config_var import getconfig


def get_nm_style(configkey):
    e = configkey
    nmsetting = e.get('Text_in_menu_styling_nightmode')
    if nmsetting:
        nmstyle = str(nmsetting)
    else:
        nmstyle = str(e['Text_in_menu_styling'])
    return nmstyle


def create_css_for_webviews_from_config():
    classes_str = ""
    for e in getconfig()["v3"]:
        nmstyle = get_nm_style(e)
        if e["Category"] in ["class (other)", "class (other), wrapped in div"]:
            classes_str += ("." + str(e["Setting"]) +
                            "{\n" + str(e['Text_in_menu_styling']) +
                            "\n}\n\n"
                            ".nightMode ." + str(e["Setting"]) +
                            "{\n" + nmstyle +
                            "\n}\n\n"
                            )
        if e["Category"] in ["Backcolor (via class)"]:
            classes_str += ("." + str(e["Setting"]) +
                            "{\nbackground-color: " + str(e['Text_in_menu_styling']) + " !important;" +
                            "\n}\n\n"
                            ".nightMode ." + str(e["Setting"]) +
                            "{\nbackground-color: " + nmstyle + " !important;" +
                            "\n}\n\n"
                            )
        if e["Category"] in ["Forecolor (via class)"]:
            classes_str += ("." + str(e["Setting"]) +
                            "{\ncolor: " + str(e['Text_in_menu_styling']) + " !important;" +
                            "\n}\n\n"
                            ".nightMode ." + str(e["Setting"]) +
                            "{\ncolor: " + nmstyle + " !important;" +
                            "\n}\n\n"
                            )
        if e["Category"] in ["font size (via class)"]:
            classes_str += ("." + str(e["Setting"]) +
                            "{\nfont-size: " + str(e['Text_in_menu_styling']) + " !important;" +
                            "\n}\n\n"
                            )
    return classes_str
