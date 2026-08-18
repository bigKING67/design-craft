# pbakaus/impeccable absorption matrix

This document records the deliberate fusion and runtime boundary for
`https://github.com/pbakaus/impeccable` through reviewed remote commit
`f88b2837a7d7c3182e46307bbbb091a1ed547571`. The compatibility submodule is
pinned at `80e4dd0d581fcdb42be62252b7bc07dcd2238330`, the last selected canonical
detector correctness commit in that reviewed range.

## Contents

- [Inventory truth](#inventory-truth)
- [Status vocabulary](#status-vocabulary)
- [Command taxonomy](#command-taxonomy)
- [Detector and platform coverage](#detector-and-platform-coverage)
- [Latest reviewed range](#latest-reviewed-range)
- [Runtime and packaging boundary](#runtime-and-packaging-boundary)
- [Current conclusion](#current-conclusion)

## Inventory truth

The pinned compatibility snapshot exposes one canonical source Skill, metadata
for twenty-three public commands plus the umbrella Skill, native platform
references, a detector, generated multi-host copies, and a substantial
live-browser/manual-edit/provider/package runtime. `design-craft` executes only
the stable source detector entrypoint. It absorbs general workflow, judgment,
selected detector correctness, native quality guidance, production hardening,
and bounded reference-fidelity review. It deliberately does not vendor or call
a second browser runtime, hook, forced reviewer, or provider/package system
beside browser67 and the host's existing execution contracts.

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
| `/craft` | absorbed | `craft` mode and bounded implementation/verification passes |
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
| Mechanical pre-scan and deterministic anti-pattern signals | absorbed | `design_craft_detect.sh` invokes `upstreams/impeccable/skill/scripts/detect.mjs` when the source checkout is available and preserves JSON findings even when upstream exits `2` |
| Style-carrier, comment-safe, linked-stylesheet, `rounded-none`, retired single-font, YAML-escape, and Blade-suffix correctness | absorbed | compatibility pin `80e4dd0`; selected behavior is proven by function-level `test_impeccable_detector_contract.py` coverage and `evals/fixtures/impeccable-detector/` |
| Source detector capability disclosure | absorbed | default and `--full-json` output distinguish `available`, `available_regex_fallback`, and `unavailable`; raw `--json-only` intentionally has no wrapper metadata |
| Detector/design-system reconciliation | absorbed | `impeccable-workflow.md`, project authority order, explicit exceptions |
| Reference-first salient-element inventory and fidelity classification | absorbed | `system-review.md`: direct reference inspection before builder summary; match/adaptation/missing/contradicted/unapproved-added matrix |
| Post-fix verdict | absorbed | original finding IDs return as resolved/partial/unresolved without a new defect hunt |
| Browser-native selection/caret/focus/underline/numeral/scrollbar surfaces | partial | focus is required; other surfaces follow project/browser authority and defaults are not automatic defects |
| Degraded/single-context evidence honesty | absorbed | critique method provenance and no-false-delegation rules |
| iOS audit/adapt guidance | absorbed | `ios-quality.md`, platform scanner and fixtures |
| Android audit/adapt guidance | absorbed | `android-quality.md`, platform scanner and fixtures |
| Adaptive parity | absorbed | `adaptive-quality.md`, shared-versus-platform-specific contracts |
| Hostile-data hardening and measurement-first optimization | absorbed | `impeccable-workflow.md`, engineering and performance references |

## Latest reviewed range

The latest range after `5c5553b1d7f9e89bb833f9179cea681742a17720`
through `f88b2837a7d7c3182e46307bbbb091a1ed547571` was reviewed on
2026-08-18 and is `provenance-only`. Its single commit changes only `bun.lock`
compatible dependency resolutions, including AI SDK, Claude agent SDK,
Puppeteer, and Svelte entries. It changes no canonical Skill, command metadata,
detector source, platform reference, or package manifest. Design Craft does not
vendor or execute this Bun dependency graph, so neither the compatibility pin
nor the selected behavior boundary advances.

### Earlier behavior-bearing range

The earlier range after `ae5e95101a6979e7f7973a4ff57680b3c7adc1ec`
through `5c5553b1d7f9e89bb833f9179cea681742a17720` was reviewed on
2026-08-17 and is `partial`:

| Capability | Status | Local target or boundary |
| --- | --- | --- |
| Reduced-motion alternatives and platform-specific capture evidence | absorbed | Local motion and native quality contracts already require intentional reduced-motion behavior, real simulator/emulator or device evidence, and explicit hardware limits. |
| Capture validity, comp fidelity, bounded review passes, and scoped verdicts | absorbed with calibration | Local visual acceptance separates screenshot validity, rendered comparison, original findings, and exact verdict scope without importing a mandatory reviewer runtime. |
| Shadow interpolation, layout-transition, ground-color, occlusion, image-backed contrast, scoped-ignore, and selector-compilation detector fixes | partial | These are useful canonical engine corrections, but the installed package uses the disclosed regex fallback because parser dependencies are not vendored. The compatibility pin does not advance without local executable fixtures for the selected engine boundary. |
| Critique snapshot/routing and direction/comps workflow changes | partial | Evidence-led critique and direction-first composition already exist locally. Upstream question UI, persisted runtime, fixed routing mechanics, and provider-specific orchestration remain outside the package. |
| Live/provider/browser-session, hook, asset-generation, and generated host copies | intentionally-rejected | These duplicate browser67 or host runtime ownership and would create a second session/evidence authority. |
| Universal detector bans or automatic runtime claims | intentionally-rejected | Static findings remain contextual signals; source presence does not prove browser, native, performance, or installed-host behavior. |

### Cumulative selected boundary

The cumulative absorption state remains `selective_absorbed` through the
selected behavior boundary `80e4dd0d581fcdb42be62252b7bc07dcd2238330`:

| Capability | Status | Local target or boundary |
| --- | --- | --- |
| Explicit brief authority and evidence-based visual authority | absorbed | `visual-judgment.md` |
| Refinement preserves; redesign replaces the visual world without replacing product truth | absorbed | `visual-judgment.md`, existing-redesign playbook |
| Per-surface `Persuade`, `Operate`, `Read`, and `Experience` modes | absorbed | `surface-playbooks.md` |
| Direction-first craft floor and applicable-denominator critique scoring | absorbed | `impeccable-workflow.md` |
| At-most-two batched rendered-verification passes | absorbed | `SKILL.md`; per-tweak screenshot loops remain outside the default workflow |
| Radial halo/spotlight glow, kicker, meaningless section number, fake cursor/pulse, shape-assembled illustration, and aphoristic-copy signals | absorbed | `visual-judgment.md`; treated as contextual signals, not universal bans |
| Random concept seeds, mandatory context loader and no-argument menu | intentionally-rejected | local routing and project discovery remain deterministic and task-led |
| Live/browser/provider/hooks/doctor runtime, asset generation, full detector/vendor bundle, generated provider copies | intentionally-rejected | browser67, host tools, and existing repository governance own these boundaries |
| `fc3dc50..bdaa5a4` live overlay/resume changes, TanStack adapters, deferred source writes, resolution caching, injection/progress coordination, tests, and generated providers | intentionally-rejected | The tail changes only the upstream live/provider runtime; no selected `design-craft` behavior was imported |
| Universal category, font, framework, and library prescriptions | intentionally-rejected | project authority and observed performance/accessibility evidence win |
| Promotional or "award-winning" tone | intentionally-rejected | local output remains factual and evidence-led |

The compatibility pin remains at the selected canonical detector boundary, not
the reviewed remote head. The later tail remains reviewed but outside the pin
because its additional detector engine behavior is not executable in the
dependency-free installed fallback and the runtime/provider changes are outside
the product boundary.

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
signal. The full static HTML/CSS engine resolves `htmlparser2`, `css-select`,
`css-tree`, and `domutils`; when they are absent, the wrapper runs the regex
fallback and marks the result degraded instead of claiming full engine parity.
Function-level selected-behavior tests, source pinning, and raw detector JSON do
not establish installed-host parity. Design Craft never claims live/browser
evidence unless the corresponding local tool actually ran.

## Current conclusion

`missing-high-value`: none within the selected fusion boundary through remote
head `f88b2837a7d7c3182e46307bbbb091a1ed547571`, reviewed on 2026-08-18.

The cumulative state is selective absorption. General workflow, brief and
change-scope authority, surface modes, native quality, detector discipline and
correctness, reference-first fidelity, post-fix verdicts, mechanical craft
verification, hardening, and evidence honesty are local. The duplicative
live/provider/package/hook runtime, forced delegation, universal visual bans,
and prescriptive ecosystem choices remain intentionally outside the product.

Current independent blind evidence is recorded in
`evals/comparative/impeccable-production-ablation/`: `design-craft` 100,
focused Impeccable upstream 97, no-skill baseline 96.
