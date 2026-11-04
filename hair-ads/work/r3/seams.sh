#!/bin/bash
# seams.sh FILE — резкие смены кадра (scene>0.28): время и величина; это кандидаты в «рваные» стыки
ffmpeg -nostdin -v error -i "$1" -vf "select='gt(scene,0.28)',metadata=print:file=-" -an -f null - 2>/dev/null | \
  awk '/pts_time/{split($0,a,"pts_time:");t=a[2]} /scene_score/{split($0,b,"=");printf "%.2f %.2f\n", t, b[2]}'
