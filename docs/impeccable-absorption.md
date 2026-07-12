# pbakaus/impeccable absorption matrix

This document records the deliberate fusion and runtime boundary for
`https://github.com/pbakaus/impeccable` at commit
`630fc2682a5bd39b25a8e61f74b6b3f14f2b1e21`.

## Contents

- [Inventory truth](#inventory-truth)
- [Status vocabulary](#status-vocabulary)
- [Command taxonomy](#command-taxonomy)
- [Detector and platform coverage](#detector-and-platform-coverage)
- [Runtime and packaging boundary](#runtime-and-packaging-boundary)
- [Current conclusion](#current-conclusion)

## Inventory truth

The reviewed upstream exposes one generated Agent Skill, twenty-four public
command documents, native platform references, a detector, and a substantial
live-browser/manual-edit/provider/package runtime. `design-craft` absorbs the
general workflow, detector signals, native quality guidance, and production
hardening discipline. It deliberately does not vendor a second browser runtime
or provider/package system beside browser67 and the host's existing execution
contracts.

## Status vocabulary

- `absorbed`: represented in local instructions, references, scripts,
  templates, or validation.
- `partial`: the general behavior is local, while branded command syntax or a
  specialized runtime remains upstream-only.
- `missing-high-value`: a valuable capability is absent and blocks a complete
  absorption claim.
- `intentionally-rejected`: copying would duplicate runtime infrastructure,
  widen trust boundaries, or conflict with local authority.
- `provenance-only`: retained for traceability without local behavior.

## Command taxonomy

| Upstream command | Status | Local expression |
| --- | --- | --- |
| `/shape` | absorbed | `shape` mode and product/design brief |
| `/craft` | absorbed | `craft` mode and implementation/verification loop |
| `/critique` | absorbed | bounded read-only product/visual judgment |
| `/audit` | absorbed | accessibility, responsive, performance, theming, and anti-pattern audit |
| `/polish` | absorbed | final-state visual and interaction refinement |
| `/harden` | absorbed | hostile data, failures, i18n, overflow, permission, and offline states |
| `/adapt` | absorbed | viewport/context adaptation plus native/adaptive routing |
| `/optimize` | absorbed | measurement-first performance diagnosis |
| `/extract` | absorbed | repeated-use-first token/component extraction |
| `/document` | absorbed | project-approved `DESIGN.md` evolution |
| `/live` | absorbed | browser iteration as a capability; browser67 supplies the runtime |
| `/init` | partial | `PRODUCT.md`/`DESIGN.md` discovery and safe seed helpers replace branded initialization |
| `/onboard` | partial | product context and project authority discovery are local |
| `/animate` | partial | motion-quality, pattern, planning, and runtime-evidence references are local |
| `/layout` | partial | hierarchy, grid, responsive, and surface playbooks are local |
| `/typeset` | partial | typography roles, optical sizing, line length, and hierarchy are local |
| `/colorize` | partial | semantic color roles and contrast are local; arbitrary recoloring is not a baseline mode |
| `/clarify` | partial | information hierarchy, copy, and decision-flow repairs are local |
| `/delight` | partial | causal feedback and restrained product delight are local |
| `/bolder` | partial | stronger hierarchy is supported without a universal intensity transform |
| `/quieter` | partial | reduced noise and surface restraint are supported without a universal style transform |
| `/overdrive` | partial | high-expression work requires explicit style authority rather than an automatic extreme mode |
| `/distill` | partial | repeated patterns can become design-system contracts after evidence of reuse |
| `/impeccable` | partial | the umbrella workflow is fused into `design-craft`; upstream branding and runtime remain separate |

## Detector and platform coverage

| Capability | Status | Local target |
| --- | --- | --- |
| Mechanical pre-scan and deterministic anti-pattern signals | absorbed | `design_craft_detect.sh` invokes `upstreams/impeccable/skill/scripts/detect.mjs` when the source checkout is available |
| Detector/design-system reconciliation | absorbed | `impeccable-workflow.md`, project authority order, explicit exceptions |
| Degraded/single-context evidence honesty | absorbed | critique method provenance and no-false-delegation rules |
| iOS audit/adapt guidance | absorbed | `ios-quality.md`, platform scanner and fixtures |
| Android audit/adapt guidance | absorbed | `android-quality.md`, platform scanner and fixtures |
| Adaptive parity | absorbed | `adaptive-quality.md`, shared-versus-platform-specific contracts |
| Hostile-data hardening and measurement-first optimization | absorbed | `impeccable-workflow.md`, engineering and performance references |

## Runtime and packaging boundary

The following surfaces are `intentionally-rejected` from the baseline package:

- upstream `live-server`, browser injection, browser session, overlay, and
  manual-edit runtimes, because browser67 and project tools already own that
  trust and lifecycle boundary;
- upstream asset-producer/manual-edit agents and forced delegation policy;
- generated provider output, extension/store artifacts, site output,
  dependencies, and OpenAI/Claude plugin packaging;
- GitHub sheriff automation, which is repository operations rather than product
  design behavior.

The pristine submodule remains available for provenance and selective manual
use. `design-craft` calls only the detector path as an optional source-level
signal and never claims live/browser evidence unless the corresponding local
tool actually ran.

## Current conclusion

`missing-high-value`: none within the selected fusion boundary.

The cumulative state is selective absorption. General workflow, native
quality, detector discipline, hardening, and evidence honesty are local; the
duplicative live/provider/package runtime is intentionally not vendored. The
range from `da99645a58400ed7acb201e6904f9413efd89c6e` to the reviewed head
changes GitHub sheriff stale-clock automation only, so its latest-range status
is repository operations rather than new design behavior.

Current independent blind evidence is recorded in
`evals/comparative/impeccable-production-ablation/`: `design-craft` 98,
focused Impeccable upstream 95, no-skill baseline 94.
