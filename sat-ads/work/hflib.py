# Общие куски для генераторов композиций HyperFrames (Study & Travel)
import json, os, shutil, html

W, H = 1080, 1920
WORK = os.path.dirname(os.path.abspath(__file__))
SFX_DIR = "/root/.claude/skills/media-use/audio/assets/sfx"

FONTS = """
@font-face{font-family:'MontUA';src:url('assets/fonts/Montserrat-cyrillic.woff2') format('woff2');font-weight:100 900;unicode-range:U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116;}
@font-face{font-family:'MontUA';src:url('assets/fonts/Montserrat-cyrillic-ext.woff2') format('woff2');font-weight:100 900;unicode-range:U+0460-052F,U+1C80-1C8A,U+20B4,U+2DE0-2DFF,U+A640-A69F,U+FE2E-FE2F;}
@font-face{font-family:'MontUA';src:url('assets/fonts/Montserrat-latin.woff2') format('woff2');font-weight:100 900;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD;}
@font-face{font-family:'MontUA';src:url('assets/fonts/Montserrat-latin-ext.woff2') format('woff2');font-weight:100 900;unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF;}
@font-face{font-family:'HandUA';src:url('assets/fonts/Caveat-cyrillic.woff2') format('woff2');font-weight:700;unicode-range:U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116;}
@font-face{font-family:'HandUA';src:url('assets/fonts/Caveat-latin.woff2') format('woff2');font-weight:700;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2212;}
"""

BRAND = """
:root{--y:#FDDC27;--y2:#F2B705;--k:#111111;--w:#FFFFFF;--r:#E5302B;--g:#1B1A18;}
.f{font-family:'MontUA',Montserrat,sans-serif;}
.hand{font-family:'HandUA',cursive;font-weight:700;}
.abs{position:absolute;}
.row{position:absolute;left:0;width:1080px;display:flex;justify-content:center;}
.tape{display:inline-block;font-family:'MontUA',sans-serif;font-weight:900;line-height:1.02;padding:14px 26px 18px;border-radius:14px;white-space:nowrap;}
.tk{background:var(--k);color:var(--w);}
.ty{background:var(--y);color:var(--k);}
.tw{background:var(--w);color:var(--k);}
.sh{box-shadow:0 14px 34px rgba(0,0,0,.28);}
"""

# логотип «Study & Travel / EDUCATION ABROAD», пересобран текстом по растру с сайта
def logo(id_, color="#111", scale=1.0):
    plane = ("<svg class='abs' style='left:{x}px;top:{y}px' width='{s}' height='{s}' viewBox='0 0 24 24'>"
             "<path fill='{c}' d='M21 15.5v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V8.5l-8 5v2l8-2.5V18l-2 1.5V21l3.5-1 3.5 1v-1.5L13 18v-5z'"
             " transform='rotate(45 12 12)'/></svg>")
    s = scale
    return (f"<div id='{id_}' class='abs f' style='width:{int(560*s)}px;height:{int(150*s)}px;color:{color}'>"
            f"<div class='abs' style='left:0;top:0;font-weight:800;font-size:{int(92*s)}px;letter-spacing:-0.02em;line-height:1;white-space:nowrap'>"
            f"Study<span style='font-weight:600'>&amp;</span>&#8202;Travel</div>"
            + plane.format(x=int(264*s), y=int(-6*s), s=int(34*s), c=color) +
            f"<div class='abs' style='left:{int(4*s)}px;top:{int(104*s)}px;font-weight:600;font-size:{max(28,int(25*s))}px;letter-spacing:0.5em;white-space:nowrap'>EDUCATION ABROAD</div>"
            "</div>")

CHECK_SVG = ("<svg width='{s}' height='{s}' viewBox='0 0 48 48'><circle cx='24' cy='24' r='24' fill='{bg}'/>"
             "<path class='ck' d='M13 25 l7 7 l15 -16' fill='none' stroke='{fg}' stroke-width='6' stroke-linecap='round' stroke-linejoin='round'/></svg>")

ARROW_DOWN = ("<svg width='{w}' height='{h}' viewBox='0 0 60 120'><path class='ar' d='M30 4 C 22 40, 40 70, 30 108' fill='none' stroke='{c}'"
              " stroke-width='7' stroke-linecap='round'/><path class='ah' d='M12 90 L30 112 L48 90' fill='none' stroke='{c}' stroke-width='7'"
              " stroke-linecap='round' stroke-linejoin='round'/></svg>")


def esc(s):
    return html.escape(s, quote=False)


def scene(cid, body, js, css="", dur=None):
    """Файл сцены: всё внутри <template>, корень #root прозрачный."""
    return f"""<template>
  <style>
{FONTS}
{BRAND}
    #root{{position:absolute;inset:0;overflow:visible;}}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


def captions_scene(cid, groups, ycenter=1170, css_extra=""):
    """groups: [{'t0','t1','words':[{'w','t','e','hl'?}]}]; активное слово — жёлтая плашка.
    Всё время — от начала композиции (хост с data-start=0)."""
    body, js = [], []
    for gi, g in enumerate(groups):
        gid = f"cg{gi}"
        spans = []
        for wi, w in enumerate(g["words"]):
            spans.append(f"<span id='{gid}w{wi}' class='cw'>{esc(w['w'])}</span>")
        body.append(f"    <div id='{gid}' class='cgrp f' style='top:{ycenter-90}px'><div class='cin'>{' '.join(spans)}</div></div>")
        t0, t1 = g["t0"], g["t1"]
        js.append(f"tl.fromTo('#{gid}',{{opacity:0,scale:0.9,y:14}},{{opacity:1,scale:1,y:0,duration:0.16,ease:'back.out(2)'}},{t0:.3f});")
        for wi, w in enumerate(g["words"]):
            on = max(t0, w["t"] - 0.02)
            js.append(f"tl.set('#{gid}w{wi}',{{backgroundColor:'#FDDC27',color:'#111','--sc':'rgba(17,17,17,0)'}},{on:.3f});")
            if wi < len(g["words"]) - 1:
                off = g["words"][wi + 1]["t"] - 0.02
                js.append(f"tl.set('#{gid}w{wi}',{{backgroundColor:'rgba(253,220,39,0)',color:'#fff','--sc':'rgba(17,17,17,1)'}},{off:.3f});")
        js.append(f"tl.to('#{gid}',{{opacity:0,duration:0.1,ease:'power2.in'}},{max(t1-0.1, t0+0.17):.3f});")
        t1 = max(t1, t0 + 0.27)
        js.append(f"tl.set('#{gid}',{{opacity:0,visibility:'hidden'}},{t1:.3f});")
    css = """
    .cgrp{position:absolute;left:0;width:1080px;height:180px;display:flex;align-items:center;justify-content:center;opacity:0;}
    .cin{max-width:900px;text-align:center;line-height:1.28;}
    .cw{display:inline-block;font-weight:800;font-size:62px;color:#fff;padding:2px 12px 6px;border-radius:12px;margin:0 -4px;
        --sc:rgba(17,17,17,1);-webkit-text-stroke:10px var(--sc);paint-order:stroke fill;background-color:rgba(253,220,39,0);}
""" + css_extra
    return scene(cid, "\n".join(body), "\n    ".join(js), css)


def build_groups(words, hide=(), maxw=3, maxc=22, gap=0.28, fixes=None, tail=0.25, seg_t0=None):
    """Слова -> группы субтитров. hide: [(a,b)] — интервалы без субтитров (по началу слова)."""
    fixes = fixes or {}
    ws = []
    for i, w in enumerate(words):
        txt = fixes.get(i, w["w"])
        if txt is None:
            continue
        if any(a <= w["t"] < b for a, b in hide):
            continue
        ws.append({"w": txt, "t": w["t"], "e": w["e"], "seg": w["seg"]})
    groups, cur = [], []
    def flush():
        if cur:
            groups.append(cur[:])
            cur.clear()
    for i, w in enumerate(ws):
        if cur:
            prev = cur[-1]
            chars = sum(len(x["w"]) + 1 for x in cur) + len(w["w"])
            if (len(cur) >= maxw or chars > maxc or w["t"] - prev["e"] > gap or w["seg"] != prev["seg"]
                    or prev["w"][-1] in ".,?!:"):
                flush()
        cur.append(w)
    flush()
    out = []
    for gi, g in enumerate(groups):
        t0 = g[0]["t"] - 0.06
        if seg_t0 is not None:          # не раньше склейки, на которой звучит первое слово
            t0 = max(t0, seg_t0[g[0]["seg"]] + 0.01)
        t1 = g[-1]["e"] + 0.05
        if gi + 1 < len(groups):
            t1 = min(t1 + tail, groups[gi + 1][0]["t"] - 0.08)
        for ha, hb in hide:             # группа гаснет до начала скрытого участка (B-roll, графика)
            if ha > g[0]["t"]:
                t1 = min(t1, ha - 0.02)
        out.append({"t0": round(max(0.02, t0), 3), "t1": round(t1, 3), "words": g})
    return out


def copy_assets(proj, extra=()):
    a = os.path.join(proj, "assets")
    for d in ("fonts", "vendor", "sfx", "img"):
        os.makedirs(os.path.join(a, d), exist_ok=True)
    for f in os.listdir(os.path.join(WORK, "shared/fonts")):
        shutil.copy(os.path.join(WORK, "shared/fonts", f), os.path.join(a, "fonts", f))
    shutil.copy(os.path.join(WORK, "shared/vendor/gsap.min.js"), os.path.join(a, "vendor/gsap.min.js"))
    for src, dst in extra:
        shutil.copy(src, os.path.join(a, dst))


def sfx(name):
    return os.path.join(SFX_DIR, name + ".mp3") if os.path.exists(os.path.join(SFX_DIR, name + ".mp3")) else os.path.join(SFX_DIR, name + ".wav")


def index_html(dur, root_body, root_js, css=""):
    return f"""<!doctype html>
<html lang="uk" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{FONTS}
{BRAND}
      *{{margin:0;padding:0;box-sizing:border-box;}}
      html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:#111;}}
      #root{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:#111;}}
      .full{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;}}
      video.full{{object-fit:cover;}}
{css}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="{W}" data-height="{H}">
{root_body}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{root_js}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""


def host(cid, start, dur, z, track, kind="graphics"):
    return (f"      <div id=\"{cid}\" data-composition-id=\"{cid}\" data-composition-src=\"compositions/{cid}.html\" "
            f"data-start=\"{start}\" data-duration=\"{dur}\" data-track-index=\"{track}\" data-track-kind=\"{kind}\" "
            f"data-width=\"{W}\" data-height=\"{H}\" style=\"position:absolute;inset:0;z-index:{z}\"></div>")


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(text)
