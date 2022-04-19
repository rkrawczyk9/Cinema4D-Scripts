import c4d
from c4d import gui

PRINTING = True

def main():
    if PRINTING:
        gui.MessageDialog('Extract XZ\n\nRunning part 2')
    if extract_xz_pt2():
        gui.MessageDialog('Extract XZ complete!\nNow you can add the skeleton as a motion clip and blend relatively seamlessly without worrying about position.')

def extract_xz_pt2():
    # Starting up
    root = doc.GetFirstObject()
    Pos_Orig = root.GetDown().GetNext()
    if Pos_Orig == None:
        gui.MessageDialog("No baked Pos_Orig found. Run extract_xz, do Timeline>Functions>Bake Objects, then run this")
        return False
    elif Pos_Orig.GetName() != "Pos_Orig (Copy)":
        gui.MessageDialog("No baked Pos_Orig found. Run extract_xz, do Timeline>Functions>Bake Objects, then run this")
        return False

    doc.StartUndo()

    # Rename
    doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, Pos_Orig)
    Pos_Orig.SetName("Pos_Orig")

    # Delete old Pos_Orig
    if Pos_Orig.GetPred() != None:
        if Pos_Orig.GetPred().GetName() == "Pos_Orig":
            doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, Pos_Orig.GetPred())
            Pos_Orig.GetPred().Remove()
            if PRINTING:
                print("deleted expression-driven Pos_Orig")

    # Delete Hips_orig
    if Pos_Orig.GetNext() != None:
        if Pos_Orig.GetNext().GetName() == "Hips_orig":
            doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, Pos_Orig.GetNext())
            Pos_Orig.GetNext().Remove()
            if PRINTING:
                print("deleted Hips_orig")

    if Pos_Orig.GetNext() != None:
        # Delete Hips_orig (Copy)
        if Pos_Orig.GetNext().GetName() == "Hips_orig (Copy)":
            doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, Pos_Orig.GetNext())
            Pos_Orig.GetNext().Remove()
            if PRINTING:
                print("deleted Hips_orig (Copy)")

    # For some reason a second root is created (sometimes?)
    # Delete extra root
    if root.GetNext() != None:
        if root.GetNext().GetName() == root.GetName() + " (Copy)":
            doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, root.GetNext())
            root.GetNext().Remove()
            if PRINTING:
                print("deleted extra root: " + root.GetName() + " (Copy)")

    # Change color of this skeleton to indicate that it has been processed
    for obj in UnfoldRig(root):
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        obj[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(.5,0,.8)

    # Finishing up
    doc.EndUndo()
    c4d.EventAdd()
    return True


def UnfoldRig(root):
    """Returns an object and its children as a python list."""
    objlist = []
    objlist.append(root)
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