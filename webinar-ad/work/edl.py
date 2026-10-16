# EDL: какие куски исходника оставляем (паузы вырезаны) → тайминги слов в выходном времени.
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
# (src_in, src_out) — речь по silencedetect -35 dB, запас 0.06 до / 0.08–0.10 после
KEEP = [
    (0.10, 5.04),   # П'ять речей … після школи
    (5.82, 7.18),   # Як обрати університет?
    (7.65, 9.03),   # Які документи підготувати?
    (9.22, 12.33),  # Скільки коштуватиме проживання та де житиме студент?
    (12.52, 14.02), # Скільки він може заробляти?
    (14.16, 16.11), # Та ще багато цікавої інформації.
    (17.21, 19.96), # Приходьте на безкоштовний вебінар, де ми розберемо
    (20.31, 22.25), # весь шлях вступу до Словаччини.
    (22.44, 23.53), # Від перших кроків
    (23.93, 25.95), # до студентського життя після переїзду.
    (26.33, 29.20), # Ми вже супроводили понад 1200 студентів.
    (29.57, 32.04), # Тому знаємо, скільки запитань виникає у батьків.
    (32.59, 35.92), # Ви також можете поставити свої запитання і отримати відповідь.
    (37.08, 42.60), # Бронюйте місце … перед вступом до Словаччини.
]
def segs():
    t = 0; out = []
    for a, b in KEEP:
        out.append(dict(src_in=a, src_out=b, out_in=round(t, 3), out_out=round(t + b - a, 3))); t += b - a
    return out
def to_out(ts):
    s = min(segs(), key=lambda s: 0 if s['src_in'] <= ts <= s['src_out'] else min(abs(ts - s['src_in']), abs(ts - s['src_out'])))
    return round(s['out_in'] + min(max(ts - s['src_in'], 0), s['src_out'] - s['src_in']), 3)
if __name__ == '__main__':
    S = segs(); json.dump(S, open(f'{HERE}/segments.json', 'w'), indent=1)
    W = json.load(open(f'{HERE}/words_raw.json'))
    # начало ролика GigaAM не распознал — расставляем по огибающей (речь 0.15–2.12)
    manual = {0: (0.16, 0.42), 1: (0.44, 0.74), 2: (0.78, 0.94), 3: (0.96, 1.20), 5: (1.62, 1.98), 6: (2.04, 2.12), 7: (2.14, 2.42)}
    for i, (s, e) in manual.items(): W[i]['s'], W[i]['e'] = s, e
    # дыры внутри фраз — интерполяция по соседям
    for i, w in enumerate(W):
        if w['s'] is None:
            p = max(j for j in range(i) if W[j]['s'] is not None); n = min(j for j in range(i + 1, len(W)) if W[j]['s'] is not None)
            gap = (W[n]['s'] - W[p]['e']); k = n - p
            w['s'] = W[p]['e'] + gap * (i - p) / k; w['e'] = w['s'] + gap / k * 0.8
    # GigaAM ставит метку чуть раньше — сдвиг +0.04
    out = []
    for w in W:
        out.append(dict(w=w['w'], s=to_out(w['s'] + 0.04), e=to_out(max(w['e'], w['s']) + 0.12)))
    json.dump(out, open(f'{HERE}/words.json', 'w'), ensure_ascii=False, indent=0)
    for s in S: print(s)
    print('total', S[-1]['out_out'])
    for o in out: print(o['s'], o['e'], o['w'])
