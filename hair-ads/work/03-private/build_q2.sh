#!/bin/bash
# 03 — кремовая сцена с аркой: внутри арки «боль» (пробка → ожидание → часы), обводка вшита в кадр (появляется вместе с аркой).
set -euo pipefail
cd "$(dirname "$0")"
S=../../material/stock
PAIN="eq=saturation=0.6:contrast=1.03:gamma=1.0,colortemperature=temperature=7400:mix=0.25"
W() { # W OUT SRC START DUR CROPX(доля центра) FPSFILTER
  ffmpeg -v error -y -ss "$3" -t "$(echo "$4+0.2" | bc -l)" -i "$S/$2" -an -vf "\
setpts=PTS-STARTPTS,$6,crop=trunc(ih*600/820/2)*2:ih:min(max(iw*$5-ih*300/820\,0)\,iw-ih*600/820):0,scale=1200:1640:flags=lanczos,${PAIN},\
scale=w='trunc(1200*(1.0+0.05*t/$4)/2)*2':h='trunc(1640*(1.0+0.05*t/$4)/2)*2':eval=frame:flags=bicubic,crop=1200:1640,scale=600:820:flags=lanczos,setsar=1,format=yuv420p" \
    -t "$4" -c:v libx264 -crf 12 -preset slow "$1"
}
W shots/a1.mp4 mk_4241.mp4  0.5 1.70 0.50 "fps=30"
W shots/a2.mp4 mk_22536.mp4 3.0 1.70 0.38 "framerate=fps=30"
W shots/a3.mp4 mk_46423.mp4 2.0 1.50 0.45 "framerate=fps=30"
ffmpeg -v error -y -i shots/a1.mp4 -i shots/a2.mp4 -i shots/a3.mp4 -filter_complex \
  "[0][1]xfade=transition=fade:duration=0.35:offset=1.35[x];[x][2]xfade=transition=fade:duration=0.35:offset=2.70,format=yuv420p" \
  -c:v libx264 -crf 12 -preset slow shots/arch_in.mp4
ffmpeg -v error -y -stream_loop -1 -i arch_mask.png -i shots/arch_in.mp4 -f lavfi -i "color=c=0xF2ECE3:s=1080x1920:r=30:d=4.2" -loop 1 -i arch_outline.png -filter_complex "\
[1:v]format=yuva420p[win];[0:v]format=gray,scale=600:820[m];[win][m]alphamerge[wa];[2:v][wa]overlay=240:540:shortest=1[c];\
[3:v]format=rgba[ol];[c][ol]overlay=0:0:shortest=1,format=yuv420p,setsar=1" \
  -t 4.2 -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 shots/q2.mp4
