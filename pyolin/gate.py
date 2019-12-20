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
    def __init__(self, name, iptg, rpu_in, rpu_out):
        self.iptg = iptg
        self.rpu_in = rpu_in
        self.rpu_out = rpu_out
        self._name = name
        self._params = None
        self._upper_t = 2
        self._lower_t = 2

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

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
        return max(self.rpu_out) / min(self.rpu_out)

    @property
    def dynamic_input_range(self):
        return max(self.rpu_in) / min(self.rpu_in)

    @property
    def name(self):
        return self._name

    @property
    def strain(self):
        return self.name.split('_')[0]

    @property
    def backbone(self):
        return self.name.split('_')[1]

    @property
    def cargo(self):
        return '_'.join(self.name.split('_')[-2:])

    @property
    def params(self):
        if self._params is None:
            ymin = min(self.rpu_out)
            ymax = max(self.rpu_out)
            loss = utils.residuals(self.rpu_in, self.rpu_out, ymin, ymax)
            lb = numpy.array([0.0, 1.0])
            ub = numpy.array([numpy.inf, numpy.inf])
            initial = numpy.array([1.0, 2.0])
            try:
                x = optim.least_squares(loss, initial, bounds=(lb, ub)).x
                self._params = {"ymin" : ymin, "ymax" : ymax, "K" : x[0], "n" : x[1]}
            except ValueError:
                print(self.name, self.iptg, self.rpu_in, self.rpu_out)
        return self._params

    @property
    def hill_function(self):
        params = ["ymin", "ymax", "K", "n"]
        params = [self.params[p] for p in params]
        return utils.hill_lambda(*params)

    @property
    def normalised_hill_function(self):
        return utils.hill_lambda(1e-6, 1.0, self.params["K"], self.params["n"])

    def baseplot(self, ylimits=None):
        figure, axes = plt.subplots()
        axes.set_title(self.name)
        axes.set_yscale("log")
        axes.set_xscale("log")

        if ylimits is not None:
            axes.set_ylim(*ylimits)
        else:
            axes.set_ylim(self.params["ymin"] * 0.1,
                          self.params["ymax"] * 10.0)

        return figure, axes

    def rpuplot(self, ylimits=None):
        figure, axes = self.baseplot(ylimits=ylimits)
        axes.set_xlabel("Input (RPUs)")
        axes.set_ylabel("Output (RPUs)")
        axes.set_xlim(min(self.rpu_in), max(self.rpu_in))
        axes.scatter(self.rpu_in, self.rpu_out)
        smooth_xs = numpy.logspace(log(min(self.rpu_in)),
                                   log(max(self.rpu_in)),
                                   100)
        hs = list(map(self.hill_function, smooth_xs))
        axes.plot(smooth_xs, hs)
        axes.axvline(self.il, ls='--', c='r')
        axes.axvline(self.ih, ls='--', c='b')
        axes.axhline(self.ol, ls='--', c='r')
        axes.axhline(self.oh, ls='--', c='b')

        return figure

    def plot(self, ylimits=None):
        figure, axes = self.baseplot(ylimits=ylimits)
        axes.set_xlabel("IPTG (µM)")
        axes.set_ylabel("Output (RPUs)")
        axes.set_xlim(min(self.iptg), max(self.iptg))
        axes.scatter(self.iptg, self.rpu_out)

        return figure

    @property
    def histograms(self):
        return [self.histogram(x) for x in self.rpu_in]

    @property
    def has_valid_thresholds(self):
        return self.ih > self.il and self.oh > self.ol

    def histogram(self, x_index):
        figure, axes = plt.subplots()
        axes.set_title(self.name)
        axes.set_xscale("log")
        xs, bins = self._histograms[x_index]
        axes.hist(xs, bins=bins)
        return figure, axes

    def is_compatible_with(self, other, offset=0.0):
        this_gate = self.name.split('_')[2]
        that_gate = other.name.split('_')[2]
        return (utils.score(self, other, offset=offset) > 0
                and self.has_valid_thresholds
                and other.has_valid_thresholds
                and this_gate != that_gate)

    def numpy_curve(self, normal=True):
        data = numpy.zeros((len(self.rpu_in), 2))
        data[:, 0] = numpy.array(self.rpu_in)
        if normal:
            data[:, 1] = numpy.array(self.normalised_rpu_out)
        else:
            data[:, 1] = numpy.array(self.rpu_out)
        return data

    @property
    def normalised_rpu_out(self):
        ymin = self.params["ymin"]
        ymax = self.params["ymax"]
        yrange = ymax - ymin
        return [(y - ymin) / yrange for y in self.rpu_out]
