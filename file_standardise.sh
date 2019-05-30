#!/bin/bash

DEST_DIR=$1

declare -A MAP
MAP[1201]=1201
MAP[1717]=1717
MAP[1818]=1818
MAP[AmeR-F1]=F1_AmeR
MAP[AmtR-A1]=A1_AmtR
MAP[BetI-E1]=E1_BetI
for i in {1..3}; do MAP[BM3R1-B${i}]=B${i}_BM3R1; done
MAP[HIYIIR-H1]=H1_HlyIIR
MAP[lcaRA-I1]=I1_IcaRA
MAP[LitR-L1]=L1_LitR
MAP[LmrA-N1]=N1_LmrA
for i in {1..3}; do MAP[PhIF-P${i}]=P${i}_PhlF; done
MAP[PsrA-R1]=R1_PsrA
for i in {1..2}; do MAP[QacR-Q${i}]=Q${i}_QacR; done
for i in {1..4}; do MAP[SrpR-S${i}]=S${i}_SrpR; done

for old in ${!MAP[@]};
do for f in ${old}*.csv; do
       new=${f//${old}/${MAP[${old}]}};
       mv -f $f ${DEST_DIR}/${new};
       sed -i 's/["\| ]//g' ${DEST_DIR}/${new};
       chmod 664 ${DEST_DIR}/${new};
   done;
done
