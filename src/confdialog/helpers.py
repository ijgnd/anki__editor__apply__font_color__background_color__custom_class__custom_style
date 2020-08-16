import random

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
)

from aqt.utils import showInfo

def bg_classname():
    alnum = 'abcdefghijklmnopqrstuvwxyz0123456789'
    id = 'bgCol_'
    for i in range(6):
        id += random.choice(alnum)
    return id
