#!/bin/bash
# V4 FRIZZ TO GLASS — процесс крупно, мало текста
set -euo pipefail
cd "$(dirname "$0")"; source ../../lib.sh
GR="eq=contrast=1.04:saturation=1.02,colortemperature=temperature=6000:mix=0.25,curves=all='0/0.02 0.5/0.5 1/0.98'"
shot shots/d1.mp4 new/lud_4664.mov 1.6 1.8 0.9 1.00 1.06 "$GR"    # пушистые сухие
shot shots/d2.mp4 new/det_5585.mov 3.0 1.5 0.7 1.00 1.05 "$GR"    # крем в чаше сверху
shot shots/d3.mp4 new/lud_4707.mov 2.6 1.4 0.8 1.02 1.08 "$GR"    # пена в ладони
shot shots/d4.mp4 new/lud_4674.mov 6.0 1.4 0.8 1.00 1.05 "$GR"    # нанесение на пряди
shot shots/d5.mp4 new/lud_4710.mov 12.5 1.4 0.8 1.00 1.05 "$GR"   # фен со щёткой
shot shots/d6.mp4 new/mur_5694.mov 13.5 2.2 0.6 1.00 1.06 "$GR"   # блеск крупно
shot shots/d7.mp4 new/joa_5750.mov 10.0 2.0 0.8 1.00 1.05 "$GR"   # ладонь
shot shots/d8.mp4 new/mur_5693.mov 9.0 3.4 0.6 1.00 1.04 "$GR"    # взмах — финал/CTA
xfade_seq plate.mp4 shots/d1.mp4 fade 0.2 shots/d2.mp4 fade 0.2 shots/d3.mp4 fade 0.2 shots/d4.mp4 fade 0.2 shots/d5.mp4 fadewhite 0.35 shots/d6.mp4 fade 0.25 shots/d7.mp4 fade 0.25 shots/d8.mp4
