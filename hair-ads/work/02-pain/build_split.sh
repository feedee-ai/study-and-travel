#!/bin/bash
# ч/б сплит для кадра 1 (02 PAIN v2)
set -euo pipefail
cd "$(dirname "$0")"; source ../lib.sh
shot shots/p1bot_full.mp4 root_8e8d.mp4 0.10 4.717 0.66 1.03 1.07 "$GRADE_BW"
ffmpeg -v error -y -i ../../material/stock/mk_45573.mp4 -i shots/p1bot_full.mp4 -filter_complex "\
[0:v]trim=start=2.0:duration=4.9,setpts=PTS-STARTPTS,framerate=fps=30,scale=-2:1000:flags=lanczos,crop=1080:960:(iw-1080)/2+60:20,${GRADE_BW},\
scale=w='trunc(1080*(1+0.05*t/4.717)/2)*2':h='trunc(960*(1+0.05*t/4.717)/2)*2':eval=frame:flags=bicubic,crop=1080:960,setsar=1[top];\
[1:v]crop=1080:960:0:500,setsar=1[bot];[top][bot]vstack,format=yuv420p" -t 4.717 -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p \
-color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 shots/p1split.mp4
