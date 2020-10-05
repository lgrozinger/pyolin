"""
(Re)produce the plots from the figures!
"""
from pyolin import FIGDIR
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
    inverter_names = data.gates[3:]

    # Figure 2
    # this generates the comparison plot for ALL pairs of gates. The
    # produced files weigh quite a lot. But you could also get rid of
    # the for loops and do:
    # figures.figure2(data[::<GATE_NAME>], data[::<OTHER_NAME>], fig_dir + '/Figure2')
    # obviously replacing the names between <>
    for a in inverter_names:
        for b in inverter_names:
            figures.figure2(data[::a], data[::b])

    os.system(f"gnuplot '{FIGDIR / 'Figure2'}/figure2_with_Psra_r1_vs_Phif_p2.gnuplot'")

    # Figure 1
    os.system(f"gnuplot {FIGDIR/'Figure1/figure.gp'}")

    # Figure 3
    for a in inverter_names:
        figures.similaritymap(data[::a], FIGDIR / 'Figure3/B')
    os.system(f"gnuplot {FIGDIR / 'Figure3/B/similarity_matrix_Phif_p1.gnuplot'}")
    
    gates = filter_valid(data['DH5alpha':'pAN':])
    figures.compatmap(gates, 'DH5alpha_+_pAN_Context', FIGDIR / 'Figure3/C')
    gates = filter_valid(data['DH5alpha'::])
    figures.compatmap(gates, 'DH5alpha_Strain', FIGDIR / 'Figure3/C')
    gates = filter_valid(data[::])
    figures.compatmap(gates, 'All_Strains', FIGDIR / 'Figure3/C')
    os.system(f"gnuplot {FIGDIR/'Figure3/C/compat_map_DH5alpha_+_pAN_Context.gnuplot'}")
    os.system(f"gnuplot {FIGDIR/'Figure3/C/compat_map_DH5alpha_Strain.gnuplot'}")
    os.system(f"gnuplot {FIGDIR/'Figure3/C/compat_map_All_Strains.gnuplot'}")

    # Figure 4
    os.system(f"gnuplot '{FIGDIR}/Figure4/panelI.gp'")
    os.system(f"gnuplot '{FIGDIR}/Figure4/panelII.gp'")
    os.system(f"gnuplot '{FIGDIR}/Figure4/panelIII.gp'")

    # Supplementary
    # S2
    for strain in data.strains:
        figures.compatmap(data[strain::], f"{strain}_Strain", FIGDIR/'SuppFigure2')
        os.system(f"gnuplot {FIGDIR}/SuppFigure2/compat_map_{strain}_Strain.gnuplot")

    # S3
    for s, b in data.contexts:
        figures.compatmap(data[s:b:], f"{b}_in_{s}", FIGDIR/'SuppFigure3')
        os.system(f"gnuplot {FIGDIR}/SuppFigure3/compat_map_{b}_in_{s}.gnuplot")

    # S4
    for inverter in inverter_names:
        figures.similaritymap(data[::inverter], FIGDIR/'SuppFigure4')
        os.system(f"gnuplot {FIGDIR}/SuppFigure4/similarity_matrix_{inverter}.gnuplot")
