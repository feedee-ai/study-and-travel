#!/bin/bash
# peek.sh SRC START END STEP OUT — кадры из отрезка исходника в одну полосу (по 8 в ряд)
src=$1 a=$2 b=$3 st=$4 out=$5
ffmpeg -nostdin -v error -y -ss "$a" -to "$b" -i "$src" -vf "fps=1/$st,scale=200:-2,drawtext=text='%{eif\:t+$a\:d}.%{eif\:mod((t+$a)*10\,10)\:d}':x=4:y=4:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.5,tile=8x1:padding=2" -frames:v 1 -q:v 4 "$out"
