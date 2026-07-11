#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

EVIDENCE_DIR="${DESIGN_CRAFT_NATIVE_EVIDENCE_DIR:-${RUNNER_TEMP:-${TMPDIR:-/tmp}}/native-runtime-android}"
mkdir -p "${EVIDENCE_DIR}"

dump_ui() {
  local output="$1"
  local expected_text="${2:-}"
  local remote_path="/data/local/tmp/design-craft-window.xml"
  local temporary="${output}.tmp"
  local attempt

  for attempt in {1..10}; do
    rm -f "${temporary}"
    if adb shell rm -f "${remote_path}" >/dev/null 2>&1 \
      && adb shell uiautomator dump "${remote_path}" >/dev/null 2>&1 \
      && adb exec-out cat "${remote_path}" > "${temporary}" 2>/dev/null; then
      if ! grep -q '<hierarchy' "${temporary}"; then
        sleep 3
        continue
      fi
      if [[ -n "${expected_text}" ]] && ! grep -q -- "${expected_text}" "${temporary}"; then
        sleep 3
        continue
      fi
      mv "${temporary}" "${output}"
      return 0
    fi
    sleep 3
  done

  adb shell dumpsys window windows > "${EVIDENCE_DIR}/window-diagnostics.txt" 2>&1 || true
  echo "Unable to capture a stable UIAutomator tree containing: ${expected_text}" >&2
  return 1
}

PROJECT_DIR="${EVIDENCE_DIR}/android-project"
rm -rf "${PROJECT_DIR}"
cp -R evals/native-runtime/fixtures/android "${PROJECT_DIR}"
gradle -p "${PROJECT_DIR}" :app:assembleDebug --no-daemon
apk="${PROJECT_DIR}/app/build/outputs/apk/debug/app-debug.apk"
adb install -r "${apk}"
adb wait-for-device
adb shell am force-stop dev.designcraft.runtimeevidence
adb shell am start -W -n dev.designcraft.runtimeevidence/.MainActivity > "${EVIDENCE_DIR}/launch.txt"
sleep 3
dump_ui "${EVIDENCE_DIR}/window-before.xml" "Native runtime evidence title"

read -r tap_x tap_y < <(python3 - "${EVIDENCE_DIR}/window-before.xml" <<'PY'
import re
import sys
import xml.etree.ElementTree as ET

root = ET.parse(sys.argv[1]).getroot()
for node in root.iter("node"):
    if node.attrib.get("content-desc") == "Confirm native runtime":
        match = re.fullmatch(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", node.attrib["bounds"])
        if not match:
            break
        left, top, right, bottom = map(int, match.groups())
        print((left + right) // 2, (top + bottom) // 2)
        raise SystemExit(0)
raise SystemExit("Confirm runtime button not found")
PY
)
adb shell input tap "${tap_x}" "${tap_y}"
dump_ui "${EVIDENCE_DIR}/window-after.xml" "Runtime interaction confirmed"
adb exec-out screencap -p > "${EVIDENCE_DIR}/android-emulator.png"

python3 scripts/design_craft_native_runtime_record.py \
  --platform android \
  --runtime-kind android_emulator \
  --runtime-id "$(adb get-serialno)" \
  --tool "Gradle/adb/UIAutomator" \
  --command "gradle :app:assembleDebug" \
  --command "adb install and am start -W" \
  --command "UIAutomator dump, input tap, and screencap" \
  --assertion build_succeeded=true \
  --assertion install_and_launch_succeeded=true \
  --assertion accessibility_tree_observed=true \
  --assertion interaction_observed=true \
  --assertion screenshot_captured=true \
  --artifact "${EVIDENCE_DIR}/android-emulator.png" \
  --fixture-root evals/native-runtime/fixtures/android \
  --output "${EVIDENCE_DIR}/android-observed.json"
python3 scripts/design_craft_native_runtime_validate.py \
  --validate \
  --root "${EVIDENCE_DIR}" \
  --require android \
  --require-current-source \
  --json
