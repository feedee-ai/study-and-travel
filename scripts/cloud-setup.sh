#!/bin/bash
# Стек для видео: HyperFrames + whisper.cpp + headless Chrome + скиллы.
# Для поля "Setup script" облачного окружения Claude Code — работает с любым репо.
set -euo pipefail
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1

if [ "$(hyperframes --version 2>/dev/null || true)" != "0.8.113" ]; then
  npm install -g hyperframes@0.8.113 --no-fund --no-audit
fi

if ! command -v whisper-cli >/dev/null 2>&1; then
  [ -d /opt/whisper.cpp/.git ] || git clone --depth 1 --branch v1.9.4 https://github.com/ggml-org/whisper.cpp.git /opt/whisper.cpp
  cmake -S /opt/whisper.cpp -B /opt/whisper.cpp/build -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DWHISPER_BUILD_TESTS=OFF
  cmake --build /opt/whisper.cpp/build -j"$(nproc)" --config Release --target whisper-cli
  ln -sf /opt/whisper.cpp/build/bin/whisper-cli /usr/local/bin/whisper-cli
fi

hyperframes browser ensure
[ -d "$HOME/.claude/skills/hyperframes" ] || hyperframes skills
