import matplotlib.pyplot as plot
from .utils import score
import seaborn as sns
import numpy

def compatibility_heatmap(gates):

    valid_gates = [g for g in filter(lambda x: x.has_valid_thresholds, gates)]
    num_gates = len(valid_gates)
    compatibility = numpy.zeros((num_gates, num_gates), dtype=bool)
    for j in range(num_gates):
        a = valid_gates[j]
        for i in range(num_gates):
            b = valid_gates[i]
            compatibility[i,j] = a.is_compatible_with(b)

    figure, axes = plot.subplots()
    gate_names = [g.name for g in valid_gates]

    sns.heatmap(compatibility,
                cmap=["gainsboro", "grey"],
                linecolor="white",
                linewidths=3,
                xticklabels=gate_names,
                yticklabels=gate_names,
                cbar=True,
                cbar_kws={'ticks':[0, 1]},
                square=True,
                ax=axes)
    axes.invert_yaxis()
    axes.set_xlabel("Input Gate")
    axes.set_ylabel("Output Gate")

    return figure

def score_heatmap(gates):

    valid_gates = [g for g in filter(lambda x: x.has_valid_thresholds, gates)]
    num_gates = len(valid_gates)
    scores = numpy.zeros((num_gates, num_gates), dtype=numpy.single)
    for j in range(num_gates):
        a = valid_gates[j]
        for i in range(num_gates):
            b = valid_gates[i]
            scores[i,j] = score(a, b)

    figure, axes = plot.subplots()
    gate_names = [g.name for g in valid_gates]

    sns.heatmap(scores,
                linecolor="white",
                linewidths=1,
                xticklabels=gate_names,
                yticklabels=gate_names,
                cbar=True,
                square=True,
                ax=axes)
    axes.invert_yaxis()
    axes.set_xlabel("Input Gate")
    axes.set_ylabel("Output Gate")

    return figure
