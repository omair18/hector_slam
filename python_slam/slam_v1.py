# def matchData():




# protected: 
# def estimateTransformationLogLh(): #log likelihood

# 	- OccGridMapUtil.h -> getCompleteHessianDerivs - need to log
# 	- H -> covMatrix - logged
	

# def updateEstimatedPose():
# 	estimate = estimate+change

# def drawScan():

# drawInterface
# debugInterface
import numpy as np

class Util(object):
	@staticmethod
	def normalize_angle_pos(angle):
		return ((angle % (2*np.pi)) + 2*np.pi) % (2*np.pi)

	@staticmethod
	def normalize_angle(angle):
		""" Constrains the angles to the range [0, pi) U [-pi, 0) """
		a = Util.normalize_angle_pos(angle)
		if a > np.pi:
			a -= 2*np.pi
		return a

class ScanMatcher(object):

	def __init__(self):
		pass

	def matchData(self):
		pass

	def estimateTransformationLogLh(self):
		pass

	def updateEstimatedPose():
		pass