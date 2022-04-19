import c4d
from c4d import gui
import sys
import os
sys.path.append(os.path.dirname(__file__))

import rhelpers

PRINTING = True

def main():
    # Select Root (parent of all currently selected)
    root = doc.GetActiveObject()
    while rhelpers.RemoveAllPrefixes(root.GetName()) != "Root":
        root = root.GetUp()
        if root == None:
            gui.MessageDialog("No 'Root' found as ancestor of selected")
            return

    # Run delete_tags.py and delete_empties.py
    DeleteTags(root)
    DeleteEmpties(root)

    # Tell user it's done
    gui.MessageDialog("Skeleton cleaned, now you can export it :)\n\nCheck Selection Only and Animation. For Unreal, use Up Axis: Z")

    # Open Export FBX dialog
    c4d.CallCommand(60000, 12) # Export FBX

    c4d.EventAdd()
    return

def DeleteTags(root):
    """Deletes all tags on descendents"""
    doc = c4d.documents.GetActiveDocument()
    if PRINTING:
        c4d.GePrint("Running delete_tags")

    for obj in rhelpers.UnfoldRigs( root ):
        for tag in obj.GetTags():
            if PRINTING:
                c4d.GePrint("- deleting " + tag.GetName())
            doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, tag)
            tag.Remove()

    if PRINTING:
        c4d.GePrint("delete_tags done\n")
    return

def DeleteEmpties(roots):
    """Deletes all descendent empty nulls and splines, helper sites, and bounding boxes"""
    doc = c4d.documents.GetActiveDocument()
    if PRINTING:
        c4d.GePrint("Running delete_empties")

    for obj in reversed( rhelpers.UnfoldRigs( roots ) ):
        # Starting with deepest descendents (to catch nulls with only empty nulls for children,)
        # Delete empty nulls
        if obj.GetType() in (c4d.Onull, c4d.Ospline) and obj.GetDown() == None:
            deleteIt(obj)
        # Delete helper sites
        elif obj.GetType()==c4d.Ojoint and "helpersite" in obj.GetName().lower():
            rhelpers.deleteIt(obj)
        # Delete bounding boxes
        elif obj.GetType()!=c4d.Ojoint and rhelpers.RemoveAllPrefixes(obj.GetName()).lower()=="bounds":
            rhelpers.deleteIt(obj)

    if PRINTING:
        c4d.GePrint("delete_empties done\n")
    return
def deleteIt(obj):
    if PRINTING:
        c4d.GePrint("- deleting " + obj.GetName())
    c4d.documents.GetActiveDocument().AddUndo(c4d.UNDOTYPE_DELETEOBJ, obj)
    obj.Remove()

# Execute main()
if __name__=='__main__':
    main()