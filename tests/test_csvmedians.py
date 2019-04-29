from .context import pyolin

from pyolin.csvdata import CSVMedians

import unittest
import os

class TestCVSMedians(unittest.TestCase):

    def setUp(self):
        self.wd = os.path.dirname(os.path.abspath(__file__))

    def tearDown(self):
        pass

    def test_names(self):
        with open(self.wd + "/test_file.csv", newline='') as io:
            expected = ["Name1", "Name2", "Name3"]
            dat = CSVMedians(io)
            actually = dat.names
            self.assertEqual(expected, actually)

    def test_get_xs(self):
        with open(self.wd + "/test_file.csv", newline='') as io:
            expected = [1.0, 2.0, 3.0]
            dat = CSVMedians(io)
            actually = dat.xs
            self.assertEqual(expected, actually)

    def test_get_ys(self):
        with open(self.wd + "/test_file.csv", newline='') as io:
            dat = CSVMedians(io)
            expected = [0.0, 0.0, 0.0]
            actually = dat["Name1"]
            self.assertEqual(expected, actually)

            expected = [2.0, 3.0, 4.0]
            actually = dat["Name3"]
            self.assertEqual(expected, actually)
