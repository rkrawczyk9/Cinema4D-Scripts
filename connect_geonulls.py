import c4d
from c4d import gui

def main():
    print('Running connect_geonulls; Connecting the children of each selected object')
    gui.MessageDialog('Connecting the children of each selected object')
    parents = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    doc.StartUndo()
    DeselectAll()
    
    for parent in parents:
        children = parent.GetChildren()
        if len(children) == 0: # Skip if empty
            continue
        else: # If there are multiple things, connect each to its children
            for child in children:
                
                child.SetBit(c4d.BIT_ACTIVE)
                # If it has no children, it's probably an instance, so make it editable
                if child.GetType() in (c4d.Oinstance, c4d.Oxref):
                    c4d.CallCommand(12236) # Make Editable

                # Delete hidden
                for obj in UnfoldRig(child):
                    if obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] == 1:
                        doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, obj)
                        obj.Remove()


                # Connect the contents
                if child.GetDown() != None:
                    child.GetDown().SetBit(c4d.BIT_ACTIVE)
                    c4d.CallCommand(16768) # Connect Objects + Delete
                    #child.GetDown().DelBit(c4d.BIT_ACTIVE) # don't need to delete because it's gone
                #child.DelBit(c4d.BIT_ACTIVE) # don't need to delete because it's gone
                DeselectAll()

        # Delete splines created by Connect
        for newchild in parent.GetChildren():
            if newchild.GetType() == c4d.Ospline:
                doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, newchild)
                newchild.Remove()
    
    doc.EndUndo()
    c4d.EventAdd()
    return

def DeselectAll():
    objs = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    for obj in objs:
        doc.AddUndo(c4d.UNDOTYPE_BITS, obj)
        obj.DelBit(c4d.BIT_ACTIVE)

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