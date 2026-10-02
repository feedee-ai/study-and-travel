# Передача: 4 рилса для hair-treatment, облачная сессия

Задача и все требования — в `hair-ads/HAIR-ADS-PROMPT.md`. Этот файл — только то, что нужно, чтобы выполнить его **в облачной сессии** вместо Windows.

## Поправки к брифу для облака
- Работаем в `hair-ads/` этого репозитория. `material/` → `hair-ads/material/`, `work/` → `hair-ads/work/`, `out/` → `hair-ads/out/`.
- Видео в git **не коммитить** (`.gitignore` уже отсекает `*.mp4`, `*.mov`). Коммитить можно только планы, json, скрипты, композиции, листы-превью (PNG до ~1 МБ).
- Пункт про Windows и кириллицу в путях не актуален, но латинские имена в `work/takes/` всё равно делаем.
- Готовые ролики отдать пользователю через `SendUserFile` (по одному файлу, `display: attach`) и сказать, где они лежат.
- Стек ставит SessionStart-хук репо. Проверь `npx hyperframes doctor` перед работой.

## Исходники: Google Drive, папка MATERIAL
Пользователь временно открыл папку по ссылке (Anyone with the link → Viewer). Фото не качать.
Копии с суффиксами `(1)`, `(2)`, `(3)` не качать — это байт-в-байт дубли.

| Имя для work/takes | Исходное имя (папка) | Drive file ID | Размер |
|---|---|---|---|
| root_a11e.mp4 | a11e4507ccbb4622876c0d2fc79e5373.mp4 (MATERIAL) | 162jcgIU_HaNnCZDdsoNfmx02JBSJR6ZS | 35,7 МБ |
| root_8e8d.mp4 | 8e8d5ed0305d4ffface8c8cc8a2bbafb.mp4 (MATERIAL) | 1NanNtK-z86ACNbBduUbLHPcg9AwKdC5O | 60,7 МБ |
| leda_2235.mov | IMG_2235.MOV (Леда) | 1KAJLrlRPwewpT0_LmK1TxiSL_j2I4yQI | 103,4 МБ |
| cam_2264.mov | IMG_2264.mov (Леда/З камери) | 14mE7t8xVHrMwmZU2hWrTjftLHHZtTQoZ | 22,8 МБ |
| cam_2265.mov | IMG_2265.mov (Леда/З камери) | 1uSsvJeUxTDmqbrNLQgoqRDfGw7qHMq09 | 15,2 МБ |
| cam_2266.mov | IMG_2266.mov (Леда/З камери) | 1guWsMvNAHa-8CL-9czQEKT_oGvi7eVNI | 33,3 МБ |
| cam_2275.mov | IMG_2275.MOV (Леда/З камери) | 1EnyeEWFxnzy1WCqgPeEfhwev3q0Ngc38 | 28,8 МБ |
| luda_3336.mov | IMG_3336.MOV (Люда) | 12bE6GwxG12se_KQ0KZLI44K8oKudjcum | 122,3 МБ |
| luda_3348.mov | IMG_3348.MOV (Люда) | 1i0nIvMzUbYTnONUlO7oNamcowLE9YDl7 | 87,4 МБ |

Скачивание (большие файлы требуют `confirm=t`):

```bash
mkdir -p hair-ads/material
dl() { curl -fL --retry 3 -o "hair-ads/material/$1" "https://drive.usercontent.google.com/download?id=$2&export=download&confirm=t"; }
dl root_a11e.mp4  162jcgIU_HaNnCZDdsoNfmx02JBSJR6ZS
dl root_8e8d.mp4  1NanNtK-z86ACNbBduUbLHPcg9AwKdC5O
dl leda_2235.mov  1KAJLrlRPwewpT0_LmK1TxiSL_j2I4yQI
dl cam_2264.mov   14mE7t8xVHrMwmZU2hWrTjftLHHZtTQoZ
dl cam_2265.mov   1uSsvJeUxTDmqbrNLQgoqRDfGw7qHMq09
dl cam_2266.mov   1guWsMvNAHa-8CL-9czQEKT_oGvi7eVNI
dl cam_2275.mov   1EnyeEWFxnzy1WCqgPeEfhwev3q0Ngc38
dl luda_3336.mov  12bE6GwxG12se_KQ0KZLI44K8oKudjcum
dl luda_3348.mov  1i0nIvMzUbYTnONUlO7oNamcowLE9YDl7
```

Проверка: размер каждого файла совпадает с таблицей, `ffprobe` читает длительность. Если пришёл HTML вместо видео — доступ по ссылке не открыт или хост не разрешён в сети окружения; скажи пользователю.

**Как только все 9 файлов скачаны и проверены — сразу скажи пользователю закрыть доступ по ссылке к папке MATERIAL.**
