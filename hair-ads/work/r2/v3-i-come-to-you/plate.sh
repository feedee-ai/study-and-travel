#!/bin/bash
# V3 I COME TO YOU — мастер в кадре, выезд
set -euo pipefail
cd "$(dirname "$0")"; source ../../lib.sh
GR="eq=contrast=1.04:saturation=1.02,colortemperature=temperature=6000:mix=0.25,curves=all='0/0.02 0.5/0.5 1/0.98'"
shot shots/c1.mp4 new/lud_4691.mov 0.2 2.6 0.9 1.00 1.05 "$GR"    # мастер за работой, лицо
shot shots/c2.mp4 new/lud_4666.mov 2.6 2.2 1.0 1.00 1.04 "$GR"    # раскладывает инструменты
shot shots/c3.mp4 new/lud_4672.mov 0.6 1.6 0.8 1.05 1.10 "$GR"    # состав в чаше крупно
shot shots/c4.mp4 new/lud_4688.mov 3.6 2.2 0.9 1.00 1.05 "$GR"    # лицо мастера крупнее
shot shots/c5.mp4 new/ann_5489.mov 135 1.8 0.8 1.00 1.05 "$GR"    # утюжок
shot shots/c6.mp4 new/mur_5694.mov 6.0 2.4 0.7 1.00 1.05 "$GR"    # ладонь по блестящим волосам
shot shots/c7.mp4 new/ann_5495.mov 11.0 3.6 0.7 1.00 1.05 "$GR"   # результат брюнетка — финал/CTA
xfade_seq plate.mp4 shots/c1.mp4 fade 0.3 shots/c2.mp4 fade 0.3 shots/c3.mp4 fade 0.3 shots/c4.mp4 fade 0.3 shots/c5.mp4 fade 0.3 shots/c6.mp4 fade 0.3 shots/c7.mp4
