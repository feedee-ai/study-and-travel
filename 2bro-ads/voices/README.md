# Пробные голоса — фраза сцены 1

Модель `eleven_multilingual_v2`, `mp3_44100_128`, настройки: stability 0.45, similarity 0.8, style 0.3, speaker boost.
Голоса из библиотеки ElevenLabs (носители украинского), добавлены в аккаунт. Проверено распознаванием (Scribe): текст прочитан без ошибок.

| Файл | Голос | voice_id | Характер | Длина |
|---|---|---|---|---|
| 1-andriy-ad.mp3 | Andriy Tkachenko — Advertising Narrator | `hWHihsTve3RbzG4PHDBQ` | мужской, рекламный диктор, размеренный | 11.3 с |
| 2-anton-lively.mp3 | Anton — Clear, Lively and Smooth | `4nLP0u2B3yI0lyzATFnN` | мужской, живой, «соцсетевой» | 7.9 с |
| 3-anna-bright.mp3 | Anna Stepanenko — Bright and Distinct | `2o2uQnlGaNuV3ObRpxXt` | женский, яркий, чёткий | 8.4 с |

Фраза длиннее слота 0–5 с в сценарии при любом голосе: длительности сцен берём из озвучки (шаг 2), темп можно поднять `speed` до 1.1–1.15.
