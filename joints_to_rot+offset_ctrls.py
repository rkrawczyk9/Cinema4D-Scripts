import c4d
from c4d import gui

def main():
    print("\njoints_to_rot+offset_ctrls started...")

    offset_color = c4d.Vector(160,153,255) # Light indigo
    ctrl_color = c4d.Vector(97,255,175) # Light green
    offset_radius = 50 # Offset circle radius
    ctrl_radius = 80 # Control octagon radius

    for joint in doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN):
        # Check for existing nulls created by this script
        curr_parent = joint.GetUp()
        while curr_parent.GetName() not in ( "ctrl_"+joint.GetName(), "offset_"+joint.GetName() ):
            curr_parent = curr_parent.GetUp()
        parent_joint = curr_parent # rename
        first_null = parent_joint.GetDown()
        joint.InsertUnder(parent_joint)
        first_null.Remove()
        print("Removed old nulls made by this script")

        print("Doing " + joint.GetName())
        # CREATE CONTROL NULL
        null_ctrl = c4d.BaseObject(c4d.Onull) # Create null
        null_ctrl.SetName("ctrl_" + joint.GetName()) # Rename
        null_ctrl[c4d.NULLOBJECT_DISPLAY] = 8 # Set null to display as Octagon
        null_ctrl[c4d.NULLOBJECT_ORIENTATION] = 1 # Make octagon orient to Z axis
        null_ctrl[c4d.NULLOBJECT_RADIUS] = 80 # Set octagon radius
        null_ctrl[c4d.ID_BASEOBJECT_USECOLOR] = 2 # Enable Display Color
        null_ctrl[c4d.ID_BASEOBJECT_COLOR] = ctrl_color # Set color to light green
        # Match offset PSR to joint PSR
        null_ctrl.InsertUnder(joint) # Place under joint
        null_ctrl.SetRelPos(c4d.Vector(0)) # Zero position
        null_ctrl.SetRelScale(c4d.Vector(1)) # Zero scale
        null_ctrl.SetRelRot(c4d.Vector(0)) # Zero rotation
        null_ctrl.InsertUnder(joint.GetUp()) # Place control null as sibling to joint

        # CREATE OFFSET NULL
        null_offset = c4d.BaseObject(c4d.Onull) # Create null
        null_offset.SetName("offset_" + joint.GetName()) # Rename
        null_offset[c4d.NULLOBJECT_DISPLAY] = 2 # Set null to display as Circle
        null_offset[c4d.NULLOBJECT_ORIENTATION] = 1 # Make circle orient to Z axis
        null_offset[c4d.NULLOBJECT_RADIUS] = 50 # Set circle radius
        null_offset[c4d.ID_BASEOBJECT_USECOLOR] = 2 # Enable Display Color
        null_offset[c4d.ID_BASEOBJECT_COLOR] = offset_color # Set color to light indigo
        # Match offset PSR to joint PSR
        null_offset.InsertUnder(joint) # Place under joint
        null_offset.SetRelPos(c4d.Vector(0)) # Zero position
        null_offset.SetRelScale(c4d.Vector(1)) # Zero scale
        null_offset.SetRelRot(c4d.Vector(0)) # Zero rotation
        null_offset.InsertUnder(null_ctrl) # Insert offset null into scene

        # Move joint to be child of new nulls (TODO does this work?)
        joint.InsertUnder(null_offset)

if __name__=='__main__':
    main()