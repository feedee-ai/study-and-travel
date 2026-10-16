# voice.py SRC OUT — склейка речи по EDL (микрофейды 8 мс) + обработка голоса
import json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edl import segs
src, out = sys.argv[1], sys.argv[2]
S = segs(); parts = []
for i, s in enumerate(S):
    d = s['src_out'] - s['src_in']
    parts.append(f"[0:a]atrim={s['src_in']}:{s['src_out']},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={d-0.012:.3f}:d=0.012[a{i}]")
chain = ("highpass=f=80,afftdn=nf=-48:tn=1,"
         "equalizer=f=200:t=q:w=1.1:g=-2.5,equalizer=f=3200:t=q:w=1.2:g=2.2,equalizer=f=10000:t=h:w=0.7:g=1.8,"
         "deesser=i=0.3:m=0.5:f=0.5,"
         "acompressor=threshold=-24dB:ratio=3:attack=6:release=110:makeup=2,alimiter=limit=0.85:level=false,"
         "aresample=48000")
fc = ";".join(parts) + ";" + "".join(f"[a{i}]" for i in range(len(S))) + f"concat=n={len(S)}:v=0:a=1[c];[c]{chain}[v]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", fc, "-map", "[v]", "-ac", "2", "-c:a", "pcm_s24le", out], check=True)
print(out)
