import c4d
from c4d import gui

USING_GUI = False # Unessential GUI but may be nice if you're not reading the Console or script
USING_MY_UNDO = False # At the end it asks if you want to undo this, tbh just save a copy of GEO instead

"""
DIRECTIONS = {
    "X+":,
    "X-":,
    "Y+":,
    "Y-":,
    "Z+":,
    "Z-":
    }

HIK_ALIGNMENTS = {
    "Hips":
    "RightUpLeg":
    "RightLeg":
    "RightFoot":
    "Site":
    "LeftUpLeg":
    "LeftLeg":
	"LeftFoot":
	"Site":
	"Spine":
	"Spine1":
	"Spine2":
	"Spine3":
	"Neck":
	"Head":
	"Site":
	"RightShoulder":
	"RightArm":
	"RightForeArm":
	"RightHand":
	"RightHandThumb1":
	"RightHandThumb2":
	"RightHandThumb3":
	"Site":
	"RightInHandIndex":
	"RightHandIndex1":
	"RightHandIndex2":
	"RightHandIndex3":
	"Site":
	"RightInHandMiddle":
	"RightHandMiddle1":
	"RightHandMiddle2":
	"RightHandMiddle3":
	"Site":
	"RightInHandRing":
	"RightHandRing1":
	"RightHandRing2":
	"RightHandRing3":
	"Site":
	"RightInHandPinky":
	"RightHandPinky1":
	"RightHandPinky2":
	"RightHandPinky3":
	"Site":
	"LeftShoulder":
	"LeftArm":
	"LeftForeArm":
	"LeftHand":
	"LeftHandThumb1":
	"LeftHandThumb2":
	"LeftHandThumb3":
	"Site":
	"LeftInHandIndex":
	"LeftHandIndex1":
	"LeftHandIndex2":
	"LeftHandIndex3":
	"Site":
	"LeftInHandMiddle":
	"LeftHandMiddle1":
	"LeftHandMiddle2":
	"LeftHandMiddle3":
	"Site":
	"LeftInHandRing":
	"LeftHandRing1":
	"LeftHandRing2":
	"LeftHandRing3":
	"Site":
	"LeftInHandPinky":
	"LeftHandPinky1":
	"LeftHandPinky2":
	"LeftHandPinky3":
	"Site":
    }
"""

def main():
    if len(doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)) == 0:
        doc.SearchObject("SEG_GEO").SetBit(c4d.BIT_ACTIVE)
        doc.GetActiveObject()
        doc.SearchObject("Titus Mechanics Skeleton").SetBit(c4d.BIT_ACTIVE)
        doc.GetActiveObject()

    print("constrain_geonulls_5.py started")

    try:
        georoot, rigroot = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    except:
        gui.MessageDialog("Deselect all, select GEO, then select Titus Mechanics Skeleton, then Execute this")
        return
    # Unfold provided rig roots
    geonulls = georoot.GetChildren() # Get children, but not grandchildren
    skips = 1 # Hardcoded to skip the starting null (which should be "GEO")
    print("Skipping the first " + str(skips) + "object(s). Verify that this is correct.")
    rig = UnfoldRig(rigroot)[skips:]

    doc.StartUndo()
    # Deselect
    georoot.DelBit(c4d.BIT_ACTIVE)
    rigroot.DelBit(c4d.BIT_ACTIVE)

    xtagname = "Drive GeoNulls Xpresso"
    for tag in georoot.GetTags(): # Remove old Xpresso tag(s)
        if tag.GetName() == xtagname:
            tag.Remove()
            print("removed old xpresso tag")

    """
    aimc_name = "Geonull Aim: "
    for geonull in geonulls: # Remove old aim constraint(s)
        for tag in geonull.GetTags():
            if tag.GetName()[:len(aimc_name)] == aimc_name:
                tag.Remove()
    """

    psrc_name = "Geonull PSR: "
    for geonull in geonulls: # Remove old PSR constraint(s)
        for tag in geonull.GetTags():
            if tag.GetName()[:len(psrc_name)] == psrc_name:
                tag.Remove()

    #### XPRESSO START #####

    # Set up the Xpresso tag
    xtag = c4d.BaseTag(c4d.Texpresso) # lol I'm assuming this is supposed to be Xpresso
    xtag.SetName(xtagname)
    georoot.InsertTag(xtag)
    nodemaster = xtag.GetNodeMaster()

    xgroupname = "Drive GeoNulls"
    #if nodemaster.SearchNode(xgroupname) != None: remove
    #    Create Xgroup
    #xgroup = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_GV_OPERATOR_GROUP)
    xgroup = nodemaster.GetRoot()
    xgroup.SetName(xgroupname)
    #    Create node for GEO, if we needed to get UserData from it or something
    #n_thisobj = nodemaster.CreateNode(xgroup, c4d.ID_OPERATOR_OBJECT)

    geonulls_psr = []

    nodeposx_left = 560
    nodeposx_right = 400
    nodeposy_rowheight = 100
    nodeposy_curr = 0
    ##### XPRESSO BREAK ####
    for geonull in geonulls:
        # Before we change the positions, save the original positions so the user can undo
        geonulls_psr.append( (geonull.GetRelPos(), geonull.GetRelScale(), geonull.GetRelRot()) )

        # Search driver hierarchy for joint name matching geo null. This is the joint we constrain to.
        found = False
        for obj in rig:
            #print("Checking " + obj.GetName()[-len(geonull.GetName()):])
            if obj.GetName()[-len(geonull.GetName()):] == geonull.GetName():
                joint = obj
                found = True
                break
        if not found:
            print("Didn't find a corresponding joint for GEO Null: " + geonull.GetName() + ". Skipping..")
            continue

        # Find site (joint's child)
        site = joint.GetDown() # Assumes the first child is a valid site (aligned)
        for obj in joint.GetChildren():
            if obj.GetName()[-4:] == "Site": # If there's one actually named 'Site' then go with that one
                site = obj
                break
        # If no children
        if site == None:
            print("No child of joint: " + joint.GetName() + ". Skipping..")
            if USING_GUI:
                gui.MessageDialog(joint.GetName() + " does not have a child. All joints that want to have a geonull follow them must have a child joint (perhaps make a 'Site')")
            continue

        # Check Alignment
        nonzero_dimension_count = 0
        for i in range(3):
            if abs(site.GetRelPos()[i]) > 0.1: # Some tolerance
                nonzero_dimension_count += 1
        if nonzero_dimension_count > 1:
            print(site.GetName() + " not aligned. pos=" + vec2str(site.GetAbsPos(), trim=6) + " Maybe add an aligned Site.")
            if USING_GUI:
                gui.MessageDialog(site.GetName() + " not aligned. Maybe add a Site.")
            # continue # Used to skip joints that were not aligned but whatever


        # Move GEO nulls to joint's global position, but leave children behind (The equivalent of pressing L then moving the GEO null)
        new_gpos = GetGlobalPos( geonull )
        old_gpos = GetGlobalPos( joint )
        geonull.SetAbsPos(new_gpos) # aka add the difference
        for child in geonull.GetChildren():
            child.SetAbsPos( child.GetAbsPos() - (new_gpos-old_gpos) ) # aka subtract the difference

        ##### XPRESSO RESUME #######

        # Create Geonull node
        n_geonull = nodemaster.CreateNode(xgroup, c4d.ID_OPERATOR_OBJECT, x=nodeposx_left, y=nodeposy_curr)
        n_geonull[c4d.GV_OBJECT_OBJECT_ID] = geonull
        p_geonull_gpos = n_geonull.AddPort(c4d.GV_PORT_INPUT, c4d.ID_BASEOBJECT_GLOBAL_POSITION)
        #p_geonull_rot = n_geonull.AddPort(c4d.GV_PORT_INPUT, c4d.ID_BASEOBJECT_REL_ROTATION)
        p_geonull_scale = n_geonull.AddPort(c4d.GV_PORT_INPUT, c4d.ID_BASEOBJECT_REL_SCALE)
        p_geonull_vis = n_geonull.AddPort(c4d.GV_PORT_INPUT, c4d.ID_BASEOBJECT_VISIBILITY_EDITOR)

        # Create Joint node
        n_joint = nodemaster.CreateNode(xgroup, c4d.ID_OPERATOR_OBJECT, x=nodeposx_right, y=nodeposy_curr)
        n_joint[c4d.GV_OBJECT_OBJECT_ID] = joint
        p_joint_gpos = n_joint.AddPort(c4d.GV_PORT_OUTPUT, c4d.ID_BASEOBJECT_GLOBAL_POSITION)
        #p_joint_rot = n_joint.AddPort(c4d.GV_PORT_OUTPUT, c4d.ID_BASEOBJECT_REL_ROTATION)
        p_joint_scale = n_joint.AddPort(c4d.GV_PORT_OUTPUT, c4d.ID_BASEOBJECT_REL_SCALE)
        p_joint_vis = n_joint.AddPort(c4d.GV_PORT_OUTPUT, c4d.ID_BASEOBJECT_VISIBILITY_RENDER)

        # Connect the ports
        p_joint_gpos.Connect(p_geonull_gpos)
        #p_joint_rot.Connect(p_geonull_rot)
        p_joint_scale.Connect(p_geonull_scale)
        p_joint_vis.Connect(p_geonull_vis)

        nodeposy_curr += nodeposy_rowheight

        ##### XPRESSO END ####

        # I am no longer doing an aim constraint here, instead I am letting PSR handle all the rotation because aim constraint was failing with B
        """
        # Create Aim Constraint tag
        geonull.SetBit(c4d.BIT_ACTIVE)
        c4d.CallCommand(100004788, 50048) #creates constraint tag on selected object
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, geonull.GetFirstTag())
        geonull.DelBit(c4d.BIT_ACTIVE)
        aimc = geonull.GetFirstTag()
        if aimc == None:
            print("Failed to create aim constraint")
            return
        aimc.SetName(aimc_name)
        aimc[c4d.ID_CA_CONSTRAINT_TAG_AIM] = True # Check Aim (constraint type)
        aimc[c4d.ID_CA_CONSTRAINT_TAG_AIM_MAINTAIN] = True # Check Maintain Original (IMPORTANT - lets geonull stay where it started)
        aimc[20004] = 0 # Set Axis (X+:0 X-:3 Y+:1 Y-:4 Z+:2 Z-:5)
        aimc[c4d.ID_CA_CONSTRAINT_TAG_AIM_CONSTRAIN_X] = True
        aimc[c4d.ID_CA_CONSTRAINT_TAG_AIM_CONSTRAIN_Y] = True
        aimc[c4d.ID_CA_CONSTRAINT_TAG_AIM_CONSTRAIN_Z] = False # Not constraining B because aim constraints don't handle B well. I make the parent constraint for B
        aimc[20001] = site # Set aim Target to site (aka joint.GetDown())
        # This priority code is commented because not setting to the right thing:
        #priority = c4d.PriorityData()
        #priority.SetPriorityValue(c4d.CYCLE_EXPRESSION, 305) # 305 is the magic number for high priority according to Brent
        #aimc[c4d.EXPRESSION_PRIORITY] = priority # Set Expression Priority
        """

        # Create Parent Constraint for B
        geonull.SetBit(c4d.BIT_ACTIVE)
        c4d.CallCommand(100004788, 50048) #creates constraint tag on selected object
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, geonull.GetFirstTag())
        geonull.DelBit(c4d.BIT_ACTIVE)
        psrc = geonull.GetFirstTag() # PSR Constraint (PSRC)
        if psrc == None:
            print("Failed to create PSR constraint")
            return
        psrc.SetName(psrc_name)
        psrc[c4d.ID_CA_CONSTRAINT_TAG_PSR] = True # Make it a PSR constraint
        psrc[c4d.ID_CA_CONSTRAINT_TAG_PSR_MAINTAIN] = True # Check Maintain Original (IMPORTANT - lets geonull stay where it started)
        # Disabling all PSR except B
        psrc[c4d.ID_CA_CONSTRAINT_TAG_PSR_CONSTRAIN_P_X] = False # Only enable B
        psrc[c4d.ID_CA_CONSTRAINT_TAG_PSR_CONSTRAIN_P_Y] = False
        psrc[c4d.ID_CA_CONSTRAINT_TAG_PSR_CONSTRAIN_P_Z] = False
        psrc[c4d.ID_CA_CONSTRAINT_TAG_PSR_CONSTRAIN_S_X] = False
        psrc[c4d.ID_CA_CONSTRAINT_TAG_PSR_CONSTRAIN_S_Y] = False
        psrc[c4d.ID_CA_CONSTRAINT_TAG_PSR_CONSTRAIN_S_Z] = False
        psrc[c4d.ID_CA_CONSTRAINT_TAG_PSR_CONSTRAIN_R_X] = True
        psrc[c4d.ID_CA_CONSTRAINT_TAG_PSR_CONSTRAIN_R_Y] = True
        psrc[c4d.ID_CA_CONSTRAINT_TAG_PSR_CONSTRAIN_R_Z] = True
        psrc[10001] = joint # Set PSR target to the Joint
        # This priority code is commented because not setting to the right thing:
        #priority = c4d.PriorityData()
        #priority.SetPriorityValue(c4d.CYCLE_EXPRESSION, 305) # 305 is the magic number for high priority according to Brent
        #psrc[c4d.EXPRESSION_PRIORITY] = priority # Set Expression Priority

        #endfor

    print("constrain_geonulls.py done!")

    if USING_MY_UNDO:
        right = "default"
        while right not in ("yes", "no"):
            c4d.EventAdd() # TODO Force update viewport
            right = gui.InputDialog("Does this look right? Last chance to undo. (yes/no)")
        if right == "no":
            # Undo what we did and reset the geonulls' PSR (XPresso is not undoable by default)
            xtag.Remove()
            for geonull in geonulls: # Remove aim constraints
                for tag in geonull.GetTags():
                    if tag.GetName()[:len(aimc_name)] == aimc_name:
                        tag.Remove()
            c4d.EventAdd()
            for i in range(len(geonulls)):
                gn = geonulls[i]
                psr = geonulls_psr[i]
                gn.SetRelPos(psr[0])
                gn.SetRelScale(psr[1])
                gn.SetRelRot(psr[2])
            gui.MessageDialog("Undid everything")

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

# Execute main()
if __name__=='__main__':
    main()