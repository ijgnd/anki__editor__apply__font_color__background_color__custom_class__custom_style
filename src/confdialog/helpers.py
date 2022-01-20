import random

from aqt.utils import showInfo

def bg_classname():
    alnum = 'abcdefghijklmnopqrstuvwxyz0123456789'
    id = 'bgCol_'
    for i in range(6):
        id += random.choice(alnum)
    return id
