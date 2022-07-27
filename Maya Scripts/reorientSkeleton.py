import maya.cmds
import rhelpers
from rhelpers import Axis
import skelOrientation



def main():
	sel = maya.cmds.ls(selection=True, long=True)
	sel_hrc = sel + maya.cmds.listRelatives(sel, allDescendents=True, path=True)

	#TODO: Window

	reorientSkeleton(sel_hrc, skelOrientation.mixamo, skelOrientation.volition) # convert mixamo to volition


def reorientSkeleton(skeleton_list, curr_skel_orientation, desired_skel_orientation, delims=""):
	"""
	Rotates each joint (without affecting its children)
	Default axes are for converting mixamo skeleton to volition skeleton
	"""
	delims = "|:" + delims

	joints_to_reorient = []
	# Get the appropriate joints
	for obj in skeleton_list:
		obj_name = rhelpers.trim(obj, delims)
		# Could add other conditions here to determine whether an object should be reoriented
		if obj_name not in ("Hips") and maya.cmds.joint(obj, q=True, exists=True):
			# Store the joint with its parent in the list
			joints_to_reorient.append( (obj, obj.listRelatives(obj, parent=True, path=True)[0]) )


	children_to_preserve = []
	# Any non-joint children of the joints should not be affected
	for joint in joints_to_reorient:
		for child in maya.cmds.listRelatives(joint, children=True, path=True):
			if child not in joints_to_reorient:
				children_to_preserve.append((child, joint))



	# Unparent the joints to reorient, and the children to preserve
	for (obj, _) in joints_to_reorient + children_to_preserve:
		maya.cmds.parent(obj, world=True)


	# Rotato potato
	for (joint, _) in joints_to_reorient:
		rx = None
		ry = None
		rz = None

		# Could do some thinking here
		if curr_primary_axis == Axis.Ypos and desired_primary_axis == Axis.Xpos:
			rx = 0
			ry = 0
			rz = 0

		#joint_name = rhelpers.trim(joint, delims)

		maya.cmds.rotate(relative=True, euler=True, rx, ry, rz, joint)


	# Reconstruct hierarchy
	for (obj, parent) in joints_to_reorient + children_to_preserve:
		maya.cmds.parent(obj, parent)


	print("Reoriented joints in skeleton")
	return





if __name__ == '__main__':
	main()
