import json
import numpy
import wquantiles
import matplotlib.pyplot as plt
from io import StringIO

from . import utils
from .gate import Gate


def from_ucf(filename):
    ucf = None
    with open(filename, encoding='utf-8') as f:
        io = StringIO(f.read())
        ucf = json.load(io)

    return ucf

def collections(ucf, name):
    results = []
    for section in ucf:
        if "collection" in section.keys() and section["collection"] == name:
            results.append(section)

    return results

def params(ucf, name):
    responses = collections(ucf, "response_functions")
    gates = list(filter(lambda x: x["gate_name"] == name, responses))
    parameters = gates[0]["parameters"]

    return {p["name"]: p["value"] for p in parameters}

def cytometry(ucf, name):
    cytometries = collections(ucf, "gate_cytometry")
    gates = list(filter(lambda x: x["gate_name"] == name, cytometries))

    return gates[0]

def gate_histogram(ucf, name, induction):
    data = cytometry(ucf, name)["cytometry_data"][induction]

    bins = data["output_bins"]
    probability = data["output_counts"]

    return numpy.array(bins), numpy.array(probability)

def histogram_induction(ucf, name, induction):
    return cytometry(ucf, name)["cytometry_data"][induction]["input"]

def gate_median(ucf, name, induction):
    bins, probability = gate_histogram(ucf, name, induction)
    return wquantiles.median(bins, probability)

def gate_medians(ucf, name):
    cyto_data = cytometry(ucf, name)["cytometry_data"]
    medians = []
    for i, _ in enumerate(cyto_data):
        medians.append(gate_median(ucf, name, i))

    return medians

def all_names(ucf):
    gates = collections(ucf, "gates")
    names = []
    for gate in gates:
        names.append(gate["gate_name"])

    return names

class UCF:

    def __init__(self, ucf_filename):
        self._data = from_ucf(ucf_filename)

    @property
    def names(self):
        return all_names(self._data)

    def collections(self, collection_name):
        return collections(self._data, collection_name)

    def __getitem__(self, key):
        gate = None
        if isinstance(key, str):
            gate = UCFGate(self._data, key)
        else:
            raise TypeError("Provide gate name as string.")

        return gate

    def __contains__(self, item):
        return item in self.names


class UCFGate(Gate):

    def __init__(self, ucf, gate_name):
        assert gate_name in all_names(ucf)
        self._name = gate_name
        self._params = params(ucf, gate_name)
        self._cytodata = cytometry(ucf, gate_name)["cytometry_data"]
        self._upper_t = 2
        self._lower_t = 2

    @property
    def params(self):
        return self._params

    @property
    def xs(self):
        xs = []
        for i, c in enumerate(self._cytodata):
            xs.append(c["input"])

        return xs

    @property
    def ys(self):
        ys = []
        for i, c in enumerate(self._cytodata):
            bins = numpy.array(c["output_bins"])
            probabilities = numpy.array(c["output_counts"])
            median = wquantiles.median(bins, probabilities)
            ys.append(median)

        return ys


