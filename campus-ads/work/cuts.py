# cuts.py VID — находит реальные кадры склеек в plate.mp4 (рядом с границами из EDL) → VID/plate_cuts.json.
# Склейка кусков квантуется по кадрам, поэтому зум и смена сцен должны вставать на фактический кадр склейки.
import json, os, subprocess, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); VID = sys.argv[1]
E = json.load(open(f"{HERE}/../{VID}/edl.json"))
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{HERE}/../{VID}/hf/assets/media/plate.mp4", "-vf", "scale=64:114,format=gray",
                      "-f", "rawvideo", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 114, 64).astype(np.float32)
diff = np.r_[0, np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))]   # diff[i] — скачок на входе в кадр i
cuts = [0.0]
for s in E["segs"][1:]:
    c = int(round(s["out_in"] * 30)); lo, hi = max(1, c - 4), min(len(diff) - 1, c + 4)
    i = lo + int(np.argmax(diff[lo:hi + 1]))
    cuts.append(round(i / 30, 4))
    print(f"{s['clip']}: EDL {s['out_in']:.3f} → кадр {i} ({i / 30:.3f}), скачок {diff[i]:.1f}")
json.dump(cuts, open(f"{HERE}/../{VID}/plate_cuts.json", "w"))
