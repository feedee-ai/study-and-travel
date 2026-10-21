# 2BRO.LAB — ролик «Сайт за $40/міс»

9:16, 1080×1920, 30 к/с, 52 с. Озвучка v5 (ElevenLabs, Andriy Tkachenko), музыка Mixkit «Minimal Emotion», SFX Mixkit
(Mixkit Free License — коммерческое использование, включая рекламу, без указания автора).

## Сборка с нуля
```bash
cd 2bro-ads
ln -sfn /opt/node-tools/node_modules node_modules          # playwright + http-server для съёмки кейсов
node tools/capture.mjs work/captures                       # кейсы из site/ клонов в /home/user
mkdir -p hf/assets/img && for n in darya fedoristov confiteria romantic sirenita katya sylchuk alifannk; do
  ffmpeg -y -i work/captures/$n-m.png -q:v 3 hf/assets/img/$n.jpg; done
python3 tools/voiceover.py vo/v5 1.15                      # озвучка по SCRIPT.md (если менялся текст)
mkdir -p work/music hf/assets/audio && curl -o work/music/160.mp3 https://assets.mixkit.co/music/160/160.mp3
# SFX: hf/assets/sfx/*.mp3 — https://assets.mixkit.co/active_storage/sfx/<id>/<id>-preview.mp3 (id — в комментарии tools/mix.py)
cp ../hf-demo/assets/vendor/gsap.min.js hf/assets/vendor/
python3 tools/mix.py                                       # голос + музыка + SFX → hf/assets/audio/mix.mp3
cd hf && npx hyperframes check && npx hyperframes render --quality high --output ../out/2bro-40.mp4
```

## Как устроено
- `hf/index.html` — вся композиция, тайминги сцен и слов взяты из пословной разметки озвучки (Scribe).
- Сцены: 1 хук $40/міс · 2 «як зазвичай» (без цвета, музыка «за стеной») · 3 дроп на «ДваБро», «навпаки», демо → выбор $0 / $40
  · 4 підтримка (хостинг, аналітика, заявки → Telegram / Таблиця / CRM), чат «Готово» · 5 разово $250 · 6 заявка, мозаика кейсов, финальная карточка.
- Бренд: `2brolabs/docs/brand.md` — фон `#f9f9f7`, чернила `#0e1013`, бирюза только заливкой, Onest 500 + Geist Mono, стекло только над изображением.
- Скриншоты клиентских сайтов, аудио и рендеры в git не идут (репо публичный).
