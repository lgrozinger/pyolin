reset session
home='notebooks/results/figure_data/FigureS2/'
set term epslatex color size 4, 3.5 font ',10' standalone
# set term epslatex color size 4, 3.5

set output home.'figureS2_'.ARG1.'.tex'

load 'notebooks/results/figure_data/Figure3/compat_map_style.gp'
set datafile separator comma

set cblabel 'Not Compatible \hspace{0.6cm} Compatible' rotate offset 1, -0.7

set size ratio 1
set ylabel '{\Large Output Gate}'
set xlabel '{\Large Input Gate}'

set bmargin at screen 0.2
set lmargin at screen 0.2

plot home.'/compat_matrix_'.ARG1.'_Strain.dat' matrix rowheaders columnheaders using 1:2:3 with image notitle
