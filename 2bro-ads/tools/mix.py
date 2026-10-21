# Звук ролика одним файлом: голос + музыка + SFX по таймкодам → hf/assets/audio/mix.mp3 (и mix.wav для финальной склейки).
# Музыка: Mixkit «Lo-Fi 02» (764) — спокойная, без дропов; вступление баса (23.4 с трека) встаёт на «ДваБро».
# Голос: из vo/v5-all.mp3 вырезаны две паузы (перед «як» и перед «у Telegram»), заглушён щелчок перед «Залиште».
# Все таймкоды ниже — по исходной дорожке; R() переводит их в смонтированное время (те же CUTS в hf/index.html).
# Использование: python3 tools/mix.py
import os, subprocess

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
HF = os.path.join(ROOT, 'hf', 'assets')
CUTS = [(9.44, 0.38), (33.78, 0.32)]   # (начало в исходной дорожке, длина)
MUTE = (44.46, 44.62)                  # хвост-щелчок в конце фразы про $250
DUR = 52.0 - sum(l for _, l in CUTS)


def R(t):
    d = 0.0
    for a, l in CUTS:
        d += l if t >= a + l else max(0.0, t - a)
    return t - d


MUSIC = os.path.join(ROOT, 'work', 'music', '764.mp3')
MUSIC_OFF = 23.4 - R(18.40)
VO_END = R(48.9)

# id на Mixkit: sweep 166, whoosh 1490, lightpop 3005, msgpop 2354, drypop 2356, check 1120, tick 2568,
# mouse 2997, confirm 2867, phonetype 1393, hardpop 2364, select 1109, swoosh2 1471
# (время, файл в hf/assets/sfx, громкость)
SFX = [
    (0.00, 'swoosh2', 0.35),
    (0.40, 'tick', 0.30), (0.58, 'tick', 0.30), (0.82, 'tick', 0.30),
    (1.58, 'hardpop', 0.55), (2.56, 'lightpop', 0.45),
    (3.44, 'drypop', 0.45), (4.82, 'drypop', 0.45), (6.32, 'check', 0.55),
    (8.38, 'sweep', 0.45),
    (10.32, 'lightpop', 0.30), (11.74, 'hardpop', 0.55), (12.36, 'lightpop', 0.30),
    (13.98, 'sweep', 0.35), (14.60, 'hardpop', 0.55),
    (15.72, 'msgpop', 0.45), (16.62, 'msgpop', 0.45), (17.36, 'msgpop', 0.45),
    (17.95, 'whoosh', 0.50), (18.38, 'lightpop', 0.55),
    (19.44, 'swoosh2', 0.35), (20.38, 'sweep', 0.35),
    (20.96, 'check', 0.45), (21.78, 'drypop', 0.35),
    (22.86, 'drypop', 0.40), (25.34, 'drypop', 0.40), (26.30, 'mouse', 0.70), (28.16, 'confirm', 0.50),
    (29.00, 'sweep', 0.40),
    (30.80, 'check', 0.45), (32.06, 'check', 0.45), (33.12, 'check', 0.45),
    (34.22, 'msgpop', 0.40), (35.14, 'msgpop', 0.40), (36.30, 'msgpop', 0.40),
    (36.95, 'sweep', 0.40), (37.40, 'msgpop', 0.45), (37.95, 'phonetype', 0.30), (38.70, 'confirm', 0.50), (39.15, 'lightpop', 0.30),
    (39.85, 'sweep', 0.40), (41.24, 'select', 0.55), (42.86, 'hardpop', 0.45), (43.70, 'lightpop', 0.35),
    (44.72, 'whoosh', 0.40), (45.20, 'phonetype', 0.22), (46.30, 'mouse', 0.70), (46.75, 'confirm', 0.45), (47.90, 'lightpop', 0.40),
    (48.95, 'sweep', 0.40), (49.15, 'confirm', 0.40),
]

inputs = ['-i', os.path.join(ROOT, 'vo', 'v5-all.mp3'), '-i', MUSIC]
fil = []
# голос: заглушить щелчок, нарезать куски между вырезами, склеить с короткими фейдами (без щелчков на стыках)
keep, t0 = [], 0.0
for a_, l in CUTS:
    keep.append((t0, a_)); t0 = a_ + l
keep.append((t0, 52.0))
fil.append(f"[0:a]volume=0:enable='between(t,{MUTE[0]},{MUTE[1]})',asplit={len(keep)}" + ''.join(f'[k{i}]' for i in range(len(keep))))
for i, (x, y) in enumerate(keep):
    fil.append(f"[k{i}]atrim=start={x}:end={y},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={y-x-0.012:.3f}:d=0.012[v{i}]")
fil.append(''.join(f'[v{i}]' for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1,highpass=f=80,"
           f"acompressor=threshold=0.12:ratio=2.5:attack=8:release=120:makeup=1.6,apad=whole_dur={DUR},asplit[vo][vsc]")
# музыка: ровный фон под голосом, после последней фразы чуть громче, хвост гаснет
mvol = f"if(lt(t,{VO_END}),0.30,0.30+min(1,(t-{VO_END})/0.8)*0.30)"
fil.append(f"[1:a]atrim=start={MUSIC_OFF}:duration={DUR},asetpts=PTS-STARTPTS,volume='{mvol}':eval=frame,"
           f"afade=t=in:d=0.4,afade=t=out:st={DUR-2.2}:d=2.2[mus]")
fil.append("[mus][vsc]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=400[mduck]")
labels = ['[vo]', '[mduck]']
for k, (t, f, g) in enumerate(SFX):
    inputs += ['-i', os.path.join(HF, 'sfx', f + '.mp3')]
    idx = k + 2
    trim = ',atrim=duration=0.9' if f == 'phonetype' else ''
    fil.append(f"[{idx}:a]aformat=channel_layouts=stereo{trim},volume={g * 0.85:.3f},adelay={int(R(t)*1000)}:all=1[s{k}]")
    labels.append(f'[s{k}]')
fil.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=duration={DUR},"
           "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[out]")

wav = os.path.join(HF, 'audio', 'mix.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(fil), '-map', '[out]', '-ac', '2', wav], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', wav, '-b:a', '192k', os.path.join(HF, 'audio', 'mix.mp3')], check=True)
print('ok', wav)
