"""
(Re)produce the plots from the figures!
"""
import pyolin.figures as figures

import pandas
import os
import sys
from shutil import which

from pyolin.dataframe import GateData
from pyolin.analysis import filter_valid

fig_dir = 'notebooks/results/figure_data'


def plot_system_call(filepath, *gnuplotargs):
    minus_extension = filepath.rpartition('.')[0]
    directory = filepath.rpartition('/')[0]
    os.system(f"gnuplot -c {filepath} {' '.join(gnuplotargs)}")
    os.system(f"latex -output-directory={directory} {minus_extension}.tex")
    os.system(f"dvips -E -o {minus_extension}.ps {minus_extension}.dvi")

    
if __name__ == '__main__':
    # check the required utilities are available
    gnuplot = which("gnuplot")
    latex = which("latex")
    dvips = which("dvips")
    if latex is None or gnuplot is None or dvips is None:
        print("ERR: Plotting requires gnuplot, latex and dvips are installed.")
        sys.exit(1)

    convert = which("convert")
    if convert is None:
        print("WARN: convert not found, skipping conversion to png.")

    # reading and renaming some columns
    raw = pandas.read_csv('cyto2func/standardised_cheeky.csv')
    raw = raw.rename(columns={'rrpu': 'decomp_flor'})
    raw = raw.rename(columns={'newstandard': 'rrpu'})

    data = GateData(raw)
    inverter_names = data.plasmids[3:]

    # generate the data files
    if len(sys.argv) > 1 and sys.argv[1] == 'full-update':
        # this generates the comparison plot for ALL pairs of
        # gates. The produced files weigh quite a lot. But you could
        # also get rid of the for loops and do:
        # figures.figure2(data[::<GATE>], data[::<OTHER>], fig_dir +
        # '/Figure2')
        for a in inverter_names:
            for b in inverter_names:
                figures.figure2(data[::a], data[::b], fig_dir + '/Figure2')

        for a in inverter_names:
            figures.figure3d(data[::a], fig_dir + '/Figure3/D')

        gs = filter_valid(data['DH5alpha':'pAN':])
        figures.figure3bc(gs, fig_dir + '/Figure3/B', 'DH5alpha_+_pAN_Context')
        gs = filter_valid(data['DH5alpha'::])
        figures.figure3bc(gs, fig_dir + '/Figure3/B', 'DH5alpha_Strain')
        gs = filter_valid(data[::])
        figures.figure3bc(gs, fig_dir + '/Figure3/C', 'All_Strains')

        figures.figure5(data,
                        data['CC118Lpir':'pSeva221':'Amtr_a1'],
                        data['DH5alpha':'pSeva221':'Amtr_a1'],
                        f"{fig_dir}/Figure5")

        figures.figureS1(data, f"{fig_dir}/FigureS2")
        figures.figureS3(data, f"{fig_dir}/FigureS3")
        figures.figureS4(data, f"{fig_dir}/FigureS4")

    # Figure 1
    os.system(f"gnuplot '{fig_dir}/Figure1/figure.gp'")

    # Figure 2
    plot_system_call(f"{fig_dir}/Figure2/figure.gp", 'Litr_l1', 'Phif_p2')

    # Figure 3
    plot_system_call(f"{fig_dir}/Figure3/figure.gp")

    # Figure 4
    os.system(f"gnuplot '{fig_dir}/Figure4/panelI.gp'")
    os.system(f"gnuplot '{fig_dir}/Figure4/panelII.gp'")
    os.system(f"gnuplot '{fig_dir}/Figure4/panelIII.gp'")

    # Figure 5

    # SUPPLEMENTARY
    for strain in data.strains:
        outdir = f"{fig_dir}/FigureS2/"
        outprefix = f"{outdir}/figureS2_{strain}"
        os.system(f"gnuplot -c {outdir}/figureS2.gp {strain}")
        os.system(f"latex -output-directory={outdir} {outprefix}.tex")
        os.system(f"dvips -E -o {outprefix}.ps {outprefix}.dvi")
        if convert is not None:
            os.system(f"convert -density 400 {outprefix}.ps {outprefix}.png")

    for name in inverter_names:
        outdir = f"{fig_dir}/FigureS3/"
        outprefix = f"{outdir}/figureS3_{name}"
        os.system(f"gnuplot -c {outdir}/figureS3.gp {name}")
        os.system(f"latex -output-directory={outdir} {outprefix}.tex")
        os.system(f"dvips -E -o {outprefix}.ps {outprefix}.dvi")
        if convert is not None:
            os.system(f"convert -density 400 {outprefix}.ps {outprefix}.png")

    for strain, backbone in data.contexts:
        outdir = f"{fig_dir}/FigureS4/"
        outprefix = f"{outdir}/figureS4_{strain}_{backbone}"
        os.system(f"gnuplot -c {outdir}/figureS4.gp {strain} {backbone}")
        os.system(f"latex -output-directory={outdir} {outprefix}.tex")
        os.system(f"dvips -E -o {outprefix}.ps {outprefix}.dvi")
        if convert is not None:
            os.system(f"convert -density 400 {outprefix}.ps {outprefix}.png")
