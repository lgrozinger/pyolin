reset session
set term postscript eps enhanced color size 5, 2.7

set autoscale

set xtics 1 font 'Computer Modern Roman,10' rotate out nomirror
set ytics 1 font 'Computer Modern Roman,10' out nomirror

set cbtics format ''
set cblabel 'Not Compatible      Compatible' font 'Computer Modern Roman,14' rotate offset 0, -0.65
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

set tmargin at screen 0.95
set bmargin at screen 0.3

load '~/src/gnuplot/gnuplot-palettes/blues.pal'

set xlabel 'Input Gate' font 'Computer Modern Roman,16'
    
set output '/home/campus.ncl.ac.uk/b8051106/my/src/python/pyolin/notebooks/results/figure_data/Figure3/B/panelB.eps'

set multiplot layout 1,2 title 'Compatibility Table for DH5alpha Strain' font 'Computer Modern Roman,28'

set ylabel 'Ouput Gate' font 'Computer Modern Roman,16'
set title 'Any Backbone' font 'Computer Modern Roman,18'
unset key
unset colorbox
set lmargin at screen 0.17

set datafile separator comma
plot '/home/campus.ncl.ac.uk/b8051106/my/src/python/pyolin/notebooks/results/figure_data/Figure3/B/compat_matrix_DH5alpha_Strain.dat' matrix rowheaders columnheaders using 1:2:3 with image

unset ylabel

set colorbox
set lmargin at screen 0.6
set title 'pSeva221 Only' font 'Computer Modern Roman,18'
plot '/home/campus.ncl.ac.uk/b8051106/my/src/python/pyolin/notebooks/results/figure_data/Figure3/B/compat_matrix_DH5alpha_+_pAN_Context.dat' matrix rowheaders columnheaders using 1:2:3 with image


set datafile separator

