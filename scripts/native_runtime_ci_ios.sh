#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

EVIDENCE_DIR="${DESIGN_CRAFT_NATIVE_EVIDENCE_DIR:-${RUNNER_TEMP:-${TMPDIR:-/tmp}}/native-runtime-ios}"
APP_DIR="${EVIDENCE_DIR}/DesignCraftEvidence.app"
mkdir -p "${APP_DIR}"
cp evals/native-runtime/fixtures/ios/Info.plist "${APP_DIR}/Info.plist"

sdk_path="$(xcrun --sdk iphonesimulator --show-sdk-path)"
deployment_target="$(/usr/libexec/PlistBuddy -c 'Print :MinimumOSVersion' evals/native-runtime/fixtures/ios/Info.plist)"
arch="$(uname -m)"
xcrun --sdk iphonesimulator swiftc \
  -parse-as-library \
  -module-name DesignCraftEvidence \
  -sdk "${sdk_path}" \
  -target "${arch}-apple-ios${deployment_target}-simulator" \
  -framework UIKit \
  evals/native-runtime/fixtures/ios/App.swift \
  -o "${APP_DIR}/DesignCraftEvidence"
codesign --force --sign - "${APP_DIR}"

if [[ "${DESIGN_CRAFT_NATIVE_BUILD_ONLY:-0}" == "1" ]]; then
  echo "iOS fixture build verified: ${APP_DIR}"
  exit 0
fi

selection="$(xcrun simctl list devices available -j | python3 -c '
import json
import re
import sys

payload = json.load(sys.stdin)
candidates = []
for runtime, devices in payload.get("devices", {}).items():
    match = re.search(r"\.iOS-([0-9-]+)$", runtime)
    if not match:
        continue
    version = tuple(int(part) for part in match.group(1).split("-"))
    for device in devices:
        name = str(device.get("name", ""))
        device_type = str(device.get("deviceTypeIdentifier", ""))
        if device.get("isAvailable") and name.startswith("iPhone") and device_type:
            preferred = int("Pro" in name and "Max" not in name)
            candidates.append((version, preferred, name, runtime, device_type))
if not candidates:
    raise SystemExit("No available iPhone Simulator")
selected = max(candidates)
print(f"{selected[3]}\t{selected[4]}")
')"
IFS=$'\t' read -r runtime_identifier device_type_identifier <<< "${selection}"
printf 'runtime=%s\ndevice_type=%s\n' \
  "${runtime_identifier}" \
  "${device_type_identifier}" \
  > "${EVIDENCE_DIR}/simulator-selection.txt"
simulator_name="Design Craft Evidence ${GITHUB_RUN_ID:-$$}"
udid="$(xcrun simctl create \
  "${simulator_name}" \
  "${device_type_identifier}" \
  "${runtime_identifier}")"
cleanup_simulator() {
  xcrun simctl shutdown "${udid}" >/dev/null 2>&1 || true
  xcrun simctl delete "${udid}" >/dev/null 2>&1 || true
}
trap cleanup_simulator EXIT
xcrun simctl boot "${udid}"
xcrun simctl bootstatus "${udid}" -b
xcrun simctl install "${udid}" "${APP_DIR}"
xcrun simctl launch "${udid}" dev.designcraft.runtime-evidence > "${EVIDENCE_DIR}/launch.txt"
sleep 2
xcrun simctl io "${udid}" screenshot "${EVIDENCE_DIR}/ios-before-interaction.png"
data_container="$(xcrun simctl get_app_container "${udid}" dev.designcraft.runtime-evidence data)"
interaction_marker="${data_container}/Documents/runtime-interaction.txt"
runtime_events="${data_container}/Documents/runtime-events.txt"
rm -f "${interaction_marker}"
copy_runtime_events() {
  if [[ -f "${runtime_events}" ]]; then
    cp "${runtime_events}" "${EVIDENCE_DIR}/runtime-events.txt"
  fi
}
wait_for_interaction() {
  local attempt
  for attempt in {1..15}; do
    if [[ -f "${interaction_marker}" ]] \
      && grep -q "Runtime interaction confirmed" "${interaction_marker}"; then
      return 0
    fi
    sleep 2
  done
  return 1
}

interaction_path=""
if xcrun simctl openurl \
  "${udid}" \
  "designcraft-evidence://confirm" \
  > "${EVIDENCE_DIR}/openurl-live.txt" 2>&1 \
  && wait_for_interaction; then
  interaction_path="live-deep-link"
else
  xcrun simctl io "${udid}" screenshot \
    "${EVIDENCE_DIR}/ios-live-deep-link-timeout.png" \
    >/dev/null 2>&1 || true
  xcrun simctl terminate "${udid}" dev.designcraft.runtime-evidence || true
  rm -f "${interaction_marker}"
  if xcrun simctl openurl \
    "${udid}" \
    "designcraft-evidence:///confirm" \
    > "${EVIDENCE_DIR}/openurl-cold.txt" 2>&1 \
    && wait_for_interaction; then
    interaction_path="cold-deep-link"
  else
    xcrun simctl io "${udid}" screenshot \
      "${EVIDENCE_DIR}/ios-cold-deep-link-timeout.png" \
      >/dev/null 2>&1 || true
  fi
fi

copy_runtime_events
{
  printf '%s\n' '[initial launch]'
  cat "${EVIDENCE_DIR}/launch.txt"
  printf '%s\n' '[live deep link]'
  cat "${EVIDENCE_DIR}/openurl-live.txt" 2>/dev/null || true
  if [[ -f "${EVIDENCE_DIR}/openurl-cold.txt" ]]; then
    printf '%s\n' '[cold deep link fallback]'
    cat "${EVIDENCE_DIR}/openurl-cold.txt"
  fi
  printf '%s\n' '[application events]'
  cat "${EVIDENCE_DIR}/runtime-events.txt" 2>/dev/null || true
  printf '%s\n' "[confirmed interaction path] ${interaction_path:-none}"
} > "${EVIDENCE_DIR}/runtime-launch.log"

if [[ -z "${interaction_path}" ]]; then
  xcrun simctl spawn "${udid}" log show --last 3m --info --debug \
    --predicate 'process == "DesignCraftEvidence" OR eventMessage CONTAINS[c] "designcraft" OR eventMessage CONTAINS[c] "openurl"' \
    > "${EVIDENCE_DIR}/interaction-diagnostics.log" 2>&1 || true
  echo "iOS runtime deep link did not produce the interaction marker" >&2
  exit 1
fi
cp "${interaction_marker}" "${EVIDENCE_DIR}/runtime-interaction.txt"
xcrun simctl io "${udid}" screenshot "${EVIDENCE_DIR}/ios-after-interaction.png"

python3 scripts/design_craft_native_runtime_record.py \
  --platform ios \
  --runtime-kind ios_simulator \
  --runtime-id "${udid}" \
  --tool "xcodebuild/xcrun simctl" \
  --command "xcrun swiftc iOS fixture" \
  --command "xcrun simctl boot/install/launch" \
  --command "xcrun simctl openurl live/cold deep-link interaction and marker assertion" \
  --command "xcrun simctl io before/after screenshots" \
  --assertion build_succeeded=true \
  --assertion install_and_launch_succeeded=true \
  --assertion runtime_interaction_observed=true \
  --assertion before_and_after_screenshots_captured=true \
  --artifact "before_screenshot=${EVIDENCE_DIR}/ios-before-interaction.png" \
  --artifact "after_screenshot=${EVIDENCE_DIR}/ios-after-interaction.png" \
  --artifact "interaction_marker=${EVIDENCE_DIR}/runtime-interaction.txt" \
  --artifact "launch_log=${EVIDENCE_DIR}/runtime-launch.log" \
  --fixture-root evals/native-runtime/fixtures/ios \
  --output "${EVIDENCE_DIR}/ios-observed.json"
python3 scripts/design_craft_native_runtime_validate.py \
  --validate \
  --root "${EVIDENCE_DIR}" \
  --require ios \
  --require-current-source \
  --json
