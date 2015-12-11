"""
To test, run the command
>>> nosetests
or to see print statements
>>> nosetests --nocapture
"""
import unittest

import json
import os
import numpy as np

from slam_v1 import Util, ScanMatcher

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

data_path = os.path.join(__location__, 'ScanMatcherLogs')
data_files = os.listdir(data_path)

i = 0
io_path = os.path.join(data_path, data_files[i])
dc_path = os.path.join(data_path, data_files[i+1])
io = json.load(open(io_path, 'r'))
dc = json.load(open(dc_path, 'r'))

class TestDataSerialization(unittest.TestCase):
	def test_io_loaded(self):
		self.assertTrue('beginEstimateWorld' in io)
		self.assertTrue('covMatrixIn' in io)
		self.assertTrue('maxIterations' in io)
		self.assertTrue('beginEstimateMap' in io)
		self.assertTrue('covMatrixOut' in io)
		self.assertTrue('newEstimateMap' in io)
		self.assertTrue('newEstimateWorld' in io)

	def test_dataContainer_loaded(self):
		self.assertTrue('origo' in dc)
		self.assertTrue('size' in dc)
		self.assertTrue('dataPoints' in dc)

class TestUtil(unittest.TestCase):
	def test_normalize_angle(self):
		x1 = np.linspace(-2*np.pi, 2*np.pi, 25)
		f = np.vectorize(Util.normalize_angle)
		x2 = f(x1)
		print "\n", np.column_stack((x1,x2))
		self.assertTrue(x2.min() >= -np.pi)
		self.assertTrue(x2.max() >= np.pi)

class TestScanMatcher(unittest.TestCase):
	def test_matchData(self):
		scanMatcher = ScanMatcher(io=io, dc=dc)
		out = scanMatcher.matchData(
			  beginEstimateWorld=scanMatcher.io['beginEstimateWorld']
			, gridMapUtil=None
			, dataContainer=scanMatcher.dc
			, covMatrix=scanMatcher.io['covMatrixIn']
			, maxIterations=scanMatcher.io['maxIterations']
			)
		newEstimateWorld, newEstimateMap, covMatrixOut = out
		vector3ify = lambda arr: np.array(arr).reshape((3,))
		matrix3ify = lambda arr: np.array(arr).reshape((3,3))
		print "test values"
		print vector3ify(scanMatcher.io['newEstimateWorld'])
		print vector3ify(scanMatcher.io['newEstimateMap'])
		print matrix3ify(scanMatcher.io['covMatrixOut'])

		print "output values"
		print newEstimateWorld
		print newEstimateMap
		print covMatrixOut
		self.assertTrue(np.allclose(newEstimateWorld, vector3ify(scanMatcher.io['newEstimateWorld'])))
		self.assertTrue(np.allclose(newEstimateMap, vector3ify(scanMatcher.io['newEstimateMap'])))
		self.assertTrue(np.allclose(covMatrixOut, matrix3ify(scanMatcher.io['covMatrixOut'])))
