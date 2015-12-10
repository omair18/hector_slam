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

from slam_v1 import Util

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
		# not a comprehensive test for parameters, but shows you the gist
		self.assertTrue('covMatrixIn' in io)
		self.assertTrue('beginEstimateWorld' in io)

	def test_dataContainer_loaded(self):
		self.assertTrue('origo' in dc)
		self.assertTrue('size' in dc)
		self.assertTrue('dataPoints' in dc)

	def test_shouldFail(self):
		self.assertTrue('ryan' in dc)

class TestUtil(unittest.TestCase):
	def test_normalize_angle(self):
		x1 = np.linspace(-2*np.pi, 2*np.pi, 25)
		f = np.vectorize(Util.normalize_angle)
		x2 = f(x1)
		print "\n", np.column_stack((x1,x2))
		self.assertTrue(x2.min() >= -np.pi)
		self.assertTrue(x2.max() >= np.pi)
