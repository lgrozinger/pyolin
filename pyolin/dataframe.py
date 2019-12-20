from math import exp

from pyolin.gate import Gate


def remove_emptys(df):
    return df[(df.plasmid != 'Empty') &
              (df.plasmid != 'EmptyRow') &
              (df.strain != 'Empty') &
              (df.strain != 'EmptyRow') &
              (df.backbone != 'Empty') &
              (df.backbone != 'EmptyRow')]


class GateData:
    def __init__(self, pandas_dataframe):
        self.df = remove_emptys(pandas_dataframe)

    def __getitem__(self, key):
        if isinstance(key, slice):
            strain = key.start
            backbone = key.stop
            cargo = key.step

            data = self.df[(self.df.plasmid != '1818') &
                           (self.df.plasmid != '1717') &
                           (self.df.plasmid != '1201')]
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

            if results:
                results = results if len(results) > 1 else results[0]

            return results
        else:
            raise TypeError

    def get_gate_curve(self, strain, backbone, plasmid, x='iptg', y='rrpu'):
        view = self.df[(self.df.strain == strain) &
                       (self.df.backbone == backbone) &
                       (self.df.plasmid == plasmid)]

        gate_curve = []
        for (x, y) in [(row[x], row[y]) for id, row in view.iterrows()]:
            if y <= 0.0:
                gate_curve.append((x, 1e-6))
            else:
                gate_curve.append((x, y))
        gate_curve.sort()
        return gate_curve

    def get_input_rpus(self, strain, backbone):
        input_gate_curve = self.get_gate_curve(strain, backbone, '1818')
        return [rpu for (iptg, rpu) in input_gate_curve]

    def auto_gate(self, strain, backbone):
        curve = self.get_gate_curve(strain, backbone, '1201')
        iptg = [x for (x, y) in curve]
        rpu = [y for (x, y) in curve]
        return Gate(f"auto_{strain}_{backbone}", iptg, iptg, rpu)

    def input_gate(self, strain, backbone):
        curve = self.get_gate_curve(strain, backbone, '1818')
        iptg = [x for (x, y) in curve]
        rpu = [y for (x, y) in curve]
        return Gate(f"input_{strain}_{backbone}", iptg, iptg, rpu)

    def standard_gate(self, strain, backbone):
        curve = self.get_gate_curve(strain, backbone, '1717')
        iptg = [x for (x, y) in curve]
        rpu = [y for (x, y) in curve]
        return Gate(f"standard_{strain}_{backbone}", iptg, iptg, rpu)

    def get_from_name(self, name):
        parts = name.split('_')
        strain = parts[0]
        backbone = parts[1]
        cargo = f"{parts[2]}_{parts[3]}"
        return self[strain:backbone:cargo]

    @property
    def strains(self):
        return self.df.strain.drop_duplicates()

    @property
    def plasmids(self):
        return self.df.plasmid.drop_duplicates()

    @property
    def backbones(self):
        return self.df.backbone.drop_duplicates()

    @property
    def contexts(self):
        return [name for name, _ in self.df.groupby(['strain', 'backbone'])]
