#!/usr/bin/env bash
# 설치와 비교 및 회수는 운영체제에 공통인 Python 엔진에서 처리한다.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  cat <<'USAGE'
Usage: bash bootstrap/sync-gpt.sh [--status | --push | --pull] [--home PATH] [--codex-home PATH]

Default: show the status table, then choose Push, Pull, or Exit with the arrow keys.
--status: compare only. --push: install managed instructions and skills, then merge declared shared settings.
--pull: collect existing managed files and declared settings.
Requires Python 3.11+. GPT_SET_PYTHON can select an explicit Python executable.
USAGE
  exit 0
fi

# 특정 컴퓨터의 Python 경로를 저장소에 고정하지 않는다.
selected_python=""
if [[ -n "${GPT_SET_PYTHON:-}" ]]; then
  candidates=("$GPT_SET_PYTHON")
else
  candidates=(python3 python)
fi
for candidate in "${candidates[@]}"; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' >/dev/null 2>&1; then
    selected_python="$candidate"
    break
  fi
done
if [[ -z "$selected_python" ]]; then
  printf '%s\n' 'ERROR: Python 3.11+ was not found. Install Python or set GPT_SET_PYTHON.' >&2
  exit 2
fi

exec "$selected_python" -X utf8 "$SCRIPT_DIR/sync_gpt.py" "$@"
