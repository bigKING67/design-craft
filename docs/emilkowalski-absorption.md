# Emil Kowalski five-skill absorption matrix

This document records the deliberate absorption boundary for
`https://github.com/emilkowalski/skills` at commit
`e695d13cb298db0f46d5ef05be2ad13fa12908a6`. The compatibility submodule
stays pinned at `7bb7061b5cf7de15ea1aeaf00fbd9e6592a20fce`.

## Contents

- [Inventory truth](#inventory-truth)
- [Status vocabulary](#status-vocabulary)
- [Skill-level matrix](#skill-level-matrix)
- [Latest-range entrypoints](#latest-range-entrypoints)
- [Auxiliary-file matrix](#auxiliary-file-matrix)
- [Intentionally rejected rules](#intentionally-rejected-rules)
- [Current conclusion](#current-conclusion)

## Inventory truth

The pinned compatibility snapshot contains:

- five `SKILL.md` entrypoints;
- three auxiliary Markdown references;
- no `scripts/`, `assets/`, `templates/`, `agents/`, package source, or runtime
  component library under the five Skill directories.

Therefore, "copy more source" means adapting Markdown rules and small CSS/JS
examples. It does not mean vendoring an upstream implementation library that is
not present. The reviewed remote range adds `find-animation-opportunities` and
`pick-ui-library`; both receive an explicit decision below. The pristine
compatibility source remains available under `upstreams/emilkowalski-skills/`;
the installed Skill receives only the high-value fusion layer.

## Status vocabulary

- `absorbed`: the capability is represented in local instructions, references,
  scripts, templates, or validation.
- `partial`: a useful subset is local, while contextual or lower-value material
  remains upstream-only.
- `missing-high-value`: a valuable capability is still absent and should block
  an "absorption complete" claim.
- `intentionally-rejected`: copying would reduce correctness, conflict with
  authority/runtime evidence, or impose an inappropriate operating policy.
- `provenance-only`: retained for traceability but not used as local behavior.

## Skill-level matrix

### `emil-design-eng`

| Capability | Status | Local target | Decision |
| --- | --- | --- | --- |
| Motion purpose, frequency, easing, duration, physicality, interruption, accessibility | absorbed | `motion-quality.md` | Kept as calibrated starting points under project authority. |
| Concrete press, anchored overlay, tooltip-group, enter/exit, clip-path, and crossfade recipes | absorbed | `motion-patterns.md` | Added as implementation patterns with browser/performance caveats. |
| Component defaults, low-friction APIs, invisible edge cases, interactive documentation | absorbed | `engineering-quality.md`, `motion-patterns.md` | Adapted from the Sonner lessons without turning memorable naming into a universal rule. |
| Optical sizing, role-specific tracking and leading, text scaling | absorbed | `design-system-contract.md` | Added to the typography contract instead of motion guidance. |
| Animation vocabulary | absorbed | `motion-vocabulary.md` | Expanded to include spring parameters, ambient motion, and animation principles. |
| Mandatory promotional initial response | intentionally-rejected | none | Host/user intent controls the first response; the Skill must not advertise a course before doing work. |
| Absolute framework/GPU assertions | intentionally-rejected | `motion-audit-planning.md` | Local rules distinguish source risk from measured jank/compositing. |

### `apple-design`

| Capability | Status | Local target | Decision |
| --- | --- | --- | --- |
| Pointer-down response, 1:1 tracking, grab offset, capture | absorbed | `interaction-physics.md` | Includes coordinate-space and transform-ownership checks missing upstream. |
| Presentation-value interruption, velocity handoff, projection, snap selection | absorbed | `interaction-physics.md` | Preserves velocity units and runtime verification boundaries. |
| Springs, damping/response, rubber-banding, hysteresis | absorbed | `interaction-physics.md` | Values remain starting points, not universal constants. |
| Product purpose, agency, responsibility, familiarity, flexibility, simplicity, craft, delight | absorbed | `product-design-principles.md` | Converted into operational product tests. |
| Optical typography and multimodal causal feedback | absorbed | `design-system-contract.md`, `product-design-principles.md`, platform references | Applied where the platform supports the behavior. |
| Translucent materials and decorative depth recipes | partial | `visual-judgment.md`, iOS/Android references | Kept contextual; global glass/backdrop-filter rules would conflict with product authority and performance evidence. |
| Exact Apple-like appearance as a default aesthetic | intentionally-rejected | none | Platform behavior may be authoritative; visual imitation is not. |

### `review-animations`

| Capability | Status | Local target | Decision |
| --- | --- | --- | --- |
| Purpose/frequency/timing/origin/interruption/accessibility review bar | absorbed | `motion-quality.md` | Preserves the high craft bar. |
| `Before | After | Why` review format and explicit verdict | absorbed | `motion-quality.md` | Used for normal motion review with bounded findings. |
| Static detector signals for transition-all, ease-in, scale-zero, origin, duration, layout properties, hover, Reduced Motion | absorbed | `design_craft_detect.sh` | Signals require contextual confirmation before becoming findings. |
| "Default to flagging" tone and automatic hard blocks | intentionally-rejected | none | Evidence and user impact decide severity; aggressive tone is not quality. |
| Static code as proof of dropped frames/GPU execution/device feel | intentionally-rejected | `motion-audit-planning.md` | Runtime claims require trace/browser/device evidence. |

### `improve-animations`

| Capability | Status | Local target | Decision |
| --- | --- | --- | --- |
| Recon, stack/token/frequency map, eight-dimension audit | absorbed | `motion-audit-planning.md` | Adds authority and evidence checkpoints. |
| Re-read/vet findings, prioritize by leverage, separate missed opportunities | absorbed | `motion-audit-planning.md` | Uses user impact x frequency x confidence / cost. |
| Self-contained source-stamped plans | absorbed | `templates/motion-plan/plan.md`, `design_craft_motion_plan.py` | Deterministic scaffold plus drift stop conditions. |
| Execute/reconcile lifecycle | absorbed | `motion-audit-planning.md` | Supports proposed/in-progress/complete/stale/retired states. |
| Mandatory subagent fan-out | intentionally-rejected | none | Host capability, current authorization, task size, and project rules govern delegation. |
| Permanent read-only refusal after the user asks to implement | intentionally-rejected | none | Audit-only requests remain read-only; explicit implementation requests can proceed through normal quality gates. |

### `animation-vocabulary`

| Capability | Status | Local target | Decision |
| --- | --- | --- | --- |
| Reverse lookup and concise disambiguation | absorbed | `motion-vocabulary.md` | Keeps naming questions concise and implementation-neutral. |
| Entrances, timing, transforms, state, scroll, interaction, easing, effects, performance | absorbed | `motion-vocabulary.md` | Core glossary retained. |
| Spring parameter terms, looping/ambient motion, anticipation/follow-through/squash-stretch principles | absorbed | `motion-vocabulary.md` | Filled the previous low-cost vocabulary gap. |
| Requirement to quote upstream wording verbatim | intentionally-rejected | none | Local phrasing may be clearer, more concise, and license-attributed without forcing verbatim output. |

## Latest-range entrypoints

| Upstream entrypoint or change | Status | Local target or boundary | Decision |
| --- | --- | --- | --- |
| `find-animation-opportunities` | absorbed | `motion-quality.md`, `motion-audit-planning.md`, `motion-vocabulary.md` | Purpose, frequency, speed, function, missed-opportunity, explicit rejection, and bounded-output rules are already represented locally. The local workflow can report that no candidate survives rather than manufacturing motion. |
| `pick-ui-library` | intentionally-rejected | project dependency authority | Its curated list is a personal library preference, not a stable cross-framework design baseline. Existing dependencies, project constraints, bundle/performance evidence, accessibility, and maintenance cost decide library selection. |
| Radix UI to Base UI-only prescription | intentionally-rejected | framework-neutral component guidance | `design-craft` supports both when project authority selects them; an upstream wording replacement does not justify ecosystem churn. |
| README and library-link corrections | provenance-only | pristine upstream history | These edits do not add product behavior. |
| `f6f79ca..e695d13` README copy cleanup | provenance-only | pristine upstream history | The new tail changes README wording only and adds no runtime or design behavior. |

## Auxiliary-file matrix

| Upstream file | Status | Local target |
| --- | --- | --- |
| `improve-animations/AUDIT.md` | absorbed | `motion-quality.md`, `motion-audit-planning.md`, detector rules |
| `improve-animations/PLAN-TEMPLATE.md` | absorbed | `templates/motion-plan/plan.md`, `design_craft_motion_plan.py` |
| `review-animations/STANDARDS.md` | absorbed with calibration | `motion-quality.md`, `motion-patterns.md`, `motion-audit-planning.md` |

## Intentionally rejected rules

The local fusion does not copy these as universal truth:

- `transition: all` is a broad ownership risk, but static text alone does not
  prove layout, paint, or dropped frames.
- Transform use does not by itself prove GPU compositing; a full transform
  string does not automatically move a JavaScript-driven animation off the
  main thread.
- `ease-in`, animation above 300 ms, layout-property animation, blur, or
  keyframes require context. They are review signals rather than automatic
  runtime conclusions.
- Keyboard/high-frequency actions normally remove travel and delay, but may
  preserve immediate causal state feedback.
- Reduced Motion is a behavior contract, not simply a shorter duration or a
  blanket removal of all feedback.
- Native haptics, web vibration, translucency preferences, and high-refresh
  behavior must be verified on a platform that actually supports them.

## Current conclusion

`missing-high-value`: none within the selected fusion boundary through the
reviewed remote head.

The cumulative state is now `selective_absorbed`, not an unqualified full-copy
claim. High-value behavior from the five pinned Skills and the new motion
opportunity gate is local; the opinionated library picker, Base UI-only
prescription, promotional text, aggressive review posture, host-policy
conflicts, decorative recipes, and technically overbroad claims remain
`intentionally-rejected`, `partial`, or `provenance-only`.

Current independent blind evidence is recorded in two cases:

- `emil-motion-ablation`: `design-craft` 99, focused Emil upstream 98,
  no-skill baseline 94.
- `emil-motion-planning-ablation`: `design-craft` 94, focused Emil upstream 93,
  no-skill baseline 86.
