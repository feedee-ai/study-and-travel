# Сборка A-roll по EDL: куски дублей -> plate.mp4 (1080x1920, 30 к/с, грейд) + voice.wav + words.json
# Запуск: /opt/asr/venv/bin/python -I edl.py edl.json
# Точки реза уточняются по минимуму громкости в окне ±SNAP с, чтобы не резать слово.
import sys, json, os, subprocess
import numpy as np, soundfile as sf

E = json.load(open(sys.argv[1]))
base = os.path.dirname(os.path.abspath(sys.argv[1]))
RAW = E["raw"]; OUT = os.path.join(base, E["out"]); os.makedirs(OUT, exist_ok=True)
TR = json.load(open(E["transcript"]))
SNAP = E.get("snap", 0.08)
TAIL = 1.0                       # стоп-кадр в конце plate.mp4, длина голоса не меняется
FPS = 30

def run(cmd):
    subprocess.run(cmd, check=True)

def find(name):
    for f in os.listdir(RAW):
        if f.startswith(name):
            return os.path.join(RAW, f)
    raise SystemExit("нет файла " + name)

_audio = {}
def audio(src):
    if src not in _audio:
        tmp = os.path.join(OUT, "_a_" + src + ".wav")
        run(["ffmpeg", "-v", "error", "-y", "-i", find(src), "-vn", "-ac", "1", "-ar", "48000", tmp])
        a, _ = sf.read(tmp, dtype="float32"); os.remove(tmp)
        _audio[src] = a
    return _audio[src]

def snap(src, t):
    a = audio(src); sr = 48000; w = int(0.02 * sr)
    best, bt = None, t
    for k in np.arange(-SNAP, SNAP + 1e-6, 0.01):
        c = t + k
        i = int(c * sr)
        if i - w < 0 or i + w > len(a):
            continue
        e = float(np.sqrt(np.mean(a[i - w:i + w] ** 2)))
        if best is None or e < best - 1e-5:
            best, bt = e, c
    return round(bt, 3)

# длительность каждого куска — целое число кадров, чтобы картинка и звук не расходились
segs, t = [], 0.0
for s in E["segments"]:
    i0 = snap(s["src"], s["in"]) if s.get("snap", True) else s["in"]
    i1 = snap(s["src"], s["out"]) if s.get("snap", True) else s["out"]
    n = max(1, round((i1 - i0) * FPS)); d = n / FPS
    segs.append({**s, "in": i0, "out": i0 + d, "dur": d, "t0": round(t, 4)})
    t += d
total = t

# видео: каждый кусок отдельно (кадрирование/грейд), затем concat без перекодирования параметров
parts = []
for k, s in enumerate(segs):
    p = os.path.join(OUT, f"_v{k:02d}.mp4"); parts.append(p)
    vf = E["vf"].get(s["src"], E["vf"]["*"]) if isinstance(E["vf"], dict) else E["vf"]
    if s.get("zoom"):
        # zoom: [s, fx, fy] — наезд в s раз с неподвижной точкой (fx,fy); [s, fx, fy, tx, ty] — точка (fx,fy) уезжает в (tx,ty)
        z = s["zoom"]; zk, fx, fy = z[0], z[1], z[2]; tx, ty = (z[3], z[4]) if len(z) > 3 else (fx, fy)
        w, h = 1080 / zk, 1920 / zk
        x0 = min(max(fx - tx / zk, 0), 1080 - w); y0 = min(max(fy - ty / zk, 0), 1920 - h)
        vf += f",scale=2160:3840:flags=lanczos,crop={w*2:.0f}:{h*2:.0f}:{x0*2:.0f}:{y0*2:.0f},scale=1080:1920:flags=lanczos"
    last = k == len(segs) - 1           # последний кусок — плюс 1 с стоп-кадра под энд-кард
    tail = f",tpad=stop_mode=clone:stop_duration={TAIL}" if last else ""
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['in']:.3f}", "-t", f"{s['dur']:.4f}", "-i", find(s["src"]), "-an",
         "-vf", f"fps={FPS},{vf}{tail},setsar=1,format=yuv420p", "-frames:v", str(round((s["dur"] + (TAIL if last else 0)) * FPS)),
         "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-g", "15", "-pix_fmt", "yuv420p",
         "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", p])
lst = os.path.join(OUT, "_list.txt")
open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart",
     os.path.join(OUT, "plate.mp4")])
for p in parts: os.remove(p)
os.remove(lst)

# звук: куски с короткими фейдами 8 мс на стыках, затем чистка и громкость
sr = 48000; fade = int(0.008 * sr); chunks = []
for s in segs:
    a = audio(s["src"]); i0 = int(round(s["in"] * sr)); n = int(round(s["dur"] * sr))
    c = a[i0:i0 + n].copy()
    if len(c) < n: c = np.pad(c, (0, n - len(c)))
    r = np.linspace(0, 1, fade, dtype="float32"); c[:fade] *= r; c[-fade:] *= r[::-1]
    chunks.append(c)
raw = os.path.join(OUT, "_voice_raw.wav")
sf.write(raw, np.concatenate(chunks), sr)
run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", E.get("af",
     "highpass=f=80,afftdn=nr=10:nf=-45,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-15:TP=-1.5:LRA=7"),
     "-ar", "48000", "-ac", "2", os.path.join(OUT, "voice.wav")])
os.remove(raw)

# слова на выходной шкале времени (конец слова = начало следующего, но не позже конца куска)
words = []
for k, s in enumerate(segs):
    W = TR[s["src"]]["words"]
    for j, w in enumerate(W):
        if s["in"] - 0.06 <= w["t"] < s["out"] - 0.05:
            nxt = W[j + 1]["t"] if j + 1 < len(W) else s["out"]
            end = min(nxt, s["out"])
            words.append({"w": w["w"], "t": round(s["t0"] + w["t"] - s["in"], 3),
                          "e": round(s["t0"] + end - s["in"], 3), "seg": k, "tag": s.get("tag", "")})
json.dump({"duration": round(total, 4), "segments": segs, "words": words},
          open(os.path.join(OUT, "edl_out.json"), "w"), ensure_ascii=False, indent=1)
print(f"готово: {len(segs)} кусков, {total:.2f} с -> {OUT}")
for k, s in enumerate(segs):
    print(f"{k:2d} {s['t0']:6.2f} {s['src']:9s} {s['in']:6.2f}-{s['out']:6.2f} {s.get('tag','')}")
