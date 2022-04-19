"""Deletes any empty null descendents"""

import c4d
from c4d import gui
import sys
import os
sys.path.append(os.path.dirname(__file__))

import rhelpers

PRINTING = True

def main():
    doc.StartUndo()

    rhelpers.DeleteEmpties( doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER) )

    doc.EndUndo()
    c4d.EventAdd()
    return

if __name__=='__main__':
    main()