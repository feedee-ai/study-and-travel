# Ролик A — «Безкоштовний вебінар для батьків». Генерирует HyperFrames-проект в a-webinar/
import json, os
from hflib import *

P = os.path.join(WORK, "a-webinar")
E = json.load(open(os.path.join(P, "build/edl_out.json")))
SEG = {s["tag"]: s["t0"] for s in E["segments"]}
VD = E["duration"]                    # конец голоса
END0 = round(VD - 0.25, 3)            # старт энд-карда
DUR = round(VD + 3.2, 2)             # длина ролика

copy_assets(P, [(os.path.join(P, "build/plate.mp4"), "plate.mp4"), (os.path.join(P, "build/voice.wav"), "voice.wav")])
GIFT = open(os.path.join(WORK, "shared/img/icn_gift.svg")).read() if os.path.exists(os.path.join(WORK, "shared/img/icn_gift.svg")) else ""

# ---------- билет ----------
TICKET_CSS = """
.ticket{position:absolute;width:900px;height:340px;background:var(--y);border-radius:30px;
  -webkit-mask:radial-gradient(circle 28px at 676px 0px,#0000 97%,#000 100%),radial-gradient(circle 28px at 676px 340px,#0000 97%,#000 100%);
  -webkit-mask-composite:source-in;mask-composite:intersect;}
.ticket .perf{position:absolute;left:674px;top:44px;height:252px;border-left:5px dashed rgba(17,17,17,.38);}
.ticket .lb{position:absolute;left:46px;top:34px;font-weight:700;font-size:28px;letter-spacing:.32em;color:#111;}
.ticket .big{position:absolute;left:42px;font-weight:900;font-size:68px;line-height:1;color:#111;letter-spacing:-.01em;}
.ticket .sm{position:absolute;left:46px;top:258px;font-weight:600;font-size:28px;color:#111;}
.ticket .stub{position:absolute;left:680px;top:0;width:220px;height:340px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#111;}
.ticket .stub .s1{font-weight:700;font-size:28px;letter-spacing:.32em;margin-left:.32em;}
.ticket .stub .s2{font-weight:900;font-size:92px;line-height:1.05;}
.ticket .stub .s3{font-weight:700;font-size:28px;letter-spacing:.06em;}
"""
def ticket(id_, left, top):
    return f"""    <div id="{id_}" class="ticket f sh" data-layout-allow-overlap style="left:{left}px;top:{top}px">
      <div class="perf"></div>
      <div class="lb">ЗАПРОШЕННЯ</div>
      <div class="big" style="top:84px">БЕЗКОШТОВНИЙ</div>
      <div class="big" style="top:156px">ВЕБІНАР</div>
      <svg id="{id_}-ul" class="abs" style="left:36px;top:142px" width="560" height="30" viewBox="0 0 560 30"><path d="M6 18 C 120 6, 260 28, 380 14 S 520 10, 552 16" fill="none" stroke="#E5302B" stroke-width="9" stroke-linecap="round"/></svg>
      <div class="sm">для батьків · вступ до Словаччини</div>
      <div class="stub"><div class="s1">ВХІД</div><div class="s2">0&#8202;₴</div><div class="s3">ВІЛЬНИЙ</div></div>
    </div>"""

files = {}

# ---------- 1. хук ----------
files["a-hook"] = scene("a-hook", """
    <div class="row" style="top:290px"><div id="h1" class="tape tk sh" style="font-size:96px;transform:rotate(-3deg)">Для батьків,</div></div>
    <div class="row" style="top:448px"><div id="h2" class="tape ty sh" style="font-size:54px;transform:rotate(1.5deg)">які розглядають вступ</div></div>
    <div class="row" style="top:538px"><div id="h3" class="tape ty sh" style="font-size:54px;transform:rotate(-1deg)">дитини до Словаччини</div></div>
""", """
    tl.fromTo('#h1',{scale:1.22,rotation:-7},{scale:1,rotation:-3,duration:0.32,ease:'expo.out'},0);
    tl.fromTo('#h2',{clipPath:'inset(0% 100% 0% 0%)'},{clipPath:'inset(0% 0% 0% 0%)',duration:0.34,ease:'power3.out'},0.72);
    tl.fromTo('#h3',{clipPath:'inset(0% 100% 0% 0%)'},{clipPath:'inset(0% 0% 0% 0%)',duration:0.34,ease:'power3.out'},2.3);
    tl.to(['#h1','#h2','#h3'],{y:-50,opacity:0,filter:'blur(8px)',duration:0.2,ease:'power3.in',stagger:0.04},3.18);
""")

# ---------- 2. билет ----------
T2 = 3.40
files["a-ticket"] = scene("a-ticket", ticket("tk1", 90, 300), f"""
    tl.fromTo('#tk1',{{x:980,rotation:14,filter:'blur(10px)'}},{{x:0,rotation:-2,filter:'blur(0px)',duration:0.55,ease:'expo.out'}},0.04);
    tl.fromTo('#tk1-ul path',{{strokeDasharray:620,strokeDashoffset:620}},{{strokeDashoffset:0,duration:0.38,ease:'power2.out'}},{4.30-T2:.2f});
    tl.to('#tk1',{{x:-1150,rotation:-12,duration:0.3,ease:'power3.in'}},{SEG['proof']-T2-0.18:.2f});
""", TICKET_CSS)

# ---------- 3. счётчик 1200+ ----------
T3 = SEG["proof"]
files["a-count"] = scene("a-count", """
    <div id="cc" class="abs f sh" style="left:90px;top:1050px;width:900px;height:250px;background:var(--y);border-radius:30px;color:#111">
      <div class="abs" style="left:46px;top:30px;font-weight:700;font-size:28px;letter-spacing:.3em">ПОНАД</div>
      <div class="abs" style="left:38px;top:62px;font-weight:900;font-size:150px;line-height:1;letter-spacing:-.03em;font-variant-numeric:tabular-nums;white-space:nowrap"><span id="cn">0</span><span id="cp" style="display:inline-block">+</span></div>
      <div class="abs" style="left:540px;top:78px;width:330px">
        <div style="font-weight:900;font-size:46px;line-height:1.05">студентів</div>
        <div style="font-weight:600;font-size:31px;line-height:1.2;margin-top:8px">супроводили на&nbsp;шляху до&nbsp;вступу</div>
      </div>
    </div>
""", f"""
    const cnt = {{v:0}};
    const cn = document.querySelector('#cn');
    tl.fromTo('#cc',{{y:160,opacity:0}},{{y:0,opacity:1,duration:0.45,ease:'expo.out'}},{8.55-T3:.2f});
    tl.fromTo(cnt,{{v:0}},{{v:1200,duration:0.85,ease:'power3.out',onUpdate:()=>{{cn.textContent=String(Math.round(cnt.v));}}}},{8.68-T3:.2f});
    tl.fromTo('#cp',{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:'expo.out'}},{9.5-T3:.2f});
    tl.to('#cc',{{y:120,opacity:0,duration:0.2,ease:'power3.in'}},{SEG['step']-T3-0.2:.2f});
""")

# ---------- 4. программа вебинара (спикер в круге) ----------
T4 = SEG["step"]; T4E = SEG["qa"]
items = [("Вибір університету і спеціальності", SEG["ag1"]),
         ("Які документи підготувати", SEG["ag2"]),
         ("Коли подавати заявку", SEG["ag3"]),
         ("Як навчатися <span id='hl' class='hl'><i id='hlm'></i><b>безкоштовно</b></span>", SEG["ag4"] + 0.1),
         ("Витрати на проживання", 22.05),
         ("Що чекає після переїзду", 24.05)]
rows, js = [], []
for i, (txt, t) in enumerate(items):
    y = 838 + i * 84
    rows.append(f"""    <div id="it{i}" class="abs f" style="left:90px;top:{y}px;height:66px;display:flex;align-items:center;gap:22px;white-space:nowrap">
      <div class="num">{i+1}</div><div class="itx">{txt}</div></div>""")
    js.append(f"tl.fromTo('#it{i}',{{x:-46,opacity:0,filter:'blur(6px)'}},{{x:0,opacity:1,filter:'blur(0px)',duration:0.36,ease:'expo.out'}},{t-T4:.2f});")
js.append(f"tl.fromTo('#hlm',{{scaleX:0}},{{scaleX:1,duration:0.3,ease:'power3.out'}},{19.86-T4:.2f});")
js.append(f"tl.to('#hl b',{{color:'#fff',duration:0.12}},{19.92-T4:.2f});")
files["a-program"] = scene("a-program", f"""
    <div id="ring" class="abs" style="left:278px;top:186px;width:524px;height:524px;border-radius:50%;border:12px solid #111"></div>
    <div id="kk" class="abs hand" style="left:700px;top:600px;font-size:66px;color:#111;transform:rotate(-8deg);white-space:nowrap">крок за кроком</div>
    <div class="row" style="top:740px"><div id="ph" class="tape tk" style="font-size:46px;padding:12px 26px 14px">ПРОГРАМА ВЕБІНАРУ</div></div>
{chr(10).join(rows)}
""", f"""
    tl.fromTo('#ring',{{scale:1.9,opacity:0}},{{scale:1,opacity:1,duration:0.6,ease:'power3.inOut'}},0.05);
    tl.fromTo('#ph',{{clipPath:'inset(0% 100% 0% 0%)'}},{{clipPath:'inset(0% 0% 0% 0%)',duration:0.36,ease:'power3.out'}},0.55);
    tl.fromTo('#kk',{{opacity:0,scale:0.6,rotation:-20}},{{opacity:1,scale:1,rotation:-8,duration:0.4,ease:'expo.out'}},{12.09-T4:.2f});
    {chr(10).join('    '+j for j in js)}
    tl.to(['#ring','#kk','#ph'],{{opacity:0,scale:1.12,duration:0.28,ease:'power3.in'}},{T4E-T4-0.2:.2f});
    tl.to('[id^=it]',{{opacity:0,x:60,duration:0.24,ease:'power3.in',stagger:0.025}},{T4E-T4-0.3:.2f});
""", """
    .num{width:68px;height:68px;border-radius:16px;background:#111;color:var(--y);font-weight:900;font-size:38px;display:flex;align-items:center;justify-content:center;}
    .itx{font-weight:800;font-size:40px;color:#111;}
    .hl{position:relative;display:inline-block;isolation:isolate;}
    .hl i{position:absolute;left:-10px;right:-10px;top:-4px;bottom:-6px;background:#E5302B;border-radius:10px;transform-origin:0 50%;z-index:-1;}
    .hl b{font-weight:900;}
""")

# ---------- 5. Q&A ----------
T5 = SEG["qa"]
files["a-qa"] = scene("a-qa", """
    <div id="qb" class="abs f sh" style="left:90px;top:850px;padding:24px 34px;background:#fff;border-radius:38px 38px 38px 10px;max-width:760px">
      <div id="qd" class="abs" style="left:34px;top:34px;display:flex;gap:12px"><i class="dot"></i><i class="dot"></i><i class="dot"></i></div>
      <div id="qt" style="font-weight:800;font-size:44px;line-height:1.15;color:#111">А навчання справді безкоштовне?</div>
    </div>
    <div id="ab" class="abs f sh" style="right:90px;top:1000px;padding:20px 30px;background:var(--y);border-radius:38px 38px 10px 38px;display:flex;align-items:center;gap:18px">
      <svg width="54" height="54" viewBox="0 0 48 48"><circle cx="24" cy="24" r="24" fill="#111"/><path d="M13 25 l7 7 l15 -16" fill="none" stroke="#FDDC27" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <div style="font-weight:800;font-size:40px;line-height:1.15;color:#111">Розповімо, за&nbsp;яких умов</div>
    </div>
""", f"""
    tl.fromTo('#qb',{{scale:0.6,opacity:0,transformOrigin:'0% 100%'}},{{scale:1,opacity:1,duration:0.4,ease:'expo.out'}},0.15);
    tl.fromTo('#qt',{{opacity:0}},{{opacity:1,duration:0.15}},0.6);
    tl.set('#qd',{{opacity:0}},0.6);
    tl.fromTo('#qd .dot',{{y:0}},{{y:-10,duration:0.18,ease:'sine.inOut',yoyo:true,repeat:1,stagger:0.06}},0.2);
    tl.fromTo('#ab',{{scale:0.6,opacity:0,transformOrigin:'100% 100%'}},{{scale:1,opacity:1,duration:0.4,ease:'expo.out'}},{27.95-T5:.2f});
    tl.to(['#qb','#ab'],{{opacity:0,y:-40,duration:0.22,ease:'power3.in',stagger:0.05}},{SEG['cta']-T5-0.25:.2f});
""", """
    #qt{opacity:0;}
    .dot{display:block;width:16px;height:16px;border-radius:50%;background:#9a9a9a;}
""")

# ---------- 6. CTA: билет возвращается + подарок ----------
T6 = SEG["cta"]
files["a-cta"] = scene("a-cta", ticket("tk2", 90, 790) + f"""
    <div id="gift" class="abs f" style="left:800px;top:676px;width:190px;height:190px;border-radius:50%;background:#fff;box-shadow:0 14px 34px rgba(0,0,0,.28);display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(10deg)">
      <svg width="70" height="70" viewBox="0 0 24 24" fill="none" stroke="#E5302B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C10 3 12 8 12 8s2-5 4.5-5a2.5 2.5 0 0 1 0 5"/></svg>
      <div class="hand" style="font-size:36px;line-height:.95;text-align:center;color:#111;margin-top:2px">подарунок<br>кожному</div>
    </div>
""", f"""
    tl.fromTo('#tk2',{{y:520,rotation:8,opacity:0,scale:0.82}},{{y:0,rotation:-2,opacity:1,scale:0.82,duration:0.55,ease:'expo.out'}},{29.45-T6:.2f});
    tl.set('#tk2-ul path',{{strokeDasharray:620,strokeDashoffset:0}},0);
    tl.fromTo('#gift',{{scale:0,rotation:-40}},{{scale:1,rotation:10,duration:0.5,ease:'back.out(1.6)'}},{31.35-T6:.2f});
""", TICKET_CSS)

# ---------- 7. энд-кард ----------
files["a-end"] = scene("a-end", f"""
    <div id="eb" class="abs" style="left:0;top:0;width:1080px;height:1920px;background:var(--y)"></div>
    <div class="row" style="top:300px"><div style="position:relative;width:504px;height:135px">{logo('elogo', '#111', 0.9)}</div></div>
    <div class="row" style="top:500px"><div id="et1" class="f" style="font-weight:900;font-size:98px;line-height:1;color:#111;letter-spacing:-.01em">БЕЗКОШТОВНИЙ</div></div>
    <div class="row" style="top:604px"><div id="et2" class="tape tk" style="font-size:98px;padding:6px 30px 14px">ВЕБІНАР</div></div>
    <div class="row" style="top:770px"><div id="es" class="f" style="width:860px;text-align:center;font-weight:600;font-size:36px;line-height:1.3;color:#111">для батьків, які розглядають вступ дитини до&nbsp;Словаччини</div></div>
    <div class="row" style="top:900px"><div id="eg" class="f" style="display:flex;align-items:center;gap:16px;font-weight:700;font-size:34px;color:#111">
      <svg width="52" height="52" viewBox="0 0 24 24" fill="none" stroke="#E5302B" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C10 3 12 8 12 8s2-5 4.5-5a2.5 2.5 0 0 1 0 5"/></svg>
      подарунок кожному учаснику</div></div>
    <div class="row" style="top:1010px"><div id="ebt" class="f" style="background:#111;color:var(--y);font-weight:800;font-size:54px;padding:26px 56px 30px;border-radius:24px;box-shadow:0 14px 0 rgba(0,0,0,.18)">Зареєструватися</div></div>
    <div class="row" style="top:1160px"><div id="ea">{ARROW_DOWN.format(w=60, h=120, c='#111')}</div></div>
""", f"""
    tl.fromTo('#eb',{{clipPath:'circle(0px at 540px 860px)'}},{{clipPath:'circle(1500px at 540px 860px)',duration:0.55,ease:'power2.inOut'}},0);
    tl.fromTo('#elogo',{{y:-40,opacity:0}},{{y:0,opacity:1,duration:0.45,ease:'expo.out'}},0.38);
    tl.fromTo('#et1',{{y:50,opacity:0,filter:'blur(8px)'}},{{y:0,opacity:1,filter:'blur(0px)',duration:0.4,ease:'expo.out'}},0.5);
    tl.fromTo('#et2',{{scale:1.3,opacity:0,rotation:-6}},{{scale:1,opacity:1,rotation:-2,duration:0.36,ease:'expo.out'}},0.62);
    tl.fromTo(['#es','#eg'],{{y:24,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:'expo.out',stagger:0.1}},0.78);
    tl.fromTo('#ebt',{{scale:0.7,opacity:0}},{{scale:1,opacity:1,duration:0.4,ease:'expo.out'}},1.0);
    tl.fromTo('#ea .ar',{{strokeDasharray:130,strokeDashoffset:130}},{{strokeDashoffset:0,duration:0.35,ease:'power2.out'}},1.25);
    tl.fromTo('#ea .ah',{{opacity:0}},{{opacity:1,duration:0.1}},1.55);
    tl.to('#ebt',{{scale:0.94,duration:0.08,ease:'power2.in'}},1.95);
    tl.to('#ebt',{{scale:1,duration:0.25,ease:'expo.out'}},2.03);
""")

# ---------- субтитры ----------
fixes = {}
for i, w in enumerate(E["words"]):
    if w["w"] == "зможе": fixes[i] = "зможете"
    if w["w"] == "бронюєте": fixes[i] = "бронюйте"
hide = [(0, 5.3), (SEG["proof"] - 0.1, SEG["qa"] - 0.05), (END0, 99)]
groups = build_groups(E["words"], hide=hide, fixes=fixes)
for g in groups:
    g["t1"] = min(g["t1"], END0 + 0.05)
files["a-captions"] = captions_scene("a-captions", groups, ycenter=1200)

for k, v in files.items():
    write(os.path.join(P, "compositions", k + ".html"), v)

# ---------- звук ----------
SFX = [("whoosh-short", 3.42, .45), ("pop", 4.30, .35), ("whoosh", 8.52, .3), ("ping", 9.50, .3),
       ("whoosh", T4 + 0.02, .4), ("click-soft", SEG["ag1"], .45), ("click", SEG["ag2"], .3), ("click-soft", SEG["ag3"], .45),
       ("click", SEG["ag4"] + 0.1, .3), ("pop", 19.86, .4), ("click-soft", 22.05, .45), ("click", 24.05, .3),
       ("whoosh-short", T4E - 0.1, .4), ("notification", T5 + 0.15, .25), ("pop", 27.95, .35),
       ("whoosh-short", 29.43, .4), ("sparkle", 31.35, .3), ("whoosh", END0, .4), ("impact-bass-1", END0 + 0.4, .3),
       ("click", END0 + 1.95, .45)]
man = json.load(open(os.path.join(SFX_DIR, "manifest.json")))
sfx_html = []
for i, (n, t, v) in enumerate(SFX):
    import shutil; shutil.copy(os.path.join(SFX_DIR, n + ".mp3"), os.path.join(P, "assets/sfx", n + ".mp3"))
    d = man[n]["duration"]
    sfx_html.append(f'      <audio id="sfx{i}" class="clip" src="assets/sfx/{n}.mp3" data-start="{t:.2f}" data-duration="{d}" data-track-index="{20+i}" data-volume="{v}"></audio>')

# ---------- корень ----------
def pw(s, fx, fy, cx=None, cy=None):
    """масштаб s так, чтобы точка лица (fx,fy) оказалась в (cx,cy) (по умолчанию — на месте)"""
    cx = fx if cx is None else cx; cy = fy if cy is None else cy
    return f"{{scale:{s},x:{cx - s*fx:.1f},y:{cy - s*fy:.1f}}}"

root_js = [
    "tl.set('#pw',{transformOrigin:'0px 0px',scale:1,x:0,y:0},0);",
    f"tl.set('#pw',{pw(1.12, 538, 856)},2.78);",
    f"tl.set('#pw',{pw(1, 538, 856)},{T2+0.04});",
    f"tl.set('#pw',{pw(1, 600, 730)},{SEG['proof']});",
    f"tl.set('#pw',{pw(1.1, 600, 730)},9.03);",
    f"tl.set('#pw',{pw(1, 600, 730)},{SEG['step']});",
    # жёлтый мир + круг
    f"tl.fromTo('#gy',{{clipPath:'inset(100% 0% 0% 0%)'}},{{clipPath:'inset(0% 0% 0% 0%)',duration:0.3,ease:'power2.out'}},{T4-0.06});",
    f"tl.fromTo('#pclip',{{clipPath:'circle(1900px at 540px 448px)'}},{{clipPath:'circle(250px at 540px 448px)',duration:0.62,ease:'power3.inOut'}},{T4+0.12});",
    f"tl.to('#pw',{{...{pw(0.6, 600, 735, 540, 456)},duration:0.62,ease:'power3.inOut'}},{T4+0.12});",
    f"tl.set('#pw',{pw(0.95, 540, 628, 540, 456)},{SEG['ag1']});",
    f"tl.set('#pw',{pw(0.6, 600, 735, 540, 456)},{SEG['ag2']});",
    f"tl.set('#pw',{pw(0.95, 540, 628, 540, 456)},{SEG['ag3']});",
    f"tl.set('#pw',{pw(0.6, 600, 735, 540, 456)},{SEG['ag4']});",
    f"tl.set('#pw',{pw(0.95, 540, 628, 540, 456)},{SEG['ag56']});",
    f"tl.to('#pclip',{{clipPath:'circle(1900px at 540px 448px)',duration:0.55,ease:'power3.inOut'}},{T4E-0.12});",
    f"tl.to('#pw',{{scale:1,x:0,y:0,duration:0.55,ease:'power3.inOut'}},{T4E-0.12});",
    f"tl.to('#gy',{{clipPath:'inset(0% 0% 100% 0%)',duration:0.5,ease:'power2.inOut'}},{T4E+0.1});",
    f"tl.set('#pw',{pw(1.08, 530, 604)},{SEG['cta']+2.0});",
]
root_body = f"""      <div id="gy" class="full" style="background:#FDDC27;z-index:0"></div>
      <div id="pclip" class="full" style="z-index:1">
        <div id="pw" class="full">
          <video id="plate" class="clip full" src="assets/plate.mp4" data-start="0" data-duration="{VD}" data-track-index="1" muted playsinline></video>
        </div>
      </div>
      <audio id="voice" class="clip" src="assets/voice.wav" data-start="0" data-duration="{VD}" data-track-index="2" data-volume="1"></audio>
{chr(10).join(sfx_html)}
{host('a-hook', 0, 3.5, 10, 3)}
{host('a-ticket', T2, round(SEG['proof'] - T2 + 0.15, 2), 11, 4)}
{host('a-count', SEG['proof'], round(SEG['step'] - SEG['proof'], 2), 12, 5)}
{host('a-program', T4, round(T4E - T4 + 0.1, 2), 13, 6)}
{host('a-qa', T5, round(SEG['cta'] - T5, 2), 14, 7)}
{host('a-cta', T6, round(END0 - T6 + 0.6, 2), 15, 8)}
{host('a-end', END0, round(DUR - END0, 2), 40, 9)}
{host('a-captions', 0, DUR, 30, 10, 'captions')}"""
write(os.path.join(P, "index.html"), index_html(DUR, root_body, "\n      ".join(root_js)))
print("A:", DUR, "s;", len(groups), "групп субтитров")
