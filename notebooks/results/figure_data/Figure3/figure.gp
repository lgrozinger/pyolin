reset session
set term postscript eps enhanced color size 18, 11.69
set output 'notebooks/results/figure_data/Figure3/figure.eps'

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
set style line 1 lt 7 lw 3 linecolor rgb '#00B341'
set style line 2 lt 1 lw 3 linecolor rgb '#00B341'

## BEGIN
set autoscale

set multiplot layout 3,4

## PANEL A
set lmargin at screen 0.05
set rmargin at screen 0.2
set tmargin at screen 1.0-0.05

set xlabel 'Input' offset 0,-2.5
set ylabel 'Output' offset -2,0

set format y "10^{%L}"
set format x "10^{%L}"
set xtics offset 0,-0.5

set logscale x
set logscale y

set tics nomirror

set title 'Litr L1'
set size ratio 1

plot \
     'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Litr_l1_scatter.dat' using 2:3 ls 1 notitle,\
     'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Litr_l1_curve.dat' using 1:2 w l ls 2 notitle, \
     [0.1:10] 3.93 w l dashtype 2 lc "red" lw 5 title 'OH', \
     [0.1:10] 0.66 w l dashtype 2 lc "blue" lw 5 title 'OL'


set xlabel 'Output' offset 0, -2.5
set ylabel 'Input' offset -2, 0

set lmargin at screen 0.2+0.05
set rmargin at screen 0.4

set title 'Amer F1'

plot \
     'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Amer_f1_scatter.dat' using 3:2 ls 1 notitle, \
     'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Amer_f1_curve.dat' using 2:1 w l ls 2 notitle, \
     [0.1:10.0] 1.37 w l dashtype 2 lc "red" lw 5 title 'IH', \
     [0.1:10.0] 0.87 w l dashtype 2 lc "blue" lw 5 title 'IL'

unset logscale x
unset logscale y


## PANEL B
load 'notebooks/results/figure_data/Figure3/compat_map_style.gp'

set lmargin at screen 0.4+0.1
set rmargin at screen 0.75
set bmargin at screen 0.65


set datafile separator comma

set xlabel 'Input Gate' offset 0, -4.5
set ylabel 'Output Gate' offset -5
unset colorbox
set title 'Any Backbone'
plot \
     'notebooks/results/figure_data/Figure3/B/compat_matrix_DH5alpha_Strain.dat' matrix rowheaders columnheaders using 1:2:3 with image notitle

set ylabel ''
set colorbox
set lmargin at screen 0.75

set title 'pAN Only'
plot 'notebooks/results/figure_data/Figure3/B/compat_matrix_DH5alpha_+_pAN_Context.dat' matrix rowheaders columnheaders using 1:2:3 with image notitle


# ## FORMULA IMG
# set lmargin 0.075
# set rmargin 0.075+0.175+0.05+0.175
# set bmargin 0.6
# set tmargin 0.7
# set size ratio -1
# unset key
# unset xlabel
# unset ylabel
# unset title
# unset tics
# plot 'formula.png' binary filetype=png with rgbimage notitle


## PANEL C
set multiplot next
set multiplot next

set bmargin at screen 0.1
set lmargin at screen 0.1
set rmargin at screen 0.5
set tmargin at screen 0.5
set ylabel 'Output Gate' offset -7

set xlabel 'Input Gate' offset 0, -4
set title ''
plot 'notebooks/results/figure_data/Figure3/C/compat_matrix_All_Strains.dat' matrix rowheaders columnheaders using 1:2:3 with image notitle


## PANEL D
set palette maxcolors 256
set cblabel ''
set cbtics format '%.1f'

set lmargin at screen 0.5+0.1
set rmargin at screen 1.0
set bmargin at screen 0.1
set tmargin at screen 0.5
unset xlabel
unset ylabel
set title ''
plot 'notebooks/results/figure_data/Figure3/D/similarity_matrix_Phif_p1.dat' matrix rowheaders columnheaders using 1:2:3 with image notitle


unset multiplot
