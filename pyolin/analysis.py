from pyolin.utils import score
from similaritymeasures import frechet_dist as dog_leash
from similaritymeasures import curve_length_measure as curve_length
from similaritymeasures import area_between_two_curves as area_between
import seaborn

import numpy
import pandas
import matplotlib.pyplot as plt


def frechet(a, b):
    return dog_leash(a.numpy_curve(), b.numpy_curve())


def arc_length(a, b):
    return curve_length(a.numpy_curve(normal=False),
                        b.numpy_curve(normal=False))


def area(a, b):
    return area_between(a.numpy_curve(normal=False),
                        b.numpy_curve(normal=False))


def comparison(gates, comparison_func, extra_args=()):
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


def paths_for_gate(gate, gates):
    edges = compatibility_table(gates)

    stack = [gate.name]
    visited = []
    current_path = []
    paths = []

    while stack:
        current_gate = stack.pop()
        visited.append(current_gate)
        current_path.append(current_gate)

        outedges = []
        for name, data in edges.loc[:, current_gate].iteritems():
            if data != 0.0:
                outedges.append(name)

        unvisited = [name for name in outedges if name not in visited]
        if unvisited:
            stack += unvisited
        else:
            paths.append(current_path)
            current_path = current_path[:-1]

    return paths


def dfs_path_collect(adj_matrix, i, visited, paths, gates):
    if i not in visited:
        outgoings = [j for (j, t) in enumerate(adj_matrix[:, i]) if t]
        try:
            paths[len(visited) + 1] += 1
        except KeyError:
            paths[len(visited) + 1] = 1

        if outgoings:
            for j in outgoings:
                dfs_path_collect(adj_matrix, j, visited + [i], paths, gates)


def all_paths(gates):
    results = {}
    edges = numpy.array(compatibility_table(gates))
    for i, gate in enumerate(gates):
        paths = {}
        dfs_path_collect(edges, i, [], paths, gates)
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
    
        count = 0
        for id, row in compat_results.iterrows():
            count += len([x for x in row if x == 1.0 ])
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
            print(f"{paths}", file=f)
            max_length = 0
            for gate, counts in paths.items():
                length = max(counts.keys())
                max_length = length if length > max_length else max_length

            print(f"The maximum pathlength is {max_length}", file=s)

        plt.close('all')
