#!/usr/bin/env python3
"""Файл массового импорта Meta Ads (UTF-16, табы — как экспорт кабинета) для 5 роликов R3.
python3 make_import.py PAGE_ID IG_ACCOUNT_ID  →  R3-import.csv
Всё создаётся на ПАУЗЕ: после импорта проверь превью и аудитории, затем включи."""
import sys, pathlib
here = pathlib.Path(__file__).parent
page, ig = (sys.argv[1:3] + ["<PAGE_ID>", "<IG_ACCOUNT_ID>"])[:2] if len(sys.argv) < 3 else sys.argv[1:3]
H = (here / "header_template.csv").read_text(encoding="utf-16").splitlines()[0].split("\t")

VIDEOS = {"classic": "2071472733573470", "glass": "1102068022634572", "arrival": "2287178758524569",
          "winter": "3358940537626367", "words": "1444635664490225"}
COPY = {  # заголовок + основной текст (вариант A); B и C добавляются в кабинете через «Добавить вариант текста»
 "classic": ("Smooth. Silky. Glossy.", "Smooth. Silky. Glossy — without leaving home.\nKeratin, Hair Botox and Hair Recovery, tailored to your hair and done at your place in St. Moritz & the Engadin.\nDM to book 🤍"),
 "glass":   ("Glass hair, now in St. Moritz", "That glass-hair shine you keep saving on Instagram?\nIt's done here — at your place in St. Moritz. Keratin & Hair Botox.\nDM to book 🤍"),
 "arrival": ("Your salon, at home", "No salon. No commute. No waiting room.\nI bring everything with me and treat your hair at your home, chalet or hotel in St. Moritz.\nDM to book 🤍"),
 "winter":  ("Winter-proof your hair", "Dry mountain air, heating, hats, ski helmets — winter here is beautiful, but hard on hair.\nSmooth, glossy hair before the season starts. At your place in St. Moritz.\nDM to book ❄️"),
 "words":   ("Finally, in the valley", "\"I couldn't find anyone in the valley who does this.\"\nNow you don't have to look. Keratin, Hair Botox and Hair Recovery — at your home in St. Moritz & the Engadin.\nDM to book 🤍"),
}
COMMON = {
    "Campaign Status": "PAUSED", "Buying Type": "AUCTION", "Special Ad Categories": "None",
    "Campaign Page ID": page, "Link Object ID": f"o:{page}",
    "Ad Set Run Status": "PAUSED", "Ad Status": "PAUSED",
    "Cities": "St. Moritz, Graubünden, Switzerland (+40 km)", "Location Types": "home, recent",
    "Gender": "Women", "Age Min": "23", "Age Max": "55", "Locales": "English (All)",
    "Publisher Platforms": "instagram", "Instagram Positions": "stream, story, explore, reels", "Device Platforms": "mobile",
    "Billing Event": "IMPRESSIONS", "Attribution Spec": '[{"event_type":"CLICK_THROUGH","window_days":1}]',
    "Creative Type": "Video Page Post Ad", "Instagram Account ID": ig, "Use Page as Actor": "No",
}
CAMPAIGNS = [
    # холодная: посещения профиля — как лучшая кампания октября
    dict(camp="R3 · Profile · EN · cold", obj="Outcome Traffic", adset="Women 23-55 · St. Moritz +40km", budget="14",
         dest="INSTAGRAM_PROFILE", goal="VISIT_INSTAGRAM_PROFILE", cta="VIEW_INSTAGRAM_PROFILE",
         ads=["classic", "glass", "arrival", "winter"]),
    # ретаргет: сообщения в директ (аудитории выбрать в кабинете до запуска)
    dict(camp="R3 · Messages · EN · retarget", obj="Outcome Engagement", adset="Retarget · video viewers + IG engagers 60d", budget="5",
         dest="INSTAGRAM_DIRECT", goal="CONVERSATIONS", cta="INSTAGRAM_MESSAGE", ads=["words"]),
]
rows = []
for c in CAMPAIGNS:
    for v in c["ads"]:
        r = dict(COMMON)
        r.update({"Campaign Name": c["camp"], "Campaign Objective": c["obj"], "Ad Set Name": c["adset"],
                  "Ad Set Daily Budget": c["budget"], "Destination Type": c["dest"], "Optimization Goal": c["goal"],
                  "Call to Action": c["cta"], "Ad Name": f"R3 · {v} · DM to book", "Title": COPY[v][0],
                  "Body": COPY[v][1], "Video ID": VIDEOS[v]})
        rows.append(r)
miss = [k for r in rows for k in r if k not in H]
assert not miss, f"нет колонок в шаблоне: {set(miss)}"
esc = lambda s: '"' + s.replace('"', '""') + '"' if any(ch in s for ch in '\t\n"') else s
lines = ["\t".join(H)] + ["\t".join(esc(r.get(h, "")) for h in H) for r in rows]
out = here / "R3-import.csv"
out.write_text("\r\n".join(lines) + "\r\n", encoding="utf-16")
print("ok", out, len(rows), "объявлений; page", page, "ig", ig)
