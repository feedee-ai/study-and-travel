#!/bin/bash
# strip.sh DIR — все frame-*.png из DIR в одну сетку (6 в ряд, 300 px) → DIR/strip.jpg
d=$1; fs=($(ls $d/frame-*.png | sort -V)); n=${#fs[@]}; a=(); f=""
for ((i=0;i<n;i++)); do a+=(-i "${fs[$i]}"); t=$(basename ${fs[$i]} .png | sed 's/.*-at-//'); f+="[$i:v]scale=300:-2,drawtext=text='$t':x=6:y=6:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.5[v$i];"; done
cols=6; rows=$(( (n+cols-1)/cols )); for ((i=0;i<n;i++)); do f+="[v$i]"; done
ffmpeg -nostdin -v error -y "${a[@]}" -filter_complex "${f}xstack=inputs=$n:layout=$(python3 -c "print('|'.join(f'{(i%$cols)*300}_{(i//$cols)*534}' for i in range($n)))"):fill=black" -q:v 4 $d/strip.jpg
