#!/bin/bash
# Общие функции сборки подложки: кадр из исходника → 1080x1920, 30 к/с, SDR BT.709, грейд, плавный наезд.
set -euo pipefail
HA="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAT="$HA/material"

TONEMAP="zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
# Тёплый мягкий грейд; гасит фиолетовую LED-подсветку (magenta/blue).
GRADE_WARM="huesaturation=saturation=-1:colors=m:strength=40,huesaturation=saturation=-0.6:colors=b:strength=20,huesaturation=hue=-25:saturation=-0.3:colors=m:strength=40,colortemperature=temperature=5600:mix=0.35,eq=contrast=0.95:saturation=1.04:gamma=1.03,curves=all='0/0.035 0.5/0.51 1/0.975'"
# Для leda_2235 (SDR, рыжее остальных): чуть меньше насыщенности и теплоты.
GRADE_LD="$GRADE_WARM,eq=saturation=0.84,colortemperature=temperature=7000:mix=0.3"
# Для luda_3348/3336 (очень светлый блонд выглядит выбеленным): плотнее, теплее.
GRADE_L48="$GRADE_WARM,eq=gamma=0.86:contrast=1.07:saturation=1.12,colortemperature=temperature=4700:mix=0.25"
# Для root_a11e кусков со стулом (смонтированный рилс со своим «светлым» фильтром): плотнее, теплее.
GRADE_RA="$GRADE_WARM,eq=gamma=0.90:saturation=0.74,colorbalance=gm=-0.07:gh=-0.05:rm=0.03:bm=0.02,colortemperature=temperature=4900:mix=0.15"
# Сток (Альпы и т.п.): чуть мягче контраст, меньше «стоковой» синевы, тёплый оттенок как у серии.
GRADE_STOCK="eq=contrast=0.95:saturation=0.82:gamma=1.02,colortemperature=temperature=5900:mix=0.3,curves=all='0/0.04 0.5/0.51 1/0.97'"
# Холодный приглушённый «до» (02 PAIN).
GRADE_COLD="huesaturation=saturation=-1:colors=m:strength=40,colortemperature=temperature=8200:mix=0.45,eq=contrast=1.04:saturation=0.55:gamma=0.97,curves=all='0/0.05 0.5/0.47 1/0.93',noise=alls=7:allf=t"

# shot OUT SRC START DUR SPEED Z0 Z1 [GRADE] [XSHIFT]
#   DUR — длительность на выходе (с); SPEED — 0.5 = слоу-мо ×2; Z0→Z1 — масштаб (наезд, кривая sine.inOut по логарифму масштаба)
#   XSHIFT — сдвиг центра кадрирования по горизонтали в долях ширины (−0.2…0.2)
shot() {
  local out=$1 src=$2 ss=$3 dur=$4 sp=$5 z0=$6 z1=$7 grade=${8:-$GRADE_WARM} xs=${9:-0}
  [ -s "$out" ] && [ "${FORCE:-0}" != 1 ] && return 0   # кэш: удалите файл, чтобы пересобрать
  local f="$MAT/$src" pre=""
  [ "$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of csv=p=0 "$f")" = "arib-std-b67" ] && pre="$TONEMAP,"
  local geo; geo=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 "$f")
  local w h r; IFS=, read -r w h r <<< "$geo"
  local pre_crop="" fpsf="fps=30"
  [ "$w" -gt "$h" ] && pre_crop="crop=trunc(ih*9/16/2)*2:ih:(iw-ih*9/16)/2+iw*${XS0:-0}:0,"
  [ "$r" = "24000/1001" ] || [ "$r" = "24/1" ] || [ "$r" = "25/1" ] && fpsf="framerate=fps=30"
  local srcdur; srcdur=$(echo "$dur*$sp+0.2" | bc -l | sed "s/^\./0./")
  # масштаб: z(t) = z0 * (z1/z0)^S(t/dur), S = sine.inOut; рендер в 2× для субпиксельной точности
  local Z="($z0*pow($z1/$z0,0.5-0.5*cos(PI*min(t/$dur,1))))"
  ffmpeg -v error -y -ss "$ss" -t "$srcdur" -i "$f" -an -vf "\
setpts=(PTS-STARTPTS)/$sp,${fpsf},${pre}${pre_crop}scale=2160:3840:flags=lanczos,${grade},\
scale=w='trunc(2160*$Z/2)*2':h='trunc(3840*$Z/2)*2':eval=frame:flags=bicubic,\
crop=2160:3840:'(iw-2160)/2+iw*$xs':'(ih-3840)/2',scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p" \
    -t "$dur" -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p \
    -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 "$out"
}

# xfade_chain OUT D clip1 clip2 ...  — растворения длиной D между всеми клипами
xfade_chain() {
  local out=$1 d=$2; shift 2
  local inputs=() filter="" prev="[0:v]" off=0 i=0
  for c in "$@"; do inputs+=(-i "$c"); done
  local n=$#
  local durs=(); for c in "$@"; do durs+=("$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$c")"); done
  off=$(echo "${durs[0]} - $d" | bc -l | sed "s/^\./0./")
  for ((i=1;i<n;i++)); do
    local o="[v$i]"; [ $i -eq $((n-1)) ] && o="[vout]"
    filter+="${prev}[$i:v]xfade=transition=fade:duration=$d:offset=$off${o};"
    prev="[v$i]"
    off=$(echo "$off + ${durs[$i]} - $d" | bc -l | sed "s/^\./0./")
  done
  ffmpeg -v error -y "${inputs[@]}" -filter_complex "${filter%;}" -map "[vout]" -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p \
    -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 "$out"
}

# concat_hard OUT clip1 clip2 ... — жёсткие склейки
concat_hard() {
  local out=$1; shift; local lst; lst=$(mktemp)
  for c in "$@"; do echo "file '$c'" >> "$lst"; done
  ffmpeg -v error -y -f concat -safe 0 -i "$lst" -c copy "$out"; rm -f "$lst"
}

# xfade_seq OUT clip1 TRANS D clip2 TRANS D clip3 ... — переходы разных типов (fade, smoothleft, ...); печатает старты клипов
xfade_seq() {
  local out=$1; shift
  local clips=() trans=() ds=()
  clips+=("$1"); shift
  while [ $# -gt 0 ]; do trans+=("$1"); ds+=("$2"); clips+=("$3"); shift 3; done
  local inputs=() filter="" prev="[0:v]" n=${#clips[@]} i
  for c in "${clips[@]}"; do inputs+=(-i "$c"); done
  local start=0 dur; dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "${clips[0]}")
  echo "start ${clips[0]} 0" >&2
  for ((i=1;i<n;i++)); do
    local d=${ds[$((i-1))]} t=${trans[$((i-1))]}
    start=$(echo "$start + $dur - $d" | bc -l | sed "s/^\./0./")
    local o="[v$i]"; [ $i -eq $((n-1)) ] && o="[vout]"
    filter+="${prev}[$i:v]xfade=transition=$t:duration=$d:offset=$start${o};"
    prev="[v$i]"; dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "${clips[$i]}")
    printf "start %s %.3f\n" "${clips[$i]}" "$start" >&2
  done
  printf "end %.3f\n" "$(echo "$start + $dur" | bc -l)" >&2
  ffmpeg -v error -y "${inputs[@]}" -filter_complex "${filter%;}" -map "[vout]" -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p \
    -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 "$out"
}
