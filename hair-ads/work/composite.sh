#!/bin/bash
# composite.sh PLATE OVERLAY OUT — сведение подложки и прозрачного слоя HyperFrames (ProRes 4444, BT.601 без метки) в H.264 BT.709 tv
set -euo pipefail
ffmpeg -v error -y -i "$1" -i "$2" -f lavfi -i anullsrc=r=48000:cl=stereo -filter_complex "\
[0:v]scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int+full_chroma_inp,format=gbrp[bg];\
[1:v]scale=in_color_matrix=bt601:flags=accurate_rnd+full_chroma_int+full_chroma_inp,format=gbrap[fg];\
[bg][fg]overlay=format=gbrp:shortest=1,scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p,\
setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv[v]" \
  -map "[v]" -map 2:a -shortest -c:v libx264 -profile:v high -preset slow -crf 15 -maxrate 20M -bufsize 40M -tune film \
  -c:a aac -b:a 128k -movflags +faststart \
  -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 "$3"
