#!/bin/bash
# grid.sh FILE OUT [STEP] — раскадровка готового ролика: кадр каждые STEP с, 8 в ряд
f=$1; o=$2; st=${3:-0.6}
ffmpeg -nostdin -v error -y -i "$f" -vf "fps=1/$st,scale=216:-2,drawtext=text='%{eif\:t*$st\:d}.%{eif\:mod(t*$st*10\,10)\:d}':x=4:y=4:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.5,tile=8x4:padding=2" -q:v 4 "$o"
