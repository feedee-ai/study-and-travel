#!/bin/bash
# 01 DESIRE — подложка. Растворения 0,4 с между текстовыми кадрами, жёсткие склейки внутри кадра 3 и 5.
set -euo pipefail
cd "$(dirname "$0")"; source ../lib.sh
mkdir -p shots
#    out                src             start  dur   speed z0   z1
shot shots/c1.mp4   leda_2235.mov   17.60  3.40  0.60  1.00 1.06 "$GRADE_LD"
shot shots/c2.mp4   root_a11e.mp4   13.75  3.20  0.90  1.12 1.19
shot shots/c3a.mp4  leda_2235.mov    2.95  1.25  0.50  1.04 1.07 "$GRADE_LD"
shot shots/c3b.mp4  cam_2275.mov     8.45  1.00  0.50  1.06 1.09
shot shots/c3c.mp4  leda_2235.mov   29.20  1.00  0.50  1.04 1.07 "$GRADE_LD"
shot shots/c4.mp4   cam_2266.mov     3.40  3.00  0.85  1.02 1.08
shot shots/c5a.mp4  root_8e8d.mp4    5.00  2.40  0.85  1.03 1.07
shot shots/c5b.mp4  root_8e8d.mp4    7.30  1.25  0.75  1.03 1.06
concat_hard shots/c3.mp4 "$PWD/shots/c3a.mp4" "$PWD/shots/c3b.mp4" "$PWD/shots/c3c.mp4"
concat_hard shots/c5.mp4 "$PWD/shots/c5a.mp4" "$PWD/shots/c5b.mp4"
xfade_chain plate.mp4 0.4 shots/c1.mp4 shots/c2.mp4 shots/c3.mp4 shots/c4.mp4 shots/c5.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 plate.mp4
