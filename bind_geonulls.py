import c4d
from c4d import gui

REPLACE = True # True for replacing any existing Skins/Weight tags on the geonulls
USING_GUI = False # Unessential GUI but may be nice if you're not reading the Console or script

def main():
    if len(doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)) == 0:
        doc.SearchObject("SEG GEO").SetBit(c4d.BIT_ACTIVE)
        doc.GetActiveObject()
        doc.SearchObject("Titus Mechanics Rig v3.3 T").SetBit(c4d.BIT_ACTIVE)
        doc.GetActiveObject()

    print("constrain_geonulls_5.py started")

    try:
        georoot, rigroot = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    except:
        gui.MessageDialog("Deselect all, select SEG GEO, then select Titus Mechanics Skeleton, then Execute this")
        return
    # Unfold provided rig roots
    geonulls = georoot.GetChildren() # Get children, but not grandchildren
    skips = 1 # Hardcoded to skip the starting null (which should be "GEO")
    #print("Skipping the first " + str(skips) + " object(s). Verify that this is correct.")
    rig = UnfoldRig(rigroot)[skips:]

    doc.StartUndo()
    # Deselect
    georoot.DelBit(c4d.BIT_ACTIVE)
    rigroot.DelBit(c4d.BIT_ACTIVE)

    weight_name = "Geonull Weight"

    for geonull in geonulls:
        alreadyBound = False
        for obj in UnfoldRig(geonull)[1:]:
            if obj.GetType() == c4d.Oskin: # If the object is a Skin
                if REPLACE:
                    doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, obj)
                    obj.Remove()
                    continue
                else:
                    alreadyBound = True
                    break
            else:
                for tag in obj.GetTags():
                    if tag.GetType() == c4d.Tweights:
                        if REPLACE:
                            doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, tag)
                            tag.Remove()
        if alreadyBound and not REPLACE:
            continue # Skip this geonull

        # Search driver hierarchy for joint name matching geo null. This is the joint we constrain to.
        found = False
        for obj in rig:
            #print("Checking " + obj.GetName()[-len(geonull.GetName()):])
            if obj.GetName()[-len(geonull.GetName()):] == geonull.GetName(): # If last part of joint name matches whole geonull name
                joint = obj
                found = True
                break
        if not found:
            print("Didn't find a corresponding joint for GEO Null: " + geonull.GetName() + ". Skipping..")
            continue
        # Now we can safely use the variable 'joint'

        print("- " + RemoveAllPrefixes(geonull.GetName()) + ": Binding ", end="")

        # Select bindees (geo objects being bound to the joint)
        bindees = []
        for obj in UnfoldRig(geonull)[1:]:
            if obj.GetType() in (c4d.Opolygon, c4d.Osphere, c4d.Ocylinder, c4d.Otube):
                bindees.append(obj)
                obj.SetBit(c4d.BIT_ACTIVE)
                c4d.CallCommand(12236) # Make Editable
                print(RemoveAllPrefixes(obj.GetName()),end=", ")
        # Select joint
        joint.SetBit(c4d.BIT_ACTIVE)
        print("to " + RemoveAllPrefixes(joint.GetName()))

        # Bind
        c4d.CallCommand(1019881) # Bind

        # Do stuff to bindees
        for bindee in bindees:
            bindee.DelBit(c4d.BIT_ACTIVE) # Deselect each bindee
            weightTag = bindee.GetFirstTag()
            weightTag.SetName(weight_name) # Rename each weight tag

            # Tried manually setting the weight of each point in the geo, but this doesn't do anything
            """
            # Make every point 100% bound to the joint
            jointID = 0 # First (and only) joint that the bindee is bound to
            new_weight = 1 # 100% weight
            print("  (setting points 0-" + str(bindee.GetPointCount()) + " to weight 100%)")
            doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, weightTag)
            for pointID in range(bindee.GetPointCount()):
                weightTag.SetWeight(jointID, pointID, new_weight) # Set the weight of every point to 100%
            """

        # Deselect joint
        joint.DelBit(c4d.BIT_ACTIVE)


    print("bind_geonulls.py done!")

    # Reselect roots
    georoot.DelBit(c4d.BIT_ACTIVE)
    rigroot.DelBit(c4d.BIT_ACTIVE)
    # Finish up
    doc.EndUndo() # TODO AddUndo's
    c4d.EventAdd()
    return #endmain


# Utilities

def GetGlobalPos(obj):
    return obj.GetMg().off

def GetTotalRot(obj):
    trot = obj.GetAbsRot()
    curr_ancestor = obj.GetUp()
    while curr_ancestor != None:
        trot += curr_ancestor.GetAbsPos()
        curr_ancestor = curr_ancestor.GetUp()
    return trot

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

def vec2str(vec, length=3, delim=", ", trim=10):
    """Vector to String. Works on c4d.Vector"""
    vec_str = "("
    for i in range(length):
        vec_str += str(vec[i])[:trim] + delim
    vec_str = vec_str[:-2] + ")"
    return vec_str

def PrintObjListNames(objlist, prefix=""):
    for o in objlist:
        print(prefix + o.GetName())

def RemoveAllPrefixes(name, delims="_"):
    """Returns the last 'word' in a [delims]-separated string.
    Ex. RemoveAllPrefixes('DEF_New.RightArm', '._') returns 'RightArm'"""
    bareName = ""
    for char in reversed(name):
        if char in delims:
            break
        bareName = char + bareName
    return bareName

# Execute main()
if __name__=='__main__':
    main()