import maya.cmds as cmd
import pymel.core as pmc

def main():
    objs = cmd.ls(sl=True, long=True) # Long names in case of same name at same level
    objShortnames = cmd.ls(sl=True)
    
    # For loop through two corresponding lists
    for i in range(len(objs)):
        obj = objs[i]
        objShortname = objShortnames[i]
        
        # Get location and parent of each selected object
        pos = pmc.xform(obj, query=True, worldSpace=True, translation=True)
        rot = pmc.xform(obj, query=True, worldSpace=True, rotation=True)
        objParent = cmd.listRelatives(obj, parent=True)[0]
        
        # Create locator at origin
        locator = cmd.spaceLocator()[0]
        
        # Parent locator to object's parent, and set position and rotation
        cmd.parent(locator, objParent)
        pmc.xform(locator, worldSpace=True, translation=pos, rotation=rot)
        
        print("Created "+locator+" at location of "+objShortname)
    return
main()