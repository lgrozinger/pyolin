from pyolin.utils import score
from similaritymeasures import frechet_dist as dog_leash
from similaritymeasures import curve_length_measure as curve_length
from similaritymeasures import area_between_two_curves as area_between
import seaborn

import numpy
import pandas
import matplotlib.pyplot as plt


def gate_drop_context(gate_namestring):
    splut = gate_namestring.split('_')
    return f"{splut[-2]} {splut[-1].upper()}"


def frechet(a, b):
    return 1.0 - dog_leash(a.numpy_curve(), b.numpy_curve())


def arc_length(a, b):
    return curve_length(a.numpy_curve(normal=False),
                        b.numpy_curve(normal=False))


def area(a, b):
    return area_between(a.numpy_curve(normal=False),
                        b.numpy_curve(normal=False))


def comparison(gates, comparison_func, extra_args=()):
    """
    Creates a square matrix whose entries contain the results of
    applying comparison_func to the gates provided. That is, Aij
    contains the result of `comparison_func(gate[i], gate[j])`.
    """
    count = len(gates)
    matrix = numpy.zeros((count, count))
    for i, a in enumerate(gates):
        for j, b in enumerate(gates):
            matrix[i, j] = comparison_func(a, b, *extra_args)

    labels = [gate.name for gate in gates]
    return pandas.DataFrame(matrix, index=labels, columns=labels)


def similarity_table(gates, func=frechet):
    return comparison(gates, func)


def compatibility_table(gates):
    return comparison(gates, lambda x, y: x.is_compatible_with(y))


def reduced_compatibility_table(gates):
    full_table = comparison(gates, lambda x, y: x.is_compatible_with(y))
    full_table = full_table.rename(gate_drop_context, axis='index')
    full_table = full_table.rename(gate_drop_context, axis='columns')
    full_table = full_table.groupby(full_table.index).agg(numpy.max).T
    return full_table.groupby(full_table.index).agg(numpy.max).T


def score_table(gates):
    return comparison(gates, score)


def similarity_heatmap(gates, func=frechet):
    results = similarity_table(gates, func)
    return seaborn.heatmap(results, linewidth=0.5, square=True)


def compatibility_heatmap(gates):
    results = compatibility_table(gates)
    return seaborn.heatmap(results, linewidth=0.5, square=True)


def score_heatmap(gates):
    results = score_table(gates)
    return seaborn.heatmap(results, linewidth=0.5, square=True)


def filter_valid(gates):
    """Return a list of only those gates with valid IL, OL, IH and OH"""
    return list(filter(lambda x: x.has_valid_thresholds, gates))


def predict(reference_gate, leash_length, ymin_ratio, ymax_ratio):
    pass


def dfs_max_path(adj_matrix, start, disallowed, visited, gates, paths):
    if start not in disallowed:
        outgoings = {j for (j, t) in enumerate(adj_matrix[start, :]) if t}
        outgoings = outgoings - disallowed
        if outgoings:
            gate = gates[start]
            def are_similar(A, B):
                return A.repressor == B.repressor
            similar = {i for (i, g) in enumerate(gates) if are_similar(gate, g)}
            similar = similar | disallowed
            for conn in outgoings:
                dfs_max_path(adj_matrix, conn, similar, visited + [start], gates, paths)
        else:
            paths[len(visited) + 1] = [gates[i].name for i in visited + [start]]


def dfs_path_collect(adj_matrix, i, disallowed, paths, gates, edges):
    if i not in disallowed:
        outgoings = {j for (j, t) in enumerate(adj_matrix[i, :]) if t}
        outgoings = outgoings - disallowed

        if outgoings:
            gate = gates[i]
            similar = {i for i, g in enumerate(gates) if gate.repressor == g.repressor}
            for j in outgoings:
                dfs_path_collect(adj_matrix, j, similar | disallowed, paths, gates, edges + 1)
        else:
            try:
                paths[edges] += 1
            except KeyError:
                paths[edges] = 1


def max_named_paths(gates):
    results = {}
    edges = numpy.array(compatibility_table(gates), dtype=numpy.bool)
    for i, gate in enumerate(gates):
        paths = {}
        dfs_max_path(edges, i, set(), [], gates, paths)
        results[gate.name] = paths

    return results


def all_paths(gates):
    results = {}
    edges = numpy.array(compatibility_table(gates), dtype=numpy.bool)
    for i, gate in enumerate(gates):
        paths = {}
        dfs_max_path(edges, i, set(), [], gates, paths)
        results[gate.name] = paths

    return results


def analyse(gates, label):
    summary_filename = f"results/summary_results_{label}.txt"
    score_data_filename = f"results/score_table_{label}_valid_gates_only.csv"
    compat_data_filename = f"results/compat_table_{label}_valid_gates_only.csv"
    score_map_filename = f"results/score_heatmap_of_valid_gates_{label}.eps"
    compat_map_filename = f"results/compat_heatmap_of_valid_gates_{label}.eps"
    path_filename = f"results/paths_{label}.txt"
    
    with open(summary_filename, 'w') as s:
        print(f"Analysis for {label}", file=s)
        valid_gates = filter_valid(gates)
        for gate in valid_gates:
            gate.rpuplot()
            plt.savefig(f"results/rpu_vs_rpu_for_{gate.name}.eps")
            plt.close()

        print(f"Valid gates {len(valid_gates)}/{len(gates)}.", file=s)

        score_results = score_table(valid_gates)
        compat_results = compatibility_table(valid_gates)
        score_results.to_csv(score_data_filename)
        compat_results.to_csv(compat_data_filename)

        count = sum(sum(compat_results.to_numpy()))
        print(f"There are {count} compatible pairs of gates.", file=s)

        print(f"Gate compatibility: {compat_data_filename}", file=s)
        plt.figure()  # ensures new plot
        compatibility_heatmap(valid_gates)
        plt.savefig(compat_map_filename)
        print(f"Gate combination scores: {score_data_filename}", file=s)
        plt.figure()
        score_heatmap(valid_gates)
        plt.savefig(score_map_filename)

        with open(path_filename, 'w') as f:
            print(f"Paths and path length: {path_filename}", file=s)
            paths = all_paths(valid_gates)
            for k in paths:
                print(f"START AT {k}: {paths[k]}", file=f)
            max_length = 0
            for gate, counts in paths.items():
                if counts:
                    length = max(counts.keys())
                else:
                    length = 0
                max_length = length if length > max_length else max_length

            print(f"The maximum pathlength is {max_length}", file=s)

        plt.close('all')
