#!/bin/bash
# V1 SAME HAIR — Joana: до → после
set -euo pipefail
cd "$(dirname "$0")"; source ../../lib.sh
GR="eq=contrast=1.04:saturation=1.02,colortemperature=temperature=6000:mix=0.25,curves=all='0/0.02 0.5/0.5 1/0.98'"
shot shots/a1.mp4 new/joa_5744.mov 15.4 2.6 1.0 1.00 1.07 "$GR"   # сухие пушистые концы в руке
shot shots/a2.mp4 new/joa_5744.mov 21.4 1.7 0.8 1.06 1.12 "$GR"   # две руки собирают пух
shot shots/a3.mp4 new/joa_5749.mov 26.0 2.6 0.7 1.08 1.02 "$GR"   # после: гладкое полотно
shot shots/a4.mp4 new/joa_5750.mov 3.2 2.0 0.8 1.00 1.05 "$GR"    # крупно прямые блестящие
shot shots/a5.mp4 new/joa_5750.mov 10.0 1.9 0.8 1.02 1.06 "$GR"   # ладонь по волосам
shot shots/a6.mp4 new/joa_5749.mov 3.6 3.8 0.6 1.00 1.05 "$GR"    # взмах — финал/CTA
xfade_seq plate.mp4 shots/a1.mp4 fade 0.25 shots/a2.mp4 fadewhite 0.4 shots/a3.mp4 fade 0.3 shots/a4.mp4 fade 0.3 shots/a5.mp4 fade 0.3 shots/a6.mp4
