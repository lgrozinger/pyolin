reset session
set term postscript eps enhanced color

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
    
set output 'notebooks/results/figure_data/Figure3/B/DH5alpha_+_pAN_Context_compat_map.eps'
set title 'Compatibility Table for DH5alpha + pAN Context' font 'Computer Modern Roman,30'
unset key
set datafile separator comma
plot 'notebooks/results/figure_data/Figure3/B/compat_matrix_DH5alpha_+_pAN_Context.dat' matrix rowheaders columnheaders using 1:2:3 with image
set datafile separator
