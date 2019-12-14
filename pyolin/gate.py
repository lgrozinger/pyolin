import numpy
import scipy.optimize as optim
import matplotlib.pyplot as plt

import similaritymeasures as sm

import pyolin.csvflow as csvflow
from pyolin.csvdata import CSVMedians
import pyolin.utils as utils

from math import log10 as log
from math import exp


class Gate:
    def __init__(self, name, xs, ys):
        self.xs = xs
        self.ys = ys
        self._name = name
        self._params = None
        self._upper_t = 2
        self._lower_t = 2

    @classmethod
    def from_dataframe(cls, df, strain, cargo, backbone):
        xy = []
        for id, row in df.iterrows():
            xy.append((row.iptg, row.rrpu))

        xy.sort()
        xs = [x for (x, y) in xy]
        ys = [exp(y) for (x, y) in xy]
        gate = Gate(f"{strain}_{backbone}_{cargo}", xs, ys)
        gate.dataframe = df
        return gate

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
        gate._histograms = [csvflow.rpu_histogram(p, bin_min=0.001, bin_max=946.2371) for _, p in files]
        return gate

    @property
    def il(self):
        n = self.params["n"]
        k = self.params["K"]
        t = self.thresholds[0]
        ymin = self.params["ymin"]
        ymax = self.params["ymax"]
        return ((k**n * ymax * (t - 1)) / (ymax - t * ymin))**(1 / n)

    @property
    def ol(self):
        return self.params["ymin"] * self.thresholds[1]

    @property
    def ih(self):
        n = self.params["n"]
        k = self.params["K"]
        t = self.thresholds[1]
        ymin = self.params["ymin"]
        ymax = self.params["ymax"]
        return (k**n * (ymax - t * ymin) / (t * ymin - ymin))**(1 / n)

    @property
    def oh(self):
        return self.params["ymax"] / self.thresholds[0]

    @property
    def thresholds(self):
        return (self._upper_t, self._lower_t)

    @thresholds.setter
    def thresholds(self, v):
        self._upper_t = v[0]
        self._lower_t = v[1]

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
        if self._params is None:
            ymin = min(self.ys)
            ymax = max(self.ys)
            loss = utils.residuals(self.xs, self.ys, ymin, ymax)
            lb = numpy.array([0.0, 1.0])
            ub = numpy.array([numpy.inf, numpy.inf])
            initial = numpy.array([1.0, 2.0])
            x = optim.least_squares(loss, initial, bounds=(lb, ub)).x
            self._params = {"ymin" : ymin, "ymax" : ymax, "K" : x[0], "n" : x[1]}

        return self._params

    @property
    def hill_function(self):
        params = ["ymin", "ymax", "K", "n"]
        params = [self.params[p] for p in params]
        return utils.hill_lambda(*params)

    @property
    def quickplot(self):
        figure, axes = plt.subplots()
        axes.set_title(self.name)
        axes.set_yscale("log")
        axes.set_xscale("log")
        axes.scatter(self.xs, self.ys)
        smooth_xs = numpy.logspace(log(min(self.xs)), log(max(self.xs)), 100)
        hs = list(map(self.hill_function, smooth_xs))
        axes.plot(smooth_xs, hs)
        axes.axvline(self.il, ls='--', c='r')
        axes.axvline(self.ih, ls='--', c='b')
        axes.axhline(self.ol, ls='--', c='r')
        axes.axhline(self.oh, ls='--', c='b')

        return figure

    @property
    def histograms(self):
        return [self.histogram(x) for x in self.xs]

    @property
    def has_valid_thresholds(self):
        return self.ih > self.il and self.oh > self.ol

    def histogram(self, x_index):
        figure, axes = plt.subplots()
        axes.set_title(self.name)
        axes.set_xscale("log")
        xs, bins = self._histograms[x_index]
        axes.hist(xs, bins=bins)
        return figure

    def is_compatible_with(self, other, offset=0.0):
        return (utils.score(self, other, offset=offset) > 0
                and self.has_valid_thresholds
                and other.has_valid_thresholds
                and self.name[2:] != other.name[2:])

    def numpy_curve(self, normal=True):
        data = numpy.zeros((len(self.xs), 2))
        data[:, 0] = numpy.array(self.xs)
        if normal:
            data[:, 1] = numpy.array(self.normalised_ys)
        else:
            data[:, 1] = numpy.array(self.ys)
        return data

    def frechet_similarity_to(self, other):
        return sm.frechet_dist(self.numpy_curve, other.numpy_curve)

    def curve_length_similarity_to(self, other):
        return sm.curve_length_measure(self.numpy_curve, other.numpy_curve)

    @property
    def normalised_ys(self):
        ymin = self.params["ymin"]
        ymax = self.params["ymax"]
        yrange = ymax - ymin
        return [(y - ymin) / yrange for y in self.ys]
