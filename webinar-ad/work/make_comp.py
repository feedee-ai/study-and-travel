# make_comp.py — собирает hf/index.html из index.src.html: тайминги сцен, B-roll, субтитры (из words.json)
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
HF = os.path.join(HERE, "..", "hf")
W = json.load(open(f"{HERE}/words.json"))
# «тисяча двісті» → «1200»
for i, w in enumerate(W):
    if w["w"] == "тисяча" and W[i + 1]["w"] == "двісті":
        w["w"], w["e"] = "1200", W[i + 1]["e"]; W[i + 1]["drop"] = True
W = [w for w in W if not w.get("drop")]

VDUR = 36.23          # конец речи / видео спикера
END0 = 36.0          # старт финальной карточки
DUR = 38.6

T = dict(free=2.74, country=3.62, list0=4.94, list1=12.29, more0=12.75, more1=14.2,
         web0=14.86, web1=16.07, route0=16.1, routeDraw=2.1, route1=18.93,
         steps0=18.95, stepsMid=20.6, steps1=22.04, count0=23.05, count1=24.91, q1=27.38,
         mq=28.25, ma=29.93, chat1=30.71, cta0=30.73, tap=31.6, end0=END0)

# B-roll: id, файл, старт, конец, въезд (R — справа, L — слева, cut — склейка), зум от/до
BR = [("castle", 3.55, 4.94, "cut", 1.22, 1.04), ("uni", 4.94, 6.30, "R", 1.10, 1.0), ("docs", 6.30, 7.68, "L", 1.10, 1.0),
      ("grocery", 7.68, 9.62, "R", 1.10, 1.0), ("dorm", 9.62, 10.79, "L", 1.12, 1.0), ("barista", 10.79, 12.29, "R", 1.10, 1.0),
      ("town", 16.07, 18.93, "cut", 1.18, 1.0), ("suitcase", 18.93, 20.02, "R", 1.10, 1.0), ("campus", 20.02, 22.04, "R", 1.10, 1.0),
      ("grad", 23.45, 24.91, "cut", 1.14, 1.0), ("hug", 24.91, 27.38, "R", 1.10, 1.0), ("webinar", 28.85, 30.71, "cut", 1.12, 1.0)]
broll_html, broll_data = [], []
for i, (bid, a, b, enter, z0, z1) in enumerate(BR):
    nxt = BR[i + 1] if i + 1 < len(BR) else None
    overlap = 0.34 if nxt and abs(nxt[1] - b) < 1e-6 and nxt[3] in "RL" else 0.0
    d = round(b - a + overlap, 3)
    broll_html.append(f'  <div class="vw" id="bw-{bid}"><div class="vz" id="bz-{bid}"><video id="v-{bid}" class="clip full" data-start="{a}" '
                      f'data-duration="{d}" data-track-index="{i + 1}" src="assets/media/{bid}.mp4" muted playsinline></video></div></div>')
    broll_data.append(dict(id=bid, t=a, d=b - a, enter={"R": "left", "L": "right"}.get(enter, "cut"), z0=z0, z1=z1))

# спикер: [время, зум от, до, длительность]
FZ = [(0, 1.16, 1.03, 3.55), (12.29, 1.0, 1.03, 1.95), (14.24, 1.10, 1.12, 0.62), (14.86, 1.17, 1.19, 1.21),
      (22.04, 1.06, 1.09, 1.41), (27.38, 1.0, 1.03, 1.47), (30.71, 1.03, 1.07, 2.34), (33.05, 1.14, 1.17, 3.2)]
BUB = [(4.94, 12.29), (16.07, 22.04), (23.45, 24.91)]

# список: 5 пунктов, ключевое слово — жёлтым
ITEMS = [(4.94, 6.30, "Як обрати університет?", "університет?"),
         (6.30, 7.68, "Які документи підготувати?", "документи"),
         (7.68, 9.62, "Скільки коштуватиме проживання?", "проживання?"),
         (9.62, 10.79, "Де житиме студент?", "житиме"),
         (10.79, 12.29, "Скільки він може заробляти?", "заробляти?")]
def wt(word, t0, t1):
    base = re.sub(r"[^\w']", "", word.lower())
    for w in W:
        if t0 - 0.3 <= w["s"] <= t1 and re.sub(r"[^\w']", "", w["w"].lower()) == base: return w["s"]
    raise KeyError((word, t0))
items_html, items_data = [], []
for i, (a, b, text, key) in enumerate(ITEMS):
    ws = text.split()
    ems = "".join(f'<em class="{"k" if w == key else ""}">{w}</em>' for w in ws)
    items_html.append(f'  <div class="item" id="it{i}" style="opacity:0"><div class="num"><b>0{i + 1}</b><span>/ 05</span></div><div class="st">{ems}</div></div>')
    items_data.append(dict(s=a, e=b, w=[dict(s=max(a, wt(w, a, b) - 0.04)) for w in ws]))

# субтитры: куски по 1–3 слова, рвём на пунктуации; в списке и на финале — без субтитров
HIDE = [(4.94, 12.29), (END0 + 0.25, 99)]
def hidden(t): return any(a - 0.05 <= t < b for a, b in HIDE)
SMALL = {"у", "в", "на", "до", "і", "та", "ще", "що", "де", "ми", "ви", "він", "не"}
chunks, cur = [], []
for w in W:
    if hidden(w["s"]):
        if cur: chunks.append(cur); cur = []
        continue
    if len(cur) >= 2 and w["w"].lower() in {"після", "перед", "від", "де", "тому", "що"}: chunks.append(cur); cur = []
    if cur and (len(cur) >= 3 or sum(len(x["w"]) for x in cur) + len(w["w"]) > 18):
        carry = []
        while len(cur) > 1 and cur[-1]["w"].lower() in SMALL: carry.insert(0, cur.pop())
        chunks.append(cur); cur = carry
    cur.append(w)
    if re.search(r"[.,?!]$", w["w"]): chunks.append(cur); cur = []
if cur: chunks.append(cur)
caps = []
for i, c in enumerate(chunks):
    s = c[0]["s"] - 0.03
    nxt = chunks[i + 1][0]["s"] - 0.03 if i + 1 < len(chunks) else 99
    e = min(nxt, c[-1]["e"] + 0.35)
    for a, b in HIDE:
        if s < a < e: e = a
    caps.append(dict(s=round(s, 3), e=round(e, 3), w=[dict(t=w["w"], s=round(w["s"], 3), e=round(w["e"], 3)) for w in c]))

QS = [("#q1", 25.3, -3), ("#q2", 25.66, 2), ("#q3", 26.06, -2), ("#q4", 26.5, 3)]
data = dict(T=T, broll=broll_data, faceZoom=FZ, bubble=BUB, items=items_data, caps=caps, qs=QS)
src = open(f"{HERE}/index.src.html").read()
out = (src.replace("__BROLL__", "\n".join(broll_html)).replace("__ITEMS__", "\n".join(items_html))
          .replace("__DATA__", json.dumps(data, ensure_ascii=False)).replace("__VDUR__", str(VDUR)).replace("__DUR__", str(DUR)))
open(f"{HF}/index.html", "w").write(out)
json.dump(dict(T=T, BR=BR, DUR=DUR, VDUR=VDUR, END0=END0), open(f"{HERE}/timing.json", "w"), indent=1)
print("caps", len(caps)); [print(c["s"], c["e"], " ".join(w["t"] for w in c["w"])) for c in caps]
