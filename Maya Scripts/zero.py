import maya.cmds



def main():
    """
	Zeroes the rotation of the selected objects.

	**Author:**

		Robert Krawczyk, robert.krawczyk@dsvolition.com, 6/27/2022
		
    **Todo:**
    
        Create UI window to run this instead of hardcoding.
        
	"""
    

    setAttrs(maya.cmds.ls(selection=True), ("rotate",), dims = ("X","Y","Z"))


def setAttrs(objs, attrs = ("translate", "rotate", "scale"), dims = ("X","Y","Z"), value = 0):
    """
	Sets the specified attributes of each object to the specified value.

	**Arguments:**

		:``objs``:	`string tuple` The objects whose attributes will be set.

	**Keyword Arguments:**

		:``attrs``:	`string tuple` Tuple of attribute names to set.
		:``dims`` :	`string tuple` Tuple of dimensions to set. Ex. ("X","Y","Z")
		:``value``:	`float`        Value to set each attribute to.

	**Examples:** ::

		setAttrs(maya.cmds.ls(selection=True), ("translate", "rotate"), dims = ("X","Y","Z"))

	**Author:**

		Robert Krawczyk, robert.krawczyk@dsvolition.com, 6/27/2022
	"""
    
    
    for obj in objs:
        for attr in attrs:
            for dim in dims: # dimensions
                
                try:
                    maya.cmds.setAttr("{}.{}{}".format(obj, attr, dim), 0)
                    
                except RuntimeError as re:
                    if "is locked or connected" in str(re):
                        # Skip this dimension
                        continue
                    else:
                        raise RuntimeError(re)
                    
                    
        
if __name__ == '__main__':
    main()
