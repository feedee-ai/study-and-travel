# v2conf.py — тайминги ролика 2 «Мрія → реальність»
def conf(E, wt, seg):
    DUR = 46.6
    T = dict(s1=seg[1], s2=seg[2], s3=seg[3], s4=seg[4], voiceEnd=E["dur"],
             lab=0.06, tiles=[wt("європейський"), wt("легально"), wt("подорожувати"), wt("будувати")],
             dost=wt("доступне,"), zero=wt("безкоштовне."), lang=wt("Мова"), alone=wt("дитина", 12), ukr=wt("українців,"),
             cur=wt("куратор"), real=wt("реальністю,"), path=wt("правильно"),
             steps=[wt("вибору", 27), wt("спеціальності", 28.5), wt("супроводження"), wt("вивченням"), wt("підготовкою"), wt("будемо")],
             q=seg[4] + 0.02, form=wt("Залишайте"), type1=wt("заявку") + 0.2, tap=wt("консультацію", 42), end0=wt("за", 43.5) - 0.3)
    T["avat"] = [T["alone"] + 0.12 * k for k in range(6)]
    extra = dict(music="m726", moff=0.0,
                 whoosh=[T["s1"], T["s2"], T["s3"], T["s4"]],
                 pops=T["tiles"] + [T["dost"], T["lang"], T["alone"], T["ukr"], T["cur"], T["path"], T["q"], T["form"]] + T["steps"],
                 sparks=[T["zero"], T["steps"][-1], T["tap"] + 0.2], big=T["end0"] + 0.1)
    ZOOM = [(0, 1.18, 1.0, seg[1], .49, .45), (seg[1], 1.0, 1.04, T["alone"] - seg[1], .47, .44),
            (T["alone"], 1.2, 1.24, T["cur"] - T["alone"], .47, .33), (T["cur"], 1.06, 1.1, seg[2] - T["cur"], .47, .40),
            (seg[2], 1.22, 1.28, seg[3] - seg[2], .48, .36), (seg[3], 1.08, 1.12, seg[4] - seg[3], .51, .48),
            (seg[4], 1.0, 1.06, DUR - seg[4], .46, .45)]
    HIDE = [(seg[3] - 0.05, seg[4] - 0.05), (T["form"] - 0.05, 99)]
    cols = ["#BFD9F2", "#F6C9A8", "#BDE6CF", "#D7C8F2", "#FFE27A", "#E3E3E3"]
    pos = [(0, 70), (135, 0), (270, 90), (405, 10), (540, 80), (675, 0)]
    av = "".join(f'<div class="av" style="left:{x}px; top:{y}px; background:{c}"><svg viewBox="0 0 134 134"><circle cx="67" cy="54" r="24" fill="#fff"/>'
                 f'<path d="M22 134 c0 -32 20 -46 45 -46 s45 14 45 46 Z" fill="#fff"/></svg></div>' for (x, y), c in zip(pos, cols))
    return DUR, T, extra, ZOOM, HIDE, " capB", {"__AVATARS__": av}
