figure2_style = (
    """set term postscript eps enhanced color

set autoscale

set lmargin at screen 0.15
set bmargin at screen 0.15

set xlabel 'RPU input' offset 0,-1.5,0 font 'Computer Modern Roman,24'
set ylabel 'RPU output' offset -2,0,0 font 'Computer Modern Roman,24'

set xtics offset 0,-0.75 font 'Computer Modern Roman,16'
set ytics font 'Computer Modern Roman,16'

set logscale x
set logscale y

set style line 1 lt 7 linecolor rgb '#00B341'
set style line 2 lt 1 lw 5 linecolor rgb '#00B341'

set style line 3 lt 7 linecolor rgb '#D00050'
set style line 4 lt 1 lw 5 linecolor rgb '#D00050'
    """)


def figure2(gateA_list, gateB_list, directory):
    with open((f"{directory}/{gateA_list[0].cargo}_and_"
               f"{gateB_list[1].cargo}_context_comp.gp"), 'w') as f:

        print("reset session", file=f)
        print(figure2_style, file=f)

        for a, b in zip(gateA_list, gateB_list):
            assert a.backbone == b.backbone and a.strain == b.strain

            a_scatter, a_curve = a.to_gnuplot(directory)
            b_scatter, b_curve = b.to_gnuplot(directory)

            print(f"set output '{directory}/{a.strain}_{a.backbone}_{a.cargo}_and_{b.cargo}.eps'", file=f)

            print(f"set title 'In host {a.strain}, with backbone {a.backbone}' font 'Computer Modern Roman,32", file=f)

            print("set format y '10^{%L}'", file=f)
            print("set format x '10^{%L}'", file=f)

            print("plot \\", file=f)
            print(f"'{a_scatter}' using 2:3 ls 1 notitle, \\", file=f)
            print(f"'{a_curve}' using 1:2 w l ls 2 notitle, \\", file=f)

            print(f"'{b_scatter}' using 2:3 ls 3 notitle, \\", file=f)
            print(f"'{b_curve}' using 1:2 w l ls 4 notitle", file=f)

figure3d_style = (
    """set term postscript eps enhanced color

set autoscale

set lmargin at screen 0.25
set bmargin at screen 0.16

set xtics 1 offset 0,-4.5 font 'Computer Modern Roman,14' rotate by 90 out nomirror
set ytics 1 font 'Computer Modern Roman,14' out nomirror
set cbtics scale 0 font 'Computer Modern Roman,14'
set tics scale 0, 0.001

set size ratio 1

set x2tics 1 format ''
set y2tics 1 format ''
set mx2tics 2
set my2tics 2

set grid front mx2tics my2tics lw 1.5 lt -1 lc rgb 'white'

set link x
set link y

load '~/src/gnuplot/gnuplot-palettes/blues.pal'
    """)


import numpy

from pyolin.analysis import similarity_table


def gate_drop_name(gate_namestring):
    strain = gate_namestring.split('_')[0]
    backbone = gate_namestring.split('_')[1]
    return f"{strain}\\n{backbone}"


def gate_rename(gate_namestring):
    splut = gate_namestring.split('_')
    strain = splut[0]
    backbone = splut[1]
    cargo = splut[-2] + ' ' + splut[-1].upper()
    return f"{cargo} in {strain} with {backbone}"


def gate_drop_context(gate_namestring):
    splut = gate_namestring.split('_')
    return f"{splut[-2]} {splut[-1].upper()}"


def figure3d(gates, directory):
    assert len(set([gate.cargo for gate in gates])) == 1
    matrix_file = f"{directory}/similarity_matrix_{gates[0].cargo}.dat"
    scores = similarity_table(gates)
    scores = scores.rename(gate_drop_name, axis='index')
    scores = scores.rename(gate_drop_name, axis='columns')

    with open(matrix_file, 'w') as f:
        f.write(scores.to_csv())

    with open((f"{directory}/similarity_map_"
               f"{gates[0].cargo}.gp"),
              'w') as f:

        print("reset session", file=f)
        print(figure3d_style, file=f)

        print((f"set output '{directory}/{gates[0].cargo}"
               f"_similarity_map.eps'"),
              file=f)

        print((f"set title 'Inter-context Similarity Scores for "
               f"{gates[0].cargo.split('_')[0]} "
               f"{gates[0].cargo.split('_')[1].upper()}' "
               f"font 'Computer Modern Roman,32'"),
              file=f)

        print("unset key", file=f)

        print("set datafile separator comma", file=f)
        print((f"plot '{matrix_file}' matrix rowheaders columnheaders "
               f"using 1:2:3 with image"),
              file=f)
        print("set datafile separator", file=f)

    return scores


from pyolin.analysis import compatibility_table
from pyolin.analysis import reduced_compatibility_table


figure3bc_style = (
    """set term postscript eps enhanced color

set autoscale

set lmargin at screen 0.25
set bmargin at screen 0.25

set xtics 1 offset 0,-4 font 'Computer Modern Roman,14' rotate by 90 out nomirror
set ytics 1 font 'Computer Modern Roman,14' out nomirror

set cbtics ("Not Compatible" 0.25, "Compatible" 0.75) font 'Computer Modern Roman,16' rotate scale 0
set palette maxcolors 2

set tics scale 0, 0.001

set size ratio 1

set x2tics 1 format ''
set y2tics 1 format ''
set mx2tics 2
set my2tics 2

set grid front mx2tics my2tics lw 1.5 lt -1 lc rgb 'white'

set link x
set link y

set xlabel 'Input Gate' font 'Computer Modern Roman,18' offset 0, -5
set ylabel 'Ouput Gate' font 'Computer Modern Roman,18'


load '~/src/gnuplot/gnuplot-palettes/blues.pal'
    """)


def figure3bc(gates, directory, name):
    matrix_file = f"{directory}/compat_matrix_{name}.dat"
    scores = reduced_compatibility_table(gates)
    # scores = scores.rename(gate_drop_context, axis='index')
    # scores = scores.rename(gate_drop_context, axis='columns')

    with open(matrix_file, 'w') as f:
        f.write(scores.to_csv())

    with open(f"{directory}/compat_map_{name}.gp", 'w') as f:

        print("reset session", file=f)
        print(figure3bc_style, file=f)

        print((f"set output '{directory}/{name}"
               f"_compat_map.eps'"),
              file=f)

        print((f"set title 'Compatibility Table for "
               f"{name.replace('_', ' ')}' "
               f"font 'Computer Modern Roman,30'"),
              file=f)

        print("unset key", file=f)

        print("set datafile separator comma", file=f)
        print((f"plot '{matrix_file}' matrix rowheaders columnheaders "
               f"using 1:2:3 with image"),
              file=f)
        print("set datafile separator", file=f)

    return scores
