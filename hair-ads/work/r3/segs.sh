#!/bin/bash
# R3: чистые вертикальные куски 1080x1920 (тонмап HLG→SDR, грейд, без наездов — движение делает HyperFrames)
set -euo pipefail
cd "$(dirname "$0")"; source ../lib.sh
# тёплый мягкий (люкс): гасим розовую щётку и фиолетовые расчёски, мягкий контраст, приподнятые тени
W="huesaturation=saturation=-0.85:colors=m:strength=40,huesaturation=saturation=-0.5:colors=b:strength=25,colortemperature=temperature=5500:mix=0.3,eq=contrast=0.98:saturation=0.98:gamma=1.02,curves=all='0/0.03 0.5/0.505 1/0.975'"
# холодный «мороз»
ICE="colortemperature=temperature=9500:mix=0.55,eq=saturation=0.55:contrast=1.04:gamma=1.0,curves=all='0/0.045 0.5/0.48 1/0.96':b='0/0.07 1/1'"
s(){ shot seg/$1.mp4 "$2" "$3" "$4" "$5" 1.0 1.0 "$6"; }
# --- Winter
s w_alps  stock/mk_4283-2160.mp4 1.0 3.2 1.0 "$ICE,eq=saturation=0.8"
s w_frizz new/joa_5744.mov 15.2 2.7 0.8 "$ICE"
s w_p1    new/mur_5683.mov 5.0 2.6 0.9 "$ICE"
s w_p2    new/lud_4664.mov 1.5 2.6 0.9 "$ICE"
s w_p3    new/joa_5744.mov 21.4 2.6 0.9 "$ICE"
s w_mixc  new/det_5587.mov 0.8 2.2 0.7 "$ICE"
s w_mixw  new/det_5587.mov 0.8 2.2 0.7 "$W"
s w_iron  new/ann_5489.mov 135 1.8 0.8 "$W"
s w_swing new/mur_5693.mov 9.0 5.6 0.6 "$W"
# --- Arrival
s a_tools new/lud_4666.mov 2.6 2.8 1.0 "$W"
s a_face  new/lud_4688.mov 3.6 2.4 0.9 "$W"
s a_mix   new/det_5585.mov 3.0 2.0 0.7 "$W"
s a_comb  new/lud_4700.mov 4.0 2.0 0.9 "$W"
s a_iron  new/ann_5489.mov 160 1.8 0.8 "$W"
s a_rev   new/ann_5495.mov 11.0 3.8 0.7 "$W"
s a_end   new/ann_5500.mov 7.4 4.4 0.6 "$W"
# --- Glass
s g_macro new/mur_5694.mov 13.0 2.2 0.6 "$W"
s g_m1    new/joa_5750.mov 3.2 0.9 0.8 "$W"
s g_m2    new/ann_5494.mov 58 0.9 0.8 "$W"
s g_m3    new/mur_5693.mov 0.2 0.9 0.8 "$W"
s g_m4    new/ann_5563.mov 3.0 0.9 0.8 "$W"
s g_m5    new/joa_5749.mov 26 0.9 0.8 "$W"
s g_m6    new/ann_5500.mov 4.2 0.9 0.8 "$W"
s g_hand  new/joa_5750.mov 10.0 2.8 0.6 "$W"
s g_swing new/mur_5693.mov 9.0 3.0 0.6 "$W"
s g_end   new/ann_5563.mov 20 4.4 0.6 "$W"
# --- Meet Alena
s m_face  new/lud_4688.mov 3.4 2.8 0.9 "$W"
s m_full  new/lud_4691.mov 0.2 2.6 0.9 "$W"
s m_lean  new/lud_4690.mov 5.8 3.0 0.9 "$W"
s m_mix   new/det_5584.mov 1.0 2.0 0.7 "$W"
s m_res1  new/lud_4744.mov 17.5 2.2 0.8 "$W"
s m_res2  new/ann_5500.mov 7.4 2.2 0.6 "$W"
s m_end   new/ann_5495.mov 14 4.4 0.7 "$W"
# --- Client's words
s c_q     new/ann_5494.mov 20 4.0 0.6 "$W"
s c_proc  new/ann_5487.mov 80 2.0 0.9 "$W"
s c_iron  new/ann_5489.mov 136 1.8 0.8 "$W"
s c_res   new/ann_5495.mov 6.0 2.6 0.7 "$W"
s c_end   new/ann_5494.mov 60 4.4 0.6 "$W"
# --- Classic
s k1      new/ann_5563.mov 3.0 2.0 0.7 "$W"
s k2      new/joa_5750.mov 3.4 1.8 0.7 "$W"
s k3      new/mur_5693.mov 9.2 2.0 0.6 "$W"
s k_b     new/joa_5744.mov 12.0 2.8 0.8 "$W"
s k_a     new/joa_5749.mov 27 2.8 0.8 "$W"
s k_alena new/lud_4692.mov 5.0 2.4 0.9 "$W"
s k_res   new/ann_5495.mov 11 2.6 0.7 "$W"
s k_end   new/mur_5694.mov 6.0 4.4 0.6 "$W"
echo SEGS_DONE
# --- Client's words v2 (отзыв → процесс и процедуры → результаты разных клиенток)
s c_q2    new/ann_5494.mov 20 4.8 0.6 "$W"
s c_tools new/lud_4665.mov 2.6 2.8 1.0 "$W"
s c_drip  new/det_5588.mov 50.5 1.9 0.6 "$W"
s c_apply new/lud_4700.mov 11.0 1.8 0.9 "$W"
s c_r1    new/mur_5693.mov 9.0 2.3 0.6 "$W"
s c_r2    new/joa_5749.mov 3.6 2.3 0.6 "$W"
s c_r3    new/ann_5563.mov 24 5.6 0.6 "$W"
