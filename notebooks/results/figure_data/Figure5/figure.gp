reset session
set term epslatex color size 12, 8 font ',10' standalone
set output 'notebooks/results/figure_data/Figure5/figure.tex'
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

set multiplot layout 2, 3

# set lmargin at screen 0.05
# set rmargin at screen 0.2
# set tmargin at screen 1.0-0.05
unset xlabel

set ylabel '{\Large Output}'

set format y "$10^{%L}$"
set format x "$10^{%L}$"
set xtics offset 0,-0.5

set logscale x
set logscale y

set tics nomirror

set title '{\huge Amer F1}'
set size ratio 1

file_prefix = "notebooks/results/figure_data/Figure5/
plot \
     file_prefix.'DH5alpha_pSeva221_Amer_f1_curve.dat' w l lw 3 title 'Predicted', \
     'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Amer_f1_curve.dat' w l lw 3 title 'Measured', \
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Amer_f1_curve.dat' w l lw 3 title 'Reference'

set title '{\huge Beti E1}'
set size ratio 1

plot \
     file_prefix.'DH5alpha_pSeva221_Beti_e1_curve.dat' w l lw 3 title 'Predicted' ,\
     'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Beti_e1_curve.dat' w l lw 3 title 'Measured', \
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Beti_e1_curve.dat' w l lw 3 title 'Reference'

set title '{\huge Phif P2}'
set size ratio 1

plot \
     file_prefix.'DH5alpha_pSeva221_Phif_p2_curve.dat' w l lw 3 title 'Predicted' ,\
     'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Phif_p2_curve.dat' w l lw 3 title 'Measured', \
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Phif_p2_curve.dat' w l lw 3 title 'Reference'

set xlabel '{\Large Input}' 
set title '{\huge Phif P3}'
set size ratio 1

plot \
     file_prefix.'DH5alpha_pSeva221_Phif_p3_curve.dat' w l lw 3 title 'Predicted' ,\
     'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Phif_p3_curve.dat' w l lw 3 title 'Measured', \
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Phif_p3_curve.dat' w l lw 3 title 'Reference'

set title '{\huge Qacr Q1}'
set size ratio 1

plot \
     file_prefix.'DH5alpha_pSeva221_Qacr_q1_curve.dat' w l lw 3 title 'Predicted' ,\
     'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Qacr_q1_curve.dat' w l lw 3 title 'Measured', \
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Qacr_q1_curve.dat' w l lw 3 title 'Reference'

set title '{\huge Qacr Q2}'
set size ratio 1

plot \
     file_prefix.'DH5alpha_pSeva221_Qacr_q2_curve.dat' w l lw 3 title 'Predicted' ,\
     'notebooks/results/figure_data/Figure2/DH5alpha_pSeva221_Qacr_q2_curve.dat' w l lw 3 title 'Measured', \
     'notebooks/results/figure_data/Figure2/CC118Lpir_pSeva221_Qacr_q2_curve.dat' w l lw 3 title 'Reference'

