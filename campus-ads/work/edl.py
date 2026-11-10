# edl.py — монтажные листы двух роликов: куски исходников (уже по порядку), ускорение,
# слова с таймингами в выходном времени (Parakeet v3 → правки текста).
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
ASR = json.load(open(f"{HERE}/asr_parakeet.json"))

# (клип, вход, выход) в секундах исходника
CUTS = {
    "v1": dict(speed=1.12, segs=[
        ("IMG_1975", 0.06, 5.03),   # хук: 4 речі
        ("IMG_1977", 0.55, 5.99),   # 1 мова: …реально вчити
        ("IMG_1977", 8.13, 14.60),  #   Тому Study and Travel готує … до вступу
        ("IMG_1978", 0.00, 9.31),   # 2 без іспитів … саме під вашу дитину
        ("IMG_1981", 0.00, 9.40),   # 3 місця та дедлайни
        ("IMG_1979", 0.40, 8.26),   # 4 а головне … і будувати власне майбутнє
        ("IMG_1982", 0.00, 6.92),   # CTA: якщо … до вступу
        ("IMG_1982", 8.94, 13.00),  #   тисніть «Детальніше» …
    ]),
    "v2": dict(speed=1.10, segs=[
        ("IMG_1983", 0.20, 8.30),   # мрія: диплом, заробіток, подорожі, майбутнє
        ("IMG_1984", 0.50, 14.68),  # доступно, мова, не одна, куратор (хвост поджат)
        ("IMG_1985", 0.85, 5.75),   # але щоб усе це стало реальністю
        ("IMG_1986", 0.20, 12.02),  # Study and Travel на кожному етапі
        ("IMG_1987", 0.08, 9.10),   # CTA: заявка на консультацію
    ]),
}

# правки распознавания: (клип, слово как распознано) → замена (несколько слов делят его время)
FIX = {
    ("IMG_1978", "іспіти"): "іспитів", ("IMG_1978", "спеціальності,"): "спеціальностей,",
    ("IMG_1978", "дитину,"): "дитину.",
    ("IMG_1982", "вступу"): "вступу.", ("IMG_1982", "Тисні"): "Тисніть", ("IMG_1982", "детальніше,"): "«Детальніше»",
    ("IMG_1982", "ти"): "та", ("IMG_1977", "вчити,"): "вчити.",
    ("IMG_1986", "Під"): "Від", ("IMG_1986", "вибори"): "вибору", ("IMG_1986", "вивченням,"): "вивченням", ("IMG_1986", "мовою,"): "мови,",
    ("IMG_1987", "заяку"): "заявку", ("IMG_1983", "словаччині"): "Словаччині", ("IMG_1977", "так,"): "— так,",
}
BRAND = re.compile(r"^(стаді|стадія|стадієн|стадіан|стадіїн|stadion)", re.I)

def clip_words(clip):
    v = ASR[clip]; W = []
    for tok, t in zip(v["tokens"], v["ts"]):
        if tok.startswith(" ") or not W: W.append(dict(w=tok.strip(), s=t, last=t))
        else: W[-1]["w"] += tok; W[-1]["last"] = t
    for i, w in enumerate(W):
        w["e"] = min(w["last"] + 0.2, W[i + 1]["s"] if i + 1 < len(W) else w["last"] + 0.3)
    out, i = [], 0
    while i < len(W):
        w = W[i]
        if BRAND.match(w["w"]):
            j = i + 1 if (i + 1 < len(W) and W[i + 1]["w"].lower().startswith("тревел")) else i
            s, e = w["s"], W[j]["e"]; tail = re.sub(r"^.*?([,.?!]*)$", r"\1", W[j]["w"])
            parts = ["Study", "and", "Travel" + tail]; d = (e - s) / 3
            out += [dict(w=p, s=s + k * d, e=s + (k + 1) * d) for k, p in enumerate(parts)]; i = j + 1; continue
        w = dict(w=FIX.get((clip, w["w"]), w["w"]), s=w["s"], e=w["e"])
        for k, p in enumerate(w["w"].split()):
            n = len(w["w"].split()); d = (w["e"] - w["s"]) / n
            out.append(dict(w=p, s=w["s"] + k * d, e=w["s"] + (k + 1) * d))
        i += 1
    return out

def build(vid):
    c = CUTS[vid]; sp = c["speed"]; t = 0.0; segs, words = [], []
    for clip, a, b in c["segs"]:
        d = (b - a) / sp
        segs.append(dict(clip=clip, src_in=a, src_out=b, out_in=round(t, 3), out_out=round(t + d, 3)))
        for w in clip_words(clip):
            if (w["s"] >= a - 0.05 or a < 0.2) and w["s"] < b - 0.05:
                words.append(dict(w=w["w"], s=round(t + max(0, w["s"] - a) / sp, 3), e=round(t + min(b - a, w["e"] - a) / sp, 3), seg=len(segs) - 1))
        t += d
    return dict(speed=sp, segs=segs, words=words, dur=round(t, 3))

if __name__ == "__main__":
    for vid in CUTS:
        r = build(vid); os.makedirs(f"{HERE}/../{vid}", exist_ok=True)
        json.dump(r, open(f"{HERE}/../{vid}/edl.json", "w"), ensure_ascii=False, indent=1)
        print(vid, "speech", r["dur"]); print("  " + " ".join(f"{w['w']}" for w in r["words"]))
