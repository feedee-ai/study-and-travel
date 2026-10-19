# Передача: пиксель Meta + Conversions API на WordPress

## Проблема
Заявки с сайта приходят в Telegram, а в Facebook часть из них не видна, без закономерности.
Lead зависел от клика «ОК»/страницы «Спасибо», с сервера ничего не шло («Conversions API · Только в браузере»).

## Решения (согласованы с пользователем)
- Один пиксель на все лендинги: **Study and Travel 2024, ID 1146010926423221**.
- Заявка → `Lead`. Регистрация на вебинар (`/webinar*`, `/studying-in-slovakia/`) → `CompleteRegistration`.
- Остальные пиксели на страницах (842000908287986, 1557571255679048, 1730677428340549) **не трогаем**:
  браузерное событие уходит и в них (fbq('track') бьёт во все пиксели страницы). Снять — только по «да».
- Клик в Telegram лидом не считается, Contact не нужен.

## Как устроен сайт (аудит 19.10.2026)
- Тема `main-template`, формы свои: кнопка `.send-ajax` → `jQuery.ajax` в мейлер темы
  (`mailer/form.php` на WP-страницах — пустой ответ = успех; `mailer/slovakia.php` на лендингах Словакии),
  мейлер шлёт в Telegram, страница показывает модалку. CF7/Elementor/WPForms-форм в бою нет.
- `/studying-in-slovakia/` и `/consultation-studying-in-slovakia/` — **статические папки вне WordPress**
  (свои `js/script.js`, jQuery 3.7.1). Пиксели там вшиты в HTML:
  studying — только 1557571255679048; consultation — 1146010926423221 + 1730677428340549.
- WP-страницы: в шапке темы вшиты 1146010926423221 + 842000908287986, GTM-WPTS72 с consent mode.
  Lead в HTML нет — старый Lead, если есть, сидит в GTM (googletagmanager.com закрыт сетью среды, не проверено).
- Cloudflare перед сайтом (IP из `CF-Connecting-IP`, страна из `CF-IPCountry`).

## Что сделано
- Плагин Code Snippets включён, сниппет **id 5 «Study and Travel — Meta Pixel + CAPI»** активен
  (исходник — `tracking/st-meta-tracking.php`, токен подставлен при заливке).
- Браузер: на успешный ответ мейлера → `fbq('track', Lead|CompleteRegistration, {...}, {eventID})` +
  `sendBeacon` на `POST /wp-json/st/v1/lead` (свой домен). Сервер → CAPI с тем же event_id:
  ph/em/fn/ln/country/external_id (sha256), IP, UA, fbc/fbp (свои cookie, если fbevents заблокирован), UTM, referrer.
  Защита эндпоинта: Origin/Referer своего домена, 20 заявок/час на IP, event_id один раз.
- WP-страницы получают скрипт в футере автоматически. Лендинги Словакии (движок CL9/F3, хостинг Hostinger,
  `public_html/<папка>/main.php` — шаблон страницы) — 19.10.2026 перед `</body>` в `main.php` обеих папок вставлен
  `<script src="https://study-and-travel.net/?st-track-js=1" defer></script>`; бэкап рядом: `main.php.bak-st-*`.
  Вставка сделана одноразовым сниппетом Code Snippets (удалён сразу после запуска).
- Проверено в Chromium на обоих лендингах (мейлер, beacon и facebook.com/tr перехвачены, наружу ничего не ушло):
  модалка показана, событие ушло ДО клика «ОК»; studying → CompleteRegistration + Lead, consultation → Lead;
  у браузерного события и beacon один event_id; beacon несёт телефон, email, имя, fbc (из fbclid), fbp, UTM.
  fbevents.js в тесте был заблокирован сетью — beacon всё равно ушёл (сценарий адблока).
- Токен проверен: `events_received: 1`. ⚠ Проверочное событие ушло с неактивным test-кодом и засчиталось
  в бою: **1 тестовый Lead (test@example.com) в пикселе 1146010926423221, 19.10.2026 ~18:40 UTC**.
- На регистрациях (studying-in-slovakia, /webinar) вместе с CompleteRegistration уходит и Lead (тот же event_id).
- Для `/studying-in-slovakia/` сервер шлёт CAPI ещё и в пиксель лендинга 1557571255679048 (токен к нему имеет доступ).
- Лог CAPI: `GET /wp-json/st/v1/capi-log` (только админ).

## Осталось
1. GTM-WPTS72: найти и поставить на паузу старый Meta Lead (клик «ОК» / «Спасибо»), иначе двойной счёт на WP-страницах.
2. Тест: Events Manager → Test Events, код в `ST_TEST_CODE` (сниппет 5), заявка на каждом лендинге →
   браузер + сервер «дедуплицировано», запись в capi-log с кодом 200, сообщение в Telegram. Потом код обнулить.
3. Events Manager → настройки пикселя: включить «Автоматическое расширенное сопоставление» (все поля).
4. Желательно: event_id и UTM в сообщение Telegram (правка мейлеров темы — нужен доступ к файлам).
