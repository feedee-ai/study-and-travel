# Распознавание речи (Parakeet TDT 0.6b v3, sherpa-onnx) -> JSON со словами и таймкодами
import sys, json, glob, os
import sherpa_onnx, soundfile as sf
M = sys.argv[1]; out = sys.argv[3]
rec = sherpa_onnx.OfflineRecognizer.from_transducer(
    encoder=f"{M}/encoder.int8.onnx", decoder=f"{M}/decoder.int8.onnx",
    joiner=f"{M}/joiner.int8.onnx", tokens=f"{M}/tokens.txt",
    model_type="nemo_transducer", num_threads=4)
res = {}
for wav in sorted(glob.glob(sys.argv[2] + "/*.wav")):
    name = os.path.basename(wav)[:-4]
    if name == "gap": continue
    a, sr = sf.read(wav, dtype="float32")
    s = rec.create_stream(); s.accept_waveform(sr, a); rec.decode_stream(s)
    r = s.result
    # склейка BPE-токенов в слова
    words, cur, t0 = [], "", None
    for tok, ts in zip(r.tokens, r.timestamps):
        if tok.startswith(" ") or tok.startswith("▁"):
            if cur: words.append({"w": cur, "t": round(t0, 2)})
            cur, t0 = tok.strip(" ▁"), ts
        else:
            if t0 is None: t0 = ts
            cur += tok
    if cur: words.append({"w": cur, "t": round(t0, 2)})
    res[name] = {"text": r.text.strip(), "words": words, "dur": round(len(a) / sr, 2)}
    print(name, "|", r.text.strip(), flush=True)
json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
