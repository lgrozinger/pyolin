import json
import numpy
import wquantiles
from io import StringIO

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
