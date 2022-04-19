import c4d
from c4d import gui

SELECT_CHILDREN_AFTER = True

def main():
    # Take selected objects
    try:
        srcRoot, hpRoot = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    except:
        gui.MessageDialog("First selected = source's deformation/mechanics Root\nSecond selected = highpoly rig's main null")
        return

    # Find roots
    srcSkelRoot = FindObjWithName(UnfoldRig(srcRoot), "Root", objType=c4d.Onull)

    # Find the null with the userdata we need to set
    plugger = FindObjWithName(UnfoldRig(hpRoot), "Plug ", contains=True)
    if plugger == None:
        gui.MessageDialog("No 'Plug In Source Here' object found in first selected descendents")
        return

    # Variables to navigate the userdata (ud)
    char = -1 # 1:Titus, 2:Colt/Merc
    udId_to_objName = []

    # See if this is Titus or Colt/Merc
    if "Titus" in hpRoot.GetName():
        char = 1
        udId_to_objName = [(5,"Hips",False),(6,"Mace",False),(7,"CD Mech",True)]
    elif "Colt" in hpRoot.GetName() or "Merc" in hpRoot.GetName():
        char = 2
        udId_to_objName = [(2,"Hips",False),(3,"Gun",False),(5,"CD Def",True)]

    # Rename HP main null for convenience
    doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, hpRoot) # Undo
    hpRoot.SetName( hpRoot.GetName() + ": <" + srcRoot.GetName() + ">" )
    doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, hpRoot.GetDown().GetNext()) # Undo
    hpRoot.GetDown().GetNext().SetName( hpRoot.GetDown().GetNext().GetName() + " (" + srcRoot.GetName() + ")" )

    # Set plugger's userdata with search result
    for udId, objName, isTag in udId_to_objName:
        value = None
        if not isTag:
            value =  FindObjWithName(UnfoldRig(srcSkelRoot), objName, objType=c4d.Ojoint)
        else:
            value = FindTagWithName(UnfoldRig(srcSkelRoot), objName, tagType=None) # None because c4d.Tchardefinition is not implemented in this version

        # Set the new value
        doc.AddUndo(c4d.UNDOTYPE_BITS, plugger) # Undo
        SetUserdata( plugger, udId, value, default=True )
        print("Set userdata " + str(udId) + " to " + value.GetName())

    DeselectAll()

    # We made big expression changes, the viewport needs to catch up
    c4d.EventAdd()
    c4d.EventAdd()
    c4d.EventAdd()

    if SELECT_CHILDREN_AFTER:
        # Find HP skeleton's root
        hpSkelRoot = FindObjWithName(UnfoldRig(hpRoot), "Root", objType=c4d.Onull)
        if hpSkelRoot == None:
            gui.MessageDialog("No 'Root' in selected highpoly rig")
            return
        else:
            # Select it
            doc.AddUndo(c4d.UNDOTYPE_BITS, hpSkelRoot) # Undo
            hpSkelRoot.SetBit(c4d.BIT_ACTIVE)

            c4d.CallCommand(100004768) # Select Children

            # Deselect it ('Bake Objects...' sometimes prefers not to have it selected)
            doc.AddUndo(c4d.UNDOTYPE_BITS, hpSkelRoot) # Undo
            hpSkelRoot.DelBit(c4d.BIT_ACTIVE)

    return


# Utility

def SetUserdata(obj, userdataId, value, default=False):
    """Sets the value of a specific userdata. I always forget how to do this so I made a function."""
    doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, obj) # Undo
    obj[c4d.ID_USERDATA,userdataId] = value

    if default:
        for descId, container in obj.GetUserDataContainer():
            if descId[1].id == userdataId:
                container[c4d.DESC_DEFAULT] = value
                doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, obj)
                obj.SetUserDataContainer(descId, container)

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

def FindTagWithName(objList, tagName, tagType=None, removePrefixes=True, contains=False):
    """Searches an object list for the first tag with a specific name"""
    prefixes = "_:"
    if not removePrefixes:
        prefixes = ""

    if contains:
        for obj in objList:
            for tag in obj.GetTags():
                if tagName in RemoveAllPrefixes(tag.GetName(), prefixes) and (tagType==None or tag.GetType()==tagType):
                    return tag
    else: # must be exact match
        for obj in objList:
            for tag in obj.GetTags():
                if tagName in RemoveAllPrefixes(tag.GetName(), prefixes) and (tagType==None or tag.GetType()==tagType):
                    return tag
    return None

def DeselectAll():
    objs = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    for obj in objs:
        doc.AddUndo(c4d.UNDOTYPE_BITS, obj)
        obj.DelBit(c4d.BIT_ACTIVE)

def RemoveAllPrefixes(name, delims="_:"):
    """Returns the last 'word' in a [delims]-separated string.
    Ex. RemoveAllPrefixes('DEF_New.RightArm', '._') returns 'RightArm'"""
    if delims == "":
        return name
    bareName = ""
    for char in reversed(name):
        if char in delims:
            break
        bareName = char + bareName
    return bareName

def UnfoldRig(root):
    """Returns an object and its descendents in a list."""
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

# Execute main()
if __name__=='__main__':
    main()