#!/bin/bash
# V5 MOUNTAIN AIR — боль: горный климат сушит волосы (план Б)
set -euo pipefail
cd "$(dirname "$0")"; source ../../lib.sh
GR="eq=contrast=1.04:saturation=1.02,colortemperature=temperature=6000:mix=0.25,curves=all='0/0.02 0.5/0.5 1/0.98'"
shot shots/e1.mp4 stock/mk_4283-2160.mp4 2.0 2.4 1.0 1.00 1.06 "$GRADE_STOCK"  # Альпы, таймлапс (Mixkit 4283)
shot shots/e2.mp4 new/joa_5744.mov 15.4 1.9 0.9 1.02 1.08 "$GR"   # сухие концы в руке
shot shots/e3.mp4 new/mur_5683.mov 10.6 1.7 0.9 1.00 1.06 "$GR"   # ладонь по сухой длине
shot shots/e4.mp4 new/lud_4673.mov 1.0 1.5 0.8 1.04 1.09 "$GR"    # состав в чаше
shot shots/e5.mp4 new/ann_5489.mov 134 1.6 0.9 1.00 1.05 "$GR"    # утюжок запечатывает
shot shots/e6.mp4 new/joa_5750.mov 10.0 1.9 0.8 1.00 1.05 "$GR"   # ладонь по гладким волосам
shot shots/e7.mp4 new/ann_5495.mov 11.0 3.6 0.7 1.00 1.05 "$GR"   # результат — финал/CTA
xfade_seq plate.mp4 shots/e1.mp4 fade 0.3 shots/e2.mp4 fade 0.25 shots/e3.mp4 fade 0.25 shots/e4.mp4 fade 0.25 shots/e5.mp4 fadewhite 0.35 shots/e6.mp4 fade 0.3 shots/e7.mp4
