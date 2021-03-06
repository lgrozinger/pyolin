load 'notebooks/results/figure_data/Figure3/blues.pal'

set xtics 1 rotate out nomirror
set ytics 1 out nomirror

set cbtics format ''
set cblabel '{\Large Not Compatible \hspace{2cm} Compatible}' rotate offset 1, -0.7
set palette maxcolors 2

set tics scale 0, 0.001

set x2tics 1 format ''
set y2tics 1 format ''
set mx2tics 2
set my2tics 2

set grid front mx2tics my2tics lw 1.5 lt -1 lc rgb 'black'

set link x
set link y

set size ratio 1
