#!/bin/bash
# apdl.sh OUTDIR URL... — скачать файлы через Apify (nerolabs/bulk-file-downloader), когда хост закрыт сетью среды.
# Файлы сохраняются как <порядковый номер>.<расширение> в OUTDIR.
set -euo pipefail
OUT=$1; shift; mkdir -p "$OUT"
H="Authorization: Bearer $APIFY_TOKEN"
IN=$(python3 -c 'import json,sys;print(json.dumps({"fileUrls":sys.argv[1:],"maxFileMb":1000,"requestTimeoutSecs":600,"dedupeUrls":False}))' "$@")
R=$(curl -s -X POST -H "$H" -H "Content-Type: application/json" "https://api.apify.com/v2/acts/nerolabs~bulk-file-downloader/runs?waitForFinish=280" -d "$IN")
DS=$(echo "$R" | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['defaultDatasetId'])")
KV=$(echo "$R" | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['defaultKeyValueStoreId'])")
curl -s -H "$H" "https://api.apify.com/v2/datasets/$DS/items?clean=true&fields=rowNumber,fileIndex,fileName,downloadStatus,extension,sourceUrl" | python3 -c "
import sys,json
for i in json.load(sys.stdin): print(i['rowNumber'], i['downloadStatus'], i.get('fileName') or '-', i.get('extension') or 'bin')" | while read n st fn ext; do
  if [ "$st" = downloaded ]; then curl -s -H "$H" -o "$OUT/$(printf %02d $n).$ext" "https://api.apify.com/v2/key-value-stores/$KV/records/$fn"; else echo "row $n: $st" >&2; fi
done
ls "$OUT" | wc -l
