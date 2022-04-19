# Robert Krawczyk
# selectExpressionTags.py
# Selects all expression tags on children of the selected objects.
# Intended to use to easily change the priority of all tags at once, to stop viewport lag.
import c4d
from c4d import gui

def main():
    objs = []
    for activeObj in doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER):
        objs += UnfoldRig(activeObj)
    SelectTagsByName( objs )

def SelectTagsByName(objs, names=('Constraint', 'Xpresso', 'Motion Solver', 'IK', 'IK-Spline', 'Pose Morph')):

    doc.StartUndo()

    for obj in objs:
        doc.AddUndo(c4d.UNDOTYPE_BITS, obj)
        obj.DelBit(c4d.BIT_ACTIVE) # Deselect the object

        for tag in obj.GetTags():
            if tag.GetName() in names:
                doc.AddUndo(c4d.UNDOTYPE_BITS, tag)
                tag.SetBit(c4d.BIT_ACTIVE) # Select the tag

    doc.EndUndo()
    c4d.EventAdd()
    gui.MessageDialog('Selected all expression tags in the tree')
    return




def UnfoldRig(root):
    """Returns an object and its children as a python list."""
    objlist = []
    objlist.append(root)
    if root.GetDown() != None:
        UnfoldRig_recurse(root.GetDown(), objlist)
    return objlist
def UnfoldRig_recurse(root, objlist):
    objlist.append(root)

    if root.GetDown() != None:
        objlist = UnfoldRig_recurse(root.GetDown(), objlist)

    if root.GetNext() != None:
        objlist = UnfoldRig_recurse(root.GetNext(), objlist)

    return objlist

if __name__=='__main__':
    main()