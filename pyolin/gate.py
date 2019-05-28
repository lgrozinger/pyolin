import numpy
import matplotlib.pyplot as plt

import pyolin.csvflow as csvflow
from pyolin.csvdata import CSVMedians
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

    @classmethod
    def from_csvflow(cls, gate_name):
        files = csvflow.csv_paths(gate_name)
        files.sort(key=lambda pair : pair[0])
        xs = [x for x, _  in files]
        af = csvflow.median_af()
        st = csvflow.median_standard()
        def rpu(path):
            median = csvflow.median(path)
            return utils.au_to_rpu(median, af, st)

        ys = [rpu(path) for _, path in files]
        gate = cls(gate_name, xs, ys)
        gate.histograms = [csvflow.rpu_histogram(p, bin_min=0.001, bin_max=946.2371) for _, p in files]
        return gate

    @property
    def from_gates(cls, input_gate, output_gate):
        return cls(output_gate.name, input_gate.ys, output_gate.ys)

    @property
    def dynamic_output_range(self):
        return max(self.ys) / min(self.ys)

    @property
    def dynamic_input_range(self):
        return max(self.xs) / min(self.xs)

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
        params = ["ymin", "ymax", "K", "n"]
        params = [self.params[p] for p in params]
        return utils.hill_lambda(*params)

    @property
    def plot(self):
        figure, axes = plt.subplots()
        # axes.set_xlabel(xaxis)
        # axes.set_ylabel(yaxis)
        axes.set_title(self.name)
        axes.set_yscale("log")
        axes.set_xscale("log")
        axes.scatter(self.xs, self.ys)
        hs = list(map(self.hill_function, self.xs))
        axes.plot(self.xs, hs)
        return figure

    def histogram(self, x_index):
        figure, axes = plt.subplots()
        # axes.set_xlabel(xaxis)
        # axes.set_ylabel(yaxis)
        axes.set_title(self.name)
        axes.set_xscale("log")
        bins, xs = self.histograms[x]
        axes.hist(xs, bins=bins)
        return figure
