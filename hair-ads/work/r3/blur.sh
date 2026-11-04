#!/bin/bash
# размытые копии финальных кусков (для карточки CTA): gblur, чуть темнее
cd "$(dirname "$0")/seg"
for s in w_swing a_end g_end m_end c_end k_end; do
  [ -s ${s}_bl.mp4 ] && [ "${FORCE:-0}" != 1 ] && continue
  ffmpeg -v error -y -i $s.mp4 -vf "gblur=sigma=26,eq=brightness=-0.02:saturation=0.9" -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p \
    -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 ${s}_bl.mp4 && echo "bl $s"
done
