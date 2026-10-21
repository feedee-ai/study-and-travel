# Озвучка по сценам из SCRIPT.md (строки «> ...» по порядку) одним голосом ElevenLabs.
# previous_text/next_text — чтобы интонация не обрывалась на стыках сцен.
# Использование: python3 tools/voiceover.py <out_dir> [speed] [script.md]
import json, os, subprocess, sys, urllib.request

VOICE = 'hWHihsTve3RbzG4PHDBQ'  # Andriy Tkachenko — Advertising Narrator (выбор заказчика 21.10)
MODEL = 'eleven_multilingual_v2'
# Латиницу модель читает по-английски или по буквам непредсказуемо — даём произношение явно.
SAY = {'Telegram': 'Телеграм', 'CRM': 'сі-ар-ем', '$250': 'двісті п’ятдесят доларів'}

out = sys.argv[1]
speed = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
os.makedirs(out, exist_ok=True)

src = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(__file__), '..', 'SCRIPT.md')
script = open(src, encoding='utf-8').read()
lines = [l[2:].strip() for l in script.splitlines() if l.startswith('> ')]
for k, v in SAY.items():
    lines = [l.replace(k, v) for l in lines]


def tts(i):
    body = {
        'text': lines[i],
        'model_id': MODEL,
        'previous_text': lines[i - 1] if i else None,
        'next_text': lines[i + 1] if i + 1 < len(lines) else None,
        'voice_settings': {'stability': 0.45, 'similarity_boost': 0.8, 'style': 0.3,
                           'use_speaker_boost': True, 'speed': speed},
    }
    req = urllib.request.Request(
        f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128',
        data=json.dumps(body).encode(), method='POST',
        headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as r:
        return r.read()


total = 0.0
for i in range(len(lines)):
    path = os.path.join(out, f'scene{i + 1}.mp3')
    open(path, 'wb').write(tts(i))
    dur = float(subprocess.check_output(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path]))
    total += dur
    print(f'scene{i + 1} {dur:5.2f}s  {lines[i][:60]}')
print(f'total {total:.2f}s, chars {sum(map(len, lines))}')
