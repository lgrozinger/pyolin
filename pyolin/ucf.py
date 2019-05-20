import json
import numpy

def from_ucf(filename):
    ucf = None
    with open(filename) as f:
        ucf = json.decode(read(f))

    return ucf

def collections(ucf, name)
    results = []
    for section in ucf.keys():
        if "collection" in section.keys() && section["collection"] == name:
            results.append(section)

    return results

def params(ucf, name)
    responses = collections(ucf, "response_functions")
    gates = [x if x["gate_name"] == name for x in responses]
    parameters = gates[0]["parameters"]

    return {p["name"]: p["value"] for p in paramters}

def cytometry(ucf, name)
    cytometries = collections(ucf, "gate_cytometry")
    gates = [x if x["gate_name"] == name for x in cytometries]

    return gates[0]

def gate_histogram(ucf, name, induction)
    data = cytometry(ucf, gate_name)["cytometry_data"][induction]

    bins = data["output_bins"]
    counts = data["output_counts"]

    return numpy.histogram(counts, bins=bins, density=True)

def gate_median(ucf, name, induction)
    b, pdf = gate_histogram(ucf, name, induction)
    cp = 0.0
    i = 0
    while cp < 0.5:
        cp += pdf
        i = 1 + i

    return (b[i - 1] + b[i]) * 0.5

def gate_medians(ucf, name)
    cyto_data = cytometry(ucf, name)["cytometry_data"]
    medians = []
    for i, _ in enumerate(cyto_data):
        medians.append(gate_median(ucf, name, i))

    return medians

def all_names(ucf)
    gates = collections(ucf, "gates")
    names = []
    for gate in gates:
        names.append(gate["gate_name"])

    return names
