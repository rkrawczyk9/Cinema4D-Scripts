import c4d
from c4d import gui
import math

def main():
    muz_roots = []
    muz_locs = []
    titus_root = None
    fireMain_loc = None
    fireEyes_loc = None
    for root in doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER):
        if "Merc" in root.GetName() or "Colt" in root.GetName():
            muz_roots.append(root)
        elif "Titus" in root.GetName():
            titus_root = root

    DeselectAll()

    for i in range(len(muz_roots)):
        muz_root = muz_roots[i]
        muz_locs.append( c4d.BaseObject(c4d.Onull) )
        muz_locs[i].SetName("muz_loc_"+str(i))
        doc.InsertObject(muz_locs[i])
        c4d.EventAdd()

        gun = FindObjWithName(UnfoldRig(muz_root), "GEO_Gun", objType=c4d.Ojoint, contains=True, removePrefixes=False)
        # Create constraint
        muz_locs[i].SetBit(c4d.BIT_ACTIVE)
        gun.SetBit(c4d.BIT_ACTIVE)
        c4d.CallCommand(1022414) # Add PSR Constraint
        DeselectAll()

        # Set constraint offset PSR
        c = muz_locs[i].GetFirstTag()
        #c[c4d.ID_CA_CONSTRAINT_TAG_PSR_P_OFFSET,c4d.VECTOR_X] = -267.0
        #c[c4d.ID_CA_CONSTRAINT_TAG_PSR_R_OFFSET,c4d.VECTOR_Y] = math.radians(180)
        #c[c4d.ID_CA_CONSTRAINT_TAG_PSR_R_OFFSET,c4d.VECTOR_Z] = math.radians(-90)

    if titus_root != None:
        fireMain_loc = c4d.BaseObject(c4d.Onull)
        fireMain_loc.SetName("fireMain_loc")
        doc.InsertObject(fireMain_loc)
        fireEyes_loc = c4d.BaseObject(c4d.Onull)
        fireEyes_loc.SetName("fireEyes_loc")
        doc.InsertObject(fireEyes_loc)
        c4d.EventAdd()

        fireMain = FindObjWithName(UnfoldRig(titus_root), "Spine3", objType=c4d.Ojoint, contains=True)
        fireEyes = FindObjWithName(UnfoldRig(titus_root), "PlaceFireFXHere", objType=c4d.Onull, contains=True)

        # Create constraint fireMain
        fireMain_loc.SetBit(c4d.BIT_ACTIVE)
        fireMain.SetBit(c4d.BIT_ACTIVE)
        c4d.CallCommand(1022414) # Add PSR Constraint
        DeselectAll()
        # Set constraint offset PSR
        c = fireMain.GetFirstTag()
        #c[c4d.ID_CA_CONSTRAINT_TAG_PSR_R_OFFSET,c4d.VECTOR_Y] = math.radians(-90)

        # Create constraint fireEyes
        fireEyes_loc.SetBit(c4d.BIT_ACTIVE)
        fireEyes.SetBit(c4d.BIT_ACTIVE)
        c4d.CallCommand(1022414) # Add PSR Constraint
        DeselectAll()
        # Set constraint offset PSR
        c = fireMain.GetFirstTag()
        #c[c4d.ID_CA_CONSTRAINT_TAG_PSR_R_OFFSET,c4d.VECTOR_Y] = math.radians(-90)
        #c[c4d.ID_CA_CONSTRAINT_TAG_PSR_R_OFFSET,c4d.VECTOR_Z] = math.radians(180)

    # Select for bake
    for muz_loc in muz_locs:
        muz_loc.SetBit(c4d.BIT_ACTIVE)

    fireMain_loc.SetBit(c4d.BIT_ACTIVE)
    fireEyes_loc.SetBit(c4d.BIT_ACTIVE)

    gui.MessageDialog("Now bake!")


def FindObjWithName(objList, objName, objType=None, removePrefixes=True, contains=False):
    """Searches an object list for the first object with a specific name"""
    prefixes = "_:"
    if not removePrefixes:
        prefixes = ""

    if contains:
        for obj in objList:
            if objName in RemoveAllPrefixes(obj.GetName(), prefixes) and (objType==None or obj.GetType()==objType):
                return obj
    else: # must be exact match
        for obj in objList:
            if objName == RemoveAllPrefixes(obj.GetName(), prefixes) and (objType==None or obj.GetType()==objType):
                return obj
    return None

def DeselectAll():
    objs = c4d.documents.GetActiveDocument().GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    for obj in objs:
        doc.AddUndo(c4d.UNDOTYPE_BITS, obj)
        obj.DelBit(c4d.BIT_ACTIVE)

def UnfoldRigs(roots):
    """Combined results of calling UnfoldRig() on each root"""
    combinedList = []

    try:
        for root in roots:
            break
    except:
        roots = [roots]

    for root in roots:
        combinedList += UnfoldRig(root)
    return combinedList
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

def RemoveAllPrefixes(name, delims="_:"):
    """Returns the last 'word' in a [delims]-separated string.
    Ex. RemoveAllPrefixes('DEF_New.RightArm', '._') returns 'RightArm'"""
    bareName = ""
    for char in reversed(name):
        if char in delims:
            break
        bareName = char + bareName
    return bareName

if __name__=='__main__':
    main()