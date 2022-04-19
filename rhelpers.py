import c4d

PRINTING = True

def init():
    global TYPE_SPLINEWRAP
    global TYPE_MOTIONSOLVER
    global TYPE_CHARDEF
    global TYPE_POINTCACHE
    TYPE_SPLINEWRAP = 1019221
    TYPE_MOTIONSOLVER = 1055068
    TYPE_CHARDEF = 1054858
    TYPE_POINTCACHE = 1021302

def main():
    c4d.GePrint("Hey you're not supposed to run this, these are for other scripts to use")
    return

# General Helper Functions
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

def DeselectAll():
    objs = c4d.documents.GetActiveDocument().GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    for obj in objs:
        doc.AddUndo(c4d.UNDOTYPE_BITS, obj)
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

def SetUserdata(obj, userdataId, value, default=False):
    """Sets the value of a specific userdata. I always forget how to do this so I made a function."""
    doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, obj)
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
            if objName in rhelpers.RemoveAllPrefixes(obj.GetName(), prefixes) and (objType==None or obj.GetType()==objType):
                return obj
    else: # must be exact match
        for obj in objList:
            if objName == rhelpers.RemoveAllPrefixes(obj.GetName(), prefixes) and (objType==None or obj.GetType()==objType):
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
                if tagName in rhelpers.RemoveAllPrefixes(tag.GetName(), prefixes) and (tagType==None or tag.GetType()==tagType):
                    return tag
    else: # must be exact match
        for obj in objList:
            for tag in obj.GetTags():
                if tagName in rhelpers.RemoveAllPrefixes(tag.GetName(), prefixes) and (tagType==None or tag.GetType()==tagType):
                    return tag
    return None

def RemoveAllPrefixes(name, delims="_:"):
    """Returns the last 'word' in a [delims]-separated string.
    Ex. RemoveAllPrefixes('DEF_New.RightArm', '._') returns 'RightArm'"""
    bareName = ""
    for char in reversed(name):
        if char in delims:
            break
        bareName = char + bareName
    return bareName

def GetFirstAncestor(obj):
    firstAncestor = obj
    while firstAncestor is not None:
        firstAncestor = firstAncestor.GetUp()
    return firstAncestor

def DeleteTags(root):
    """Deletes all tags on descendents"""
    doc = c4d.documents.GetActiveDocument()
    if PRINTING:
        c4d.GePrint("Running delete_tags")

    for obj in rhelpers.UnfoldRigs( root ):
        for tag in obj.GetTags():
            if PRINTING:
                c4d.GePrint("- deleting " + tag.GetName())
            doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, tag)
            tag.Remove()

    if PRINTING:
        c4d.GePrint("delete_tags done\n")
    return

def DeleteEmpties(roots):
    """Deletes all descendent empty nulls and splines, helper sites, and bounding boxes"""
    doc = c4d.documents.GetActiveDocument()
    if PRINTING:
        c4d.GePrint("Running delete_empties")

    for obj in reversed( rhelpers.UnfoldRigs( roots ) ):
        # Starting with deepest descendents (to catch nulls with only empty nulls for children,)
        # Delete empty nulls
        if obj.GetType() in (c4d.Onull, c4d.Ospline) and obj.GetDown() == None:
            deleteIt(obj)
        # Delete helper sites
        elif obj.GetType()==c4d.Ojoint and "helpersite" in obj.GetName().lower():
            rhelpers.deleteIt(obj)
        # Delete bounding boxes
        elif obj.GetType()!=c4d.Ojoint and rhelpers.RemoveAllPrefixes(obj.GetName()).lower()=="bounds":
            rhelpers.deleteIt(obj)

    if PRINTING:
        c4d.GePrint("delete_empties done\n")
    return
def deleteIt(obj):
    if PRINTING:
        c4d.GePrint("- deleting " + obj.GetName())
    c4d.documents.GetActiveDocument().AddUndo(c4d.UNDOTYPE_DELETEOBJ, obj)
    obj.Remove()


# Conversions

def ObjList2String(objlist, prefix="", delim=", ", trim=0):
    string = ""
    for o in objlist:
        string += prefix + o.GetName()[trim:] + delim
    string = string[:-len(delim)] #  Chop off last delim
    return string

def PrintBigString(bigString, chunk=80):
    doc = c4d.documents.GetActiveDocument()
    for i in range(0, len(bigString), chunk):
        c4d.GePrint(bigString[ i : min(i+chunk, len(bigString)) ],end="")
    c4d.GePrint()
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
        pyList.append(inexcludeList.ObjectFromIndex(doc,i))
    return pyList