#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DETECTOR="${ROOT_DIR}/upstreams/impeccable/skill/scripts/detect.mjs"
TARGET="."
JSON_ONLY=0

usage() {
  cat <<'EOF'
Usage:
  scripts/frontend_craft_detect.sh [--target <path>] [--json-only]
  scripts/frontend_craft_detect.sh <path>

Runs the pinned Impeccable detector as a frontend-craft signal.
EOF
}

abspath() {
  python3 - "$1" <<'PY'
import sys
from pathlib import Path
print(Path(sys.argv[1]).expanduser().resolve())
PY
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="${2:?Missing value for --target}"
      shift 2
      ;;
    --json-only)
      JSON_ONLY=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      TARGET="$1"
      shift
      ;;
  esac
done

if [[ ! -f "${DETECTOR}" ]]; then
  echo "Missing detector: ${DETECTOR}" >&2
  echo "Run from the frontend-craft repo with upstream submodules initialized." >&2
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  echo "Missing node runtime required by ${DETECTOR}" >&2
  exit 1
fi

TARGET="$(abspath "${TARGET}")"
DETECTOR_TARGET="${TARGET}"
DETECTOR_NOTE=""
if [[ "${TARGET}" == "${ROOT_DIR}" ]]; then
  DETECTOR_TARGET="${ROOT_DIR}/skills/frontend-craft"
  DETECTOR_NOTE="source repo root normalized to installable skill folder"
fi

TMP_JSON="$(mktemp -t frontend-craft-detect.XXXXXX)"
trap 'rm -f "${TMP_JSON}"' EXIT

node "${DETECTOR}" --json "${DETECTOR_TARGET}" >"${TMP_JSON}"

if [[ "${JSON_ONLY}" == "1" ]]; then
  cat "${TMP_JSON}"
  exit 0
fi

python3 - "${TMP_JSON}" "${TARGET}" "${DETECTOR_TARGET}" "${DETECTOR_NOTE}" <<'PY'
import json
import sys
from collections import Counter
from pathlib import Path

path = Path(sys.argv[1])
target = sys.argv[2]
detector_target = sys.argv[3]
detector_note = sys.argv[4]

try:
    payload = json.loads(path.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"frontend-craft detector: failed to parse JSON for {target}: {exc}", file=sys.stderr)
    raise

if isinstance(payload, list):
    items = payload
elif isinstance(payload, dict):
    items = payload.get("issues") or payload.get("findings") or []
else:
    items = []

print(f"frontend-craft detector target: {target}")
if detector_target != target:
    print(f"detector_scan_target: {detector_target}")
if detector_note:
    print(f"detector_note: {detector_note}")
print(f"findings: {len(items)}")

if items:
    severities = Counter(str(item.get("severity", "unknown")) for item in items if isinstance(item, dict))
    if severities:
        print("severity_counts: " + ", ".join(f"{key}={value}" for key, value in sorted(severities.items())))
    print("Treat findings as signals; project DESIGN.md and runtime evidence remain higher authority.")
else:
    print("No detector findings.")

print("\nraw_json:")
PY

cat "${TMP_JSON}"
