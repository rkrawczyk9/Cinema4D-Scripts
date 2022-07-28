# Allow importing from Maya Scripts folder
import sys
sys.path.append(r'C:/Users/robert.krawczyk/Documents/mybin')
sys.path.append(r'C:/Users/robert.krawczyk/Documents/Scripts/Maya Scripts')
# Reload imports from physics folder (to update code if I changed it)
import module_reloader
reload(module_reloader)
module_reloader.resetSessionForScript(r"C:/Users/robert.krawczyk/Documents/Physics Practice")

import maya.cmds
import rhelpers
from rhelpers import Axis
import skelOrientation

###### From rhelpers ########################### (These are pasted here because calling it from the other file is causing attribute errors)
def str_axis(axis):
	"""Axis to string"""
	if axis == Axis.Xpos:
		return "X+"
	elif axis == Axis.Ypos:
		return "Y+"
	elif axis == Axis.Zpos:
		return "Z+"
	elif axis == Axis.Xneg:
		return "X-"
	elif axis == Axis.Yneg:
		return "Y-"
	elif axis == Axis.Zneg:
		return "Z-"
	else:
		return "Unknown Axis: {}".format(axis)

def opp_axis(axis):
	"""Opposite of an Axis"""
	if axis == Axis.Xpos:
		return Axis.Xneg
	elif axis == Axis.Ypos:
		return Axis.Yneg
	elif axis == Axis.Zpos:
		return Axis.Zneg
	elif axis == Axis.Xneg:
		return Axis.Xpos
	elif axis == Axis.Yneg:
		return Axis.Ypos
	elif axis == Axis.Zneg:
		return Axis.Zpos
	else:
		return "Unknown Axis: {}".format(axis)

def other_axis(axis1, axis2):
	"""Returns the other axis from the ones given (positive) (the given axes must be different)"""
	axes = (axis1, axis2)

	if Axis.Xpos not in axes and Axis.Xneg not in axes:
		return Axis.Xpos
	elif Axis.Ypos not in axes and Axis.Yneg not in axes:
		return Axis.Ypos
	elif Axis.Zpos not in axes and Axis.Zneg not in axes:
		return Axis.Zpos
	else:
		print("{} and {} are not different".format(str_axis(axis1), str_axis(axis2)))

def int_axis(axis):
	"""Axis to int"""
	if axis == Axis.Xpos:
		return 0
	elif axis == Axis.Ypos:
		return 1
	elif axis == Axis.Zpos:
		return 2
	elif axis == Axis.Xneg:
		return 0
	elif axis == Axis.Yneg:
		return 1
	elif axis == Axis.Zneg:
		return 2
	else:
		return "Unknown Axis: {}".format(axis)

def add_to_joint_orient(joint, add):
	"""add: tuple of 3 floats"""
	maya.cmds.setAttr(joint+".jointOrientX", add[0] + maya.cmds.getAttr(joint+".jointOrientX"))
	maya.cmds.setAttr(joint+".jointOrientY", add[1] + maya.cmds.getAttr(joint+".jointOrientY"))
	maya.cmds.setAttr(joint+".jointOrientZ", add[2] + maya.cmds.getAttr(joint+".jointOrientZ"))
##########################################################


def main():
	sel = maya.cmds.ls(selection=True)# long=True)
	desc = maya.cmds.listRelatives(sel, allDescendents=True) #path=True)
	sel_hrc = sel + desc if desc else []

	if len(sel_hrc) == 0:
		print("Nothing selected")
		return

	#TODO: Window

	reorientSkeleton(sel_hrc, skelOrientation.mixamo, skelOrientation.volition) # convert mixamo to volition


def reorientSkeleton(skeleton_list, curr_so, desired_so, delims=""):
	"""
	Rotates each joint, without affecting its children, so that the skeleton has the desired orientation.
	*Object names must be unique - this script uses raw names, not full paths.
	"""
	delims = "|:" + delims

	joints_to_reorient = []
	# Get the appropriate joints
	for obj in skeleton_list:
		obj_name = rhelpers.trim(obj, delims)
		# Could add other conditions here to determine whether an object should be reoriented
		is_joint = maya.cmds.joint(exists=obj)
		#print("{} is joint: {}".format(obj_name, is_joint))
		if obj_name not in ("Hips", "Master", "Reference") and is_joint:
			# Store the joint with its parent in the list
			parent = maya.cmds.listRelatives(obj, parent=True)[0]#, path=True)[0]
			#print("{} parent = {}".format(obj_name, rhelpers.trim(parent)))
			joints_to_reorient.append( (obj, parent) )


	children_to_preserve = []
	# Any non-joint children of the joints should not be affected
	for (joint, _) in joints_to_reorient:
		children = maya.cmds.listRelatives(joint, children=True)
		if children:
			for child in children:# path=True):
				if (child, joint) not in joints_to_reorient:
					children_to_preserve.append((child, joint))



	# Unparent the joints to reorient, and the children to preserve
	for (obj, _) in joints_to_reorient + children_to_preserve:
		try:
			maya.cmds.parent(obj, world=True)
		except RuntimeError as e:
			#print("{} Continuing...".format(e))
			continue


	## Rotato potato ##

	# rotations dict format
	#     (current primary axis, current forward axis, desired primary axis, desired forward axis): rotation numbers
	rotations = {(Axis.Ypos, Axis.Zpos, Axis.Xpos, Axis.Ypos): [[90, 0, 90], [30, 30, 30]], # torso/head(mixamo->volition)
					 (Axis.Ypos, Axis.Xneg, Axis.Xpos, Axis.Zneg): [[90, 0, 90]], # left arm (mixamo->volition)
					 (Axis.Ypos, Axis.Xneg, Axis.Xneg, Axis.Zpos): [[-90, 0, -90]], # right arm (mixamo->volition)
					 (Axis.Ypos, Axis.Zpos, Axis.Xpos, Axis.Ypos): [[90, 180, -90]], # left leg (mixamo->volition)
					 (Axis.Ypos, Axis.Zpos, Axis.Xneg, Axis.Yneg): [[-90, 0, -90]], # right leg (mixamo->volition)
					 }
	#
	for (joint, _) in joints_to_reorient:
		joint_name = rhelpers.trim(joint)

		orientation_conversion = None
		def str_orientation_conversion():
			if not orientation_conversion or len(orientation_conversion) < 4:
				return "None"
			return "{} primary, {} forward -> {} primary, {} forward".format(str_axis(orientation_conversion[0]), str_axis(orientation_conversion[1]), str_axis(orientation_conversion[2]), str_axis(orientation_conversion[3]))

		reverse = False
		reverse_axis = None

		# Choose a rotation to execute based on the body part
		if any([word in joint_name for word in ("Spine", "Neck", "Head", "Eye", "Jaw")]):
			# Torso
			orientation_conversion = (curr_so.primary_axis, curr_so.torso_forward, desired_so.primary_axis, desired_so.torso_forward)

			print("\nRotating {} as a torso/head joint: {}".format(joint_name, str_orientation_conversion()))


		elif any([word in joint_name for word in ("Shoulder", "Arm", "Hand", "Elbow")]):
			# Arm
			orientation_conversion = (curr_so.primary_axis, curr_so.elbow_forward, desired_so.primary_axis, desired_so.elbow_forward)

			reverse = (not curr_so.right_side_reversed) and desired_so.right_side_reversed and "Right" in joint_name
			if reverse:
				reverse_axis = other_axis(desired_so.primary_axis, desired_so.elbow_forward)

			print("\nRotating {} as an arm joint{}: {}".format(joint_name, " (reversed)" if reverse else "", str_orientation_conversion()))


		elif any([word in joint_name for word in ("Leg", "Foot", "Toe", "Knee", "Butt")]):
			# Leg
			orientation_conversion = (curr_so.primary_axis, curr_so.knee_forward, desired_so.primary_axis, desired_so.knee_forward)

			reverse = (not curr_so.right_side_reversed) and desired_so.right_side_reversed and "Right" in joint_name
			if reverse:
				reverse_axis = other_axis(desired_so.primary_axis, desired_so.knee_forward)

			print("\nRotating {} as a leg joint{}: {}".format(joint_name, " (reversed)" if reverse else "", str_orientation_conversion()))


		else:
			print("Don't know what to call {}".format(joint_name))
			rotate = (0,0,0)

		#joint_name = rhelpers.trim(joint, delims)

		# Reverse
		if reverse:
			# Make the desired axes opposite
			orientation_conversion = (orientation_conversion[0], orientation_conversion[1], opp_axis(orientation_conversion[2]), opp_axis(orientation_conversion[3]))


		# Get rotation from rotations dict
		rotate = rotations.get(orientation_conversion, None)
		if rotate:
			# Rotate the joint
			for r in rotate:
				maya.cmds.rotate(r[0], r[1], r[2], joint, relative=True)#, euler=True)

		else:
			print("- axis combination not supported: {}".format(str_orientation_conversion()))
			continue

		# Reverse



		# TODO: For animations, go through each key in the rotation tracks and add the rotation to the key value


	# Reconstruct hierarchy
	for (obj, parent) in joints_to_reorient + children_to_preserve:
		#print("Parenting child {} to {}".format(obj, parent))
		try:
			maya.cmds.parent(obj, parent)
		except RuntimeError as e:
			#print("{}. Continuing...".format(e))
			continue



	print("\nReoriented joints in skeleton")
	return





if __name__ == '__main__':
	main()
