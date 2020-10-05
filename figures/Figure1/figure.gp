set term postscript eps enhanced color size 4, 20 fontfile '/usr/share/texmf/fonts/type1/public/cm-super/sfrm1200.pfb' 'SFRM1200,14'
set output 'figures/Figure1/figure.eps'

# font sizes
set font ',8'
set tics font ',24'
set title font ',32'
set label font ',28'
set xlabel font ',28'
set ylabel font ',28'
set cblabel font ',28'
set key font ',24'

# line styles
set style line 1 lt 7 lw 15 linecolor rgb '#00B341'
set style line 2 lt 7 ps 3 linecolor rgb '#00B341'

## BEGIN
set autoscale

set datafile separator whitespace

set multiplot layout 7, 1

set logscale x
set logscale y

set tics out nomirror scale 1, 0
set title ''

set size ratio 1

set multiplot next

set format y "10^{%L}"
set format x "10^{%L}"

set ylabel 'RPU Output' offset -5
set xlabel 'RPU Input'
set lmargin at screen 0.25
set rmargin at screen 1-0.15

set title 'DH5alpha pAN'
plot \
     'figures/Figure2/DH5alpha_pAN_Qacr_q1_scatter.dat' using 2:3 ls 2 notitle,\
     'figures/Figure2/DH5alpha_pAN_Qacr_q1_curve.dat' using 1:2 w l ls 1 notitle

unset xlabel 
set title 'DH5alpha pSeva221'
plot \
     'figures/Figure2/DH5alpha_pSeva221_Qacr_q1_scatter.dat' using 2:3 ls 2 notitle,\
     'figures/Figure2/DH5alpha_pSeva221_Qacr_q1_curve.dat' using 1:2 w l ls 1 notitle

set title 'CC118Lpir pSeva221'
plot \
     'figures/Figure2/CC118Lpir_pSeva221_Qacr_q1_scatter.dat' using 2:3 ls 2 notitle,\
     'figures/Figure2/CC118Lpir_pSeva221_Qacr_q1_curve.dat' using 1:2 w l ls 1 notitle

set title 'CC118Lpir pSeva231'
plot \
     'figures/Figure2/CC118Lpir_pSeva231_Qacr_q1_scatter.dat' using 2:3 ls 2 notitle,\
     'figures/Figure2/CC118Lpir_pSeva231_Qacr_q1_curve.dat' using 1:2 w l ls 1 notitle

set title 'KT2440 pSeva231'
plot \
     'figures/Figure2/KT2440_pSeva231_Qacr_q1_scatter.dat' using 2:3 ls 2 notitle,\
     'figures/Figure2/KT2440_pSeva231_Qacr_q1_curve.dat' using 1:2 w l ls 1 notitle

set title 'KT2440 pSeva221'
plot \
     'figures/Figure2/KT2440_pSeva221_Qacr_q1_scatter.dat' using 2:3 ls 2 notitle,\
     'figures/Figure2/KT2440_pSeva221_Qacr_q1_curve.dat' using 1:2 w l ls 1 notitle


set title 'KT2440 pSeva251'
plot \
     'figures/Figure2/KT2440_pSeva251_Qacr_q1_scatter.dat' using 2:3 ls 2 notitle,\
     'figures/Figure2/KT2440_pSeva251_Qacr_q1_curve.dat' using 1:2 w l ls 1 notitle
