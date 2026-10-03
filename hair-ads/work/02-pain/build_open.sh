#!/bin/bash
# 02 PAIN v3 — первый экран: ч/б монтаж на весь экран (хаос волос → отчаяние у зеркала → наше «до»), 4.717 с
set -euo pipefail
cd "$(dirname "$0")"; source ../lib.sh
XS0=0.10           shot shots/o1.mp4 stock/mk_45573.mp4  8.00  1.75  1.00  1.04 1.09 "$GRADE_BW,unsharp=7:7:0.6"
XS0=0.28 YS=0.0    shot shots/o2.mp4 stock/mk_6047.mp4   4.00  1.90  1.00  1.25 1.32 "$GRADE_BW,unsharp=7:7:0.6"
                   shot shots/o3.mp4 root_8e8d.mp4        0.10  1.667 0.90  1.03 1.07 "$GRADE_BW"
xfade_seq shots/p1open.mp4 shots/o1.mp4 fade 0.3 shots/o2.mp4 fade 0.3 shots/o3.mp4
