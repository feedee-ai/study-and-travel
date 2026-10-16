# prep.py — готовит видео для композиции: лицо по EDL и B-roll (кроп 9:16, грейд, 30 к/с, 1080x1920)
import json, subprocess, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edl import segs
SRC = os.environ['SRC']; STOCK = os.environ['STOCK']; OUT = os.environ['OUT']
os.makedirs(OUT, exist_ok=True)
GRAIN = "noise=alls=5:allf=t"
FACE_GRADE = "hqdn3d=1.2:1.2:3:3,eq=contrast=1.06:saturation=0.94:gamma=0.98,curves=all='0/0.02 0.5/0.5 1/0.98'"
STOCK_GRADE = "eq=contrast=1.04:saturation=0.86:gamma=1.0,colortemperature=temperature=5700:mix=0.35,curves=all='0/0.035 0.5/0.5 1/0.97'"
ENC = ["-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", "-an",
       "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
def run(args): subprocess.run(["ffmpeg", "-v", "error", "-y"] + args, check=True)

# 1. лицо: склейка по EDL → 1080x1920
S = segs(); parts = []
for i, s in enumerate(S):
    parts.append(f"[0:v]trim={s['src_in']}:{s['src_out']},setpts=PTS-STARTPTS[v{i}]")
fc = ";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(len(S))) + f"concat=n={len(S)}:v=1:a=0[c];" \
     f"[c]fps=30,scale=1080:-2:flags=lanczos,crop=1080:1920:0:22,{FACE_GRADE},unsharp=5:5:0.75:5:5:0,{GRAIN},setsar=1,format=yuv420p[o]"
if not os.path.exists(f"{OUT}/face.mp4") or os.environ.get('FORCE'):
    run(["-i", SRC, "-filter_complex", fc, "-map", "[o]"] + ENC + [f"{OUT}/face.mp4"])

# 2. B-roll: (имя, клип, старт в исходнике, длительность, центр кропа по x, скорость)
BROLL = [
    ("castle",   "v31447", 1.0, 1.9, 0.50, 1.0),
    ("uni",      "v4503",  3.0, 1.8, 0.47, 1.0),
    ("docs",     "v46533", 8.2, 1.8, 0.56, 1.0),
    ("room",     "v4029", 32.0, 2.4, 0.62, 1.0),
    ("keys",     "v12877", 0.2, 1.6, 0.50, 1.0),
    ("barista",  "v24405", 6.0, 1.9, 0.43, 1.0),
    ("town",     "v4235",  0.4, 3.3, 0.24, 1.0),
    ("suitcase", "v45507", 1.0, 1.6, 0.52, 1.0),
    ("campus",   "v4519",  4.0, 2.5, 0.55, 1.0),
    ("grad",     "v49461", 1.4, 2.0, 0.38, 1.0),
    ("hug",      "v49462", 1.5, 2.9, 0.45, 1.0),
    ("webinar",  "v49282", 0.0, 2.4, 0.68, 1.0),
]
for name, clip, ss, dur, xc, sp in BROLL:
    o = f"{OUT}/{name}.mp4"
    if os.path.exists(o) and not os.environ.get('FORCE'): continue
    vf = (f"setpts=(PTS-STARTPTS)/{sp},fps=30,crop=ih*9/16:ih:max(0\\,min(iw-ih*9/16\\,iw*{xc}-ih*9/32)):0,"
          f"scale=1080:1920:flags=lanczos,{STOCK_GRADE},unsharp=5:5:0.5:5:5:0,{GRAIN},setsar=1,format=yuv420p")
    run(["-ss", str(ss), "-t", str(dur * sp + 0.6), "-i", f"{STOCK}/{clip}.mp4", "-vf", vf, "-t", str(dur + 0.4)] + ENC + [o])
    print(name, "ok")
