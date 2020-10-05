reset session
set term epslatex color size 18, 11.69 font ',10' standalone
set output 'notebooks/results/figure_data/Figure3/figure.tex'
# set term pngcairo enhanced color size 1800, 1169
# set output 'notebooks/results/figure_data/Figure3/figure.png'

# font sizes
set font 'Computer Modern Roman,20'
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
set label 2 at screen 0.02, 0.98 '{\Huge A}'
set lmargin at screen 0.05
set rmargin at screen 0.2
set tmargin at screen 1.0-0.05

set xlabel '{\Large Input}' 
set ylabel '{\Large Output}'

set format y "$10^{%L}$"
set format x "$10^{%L}$"
set xtics offset 0,-0.5

set logscale x
set logscale y

set tics nomirror

set title '{\huge Litr L1}'
set size ratio 1

plot \
     'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Litr_l1_scatter.dat' using 2:3 ls 1 notitle,\
     'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Litr_l1_curve.dat' using 1:2 w l ls 2 notitle, \
     [0.1:10] 3.93 w l dashtype 2 lc "red" lw 5 title 'OH', \
     [0.1:10] 0.66 w l dashtype 2 lc "blue" lw 5 title 'OL'


set xlabel '{\Large Output}' 
set ylabel '{\Large Input}'

set lmargin at screen 0.2+0.05
set rmargin at screen 0.4

set title '{\huge Amer F1}'
set xrange [1.0:10.0]

plot \
     'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Amer_f1_scatter.dat' using 3:2 ls 1 notitle, \
     'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Amer_f1_curve.dat' using 2:1 w l ls 2 notitle, \
     [0.1:10.0] 1.37 w l dashtype 2 lc "red" lw 5 title 'IH', \
     [0.1:10.0] 0.87 w l dashtype 2 lc "blue" lw 5 title 'IL'

unset logscale x
unset logscale y
unset xrange


## PANEL B
load 'notebooks/results/figure_data/Figure3/compat_map_style.gp'
set label 3 at screen 0.47, 0.98 '{\Huge B}'
set lmargin at screen 0.4+0.1
set rmargin at screen 0.75
set bmargin at screen 0.65


set datafile separator comma

set xlabel '{\Large Input Gate}'
set ylabel '{\Large Output Gate}'
unset colorbox
set title '{\huge Any Backbone}'
plot \
     'notebooks/results/figure_data/Figure3/B/compat_matrix_DH5alpha_Strain.dat' matrix rowheaders columnheaders using 1:2:3 with image notitle

set ylabel ''
set colorbox
set lmargin at screen 0.75

set title '{\huge pAN Only}'
plot 'notebooks/results/figure_data/Figure3/B/compat_matrix_DH5alpha_+_pAN_Context.dat' matrix rowheaders columnheaders using 1:2:3 with image notitle


## formula
set label 1 at screen 0.23, screen 0.6 '{\huge $\textrm{Score} = min \left( ln \left( \frac{IL_B}{OL_A} \right) \; , ln \left(\frac{OH_A}{IH_B} \right) \right)$}'

## PANEL C
set multiplot next
set multiplot next

set label 4 at screen 0.07, 0.53 '{\Huge C}'
set bmargin at screen 0.1
set lmargin at screen 0.1
set rmargin at screen 0.5
set tmargin at screen 0.5
set ylabel '{\Large Output Gate}'

set xlabel '{\Large Input Gate}'
set title ''
plot 'notebooks/results/figure_data/Figure3/C/compat_matrix_All_Strains.dat' matrix rowheaders columnheaders using 1:2:3 with image notitle


## PANEL D
set palette maxcolors 256
set cblabel ''
set cbtics format '%.1f'

set label 5 at screen 0.57, 0.53 '{\Huge D}'
set lmargin at screen 0.5+0.1
set rmargin at screen 1.0
set bmargin at screen 0.1
set tmargin at screen 0.5
unset xlabel
unset ylabel
set title ''
plot 'notebooks/results/figure_data/Figure3/D/similarity_matrix_Phif_p1.dat' matrix rowheaders columnheaders using 1:2:3 with image notitle


unset multiplot
