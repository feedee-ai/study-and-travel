#!/bin/bash
# 04 TIME — lifestyle, динамичнее. Между текстовыми кадрами мягкая шторка вверх (smoothup), внутри кадров растворения.
set -euo pipefail
cd "$(dirname "$0")"; source ../lib.sh
mkdir -p shots
#    out                src                    start  dur   speed z0   z1
XS0=0.18 YS=-0.115 shot shots/w1a.mp4  stock/mk_51178.mp4  0.30  4.85  1.00  1.30 1.36 "$GRADE_STOCK"  # утро: полотенце, уход у зеркала
XS0=0.10  shot shots/w2a.mp4  stock/mk_45573.mp4  8.00  1.80  1.00  1.03 1.07 "$GRADE_STOCK,unsharp=7:7:0.7"  # пушащиеся пряди — less frizz
XS0=0.05  shot shots/w2b.mp4  stock/mk_48831.mp4 12.80  2.00  1.00  1.03 1.06 "$GRADE_STOCK,unsharp=7:7:0.7"  # укладка феном — less styling
XS0=0.03 shot shots/w3.mp4  stock/mk_4948.mp4  0.80  4.20  1.00  1.00 1.05 "$GRADE_STOCK"  # lifestyle: книга
shot shots/w4.mp4   cam_2275.mov            8.20  3.60  0.50  1.04 1.08                 # движение волос, слоу-мо
shot shots/w5.mp4   cam_2265.mov            3.40  4.40  1.00  1.02 1.06                 # результат + взмах
XS0=-0.03 shot shots/w6.mp4  stock/mk_31407.mp4 0.30  5.00  1.00  1.00 1.05 "$GRADE_STOCK"  # утро у окна — финал/CTA
xfade_seq plate.mp4 shots/w1a.mp4 smoothup 0.6 shots/w2a.mp4 fade 0.35 shots/w2b.mp4 \
  smoothup 0.6 shots/w3.mp4 smoothup 0.6 shots/w4.mp4 smoothup 0.6 shots/w5.mp4 fade 0.6 shots/w6.mp4
