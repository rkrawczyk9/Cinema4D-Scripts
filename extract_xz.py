import c4d
from c4d import gui

PRINTING = True

def main():
    if PRINTING:
        explanation =  'Extract XZ'
        explanation += '\n\nThis script transfers the X and Z animation from the Hips to a new null, to allow for better blending between motion clips.'
        explanation += '\nIt also centers the animation to the origin, at the currently active frame.\nYou have to bake it afterwards.'
        if not gui.QuestionDialog(explanation + '\n\nDo you want to run this?'):
            return
        else:
            gui.MessageDialog("Running part 1...")
    root_orig = doc.GetActiveObject()
    if root_orig == None:
        gui.MessageDialog("Select the skeleton's root that you want to extract from. (This script makes a copy")
        return
    # Deselect
    doc.AddUndo(c4d.UNDOTYPE_BITS, root_orig)
    root_orig.DelBit(c4d.BIT_ACTIVE)

    # Run
    if extract_xz( CopyAndShow(root_orig) ):
        if PRINTING:
            gui.MessageDialog("Successfully ran part 1.\nNow run Timeline > Functions > Bake Objects..., then run the highest version of extract_xz_pt2 to clean up the scene, and you're done.")
    return

def extract_xz(root):
    ## Starting up

    # Check root
    if root == None or root.GetDown() == None:
        gui.MessageDialog('Select the root null')
        return False

    doc.StartUndo()
    # Clean up previous runs
    if root.GetDown().GetName() == "Pos_Orig":
        # Move Hips to top
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, root.GetDown().GetDown())
        doc.InsertObject(root.GetDown().GetDown(), root)

        # Delete Pos_Orig
        doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, root.GetDown().GetNext())
        root.GetDown().GetNext().Remove()
        # Delete Hips_orig
        if root.GetDown().GetNext().GetName() == "Hips_orig":
            doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, root.GetDown().GetNext())
            root.GetDown().GetNext().Remove()

    # Find Hips
    if root.GetDown().GetName() != "Hips":
        gui.MessageDialog('Hips not found. Should be directly under root null')
        return False
    Hips = root.GetDown()

    ## Create Pos_Orig null
    # Deselect root
    doc.AddUndo(c4d.UNDOTYPE_BITS, Hips)
    root.DelBit(c4d.BIT_ACTIVE)

    # Select Hips
    doc.AddUndo(c4d.UNDOTYPE_BITS, Hips)
    Hips.SetBit(c4d.BIT_ACTIVE)

    # Convert Hips to new null (same PSR)
    c4d.CallCommand(1019941) # Convert to Null

    # Find the newly created Pos_Orig
    Pos_Orig = Hips.GetNext()
    if Pos_Orig.GetName() != "Hips":
        gui.MessageDialog('Dont put anything next to Hips')
        doc.EndUndo()
        return False
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, Pos_Orig)

    # Deselect Hips
    doc.AddUndo(c4d.UNDOTYPE_BITS, Hips)
    Hips.DelBit(c4d.BIT_ACTIVE)

    # Rename Pos_Orig
    doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, Pos_Orig)
    Pos_Orig.SetName("Pos_Orig")

    # Move Pos_Orig to outside of Hips
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, Pos_Orig)
    doc.InsertObject(Pos_Orig,parent=root)

    # Zero Pos_Orig's rotation and y position
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, Pos_Orig)
    Pos_Orig.SetRelRot(c4d.Vector(0))
    Pos_Orig.SetRelPos(c4d.Vector( Pos_Orig.GetRelPos()[0], 0, Pos_Orig.GetRelPos()[2] ))

    ## Create Hips_orig
    # Copy Hips to Hips_orig
    Hips_orig = Hips.GetClone()
    if Hips_orig == None:
        print('Failed to copy Hips')
        doc.EndUndo()
        return False
    doc.InsertObject(Hips_orig, parent=root)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, Hips_orig)

    # Rename Hips_orig
    doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, Hips_orig)
    Hips_orig.SetName("Hips_orig")

    # Delete Hips_orig children
    if Hips_orig.GetChildren() != None:
        for child in Hips_orig.GetChildren():
            doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, child)
            child.Remove()

    # Move Hips under Pos_Orig
    doc.InsertObject(Hips, parent=Pos_Orig)
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, Hips)

    # Move Pos_Orig to before Hips_orig
    doc.InsertObject(Pos_Orig, parent=root)
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, Pos_Orig)

    ######## XPRESSO START
    ## Create Xpresso Network
    # Set up the Xpresso tag
    xtagname = "Extract XZ Drive Tag"
    if Pos_Orig.GetFirstTag() != None:
        if Pos_Orig.GetFirstTag().GetName() == xtagname:
            doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, Pos_Orig.GetFirstTag())
            Pos_Orig.GetFirstTag().Remove()
    xtag = c4d.BaseTag(c4d.Texpresso) # lol I'm assuming this is supposed to be Xpresso
    xtag.SetName(xtagname)
    Pos_Orig.InsertTag(xtag)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, xtag)
    nodemaster = xtag.GetNodeMaster()

    xgroupname = "Extract XZ Xgroup"
    xgroup = nodemaster.GetRoot()
    xgroup.SetName(xgroupname)

    spacing = 200

    ## Driving Pos_Orig
    # Create Pos_Orig node
    n_Pos_Orig = nodemaster.CreateNode(xgroup, c4d.ID_OPERATOR_OBJECT, x=spacing*6, y=spacing*1)
    n_Pos_Orig[c4d.GV_OBJECT_OBJECT_ID] = Pos_Orig
    p_Pos_Orig_gpos = n_Pos_Orig.AddPort(c4d.GV_PORT_INPUT, c4d.ID_BASEOBJECT_GLOBAL_POSITION) # Can't find a way to get X,Y,Z separately. Resorting to Adapter nodes

    # Subtract offset from Pos_Orig position
    n_Offset = nodemaster.CreateNode(xgroup, c4d.ID_OPERATOR_MATH, x=spacing*5, y=spacing*1)
    n_Offset[c4d.GV_DYNAMIC_DATATYPE] = c4d.DTYPE_VECTOR ####### IMPORTANT, NOT IN DOCUMENTATION: Setting datatype of nodes
    n_Offset[c4d.GV_MATH_FUNCTION_ID] = c4d.GV_SUB_NODE_FUNCTION
    n_Offset.SetName("Offset")

    # Get starting position of Pos_Orig
    n_StartingPos = nodemaster.CreateNode(xgroup, c4d.ID_OPERATOR_CONST, x=spacing*4, y=spacing*1+100)
    n_StartingPos[c4d.GV_DYNAMIC_DATATYPE] = c4d.DTYPE_VECTOR ####### IMPORTANT, NOT IN DOCUMENTATION: Setting datatype of nodes
    doc.SetTime(c4d.BaseTime(0)) # Set to frame 0 to get offset from frame 0
    c4d.EventAdd()
    n_StartingPos[c4d.GV_CONST_VALUE] = GetGlobalPos(Pos_Orig)
    n_StartingPos.SetName("StartingPos")

    # Create Reals2Vector node 1
    n_r2v_1 = nodemaster.CreateNode(xgroup, c4d.ID_OPERATOR_REAL2VECT, x=spacing*3, y=spacing*1)
    n_r2v_1.SetName("r2v_1")

    # Create Vector2Reals node 1
    n_v2r_1 = nodemaster.CreateNode(xgroup, c4d.ID_OPERATOR_VECT2REAL, x=spacing*2, y=spacing*1)
    n_v2r_1.SetName("v2r_1")

    # Create Hips_orig node
    n_Hips_orig = nodemaster.CreateNode(xgroup, c4d.ID_OPERATOR_OBJECT, x=spacing*1, y=spacing*1)
    n_Hips_orig[c4d.GV_OBJECT_OBJECT_ID] = Hips_orig
    p_Hips_orig_gpos = n_Hips_orig.AddPort(c4d.GV_PORT_OUTPUT, c4d.ID_BASEOBJECT_GLOBAL_POSITION)

    ## Driving Hips
    # Create Hips node
    n_Hips = nodemaster.CreateNode(xgroup, c4d.ID_OPERATOR_OBJECT, x=spacing*4, y=spacing*2)
    n_Hips[c4d.GV_OBJECT_OBJECT_ID] = Hips
    p_Hips_pos = n_Hips.AddPort(c4d.GV_PORT_INPUT, c4d.ID_BASEOBJECT_POSITION)

    # Create Vector2Reals node 2
    n_v2r_2 = nodemaster.CreateNode(xgroup, c4d.ID_OPERATOR_VECT2REAL, x=spacing*2, y=spacing*2)
    n_v2r_2.SetName("v2r_2")

    # Create Reals2Vector node 2
    n_r2v_2 = nodemaster.CreateNode(xgroup, c4d.ID_OPERATOR_REAL2VECT, x=spacing*3, y=spacing*2)
    n_r2v_2.SetName("r2v_2")

    # Create Constant Zero node
    n_Zero = nodemaster.CreateNode(xgroup, c4d.ID_OPERATOR_CONST, x=spacing*1, y=spacing*2)
    n_Zero[c4d.GV_CONST_VALUE] = 0
    n_Zero.SetName("Zero")

    ## Connect
    # Group 1
    p_Pos_Orig_gpos.Connect(n_Offset.GetOutPort(0))

    n_Offset.GetInPort(0).Connect(n_r2v_1.GetOutPort(0))
    n_Offset.GetInPort(1).Connect(n_StartingPos.GetOutPort(0))

    n_r2v_1.GetInPort(0).Connect(n_v2r_1.GetOutPort(0))
    n_r2v_1.GetInPort(1).Connect(n_Zero.GetOutPort(0))
    n_r2v_1.GetInPort(2).Connect(n_v2r_1.GetOutPort(2))

    p_Hips_orig_gpos.Connect(n_v2r_1.GetInPort(0))

    # Group 2
    p_Hips_pos.Connect(n_r2v_2.GetOutPort(0))

    n_Zero.GetOutPort(0).Connect(n_r2v_2.GetInPort(0))

    p_Hips_orig_gpos.Connect(n_v2r_2.GetInPort(0))

    n_v2r_2.GetOutPort(1).Connect(n_r2v_2.GetInPort(1))
    n_Zero.GetOutPort(0).Connect(n_r2v_2.GetInPort(2))

    ###### XPRESSO END

    ## Bake Objects
    # Deselect root
    doc.AddUndo(c4d.UNDOTYPE_BITS, root)
    root.DelBit(c4d.BIT_ACTIVE)

    # Select Pos_Orig
    doc.AddUndo(c4d.UNDOTYPE_BITS, Pos_Orig)
    Pos_Orig.SetBit(c4d.BIT_ACTIVE)
    c4d.EventAdd()

    # Bake
    # Doesn't work the same for some reason. Resorting to user clicking it
    #c4d.CallCommand(465001219) # Bake Objects...

    # Rename root
    doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, root)
    root.SetName(root.GetName()[:-1-len(RemoveAllPrefixes(root.GetName(),"_ "))] + "_extractxz")

    ## Finishing up
    doc.EndUndo()
    c4d.EventAdd()
    return True
    #return extract_xz_pt2()

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

def RemoveAllPrefixes(name, delims="_"):
    """Returns the last 'word' in a [delims]-separated string.
    Ex. RemoveAllPrefixes('DEF_New.RightArm', '._') returns 'RightArm'"""
    bareName = ""
    for char in reversed(name):
        if char in delims:
            break
        bareName = char + bareName
    return bareName

def CopyAndShow(obj):
    doc.StartUndo()

    # Copy
    doc.InsertObject(obj.GetClone())
    newobj = doc.GetFirstObject()
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, newobj)

    # Show
    doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, newobj)
    newobj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 2

    doc.EndUndo()

    return newobj

def GetGlobalPos(obj):
    return obj.GetMg().off

# Execute main()
if __name__=='__main__':
    main()