#!/bin/bash
# 01 DESIRE v3 — подложка. Только плавные растворения 0,4 с между ВСЕМИ кусками; куски строго между внутренними склейками (CUTS.md).
# Старты на таймлайне: k1 0 · k2 3.4 · k3 6.8 · k4a 10.0 · k4b 12.2 · k5a 13.6 · k5b 14.8 · k5c 16.15 · k6 17.55 · конец 22.35
set -euo pipefail
cd "$(dirname "$0")"; source ../lib.sh
mkdir -p shots
#    out                src             start  dur   speed z0   z1
shot shots/k1.mp4   leda_2235.mov   17.60  3.80  0.55  1.00 1.06 "$GRADE_LD"   # длинные гладкие волосы — «with you every day»
shot shots/k2.mp4   root_a11e.mp4   13.75  3.80  0.85  1.10 1.17 "$GRADE_RA"   # руки по волосам, результат — «look its best»
shot shots/k3.mp4   leda_2235.mov   28.60  3.60  0.50  1.03 1.07 "$GRADE_LD"   # взмах волос слоу-мо — «smooth silky glossy»
shot shots/k4a.mp4  root_a11e.mp4    5.50  2.60  0.80  1.02 1.06                # мастер со щёткой — «tailored»
shot shots/k4b.mp4  root_a11e.mp4    0.05  1.80  0.80  1.04 1.08                # фен и щётка у окна
shot shots/k5a.mp4  root_8e8d.mp4    5.12  1.60  0.63  1.03 1.06                # нанесение состава
shot shots/k5b.mp4  root_8e8d.mp4    7.35  1.75  0.70  1.03 1.05                # фен
shot shots/k5c.mp4  root_a11e.mp4    1.60  1.80  0.80  1.04 1.07                # фен со щёткой крупно
shot shots/k6.mp4   root_8e8d.mp4   24.10  4.80  0.92  1.16 1.22                # мастер и клиентка в зеркале — финал/CTA
xfade_chain plate.mp4 0.4 shots/k1.mp4 shots/k2.mp4 shots/k3.mp4 shots/k4a.mp4 shots/k4b.mp4 shots/k5a.mp4 shots/k5b.mp4 shots/k5c.mp4 shots/k6.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 plate.mp4
