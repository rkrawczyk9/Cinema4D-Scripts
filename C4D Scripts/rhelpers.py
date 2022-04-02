import c4d

# General Helper Functions
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

def DeselectAll():
    objs = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    for obj in objs:
        obj.DelBit(c4d.BIT_ACTIVE)

def SearchForMatch(setter_obj, setee_objs):
    """Searches for a name match (ignoring all prefixes) within a list of objects"""
    setee_obj = None
    matchCount = 0
    for poss_setee_obj in setee_objs:
        if RemoveAllPrefixes( setter_obj.GetName() ) == RemoveAllPrefixes( poss_setee_obj.GetName() ):
            setee_obj = poss_setee_obj
            matchCount += 1
    return setee_obj, matchCount

# Helpers
def RemoveAllPrefixes(name, delims="_"):
    """Returns the last 'word' in a [delims]-separated string.
    Ex. RemoveAllPrefixes('DEF_New.RightArm', '._') returns 'RightArm'"""
    bareName = ""
    for char in reversed(name):
        if char in delims:
            break
        bareName = char + bareName
    return bareName

def ObjList2String(objlist, prefix="", delim=", ", trim=0):
    string = ""
    for o in objlist:
        string += prefix + o.GetName()[trim:] + delim
    string = string[:-len(delim)] #  Chop off last delim
    return string

def PrintBigString(bigString, chunk=80):
    for i in range(0, len(bigString), chunk):
        print(bigString[ i : min(i+chunk, len(bigString)) ],end="")
    print()
    return

def pyList2inexcludeList(pyList):
    """Converts a python List of c4d.BaseObjects to a c4d.InExcludeData"""
    inexcludeList = c4d.InExcludeData()
    for obj in pyList:
        inexcludeList.InsertObject(obj, 0)
    return inexcludeList

def inexcludeList2pyList(inexcludeList):
    """Converts an ObjectList / In/ExclusionList (c4d.InExcludeData) of c4d.BaseObjects to a """
    pyList = []
    for i in range(inexcludeList.GetObjectCount()):
        pyList.append(inexcludeList.ObjectFromIndex(i))
    return pyList