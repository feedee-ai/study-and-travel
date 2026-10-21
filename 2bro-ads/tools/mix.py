# Звук ролика одним файлом: голос + музыка + SFX по таймкодам → hf/assets/audio/mix.mp3 (и mix.wav для финальной склейки).
# Музыка: Mixkit «Minimal Emotion» (160), старт с 11.6 с — дроп трека (30.0 с) встаёт на «ДваБро» (18.4 с ролика).
# На «как обычно» (8.5–18.4) музыка звучит «за стеной» (lowpass) и раскрывается на дропе.
# Использование: python3 tools/mix.py
import os, subprocess

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
HF = os.path.join(ROOT, 'hf', 'assets')
DUR = 52.0
MUSIC, MUSIC_OFF = os.path.join(ROOT, 'work', 'music', '160.mp3'), 11.6
MUFFLE = (8.5, 18.4)
VO_END = 48.9

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
    (36.95, 'sweep', 0.40), (37.40, 'msgpop', 0.45), (37.95, 'phonetype', 0.30), (38.70, 'confirm', 0.50),
    (39.85, 'sweep', 0.40), (41.24, 'select', 0.55), (42.86, 'hardpop', 0.45), (43.70, 'lightpop', 0.35),
    (44.72, 'whoosh', 0.45), (46.00, 'mouse', 0.70), (47.90, 'lightpop', 0.45),
    (48.95, 'sweep', 0.40), (49.15, 'confirm', 0.40),
]

inputs = ['-i', os.path.join(ROOT, 'vo', 'v5-all.mp3'), '-i', MUSIC]
fil = []
a, b = MUFFLE
# громкость музыки: тише под голосом, громче после последней фразы, хвост гаснет
mvol = f"if(lt(t,{VO_END}),0.30,0.30+min(1,(t-{VO_END})/0.8)*0.35)"
fil.append(f"[1:a]atrim=start={MUSIC_OFF}:duration={DUR},asetpts=PTS-STARTPTS,asplit[ma][mb]")
fil.append(f"[ma]lowpass=f=500,lowpass=f=500,volume=1.7,volume='if(between(t,{a},{b}),min(1,(t-{a})/0.25),0)':eval=frame[mm]")
fil.append(f"[mb]volume='if(between(t,{a},{b}),max(0,1-(t-{a})/0.25),1)':eval=frame[mo]")
fil.append(f"[mm][mo]amix=inputs=2:normalize=0,volume='{mvol}':eval=frame,afade=t=in:d=0.3,afade=t=out:st={DUR-2.2}:d=2.2[mus]")
# голос немного подсушить и уплотнить
fil.append("[0:a]highpass=f=80,acompressor=threshold=0.12:ratio=2.5:attack=8:release=120:makeup=1.6,apad=whole_dur=52,asplit[vo][vsc]")
fil.append("[mus][vsc]sidechaincompress=threshold=0.04:ratio=5:attack=15:release=350[mduck]")
labels = ['[vo]', '[mduck]']
for k, (t, f, g) in enumerate(SFX):
    inputs += ['-i', os.path.join(HF, 'sfx', f + '.mp3')]
    idx = k + 2
    trim = ',atrim=duration=0.9' if f == 'phonetype' else ''
    fil.append(f"[{idx}:a]aformat=channel_layouts=stereo{trim},volume={g},adelay={int(t*1000)}:all=1[s{k}]")
    labels.append(f'[s{k}]')
fil.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=duration={DUR},"
           "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[out]")

wav = os.path.join(HF, 'audio', 'mix.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(fil), '-map', '[out]', '-ac', '2', wav], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', wav, '-b:a', '192k', os.path.join(HF, 'audio', 'mix.mp3')], check=True)
print('ok', wav)
