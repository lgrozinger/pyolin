reset session
set term postscript eps enhanced color

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
    
set output 'notebooks/results/figure_data/Figure3/D/Psra_r1_similarity_map.eps'
set title 'Inter-context Similarity Scores for Psra R1' font 'Computer Modern Roman,32'
unset key
set datafile separator comma
plot 'notebooks/results/figure_data/Figure3/D/similarity_matrix_Psra_r1.dat' matrix rowheaders columnheaders using 1:2:3 with image
set datafile separator
