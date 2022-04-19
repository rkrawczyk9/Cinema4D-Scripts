import c4d
from c4d import gui

def main():
    printType(doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER) + doc.GetActiveTags())

def printType(objs):
    for obj in objs:
        c4d.GePrint(obj.GetName() + " type: " + str( obj.GetType() ))

if __name__=='__main__':
    main()