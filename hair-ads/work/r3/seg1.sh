#!/bin/bash
# seg1.sh "<строка s ...>" — один кусок (для параллельного запуска)
set -euo pipefail
cd "$(dirname "$0")"; source ../lib.sh
eval "$(sed -n '/^W=/p;/^ICE=/p;/^s()/p' segs.sh)"
eval "$1"
