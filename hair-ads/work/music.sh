#!/bin/bash
# music.sh IN.mp4 OUT.mp4 TRACK.mp3 OFFSET [MUFFLE_UNTIL] — музыка под ролик: старт трека с OFFSET, fade-in 0.6 с, fade-out 1.8 с,
# громкость −14 LUFS / −1.5 dBTP. MUFFLE_UNTIL: до этой секунды звук «за стеной» (lowpass), затем плавно открывается за 0.9 с.
set -euo pipefail
IN=$1 OUT=$2 TR=$3 OFF=$4 MU=${5:-0}
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
FO=$(echo "$D - 1.8" | bc -l)
if [ "$MU" != 0 ]; then
  MIX="[1:a]atrim=start=$OFF:duration=$D,asetpts=PTS-STARTPTS,asplit[a][b];\
[a]lowpass=f=420,lowpass=f=420,volume=1.6,volume='if(lt(t,$MU),1,max(0,1-(t-$MU)/0.9))':eval=frame[m];\
[b]volume='if(lt(t,$MU),0,min(1,(t-$MU)/0.9))':eval=frame[o];[m][o]amix=inputs=2:normalize=0[mx]"
else
  MIX="[1:a]atrim=start=$OFF:duration=$D,asetpts=PTS-STARTPTS[mx]"
fi
ffmpeg -v error -y -i "$IN" -i "$TR" -filter_complex "$MIX;[mx]afade=t=in:d=0.6,afade=t=out:st=$FO:d=1.8,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -ac 2 -movflags +faststart -shortest "$OUT"
