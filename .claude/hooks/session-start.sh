#!/bin/bash
# Ставит стек для видео (HyperFrames + whisper.cpp + headless Chrome + скиллы)
# в облачной сессии Claude Code. Идемпотентно: что уже стоит — пропускает.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

HYPERFRAMES_VERSION="0.8.113"
WHISPER_CPP_TAG="v1.9.4"
WHISPER_DIR="/opt/whisper.cpp"

export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1

# 1. HyperFrames CLI
if [ "$(hyperframes --version 2>/dev/null || true)" != "$HYPERFRAMES_VERSION" ]; then
  npm install -g "hyperframes@$HYPERFRAMES_VERSION" --no-fund --no-audit >/dev/null
fi

# 2. whisper.cpp -> whisper-cli в PATH
if ! command -v whisper-cli >/dev/null 2>&1; then
  if [ ! -d "$WHISPER_DIR/.git" ]; then
    git clone --depth 1 --branch "$WHISPER_CPP_TAG" https://github.com/ggml-org/whisper.cpp.git "$WHISPER_DIR"
  fi
  cmake -S "$WHISPER_DIR" -B "$WHISPER_DIR/build" -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=OFF -DWHISPER_BUILD_TESTS=OFF >/dev/null
  cmake --build "$WHISPER_DIR/build" -j"$(nproc)" --config Release --target whisper-cli >/dev/null
  ln -sf "$WHISPER_DIR/build/bin/whisper-cli" /usr/local/bin/whisper-cli
fi

# 3. Headless Chrome для рендера
hyperframes browser ensure >/dev/null

# 4. Скиллы HyperFrames для агентов (~/.claude/skills)
if [ ! -d "$HOME/.claude/skills/hyperframes" ]; then
  hyperframes skills >/dev/null
fi

echo 'export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1' >> "${CLAUDE_ENV_FILE:-/dev/null}"
