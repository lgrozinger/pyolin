"""
(Re)produce the plots from the figures!
"""
import pyolin.figures as figures

import pandas
import os

from pyolin.dataframe import GateData
from pyolin.analysis import filter_valid

fig_dir = 'notebooks/results/figure_data'

if __name__ == '__main__':
    # reading and renaming some columns
    raw = pandas.read_csv('cyto2func/standardised_cheeky.csv')
    raw = raw.rename(columns={'rrpu': 'decomp_flor'})
    raw = raw.rename(columns={'newstandard': 'rrpu'})

    data = GateData(raw)
    inverter_names = data.plasmids[3:]

    # Figure 1
    os.system(f"gnuplot '{fig_dir}/Figure1/figure.gp'")

    # Figure 2
    # this generates the comparison plot for ALL pairs of gates. The
    # produced files weigh quite a lot. But you could also get rid of
    # the for loops and do:
    # figures.figure2(data[::<GATE_NAME>], data[::<OTHER_NAME>], fig_dir + '/Figure2')
    # obviously replacing the names between <>
    for a in inverter_names:
        for b in inverter_names:
            figures.figure2(data[::a], data[::b], fig_dir + '/Figure2')

    os.system(f"gnuplot '{fig_dir}/Figure2/figure.gp'")

    # Figure 3
    for a in inverter_names:
        figures.figure3d(data[::a], fig_dir + '/Figure3/D')

    gs = filter_valid(data['DH5alpha':'pAN':])
    figures.figure3bc(gs, fig_dir + '/Figure3/B', 'DH5alpha_+_pAN_Context')
    gs = filter_valid(data['DH5alpha'::])
    figures.figure3bc(gs, fig_dir + '/Figure3/B', 'DH5alpha_Strain')
    gs = filter_valid(data[::])
    figures.figure3bc(gs, fig_dir + '/Figure3/C', 'All_Strains')

    os.system(f"gnuplot '{fig_dir}/Figure3/figure.gp'")

    # Figure 4
    os.system(f"gnuplot '{fig_dir}/Figure4/panelI.gp'")
    os.system(f"gnuplot '{fig_dir}/Figure4/panelII.gp'")
    os.system(f"gnuplot '{fig_dir}/Figure4/panelIII.gp'")
