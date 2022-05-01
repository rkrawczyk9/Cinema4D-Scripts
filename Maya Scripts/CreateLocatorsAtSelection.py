import maya.cmds as cmd
def main():
    objs = cmd.ls(sl=True, long=True) # Long names in case of same name at same level
    objShortnames = cmd.ls(sl=True)
    
    # For loop through two corresponding lists
    for i in range(len(objs)):
        obj = objs[i]
        objShortname = objShortnames[i]
        
        # Get location and parent of each selected object
        pos = cmd.getAttr(obj+".translate")[0]
        rot = cmd.getAttr(obj+".rotate")[0]
        objParent = cmd.listRelatives(obj, parent=True)[0]
        
        # Create locator at origin
        locator = cmd.spaceLocator()[0]
        
        # Parent locator to object's parent, and set position and rotation
        cmd.parent(locator, objParent)
        cmd.setAttr(locator+".translate", pos[0], pos[1], pos[2])
        cmd.setAttr(locator+".rotate", rot[0], rot[1], rot[2])
        
        print("Created "+locator+" at location of "+obj)
        return
main()