import numpy
import matplotlib.pyplot as plt

from .csvdata import CSVMedians
import pyolin.utils as utils

class Gate:

    def __init__(self, name, xs, ys):
        self.xs = xs
        self.ys = ys
        self._name = name

    @classmethod
    def from_csv(cls, filename, gate_name):
        with open(filename) as f:
            data = CSVMedians(f)
            xs = data.xs
            ys = data[gate_name]
            return cls(gate_name, xs, ys)

    @property
    def name(self):
        return self._name

    @property
    def params(self):
        # Huseyin plug in fitting here please
        # return fitted_parameters(self.xs, self.ys)
        # should return dictionary of {param_name : param_value}
        return {"ymin" : 0.01, "ymax" : 10.0, "K" : 0.3, "n" : 2.0}

    @property
    def hill_function(self):
        return utils.hill_lambda(*list(self.params.values()))

    @property
    def plot(self):
        figure, axes = plt.subplots()
        # axes.set_xlabel(xaxis)
        # axes.set_ylabel(yaxis)
        axes.set_title(self.name)
        axes.scatter(self.xs, self.ys)
        hs = list(map(self.hill_function, self.xs))
        axes.plot(self.xs, hs)
        return figure
