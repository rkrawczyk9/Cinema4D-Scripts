import c4d
from c4d import gui

def printList(mylist):
    for i in mylist:
        print(i, end='')
        print(', ')

# Main function
def main():
    gui.MessageDialog('Renaming objects')
    objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    renamedObjects = []
    for o in objects:
        if o.GetName()[:10] == 'mixamorig:':
            o.SetName(o.GetName()[10:])
            renamedObjects += o.GetName()
    print("Renamed objects:")
    print(renamedObjects)

# Execute main()
if __name__=='__main__':
    main()