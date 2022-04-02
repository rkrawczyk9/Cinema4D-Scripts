"""Constrains the components of the selected receiver rig to the other selected (driver) rigs' components."""
"""Adds a constraint tag to every child (aka rig component) of the selected root object named
    'Receiver Rig'. The targets of these PSR constraint tags will be the corresponding
    objects within the other selected root objects, based on hierarchical position.
    Essentially you end up with a Character Solver setup, except it's made out of individual
    constraint tags so it's more controllable.

    How to use this script:
    - select 2 or more roots of joint skeletons
    - the rig to be driven must be named 'Receiver Rig'
        (the other rigs don't need to follow the same naming convention at all)
    - the other rigs (the driver rigs) have to follow exactly the same hierarchical order of objects
        (i.e. neck joint is before shoulder joint in object manager)"""

"""Behavior of multiple PSR constraints: new transform value is just the average of the target transform values"""

import c4d
from c4d import gui

def main():
    # For test scene only:
    """doc.SearchObject("Receiver Rig").SetBit(c4d.BIT_ACTIVE)
    doc.GetActiveObject()
    doc.SearchObject("root1").SetBit(c4d.BIT_ACTIVE)
    doc.GetActiveObject()
    doc.SearchObject("root2").SetBit(c4d.BIT_ACTIVE)
    doc.GetActiveObject()
    doc.SearchObject("root3").SetBit(c4d.BIT_ACTIVE)
    doc.GetActiveObject()"""
    #uncomment the above lines to auto select the rigs in 'receiver rig script test.c4d'

    print("constrain_recv_rig.py started")

    recvrig = []
    drivrigs = []

    ctrlobjname = "Driver Rigs Weight Controls"
    if doc.GetFirstObject().GetName() == ctrlobjname:
        doc.GetFirstObject().Remove()
        print("removed old control object")
    # Unfold provided rig roots
    for o in doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER):
        if o.GetName() == "Receiver Rig":
            recvrig.append(o)
            recvrig = UnfoldRig(o.GetDown(), recvrig)
        else:
            newdrivrig = [o]
            newdrivrig = UnfoldRig(o.GetDown(), newdrivrig)
            drivrigs.append(newdrivrig)
    if recvrig == []:
        gui.MessageDialog('Select the receiver rig (must be named "Receiver Rig") and at least one driver rig.\nThey must all have the same joint hierarchy.')
        return

    gui.MessageDialog('Running script to constrain receiver rig to driver rigs')

    # Print rig components
    print("Receiver Rig components:")
    PrintObjListNames(recvrig, "- ")
    for i in range(0, len(drivrigs)):
        print("Driver Rig " + str(i+1) + " components:")
        PrintObjListNames(drivrigs[i], "- ")

    doc.StartUndo()
    # Deselect all
    recvrig[0].DelBit(c4d.BIT_ACTIVE)
    for drivrig in drivrigs:
        drivrig[0].DelBit(c4d.BIT_ACTIVE)

    ctagname = "Component Constraint: "
    if recvrig[0].GetFirstTag() != None:
        if recvrig[0].GetFirstTag().GetName() == ctagname+"Receiver Rig":
            for c in recvrig:
                for t in c.GetTags():
                    t.Remove()
            print("removed old component constraints")

    # Constrain
    for i in range(0,len(recvrig)):
        # Create rotation-only PSR constraint tag
        # Workaround to create a PSR constraint tag. Constraint tags are not naturally supported in Python SDK
        #    but there is a CallCommand to do it. So here I create two dummy objects to make the tag on, then the
        #    tag can be copied (via InsertTag()) onto other objects. I have to do it this way because the PSR tag's
        #    P(osition) option must be unchecked before applying it to the objects or else the receiver object
        #    will immediately move to the driver object's position, and that's not what we want. There could be
        #    other ways of preventing that, such as maybe adding a protection tag first, then deleting it.
        tempDriv = c4d.BaseObject(c4d.Ocube) # Temporary object
        tempRecv = c4d.BaseObject(c4d.Ocube)
        tempDriv.SetName("tempDriv")
        tempRecv.SetName("tempRecv")
        doc.InsertObject(tempDriv)
        doc.InsertObject(tempRecv)
        doc.GetActiveObject() #need to call this after every new selection because it forces selection order to save
        tempDriv.SetBit(c4d.BIT_ACTIVE)
        doc.GetActiveObject() #need to call this after every new selection because it forces selection order to save
        tempRecv.SetBit(c4d.BIT_ACTIVE)
        doc.GetActiveObject() #need to call this after every new selection because it forces selection order to save
        c4d.CallCommand(100004788, 50048) #creates constraint tags on selected objects
        myconstraint = tempRecv.GetTags()[0]
        tempRecv.Remove()
        tempDriv.Remove()
        
        myconstraint[c4d.ID_CA_CONSTRAINT_TAG_PSR] = True # Set to PSR constraint tag
        myconstraint[c4d.ID_CA_CONSTRAINT_TAG_LOCAL_R] = True #Check 'Local R'
        myconstraint[10005] = False # Uncheck 'P'(osition)
        myconstraint[10006] = False # Uncheck 'S'(cale) (off by default)
        myconstraint[10007] = True # Check 'R'(otation) (on by default)

        for drivrig in drivrigs:
            myconstraint[10001] = drivrig[i]                      # Set Target to the driver rig component
            myconstraint.SetName(ctagname + recvrig[i].GetName()) # Change tag name
            recvrig[i].InsertTag(myconstraint)                    # Put the tag on the object

        # Notes on dealing with constraints in python
        #c4d.CallCommand(100004788, 50048) #creates constraint tags on selected objects
        #tag()[c4d.ID_CA_CONSTRAINT_TAG_PSR] = True #sets to PSR

        # My failed attempt to do it without callcommand:
        #recvrig[i].MakeTag(c4d.Tcaconstraint)
        # note about MakeTag(): second param is tag to add after



    #CreateWeightControlObj(recvrig, drivrigs, ctrlobjname)






    doc.EndUndo()


def UnfoldRig(root, objlist):
    """Recursive function that, given an empy list, returns a list of all objects on the
        same or deeper hierarchical level as the given 'root' object."""
    objlist.append(root)

    if root.GetDown() != None:
        objlist = UnfoldRig(root.GetDown(), objlist)

    if root.GetNext() != None:
        objlist = UnfoldRig(root.GetNext(), objlist)

    return objlist


def CreateWeightControlObj(recvrig, drivrigs, ctrlobjname):
    null = c4d.BaseObject(c4d.Onull)
    null.SetName(ctrlobjname)
    doc.InsertObject(null)

    xtagname = "Weight Controls Xpresso"
    if null.GetFirstTag() != None:
        if null.GetFirstTag().GetName() == xtagname:
            null.GetFirstTag().Remove()
            print("removed old xpresso tag")

    # Set up the Xpresso tag
    xtag = c4d.BaseTag(c4d.Texpresso) # lol I'm assuming this is supposed to be Xpresso
    xtag.SetName(xtagname)
    null.InsertTag(xtag)
    nodemaster = xtag.GetNodeMaster()

    xgroupname = "Constraint Controls"
    #if nodemaster.SearchNode(xgroupname) != None: remove
    #    Create Xgroup
    xgroup = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_GV_OPERATOR_GROUP)
    xgroup.SetName(xgroupname)
    #    Create node for this null
    n_thisobj = nodemaster.CreateNode(xgroup, c4d.ID_OPERATOR_OBJECT)

    # Setting up the User Data
    p_weights = []
    p_compsInfluences = []
    for i in range(0,len(drivrigs)):

        # Creating the User Data

        #    Group
        group = CreateUserDataGroup(null, "Driver Rig "+str(i+1)+"", None, 1)
        #    Main Constraint Weight
        CreateUserDataFloat(null, "Constraint Weight", 1, group, c4d.DESC_UNIT_PERCENT, c4d.CUSTOMGUI_REALSLIDER, 0, 1, .01, True)
        #    Separator
        group = CreateUserDataGroup(null, "Influence on Components", group, 2)
        #    Component influences
        for c in recvrig:
            CreateUserDataFloat(null, c.GetName(), 1, group)


        # Adding the User Datas as Xpresso ports

        #    I'm surprised I actually did the numbers right on this
        current_userdata_number = 1+ i*(3+len(recvrig))
        #    Skip the group
        current_userdata_number += 1
        #    Main weight port
        p_weights.append(n_thisobj.AddPort(c4d.GV_PORT_OUTPUT, c4d.DescID(c4d.DescLevel(c4d.ID_USERDATA, c4d.DTYPE_SUBCONTAINER), c4d.DescLevel(current_userdata_number))))
        #    Skip the separator
        current_userdata_number += 1
        #    Component influence ports
        templist = []
        for c in range(0,len(recvrig)):
            current_userdata_number += 1
            templist.append(n_thisobj.AddPort(c4d.GV_PORT_OUTPUT, c4d.DescID(c4d.DescLevel(c4d.ID_USERDATA, c4d.DTYPE_SUBCONTAINER), c4d.DescLevel(current_userdata_number))))
        p_compsInfluences.append(templist)


        # Adding the Constraint tags as Xpresso nodes with Weight ports
        for c in range(0,len(recvrig)):
            obj_thistag = recvrig[c].GetTags()[0]
            #    Create object node and link to this tag
            n_thistag = nodemaster.CreateNode(xgroup, c4d.ID_OPERATOR_OBJECT)
            n_thistag[c4d.GV_OBJECT_OBJECT_ID] = obj_thistag




            #    Create Weight port
            #--------------------------------------------------------------------------------------------------------------------
            #p_thisport = n_thistag.AddPort(c4d.GV_PORT_INPUT, c4d.ID_CA_CONSTRAINT_TAG_PSR_WEIGHT)
            #--------------------------------------------------------------------------------------------------------------------
            # This is the problem line; what symbol can I use to make Weight ports that actually correspond to multiple driver rigs?
            #    c4d.ID_CA_CONSTRAINT_TAG_PSR_WEIGHT makes a Weight port but it doesn't drive anything in the attribute manager
            #    >:(



            #    Create multiplication node
            n_multip = nodemaster.CreateNode(xgroup, c4d.ID_OPERATOR_MATH)
            n_multip[c4d.GV_MATH_FUNCTION_ID] = c4d.GV_MUL_NODE_FUNCTION
            n_multip.SetName("Multiply: "+recvrig[c].GetName()+" of Rig "+str(i+1))

            #    Connect Userdata to multiplication node's' inputs, and multiplication node's' output to this constraint tag's Weight input
            p_weights[i].Connect(n_multip.GetInPorts()[0])
            p_compsInfluences[i][c].Connect(n_multip.GetInPorts()[1])
            #n_multip.GetOutPorts()[0].Connect(p_thisport)

            #Note: obj_thistag[10002/10012]=.50 is how you would change the Weight value in python


    # Finalize
    c4d.EventAdd()


# User Data functions mostly from Cineversitys:
def CreateUserDataFloat(obj, name, val=1, parentGroup=None, unit=c4d.DESC_UNIT_PERCENT, gui=c4d.CUSTOMGUI_REALSLIDER, smin=0, smax=1, sstep=.01, newline=False):
    #default is a percent slider
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_REAL)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_DEFAULT] = val
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_ON
    bc[c4d.DESC_UNIT] = unit
    bc[c4d.DESC_CUSTOMGUI] = gui
    bc[c4d.DESC_MINSLIDER] = smin
    bc[c4d.DESC_MAXSLIDER] = smax
    bc[c4d.DESC_STEP] = sstep
    bc[c4d.DESC_NEWLINE] = newline
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup

    element = obj.AddUserData(bc)
    obj[element] = val
    return element

def CreateUserDataGroup(obj, name, parentGroup=None, columns=None, shortname=None):
    if obj is None: return False
    if shortname is None: shortname = name
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_GROUP)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = shortname
    bc[c4d.DESC_TITLEBAR] = 1
    bc[c4d.DESC_NEWLINE] = True
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    if columns is not None:
        #DESC_COLUMNS VALUE IS WRONG IN 15.057 - SHOULD BE 22
        bc[22] = columns

    return obj.AddUserData(bc)

def CreateUserDataSeparator(obj, name, parentGroup=None):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_SEPARATOR)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_SEPARATOR
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup

    return obj.AddUserData(bc)

#Printer
def PrintObjListNames(objlist, prefix=""):
    for o in objlist:
        print(prefix + o.GetName())

# Execute main()
if __name__=='__main__':
    main()