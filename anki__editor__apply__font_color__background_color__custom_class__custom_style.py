from aqt.utils import showInfo
from anki.hooks import addHook

msg = ('''You installed the add-on "editor: apply font color, background color, custom class, custom style" for the old Anki version 2.0.\n\nThis add-on no longer supports this old version 2.0.\n\nI know that it's still listed in the list of versions that are compatible with version 2.0. It's still in this list because a prior version of this add-on was compatible with 2.0. But the latest version of this add-on is no longer compatible with the version 2.0.\n\nThere's no way to unpublish an add-on for the version 2.0 at the moment. The officially recommended way is to 'display the message "as mentioned in the add-on description, 2.0 is no longer supported"', see https://anki.tenderapp.com/discussions/ankiweb/3982-unpublish-delete-add-on-version-for-20.\n\nThe first sentence of my add-on description reads "Don't download this add-on for the old Anki version 2.0" (in bold).\n\n\nJust delete this add-on.\n\nDetails: From your add-on folder delete the file "anki__editor__apply__font_color__background_color__custom_class__custom_style.py".\n\nIf you had a prior version of this add-on installed in your add-on folder you may also find\n- the subfolder "editor__apply__font_color__background_color" and\n- the file "editor  apply  font color  background color.py".\nAlso delete these.\n\nYou can get to your add-on folder from the main window of Anki. In the menu click on Tools->Add-ons->"Open Add-ons Folder". If this doesn't work for you see https://apps.ankiweb.net/docs/manual.html#file-locations.\n\nYou will see this warning message on each startup as long as you don't delete the aforementioned files and folder.''')
    
def mywarning():
    showInfo(msg)

addHook("profileLoaded", mywarning)
