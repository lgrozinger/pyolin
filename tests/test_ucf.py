from .context import pyolin

from pyolin import ucf

import unittest
import os

class TestUCF(unittest.TestCase):

    def setUp(self):
        self.wd = os.path.dirname(os.path.abspath(__file__))

    def tearDown(self):
        pass

    def test_read(self):
        u = ucf.from_ucf(self.wd + "/../ucf/Eco1C1G1T0.UCF.json")
        self.assertFalse(u is None)
        self.assertTrue(isinstance(u, list))

    def test_collection(self):
        u = ucf.UCF(self.wd + "/../ucf/Eco1C1G1T0.UCF.json")
        expected = {"collection": "gates",
                    "regulator": "AmtR",
                    "group_name": "AmtR",
                    "gate_name": "A1_AmtR",
                    "gate_type": "NOR",
                    "system": "TetR",
                    "color_hexcode": "3BA9E0"}
        actually = u.collections("gates")
        self.assertTrue(expected in actually)

    def test_params(self):
        u = ucf.UCF(self.wd + "/../ucf/Eco1C1G1T0.UCF.json")
        expected = {"ymax" : 3.8,
                    "ymin" : 0.06,
                    "K" : 0.07,
                    "n" : 1.6}
        actually = u["A1_AmtR"].params

    def test_gate_xs(self):
        u = ucf.UCF(self.wd + "/../ucf/Eco1C1G1T0.UCF.json")
        expected = [0.004843,
                    0.007426,
                    0.01253,
                    0.034109,
                    0.0627,
                    0.099936,
                    0.144093,
                    0.247036,
                    0.418091,
                    0.739476,
                    1.012582,
                    2.07846]
        actually = u["A1_AmtR"].xs
        self.assertEqual(expected, actually)

    def test_gate_medians(self):
        u = ucf.UCF(self.wd + "/../ucf/Eco1C1G1T0.UCF.json")
        expected = [13.645628355810723,
                    12.318076465819308,
                    11.03620158545664,
                    7.68886840656224,
                    4.852876727681681,
                    3.1760096981144494,
                    2.21217234423202,
                    1.3914108806984762,
                    0.8727321683477501,
                    0.5655925258268966,
                    0.44545795702228386,
                    0.32071011716003545]
        actually = u["A1_AmtR"].ys
        self.assertEqual(expected, actually)
