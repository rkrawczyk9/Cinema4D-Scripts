from rhelpers import Axis


class Skeleton_Orientation:
	primary_axis = None
	torso_forward = None
	elbow_forward = None
	knee_forward = None

	right_side_reversed = None


	def __init__(self, primary_axis=Axis.Xpos, torso_forward=Axis.Ypos, elbow_forward=Axis.Zneg, knee_forward=Axis.Ypos, right_side_reversed=True):
		self.primary_axis = primary_axis
		self.torso_forward = torso_forward
		self.elbow_forward = elbow_forward
		self.knee_forward = knee_forward
		self.right_side_reversed = right_side_reversed


mixamo = Skeleton_Orientation(primary_axis=Axis.Ypos, torso_forward=Axis.Zpos, elbow_forward=Axis.Xneg, knee_forward=Axis.Zpos, right_side_reversed=False)
volition = Skeleton_Orientation(primary_axis=Axis.Xpos, torso_forward=Axis.Ypos, elbow_forward=Axis.Zneg, knee_forward=Axis.Ypos, right_side_reversed=False)