# Comp fidelity measurements

Use this workflow when a supplied comp or approved reference must be compared
with a captured implementation. It produces review evidence, not a visual
verdict.

## Before comparison

- Capture reference and rendered PNGs at the same exact dimensions, viewport,
  device scale, browser/runtime, font state, theme, data state, and animation
  timing. The helper never registers, resizes, or silently aligns images.
- Prefer the existing browser67 or project capture path. This helper is not a
  second browser runtime and does not navigate, authenticate, or capture.
- Define 1–24 task-owned regions in a spec conforming to
  `contracts/comp-fidelity-spec.schema.json`. Each region names its salience and
  relevant dimensions: geometry, type, material, ground, controls, or content.
- Set `changed_pixel_delta` as a measurement noise floor. Optional advisory
  thresholds are project-owned diagnostics; omitting them is valid.
- The portable POC accepts at most four million canvas pixels, four million
  cumulative region pixels, and twenty-four million generated artifact pixels.
  Split larger capture sets into separately reviewed cases instead of widening
  those safety bounds ad hoc.

## Run and verify

```bash
python3 scripts/design_craft_comp_fidelity.py compare \
  --reference /abs/reference.png \
  --rendered /abs/rendered.png \
  --spec /abs/comp-spec.json \
  --output-dir /abs/new-evidence-dir

python3 scripts/design_craft_comp_fidelity.py validate \
  --manifest /abs/new-evidence-dir/report.json \
  --reference /abs/reference.png \
  --rendered /abs/rendered.png \
  --spec /abs/comp-spec.json \
  --strict
```

The output directory must not exist. The helper reads each input once into a
bounded immutable snapshot, computes its size and hash from those same bytes,
then stages and atomically promotes the output directory. Its PNG parser
rejects malformed critical-chunk ordering and trailing payloads. Strict
validation snapshots all three inputs again and recomputes metrics and
generated artifact bytes.
It emits a full heatmap,
side-by-side image, per-region pairs and heatmaps, and `report.json` conforming
to `contracts/comp-fidelity-report.schema.json`.

## Interpret the report

- `mean_delta`, `rmse`, changed-pixel ratio, luminance shift, and edge-energy
  delta are descriptive. They can locate drift; none proves design quality.
- Alpha is ignored in color metrics after PNG decoding. The comparison uses
  8-bit sRGB byte values, not perceptual color-space distance.
- `advisory.status` reports only whether optional project thresholds were
  crossed. It is never a release decision.
- Review primary regions first, then secondary and supporting regions. Use the
  region's named dimensions to explain what differs and whether the comp,
  product authority, or implementation should change.

Final acceptance still requires human visual review plus product correctness,
responsive states, accessibility, interaction, and runtime evidence. Report
the result as `measurement_only` until those separate gates are complete.
