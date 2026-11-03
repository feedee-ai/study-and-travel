#!/bin/bash
# sheet.sh FILE... — лист из 8 кадров на каждое видео (work/sheets/<name>.jpg) + строка метаданных
cd "$(dirname "$0")"
for f in "$@"; do
  n=$(basename "${f%.*}"); out=sheets/$n.jpg; [ -s "$out" ] && continue
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f"); [ -z "$d" ] && continue
  info=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,color_transfer:stream_side_data=rotation -of csv=p=0 "$f" | tr '\n' ' ')
  echo "$n dur=$d $info" >> sheets/index.txt
  ins=(); fl=""
  for i in 0 1 2 3 4 5 6 7; do t=$(echo "$d*($i+0.5)/8" | bc -l | sed "s/^\./0./"); ins+=(-ss "$t" -i "$f"); fl+="[$i:v]scale=240:-2,setsar=1,drawtext=text='$(printf %.1f "$t")':x=6:y=6:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.5[v$i];"; done
  ffmpeg -v error -y "${ins[@]}" -filter_complex "${fl}[v0][v1][v2][v3][v4][v5][v6][v7]hstack=8" -frames:v 1 -q:v 4 "$out"
done
