import maya.cmds

def main():
    selectByName("pCube")

def selectByName(string):
    """Selects any children of selected objects whose name contains [string]"""
    # Get selection
    roots = maya.cmds.ls(orderedSelection=True, long=True)
    
    # Clear selection
    maya.cmds.select(clear=True)
    
    for rootName in roots:
        print(rootName)
        # Get children
        for objName in maya.cmds.listRelatives(rootName, allDescendents=True, fullPath=True):
            # Select if name contains string
            if string in lastToken(objName, '|'):
                maya.cmds.select(objName, add=True)

def lastToken(string, delim='|'):
    """Returns the last token in the string, tokens being divided by [delim]"""
    return string.split(delim)[-1]

main()