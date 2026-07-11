#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

EVIDENCE_DIR="${DESIGN_CRAFT_NATIVE_EVIDENCE_DIR:-${RUNNER_TEMP:-${TMPDIR:-/tmp}}/native-runtime-ios}"
APP_DIR="${EVIDENCE_DIR}/DesignCraftEvidence.app"
mkdir -p "${APP_DIR}"
cp evals/native-runtime/fixtures/ios/Info.plist "${APP_DIR}/Info.plist"

sdk_path="$(xcrun --sdk iphonesimulator --show-sdk-path)"
sdk_version="$(xcrun --sdk iphonesimulator --show-sdk-version)"
arch="$(uname -m)"
xcrun swiftc \
  -parse-as-library \
  -module-name DesignCraftEvidence \
  -sdk "${sdk_path}" \
  -target "${arch}-apple-ios${sdk_version}-simulator" \
  -framework UIKit \
  evals/native-runtime/fixtures/ios/App.swift \
  -o "${APP_DIR}/DesignCraftEvidence"
codesign --force --sign - "${APP_DIR}"

xcrun simctl list devices available -j > "${EVIDENCE_DIR}/devices.json"
udid="$(python3 - "${EVIDENCE_DIR}/devices.json" <<'PY'
import json
import sys

payload = json.load(open(sys.argv[1], encoding="utf-8"))
for devices in payload.get("devices", {}).values():
    for device in devices:
        if device.get("isAvailable") and str(device.get("name", "")).startswith("iPhone"):
            print(device["udid"])
            raise SystemExit(0)
raise SystemExit("No available iPhone Simulator")
PY
)"
xcrun simctl boot "${udid}" || true
xcrun simctl bootstatus "${udid}" -b
xcrun simctl install "${udid}" "${APP_DIR}"
xcrun simctl launch "${udid}" dev.designcraft.runtime-evidence > "${EVIDENCE_DIR}/launch.txt"
sleep 2
xcrun simctl io "${udid}" screenshot "${EVIDENCE_DIR}/ios-before-interaction.png"
data_container="$(xcrun simctl get_app_container "${udid}" dev.designcraft.runtime-evidence data)"
interaction_marker="${data_container}/Documents/runtime-interaction.txt"
rm -f "${interaction_marker}"
xcrun simctl terminate "${udid}" dev.designcraft.runtime-evidence
xcrun simctl launch \
  "${udid}" \
  dev.designcraft.runtime-evidence \
  --confirm-runtime \
  > "${EVIDENCE_DIR}/interaction-launch.txt"
interaction_observed=0
for _ in {1..20}; do
  if [[ -f "${interaction_marker}" ]] \
    && grep -q "Runtime interaction confirmed" "${interaction_marker}"; then
    interaction_observed=1
    break
  fi
  sleep 2
done
if [[ "${interaction_observed}" != "1" ]]; then
  xcrun simctl spawn "${udid}" log show --last 2m \
    --predicate 'process == "DesignCraftEvidence"' \
    > "${EVIDENCE_DIR}/interaction-diagnostics.log" 2>&1 || true
  echo "iOS runtime confirmation launch did not produce the marker" >&2
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
  --command "xcrun simctl relaunch with --confirm-runtime and marker assertion" \
  --command "xcrun simctl io before/after screenshots" \
  --assertion build_succeeded=true \
  --assertion install_and_launch_succeeded=true \
  --assertion runtime_interaction_observed=true \
  --assertion before_and_after_screenshots_captured=true \
  --artifact "${EVIDENCE_DIR}/ios-before-interaction.png" \
  --artifact "${EVIDENCE_DIR}/ios-after-interaction.png" \
  --artifact "${EVIDENCE_DIR}/runtime-interaction.txt" \
  --fixture-root evals/native-runtime/fixtures/ios \
  --output "${EVIDENCE_DIR}/ios-observed.json"
python3 scripts/design_craft_native_runtime_validate.py \
  --validate \
  --root "${EVIDENCE_DIR}" \
  --require ios \
  --require-current-source \
  --json
