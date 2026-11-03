#!/usr/bin/env python3
"""Прозрачный слой текста для рилсов r2 (HyperFrames): spec.json → hf/index.html.

Стиль — нативный Reels: белые плашки с тёмным текстом (как текст-стикеры Instagram),
маленькая метка локации, чипы BEFORE/AFTER, финальный CTA над зоной подписи.
Безопасная зона: текст между y=200 и y=1500 (ниже — подпись и кнопки Instagram).

spec.json: {"duration": 14.2, "events": [ {kind, t_in, t_out, ...}, ... ]}
  kind=hook  lines:[...], y         — белые плашки построчно
  kind=sub   lines:[...], y         — белый текст с тенью
  kind=chip  text, y, tone          — пилюля (tone: dark | light)
  kind=cta   kicker, main, foot     — финальный блок у низа
  kind=scrim y0, y1, a              — затемнение-градиент снизу
"""
import json, sys, html, pathlib, shutil

d = pathlib.Path(sys.argv[1])
spec = json.loads((d / "spec.json").read_text())
hf = d / "hf"; (hf / "assets/fonts").mkdir(parents=True, exist_ok=True); (hf / "assets/vendor").mkdir(parents=True, exist_ok=True)
work = pathlib.Path(__file__).resolve().parent.parent
shutil.copy(work / "fonts/Inter.woff2", hf / "assets/fonts/Inter.woff2")
shutil.copy("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", hf / "assets/fonts/Emoji.ttf")
shutil.copy(work / "de/01-desire/hf/assets/vendor/gsap.min.js", hf / "assets/vendor/gsap.min.js")

E = lambda s: html.escape(s, quote=False)
body, js = [], []
for i, ev in enumerate(spec["events"]):
    k, eid, a, b = ev["kind"], f"e{i}", ev["t_in"], ev["t_out"]
    if k == "hook":
        st = ' style="opacity:1"' if a <= 0 else ""
        rows = "".join(f'<div class="hb"{st}><span>{E(l)}</span></div>' for l in ev["lines"])
        body.append(f'<div class="hook" id="{eid}" style="top:{ev["y"]}px">{rows}</div>')
        if a > 0: js.append(f'tl.fromTo("#{eid} .hb", {{opacity:0, y:26, scale:.94}}, {{opacity:1, y:0, scale:1, duration:.42, ease:"back.out(1.7)", stagger:.09}}, {a});')
        js.append(f'tl.to("#{eid} .hb", {{opacity:0, y:-12, duration:.22, ease:"power2.in", stagger:.04}}, {b - .22});')
    elif k == "sub":
        rows = "".join(f'<div class="sl">{E(l)}</div>' for l in ev["lines"])
        body.append(f'<div class="sub" id="{eid}" style="top:{ev["y"]}px">{rows}</div>')
        js.append(f'tl.fromTo("#{eid} .sl", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:.45, ease:"power3.out", stagger:.1}}, {a});')
        js.append(f'tl.to("#{eid} .sl", {{opacity:0, duration:.22, ease:"power2.in"}}, {b - .22});')
    elif k == "chip":
        st = ' style="opacity:1"' if a <= 0 else ""
        body.append(f'<div class="chipw" style="top:{ev["y"]}px"><div class="chip {ev.get("tone","dark")}" id="{eid}"{st}>{E(ev["text"])}</div></div>')
        if a > 0: js.append(f'tl.fromTo("#{eid}", {{opacity:0, scale:.8}}, {{opacity:1, scale:1, duration:.35, ease:"back.out(2)"}}, {a});')
        js.append(f'tl.to("#{eid}", {{opacity:0, duration:.18}}, {b - .18});')
    elif k == "scrim":
        body.append(f'<div class="scrim" id="{eid}" style="top:{ev["y0"]}px;height:{ev["y1"]-ev["y0"]}px;'
                    f'background:linear-gradient(0deg,rgba(12,10,9,{ev["a"]}),rgba(12,10,9,0))"></div>')
        js.append(f'tl.fromTo("#{eid}", {{opacity:0}}, {{opacity:1, duration:.5, ease:"power1.out"}}, {a});')
    elif k == "cta":
        body.append(f'<div class="cta" id="{eid}"><div class="ck">{E(ev["kicker"])}</div>'
                    f'<div class="cm"><span>{E(ev["main"])}</span></div><div class="cf">{E(ev["foot"])}</div></div>')
        js.append(f'tl.fromTo("#{eid} .ck", {{opacity:0, y:18}}, {{opacity:1, y:0, duration:.45, ease:"power3.out"}}, {a});')
        js.append(f'tl.fromTo("#{eid} .cm", {{opacity:0, y:26, scale:.92}}, {{opacity:1, y:0, scale:1, duration:.5, ease:"back.out(1.8)"}}, {a + .15});')
        js.append(f'tl.fromTo("#{eid} .cf", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:.45, ease:"power3.out"}}, {a + .35});')
        js.append(f'tl.to("#{eid} .cm span", {{scale:1.035, duration:.5, ease:"sine.inOut", yoyo:true, repeat:1}}, {a + 1.1});')

dur = spec["duration"]
page = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<script src="assets/vendor/gsap.min.js"></script>
<style>
  @font-face {{ font-family: "Inter"; src: url("assets/fonts/Inter.woff2") format("woff2"); font-weight: 100 900; }}
  @font-face {{ font-family: "Emoji"; src: url("assets/fonts/Emoji.ttf") format("truetype"); }}
  html, body {{ margin: 0; background: transparent; }}
  #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; color: #fff;
          font-family: "Inter", "Emoji", sans-serif; -webkit-font-smoothing: antialiased; }}
  .loc {{ position: absolute; top: 196px; left: 0; right: 0; display: flex; justify-content: center; }}
  .loc span {{ padding: 12px 26px; border-radius: 999px; background: rgba(14,12,11,.42); font-weight: 600; font-size: 34px;
              letter-spacing: .01em; backdrop-filter: blur(6px); }}
  .hook {{ position: absolute; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; gap: 10px; }}
  .hb {{ opacity: 0; }}
  .hb span {{ display: inline-block; background: #fff; color: #141210; font-weight: 760; font-size: 70px; line-height: 1.12;
             padding: 14px 28px 16px; border-radius: 16px; letter-spacing: -.01em; box-shadow: 0 10px 30px rgba(0,0,0,.18); }}
  .sub {{ position: absolute; left: 60px; right: 60px; text-align: center; }}
  .sl {{ opacity: 0; font-weight: 750; font-size: 66px; line-height: 1.14; letter-spacing: -.01em;
        text-shadow: 0 2px 4px rgba(0,0,0,.35), 0 6px 34px rgba(0,0,0,.45); }}
  .chipw {{ position: absolute; left: 0; right: 0; display: flex; justify-content: center; }}
  .chip {{ opacity: 0; padding: 14px 34px; border-radius: 999px; font-weight: 800; font-size: 38px; letter-spacing: .14em;
          padding-left: calc(34px + .14em); }}
  .chip.dark {{ background: rgba(14,12,11,.78); color: #fff; }}
  .chip.light {{ background: #fff; color: #141210; box-shadow: 0 10px 30px rgba(0,0,0,.2); }}
  .scrim {{ position: absolute; left: 0; right: 0; opacity: 0; }}
  .cta {{ position: absolute; left: 50px; right: 50px; top: 1150px; display: flex; flex-direction: column; align-items: center; text-align: center; }}
  .ck {{ opacity: 0; font-weight: 650; font-size: 38px; letter-spacing: .02em; margin-bottom: 22px;
        text-shadow: 0 2px 18px rgba(0,0,0,.5); }}
  .cm {{ opacity: 0; }}
  .cm span {{ display: inline-block; background: #fff; color: #141210; font-weight: 800; font-size: 58px; line-height: 1.12;
             padding: 22px 40px 24px; border-radius: 22px; box-shadow: 0 16px 44px rgba(0,0,0,.28); }}
  .cf {{ opacity: 0; margin-top: 24px; font-weight: 600; font-size: 36px; text-shadow: 0 2px 18px rgba(0,0,0,.55); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-start="0" data-duration="{dur}" data-fps="30">
  {chr(10).join("  " + x for x in body).strip()}
  <div class="loc" id="loc"><span>📍 {E(spec.get("loc", "St. Moritz"))}</span></div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      {(chr(10) + "      ").join(js)}
      tl.set({{}}, {{}}, {dur});
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    }})();
  </script>
</div>
</body>
</html>
"""
(hf / "index.html").write_text(page)
print("ok", hf / "index.html")
