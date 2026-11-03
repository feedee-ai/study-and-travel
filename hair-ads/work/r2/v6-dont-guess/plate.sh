#!/bin/bash
# V6 DON'T GUESS — страх выбрать не ту процедуру; консультация по фото (план Б)
set -euo pipefail
cd "$(dirname "$0")"; source ../../lib.sh
GR="eq=contrast=1.04:saturation=1.02,colortemperature=temperature=6000:mix=0.25,curves=all='0/0.02 0.5/0.5 1/0.98'"
shot shots/f1.mp4 new/lud_4664.mov 1.4 2.4 0.9 1.00 1.06 "$GR"    # руки разбирают пушистые волосы
shot shots/f2.mp4 new/joa_5744.mov 12.0 1.8 0.9 1.02 1.07 "$GR"   # осмотр длины
shot shots/f3.mp4 new/lud_4688.mov 3.6 2.2 0.9 1.00 1.05 "$GR"    # мастер в кадре
shot shots/f4.mp4 new/det_5584.mov 1.0 1.5 0.7 1.00 1.05 "$GR"    # смешивает состав
shot shots/f5.mp4 new/mur_5693.mov 9.0 2.0 0.7 1.04 1.00 "$GR"    # после: взмах блонд
shot shots/f6.mp4 new/mur_5694.mov 13.5 1.6 0.6 1.00 1.06 "$GR"   # блеск крупно
shot shots/f7.mp4 new/joa_5749.mov 3.6 3.6 0.6 1.00 1.05 "$GR"    # взмах — финал/CTA
xfade_seq plate.mp4 shots/f1.mp4 fade 0.3 shots/f2.mp4 fade 0.3 shots/f3.mp4 fade 0.3 shots/f4.mp4 fadewhite 0.35 shots/f5.mp4 fade 0.3 shots/f6.mp4 fade 0.3 shots/f7.mp4
