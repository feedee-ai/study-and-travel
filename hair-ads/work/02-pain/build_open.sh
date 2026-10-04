#!/bin/bash
# 02 PAIN v4 — первый экран: один ч/б кадр (пушащиеся спутанные волосы, сток mk_45573) на всю длину 4.733 с, лёгкое замедление
set -euo pipefail
cd "$(dirname "$0")"; source ../lib.sh
XS0=0.10 shot shots/p1open.mp4 stock/mk_45573.mp4 7.40 4.733 0.85 1.03 1.10 "$GRADE_BW,unsharp=7:7:0.6"
