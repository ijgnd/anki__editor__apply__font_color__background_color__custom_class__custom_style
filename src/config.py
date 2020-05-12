# Copyright:  (c) 2019- ignd
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from pprint import pprint as pp

import aqt
from aqt import gui_hooks
from aqt import mw

from . import config_var


def getconfig():
    #return mw.col.get_config("1899278645_config")
    return config_var.myconfig
