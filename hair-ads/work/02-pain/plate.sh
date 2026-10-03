#!/bin/bash
# 02 PAIN — «до → после». Холодный «до», мягкая шторка-трансформация в тёплый, дальше плавные растворения.
set -euo pipefail
cd "$(dirname "$0")"; source ../lib.sh
mkdir -p shots
#    out                src             start  dur   speed z0   z1
# p1split.mp4 — ч/б сплит-экран 4.717 с: сверху сток mk_45573 (пушащиеся спутанные волосы), снизу «до» root_8e8d 0.10 (см. build_split.sh)
shot shots/p2a.mp4  root_8e8d.mp4    5.12  1.70  0.60  1.03 1.06                # нанесение — тёплый
shot shots/p2b.mp4  root_8e8d.mp4    6.20  1.80  0.60  1.03 1.06                # разделение на пряди
shot shots/p2c.mp4  root_a11e.mp4    7.75  1.60  0.85  1.03 1.06                # перчатки, начало работы
shot shots/p3.mp4   root_a11e.mp4    1.62  4.30  0.86  1.04 1.10                # фен крупно — «smooth silky glossy»
shot shots/p4.mp4   root_8e8d.mp4   21.68  3.40  0.65  1.04 1.08                # мастер расчёсывает — «tailored»
shot shots/p5.mp4   root_8e8d.mp4   13.80  3.80  0.82  1.02 1.06                # результат, взмах — услуги
shot shots/p6.mp4   leda_2235.mov   32.20  4.60  0.60  1.00 1.05 "$GRADE_LD"   # улыбка — финал/CTA
xfade_seq plate.mp4 shots/p1split.mp4 smoothleft 0.9 shots/p2a.mp4 fade 0.4 shots/p2b.mp4 \
  fade 0.4 shots/p2c.mp4 fade 0.45 shots/p3.mp4 fade 0.45 shots/p4.mp4 fade 0.45 shots/p5.mp4 fade 0.5 shots/p6.mp4
