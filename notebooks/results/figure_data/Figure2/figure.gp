reset session
set term postscript eps enhanced color size 18, 9
set output 'notebooks/results/figure_data/Figure2/figure.eps'

# font sizes
set font 'Computer Modern Roman,8'
set tics font ',24'
set title font ',32'
set label font ',28'
set xlabel font ',28'
set ylabel font ',28'
set cblabel font ',28'
set key font ',24'

# line styles
set style line 1 lt 7 lw 15 linecolor rgb '#00B341'
set style line 2 lt 7 ps 3 linecolor rgb '#00B341'
set style line 3 lt 7 lw 15 linecolor rgb '#D00050'
set style line 4 lt 7 ps 3 linecolor rgb '#D00050'

## BEGIN
set autoscale

set datafile separator whitespace

set multiplot layout 4, 4

set logscale x
set logscale y

set tics out nomirror scale 1, 0
set title ''

set size ratio 1

set multiplot next

set format y "10^{%L}"
set format x "10^{%L}"

set ylabel 'Output' offset -5

set tmargin at screen 1-0.05
set bmargin at screen 0.55
set lmargin at screen 0.05+0.25


set title 'DH5alpha pAN'
plot \
     'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Litr_l1_scatter.dat' using 2:3 ls 2 notitle,\
     'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Litr_l1_curve.dat' using 1:2 w l ls 1 title 'Psra R1', \
     'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Phif_p2_scatter.dat' using 2:3 ls 4 notitle,\
     'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Phif_p2_curve.dat' using 1:2 w l ls 3 title 'Phif P2'

set ylabel ''

set lmargin at screen 0.05+0.25+0.25
set title 'DH5alpha pSeva221'
plot \
     'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Litr_l1_scatter.dat' using 2:3 ls 2 notitle,\
     'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Litr_l1_curve.dat' using 1:2 w l ls 1 notitle, \
     'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Phif_p2_scatter.dat' using 2:3 ls 4 notitle,\
     'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Phif_p2_curve.dat' using 1:2 w l ls 3 notitle

set lmargin at screen 0.05+0.25+0.25+0.25
set title 'CC118Lpir pSeva221'
plot \
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Litr_l1_scatter.dat' using 2:3 ls 2 notitle,\
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Litr_l1_curve.dat' using 1:2 w l ls 1 notitle, \
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Phif_p2_scatter.dat' using 2:3 ls 4 notitle,\
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Phif_p2_curve.dat' using 1:2 w l ls 3 notitle

set xlabel 'Input' offset 0, -3
set ylabel 'Output' offset -5

set tmargin at screen 0.5
set bmargin at screen 0.1
set lmargin at screen 0.05

set title 'CC118Lpir pSeva231'
plot \
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva231_Litr_l1_scatter.dat' using 2:3 ls 2 notitle,\
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva231_Litr_l1_curve.dat' using 1:2 w l ls 1 notitle, \
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva231_Phif_p2_scatter.dat' using 2:3 ls 4 notitle,\
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva231_Phif_p2_curve.dat' using 1:2 w l ls 3 notitle

set ylabel ''
set lmargin at screen 0.05+0.25

set title 'KT2440 pSeva231'
plot \
     'notebooks/results/figure_data/Figure2/KT2440_pSeva231_Litr_l1_scatter.dat' using 2:3 ls 2 notitle,\
     'notebooks/results/figure_data/Figure2/KT2440_pSeva231_Litr_l1_curve.dat' using 1:2 w l ls 1 notitle, \
     'notebooks/results/figure_data/Figure2/KT2440_pSeva231_Phif_p2_scatter.dat' using 2:3 ls 4 notitle,\
     'notebooks/results/figure_data/Figure2/KT2440_pSeva231_Phif_p2_curve.dat' using 1:2 w l ls 3 notitle

set lmargin at screen 0.05+0.25+0.25
set title 'KT2440 pSeva221'
plot \
     'notebooks/results/figure_data/Figure2/KT2440_pSeva221_Litr_l1_scatter.dat' using 2:3 ls 2 notitle,\
     'notebooks/results/figure_data/Figure2/KT2440_pSeva221_Litr_l1_curve.dat' using 1:2 w l ls 1 notitle, \
     'notebooks/results/figure_data/Figure2/KT2440_pSeva221_Phif_p2_scatter.dat' using 2:3 ls 4 notitle,\
     'notebooks/results/figure_data/Figure2/KT2440_pSeva221_Phif_p2_curve.dat' using 1:2 w l ls 3 notitle

set lmargin at screen 0.05+0.25+0.25+0.25
set title 'KT2440 pSeva251'
plot \
     'notebooks/results/figure_data/Figure2/KT2440_pSeva251_Litr_l1_scatter.dat' using 2:3 ls 2 notitle,\
     'notebooks/results/figure_data/Figure2/KT2440_pSeva251_Litr_l1_curve.dat' using 1:2 w l ls 1 notitle, \
     'notebooks/results/figure_data/Figure2/KT2440_pSeva251_Phif_p2_scatter.dat' using 2:3 ls 4 notitle,\
     'notebooks/results/figure_data/Figure2/KT2440_pSeva251_Phif_p2_curve.dat' using 1:2 w l ls 3 notitle

