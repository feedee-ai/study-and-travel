#!/bin/bash
# 04 TIME v3 — lifestyle. Между текстовыми кадрами мягкая шторка вверх (smoothup), внутри кадров растворения.
set -euo pipefail
cd "$(dirname "$0")"; source ../lib.sh
mkdir -p shots
#    out                src                    start  dur   speed z0   z1
XS0=0.10  shot shots/v1a.mp4  stock/mk_45573.mp4  8.00  2.50  1.00  1.03 1.07 "$GRADE_STOCK,unsharp=7:7:0.7"  # утро: пушащиеся пряди
XS0=0.05  shot shots/v1b.mp4  stock/mk_48831.mp4 12.80  2.70  1.00  1.03 1.06 "$GRADE_STOCK,unsharp=7:7:0.7"  # укладка феном
XS0=0.12  shot shots/v2.mp4   stock/mk_36468.mp4  1.50  3.45  0.85  1.02 1.06 "$GRADE_STOCK,unsharp=7:7:0.6"  # волосы на ветру в закатном свете — less frizz
          shot shots/v3.mp4   stock/mk_43785.mp4  0.90  4.20  0.85  1.00 1.06 "$GRADE_STOCK"                 # руки вверх, вид на горы — more time for you
shot shots/v4a.mp4  cam_2275.mov            8.20  3.60  0.50  1.04 1.08                 # движение волос, слоу-мо
shot shots/v4b.mp4  cam_2264.mov            7.50  2.30  0.90  1.02 1.05                 # результат со спины
shot shots/v5.mp4   cam_2265.mov            3.40  4.40  1.00  1.02 1.06                 # результат + взмах
XS0=-0.03 shot shots/v6.mp4  stock/mk_31407.mp4 0.30  5.00  1.00  1.00 1.05 "$GRADE_STOCK"  # утро у окна — финал/CTA
xfade_seq plate.mp4 shots/v1a.mp4 fade 0.35 shots/v1b.mp4 smoothup 0.6 shots/v2.mp4 smoothup 0.6 shots/v3.mp4 \
  smoothup 0.6 shots/v4a.mp4 fade 0.4 shots/v4b.mp4 smoothup 0.6 shots/v5.mp4 fade 0.6 shots/v6.mp4
