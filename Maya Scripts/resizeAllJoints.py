import maya.cmds

def main():
    # Window
    choice = maya.cmds.promptDialog(title="Resize All Joints", message="Type a number or math expression", button=["Set all joints' radius to this", "Multiply all joints' radius by this", "Cancel"], defaultButton="Set all joints' radius to this", cancelButton="Cancel", dismissString="Cancel")
    
    if choice == "Cancel":
        return
    
    # The number/math the user typed
    inputNum = eval( maya.cmds.promptDialog(query=True, text=True) )
    
    # Set each
    if choice == "Set all joints' radius to this":
        for eachJoint in maya.cmds.ls(type="joint", long=True):
            maya.cmds.setAttr(eachJoint+".radius", inputNum)
            
    elif choice == "Multiply all joints' radius by this":
        for eachJoint in maya.cmds.ls(type="joint", long=True):
            prevRadius = maya.cmds.getAttr(eachJoint+".radius")
            maya.cmds.setAttr(eachJoint+".radius", prevRadius * inputNum)

main()