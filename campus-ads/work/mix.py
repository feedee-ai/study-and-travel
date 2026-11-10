# mix.py VID — голос + музыка с дакингом под речь + SFX → VID/hf/assets/audio/mix.wav, −14 LUFS / −1.5 dBTP
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
VID = sys.argv[1]; STOCK = os.environ["STOCK"]
tm = json.load(open(f"{HERE}/../{VID}/timing.json")); T, X, DUR = tm["T"], tm["extra"], tm["DUR"]
VOICE = f"{HERE}/../{VID}/build/voice.wav"; OUT = f"{HERE}/../{VID}/hf/assets/audio/mix.wav"
WH, WH2, POP, SPK, BIG = ("s1490", 0.72), ("s1489", 0.71), ("s3005", 0.04), ("s2350", 0.96), ("s1492", 1.09)
EV = []
if VID == "v1":
    # Mixkit «Tears of Joy» (folk-pop: гитара, пианино) — тёплая ровная энергия под подачу фактов
    MUSIC, MOFF, MVOL, FOUT = "m839", 0.0, -10, 1.4
    for i, t in enumerate([T["mova"], T["f2"], T["f3"], T["f4"], T["f5"]]): EV.append(((WH, WH2)[i % 2], t, -15))
    EV.append((BIG, T["end0"] + 0.1, -12))
    for t in [0.02] + X["hookW"][2:4] + [T["par"], T["hud0"], T["b1"], T["b1"] + 0.45, T["meter"], T["spec"], T["chipTo"], T["bars"], T["dip"], T["badge"]] \
             + X["chipT"] + X["tagT"] + X["barT"]:
        EV.append((POP, t, -18))
    EV += [(POP, T["strike"] + 0.48, -10), (POP, T["tap"], -13)]
    EV += [(POP, 0.45, -16), (SPK, 0.85, -21), (POP, T["free"], -12), (SPK, T["free"] + 0.4, -18), (POP, T["b1"] - 0.3, -15)]
    EV += [(POP, T["b1"] + 0.05 + i * 0.09, -22) for i in range(7)]
    EV += [(WH2, T["spec"], -17), (POP, T["mdos"] - 0.1, -14), (POP, T["fut"], -16)]
    EV += [((WH, WH2)[i % 2], b["t"], -14) for i, b in enumerate(X["broll"])]
    EV += [(SPK, t, -20) for t in X["checks"]]
else:
    MUSIC, MOFF, MVOL, FOUT = X["music"], X["moff"], -10, 1.4
    for i, t in enumerate(X["whoosh"]): EV.append(((WH, WH2)[i % 2], t, -15))
    EV += [(POP, t, -18) for t in X["pops"]] + [(SPK, t, -20) for t in X["sparks"]] + [(BIG, X["big"], -12)]
inputs = ["-i", VOICE, "-ss", str(MOFF), "-t", str(DUR + 0.5), "-i", f"{STOCK}/{MUSIC}.mp3"]
fc = [f"[0:a]aresample=48000,apad=whole_dur={DUR}[vo]", "[vo]asplit[v1][vkey]",
      f"[1:a]aresample=48000,volume={MVOL}dB,afade=t=in:d=0.3,afade=t=out:st={DUR - FOUT}:d={FOUT}[mus]",
      "[mus][vkey]sidechaincompress=threshold=0.05:ratio=3:attack=30:release=350:makeup=1[md]"]
lab = []
for k, ((f, pk), t, db) in enumerate(EV):
    inputs += ["-i", f"{STOCK}/{f}.mp3"]; d = max(0, int(round((t - pk) * 1000)))
    fc.append(f"[{k + 2}:a]aresample=48000,volume={db}dB,adelay={d}|{d}[s{k}]"); lab.append(f"[s{k}]")
fc.append("[v1][md]" + "".join(lab) + f"amix=inputs={2 + len(lab)}:normalize=0:duration=first,atrim=0:{DUR}[mx]")
fcs = ";".join(fc)
m = subprocess.run(["ffmpeg", "-hide_banner", "-y"] + inputs + ["-filter_complex", fcs + ";[mx]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[o]",
                    "-map", "[o]", "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fcs + f";[mx]{ln},aresample=48000[o]",
                "-map", "[o]", "-ac", "2", "-c:a", "pcm_s16le", OUT], check=True)
print(OUT, "events", len(EV), "pre-norm", j["input_i"])
