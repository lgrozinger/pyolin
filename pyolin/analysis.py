from pyolin.utils import score
from similaritymeasures import frechet_dist as dog_leash
from similaritymeasures import curve_length_measure as curve_length
from similaritymeasures import area_between_two_curves as area_between
import seaborn

import numpy
import pandas
import matplotlib.pyplot as plt
import operator as op
from functools import reduce


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


def number_context_jumps(gates):
    jumps = 0
    for a, b in zip(gates, gates[1:]):
        if not a.backbone == b.backbone or not a.strain == b.strain:
            jumps += 1
    return jumps


def dfs_max_path(adj_matrix, start, disallowed, visited, gates, paths):
    if start not in disallowed:
        outgoings = {j for (j, t) in enumerate(adj_matrix[start, :]) if t}
        outgoings = outgoings - disallowed
        if outgoings:
            gate = gates[start]
            def are_similar(A, B):
                return A.repressor == B.repressor and A.strain == B.strain and A.backbone == B.backbone
            similar = {i for (i, g) in enumerate(gates) if are_similar(gate, g)}
            similar = similar | disallowed
            for conn in outgoings:
                dfs_max_path(adj_matrix, conn, similar, visited + [start], gates, paths)
        else:
            jumps = number_context_jumps([gates[i] for i in visited + [start]])
            length = len(visited) + 1
            if length in paths:
                p, j = paths[length]
                if j > jumps:
                    paths[length] = ([gates[i].name for i in visited + [start]], jumps)
            else:
                paths[length] = ([gates[i].name for i in visited + [start]], jumps)


# def dfs_path_collect(adj_matrix, start, disallowed, visited, gates, paths):
#     if start not in disallowed:
#         outgoings = {j for (j, t) in enumerate(adj_matrix[start, :]) if t}
#         outgoings = outgoings - disallowed
#         if outgoings:
#             gate = gates[start]
#             def are_similar(A, B):
#                 return A.repressor == B.repressor
#             similar = {i for (i, g) in enumerate(gates) if are_similar(gate, g)}
#             similar = similar | disallowed
#             for conn in outgoings:
#                 dfs_max_path(adj_matrix, conn, similar, visited + [start], gates, paths)
#         elif len(visited) + 1 in paths:
#             paths[len(visited) + 1].append([gates[i].name for i in visited + [start]])
#         else:
#             paths[len(visited) + 1] = [[gates[i].name for i in visited + [start]]]


# def max_named_paths(gates):
#     results = {}
#     edges = numpy.array(compatibility_table(gates), dtype=numpy.bool)
#     for i, gate in enumerate(gates):
#         paths = {}
#         dfs_max_path(edges, i, set(), [], gates, paths)
#         results[gate.name] = paths

#     return results


def all_paths(gates):
    results = {}
    edges = numpy.array(compatibility_table(gates), dtype=numpy.bool)
    for i, gate in enumerate(gates):
        paths = {}
        dfs_max_path(edges, i, set(), [], gates, paths)
        results[gate.name] = paths

    return results


def nCr(n, r):
    r = min(r, n-r)
    if r < 0:
        return 0
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom


def possible_pairs(gates):
    """Returns the number of possible pairs for the set of gates."""
    npairs = nCr(len(gates), 2) * 2
    repressors = set([g.repressor for g in gates])

    for repressor in repressors:
        nsame = len([1 for g in gates if g.repressor == repressor])
        npairs -= nCr(nsame, 2) * 2

    return npairs


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
        print('\n'.join([g.name for g in valid_gates]), file=s)

        score_results = score_table(valid_gates)
        compat_results = compatibility_table(valid_gates)
        score_results.to_csv(score_data_filename)
        compat_results.to_csv(compat_data_filename)

        possible = possible_pairs(gates)
        print(f"There are {possible} possible pairings", file=s)
        count = sum(sum(compat_results.to_numpy()))
        print(f"There are {count} compatible pairings.", file=s)
        count = sum(sum(reduced_compatibility_table(valid_gates).to_numpy()))
        print(f"There are {count} (reduced) compatible pairings.", file=s)
        print(f"Compatible percentage: {count * 100 / possible}%", file=s)

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
