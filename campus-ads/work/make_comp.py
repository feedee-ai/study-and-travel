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
    END0 = seg[7]; DUR = round(E["dur"] + 0.55, 2)
    T = dict(hud0=3.45, hud1=seg[6], f1=seg[1], f2=seg[3], f3=seg[4], f4=seg[5], f5=seg[6], end0=END0,
             par=wt("які"), free=wt("Безкоштовно"), mova=wt("навчання", 6), b1=wt("словацькою"), meter=wt("Її"),
             meterFill=wt("потрібного") - 0.1, meterStep=0.22,
             strike=wt("іспитів"), spec=wt("багато", 16.5), chips=wt("Тому", 20), chipTo=wt("напрям"),
             bars=wt("Чим"), dip=wt("головне,"), zd=wt("можливість"), mdos=wt("міжнародний"), bud=wt("і", 38), fut=wt("будувати", 38),
             p5a=wt("пройти"), p5b=wt("вступу.", 43), badge=wt("Study", 40), tap=wt("«Детальніше»"), stud1=seg[1] - 0.25)
    T["dipl"] = T["dip"] + 1.2
    extra = dict(checks=[wt("вступу.") + 0.25, wt("дитину.", 23) + 0.3, wt("факультету.", 31) + 0.4, wt("майбутнє.") + 0.35],
                 hookW=[wt(x) for x in ["речі", "про", "безкоштовний", "вступ", "до", "Словаччини,"]],
                 chipT=[wt("Study", 20.5) + 0.2, wt("допоможе", 21) + 0.1, wt("підібрати")],
                 tagT=[wt("Місця"), wt("дедлайни"), wt("залежать", 25)],
                 barT=[wt("вивчення"), wt("оформлення"), wt("вибір", 31)])
    t1 = T["zd"] - 0.02; t2 = round(t1 + (T["bud"] - t1) / 2, 3); tb = T["bud"] - 0.03
    BR = [dict(id="travel1", t=t1, d=round(t2 - t1, 3), enter=False), dict(id="travel2", t=t2, d=round(tb - t2, 3), enter=True)]
    extra["broll"] = BR
    LET = [(660, 600), (752, 636), (846, 598), (938, 640), (700, 712), (800, 722), (900, 716)]
    extra["letters"] = LET
    ZOOM = [(0, 1.20, 1.03, seg[1], .48, .47), (seg[1], 1.0, 1.05, seg[2] - seg[1], .49, .5), (seg[2], 1.24, 1.28, seg[3] - seg[2], .49, .5),
            (seg[3], 1.0, 1.04, 4.85, .6, .5), (wt("Тому", 20), 1.22, 1.26, seg[4] - wt("Тому", 20), .6, .38),
            (seg[4], 1.0, 1.04, 2.95, .62, .45), (wt("Чим"), 1.22, 1.26, seg[5] - wt("Чим"), .62, .28),
            (seg[5], 1.0, 1.05, T["zd"] - seg[5], .45, .45), (T["bud"], 1.18, 1.22, seg[6] - T["bud"], .45, .40),
            (seg[6], 1.08, 1.0, seg[7] - seg[6], .47, .47), (seg[7], 1.18, 1.22, 4.6, .47, .47)]
    HIDE = [(END0, 99)]; CAPSTYLE = ""
    cal = "".join("<i></i>" for _ in range(28))
    stars = "".join(f'<path transform="translate({105 * math.cos(2 * math.pi * k / 12 - math.pi / 2):.1f} {105 * math.sin(2 * math.pi * k / 12 - math.pi / 2):.1f})" '
                    f'd="M0 -15 L4.4 -4.6 L15 -4.6 L6.4 2.4 L9.5 13 L0 6.6 L-9.5 13 L-6.4 2.4 L-15 -4.6 L-4.4 -4.6 Z" fill="#FFD21A"/>' for k in range(12))
    letters = "".join(f'<div class="lt{" y" if i % 3 == 1 else ""}" id="lt{i}" style="left:{x}px; top:{y}px">{c}</div>' for i, ((x, y), c) in enumerate(zip(LET, "ČŠŽĎĽŤÔ")))
    IC = {  # иконки специальностей 34×34, чёрным
        "IT": '<path d="M12 9 L4 17 L12 25 M22 9 L30 17 L22 25" fill="none" stroke="#0C0C0C" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
        "Економіка": '<path d="M5 29 V19 M13 29 V12 M21 29 V16 M29 29 V6" stroke="#0C0C0C" stroke-width="5" stroke-linecap="round"/>',
        "Менеджмент": '<rect x="4" y="11" width="26" height="18" rx="4" fill="#0C0C0C"/><path d="M12 11 V7 h10 v4" fill="none" stroke="#0C0C0C" stroke-width="3"/>',
        "Дизайн": '<path d="M6 28 L10 18 L24 4 L30 10 L16 24 Z" fill="#0C0C0C"/>',
        "Туризм": '<circle cx="17" cy="17" r="13" fill="none" stroke="#0C0C0C" stroke-width="3.5"/><path d="M4 17h26M17 4c-6 7-6 19 0 26M17 4c6 7 6 19 0 26" fill="none" stroke="#0C0C0C" stroke-width="2.5"/>',
        "Педагогіка": '<path d="M3 8 c5 -2 10 -2 14 2 c4 -4 9 -4 14 -2 v20 c-5 -2 -10 -2 -14 2 c-4 -4 -9 -4 -14 -2 Z" fill="#0C0C0C"/>',
        "Інженерія": '<circle cx="17" cy="17" r="7" fill="none" stroke="#0C0C0C" stroke-width="4"/><path d="M17 3v6M17 25v6M3 17h6M25 17h6M7 7l4 4M23 23l4 4M27 7l-4 4M11 23l-4 4" stroke="#0C0C0C" stroke-width="4" stroke-linecap="round"/>',
        "Психологія": '<path d="M17 29 C4 20 3 12 8 8 c4 -3 8 -1 9 2 c1 -3 5 -5 9 -2 c5 4 4 12 -9 21 Z" fill="#0C0C0C"/>',
        "Маркетинг": '<path d="M4 14 h6 l14 -8 v22 l-14 -8 h-6 Z" fill="#0C0C0C"/><path d="M28 12 c3 3 3 7 0 10" fill="none" stroke="#0C0C0C" stroke-width="3" stroke-linecap="round"/>',
        "Журналістика": '<rect x="11" y="3" width="12" height="18" rx="6" fill="#0C0C0C"/><path d="M7 16 c0 7 5 10 10 10 s10 -3 10 -10 M17 26 v5" fill="none" stroke="#0C0C0C" stroke-width="3" stroke-linecap="round"/>',
    }
    def tick(names): return "".join(f'<div class="p{" k" if i % 2 else ""}"><i><svg viewBox="0 0 34 34">{IC[n]}</svg></i>{n}</div>' for i, n in enumerate(names))
    r1 = ["IT", "Економіка", "Менеджмент", "Дизайн", "Туризм"]; r2 = ["Педагогіка", "Інженерія", "Психологія", "Маркетинг", "Журналістика"]
    broll_html = "\n".join(f'  <div class="vw" id="bw-{b["id"]}"><div class="vz" id="bz-{b["id"]}"><video id="v-{b["id"]}" class="clip" data-start="{b["t"]}" '
                           f'data-duration="{round(b["d"] + (0.32 if i == 0 else 0), 3)}" data-track-index="{i + 1}" src="assets/media/{b["id"]}.mp4" muted playsinline></video></div></div>'
                           for i, b in enumerate(BR))
    SUBS = {"__CAL__": cal, "__STARS__": stars, "__LETTERS__": letters, "__TICK1__": tick(r1 + r1), "__TICK2__": tick(r2 + r2), "__BROLL__": broll_html}
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
STUD = ('  <div id="stud" class="abs"><div class="ic"><svg viewBox="0 0 48 48"><path d="M2 18 L24 8 L46 18 L24 28 Z" fill="#0C0C0C"/>'
        '<path d="M11 23 v11 c8 6 18 6 26 0 v-11 L24 29 Z" fill="#0C0C0C"/><path d="M42 20 v14" stroke="#0C0C0C" stroke-width="3"/></svg>'
        '<i class="ok"><svg viewBox="0 0 18 16"><path d="M2 8 l5 5 l9 -11" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg></i></div>'
        '<div><b>Вступила з Study and Travel</b><small>студентка · навчається у Словаччині</small></div></div>')
STUDJS = """      tl.fromTo("#stud", { opacity: 0, y: 40, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: EB }, 0.45);
      tl.fromTo("#stud .ok", { scale: 0 }, { scale: 1, duration: 0.35, ease: EB }, 0.85);
      tl.to("#stud", { opacity: 0, y: 30, duration: 0.25, ease: "power2.in" }, T.stud1);"""
SUBS.setdefault("__STUD__", STUD); SUBS.setdefault("__STUDJS__", STUDJS)
data = dict(T=T, zoom=ZOOM, caps=caps, capStyle=CAPSTYLE, vdur=round(E["dur"] - 0.06, 3), **extra)
src = open(f"{HERE}/../{VID}/index.src.html").read()
out = src.replace("__CSS__", open(f"{HERE}/common.css").read()).replace("__COMMONJS__", COMMONJS).replace("__DATA__", json.dumps(data, ensure_ascii=False))
for k, v in SUBS.items(): out = out.replace(k, v)
out = out.replace("__VDUR__", str(round(E["dur"] - 0.06, 3))).replace("__DUR__", str(DUR))
open(f"{HERE}/../{VID}/hf/index.html", "w").write(out)
json.dump(dict(T=T, DUR=DUR, extra=extra), open(f"{HERE}/../{VID}/timing.json", "w"), indent=1, ensure_ascii=False)
print(VID, "caps", len(caps), "DUR", DUR)
for c in caps: print(" ", c["s"], " ".join(w["t"] for w in c["w"]))
