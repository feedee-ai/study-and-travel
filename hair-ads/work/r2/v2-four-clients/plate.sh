#!/bin/bash
# V2 FOUR CLIENTS — 4 преображения за неделю (27.10–2.11)
set -euo pipefail
cd "$(dirname "$0")"; source ../../lib.sh
GR="eq=contrast=1.04:saturation=1.02,colortemperature=temperature=6000:mix=0.25,curves=all='0/0.02 0.5/0.5 1/0.98'"
shot shots/b1.mp4 new/joa_5744.mov 21.4 1.5 0.9 1.04 1.09 "$GR"   # 1 Joana до
shot shots/b2.mp4 new/joa_5749.mov 26.0 2.0 0.7 1.06 1.02 "$GR"   # 1 после
shot shots/b3.mp4 new/mur_5683.mov 5.0 1.5 0.9 1.00 1.06 "$GR"    # 2 Muriel до
shot shots/b4.mp4 new/mur_5693.mov 9.0 2.0 0.7 1.04 1.00 "$GR"    # 2 после
shot shots/b5.mp4 new/lud_4664.mov 1.5 1.5 0.9 1.00 1.06 "$GR"    # 3 до
shot shots/b6.mp4 new/lud_4744.mov 17.5 2.0 0.8 1.04 1.00 "$GR"   # 3 после
shot shots/b7.mp4 new/ann_5489.mov 134 1.5 0.9 1.00 1.05 "$GR"    # 4 Annette в процессе (утюжок)
shot shots/b8.mp4 new/ann_5500.mov 7.4 3.4 0.6 1.00 1.05 "$GR"    # 4 после — финал/CTA
xfade_seq plate.mp4 shots/b1.mp4 fadewhite 0.3 shots/b2.mp4 smoothleft 0.35 shots/b3.mp4 fadewhite 0.3 shots/b4.mp4 smoothleft 0.35 shots/b5.mp4 fadewhite 0.3 shots/b6.mp4 smoothleft 0.35 shots/b7.mp4 fadewhite 0.3 shots/b8.mp4
