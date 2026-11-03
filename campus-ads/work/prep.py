# prep.py VID — подложка (склейка кусков, HLG→SDR, 30 к/с, ускорение) и голос по edl.json
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
VID = sys.argv[1]; SRC = os.environ["SRC"]
E = json.load(open(f"{HERE}/../{VID}/edl.json")); sp = E["speed"]
MEDIA = f"{HERE}/../{VID}/hf/assets/media"; BUILD = f"{HERE}/../{VID}/build"
os.makedirs(MEDIA, exist_ok=True); os.makedirs(BUILD, exist_ok=True)
TONEMAP = "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
GRADE = "eq=contrast=1.04:saturation=1.03:gamma=0.99,curves=all='0/0.02 0.5/0.5 1/0.985'"
VOICE = ("highpass=f=95,afftdn=nf=-30:tn=1,afftdn=nf=-40,"
         "equalizer=f=180:t=q:w=1.1:g=-2,equalizer=f=3200:t=q:w=1.2:g=2.5,equalizer=f=10000:t=h:w=0.7:g=1.5,"
         "deesser=i=0.3:m=0.5:f=0.5,acompressor=threshold=-24dB:ratio=3:attack=6:release=110:makeup=2,alimiter=limit=0.85:level=false")
ins, fv, fa = [], [], []
for i, s in enumerate(E["segs"]):
    ins += ["-ss", str(s["src_in"]), "-t", str(s["src_out"] - s["src_in"]), "-i", f"{SRC}/{s['clip']}.MOV"]
    d = (s["src_out"] - s["src_in"]) / sp
    fv.append(f"[{i}:v]{TONEMAP},fps=30,setpts=(PTS-STARTPTS)/{sp},{GRADE},scale=1080:1920:flags=lanczos,setsar=1,trim=0:{d:.4f}[v{i}]")
    fa.append(f"[{i}:a]aresample=48000,asetpts=PTS-STARTPTS,atempo={sp},atrim=0:{d:.4f},afade=t=in:d=0.012,afade=t=out:st={d - 0.03:.4f}:d=0.03[a{i}]")
n = len(E["segs"])
fc = ";".join(fv + fa) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[vo];" + \
     "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[ac];[ac]{VOICE}[ao]"
subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", fc,
    "-map", "[vo]", "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p", "-an",
    "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", f"{MEDIA}/plate.mp4",
    "-map", "[ao]", "-ac", "2", "-c:a", "pcm_s24le", f"{BUILD}/voice.wav"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{MEDIA}/plate.mp4", "-vf", "scale=540:960:flags=lanczos", "-c:v", "libx264",
                "-crf", "18", "-pix_fmt", "yuv420p", "-an", f"{MEDIA}/plate_small.mp4"], check=True)
print(VID, "ok", E["dur"])
