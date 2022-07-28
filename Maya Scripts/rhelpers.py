## rhelpers.py for Maya
import maya.cmds
from enum import IntEnum

class Axis(IntEnum): # the 'int' part of this does not seem to be working in this python version
	Xpos = 0
	Ypos = 1
	Zpos = 2
	Xneg = 3
	Yneg = 4
	Zneg = 5

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


def opp_axes(axis_tuple):
	"""Opposites of a tuple of Axes"""
	opp_list = []
	for axis in axis_tuple:
		opp_list.append(opp_axis(axis))
	return tuple(opp_list)


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




def trim(name, delims="|:"):
	"""Removes prefixes separated by any character in [delims]"""
	trimmed = name
	for delim in delims:
		trimmed = trimmed.rpartition(delim)[2]
	return trimmed


def add_to_joint_orient(joint, add):
	"""add: tuple of 3 floats"""
	maya.cmds.setAttr(joint+".jointOrientX", add[0] + maya.cmds.getAttr(joint+".jointOrientX"))
	maya.cmds.setAttr(joint+".jointOrientY", add[1] + maya.cmds.getAttr(joint+".jointOrientY"))
	maya.cmds.setAttr(joint+".jointOrientZ", add[2] + maya.cmds.getAttr(joint+".jointOrientZ"))