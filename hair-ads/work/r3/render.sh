#!/bin/bash
# render.sh ID TRACK OFFSET [MUFFLE] — HyperFrames → mp4; лёгкое плёночное зерно; музыка −14 LUFS; кодирование под Reels
set -euo pipefail
cd "$(dirname "$0")"; v=$1; OUT=../../out/r3; mkdir -p $OUT/music $OUT/nomusic render
python3 build.py $v >/dev/null
hyperframes render $v -o $PWD/render/$v.mp4 --quality delivery --quiet
# зерно только по яркости, мягкое; кадр 1080x1920, BT.709 tv
ffmpeg -v error -y -i render/$v.mp4 -f lavfi -i anullsrc=r=48000:cl=stereo -vf "noise=c0s=5:c0f=t,format=yuv420p" \
  -map 0:v -map 1:a -shortest -c:v libx264 -profile:v high -preset slow -crf 17 -maxrate 10M -bufsize 20M -pix_fmt yuv420p \
  -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 128k -movflags +faststart $OUT/nomusic/$v.mp4
../music.sh $OUT/nomusic/$v.mp4 $OUT/music/$v.mp4 ../../material/music/mk_$2.mp3 $3 ${4:-0}
echo "done $v $(ffprobe -v error -show_entries format=duration -of csv=p=0 $OUT/music/$v.mp4)"
