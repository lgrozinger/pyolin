reset session
home='notebooks/results/figure_data/FigureS4/'
set term epslatex color size 4, 3.5 font ',10' standalone
#set term epslatex color size 4.135, 4.135 font ',10'
set output home.'figureS4_'.ARG1.'_'.ARG2.'.tex'

load 'notebooks/results/figure_data/Figure3/compat_map_style.gp'
set datafile separator comma

set palette maxcolors 256
set cblabel ''
set cbtics format '{\large %.1f}'
set cbtics offset 1

set size ratio 1
unset xlabel
unset ylabel
set bmargin at screen 0.2
set lmargin at screen 0.1
prefix=home.'score_matrix_'

# set title '{\huge Compatibility Scores for '.ARG1.' '.ARG2.'}'
plot prefix.ARG1.'_'.ARG2.'.dat' matrix rowheaders columnheaders using 1:2:3 with image notitle

