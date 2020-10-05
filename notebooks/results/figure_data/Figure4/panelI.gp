reset session
set term postscript eps enhanced dashed color size 11.0, 3.0
set output 'notebooks/results/figure_data/Figure4/panelI_gates.eps'

set autoscale

set xlabel 'Input'  font 'Computer Modern Roman,24'
set ylabel 'Output' font 'Computer Modern Roman,24'

set xtics font 'Computer Modern Roman,20'
set ytics font 'Computer Modern Roman,20'

set logscale x
set logscale y

set style line 1 lt 7 linecolor rgb '#00B341'
set style line 2 lt 1 lw 5 linecolor rgb '#00B341'

set style line 3 lt 7 linecolor rgb '#00B341'
set style line 4 lt 1 lw 5 linecolor rgb '#00B341'

set bmargin at screen 0.15

set datafile separator whitespace

set multiplot layout 1, 3

set logscale x
set logscale y

set tics out nomirror scale 1, 0
set title font 'Computer Modern Roman,28'

set size ratio 1

set multiplot next

set format y "10^{%L}"
set format x "10^{%L}"

set ylabel 'Output' offset -5

set title 'Psra R1'
set lmargin at screen 0.1
plot \
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Psra_r1_scatter.dat' using 2:3 ls 1 ps 2 notitle,\
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Psra_r1_curve.dat' using 1:2 w l ls 1 lw 10 notitle

set title 'Phif P3'
set ytics format ""
set lmargin at screen 0.1+0.3
unset ylabel
plot \
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Phif_p3_scatter.dat' using 2:3 ls 1 ps 2 notitle,\
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Phif_p3_curve.dat' using 1:2 w l ls 1 lw 10 notitle

set title 'Amer F1'
set lmargin at screen 0.1+0.3*2
plot \
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Amer_f1_scatter.dat' using 2:3 ls 1 ps 2 notitle,\
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Amer_f1_curve.dat' using 1:2 w l ls 1 lw 10 notitle

