#!/bin/bash
# 04 TIME — lifestyle, динамичнее. Между текстовыми кадрами мягкая шторка вверх (smoothup), внутри кадров растворения.
set -euo pipefail
cd "$(dirname "$0")"; source ../lib.sh
mkdir -p shots
#    out                src                    start  dur   speed z0   z1
shot shots/w1a.mp4  root_a11e.mp4           0.05  1.90  0.75  1.04 1.08                 # укладка: фен и щётка у окна
shot shots/w1b.mp4  root_a11e.mp4           1.62  3.30  0.78  1.04 1.09                 # фен крупно
shot shots/w2a.mp4  root_8e8d.mp4           8.68  1.80  0.75  1.04 1.07                 # пряди со щёткой
shot shots/w2b.mp4  root_a11e.mp4           9.16  2.00  0.82  1.03 1.06                 # утюжок
XS0=0.03 shot shots/w3.mp4  stock/mk_4948.mp4  0.80  4.20  1.00  1.00 1.05 "$GRADE_STOCK"  # lifestyle: книга
shot shots/w4.mp4   cam_2275.mov            8.20  3.60  0.50  1.04 1.08                 # движение волос, слоу-мо
shot shots/w5.mp4   cam_2265.mov            3.40  4.40  1.00  1.02 1.06                 # результат + взмах
XS0=-0.03 shot shots/w6.mp4  stock/mk_31407.mp4 0.30  5.00  1.00  1.00 1.05 "$GRADE_STOCK"  # утро у окна — финал/CTA
xfade_seq plate.mp4 shots/w1a.mp4 fade 0.35 shots/w1b.mp4 smoothup 0.6 shots/w2a.mp4 fade 0.35 shots/w2b.mp4 \
  smoothup 0.6 shots/w3.mp4 smoothup 0.6 shots/w4.mp4 smoothup 0.6 shots/w5.mp4 fade 0.6 shots/w6.mp4
