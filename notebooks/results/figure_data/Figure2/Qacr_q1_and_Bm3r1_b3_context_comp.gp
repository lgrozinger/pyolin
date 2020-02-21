reset session
set term postscript eps enhanced color

set autoscale

set lmargin at screen 0.15
set bmargin at screen 0.15

set xlabel 'RPU input' offset 0,-1.5,0 font 'Computer Modern Roman,24'
set ylabel 'RPU output' offset -2,0,0 font 'Computer Modern Roman,24'

set xtics offset 0,-0.75 font 'Computer Modern Roman,16'
set ytics font 'Computer Modern Roman,16'

set logscale x
set logscale y

set style line 1 lt 7 linecolor rgb '#00B341'
set style line 2 lt 1 lw 5 linecolor rgb '#00B341'

set style line 3 lt 7 linecolor rgb '#D00050'
set style line 4 lt 1 lw 5 linecolor rgb '#D00050'
    
set output 'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Qacr_q1_and_Bm3r1_b3.eps'
set title 'In host CC118Lpir, with backbone pSeva221' font 'Computer Modern Roman,32
set format y '10^{%L}'
set format x '10^{%L}'
plot \
'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Qacr_q1_scatter.dat' using 2:3 ls 1 notitle, \
'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Qacr_q1_curve.dat' using 1:2 w l ls 2 notitle, \
'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Bm3r1_b3_scatter.dat' using 2:3 ls 3 notitle, \
'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Bm3r1_b3_curve.dat' using 1:2 w l ls 4 notitle
set output 'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva231_Qacr_q1_and_Bm3r1_b3.eps'
set title 'In host CC118Lpir, with backbone pSeva231' font 'Computer Modern Roman,32
set format y '10^{%L}'
set format x '10^{%L}'
plot \
'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva231_Qacr_q1_scatter.dat' using 2:3 ls 1 notitle, \
'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva231_Qacr_q1_curve.dat' using 1:2 w l ls 2 notitle, \
'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva231_Bm3r1_b3_scatter.dat' using 2:3 ls 3 notitle, \
'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva231_Bm3r1_b3_curve.dat' using 1:2 w l ls 4 notitle
set output 'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Qacr_q1_and_Bm3r1_b3.eps'
set title 'In host DH5alpha, with backbone pAN' font 'Computer Modern Roman,32
set format y '10^{%L}'
set format x '10^{%L}'
plot \
'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Qacr_q1_scatter.dat' using 2:3 ls 1 notitle, \
'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Qacr_q1_curve.dat' using 1:2 w l ls 2 notitle, \
'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Bm3r1_b3_scatter.dat' using 2:3 ls 3 notitle, \
'notebooks/results/figure_data/Figure2/DH5alpha_pAN_Bm3r1_b3_curve.dat' using 1:2 w l ls 4 notitle
set output 'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Qacr_q1_and_Bm3r1_b3.eps'
set title 'In host DH5alpha, with backbone pSeva221' font 'Computer Modern Roman,32
set format y '10^{%L}'
set format x '10^{%L}'
plot \
'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Qacr_q1_scatter.dat' using 2:3 ls 1 notitle, \
'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Qacr_q1_curve.dat' using 1:2 w l ls 2 notitle, \
'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Bm3r1_b3_scatter.dat' using 2:3 ls 3 notitle, \
'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Bm3r1_b3_curve.dat' using 1:2 w l ls 4 notitle
set output 'notebooks/results/figure_data/Figure2/KT2440_pSeva221_Qacr_q1_and_Bm3r1_b3.eps'
set title 'In host KT2440, with backbone pSeva221' font 'Computer Modern Roman,32
set format y '10^{%L}'
set format x '10^{%L}'
plot \
'notebooks/results/figure_data/Figure2/KT2440_pSeva221_Qacr_q1_scatter.dat' using 2:3 ls 1 notitle, \
'notebooks/results/figure_data/Figure2/KT2440_pSeva221_Qacr_q1_curve.dat' using 1:2 w l ls 2 notitle, \
'notebooks/results/figure_data/Figure2/KT2440_pSeva221_Bm3r1_b3_scatter.dat' using 2:3 ls 3 notitle, \
'notebooks/results/figure_data/Figure2/KT2440_pSeva221_Bm3r1_b3_curve.dat' using 1:2 w l ls 4 notitle
set output 'notebooks/results/figure_data/Figure2/KT2440_pSeva231_Qacr_q1_and_Bm3r1_b3.eps'
set title 'In host KT2440, with backbone pSeva231' font 'Computer Modern Roman,32
set format y '10^{%L}'
set format x '10^{%L}'
plot \
'notebooks/results/figure_data/Figure2/KT2440_pSeva231_Qacr_q1_scatter.dat' using 2:3 ls 1 notitle, \
'notebooks/results/figure_data/Figure2/KT2440_pSeva231_Qacr_q1_curve.dat' using 1:2 w l ls 2 notitle, \
'notebooks/results/figure_data/Figure2/KT2440_pSeva231_Bm3r1_b3_scatter.dat' using 2:3 ls 3 notitle, \
'notebooks/results/figure_data/Figure2/KT2440_pSeva231_Bm3r1_b3_curve.dat' using 1:2 w l ls 4 notitle
set output 'notebooks/results/figure_data/Figure2/KT2440_pSeva251_Qacr_q1_and_Bm3r1_b3.eps'
set title 'In host KT2440, with backbone pSeva251' font 'Computer Modern Roman,32
set format y '10^{%L}'
set format x '10^{%L}'
plot \
'notebooks/results/figure_data/Figure2/KT2440_pSeva251_Qacr_q1_scatter.dat' using 2:3 ls 1 notitle, \
'notebooks/results/figure_data/Figure2/KT2440_pSeva251_Qacr_q1_curve.dat' using 1:2 w l ls 2 notitle, \
'notebooks/results/figure_data/Figure2/KT2440_pSeva251_Bm3r1_b3_scatter.dat' using 2:3 ls 3 notitle, \
'notebooks/results/figure_data/Figure2/KT2440_pSeva251_Bm3r1_b3_curve.dat' using 1:2 w l ls 4 notitle
