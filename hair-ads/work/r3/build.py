#!/usr/bin/env python3
"""R3: шесть эстетичных рилсов в HyperFrames. python3 build.py [id ...] → r3/<id>/index.html + assets.

Каждый ролик — одна корневая композиция 1080×1920: футаж (seg/*.mp4, уже в грейде) в обёртках,
которые двигает GSAP (маски, рамки, наезды), поверх — типографика и общая финальная карточка.
Безопасная зона Reels: текст между y=168 и y=1330.
"""
import os, sys, json, shutil, html, pathlib

R3 = pathlib.Path(__file__).resolve().parent
WORK = R3.parent
E = lambda s: html.escape(s, quote=False)

CREAM, CHAMP, ESP = "#FAF7F2", "#D8C3A5", "#2A211C"


def words(text, cls="w"):
    """'Your hair *disagrees.*' → спаны по словам; *...* — курсив."""
    out, it = [], False
    for tok in text.split(" "):
        start, end = tok.startswith("*"), tok.endswith("*")
        t = tok.strip("*")
        if start: it = True
        out.append(f'<span class="{cls}{" it" if it else ""}">{E(t)}</span>')
        if end: it = False
    return " ".join(out)


class Film:
    def __init__(self, fid, dur, bg="#000"):
        self.id, self.dur, self.bg = fid, dur, bg
        self.layers, self.js, self.segs, self.n = [], [], set(), 0
        self.ends = {}

    # ---------- футаж ----------
    def clip(self, cid, seg, start, dur, box="full", z=1, media_start=0.0, extra_style=""):
        """Видео в обёртке #w_<cid> (обёртку двигаем; видео таймится само)."""
        self.segs.add(seg); self.ends[cid] = start + dur
        if box == "full":
            pos = "left:0;top:0;width:1080px;height:1920px"
        else:
            x, y, w, h = box
            pos = f"left:{x}px;top:{y}px;width:{w}px;height:{h}px"
        ms = f' data-media-start="{media_start}"' if media_start else ""
        self.layers.append(
            f'<div class="vw" id="w_{cid}" style="{pos};z-index:{z};{extra_style}">'
            f'<video id="{cid}" class="clip" src="assets/{seg}.mp4" data-start="{start}" data-duration="{dur}"{ms} '
            f'data-track-index="{z}" muted playsinline></video></div>')

    def html(self, s):
        self.layers.append(s)

    def tl(self, s):
        self.js.append(s)

    # ---------- переходы между обёртками ----------
    def dissolve(self, a, b, t, d=0.5):
        if a in self.ends and self.ends[a] < t + d - 1e-6:
            print(f"  ! {self.id}: {a} кончается в {self.ends[a]:.2f}, а растворение в {b} идёт до {t + d:.2f}", file=sys.stderr)
        self.tl(f'tl.fromTo("#w_{b}", {{opacity:0}}, {{opacity:1, duration:{d}, ease:"sine.inOut"}}, {t});')

    def leak(self, t, d=1.0, x0=-30, x1=30, peak=.85):
        """Тёплый засвет поверх стыка (screen)."""
        self.n += 1; i = f"lk{self.n}"
        self.html(f'<div class="leak" id="{i}" style="z-index:40"></div>')
        self.tl(f'tl.fromTo("#{i}", {{opacity:0, xPercent:{x0}}}, {{opacity:{peak}, xPercent:{(x0+x1)/2}, duration:{d*0.45}, ease:"sine.in"}}, {t});')
        self.tl(f'tl.to("#{i}", {{opacity:0, xPercent:{x1}, duration:{d*0.55}, ease:"sine.out"}}, {t + d*0.45});')

    def kenburns(self, cid, t, d, s0=1.0, s1=1.06, x0=0, x1=0, y0=0, y1=0):
        self.tl(f'tl.fromTo("#w_{cid} video", {{scale:{s0}, x:{x0}, y:{y0}}}, {{scale:{s1}, x:{x1}, y:{y1}, duration:{d}, ease:"sine.inOut"}}, {t});')

    # ---------- типографика ----------
    def title(self, tid, text_lines, t_in, t_out, y, size=96, color=CREAM, align="center", shadow=True,
              static=False, family="serif", weight=300, ls="-0.01em", lh=1.04, x=70, w=940, z=50, stagger=.07):
        """Заголовок по словам: blur 8→0 + подъём, держим неподвижно, уход blur-out по словам."""
        fam = "'CG', serif" if family == "serif" else "'Jost', sans-serif"
        sh = "text-shadow:0 2px 26px rgba(20,14,10,.38),0 1px 3px rgba(20,14,10,.25);" if shadow else ""
        rows = "".join(f'<div class="ln">{words(l)}</div>' for l in text_lines)
        if shadow: rows = '<i class="sc"></i>' + rows
        if static: rows = rows.replace('class="w', 'style="opacity:1" class="w').replace('class="sc"', 'class="sc" style="opacity:1"')
        st = "" if not static else ' data-static="1"'
        self.html(f'<div class="ttl" id="{tid}"{st} style="top:{y}px;left:{x}px;width:{w}px;text-align:{align};'
                  f'font-family:{fam};font-weight:{weight};font-size:{size}px;line-height:{lh};letter-spacing:{ls};'
                  f'color:{color};z-index:{z};{sh}">{rows}</div>')
        if not static:
            if shadow: self.tl(f'tl.fromTo("#{tid} .sc", {{opacity:0}}, {{opacity:1, duration:.6, ease:"sine.out"}}, {t_in});')
            self.tl(f'tl.fromTo("#{tid} .w", {{opacity:0, y:16, filter:"blur(9px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:.6, ease:"expo.out", stagger:{stagger}}}, {t_in});')
        if t_out is not None:
            self.tl(f'tl.to("#{tid} .w", {{opacity:0, filter:"blur(7px)", duration:.22, ease:"power2.in", stagger:.025}}, {t_out - .3});')
            if shadow: self.tl(f'tl.to("#{tid} .sc", {{opacity:0, duration:.3, ease:"sine.in"}}, {t_out - .3});')

    def caps(self, tid, text, t_in, t_out, y, size=26, color=CREAM, ls=".32em", x=70, w=940, align="center",
             static=False, z=50, weight=500, rule=False, shadow=True):
        """Подпись капсом Jost; появляется маской (строка выезжает снизу)."""
        sh = "text-shadow:0 1px 14px rgba(20,14,10,.45);" if shadow else ""
        rl = f'<span class="rule" style="background:{CHAMP}"></span>' if rule else ""
        self.html(f'<div class="cap" id="{tid}" style="top:{y}px;left:{x}px;width:{w}px;text-align:{align};'
                  f'font-size:{size}px;letter-spacing:{ls};color:{color};font-weight:{weight};z-index:{z};{sh}">'
                  f'<div class="mask"><span class="in">{E(text)}</span></div>{rl}</div>')
        if not static:
            self.tl(f'tl.fromTo("#{tid} .in", {{yPercent:110, opacity:1}}, {{yPercent:0, duration:.8, ease:"expo.out"}}, {t_in});')
        if rule:
            self.tl(f'tl.fromTo("#{tid} .rule", {{scaleX:0}}, {{scaleX:1, duration:.9, ease:"expo.out"}}, {t_in + (0 if static else .15)});')
        if t_out is not None:
            self.tl(f'tl.to("#{tid} .in", {{yPercent:-110, duration:.35, ease:"power3.in"}}, {t_out - .35});')
            if rule:
                self.tl(f'tl.to("#{tid} .rule", {{scaleX:0, duration:.3, ease:"power3.in"}}, {t_out - .3});')

    def brand(self, color=CREAM, y=196, t_out=None):
        """Постоянная метка локации — на всём ролике (виден с кадра 0)."""
        self.html(f'<div class="brand" id="brand" style="top:{y}px;color:{color};z-index:60">'
                  f'<span class="bl" style="background:{color}"></span>ST. MORITZ · ENGADIN<span class="bl" style="background:{color}"></span></div>')
        if t_out is not None:
            self.tl(f'tl.to("#brand", {{opacity:0, duration:.4}}, {t_out});')

    def dm(self, did="dm", color=CREAM, y=1400, t_in=None, t_out=None):
        """Постоянная пилюля «DM TO BOOK ♡» (как в первом запуске): видна с кадра 0 до финального экрана."""
        bg = "rgba(26,19,14,.34)" if color == CREAM else "rgba(250,247,242,.55)"
        op = "" if t_in is None else "opacity:0;"
        self.html(f'<div class="dmw" style="top:{y}px;z-index:58"><div class="dm" id="{did}" style="color:{color};border-color:{color};background:{bg};{op}">'
                  f'DM TO BOOK <svg width="28" height="25" viewBox="0 0 24 21" aria-hidden="true"><path d="M12 19.5s-9-5.5-9-11.6A4.9 4.9 0 0 1 12 5.2a4.9 4.9 0 0 1 9 2.7c0 6.1-9 11.6-9 11.6z" fill="none" stroke="currentColor" stroke-width="1.7"/></svg></div></div>')
        if t_in is not None:
            self.tl(f'tl.fromTo("#{did}", {{opacity:0}}, {{opacity:1, duration:.5}}, {t_in});')
        if t_out is not None:
            self.tl(f'tl.to("#{did}", {{opacity:0, duration:.4}}, {t_out});')
        self.dm_ids = getattr(self, "dm_ids", []) + [did]

    def snow(self, t0, t1, n=70, seed=7):
        """Снег из DOM-точек: детерминированный (сид), линейное падение — функция времени таймлайна."""
        import random
        r = random.Random(seed); flakes = []
        for i in range(n):
            x = r.uniform(-40, 1100); s = r.uniform(3, 9) if r.random() < .8 else r.uniform(10, 16)
            sp = r.uniform(5.5, 11.0) * (1.4 if s > 9 else 1)  # сек на экран
            ph = r.uniform(0, 1); drift = r.uniform(-120, 120); op = r.uniform(.45, .95)
            flakes.append((x, s, sp, ph, drift, op))
        divs = "".join(f'<i class="fl" id="fl{i}" style="left:{x:.0f}px;width:{s:.1f}px;height:{s:.1f}px;opacity:{op:.2f};'
                       f'{"filter:blur(2px);" if s > 9 else ""}"></i>' for i, (x, s, sp, ph, drift, op) in enumerate(flakes))
        self.html(f'<div class="snow" id="snow" style="z-index:45">{divs}</div>')
        span = t1 - t0
        for i, (x, s, sp, ph, drift, op) in enumerate(flakes):
            y0 = -60 + ph * 1980 - 1980 * (0 if ph < .5 else 1) * 0
            # одна линейная траектория на весь отрезок: старт с фазой, без повторов
            dist = 1980 * span / sp
            ys = -60 + ph * 1980
            self.tl(f'tl.fromTo("#fl{i}", {{y:{ys - 1980:.0f}, x:0}}, {{y:{ys - 1980 + dist:.0f}, x:{drift:.0f}, duration:{span}, ease:"none"}}, {t0});')
        self.tl(f'tl.fromTo("#snow", {{opacity:1}}, {{opacity:0, duration:.5}}, {t1 - .5});')

    def endcard(self, t, blur_seg, kicker, head, keyword, foot="I come to you · St. Moritz & Engadin",
                head_family="serif", head_size=92, dur=None):
        """Финал: футаж уходит в расфокус (готовый размытый кусок поверх), молочная вуаль, текст, пилюля с бликом."""
        end = self.dur
        self.clip("endbl", blur_seg, t - .05, round(end - t + .05, 3), z=30)
        self.tl(f'tl.fromTo("#w_endbl", {{opacity:0}}, {{opacity:1, duration:.7, ease:"sine.inOut"}}, {t});')
        self.html('<div class="veil" id="veil" style="z-index:31"></div>')
        self.tl(f'tl.fromTo("#veil", {{opacity:0}}, {{opacity:1, duration:.7, ease:"sine.inOut"}}, {t});')
        for d in getattr(self, "dm_ids", []):
            self.tl(f'tl.to("#{d}", {{opacity:0, duration:.4}}, {t});')
        self.caps("ek", kicker, t + .35, None, 560, size=27, ls=".26em", rule=True, z=55)
        if head_family == "serif":
            self.title("eh", head, t + .5, None, 640, size=head_size, z=55)
        else:
            self.title("eh", head, t + .5, None, 650, size=head_size, family="sans", weight=300, ls=".14em", lh=1.25, z=55, stagger=.09)
        self.html(f'<div class="pillw" style="top:{960 if len(head) > 1 else 880}px;z-index:56"><div class="pill" id="pill">'
                  + (f'<span>DM me</span><b>“{E(keyword)}”</b>' if keyword else '<b>DM to book</b><svg width="28" height="25" viewBox="0 0 24 21" aria-hidden="true"><path d="M12 19.5s-9-5.5-9-11.6A4.9 4.9 0 0 1 12 5.2a4.9 4.9 0 0 1 9 2.7c0 6.1-9 11.6-9 11.6z" fill="none" stroke="currentColor" stroke-width="1.7"/></svg>')
                  + '<i class="shine" id="shine"><i></i></i></div></div>')
        self.tl(f'tl.fromTo("#pill", {{opacity:0, y:22, scale:.96}}, {{opacity:1, y:0, scale:1, duration:.8, ease:"expo.out"}}, {t + 1.0});')
        self.tl(f'tl.fromTo("#shine", {{x:-200}}, {{x:760, duration:1.1, ease:"power2.inOut"}}, {t + 1.7});')
        self.caps("ef", foot, t + 1.25, None, 1110 if len(head) > 1 else 1030, size=28, ls=".06em", weight=400, z=55)

    # ---------- сборка ----------
    def write(self):
        d = R3 / self.id; a = d / "assets"
        if d.exists(): shutil.rmtree(d / "assets", ignore_errors=True)
        (a / "fonts").mkdir(parents=True, exist_ok=True); (a / "vendor").mkdir(exist_ok=True)
        for s in self.segs:
            src = R3 / "seg" / f"{s}.mp4"
            if not src.exists(): sys.exit(f"нет сегмента {src}")
            os.link(src, a / f"{s}.mp4")
        for x in getattr(self, "extra", []):
            os.link(R3 / "seg" / x, a / x)
        for f in ["CG-normal-300.ttf", "CG-italic-300.ttf", "CG-normal-400.ttf", "CG-italic-400.ttf"]:
            shutil.copy(WORK / "fonts" / f, a / "fonts" / f)
        shutil.copy(WORK / "fonts/Jost.woff2", a / "fonts/Jost.woff2")
        shutil.copy(WORK / "de/01-desire/hf/assets/vendor/gsap.min.js", a / "vendor/gsap.min.js")
        page = f"""<!doctype html>
<html><head><meta charset="utf-8">
<script src="assets/vendor/gsap.min.js"></script>
<style>
  @font-face {{ font-family:"CG"; src:url("assets/fonts/CG-normal-300.ttf"); font-weight:300; font-style:normal; }}
  @font-face {{ font-family:"CG"; src:url("assets/fonts/CG-italic-300.ttf"); font-weight:300; font-style:italic; }}
  @font-face {{ font-family:"CG"; src:url("assets/fonts/CG-normal-400.ttf"); font-weight:400; font-style:normal; }}
  @font-face {{ font-family:"CG"; src:url("assets/fonts/CG-italic-400.ttf"); font-weight:400; font-style:italic; }}
  @font-face {{ font-family:"Jost"; src:url("assets/fonts/Jost.woff2") format("woff2"); font-weight:100 900; }}
  html,body {{ margin:0; background:{self.bg}; }}
  #root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:{self.bg};
          font-family:"Jost",sans-serif; -webkit-font-smoothing:antialiased; }}
  .vw {{ position:absolute; overflow:hidden; }}
  .vw video {{ position:absolute; left:0; top:0; width:100%; height:100%; object-fit:cover; }}
  .ttl {{ position:absolute; }}
  .ttl .ln {{ display:block; white-space:nowrap; position:relative; }}
  .ttl .sc {{ position:absolute; left:-12%; right:-12%; top:-45%; bottom:-45%; opacity:0; pointer-events:none;
             background:radial-gradient(closest-side, rgba(20,14,10,.42), rgba(20,14,10,.18) 60%, rgba(20,14,10,0)); }}
  .ttl .w {{ display:inline-block; opacity:0; }}
  .ttl .it {{ font-style:italic; }}
  .cap {{ position:absolute; text-transform:uppercase; }}
  .cap .mask {{ overflow:hidden; padding:4px 0; }}
  .cap .in {{ display:inline-block; }}
  .cap .rule {{ display:block; width:64px; height:1px; margin:18px auto 0; }}
  .brand {{ position:absolute; left:0; right:0; display:flex; justify-content:center; align-items:center; gap:22px;
           font-size:25px; font-weight:500; letter-spacing:.32em; padding-left:.32em;
           text-shadow:0 1px 14px rgba(20,14,10,.4); }}
  .brand .bl {{ width:46px; height:1px; opacity:.8; }}
  .leak {{ position:absolute; left:-30%; top:-10%; width:160%; height:120%; opacity:0; pointer-events:none;
          background: radial-gradient(38% 30% at 30% 42%, rgba(255,214,160,.55), rgba(255,170,100,.22) 45%, rgba(255,140,60,0) 72%),
                      radial-gradient(30% 24% at 70% 62%, rgba(255,236,200,.45), rgba(255,210,160,0) 70%); }}
  .veil {{ position:absolute; inset:0; opacity:0;
          background: linear-gradient(180deg, rgba(42,33,28,.30), rgba(42,33,28,.42) 45%, rgba(42,33,28,.30)); }}
  .pillw {{ position:absolute; left:0; right:0; display:flex; justify-content:center; }}
  .pill {{ position:relative; overflow:hidden; display:flex; align-items:baseline; gap:16px; opacity:0;
          padding:34px 74px 36px; border-radius:999px; background:{CREAM}; color:{ESP};
          font-size:46px; letter-spacing:.06em; box-shadow:0 18px 50px rgba(0,0,0,.28); }}
  .pill span {{ font-weight:400; }}
  .pill svg {{ align-self:center; }}
  .dmw {{ position:absolute; left:0; right:0; display:flex; justify-content:center; }}
  .dm {{ display:flex; align-items:center; gap:14px; padding:15px 34px 15px 40px; border:1.5px solid; border-radius:999px;
        font-size:30px; font-weight:500; letter-spacing:.28em; }}
  .dm svg {{ width:24px; height:22px; }}
  .pill b {{ font-weight:600; letter-spacing:.12em; }}
  .shine {{ position:absolute; top:-30%; bottom:-30%; width:120px; left:0; }}
  .shine i {{ position:absolute; inset:0; background:linear-gradient(100deg,rgba(255,255,255,0),rgba(255,255,255,.85),rgba(255,255,255,0)); transform:skewX(-18deg); }}
  .snow {{ position:absolute; inset:0; pointer-events:none; }}
  .fl {{ position:absolute; top:0; border-radius:50%; background:#fff; }}
  {getattr(self, "css", "")}
</style></head>
<body>
<div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-start="0" data-duration="{self.dur}" data-fps="30">
{chr(10).join(self.layers)}
<script>
  (function () {{
    const tl = gsap.timeline({{ paused: true }});
    {chr(10) + "    ".join(self.js)}
    tl.set({{}}, {{}}, {self.dur});
    window.__timelines = window.__timelines || {{}};
    window.__timelines["main"] = tl;
  }})();
</script>
</div>
</body></html>
"""
        (d / "index.html").write_text(page)
        print("ok", d)


# ======================================================================
def winter():
    f = Film("winter", 15.4)
    # 1. Альпы со снегом — «Winter in St. Moritz is beautiful.»
    f.clip("alps", "w_alps", 0, 3.1, z=1); f.kenburns("alps", 0, 3.1, 1.0, 1.07)
    f.clip("frz", "w_frizz", 2.6, 2.7, z=2); f.dissolve("alps", "frz", 2.6, .45)
    f.kenburns("frz", 2.6, 2.7, 1.04, 1.12)
    f.snow(0, 4.6)
    f.caps("alt", "1,822 m · Upper Engadin", 0, 2.45, 470, size=24, static=True)
    f.title("t1", ["Winter in St. Moritz", "*is beautiful.*"], 0, 2.55, 540, size=92, static=True)
    f.title("t2", ["Your hair", "*disagrees.*"], 2.8, 4.45, 540, size=104)
    # 2. Триптих: три вертикальные колонки въезжают сверху/снизу по очереди (холодный грейд)
    cols = [("p1", "w_p1", 0, -1), ("p2", "w_p2", 360, 1), ("p3", "w_p3", 720, -1)]
    labels = ["Dry air", "Heating", "Hats"]
    for k, (cid, seg, x, side) in enumerate(cols):
        t = 4.35 + k * .2
        f.clip(cid, seg, t, round(7.15 - t, 2), box=(x, 0, 360, 1920), z=10 + k)
        f.tl(f'tl.fromTo("#w_{cid}", {{yPercent:{side * 100}}}, {{yPercent:0, duration:.8, ease:"expo.out"}}, {t});')
        f.tl(f'tl.to("#w_{cid}", {{yPercent:{-side * 100}, duration:.5, ease:"power3.in"}}, {6.6 + k * .06});')
        f.caps(f"lb{k}", labels[k], t + .45, 6.6, 1170, size=31, ls=".26em", x=x, w=360, z=20, rule=True)
    f.html('<div id="seams" style="position:absolute;inset:0;z-index:15;pointer-events:none">'
           '<i class="sm" style="left:359px"></i><i class="sm" style="left:719px"></i></div>')
    f.css = ".sm{position:absolute;top:0;width:2px;height:1920px;background:rgba(250,247,242,.85)}"
    f.tl('tl.fromTo("#seams .sm", {scaleY:0}, {scaleY:1, duration:.8, ease:"expo.out", stagger:.12}, 4.65);')
    f.tl('tl.to("#seams .sm", {scaleY:0, duration:.3, ease:"power3.in"}, 6.55);')
    # 3. «Оттаивание»: та же чаша — холодная → тёплая, с засветом
    f.clip("mixc", "w_mixc", 6.5, 1.75, z=5); f.kenburns("mixc", 6.5, 2.4, 1.02, 1.1)
    f.clip("mixw", "w_mixw", 7.3, 1.6, z=6); f.dissolve("mixc", "mixw", 7.3, .9)
    f.kenburns("mixw", 6.5, 2.4, 1.02, 1.1)
    f.leak(7.1, 1.4)
    f.title("t3", ["Winter-proof", "*your hair.*"], 7.45, 8.6, 540, size=104)
    # 4. Утюжок → взмах
    f.clip("iron", "w_iron", 8.5, 1.8, z=7); f.dissolve("mixw", "iron", 8.5, .4); f.kenburns("iron", 8.5, 1.8, 1.0, 1.05)
    f.clip("sw", "w_swing", 9.95, 5.45, z=8); f.dissolve("iron", "sw", 9.95, .35); f.kenburns("sw", 9.95, 5.45, 1.0, 1.06)
    f.leak(9.8, 1.0, peak=.6)
    f.title("t4", ["Soft, glossy —", "*ready for the season.*"], 10.5, 11.95, 360, size=88)
    f.brand()
    f.dm()
    f.endcard(12.0, "w_swing_bl", "Keratin · Hair Botox · Hair Recovery", ["Book before", "*the season starts.*"], None)
    return f


def arrival():
    """POV: салон приехал к тебе. Футаж в «окне» на молочном фоне, как разворот журнала; финал — окно становится миром."""
    f = Film("arrival", 15.4, bg=CREAM)
    WIN = (120, 500, 840, 960)   # окно: x, y, w, h
    f.css = (".frame{position:absolute;left:104px;top:484px;width:872px;height:992px;border:1px solid " + CHAMP + ";z-index:3}"
             ".num{position:absolute;top:438px;left:120px;width:840px;display:flex;justify-content:space-between;"
             "font-size:22px;letter-spacing:.24em;text-transform:uppercase;color:#6E5E50;z-index:20}"
             ".num span{opacity:.35}")
    f.html('<div class="frame" id="frame"></div>')
    f.html('<div class="num" id="num"><span id="n1">01 Arrive</span><span id="n2">02 Prepare</span>'
           '<span id="n3">03 Treat</span><span id="n4">04 Reveal</span></div>')
    seq = [("tl1", "a_tools", 0, 2.85), ("tl2", "a_face", 2.55, 2.45), ("tl3", "a_mix", 4.7, 2.05),
           ("tl4", "a_comb", 6.45, 2.05), ("tl5", "a_iron", 8.2, 1.85)]
    for k, (cid, seg, t, d) in enumerate(seq):
        f.clip(cid, seg, t, d, box=WIN, z=5 + k)
        if k:  # следующий кадр въезжает в окно справа, предыдущий уходит влево (одна шторка)
            f.tl(f'tl.fromTo("#w_{cid}", {{clipPath:"inset(0 0 0 100%)"}}, {{clipPath:"inset(0 0 0 0%)", duration:.7, ease:"power3.inOut"}}, {t});')
            f.tl(f'tl.fromTo("#w_{cid} video", {{xPercent:12}}, {{xPercent:0, duration:.9, ease:"power3.out"}}, {t});')
        f.kenburns(cid, t, d, 1.0, 1.05)
    # номера глав: активная — тёмная
    for k, t in enumerate([0, 2.6, 6.45, 9.9]):
        f.tl(f'tl.to("#n{k+1}", {{opacity:1, color:"{ESP}", duration:.4}}, {max(t, 0.001)});')
        if k: f.tl(f'tl.to("#n{k}", {{opacity:.35, color:"#8C7B6B", duration:.4}}, {t});')
    f.tl('tl.set("#n1", {opacity:1, color:"' + ESP + '"}, 0);')
    f.brand(color=ESP)
    f.dm(color=ESP, y=1500, t_out=9.9)
    f.dm("dm2", y=1400, t_in=10.4)
    f.title("h1", ["The salon", "*just arrived.*"], 0, 2.6, 250, size=86, color=ESP, shadow=False, static=True)
    f.title("h2", ["No salon.", "*No commute.*"], 2.75, 4.65, 250, size=86, color=ESP, shadow=False)
    f.title("h3", ["Everything", "*comes with me.*"], 4.85, 6.4, 250, size=86, color=ESP, shadow=False)
    f.title("h4", ["Treated", "*at your table.*"], 6.6, 8.15, 250, size=86, color=ESP, shadow=False)
    f.title("h5", ["Sealed,", "*strand by strand.*"], 8.35, 9.9, 250, size=86, color=ESP, shadow=False)
    # 04 Reveal: окно раскрывается на весь кадр (объект становится миром)
    f.clip("rev", "a_rev", 9.85, 3.85, z=20)
    f.tl('tl.fromTo("#w_rev", {clipPath:"inset(500px 120px 460px 120px)"}, {clipPath:"inset(0px 0px 0px 0px)", duration:.9, ease:"power3.inOut"}, 9.9);')
    f.tl('tl.fromTo("#w_rev video", {scale:1.12}, {scale:1.0, duration:1.4, ease:"power3.out"}, 9.9);')
    f.tl('tl.to(["#frame","#num","#brand"], {opacity:0, duration:.35}, 9.9);')
    f.html('<div class="brand" id="brand2" style="top:196px;color:' + CREAM + ';z-index:60;opacity:0">'
           '<span class="bl" style="background:' + CREAM + '"></span>ST. MORITZ · ENGADIN<span class="bl" style="background:' + CREAM + '"></span></div>')
    f.tl('tl.fromTo("#brand2", {opacity:0}, {opacity:1, duration:.5}, 10.6);')
    f.title("h6", ["Salon result.", "*Your sofa.*"], 10.75, 12.15, 540, size=104)
    f.clip("aend", "a_end", 11.9, 3.5, z=21); f.dissolve("rev", "aend", 11.9, .5)
    f.endcard(12.2, "a_end_bl", "Keratin · Hair Botox · Hair Recovery", ["Your salon,", "*at home.*"], None)
    return f


def glass():
    """Тренд «glass hair»: блик, ритм под бит, слоу-мо на взмахе."""
    f = Film("glass", 13.6)
    f.css = (".glint{position:absolute;left:-40%;top:-20%;width:60%;height:140%;opacity:0;pointer-events:none;"
             "background:linear-gradient(100deg,rgba(255,250,240,0) 25%,rgba(255,248,236,.32) 50%,rgba(255,250,240,0) 75%)}"
             ".gl{transform:rotate(12deg)}"
             ".gl{position:absolute;inset:0;pointer-events:none}")
    def glint(t, d=.9, z=35):
        f.n += 1; i = f"gn{f.n}"
        f.html(f'<div class="gl" style="z-index:{z}"><div class="glint" id="{i}"></div></div>')
        f.tl(f'tl.fromTo("#{i}", {{x:-200, opacity:0}}, {{x:1500, opacity:1, duration:{d}, ease:"power2.inOut"}}, {t});')
        f.tl(f'tl.to("#{i}", {{opacity:0, duration:.2}}, {t + d - .2});')
    f.clip("mac", "g_macro", 0, 2.2, z=1); f.kenburns("mac", 0, 2.2, 1.04, 1.12)
    glint(.15, 1.2)
    f.caps("c1", "Now in St. Moritz", 0, 1.9, 440, size=28, static=True)
    f.title("gt", ["Glass", "*hair.*"], 0, 1.95, 500, size=230, lh=.9, static=True)
    # монтаж под бит: 6 кадров по 0.43 с, вход — короткий «вжух» с размытием
    beat = .43; t0 = 1.95
    words_ = ["Smooth", "", "Soft", "", "Mirror shine", ""]
    for k in range(6):
        t = round(t0 + k * beat, 3)
        f.clip(f"m{k}", f"g_m{k+1}", t, round(beat + .25, 3), z=2 + k)
        # мягкий «вжух»: входящий кадр проявляется 0.22 с со сдвигом и размытием поверх уходящего
        f.tl(f'tl.fromTo("#w_m{k}", {{opacity:0, xPercent:{8 if k % 2 == 0 else -8}, filter:"blur(10px)"}}, {{opacity:1, xPercent:0, filter:"blur(0px)", duration:.22, ease:"power2.out"}}, {t});')
        f.kenburns(f"m{k}", t, beat + .25, 1.08, 1.0)
        if words_[k]:
            f.caps(f"mw{k}", words_[k], t + .02, t + 2 * beat, 900, size=42, ls=".34em", z=50)
    # слоу-мо: ладонь по волосам
    tH = round(t0 + 6 * beat, 3)
    f.clip("hand", "g_hand", tH, 2.8, z=10)
    f.tl(f'tl.fromTo("#w_hand", {{opacity:0}}, {{opacity:1, duration:.25}}, {tH});')
    f.kenburns("hand", tH, 2.8, 1.0, 1.06); glint(tH + .6, 1.3)
    f.title("g2", ["Mirror shine,", "*no filter.*"], tH + .3, tH + 2.4, 540, size=96)
    tS = round(tH + 2.35, 3)
    f.clip("sw", "g_swing", tS, 3.0, z=11); f.dissolve("hand", "sw", tS, .45); f.kenburns("sw", tS, 3.0, 1.0, 1.05)
    f.leak(tS - .2, 1.0, peak=.55)
    f.title("g3", ["Real clients.", "*Real shine.*"], tS + .3, tS + 2.4, 540, size=96)
    tE = round(tS + 2.5, 3)
    f.clip("gend", "g_end", tE, round(f.dur - tE, 3), z=12); f.dissolve("sw", "gend", tE, .5)
    f.brand()
    f.dm()
    f.endcard(tE + .3, "g_end_bl", "Keratin · Hair Botox — at your place", ["Your glass hair", "*starts here.*"], None)
    return f


def alena():
    """Мастер как лицо бренда: имя за её спиной (вырезка), дальше — от первого лица."""
    f = Film("alena", 15.2)
    f.clip("face", "m_face", 0, 2.8, z=1); f.kenburns("face", 0, 2.8, 1.0, 1.05)
    f.caps("role", "Hair specialist · St. Moritz", 0, 2.55, 300, size=24, static=True)
    f.title("nm", ["Alena"], 0, 2.6, 330, size=250, lh=1, static=True, z=8, x=150, w=900)
    # вырезка мастера поверх имени (если есть) — имя «за спиной»
    if (R3 / "seg" / "m_face_cut.webm").exists():
        f.extra = ["m_face_cut.webm"]
        f.layers.append('<div class="vw" id="w_cut" style="left:0;top:0;width:1080px;height:1920px;z-index:9">'
                        '<video id="cut" class="clip" src="assets/m_face_cut.webm" data-start="0" data-duration="2.8" muted playsinline></video></div>')
        f.kenburns("cut", 0, 2.8, 1.0, 1.05)
    f.clip("full", "m_full", 2.35, 2.45, z=10); f.dissolve("face", "full", 2.35, .45); f.kenburns("full", 2.35, 2.45, 1.0, 1.05)
    f.leak(2.2, 1.0, peak=.5)
    f.title("q1", ["I bring everything", "*to your home.*"], 2.65, 4.55, 1150, size=86)
    f.clip("lean", "m_lean", 4.35, 3.0, z=11); f.dissolve("full", "lean", 4.35, .45); f.kenburns("lean", 4.35, 3.0, 1.02, 1.08)
    f.title("q2", ["I look at your hair", "*before I choose.*"], 4.6, 6.6, 1150, size=86)
    f.clip("mix", "m_mix", 6.55, 2.0, z=12)
    f.tl('tl.fromTo("#w_mix", {clipPath:"circle(0% at 50% 50%)"}, {clipPath:"circle(75% at 50% 50%)", duration:.8, ease:"power3.inOut"}, 6.55);')
    f.kenburns("mix", 6.55, 2.0, 1.1, 1.0)
    f.caps("svc", "Keratin · Hair Botox · Hair Recovery", 6.85, 8.35, 1040, size=28, rule=True)
    f.title("q3", ["*Only professional* products."], 7.05, 8.35, 1120, size=76)
    f.clip("r1", "m_res1", 8.1, 2.2, z=13); f.dissolve("mix", "r1", 8.1, .45); f.kenburns("r1", 8.1, 2.2, 1.0, 1.05)
    f.title("q4", ["*Tailored* to every", "hair type."], 8.35, 10.15, 1150, size=92)
    f.clip("r2", "m_res2", 9.85, 2.2, z=14); f.dissolve("r1", "r2", 9.85, .45)
    f.leak(9.7, 1.0, peak=.55)
    f.clip("mend", "m_end", 11.6, 3.6, z=15); f.dissolve("r2", "mend", 11.6, .45)
    f.brand()
    f.endcard(12.0, "m_end_bl", "Keratin · Hair Botox · Hair Recovery", ["Say hi —", "*I reply myself.*"], "ALENA")
    return f


def words_film():
    """Отзыв клиентки поверх ЕЁ результата → мастер раскладывает инструменты → процесс и названия процедур →
    результаты разных клиенток (блеск, движение) → CTA. Текст держится дольше: 0.5 с + 0.3 с на слово и больше."""
    f = Film("words", 18.6)
    f.css = (".qm{position:absolute;left:70px;top:330px;font-family:'CG',serif;font-size:300px;line-height:1;color:" + CHAMP + ";z-index:49;opacity:.9}"
             ".lowveil{position:absolute;left:0;right:0;top:760px;bottom:0;opacity:0;z-index:30;"
             "background:linear-gradient(180deg,rgba(20,14,10,0),rgba(20,14,10,.45) 30%,rgba(20,14,10,.55))}"
             ".menu{position:absolute;left:0;right:0;top:960px;text-align:center;z-index:50;font-family:'CG',serif;font-weight:300;color:" + CREAM + "}"
             ".menu .it{display:block;font-size:92px;line-height:1.12;opacity:0}"
             ".menu .rl{display:block;width:70px;height:1px;margin:6px auto;background:" + CHAMP + ";opacity:.9}")
    # 1. Отзыв — на результате той самой клиентки (27.10), держим долго и спокойно
    f.clip("q", "c_q2", 0, 4.8, z=1); f.kenburns("q", 0, 4.8, 1.0, 1.06)
    f.html('<div class="veil" id="qveil" style="z-index:2;opacity:1"></div>')
    f.tl('tl.to("#qveil", {opacity:0, duration:.5}, 4.3);')
    f.html('<div class="qm" id="qm">“</div>')
    f.tl('tl.to("#qm", {opacity:0, duration:.3}, 4.15);')
    f.title("qa", ["I couldn't find anyone"], 0, 4.45, 560, size=84, static=True)
    f.title("qb", ["*in the valley*"], .45, 4.45, 652, size=84)
    f.title("qc", ["who does this."], .9, 4.45, 744, size=84)
    # 2. Мастер раскладывает инструменты — «теперь я приезжаю к вам»
    f.clip("tools", "c_tools", 4.3, 2.8, z=10); f.dissolve("q", "tools", 4.3, .5); f.kenburns("tools", 4.3, 2.8, 1.0, 1.05)
    f.title("t1", ["Now I come", "*to you.*"], 4.6, 6.85, 300, size=96, color=ESP, shadow=False)
    f.caps("t1c", "Your home · your chalet · your hotel", 4.95, 6.85, 530, size=28, color=ESP, ls=".2em", shadow=False, rule=True)
    # 3. Процесс + процедуры списком (держим весь отрезок ~4.3 с)
    f.clip("drip", "c_drip", 6.65, 1.9, z=11); f.dissolve("tools", "drip", 6.65, .45)
    f.kenburns("drip", 6.65, 1.9, 1.04, 1.1)
    f.clip("apply", "c_apply", 8.2, 1.8, z=12); f.dissolve("drip", "apply", 8.2, .35); f.kenburns("apply", 8.2, 1.8, 1.0, 1.05)
    f.clip("iron", "c_iron", 9.65, 1.8, z=13); f.dissolve("apply", "iron", 9.65, .35); f.kenburns("iron", 9.65, 1.8, 1.0, 1.05)
    f.html('<div class="lowveil" id="lowveil"></div>')
    f.tl('tl.fromTo("#lowveil", {opacity:0}, {opacity:1, duration:.6, ease:"sine.inOut"}, 6.8);')
    f.tl('tl.to("#lowveil", {opacity:0, duration:.5, ease:"sine.inOut"}, 11.1);')
    f.caps("mk", "The treatments", 6.95, 11.25, 880, size=28, ls=".32em")
    f.html('<div class="menu" id="menu"><span class="it" id="mi1">Keratin</span><span class="rl" id="mr1"></span>'
           '<span class="it" id="mi2"><i>Hair Botox</i></span><span class="rl" id="mr2"></span>'
           '<span class="it" id="mi3">Hair Recovery</span></div>')
    for k, t in enumerate([7.15, 7.6, 8.05]):
        f.tl(f'tl.fromTo("#mi{k+1}", {{opacity:0, y:18, filter:"blur(8px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:.7, ease:"expo.out"}}, {t});')
    for k, t in enumerate([7.4, 7.85]):
        f.tl(f'tl.fromTo("#mr{k+1}", {{scaleX:0}}, {{scaleX:1, duration:.7, ease:"expo.out"}}, {t});')
    f.tl('tl.to(["#mi1","#mi2","#mi3","#mr1","#mr2"], {opacity:0, filter:"blur(6px)", duration:.3, ease:"power2.in", stagger:.04}, 10.95);')
    # 4. Результаты разных клиенток: блеск и движение
    f.clip("r1", "c_r1", 11.0, 2.3, z=14); f.dissolve("iron", "r1", 11.0, .45); f.kenburns("r1", 11.0, 2.3, 1.0, 1.05)
    f.leak(10.85, 1.0, peak=.5)
    f.clip("r2", "c_r2", 12.85, 2.3, z=15); f.dissolve("r1", "r2", 12.85, .45); f.kenburns("r2", 12.85, 2.3, 1.0, 1.05)
    f.clip("r3", "c_r3", 14.7, 3.9, z=16); f.dissolve("r2", "r3", 14.7, .45); f.kenburns("r3", 14.7, 3.9, 1.0, 1.05)
    f.title("res", ["Mirror shine.", "*Every hair type.*"], 11.35, 15.15, 1150, size=96)
    f.brand()
    f.dm()
    f.endcard(15.3, "c_r3_bl", "Keratin · Hair Botox · Hair Recovery", ["Your hair,", "*next.*"], None)
    return f


def classic():
    """Ближе к первому запуску (01 DESIRE): Jost light, разрядка, шампань — но реальный результат, «до/после» линией и явный выезд."""
    f = Film("classic", 15.2)
    f.css = (".gold{position:absolute;top:0;width:2px;height:1920px;left:0;z-index:25;background:linear-gradient(180deg,rgba(216,195,165,0),"
             + CHAMP + " 12%," + CHAMP + " 88%,rgba(216,195,165,0));box-shadow:0 0 18px rgba(216,195,165,.8)}")
    sans = dict(family="sans", weight=300, ls=".22em", lh=1.25)
    f.clip("k1", "k1", 0, 2.0, z=1); f.kenburns("k1", 0, 2.0, 1.0, 1.05)
    f.title("s1", ["SMOOTH."], 0, 1.75, 860, size=92, static=True, **sans)
    f.clip("k2", "k2", 1.7, 1.8, z=2); f.dissolve("k1", "k2", 1.7, .3); f.kenburns("k2", 1.7, 1.8, 1.0, 1.05)
    f.title("s2", ["SILKY."], 1.85, 3.3, 860, size=92, **sans)
    f.clip("k3", "k3", 3.2, 2.0, z=3); f.dissolve("k2", "k3", 3.2, .3); f.kenburns("k3", 3.2, 2.0, 1.0, 1.05)
    f.title("s3", ["GLOSSY."], 3.35, 4.95, 860, size=92, **sans)
    f.leak(3.1, .9, peak=.5)
    # до → после: золотая линия едет справа налево и открывает «после»
    f.clip("kb", "k_b", 4.85, 2.85, z=4); f.dissolve("k3", "kb", 4.85, .35)
    f.clip("ka", "k_a", 5.6, 2.6, z=5)
    f.tl('tl.fromTo("#w_ka", {clipPath:"inset(0 0 0 100%)"}, {clipPath:"inset(0 0 0 0%)", duration:1.5, ease:"power2.inOut"}, 5.75);')
    f.html('<div class="gold" id="gold"></div>')
    f.tl('tl.fromTo("#gold", {x:1080, opacity:1}, {x:-2, duration:1.5, ease:"power2.inOut"}, 5.75);')
    f.tl('tl.to("#gold", {opacity:0, duration:.2}, 7.25);')
    f.caps("bf", "Before", 5.05, 6.4, 1180, size=32, ls=".34em", rule=True)
    f.caps("af", "After", 6.65, 7.75, 1180, size=32, ls=".34em", rule=True)
    f.title("tl", ["TAILORED", "TO YOUR HAIR"], 5.2, 7.7, 520, size=66, **sans)
    f.clip("al", "k_alena", 7.75, 2.4, z=6); f.dissolve("ka", "al", 7.75, .4); f.kenburns("al", 7.75, 2.4, 1.0, 1.05)
    f.title("pl", ["AT YOUR PLACE", "IN ST. MORITZ"], 7.95, 9.75, 1150, size=62, **sans)
    f.clip("rs", "k_res", 9.7, 2.6, z=7); f.dissolve("al", "rs", 9.7, .45); f.kenburns("rs", 9.7, 2.6, 1.0, 1.05)
    f.leak(9.55, 1.0, peak=.5)
    f.clip("ke", "k_end", 11.8, 3.4, z=8); f.dissolve("rs", "ke", 11.8, .45)
    f.brand()
    f.dm()
    f.endcard(11.9, "k_end_bl", "Keratin · Hair Botox · Hair Recovery", ["YOUR HAIR.", "YOUR SPACE."], None,
              head_family="sans", head_size=72)
    return f


FILMS = {"winter": winter, "arrival": arrival, "glass": glass, "alena": alena, "words": words_film, "classic": classic}

if __name__ == "__main__":
    for k in (sys.argv[1:] or FILMS):
        FILMS[k]().write()
