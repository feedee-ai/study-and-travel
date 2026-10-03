#!/bin/bash
# 02 PAIN — «до → после». Холодный «до», мягкая шторка-трансформация в тёплый, дальше плавные растворения.
set -euo pipefail
cd "$(dirname "$0")"; source ../lib.sh
mkdir -p shots
#    out                src             start  dur   speed z0   z1
shot shots/p1a.mp4  root_8e8d.mp4    0.10  3.30  0.90  1.02 1.07 "$GRADE_COLD"  # «до»: волнистые, пушатся
shot shots/p1b.mp4  root_8e8d.mp4    3.30  1.85  0.90  1.04 1.08 "$GRADE_COLD"  # рука в волнистых волосах
shot shots/p2a.mp4  root_8e8d.mp4    5.12  1.70  0.60  1.03 1.06                # нанесение — тёплый
shot shots/p2b.mp4  root_8e8d.mp4    6.20  1.80  0.60  1.03 1.06                # разделение на пряди
shot shots/p2c.mp4  root_a11e.mp4    7.75  1.60  0.85  1.03 1.06                # перчатки, начало работы
shot shots/p3.mp4   root_a11e.mp4    1.62  4.30  0.86  1.04 1.10                # фен крупно — «smooth silky glossy»
shot shots/p4.mp4   root_8e8d.mp4   21.68  3.40  0.65  1.04 1.08                # мастер расчёсывает — «tailored»
shot shots/p5.mp4   root_8e8d.mp4   13.80  3.80  0.82  1.02 1.06                # результат, взмах — услуги
shot shots/p6.mp4   leda_2235.mov   32.20  4.60  0.60  1.00 1.05 "$GRADE_LD"   # улыбка — финал/CTA
xfade_seq plate.mp4 shots/p1a.mp4 fade 0.45 shots/p1b.mp4 smoothleft 0.9 shots/p2a.mp4 fade 0.4 shots/p2b.mp4 \
  fade 0.4 shots/p2c.mp4 fade 0.45 shots/p3.mp4 fade 0.45 shots/p4.mp4 fade 0.45 shots/p5.mp4 fade 0.5 shots/p6.mp4
