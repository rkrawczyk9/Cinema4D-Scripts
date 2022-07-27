## rhelpers.py for Maya
import maya.cmds
from enum import Enum

class Axis(Enum):
	Xpos = 0
	Ypos = 1
	Zpos = 2
	Xneg = 3
	Yneg = 4
	Zneg = 5


def trim(name, delims="|:"):
	trimmed = name
	for delim in delims:
		trimmed = trimmed.rpartition(delim)[2]
	return trimmed