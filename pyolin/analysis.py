from pyolin.gate import Gate
import similaritymeasures as sm
import seaborn

import numpy
from math import exp

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
                    rpu_in = self.get_input_rpus(name[0], name[1])
                    gate_curve = self.get_gate_curve(*name)
                    iptg_in = [iptg for (iptg, rpu) in gate_curve]
                    rpu_out = [rpu for (iptg, rpu) in gate_curve]
                    gate = Gate('_'.join(name), iptg_in, rpu_in, rpu_out)
                    results.append(gate)

            results = results if len(results) > 1 else results[0]
            return results
        else:
            raise TypeError

    def get_gate_curve(self, strain, backbone, plasmid):
        gate_df = self.df[(self.df.strain == strain) &
                          (self.df.backbone == backbone) &
                          (self.df.plasmid == plasmid)]

        gate_curve = [(exp(row.iptg), exp(row.rrpu)) for id, row in gate_df.iterrows()]
        gate_curve.sort()
        return gate_curve
        
    def get_input_rpus(self, strain, backbone):
        input_gate_curve = self.get_gate_curve(strain, backbone, '1818')
        return [rpu for (iptg, rpu) in input_gate_curve]
        

def frechet(a, b):
    return sm.frechet_dist(a.numpy_curve(), b.numpy_curve())


def curve_length(a, b):
    return sm.curve_length_measure(a.numpy_curve(normal=False),
                                   b.numpy_curve(normal=False))


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


def predict(reference_gate, leash_length, ymin_ratio, ymax_ratio):
    pass


def get_plasmids(df):
    return df.plasmid.drop_duplicates()[df.plasmid != 'Empty']


def get_strains(df):
    return df.strain.drop_duplicates()[df.strain != 'Empty']


def get_backbones(df):
    return df.backbone.drop_duplicates()[df.backbone != 'Empty']


