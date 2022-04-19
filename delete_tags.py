"""Deletes tags on descendents of selected objects"""

import c4d
from c4d import gui

import rhelpers

PRINTING = True

def main():
    doc.StartUndo()

    rhelpers.DeleteTags(doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER))

    doc.EndUndo()
    c4d.EventAdd()
    return

if __name__=='__main__':
    main()