from .context import pyolin

from pyolin.gate import Gate

import unittest
import os

class TestGate(unittest.TestCase):

    def setUp(self):
        self.wd = os.path.dirname(os.path.abspath(__file__))

    def tearDown(self):
        pass

    def test_gate_from_csvflow(self):
        g = Gate.from_csvflow("A1_AmtR")
        self.assertTrue(isinstance(g, Gate))

    def test_gate_param_estimation(self):
        g = Gate.from_csv(self.wd + "/../ucf/gates2.csv", "F1_AmeR")
        g.params
