# Ролик B — история студентки → «Безкоштовна консультація». Генерирует HyperFrames-проект в b-consult/
import json, os, shutil
from hflib import *

P = os.path.join(WORK, "b-consult")
E = json.load(open(os.path.join(P, "build/edl_out.json")))
SEG = {s["tag"]: s["t0"] for s in E["segments"]}
VD = E["duration"]
for f in ("hyperframes.json", "package.json", "meta.json"):
    if not os.path.exists(os.path.join(P, f)):
        shutil.copy(os.path.join(WORK, "a-webinar", f), os.path.join(P, f))
BRS = ("brNitra", "br15", "brPrague", "brBarca", "brParis")
copy_assets(P, [(os.path.join(P, "build", n), n) for n in ("plate.mp4", "voice.wav")] + [(os.path.join(P, "build", b + ".mp4"), b + ".mp4") for b in BRS])

def WT(txt, tag=None):
    """время начала слова (по смонтированной дорожке)"""
    for w in E["words"]:
        if w["w"].lower().strip(".,?!:") == txt and (tag is None or w["tag"] == tag):
            return w["t"]
    raise SystemExit("нет слова " + txt)

T_W0 = SEG["worry"] - 0.04      # уход в полароид
T_W1 = SEG["mom2"]              # «але з часом» — склейка посреди раскрытия полароида
T_L = SEG["life1"]              # B-roll
T_EDU = WT("навчаюсь") - 0.03   # лекция
T_BACK = WT("легально") - 0.02  # резкий возврат на спикера
T_TR = SEG["life3"] + 0.12      # «а інколи ми подорожуємо Європою…»
T_TR1 = round(T_TR + (SEG["brand"] - T_TR) / 3, 3); T_TR2 = round(T_TR + 2 * (SEG["brand"] - T_TR) / 3, 3)
# (id, старт, конец, нахлёст под следующий wipe, свой наезд)
BR = [("brNitra", T_L, T_EDU, 0.3, False), ("br15", T_EDU, T_BACK, 0, True),
      ("brPrague", T_TR, T_TR1, 0.3, True), ("brBarca", T_TR1, T_TR2, 0.3, True), ("brParis", T_TR2, SEG["brand"], 0, True)]
T_LOGO = WT("стадіїн") - 0.05
T_R0 = SEG["steps"]; T_R1 = SEG["cta"]
T_BTN = WT("тисніть") - 0.03
T_PRESS = WT("детальніше", "cta")
END0 = round(WT("безкоштовну", "cta") - 0.12, 3)
DUR = round(VD + 3.0, 2)

files = {}

# ---------- 1. хук-вопрос ----------
files["b-hook"] = scene("b-hook", """
    <div class="row" style="top:250px"><div id="q1" class="tape tk sh" style="font-size:92px;transform:rotate(-2deg)">Хвилюєтесь</div></div>
    <div class="row" style="top:382px"><div id="q2" class="tape tw sh" style="font-size:62px;transform:rotate(1.5deg)">відпускати дитину</div></div>
    <div class="row" style="top:478px"><div id="q3" class="tape ty sh" style="font-size:56px;transform:rotate(-1deg)">на навчання за кордон?</div></div>
""", f"""
    tl.fromTo('#q1',{{scale:1.25,rotation:-8}},{{scale:1,rotation:-2,duration:0.3,ease:'expo.out'}},0);
    tl.fromTo('#q2',{{clipPath:'inset(0% 100% 0% 0%)'}},{{clipPath:'inset(0% 0% 0% 0%)',duration:0.34,ease:'power3.out'}},0.84);
    tl.fromTo('#q3',{{clipPath:'inset(0% 100% 0% 0%)'}},{{clipPath:'inset(0% 0% 0% 0%)',duration:0.42,ease:'power3.out'}},1.9);
    tl.to(['#q1','#q2','#q3'],{{y:-40,opacity:0,filter:'blur(8px)',duration:0.2,ease:'power3.in',stagger:0.04}},{SEG['hook2']-0.2:.2f});
""")

# ---------- 2. рукописная заметка «студентка» ----------
T_N = SEG["hook2"]
files["b-note"] = scene("b-note", """
    <div id="nt" class="abs hand" style="left:70px;top:250px;font-size:92px;line-height:.9;color:#111;transform:rotate(-5deg);text-shadow:0 0 22px rgba(255,255,255,.75)">я — студентка<br>у Словаччині</div>
    <svg id="na" class="abs" style="left:590px;top:300px;overflow:visible" width="230" height="230" viewBox="0 0 230 230">
      <path class="ar" d="M10 20 C 120 0, 200 60, 150 170" fill="none" stroke="#111" stroke-width="8" stroke-linecap="round"/>
      <path class="ah" d="M126 146 L150 176 L178 150" fill="none" stroke="#111" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
""", f"""
    tl.fromTo('#nt',{{opacity:0,clipPath:'inset(0% 100% 0% 0%)'}},{{opacity:1,clipPath:'inset(0% 0% 0% 0%)',duration:0.5,ease:'power2.out'}},{5.45-T_N:.2f});
    tl.fromTo('#na .ar',{{strokeDasharray:300,strokeDashoffset:300}},{{strokeDashoffset:0,duration:0.35,ease:'power2.out'}},{5.85-T_N:.2f});
    tl.fromTo('#na .ah',{{opacity:0}},{{opacity:1,duration:0.08}},{6.18-T_N:.2f});
    tl.to(['#nt','#na'],{{opacity:0,y:-30,duration:0.2,ease:'power3.in'}},{SEG['know']-T_N-0.22:.2f});
""")

# ---------- 3. тревоги: ленты + полароид ----------
tapes = [("ДИТИНА ДАЛЕКО", SEG["worry"], "tk", -3, -40, 252), ("ЧУЖА КРАЇНА", WT("чужа"), "ty", 2, 50, 344),
         ("НОВІ ЛЮДИ", WT("нові"), "tw", -2, -70, 436), ("НЕЗНАЙОМЕ ЖИТТЯ", WT("незнайоме"), "ty", 2, 30, 528)]
tb, tj = [], []
for i, (txt, t, cls, rot, dx, y) in enumerate(tapes):
    tb.append(f"    <div class='row' style='top:{y}px'><div id='tp{i}' class='tape {cls} sh' style='font-size:52px;letter-spacing:.01em;margin-left:{dx*2}px'>{txt}</div></div>")
    tj.append(f"tl.fromTo('#tp{i}',{{opacity:0,scale:1.5,rotation:{rot*3}}},{{opacity:1,scale:1,rotation:{rot},duration:0.22,ease:'expo.out'}},{t-T_W0:.2f});")
    tj.append(f"tl.to('#tp{i}',{{x:{'-' if i%2==0 else ''}1300,rotation:{rot*4},duration:0.38,ease:'power3.in'}},{T_W1-T_W0-0.38+0.05*i:.2f});")
files["b-worry"] = scene("b-worry", "\n".join(tb) + f"""
    <div id="pn1" class="abs hand" style="left:236px;top:1262px;width:608px;text-align:center;font-size:52px;line-height:1;color:#111">моя мама теж переживала</div>
""", "\n    ".join(tj) + f"""
    tl.fromTo('#pn1',{{opacity:0,clipPath:'inset(0% 100% 0% 0%)'}},{{opacity:1,clipPath:'inset(0% 0% 0% 0%)',duration:0.5,ease:'power2.out'}},{SEG['mom']-T_W0:.2f});
    tl.to('#pn1',{{opacity:0,duration:0.15}},{T_W1-T_W0-0.32:.2f});
""")

# ---------- 4. реальность: чек-лист поверх B-roll ----------
life = [("гарне місце", WT("гарному")), ("навчання", WT("навчаюсь")), ("легальний підробіток", WT("легально")), ("друзі", WT("друзів")), ("подорожі Європою", WT("подорожуємо"))]
lb, lj = [], []
for i, (txt, t) in enumerate(life):
    y = 880 + i * 84
    lb.append(f"""    <div id="lf{i}" class="abs f" style="left:90px;top:{y}px;display:flex;align-items:center;gap:16px">
      <div class="ckw">{CHECK_SVG.format(s=60, bg='#FDDC27', fg='#111')}</div>
      <div class="tape tw" style="font-size:44px;font-weight:800;padding:8px 22px 12px;border-radius:12px">{txt}</div></div>""")
    lj.append(f"tl.fromTo('#lf{i}',{{x:-60,opacity:0}},{{x:0,opacity:1,duration:0.32,ease:'expo.out'}},{t-T_L:.2f});")
    lj.append(f"tl.fromTo('#lf{i} .ck',{{strokeDasharray:40,strokeDashoffset:40}},{{strokeDashoffset:0,duration:0.25,ease:'power2.out'}},{t-T_L+0.12:.2f});")
files["b-life"] = scene("b-life", f"""
    <div id="lh" class="abs hand" style="left:96px;top:790px;font-size:70px;color:#fff;transform:rotate(-3deg);text-shadow:0 4px 18px rgba(0,0,0,.5)">а тепер:</div>
""" + "\n".join(lb), f"""
    tl.fromTo('#lh',{{opacity:0,clipPath:'inset(0% 100% 0% 0%)'}},{{opacity:1,clipPath:'inset(0% 0% 0% 0%)',duration:0.35,ease:'power2.out'}},0.1);
    {chr(10).join('    '+j for j in lj)}
    tl.to(['#lh','[id^=lf]'],{{opacity:0,x:-80,duration:0.25,ease:'power3.in',stagger:0.03}},{SEG['brand']-T_L-0.3:.2f});
""", """
    .ckw{width:60px;height:60px;filter:drop-shadow(0 6px 14px rgba(0,0,0,.35));}
    #root .sh2{box-shadow:0 10px 26px rgba(0,0,0,.3);}
    [id^=lf] .tape{box-shadow:0 10px 26px rgba(0,0,0,.3);}
""")

# ---------- 5. логотип ----------
T_B = SEG["brand"]
files["b-brand"] = scene("b-brand", f"""
    <div id="lc" class="abs" style="left:170px;top:1010px;width:740px;height:220px;background:#fff;border-radius:32px;box-shadow:0 18px 40px rgba(0,0,0,.3)">
      <div style="position:absolute;left:118px;top:42px">{logo('blogo', '#111', 0.9)}</div>
    </div>
""", f"""
    tl.fromTo('#lc',{{scale:0.5,opacity:0,rotation:-8}},{{scale:1,opacity:1,rotation:-2,duration:0.42,ease:'back.out(1.7)'}},{T_LOGO-T_B:.2f});
    tl.to('#lc',{{y:-80,scale:0.8,opacity:0,duration:0.28,ease:'power3.in'}},{T_R0-T_B-0.1:.2f});
""")

# ---------- 6. маршрут: 4 остановки ----------
stops = [("Підбір університету", "та спеціальності", WT("під", "route") - 0.05), ("Підготовка", "документів", WT("підготовка") - 0.05), ("Вивчення мови", "", WT("вивчення") - 0.05)]
T_CUR = WT("особистий") - 0.03
sb, sj = [], []
for i, (a, b, t) in enumerate(stops):
    y = 520 + i * 165
    sb.append(f"""    <div id="st{i}" class="abs f" style="left:80px;top:{y}px;width:500px;display:flex;gap:22px;align-items:flex-start">
      <div class="dotc"></div>
      <div><div style="font-weight:900;font-size:44px;line-height:1.05;color:#111">{a}</div>{f'<div style="font-weight:700;font-size:34px;line-height:1.15;color:#111">{b}</div>' if b else ''}</div></div>""")
    sj.append(f"tl.fromTo('#st{i}',{{x:-40,opacity:0}},{{x:0,opacity:1,duration:0.34,ease:'expo.out'}},{t-T_R0:.2f});")
    sj.append(f"tl.fromTo('#st{i} .dotc',{{scale:0}},{{scale:1,duration:0.3,ease:'back.out(2.2)'}},{t-T_R0:.2f});")
    sj.append(f"tl.to('#rline',{{clipPath:'inset(0px 0px {max(0, 640 - (i+1)*165 - 40)}px 0px)',duration:0.5,ease:'power2.inOut'}},{t-T_R0-0.2:.2f});")
files["b-route"] = scene("b-route", f"""
    <div id="rh" class="abs" style="left:80px;top:262px">
      <div class="tape tk" style="font-size:52px;padding:10px 24px 14px;transform:rotate(-2deg)">НА КОЖНОМУ</div><br>
      <div class="tape tk" style="font-size:52px;padding:10px 24px 14px;margin-top:10px;transform:rotate(-2deg)">ЕТАПІ</div>
    </div>
    <svg id="rline" class="abs" style="left:96px;top:540px" width="12" height="640" viewBox="0 0 12 640"><line x1="6" y1="0" x2="6" y2="640" stroke="#111" stroke-width="6" stroke-dasharray="14 12" stroke-linecap="round"/></svg>
{chr(10).join(sb)}
    <div id="cur" class="abs f" style="left:80px;top:1040px;width:920px;height:230px;background:#111;border-radius:30px;display:flex;align-items:center;gap:28px;padding:0 40px;box-shadow:0 18px 40px rgba(0,0,0,.25)">
      <svg width="86" height="104" viewBox="0 0 24 29"><path d="M12 0C5.4 0 0 5.2 0 11.7 0 20.4 12 29 12 29s12-8.6 12-17.3C24 5.2 18.6 0 12 0z" fill="#FDDC27"/><circle cx="12" cy="11.5" r="4.6" fill="#111"/></svg>
      <div><div style="font-weight:900;font-size:60px;line-height:1.02;color:#fff">Особистий куратор</div>
        <div style="font-weight:800;font-size:46px;line-height:1.15;color:#FDDC27">у Словаччині</div></div>
    </div>
""", f"""
    tl.fromTo('#rh',{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.4,ease:'expo.out'}},0.3);
    tl.set('#rline',{{clipPath:'inset(0px 0px 640px 0px)'}},0);
    {chr(10).join('    '+j for j in sj)}
    tl.to('#rline',{{clipPath:'inset(0px 0px 0px 0px)',duration:0.4,ease:'power2.inOut'}},{T_CUR-0.16-T_R0:.2f});
    tl.fromTo('#cur',{{scale:0.6,opacity:0,y:60}},{{scale:1,opacity:1,y:0,duration:0.45,ease:'back.out(1.5)'}},{T_CUR-T_R0:.2f});
    tl.to(['#rh','#rline','[id^=st]','#cur'],{{opacity:0,y:40,duration:0.25,ease:'power3.in',stagger:0.03}},{T_R1-T_R0-0.3:.2f});
""", """
    .dotc{flex:none;width:44px;height:44px;border-radius:50%;background:#111;border:9px solid #fff;margin-top:2px;box-shadow:0 0 0 4px #111;}
""")

# ---------- 7. CTA-кнопка и энд-кард ----------
T_C = SEG["cta"]
files["b-cta"] = scene("b-cta", """
    <div class="row" style="top:1080px"><div id="bt" class="f" style="display:flex;align-items:center;gap:18px;background:#FDDC27;color:#111;font-weight:800;font-size:56px;padding:24px 48px 28px;border-radius:24px;box-shadow:0 14px 0 rgba(0,0,0,.28),0 20px 40px rgba(0,0,0,.25)">Детальніше
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div></div>
""", f"""
    tl.fromTo('#bt',{{scale:0.6,opacity:0}},{{scale:1,opacity:1,duration:0.38,ease:'back.out(1.8)'}},{T_BTN-T_C:.2f});
    tl.to('#bt',{{scale:0.93,y:8,duration:0.08,ease:'power2.in'}},{T_PRESS-T_C:.2f});
    tl.to('#bt',{{scale:1,y:0,duration:0.25,ease:'expo.out'}},{T_PRESS+0.08-T_C:.2f});
""")
files["b-end"] = scene("b-end", f"""
    <div id="eb" class="abs" style="left:0;top:0;width:1080px;height:1920px;background:var(--y)"></div>
    <div class="row" style="top:300px"><div style="position:relative;width:504px;height:135px">{logo('elogo', '#111', 0.9)}</div></div>
    <div class="row" style="top:510px"><div id="et1" class="f" style="font-weight:900;font-size:100px;line-height:1;color:#111">БЕЗКОШТОВНА</div></div>
    <div class="row" style="top:616px"><div id="et2" class="tape tk" style="font-size:86px;padding:8px 30px 16px">КОНСУЛЬТАЦІЯ</div></div>
    <div class="row" style="top:780px"><div id="es" class="f" style="width:860px;text-align:center;font-weight:600;font-size:38px;line-height:1.3;color:#111">чіткий план дій, як вступити на&nbsp;безкоштовне навчання в&nbsp;Словаччині</div></div>
    <div class="row" style="top:1010px"><div id="ebt" class="f" style="display:flex;align-items:center;gap:18px;background:#111;color:var(--y);font-weight:800;font-size:56px;padding:24px 52px 28px;border-radius:24px;box-shadow:0 14px 0 rgba(0,0,0,.18)">Детальніше
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FDDC27" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div></div>
    <div class="row" style="top:1160px"><div id="ea">{ARROW_DOWN.format(w=60, h=120, c='#111')}</div></div>
""", f"""
    tl.fromTo('#eb',{{clipPath:'circle(0px at 540px 1140px)'}},{{clipPath:'circle(1700px at 540px 1140px)',duration:0.55,ease:'power2.inOut'}},0);
    tl.fromTo('#et1',{{y:50,opacity:0,filter:'blur(8px)'}},{{y:0,opacity:1,filter:'blur(0px)',duration:0.4,ease:'expo.out'}},0.12);
    tl.fromTo('#et2',{{scale:1.3,opacity:0,rotation:-6}},{{scale:1,opacity:1,rotation:-2,duration:0.36,ease:'expo.out'}},{WT('консультацію') - END0 - 0.05:.2f});
    tl.fromTo('#elogo',{{y:-40,opacity:0}},{{y:0,opacity:1,duration:0.45,ease:'expo.out'}},0.5);
    tl.fromTo('#es',{{y:24,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:'expo.out'}},1.25);
    tl.fromTo('#ebt',{{scale:0.7,opacity:0}},{{scale:1,opacity:1,duration:0.4,ease:'expo.out'}},1.5);
    tl.fromTo('#ea .ar',{{strokeDasharray:130,strokeDashoffset:130}},{{strokeDashoffset:0,duration:0.35,ease:'power2.out'}},1.75);
    tl.fromTo('#ea .ah',{{opacity:0}},{{opacity:1,duration:0.1}},2.05);
    tl.to('#ebt',{{scale:0.94,duration:0.08,ease:'power2.in'}},2.6);
    tl.to('#ebt',{{scale:1,duration:0.25,ease:'expo.out'}},2.68);
""")

# ---------- субтитры ----------
fixes = {}
W = E["words"]
for i, w in enumerate(W):
    if w["w"] == "знаю," and w["tag"] == "know": fixes[i] = "Я знаю,"
    if w["w"] == "мама" and w["tag"] == "mom": fixes[i] = "Моя мама"
    if w["w"] == "Вступу": fixes[i] = "Зі вступом"
    if w["w"] == "стадіїн": fixes[i] = "Study"
    if w["w"] == "Травел.": fixes[i] = "and Travel."
    if w["w"] == "під": fixes[i] = "Підбір"
    if w["w"] == "пір": fixes[i] = None
hide = [(0, SEG["hook2"] - 0.05), (T_W0, T_W1 - 0.02), (T_L - 0.02, SEG["brand"] - 0.05), (T_LOGO - 0.1, T_R1 - 0.05), (T_BTN - 0.05, 99)]
groups = build_groups(W, hide=hide, fixes=fixes)
files["b-captions"] = captions_scene("b-captions", groups, ycenter=1190)

for k, v in files.items():
    write(os.path.join(P, "compositions", k + ".html"), v)

# ---------- звук ----------
SFX = [("whoosh-short", SEG["hook2"] - 0.2, .3), ("pop", 5.45, .25),
       ("whoosh", T_W0, .4)] + [("click" if i % 2 else "pop", t, .4) for i, (_, t, *_r) in enumerate(tapes)] + [
       ("whoosh", T_W1 - 0.3, .45)] + [("whoosh-short", a, .35) for _b, a, *_r in BR] + [
       ("click-soft", t + 0.05, .45) for _, t in life] + [
       ("impact-bass-1", T_LOGO, .3), ("whoosh", T_R0 + 0.02, .4)] + [("click-soft", t, .45) for *_a, t in stops] + [
       ("ping", T_CUR, .3), ("whoosh-short", T_R1 - 0.1, .4), ("pop", T_BTN, .35), ("click", T_PRESS, .45),
       ("whoosh", END0, .4), ("click", END0 + 2.6, .45)]
man = json.load(open(os.path.join(SFX_DIR, "manifest.json")))
sfx_html = []
for i, (n, t, v) in enumerate(SFX):
    shutil.copy(os.path.join(SFX_DIR, n + ".mp3"), os.path.join(P, "assets/sfx", n + ".mp3"))
    sfx_html.append(f'      <audio id="sfx{i}" class="clip" src="assets/sfx/{n}.mp3" data-start="{t:.2f}" data-duration="{man[n]["duration"]}" data-track-index="{20+i}" data-volume="{v}"></audio>')

# ---------- корень ----------
def pw(s, fx, fy, cx=None, cy=None):
    cx = fx if cx is None else cx; cy = fy if cy is None else cy
    return f"{{scale:{s},x:{cx - s*fx:.1f},y:{cy - s*fy:.1f}}}"

POL = "inset(660px 250px 660px 250px round 6px)"
PIP = "inset(250px 80px 940px 590px round 28px)"
FULL = "inset(0px 0px 0px 0px round 0px)"
root_js = [
    "tl.set('#pw',{transformOrigin:'0px 0px',scale:1,x:0,y:0},0);",
    f"tl.set('#pclip',{{clipPath:'{FULL}'}},0);",
    # тревоги: тёмный фон + полароид
    f"tl.fromTo('#gd',{{clipPath:'inset(0% 0% 100% 0%)'}},{{clipPath:'inset(0% 0% 0% 0%)',duration:0.45,ease:'power2.inOut'}},{T_W0});",
    f"tl.to('#pclip',{{clipPath:'{POL}',duration:0.55,ease:'power3.inOut'}},{T_W0});",
    f"tl.to('#pw',{{...{pw(0.8, 480, 670, 540, 960)},duration:0.55,ease:'power3.inOut'}},{T_W0});",
    f"tl.fromTo('#pol',{{opacity:0,scale:1.25}},{{opacity:1,scale:1,duration:0.55,ease:'power3.inOut'}},{T_W0});",
    f"tl.to('#pclip',{{clipPath:'{FULL}',duration:0.6,ease:'power3.inOut'}},{T_W1-0.3:.3f});",
    f"tl.to('#pw',{{scale:1,x:0,y:0,duration:0.6,ease:'power3.inOut'}},{T_W1-0.3:.3f});",
    f"tl.to('#pol',{{opacity:0,scale:1.4,duration:0.35,ease:'power3.in'}},{T_W1-0.3:.3f});",
    f"tl.to('#gd',{{clipPath:'inset(100% 0% 0% 0%)',duration:0.4,ease:'power2.inOut'}},{T_W1+0.3:.3f});",
    # маршрут: жёлтый мир + окно справа
    f"tl.fromTo('#gy',{{clipPath:'inset(100% 0% 0% 0%)'}},{{clipPath:'inset(0% 0% 0% 0%)',duration:0.3,ease:'power2.out'}},{T_R0-0.08});",
    f"tl.to('#pclip',{{clipPath:'{PIP}',duration:0.6,ease:'power3.inOut'}},{T_R0+0.1});",
    f"tl.to('#pw',{{...{pw(0.66, 470, 690, 795, 575)},duration:0.6,ease:'power3.inOut'}},{T_R0+0.1});",
    f"tl.to('#pclip',{{clipPath:'{FULL}',duration:0.55,ease:'power3.inOut'}},{T_R1-0.12});",
    f"tl.to('#pw',{{scale:1,x:0,y:0,duration:0.55,ease:'power3.inOut'}},{T_R1-0.12});",
    f"tl.to('#gy',{{clipPath:'inset(0% 0% 100% 0%)',duration:0.45,ease:'power2.inOut'}},{T_R1+0.15});",
]
for i, (bid, a, b, ext, kb) in enumerate(BR):
    root_js.append(f"tl.fromTo('#w{bid}',{{clipPath:'inset(0% 100% 0% 0%)'}},{{clipPath:'inset(0% 0% 0% 0%)',duration:0.32,ease:'power3.inOut'}},{a:.3f});")
    if kb:
        root_js.append(f"tl.fromTo('#w{bid}',{{scale:1.06}},{{scale:1.0,duration:{b-a+ext:.2f},ease:'none'}},{a:.3f});")
br_html = "\n".join(
    f'      <div id="w{bid}" class="full" style="z-index:{3+i}"><video id="{bid}" class="clip full" src="assets/{bid}.mp4" data-start="{a:.3f}" data-duration="{b-a+ext:.3f}" data-track-index="{11+i%2}" muted playsinline></video></div>'
    for i, (bid, a, b, ext, kb) in enumerate(BR))
root_body = f"""      <div id="gd" class="full" style="background:#161514;z-index:0"></div>
      <div id="gy" class="full" style="background:#FDDC27;z-index:0"></div>
      <div id="pol" class="abs" style="left:226px;top:636px;width:628px;height:688px;background:#fff;border-radius:8px;box-shadow:0 24px 60px rgba(0,0,0,.55);z-index:1;opacity:0"></div>
      <div id="pclip" class="full" style="z-index:2">
        <div id="pw" class="full">
          <video id="plate" class="clip full" src="assets/plate.mp4" data-start="0" data-duration="{VD}" data-track-index="1" muted playsinline></video>
        </div>
      </div>
{br_html}
      <audio id="voice" class="clip" src="assets/voice.wav" data-start="0" data-duration="{VD}" data-track-index="2" data-volume="1"></audio>
{chr(10).join(sfx_html)}
{host('b-hook', 0, round(SEG['hook2'], 2), 10, 3)}
{host('b-note', SEG['hook2'], round(SEG['know'] - SEG['hook2'], 2), 11, 4)}
{host('b-worry', T_W0, round(T_W1 - T_W0 + 0.6, 2), 12, 5)}
{host('b-life', T_L, round(SEG['brand'] - T_L, 2), 13, 6)}
{host('b-brand', SEG['brand'], round(T_R0 - SEG['brand'] + 0.3, 2), 14, 7)}
{host('b-route', T_R0, round(T_R1 - T_R0 + 0.1, 2), 15, 8)}
{host('b-cta', T_C, round(END0 - T_C + 0.6, 2), 16, 9)}
{host('b-end', END0, round(DUR - END0, 2), 40, 10)}
{host('b-captions', 0, DUR, 30, 13, 'captions')}"""
write(os.path.join(P, "index.html"), index_html(DUR, root_body, "\n      ".join(root_js)))
print("B:", DUR, "s;", len(groups), "групп субтитров")
