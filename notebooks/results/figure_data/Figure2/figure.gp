reset session
set term postscript eps enhanced color size 18, 9
set output 'figures/Figure2/figure.eps'

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
set style line 1 lt 7 lw 10linecolor rgb '#00B341'
set style line 2 lt 7 ps 2 linecolor rgb '#00B341'
set style line 3 lt 7 lw 10 linecolor rgb '#D00050'
set style line 4 lt 7 ps 2 linecolor rgb '#D00050'

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

set format y "$10^{%L}$"
set format x "$10^{%L}$"

set ylabel '{\Large Output}'

set tmargin at screen 1-0.05
set bmargin at screen 0.55
set lmargin at screen 0.05+0.25

datadir='notebooks/results/figure_data/Figure2/'
gate1=ARG1
gate2=ARG2

set title '{\huge DH5alpha pAN}'
plot \
     'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Psra_r1_scatter.dat' using 2:3 ls 2 notitle,\
     'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Psra_r1_curve.dat' using 1:2 w l ls 1 title 'Psra R1', \
     'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Phif_p2_scatter.dat' using 2:3 ls 4 notitle,\
     'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Phif_p2_curve.dat' using 1:2 w l ls 3 title 'Phif P2'

set ylabel ''

set lmargin at screen 0.05+0.25+0.25
set title '{\huge DH5alpha pSeva221}'
plot \
     'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Psra_r1_scatter.dat' using 2:3 ls 2 notitle,\
     'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Psra_r1_curve.dat' using 1:2 w l ls 1 notitle, \
     'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Phif_p2_scatter.dat' using 2:3 ls 4 notitle,\
     'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Phif_p2_curve.dat' using 1:2 w l ls 3 notitle

set lmargin at screen 0.05+0.25+0.25+0.25
set title '{\huge CC118Lpir pSeva221}'
plot \
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Psra_r1_scatter.dat' using 2:3 ls 2 notitle,\
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Psra_r1_curve.dat' using 1:2 w l ls 1 notitle, \
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Phif_p2_scatter.dat' using 2:3 ls 4 notitle,\
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Phif_p2_curve.dat' using 1:2 w l ls 3 notitle

set xlabel '{\Large Input}'
set ylabel '{\Large Output}' offset 2

set tmargin at screen 0.5
set bmargin at screen 0.1
set lmargin at screen 0.05

set title '{\huge CC118Lpir pSeva231}'
plot \
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva231_Psra_r1_scatter.dat' using 2:3 ls 2 notitle,\
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva231_Psra_r1_curve.dat' using 1:2 w l ls 1 notitle, \
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva231_Phif_p2_scatter.dat' using 2:3 ls 4 notitle,\
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva231_Phif_p2_curve.dat' using 1:2 w l ls 3 notitle

set ylabel ''
set lmargin at screen 0.05+0.25

set title '{\huge KT2440 pSeva231}'
plot \
     'notebooks/results/figure_data/Figure2/KT2440_pSeva231_Psra_r1_scatter.dat' using 2:3 ls 2 notitle,\
     'notebooks/results/figure_data/Figure2/KT2440_pSeva231_Psra_r1_curve.dat' using 1:2 w l ls 1 notitle, \
     'notebooks/results/figure_data/Figure2/KT2440_pSeva231_Phif_p2_scatter.dat' using 2:3 ls 4 notitle,\
     'notebooks/results/figure_data/Figure2/KT2440_pSeva231_Phif_p2_curve.dat' using 1:2 w l ls 3 notitle

set lmargin at screen 0.05+0.25+0.25
set title '{\huge KT2440 pSeva221}'
plot \
     'notebooks/results/figure_data/Figure2/KT2440_pSeva221_Psra_r1_scatter.dat' using 2:3 ls 2 notitle,\
     'notebooks/results/figure_data/Figure2/KT2440_pSeva221_Psra_r1_curve.dat' using 1:2 w l ls 1 notitle, \
     'notebooks/results/figure_data/Figure2/KT2440_pSeva221_Phif_p2_scatter.dat' using 2:3 ls 4 notitle,\
     'notebooks/results/figure_data/Figure2/KT2440_pSeva221_Phif_p2_curve.dat' using 1:2 w l ls 3 notitle

set lmargin at screen 0.05+0.25+0.25+0.25
set title '{\huge KT2440 pSeva251}'
plot \
     'notebooks/results/figure_data/Figure2/KT2440_pSeva251_Psra_r1_scatter.dat' using 2:3 ls 2 notitle,\
     'notebooks/results/figure_data/Figure2/KT2440_pSeva251_Psra_r1_curve.dat' using 1:2 w l ls 1 notitle, \
     'notebooks/results/figure_data/Figure2/KT2440_pSeva251_Phif_p2_scatter.dat' using 2:3 ls 4 notitle,\
     'notebooks/results/figure_data/Figure2/KT2440_pSeva251_Phif_p2_curve.dat' using 1:2 w l ls 3 notitle

