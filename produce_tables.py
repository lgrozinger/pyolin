"""
(Re)produce the tables from the supplement!
"""
import pandas

from pyolin.dataframe import GateData
from pyolin.analysis import filter_valid
from pyolin.analysis import possible_pairs
from pyolin.analysis import compatibility_table
from pyolin.figures import similaritymap

tex_file = 'results/tables.tex'


def gate_summary_table(gates, stream):
    columns = ['Strain', 'Plasmid',
               'Y min', 'Y max', 'n', 'k',
               'IH', 'OH', 'IL', 'OL',
               'Functional NOT']
    table = pandas.DataFrame(columns=columns)
    for gate in gates:
        row = [
            gate.strain,
            gate.backbone,
            gate.ymin,
            gate.ymax,
            gate.n,
            gate.K,
            gate.ih,
            gate.oh,
            gate.il,
            gate.ol,
            'Yes' if gate.has_valid_thresholds else 'No'
        ]

        table = table.append(pandas.DataFrame([row], columns=columns))

    if not table.empty:
        caption = f"""{gate.cargo.replace('_', ' ').upper()}: Hill equation
        parameters and thresholds across all contexts"""
        tex_out = table.to_latex(index=False, na_rep='',
                                 float_format='%2.2f',
                                 caption=caption)
        print(tex_out, file=stream)
        return table


def context_summary_table(data, stream):
    columns = ['Strain', 'Plasmid', 'Gates', 'Valid', 'Pairings(All)', 'Pairings(Valid)', 'Compatible Pairings', '% (All)', '% (Valid)']
    table = pandas.DataFrame(columns=columns)

    for strain, plasmid in data.contexts:
        gates = data[strain:plasmid:]
        functional = filter_valid(gates)
        ngates = len(gates)
        nfunctional = len(functional)
        npossibleall = possible_pairs(gates)
        npossible = possible_pairs(functional)
        ncompatible = sum(map(int, sum(compatibility_table(functional).to_numpy())))
        percentall = 100 * ncompatible / npossibleall
        percent = 100 * ncompatible / npossible
        row = [
            strain,
            plasmid,
            ngates,
            nfunctional,
            npossibleall,
            npossible,
            ncompatible,
            percentall,
            percent
        ]
        table = table.append(pandas.DataFrame([row], columns=columns))

    for strain in set([context[0] for context in data.contexts]):
        gates = data[strain::]
        functional = filter_valid(gates)
        ngates = len(gates)
        nfunctional = len(functional)
        npossibleall = possible_pairs(gates)
        npossible = possible_pairs(functional)
        ncompatible = sum(map(int, sum(compatibility_table(functional).to_numpy())))
        percentall = 100 * ncompatible / npossibleall
        percent = 100 * ncompatible / npossible
        row = [
            strain,
            'All',
            ngates,
            nfunctional,
            npossibleall,
            npossible,
            ncompatible,
            percentall,
            percent
        ]
        table = table.append(pandas.DataFrame([row], columns=columns))

    gates = data[::]
    functional = filter_valid(gates)
    ngates = len(gates)
    nfunctional = len(functional)
    npossibleall = possible_pairs(gates)
    npossible = possible_pairs(functional)
    ncompatible = sum(map(int, sum(compatibility_table(functional).to_numpy())))
    percentall = 100 * ncompatible / npossibleall
    percent = 100 * ncompatible / npossible
    row = [
        'All',
        'All',
        ngates,
        nfunctional,
        npossibleall,
        npossible,
        ncompatible,
        percentall,
        percent
    ]
    table = table.append(pandas.DataFrame([row], columns=columns))

    caption = f""
    tex_out = table.to_latex(index=False, na_rep='',
                             float_format='%2.2f',
                             caption=caption)
    print(tex_out, file=stream)
    return table


def context_increase_table_multi_backbone(data, stream):
    intra = {}
    for strain, backbone in data.contexts:
        gates = filter_valid(data[strain:backbone:])
        pairs = sum(map(int, sum(compatibility_table(gates).to_numpy())))
        intra[strain] = intra.get(strain, 0) + pairs

    inter = {}
    for strain in data.strains:
        gates = data[strain::]
        pairs = sum(map(int, sum(compatibility_table(gates).to_numpy())))
        inter[strain] = inter.get(strain, 0) + pairs

    columns = ['Strain',
               'Compatible Pairs (single-backbone)',
               'Compatible Pairs (inter-backbone)',
               'Compatible Pairs (total)',
               'Fold Change']
    column_format = 'l  p{3cm} p{3cm} p{3cm} r'
    table = pandas.DataFrame(columns=columns)
    for strain in intra:
        row = [strain,
               intra[strain],
               inter[strain] - intra[strain],
               inter[strain],
               inter[strain] / intra[strain]]
        table = table.append(pandas.DataFrame([row], columns=columns))

    caption = """A table showing how compatible pairings increases
when additional backbones are utilised in the library. For each
strain, the numbers of compatible pairings in which both gates use the
same backbone (`single-backbone'), different backbones
(`inter-backbone') and the sum of both (`total') are
shown. Fold-change is between the single backbone and `total' is also
shown."""

    tex = table.to_latex(index=False,
                         float_format='%2.2f',
                         column_format=column_format,
                         caption=caption)
    print(tex, file=stream)
    return table


def context_increase_table_multi_host(data, stream):
    intra = {}
    for strain in data.strains:
        gates = filter_valid(data[strain::])
        pairs = sum(map(int, sum(compatibility_table(gates).to_numpy())))
        intra[strain] = pairs

    gates = data[::]
    pairs = sum(map(int, sum(compatibility_table(gates).to_numpy())))

    columns = ['DH5alpha', 'CC118Lpir', 'KT2440', 
               'Compatible Pairs (single-host)',
               'Compatible Pairs (inter-host)',
               'Compatible Pairs (total)',
               'Fold Change']
    column_format = 'l l l  p{3cm} p{3cm} p{3cm} r'
    table = pandas.DataFrame(columns=columns)
    row = [intra['DH5alpha'],
           intra['CC118Lpir'],
           intra['KT2440'],
           sum(intra.values()),
           pairs - sum(intra.values()),
           pairs,
           pairs / sum(intra.values())]
    table = table.append(pandas.DataFrame([row], columns=columns))

    caption = """A table showing how compatible pairings increases
when additional hosts are utilised in the library. For each host, the
numbers of compatible pairings are shown. Also indicated is the number
of inter-host pairings and the fold change between the total of
single-host pairings and pairings across all contexts."""

    tex = table.to_latex(index=False,
                         float_format='%2.2f',
                         caption=caption,
                         column_format=column_format)
    print(tex, file=stream)
    return table


def similarity_score_table(data, stream):
    print(r'\renewcommand{\arraystretch}{2.0}', file=stream)
    for inverter in data.gates[3:]:
        scores = similaritymap(data[::inverter], 'figures/SuppFigure4/')

        def drop_newline(string):
            return string.replace(r'\n', ' ')

        scores = scores.rename(drop_newline, axis='index')
        scores = scores.rename(drop_newline, axis='columns')
        caption = f"""Numerical similarity scores for
        {inverter.replace('_', ' ').upper()} across all contexts. This
        data is plotted in Figure S4."""
        column_format = 'p{1.8cm} | p{1.8cm} p{1.8cm} p{1.8cm} p{1.8cm} p{1.8cm} p{1.8cm} p{1.8cm}'
        tex = scores.to_latex(float_format='%2.2f',
                              caption=caption,
                              column_format=column_format)
        print(tex, file=stream)
    print(r'\renewcommand{\arraystretch}{1.0}', file=stream)


if __name__ == '__main__':
    # reading and renaming some columns
    raw = pandas.read_csv('cyto2func/standardised_cheeky.csv')
    raw = raw.rename(columns={'rrpu': 'decomp_flor'})
    raw = raw.rename(columns={'newstandard': 'rrpu'})

    data = GateData(raw)

    with open(tex_file, 'w') as tex:
        for inverter in data.gates[3:]:
            gate_summary_table(data[::inverter], tex)

        context_summary_table(data, tex)
        context_increase_table_multi_backbone(data, tex)
        context_increase_table_multi_host(data, tex)
        similarity_score_table(data, tex)
