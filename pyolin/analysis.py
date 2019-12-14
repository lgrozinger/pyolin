from pyolin.gate import Gate
import similaritymeasures as sm
import seaborn

import numpy


class GateData:
    def __init__(self, pandas_dataframe):
        self.df = pandas_dataframe

    def __getitem__(self, key):
        if isinstance(key, slice):
            strain = key.start
            backbone = key.stop
            cargo = key.step

            data = self.df
            if strain is not None:
                data = data[data.strain == strain]
            if backbone is not None:
                data = data[data.backbone == backbone]
            if cargo is not None:
                data = data[data.plasmid == cargo]

            results = []
            for name, group in data.groupby(['strain', 'backbone', 'plasmid']):
                if not group.empty:
                    results.append(Gate.from_dataframe(group, *name))

            return results
        else:
            raise TypeError


def frechet(a, b):
    return sm.frechet_dist(a.numpy_curve(), b.numpy_curve())


def curve_length(a, b):
    return sm.curve_length_measure(a.numpy_curve(), b.numpy_curve())


def area(a, b):
    return sm.area_between_two_curves(a.numpy_curve(normal=False),
                                      b.numpy_curve(normal=False))


def pcm(a, b):
    return sm.pcm(a.numpy_curve(normal=False), b.numpy_curve(normal=False))


def similarity_table(gate_data, plasmid_name, func=frechet):
    plasmids = gate_data[::plasmid_name]
    count = len(plasmids)

    results = numpy.zeros((count, count))
    for i in range(count):
        for j in range(count):
            results[i, j] = func(plasmids[i], plasmids[j])

    return results, [gate.name for gate in plasmids]


def similarity_heatmap(gate_data, plasmid_name, func=frechet):
    results, labels = similarity_table(gate_data, plasmid_name, func)
    return seaborn.heatmap(results,
                           linewidth=0.5,
                           xticklabels=labels,
                           yticklabels=labels)


def get_plasmids(df):
    return df.plasmid.drop_duplicates()[df.plasmid != 'Empty']


def get_strains(df):
    return df.strain.drop_duplicates()[df.strain != 'Empty']


def get_backbones(df):
    return df.backbone.drop_duplicates()[df.backbone != 'Empty']


