#!/bin/bash
# 01 DESIRE v2 — подложка. Каждое действие в кадре — один раз; кадры длиннее; финальный CTA-кадр 4,8 с.
# Растворения 0,4 с между текстовыми кадрами, жёсткие склейки внутри кадров 4 и 5.
# Тайминг (старты на таймлайне): 0 · 3.4 · 6.8 · 10.0 · 14.0 · 18.0; конец 22.8
set -euo pipefail
cd "$(dirname "$0")"; source ../lib.sh
mkdir -p shots
#    out                src             start  dur   speed z0   z1
shot shots/k1.mp4   leda_2235.mov   32.20  3.80  0.70  1.00 1.06 "$GRADE_LD"   # улыбка, результат — «with you every day»
shot shots/k2.mp4   luda_3348.mov   45.00  3.80  0.70  1.02 1.08 "$GRADE_L48"   # каре крупно, блеск — «look its best»
shot shots/k3.mp4   leda_2235.mov   28.60  3.60  0.50  1.03 1.07 "$GRADE_LD"   # взмах волос слоу-мо — «smooth silky glossy»
shot shots/k4a.mp4  root_a11e.mp4    5.50  2.20  0.93  1.02 1.06                # мастер со щёткой — «tailored»
shot shots/k4b.mp4  luda_3348.mov    0.50  2.20  0.90  1.02 1.06 "$GRADE_L48"   # брашинг каре
shot shots/k5a.mp4  root_8e8d.mp4    5.00  1.90  0.90  1.03 1.06                # нанесение состава
shot shots/k5b.mp4  root_8e8d.mp4    7.25  1.30  0.77  1.03 1.05                # фен
shot shots/k5c.mp4  root_a11e.mp4    1.50  1.20  1.00  1.04 1.07                # фен со щёткой крупно
shot shots/k6.mp4   root_8e8d.mp4   24.00  4.80  0.92  1.16 1.22                # мастер и клиентка в зеркале — финал/CTA
concat_hard shots/k4.mp4 "$PWD/shots/k4a.mp4" "$PWD/shots/k4b.mp4"
concat_hard shots/k5.mp4 "$PWD/shots/k5a.mp4" "$PWD/shots/k5b.mp4" "$PWD/shots/k5c.mp4"
xfade_chain plate.mp4 0.4 shots/k1.mp4 shots/k2.mp4 shots/k3.mp4 shots/k4.mp4 shots/k5.mp4 shots/k6.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 plate.mp4
