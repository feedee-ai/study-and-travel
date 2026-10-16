# mix.py — финальный звук: голос + музыка (с дакингом под речь) + SFX → −14 LUFS / −1.5 dBTP
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STOCK = os.environ["STOCK"]
VOICE = f"{HERE}/build/voice.wav"
OUT = sys.argv[1]
tm = json.load(open(f"{HERE}/timing.json")); DUR = tm["DUR"]
MUSIC, MOFF = f"{STOCK}/m33.mp3", 7.06      # Mixkit «Motivating Mornings»: дроп трека (12.0 с) падает на старт списка (4.94)

# (файл, пик внутри файла, момент события в ролике, громкость dB)
WH = ("s1490", 0.72); WH2 = ("s1489", 0.71); POP = ("s3005", 0.04); SPK = ("s2350", 0.96); BIG = ("s1492", 1.09)
EV = []
for i, t in enumerate([3.55, 4.94, 6.30, 7.68, 9.62, 10.79, 16.07, 18.93, 20.02, 23.45, 24.91, 28.85]):
    EV.append(((WH, WH2)[i % 2], t, -15))
for t in [0.08, 2.74, 12.75, 14.86, 25.3, 25.66, 26.06, 26.5, 28.25, 29.93, 30.81]:
    EV.append((POP, t, -17))
EV += [(POP, 31.78, -14), (SPK, 24.2, -19), (BIG, 36.05, -12), (SPK, 36.6, -20)]

inputs = ["-i", VOICE, "-ss", str(MOFF), "-t", str(DUR + 0.5), "-i", MUSIC]
fc = ["[0:a]aresample=48000,apad=whole_dur=%s[vo]" % DUR,
      "[vo]asplit[v1][vkey]",
      f"[1:a]aresample=48000,volume=-13dB,afade=t=in:d=0.25,afade=t=out:st={DUR - 1.6}:d=1.6[mus]",
      "[mus][vkey]sidechaincompress=threshold=0.04:ratio=5:attack=25:release=400:makeup=1[md]"]
labels = []
for k, ((f, pk), t, db) in enumerate(EV):
    inputs += ["-i", f"{STOCK}/{f}.mp3"]
    delay = max(0, int(round((t - pk) * 1000)))
    fc.append(f"[{k + 2}:a]aresample=48000,volume={db}dB,adelay={delay}|{delay}[s{k}]")
    labels.append(f"[s{k}]")
fc.append("[v1][md]" + "".join(labels) + f"amix=inputs={2 + len(labels)}:normalize=0:duration=first,atrim=0:{DUR}[mx]")
fcs = ";".join(fc)
# двухпроходный loudnorm
m = subprocess.run(["ffmpeg", "-hide_banner", "-y"] + inputs + ["-filter_complex", fcs + ";[mx]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[o]",
                    "-map", "[o]", "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fcs + f";[mx]{ln},aresample=48000[o]",
                "-map", "[o]", "-ac", "2", "-c:a", "pcm_s16le", OUT], check=True)
print(OUT, j["input_i"])
