#!/bin/bash
# build.sh VDIR TRACK OFFSET [MUFFLE] — текст (HyperFrames, ProRes 4444) поверх подложки → без музыки и с музыкой в hair-ads/out/r2/
set -euo pipefail
cd "$(dirname "$0")"; v=${1%/}; OUT=../../out/r2; mkdir -p $OUT/nomusic $OUT/music
python3 gen_overlay.py $v >/dev/null
hyperframes render $v/hf --format mov -o $PWD/$v/overlay.mov --quiet
../composite.sh $v/plate.mp4 $v/overlay.mov $v/comp.mp4
# IG: H.264 high, CRF 18, ≤9 Мбит/с
enc(){ ffmpeg -v error -y -i "$1" -c:v libx264 -profile:v high -preset slow -crf 18 -maxrate 9M -bufsize 18M -pix_fmt yuv420p \
  -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a copy -movflags +faststart "$2"; }
enc $v/comp.mp4 $OUT/nomusic/$v.mp4
../music.sh $v/comp.mp4 $v/comp_m.mp4 ../../material/music/mk_$2.mp3 $3 ${4:-0}
enc $v/comp_m.mp4 $OUT/music/$v.mp4
echo "done $v $(ffprobe -v error -show_entries format=duration -of csv=p=0 $OUT/music/$v.mp4)"
