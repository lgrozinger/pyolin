reset session
set term postscript eps enhanced color size 3.5,5

set xtics 1 font 'Computer Modern Roman,10' rotate out nomirror
set ytics 1 font 'Computer Modern Roman,10' out nomirror

set cbtics format ''
set cblabel 'Not Compatible      Compatible' font 'Computer Modern Roman,14' rotate offset 0, -0.65
set palette maxcolors 2

set tics scale 0, 0.001

set lmargin at screen 0.3
#set rmargin at screen 1.0

set x2tics 1 format ''
set y2tics 1 format ''
set mx2tics 2
set my2tics 2

set grid front mx2tics my2tics lw 1.5 lt -1 lc rgb 'white'

unset xlabel

set link x
set link y

load '~/src/gnuplot/gnuplot-palettes/blues.pal'
    
set output '/home/campus.ncl.ac.uk/b8051106/my/src/python/pyolin/notebooks/results/figure_data/Figure3/C/panelC.eps'

set multiplot layout 2,1 title 'Compatibility Table for All Strains' font 'Computer Modern Roman,28'

set ylabel 'Ouput Gate' font 'Computer Modern Roman,16'
set title 'CC118Lpir Only' font 'Computer Modern Roman,18'

unset key

set bmargin at screen 0.6
set datafile separator comma

set size ratio 1
plot '/home/campus.ncl.ac.uk/b8051106/my/src/python/pyolin/notebooks/results/figure_data/Figure3/C/compat_matrix_CC118Lpir_Strain_Only.dat' matrix rowheaders columnheaders using 1:2:3 with image

set colorbox
set xlabel 'Input Gate' font 'Computer Modern Roman,16' offset 0,2
set title 'Any Host' font 'Computer Modern Roman,18'

set bmargin at screen 0.1175
set size ratio 1
plot '/home/campus.ncl.ac.uk/b8051106/my/src/python/pyolin/notebooks/results/figure_data/Figure3/C/compat_matrix_All_Strains.dat' matrix rowheaders columnheaders using 1:2:3 with image


set datafile separator

unset multiplot
