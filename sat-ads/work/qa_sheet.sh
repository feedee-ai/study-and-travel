#!/bin/bash
# qa_sheet.sh VIDEO OUT.jpg START END [COLS] — каждый кадр отрезка START..END (30 к/с) листом с таймкодами
set -euo pipefail
V=$1; O=$2; A=$3; B=$4; C=${5:-8}
N=$(python3 -c "print(round(($B-$A)*30))")
R=$(python3 -c "import math;print(math.ceil($N/$C))")
ffmpeg -v error -y -ss "$A" -i "$V" -frames:v "$N" -vf "scale=180:320,drawtext=text='%{eif\:t+$A\:d}.%{eif\:mod((t+$A)*100\,100)\:d\:2}':fontcolor=yellow:fontsize=18:x=4:y=4:box=1:boxcolor=black@0.6,tile=${C}x${R}" -frames:v 1 "$O"
