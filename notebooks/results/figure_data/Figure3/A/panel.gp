reset session
# set term postscript eps enhanced dashed color

set autoscale

set xlabel 'Input'  font 'Computer Modern Roman,18'
set ylabel 'Output' font 'Computer Modern Roman,18'

set xtics font 'Computer Modern Roman,16'
set ytics font 'Computer Modern Roman,16'

set logscale x
set logscale y

set style line 1 lt 7 linecolor rgb '#00B341'
set style line 2 lt 1 lw 5 linecolor rgb '#00B341'

set style line 3 lt 7 linecolor rgb '#00B341'
set style line 4 lt 1 lw 5 linecolor rgb '#00B341'

set bmargin at screen 0.2

#set output '/home/campus.ncl.ac.uk/b8051106/my/src/python/pyolin/notebooks/results/figure_data/Figure3/A/panelA.eps'

set multiplot layout 1,2 title 'Compatibility Scoring' font 'Computer Modern Roman,32
set format y '10^{%L}'
set format x '10^{%L}'

set lmargin at screen 0.1

set title 'Litr L1' font 'Computer Modern Roman,20'

plot \
     '/home/campus.ncl.ac.uk/b8051106/my/src/python/pyolin/notebooks/results/figure_data/Figure2/DH5alpha_pAN_Litr_l1_scatter.dat' using 2:3 ls 1 notitle, \
     '/home/campus.ncl.ac.uk/b8051106/my/src/python/pyolin/notebooks/results/figure_data/Figure2/DH5alpha_pAN_Litr_l1_curve.dat' using 1:2 w l ls 2 notitle, \
     [0.1:10] 3.93 w l dashtype 2 lc "red" lw 5 title 'OH', \
     [0.1:10] 0.66 w l dashtype 2 lc "blue" lw 5 title 'OL'

set lmargin at screen 0.5+0.1
set xlabel 'Output'  font 'Computer Modern Roman,18'
set ylabel 'Input' font 'Computer Modern Roman,18'

set title 'Amer F1' font 'Computer Modern Roman,20'

plot \
     '/home/campus.ncl.ac.uk/b8051106/my/src/python/pyolin/notebooks/results/figure_data/Figure2/DH5alpha_pAN_Amer_f1_scatter.dat' using 3:2 ls 3 notitle, \
     '/home/campus.ncl.ac.uk/b8051106/my/src/python/pyolin/notebooks/results/figure_data/Figure2/DH5alpha_pAN_Amer_f1_curve.dat' using 2:1 w l ls 4 notitle, \
     [0.1:10.0] 1.37 w l dashtype 2 lc "red" lw 5 title 'IH', \
     [0.1:10.0] 0.87 w l dashtype 2 lc "blue" lw 5 title 'IL'

set key font 'Computer Modern Roman'

unset multiplot