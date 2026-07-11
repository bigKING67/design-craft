# Native runtime evidence

Static source scans and platform fixtures do not count as native runtime
evidence. The maturity gate accepts only schema-valid observed artifacts from
an iOS Simulator/device and an Android Emulator/device.

Probe the current host:

```bash
python3 scripts/design_craft_native_runtime_validate.py --probe --json
```

Validate recorded evidence:

```bash
python3 scripts/design_craft_native_runtime_validate.py \
  --validate \
  --require ios \
  --require android \
  --require-real-device \
  --json
```

Required files for full maturity are `ios-observed.json` from an iOS Simulator,
`android-observed.json` from an Android Emulator, and
`real-device-observed.json` from at least one iOS or Android physical device.
Each must record the exact runtime identity, commands, at least three passing
runtime assertions, source commit/dirty state, local or CI capture context, and
at least one non-empty artifact stored beside the evidence JSON, with matching
relative path, byte count, and SHA-256. Missing, absolute, or directory-escaping
artifact paths are rejected. Do not create these files from static fixtures or
source inspection.
