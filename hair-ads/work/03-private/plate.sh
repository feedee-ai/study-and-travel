#!/bin/bash
# 03 PRIVATE SERVICE — тихо, альпийская роскошь. Альпы → визит → арка-окно на кремовом → процесс дома → результат → детали → Альпы (CTA).
set -euo pipefail
cd "$(dirname "$0")"; source ../lib.sh
mkdir -p shots
#    out                src                    start  dur   speed z0   z1
shot shots/q1a.mp4  stock/mk_4283.mp4       0.50  2.90  1.00  1.00 1.05 "$GRADE_STOCK"  # Альпы, облака
shot shots/q1b.mp4  root_8e8d.mp4          24.10  2.90  0.90  1.18 1.22                 # мастер и клиентка дома (зеркало)
# q2.mp4 — арка-окно с шале на кремовом фоне (собрана отдельно, build_q2.sh)
shot shots/q3.mp4   cam_2266.mov            0.30  4.40  0.90  1.03 1.08                 # процедура дома, на стуле
shot shots/q4.mp4   cam_2264.mov            1.00  4.40  0.90  1.02 1.06                 # результат
shot shots/q5.mp4   root_8e8d.mp4          10.95  3.60  0.77  1.06 1.10                 # детали: перчатка по гладким волосам
shot shots/q6.mp4   stock/mk_4283.mp4       7.00  4.90  1.00  1.03 1.08 "$GRADE_STOCK"  # Альпы — финал/CTA
xfade_seq plate.mp4 shots/q1a.mp4 fade 0.6 shots/q1b.mp4 fade 0.8 shots/q2.mp4 fade 0.6 shots/q3.mp4 \
  fade 0.5 shots/q4.mp4 fade 0.5 shots/q5.mp4 fade 0.6 shots/q6.mp4
