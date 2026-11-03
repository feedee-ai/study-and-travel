# make_comp.py VID — собирает VID/hf/index.html из VID/index.src.html: общие стили, зумы, субтитры, тайминги сцен
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
VID = sys.argv[1]
E = json.load(open(f"{HERE}/../{VID}/edl.json"))
W = E["words"]

def wt(word, after=0.0):
    """время начала слова (первое вхождение после after)"""
    base = re.sub(r"[^\w'»«]", "", word.lower())
    for w in W:
        if w["s"] >= after - 0.05 and re.sub(r"[^\w'»«]", "", w["w"].lower()) == base: return round(w["s"], 3)
    raise KeyError(word)

S = {s["clip"]: s for s in E["segs"]}
seg = [s["out_in"] for s in E["segs"]]

if VID == "v1":
    DUR, END0 = 49.5, seg[7]
    T = dict(hud0=3.45, hud1=seg[6], f1=seg[1], f2=seg[3], f3=seg[4], f4=seg[5], f5=seg[6], end0=END0,
             par=wt("які"), b1=wt("словацькою"), meter=wt("Її"), meterFill=wt("потрібного") - 0.1, meterStep=0.22,
             strike=wt("іспитів"), note=wt("багато"), chips=wt("Тому", 20), chipTo=wt("напрям"),
             bars=wt("Чим"), dip=wt("головне,"), exp=wt("здобути"), p5a=wt("пройти"), p5b=wt("вступу.", 43), badge=wt("Study", 40),
             tap=wt("«Детальніше»"))
    extra = dict(checks=[wt("вступу.") + 0.25, wt("дитину.", 23) + 0.3, wt("факультету.", 31) + 0.4, wt("досвід.") + 0.25],
                 hookW=[wt(x) for x in ["речі", "про", "безкоштовний", "вступ", "до", "Словаччини,"]],
                 chipT=[wt("Study", 20.5) + 0.2, wt("допоможе", 21) + 0.1, wt("підібрати")],
                 tagT=[wt("Місця"), wt("дедлайни"), wt("залежать", 25)],
                 barT=[wt("вивчення"), wt("оформлення"), wt("вибір", 31)])
    ZOOM = [(0, 1.20, 1.03, seg[1], .48, .47), (seg[1], 1.0, 1.05, seg[2] - seg[1], .49, .5), (seg[2], 1.24, 1.28, seg[3] - seg[2], .49, .5),
            (seg[3], 1.0, 1.04, 4.85, .6, .5), (wt("Тому", 20), 1.22, 1.26, seg[4] - wt("Тому", 20), .6, .38),
            (seg[4], 1.0, 1.04, 2.95, .62, .45), (wt("Чим"), 1.22, 1.26, seg[5] - wt("Чим"), .62, .28),
            (seg[5], 1.0, 1.07, seg[6] - seg[5], .45, .45), (seg[6], 1.08, 1.0, seg[7] - seg[6], .47, .47), (seg[7], 1.18, 1.22, 4.6, .47, .47)]
    HIDE = [(END0, 99)]; CAPSTYLE = ""
    cal = "".join("<i></i>" for _ in range(28))
    stars = "".join(f'<path transform="translate({105 * math.cos(2 * math.pi * k / 12 - math.pi / 2):.1f} {105 * math.sin(2 * math.pi * k / 12 - math.pi / 2):.1f})" '
                    f'd="M0 -15 L4.4 -4.6 L15 -4.6 L6.4 2.4 L9.5 13 L0 6.6 L-9.5 13 L-6.4 2.4 L-15 -4.6 L-4.4 -4.6 Z" fill="#FFD21A"/>' for k in range(12))
    SUBS = {"__CAL__": cal, "__STARS__": stars}
else:
    DUR, END0 = 46.6, None
    sys.path.insert(0, HERE); from v2conf import conf
    DUR, T, extra, ZOOM, HIDE, CAPSTYLE, SUBS = conf(E, wt, seg)

# ---------- субтитры: 1–3 слова, рвём на пунктуации ----------
SMALL = {"у", "в", "на", "до", "і", "та", "з", "а", "й", "не", "що", "як", "від", "за", "під", "це", "ми"}
STARTERS = {"щоб", "якщо", "тому", "але", "адже", "від", "чим", "тим", "якщо"}
def hidden(t): return any(a - 0.05 <= t < b for a, b in HIDE)
chunks, cur = [], []
for w in W:
    if hidden(w["s"]):
        if cur: chunks.append(cur); cur = []
        continue
    if len(cur) >= 2 and w["w"].lower() in STARTERS: chunks.append(cur); cur = []
    if w["w"] == "Study" and cur and len(cur) >= 2: chunks.append(cur); cur = []
    brand = cur and cur[-1]["w"] in ("Study", "and")
    if cur and not brand and (len(cur) >= 3 or sum(len(x["w"]) for x in cur) + len(w["w"]) > 18):
        carry = []
        while len(cur) > 1 and cur[-1]["w"].lower() in SMALL: carry.insert(0, cur.pop())
        chunks.append(cur); cur = carry
    cur.append(w)
    if re.search(r"[.,?!»]$", w["w"]) and not w["w"].endswith("«"): chunks.append(cur); cur = []
if cur: chunks.append(cur)
caps = []
for i, c in enumerate(chunks):
    s = c[0]["s"] - 0.03
    nxt = chunks[i + 1][0]["s"] - 0.03 if i + 1 < len(chunks) else 99
    e = min(nxt, c[-1]["e"] + 0.35)
    for a, b in HIDE:
        if s < a < e: e = a
    caps.append(dict(s=round(s, 3), e=round(e, 3), w=[dict(t=w["w"], s=round(w["s"], 3), e=round(w["e"], 3)) for w in c]))

COMMONJS = """      const D = __DATA__;
      const tl = gsap.timeline({ paused: true });
      const E = "power3.out", EB = "back.out(1.7)";
      D.zoom.forEach(([t, z0, z1, d, ox, oy]) => {
        tl.set("#plateZ", { scale: z0, transformOrigin: `${ox * 100}% ${oy * 100}%` }, t);
        tl.to("#plateZ", { scale: z1, duration: d, ease: "sine.out" }, t + 0.001);
      });
      const capsEl = document.getElementById("caps");
      D.caps.forEach((c, ci) => {
        const el = document.createElement("div"); el.className = "cap" + D.capStyle; el.id = "cap" + ci;
        c.w.forEach((w, wi) => { const s = document.createElement("span"); s.className = "cw"; s.id = `c${ci}w${wi}`; s.textContent = w.t; el.appendChild(s); });
        capsEl.appendChild(el);
        tl.fromTo(el, { opacity: 0, y: 14, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.14, ease: E }, c.s);
        tl.set(el, { opacity: 0 }, c.e);
        c.w.forEach((w, wi) => {
          tl.set(`#c${ci}w${wi}`, { attr: { class: "cw on" } }, w.s);
          tl.set(`#c${ci}w${wi}`, { attr: { class: "cw" } }, Math.min(w.e, c.e));
        });
      });
"""
data = dict(T=T, zoom=ZOOM, caps=caps, capStyle=CAPSTYLE, vdur=round(E["dur"] - 0.06, 3), **extra)
src = open(f"{HERE}/../{VID}/index.src.html").read()
out = src.replace("__CSS__", open(f"{HERE}/common.css").read()).replace("__COMMONJS__", COMMONJS).replace("__DATA__", json.dumps(data, ensure_ascii=False))
for k, v in SUBS.items(): out = out.replace(k, v)
out = out.replace("__VDUR__", str(round(E["dur"] - 0.06, 3))).replace("__DUR__", str(DUR))
open(f"{HERE}/../{VID}/hf/index.html", "w").write(out)
json.dump(dict(T=T, DUR=DUR, extra=extra), open(f"{HERE}/../{VID}/timing.json", "w"), indent=1, ensure_ascii=False)
print(VID, "caps", len(caps), "DUR", DUR)
for c in caps: print(" ", c["s"], " ".join(w["t"] for w in c["w"]))
