#!/usr/bin/env bash
# Prepares a fresh cloud container for editing and reports what is ready.
# Usage: source scripts/setup.sh   (sourcing keeps HYPERFRAMES_BROWSER_PATH in your shell)

HF_VERSION=0.8.170

ok()   { printf '  \033[32m✓\033[0m %-14s %s\n' "$1" "$2"; }
fail() { printf '  \033[31m✗\033[0m %-14s %s\n' "$1" "$2"; }

# HyperFrames cannot download its own Chrome here; reuse the preinstalled headless shell.
shell_path=$(ls -d /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell 2>/dev/null | tail -1)
[ -n "$shell_path" ] && export HYPERFRAMES_BROWSER_PATH="$shell_path"

python3 -c "import faster_whisper" 2>/dev/null ||
  pip3 install --user --break-system-packages -q faster-whisper >/dev/null 2>&1

echo "Vibe Editing environment"
command -v node    >/dev/null && ok node    "$(node --version)"                     || fail node    "missing"
command -v ffmpeg  >/dev/null && ok ffmpeg  "$(ffmpeg -version | head -1 | cut -d' ' -f3)" || fail ffmpeg "missing"
command -v python3 >/dev/null && ok python3 "$(python3 --version | cut -d' ' -f2)"  || fail python3 "missing"
v=$(python3 -c "import faster_whisper as f; print(f.__version__)" 2>/dev/null) &&
  ok whisper "faster-whisper $v" || fail whisper "pip install faster-whisper failed"
[ -x "${HYPERFRAMES_BROWSER_PATH:-}" ] && ok chrome "$HYPERFRAMES_BROWSER_PATH" || fail chrome "no headless shell found"
v=$(npx -y "hyperframes@$HF_VERSION" --version 2>/dev/null | tail -1) &&
  ok hyperframes "$v" || fail hyperframes "npx could not fetch hyperframes"
