import "ScanMatcher/7DB6utP8WqtGvV0r_io.json" as dataLog

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

	def __init__(self, io, dc):
		# cheats
		self.io = io
		self.dc = dc

		# shared parameters
		self.dTr = np.zeros((3,1)) # Gradient
		self.H = np.zeros((3,3)) # Hessian

	def matchData(self, beginEstimateWorld, gridMapUtil, dataContainer, covMatrix, maxIterations):
		""" Try to stay true to the cpp API

		Parameters
		----------
		beginEstimateWorld: array-like, shape (3,)
			estimated pose in the world frame
		gridMapUtil: GridMapUtil object
			has representation of occupancy grid and methods to compute things related to the map
		dataContainer: a dict
			stores the scan data and its metadata
		covMatrix: array-like, shape (3,3)
		maxIterations: integer

		Returns
		-------
		newEstimateWorld: array-like, shape (3,)
		newEstimateMap: array-like, shape (3,)
		covMatrixOut: array-like, shape (3,3)
		"""
		if dataContainer['size']:
      		# Eigen::Vector3f beginEstimateMap(gridMapUtil.getMapCoordsPose(beginEstimateWorld));
			if gridMapUtil is None:
				beginEstimateMap = self.io['beginEstimateMap']
			else:
				beginEstimateMap = gridMapUtil.getMapCoordsPose(beginEstimateWorld)

      		# estimateTransformationLogLh(estimate, gridMapUtil, dataContainer);
			estimate = self.estimateTransformationLogLh(beginEstimateMap, gridMapUtil, dataContainer)

			for i in range(maxIterations):
				estimate = self.estimateTransformationLogLh(estimate, gridMapUtil, dataContainer)

			estimate[2] = Util.normalize_angle(estimate[2])

			covMatrixOut = self.H
			newEstimateMap = estimate
			if gridMapUtil is None:
				newEstimateWorld = self.io['newEstimateWorld']
			else:
				newEstimateWorld = gridMapUtil.getWorldCoordsPose(estimate)
			return newEstimateWorld, newEstimateMap, covMatrixOut
		else:
			return beginEstimateWorld, self.io['beginEstimateMap'], covMatrix

	def estimateTransformationLogLh(self):
		#gridMapUtil.getCompleteHessianDerivs(estimate, dataPoints, H, dTr);
		#if ((H(0, 0) != 0.0f) && (H(1, 1) != 0.0f)) {

		#read from file, get beginEstimateWorld, covMatrixOut
		estimate = self.io['beginEstimateMap']
		H = self.io['H']

		if ((H[0,0] != 0.0) and (H[1,1] != 0.0)):
			if (searchDir[2] > 0.2):
				searchDir[2] = 0.2
				print "SearchDir angle change too large"
			elif (searchDir[2] < -0.2):
				searchDir[2] = -0.2
				print "SearchDir angle change too large"

			updateEstimatedPose(estimate, searchDir)
	      	return True
      	return False

	def updateEstimatedPose(self, estimate, change):
		estimate = estimate+change