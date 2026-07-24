# Blind comparative judgment
Judge only the supplied outputs. Do not infer which skill produced a label. Apply the machine-readable scorecard exactly, recompute each total from criterion points, and return only JSON matching the supplied schema.

## Task prompt

# Motion-system audit and implementation planning

Audit the following static project evidence and produce an implementation-ready
motion improvement roadmap. Do not edit files, create plans on disk, or claim
browser/device validation. Do not name, cite, or reveal any skill, repository,
author, or upstream source in the response; the output will be judged blind.

Product context:

- Surface: a calm desktop operations console used throughout the workday.
- Primary users: keyboard-heavy support and revenue operators.
- Motion purpose: preserve causality and state continuity without slowing task
  throughput.
- Existing authority: `DESIGN.md` requires crisp motion, existing semantic
  tokens, visible focus, and a Reduced Motion path that preserves feedback.
- Available evidence: only the snippets below. No runtime, computed-style,
  trace, screen recording, accessibility-tree, or user test was performed.

Current excerpts:

```css
/* src/styles/motion.css */
:root {
  --duration-fast: 160ms;
  --duration-panel: 240ms;
  --ease-responsive: cubic-bezier(0.23, 1, 0.32, 1);
}

.popover {
  transform-origin: center;
  transition: all 360ms ease-in;
}
```

```tsx
// src/components/CommandPalette.tsx
export function CommandPalette({ open }: { open: boolean }) {
  return (
    <div
      data-open={open}
      className="animate-[palette_420ms_ease-in_both]"
    >
      <SearchResults />
    </div>
  );
}
```

```css
/* src/components/toast.css */
@keyframes toast-enter {
  from { top: -24px; opacity: 0; }
  to { top: 0; opacity: 1; }
}

.toast {
  animation: toast-enter 500ms ease-in forwards;
}
```

```tsx
// src/components/SortableQueue.tsx
function onPointerMove(event: PointerEvent) {
  queueRef.current?.style.setProperty("--drag-y", `${event.clientY}px`);
}

function onPointerUp() {
  setDragging(false);
  animateTo(nearestSlot(currentY), { duration: 400 });
}
```

```css
/* src/components/Button.css - existing correct local precedent */
.button {
  transition: transform var(--duration-fast) var(--ease-responsive);
}

.button:active {
  transform: scale(0.98);
}

@media (prefers-reduced-motion: reduce) {
  .button { transition-duration: 80ms; }
}
```

Return:

1. A concise recon summary: stack signals, where motion lives, existing
   conventions, product personality, frequency map, and evidence level.
2. A vetted priority table with at most six findings and no unsupported runtime
   claims.
3. At most three self-contained implementation plans. Each plan must include
   exact file paths/current excerpts, target behavior, project conventions,
   ordered steps, hard boundaries, mechanical checks, runtime/feel checks,
   Reduced Motion behavior, and a source-drift stop condition.
4. A short recommended execution order and explicitly unverified states.

Stay within 180 lines. Prefer a small set of high-leverage plans over a padded
inventory.


## Human-readable scorecard

# Comparative scorecard

Generated from `scorecard.json`; do not edit by hand.

| Criterion | Weight | Full credit |
|---|---:|---|
| Evidence honesty and recon | 15 | Maps the static motion surface and labels every runtime or feel claim as unverified. |
| Project conventions | 10 | Reuses supplied tokens and the correct local precedent instead of inventing a parallel system. |
| Purpose and frequency | 10 | Prioritizes keyboard and high-frequency restraint plus causal feedback over decoration. |
| Technical accuracy | 15 | Diagnoses property cost, origin, interruption, pointer tracking, and primitive tradeoffs without framework myths. |
| Prioritization | 10 | Vets and ranks a small set by user impact, frequency, confidence, and implementation cost. |
| Plan self-containment | 20 | Plans include exact paths and excerpts, target behavior, steps, boundaries, and drift stop conditions. |
| Verification quality | 10 | Provides targeted mechanical and runtime feel checks without claiming those checks ran. |
| Accessibility and performance | 10 | Defines Reduced Motion behavior and measured performance checks while preserving useful feedback. |
| **Total** | **100** | |


## Machine-readable scorecard

```json
{
  "schema": "design-craft.comparative-scorecard.v1",
  "total": 100,
  "criteria": [
    {
      "id": "evidence_recon",
      "label": "Evidence honesty and recon",
      "weight": 15,
      "full_credit": "Maps the static motion surface and labels every runtime or feel claim as unverified."
    },
    {
      "id": "project_conventions",
      "label": "Project conventions",
      "weight": 10,
      "full_credit": "Reuses supplied tokens and the correct local precedent instead of inventing a parallel system."
    },
    {
      "id": "purpose_frequency",
      "label": "Purpose and frequency",
      "weight": 10,
      "full_credit": "Prioritizes keyboard and high-frequency restraint plus causal feedback over decoration."
    },
    {
      "id": "technical_accuracy",
      "label": "Technical accuracy",
      "weight": 15,
      "full_credit": "Diagnoses property cost, origin, interruption, pointer tracking, and primitive tradeoffs without framework myths."
    },
    {
      "id": "prioritization",
      "label": "Prioritization",
      "weight": 10,
      "full_credit": "Vets and ranks a small set by user impact, frequency, confidence, and implementation cost."
    },
    {
      "id": "plan_self_containment",
      "label": "Plan self-containment",
      "weight": 20,
      "full_credit": "Plans include exact paths and excerpts, target behavior, steps, boundaries, and drift stop conditions."
    },
    {
      "id": "verification_quality",
      "label": "Verification quality",
      "weight": 10,
      "full_credit": "Provides targeted mechanical and runtime feel checks without claiming those checks ran."
    },
    {
      "id": "accessibility_performance",
      "label": "Accessibility and performance",
      "weight": 10,
      "full_credit": "Defines Reduced Motion behavior and measured performance checks while preserving useful feedback."
    }
  ]
}
```

## Required judgment schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["results", "winner", "rationale"],
  "properties": {
    "results": {
      "type": "array",
      "minItems": 3,
      "maxItems": 3,
      "items": {
        "type": "object",
        "required": ["label", "criteria", "total", "summary"],
        "properties": {
          "label": {"enum": ["A", "B", "C"]},
          "criteria": {
            "type": "object",
            "required": [
              "evidence_recon",
              "project_conventions",
              "purpose_frequency",
              "technical_accuracy",
              "prioritization",
              "plan_self_containment",
              "verification_quality",
              "accessibility_performance"
            ],
            "additionalProperties": false,
            "properties": {
              "evidence_recon": {"type": "integer", "minimum": 0, "maximum": 15},
              "project_conventions": {"type": "integer", "minimum": 0, "maximum": 10},
              "purpose_frequency": {"type": "integer", "minimum": 0, "maximum": 10},
              "technical_accuracy": {"type": "integer", "minimum": 0, "maximum": 15},
              "prioritization": {"type": "integer", "minimum": 0, "maximum": 10},
              "plan_self_containment": {"type": "integer", "minimum": 0, "maximum": 20},
              "verification_quality": {"type": "integer", "minimum": 0, "maximum": 10},
              "accessibility_performance": {"type": "integer", "minimum": 0, "maximum": 10}
            }
          },
          "total": {"type": "integer", "minimum": 0, "maximum": 100},
          "summary": {"type": "string", "minLength": 20}
        },
        "additionalProperties": false
      }
    },
    "winner": {"enum": ["A", "B", "C"]},
    "rationale": {"type": "string", "minLength": 40}
  },
  "additionalProperties": false
}
```

## Output A

One-sentence diagnosis: the snippets show a useful motion-token seed and one good button precedent, but several high-frequency/causal interactions bypass those conventions with slow `ease-in`, hard-coded keyframes, broad property ownership, layout-position animation, and incomplete Reduced Motion evidence.

## 1. Recon summary

- **Stack signals:** React/TSX components, CSS custom properties, global/component CSS, Tailwind-style arbitrary animation utility, PointerEvent-driven drag, and an unknown `animateTo` helper.
- **Where motion lives:** `src/styles/motion.css`, component CSS keyframes, TSX utility classes, and pointer gesture handlers.
- **Existing conventions:** semantic tokens exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`; `Button.css` is the correct local precedent: transform-only transition, tokenized timing/easing, Reduced Motion duration shortened to `80ms`.
- **Product personality:** calm desktop operations console; motion should be crisp, causal, low-latency, and non-decorative.
- **Frequency map:**
  - Very high: command palette, keyboard-triggered overlays, button press feedback.
  - High/medium: sortable queue drag/reorder.
  - Medium: popovers.
  - Occasional: toasts.
- **Evidence level:** static snippets only. No runtime feel, computed styles, frame traces, accessibility tree, browser/device validation, or actual package-script discovery.

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
| --- | --- | --- | --- | --- |
| P1 | `animate-[palette_420ms_ease-in_both]` | `src/components/CommandPalette.tsx` | High-frequency keyboard surface uses a hard-coded 420ms `ease-in` keyframe; this likely delays perceived response and bypasses tokens. Runtime feel unverified. | Replace with tokenized opacity/transform transition using `--duration-fast` + `--ease-responsive`; Reduced Motion: `80ms`, no travel. |
| P1 | `animateTo(nearestSlot(currentY), { duration: 400 })` | `src/components/SortableQueue.tsx` | Direct manipulation settle is shown as fixed-duration with no visible velocity handoff, interruption-from-presentation-value, or Reduced Motion branch in the excerpt. | Preserve `nearestSlot` semantics, but measure release velocity in CSS px/s and pass it into an interruptible settle if the existing API supports it. |
| P1 | Reduced Motion only shown in `Button.css` | Multiple excerpts | `popover`, command palette, toast, and queue snippets show meaningful movement without a visible Reduced Motion path, conflicting with the stated authority within supplied evidence. | Add per-surface Reduced Motion behavior: remove/reduce spatial travel while preserving opacity/color/state feedback. |
| P2 | `transition: all 360ms ease-in` | `src/styles/motion.css` | Popover owns all transitionable properties, runs longer than existing tokens, and uses `ease-in`. `transform-origin: center` may be wrong for anchored popovers, but anchoring is unverified. | Restrict to `opacity, transform`; use token duration/easing; expose trigger-relative origin variable with safe fallback. |
| P2 | `top` keyframe, `500ms ease-in` | `src/components/toast.css` | Toast entrance animates a layout-position property and uses slow `ease-in`; static evidence cannot prove jank, but this is a clear performance/feel risk. | Animate `transform` + `opacity`; use `--duration-panel` or shorter token; add Reduced Motion opacity-only variant. |
| P3 | Mixed hard-coded durations: `360/420/500/400ms` | Supplied snippets | Motion vocabulary is fragmented despite available semantic tokens. | Normalize to existing tokens first; introduce new tokens only after repeated need is proven. |

## 3. Implementation plans

### Plan 1 — Make command palette motion immediate, tokenized, and Reduced Motion-safe

**Current excerpt**

`src/components/CommandPalette.tsx`

```tsx
export function CommandPalette({ open }: { open: boolean }) {
  return (
    <div
      data-open={open}
      className="animate-[palette_420ms_ease-in_both]"
    >
      <SearchResults />
    </div>
  );
}
```

**Target behavior**

- Opening/closing feels immediate for keyboard use.
- Motion uses opacity plus very small vertical transform only.
- Duration/easing use existing conventions: `--duration-fast`, `--ease-responsive`.
- Reduced Motion keeps state feedback but removes travel and shortens to `80ms`.
- No keyframe restart dependency for repeated open/close.

**Project conventions**

- Follow `Button.css`: transform-only transition, semantic duration/easing, `prefers-reduced-motion` duration of `80ms`.
- Do not add decorative bounce or cinematic timing.

**Ordered steps**

1. Confirm whether the `palette` keyframe exists elsewhere and whether the palette remains mounted when `open=false`.
2. Replace the arbitrary animation class with a state-driven transition.
3. If Tailwind data variants and `motion-reduce` utilities are available, use tokenized utilities directly, e.g. conceptually:
   ```tsx
   className="
     transition-[opacity,transform]
     duration-[var(--duration-fast)]
     ease-[var(--ease-responsive)]
     data-[open=true]:opacity-100 data-[open=true]:translate-y-0
     data-[open=false]:opacity-0 data-[open=false]:-translate-y-1
     motion-reduce:duration-[80ms] motion-reduce:translate-y-0
   "
   ```
4. If those utilities are not supported, move the same behavior into the nearest existing command-palette stylesheet; do not place component-specific selectors in global CSS unless that is already the project convention.
5. Remove or stop referencing the old `palette_420ms_ease-in_both` animation only after confirming no other component depends on it.

**Hard boundaries**

- Do not change search behavior, focus behavior, result rendering, keyboard shortcuts, mount/unmount semantics, or data fetching.
- Do not add a motion dependency.
- Do not introduce new duration/easing tokens unless existing tokens cannot express the behavior.

**Mechanical checks**

- Run the project’s existing type-check/lint/build gates after discovering package scripts.
- If no such scripts exist, record that rather than inventing script names.
- Search for remaining `palette_420ms` / `animate-[palette` references.

**Runtime/feel checks to perform later, not claimed here**

- Open/close repeatedly via keyboard shortcut.
- Type immediately after opening; palette should not feel delayed.
- Interrupt open with close and close with open; no visual reset/jump.
- Verify closed state does not leave hidden interactive content focusable, if the component remains mounted.

**Reduced Motion behavior**

- Keep opacity/state feedback.
- Remove vertical travel.
- Use `80ms` duration.

**Source-drift stop condition**

- Stop before editing if `CommandPalette.tsx` no longer contains the supplied class, if `open` no longer maps to visual state, or if the project has a newer command-palette motion abstraction.

---

### Plan 2 — Normalize popover and toast motion to transform/opacity plus semantic tokens

**Current excerpts**

`src/styles/motion.css`

```css
:root {
  --duration-fast: 160ms;
  --duration-panel: 240ms;
  --ease-responsive: cubic-bezier(0.23, 1, 0.32, 1);
}

.popover {
  transform-origin: center;
  transition: all 360ms ease-in;
}
```

`src/components/toast.css`

```css
@keyframes toast-enter {
  from { top: -24px; opacity: 0; }
  to { top: 0; opacity: 1; }
}

.toast {
  animation: toast-enter 500ms ease-in forwards;
}
```

**Target behavior**

- Popovers respond crisply without owning unrelated properties.
- Toasts enter with compositor-friendly movement and opacity, not animated `top`.
- Both use existing semantic tokens and a Reduced Motion path.
- Popover origin can be trigger-relative when anchored, while preserving a safe fallback for genuinely centered overlays.

**Project conventions**

- Prefer `transform` and `opacity`.
- Use `--duration-fast` for small overlays/popovers and `--duration-panel` for larger transient panels/toasts.
- Use `--ease-responsive`, which is already an ease-out-like responsive curve.
- Mirror the local Reduced Motion precedent of `80ms`.

**Ordered steps**

1. In `src/styles/motion.css`, replace broad popover transition with explicit property ownership:
   ```css
   .popover {
     transform-origin: var(--popover-transform-origin, center);
     transition-property: opacity, transform;
     transition-duration: var(--duration-fast);
     transition-timing-function: var(--ease-responsive);
   }
   ```
2. Before changing call sites, inspect actual popover placement:
   - If popovers are anchored to triggers, set `--popover-transform-origin` at the placement layer.
   - If the surface is truly centered, keep the `center` fallback.
3. Add a Reduced Motion branch:
   ```css
   @media (prefers-reduced-motion: reduce) {
     .popover { transition-duration: 80ms; }
   }
   ```
4. In `src/components/toast.css`, replace `top` animation with transform/opacity:
   ```css
   @keyframes toast-enter {
     from { transform: translateY(-8px); opacity: 0; }
     to { transform: translateY(0); opacity: 1; }
   }

   .toast {
     animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;
   }
   ```
5. Add Reduced Motion toast behavior:
   ```css
   @keyframes toast-enter-reduced {
     from { opacity: 0; }
     to { opacity: 1; }
   }

   @media (prefers-reduced-motion: reduce) {
     .toast {
       animation-name: toast-enter-reduced;
       animation-duration: 80ms;
     }
   }
   ```

**Hard boundaries**

- Do not change toast stacking, position, dismiss timing, z-index, live-region behavior, or message lifecycle.
- Do not change popover open/close semantics, focus behavior, or placement logic except for transform-origin if the placement layer already owns that data.
- Do not use `will-change` unless later measurement proves it helps.

**Mechanical checks**

- Run existing lint/build/style checks.
- Search for `transition: all`, `toast-enter`, and `.popover` references to ensure no dependent behavior expects `top` animation or broad transitions.
- Confirm no other selector depends on `.toast` animated `top` values.

**Runtime/feel checks to perform later, not claimed here**

- Open popovers from each supported placement; origin should match trigger direction where applicable.
- Trigger multiple toasts; stacking should remain stable.
- Interrupt/replace toasts if the product supports that.
- Verify no layout jump when toast enters.

**Reduced Motion behavior**

- Popover: shortened transition, no added travel beyond existing state transform.
- Toast: opacity-only `80ms` feedback; no vertical movement.

**Source-drift stop condition**

- Stop if token names or values have changed, `.popover` is no longer the active selector, toast positioning no longer uses `top`, or toast entry is already handled by a different animation system.

---

### Plan 3 — Upgrade sortable queue drag settle for direct manipulation continuity

**Current excerpt**

`src/components/SortableQueue.tsx`

```tsx
function onPointerMove(event: PointerEvent) {
  queueRef.current?.style.setProperty("--drag-y", `${event.clientY}px`);
}

function onPointerUp() {
  setDragging(false);
  animateTo(nearestSlot(currentY), { duration: 400 });
}
```

**Target behavior**

- Dragged item tracks the pointer 1:1 in a clear coordinate space.
- Release starts from the current on-screen value.
- Release velocity is measured in CSS px/s and handed into the settle animation.
- Existing `nearestSlot(currentY)` target-selection semantics are preserved unless product authority explicitly approves momentum-based target selection.
- Reduced Motion preserves direct manipulation but removes overshoot/elastic travel.

**Project conventions**

- Prefer transform ownership over layout movement.
- Keep motion crisp and non-playful for operations work.
- Use existing animation helper if it supports current value + velocity; do not add a dependency without approval.

**Ordered steps**

1. Inspect surrounding `pointerdown`, queue item CSS, and `animateTo` signature before editing.
2. Ensure drag state stores:
   - `pointerId`
   - grab offset from pointer to item
   - container/item bounds used for local coordinates
   - recent samples `{ y: CSS px, t: performance.now() }`
3. On drag start, use pointer capture if not already present.
4. On pointer move, convert `event.clientY` to local drag translation instead of storing absolute viewport Y directly.
5. Scope `--drag-y` to the dragged item or a dedicated transform wrapper, not a broad queue parent, unless current CSS proves parent-scoped variable updates are intentional and cheap.
6. Batch visual writes with `requestAnimationFrame` if pointer events can arrive faster than paint.
7. On pointer up:
   - release pointer capture;
   - compute release velocity from recent samples in CSS px/s;
   - read or preserve the current presentation value;
   - keep `const target = nearestSlot(currentY)` unless momentum targeting is separately authorized;
   - call the existing animation primitive with initial velocity if supported.
8. If `animateTo` only accepts fixed duration and cannot preserve velocity/current value, stop and request an animation-primitive decision instead of silently adding a dependency.
9. If momentum-based target selection is later authorized, use a bounded projected endpoint only for choosing the target; still keep velocity handoff as a separate step.

**Hard boundaries**

- Do not change reorder data semantics.
- Do not change `nearestSlot` behavior without explicit approval.
- Do not alter keyboard reorder behavior, selection state, persistence, or queue filtering.
- Do not add spring/gesture dependencies unless existing primitives cannot meet the requirements and the change is approved.

**Mechanical checks**

- Run existing type-check/lint/build gates.
- Add or update focused tests for `nearestSlot` only if existing tests already cover this area; do not invent product semantics.
- Search for all writers of `--drag-y` and all callers/signatures of `animateTo`.

**Runtime/feel checks to perform later, not claimed here**

- Drag slowly, quickly, and outside the original item bounds.
- Release while item is moving; settle should continue from current position without a jump.
- Interrupt a settling item by grabbing it again.
- Reorder near slot boundaries.
- Test under a large queue if that state exists, because parent-scoped CSS variable updates may affect style recalculation.

**Reduced Motion behavior**

- Keep direct 1:1 drag tracking; this is causality, not decorative motion.
- On release, use no overshoot, no elastic bounce, and a short settle or immediate snap with clear selected/drop state feedback.
- Preserve non-motion confirmation such as final position, highlight, or announcement if already present.

**Source-drift stop condition**

- Stop if `onPointerMove`, `onPointerUp`, `--drag-y`, `nearestSlot`, or `animateTo` no longer match the supplied excerpts, or if another gesture system already owns velocity/interruption.

## 4. Recommended execution order

1. **Plan 1: Command palette** — highest-frequency keyboard surface and likely low change size.
2. **Plan 2: Popover/toast CSS** — establishes tokenized transient-motion hygiene and Reduced Motion coverage.
3. **Plan 3: Sortable queue** — high impact but requires API and runtime feel decisions; do after source/API preflight.

## Explicitly unverified states

- Actual package manager, scripts, build gates, and CSS pipeline.
- Whether `palette` keyframes are defined or reused elsewhere.
- Whether command palette remains mounted while closed.
- Actual computed styles, frame rate, compositing behavior, or layout cost.
- Whether `.popover` is anchored, centered, or placement-aware.
- Toast stacking/lifecycle/live-region behavior.
- Pointer capture, grab offset, velocity tracking, and transform ownership outside the shown queue excerpt.
- `animateTo` API capabilities.
- Real keyboard throughput, interruption feel, Reduced Motion behavior, browser/device behavior, and accessibility-tree output.


## Output B

## 1. Recon summary

- **Stack signals:** TSX component files, CSS component files, global CSS tokens, utility-style arbitrary animation syntax, imperative pointer motion via JS.
- **Where motion lives:**
  - Global token layer: `src/styles/motion.css`
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`
  - Component markup classes: `src/components/CommandPalette.tsx`
  - JS gesture/reorder path: `src/components/SortableQueue.tsx`
- **Existing conventions:**
  - Semantic durations: `--duration-fast: 160ms`, `--duration-panel: 240ms`
  - Semantic easing: `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
  - Reduced Motion precedent: shorten duration to `80ms` while preserving feedback
  - Correct local precedent: button uses `transform`, semantic tokens, and Reduced Motion override
- **Product personality:** calm, crisp, operational, throughput-oriented; motion should clarify causality and state continuity, not create theatrical delay.
- **Frequency map:**
  - Very high: buttons, command palette, popovers
  - High/medium: toasts and transient feedback
  - Lower frequency but high sensitivity: sortable queue drag/release
- **Evidence level:** static excerpt audit only. No runtime behavior, computed styles, frame timing, browser validation, accessibility tree, screen recording, or user testing was performed.

---

## 2. Priority table

| Priority | Finding | Evidence | Risk | Roadmap owner |
|---:|---|---|---|---|
| P0 | Motion contract is inconsistent across surfaces | Tokens exist, but popover/palette/toast/queue use hard-coded durations/easings | Operators experience uneven timing and unclear state continuity | Plan 1 |
| P0 | `transition: all` on popover is too broad | `.popover { transition: all 360ms ease-in; }` | Unintended properties may animate; duration/easing conflict with design authority | Plan 1 |
| P0 | Command palette uses long arbitrary animation | `animate-[palette_420ms_ease-in_both]` | High-frequency keyboard surface may feel delayed; no visible Reduced Motion path in excerpt | Plan 2 |
| P1 | Toast animates layout property and is slow | `top` from `-24px` to `0`, `500ms ease-in` | Layout-affecting motion and long feedback delay are poor fit for operational alerts | Plan 2 |
| P1 | Sortable release animation is hard-coded and long | `animateTo(..., { duration: 400 })` | Drag release may feel detached from direct manipulation; no Reduced Motion path in excerpt | Plan 3 |
| P2 | Reduced Motion is implemented locally, not shown as system-wide | Button has media query; others do not in excerpt | Feedback may be preserved inconsistently for motion-sensitive users | Plans 1–3 |

---

## 3. Implementation plans

### Plan 1 — Normalize global motion contract and popover behavior

**Current file/excerpt**

`src/styles/motion.css`

```css
:root {
  --duration-fast: 160ms;
  --duration-panel: 240ms;
  --ease-responsive: cubic-bezier(0.23, 1, 0.32, 1);
}

.popover {
  transform-origin: center;
  transition: all 360ms ease-in;
}
```

**Target behavior**

- Popovers use semantic duration/easing.
- Only compositable visual properties transition, primarily `opacity` and `transform`.
- Popover timing matches calm operational surfaces: quick enough for repeated use, clear enough to preserve causality.
- Reduced Motion preserves open/close feedback with a shorter duration, following the button precedent.

**Project conventions to preserve**

- Use existing semantic tokens before adding new ones.
- Keep `--duration-fast`, `--duration-panel`, and `--ease-responsive` as the authority.
- Follow the existing Reduced Motion precedent of `80ms`.
- Keep focus visibility separate from motion; do not hide or delay focus indicators.

**Ordered implementation steps**

1. Replace broad popover transition:
   - From: `transition: all 360ms ease-in;`
   - To: transition only `opacity` and `transform`.
2. Use `var(--duration-panel)` for normal popover open/close.
3. Use `var(--ease-responsive)` instead of `ease-in`.
4. Add a Reduced Motion override for `.popover` using `80ms`.
5. If existing open/closed state selectors are present elsewhere, wire the transition to those selectors without changing state semantics.
6. If no state selectors exist, only change the transition declaration; do not invent visibility or mount behavior from this excerpt.

**Suggested shape**

```css
.popover {
  transform-origin: center;
  transition:
    opacity var(--duration-panel) var(--ease-responsive),
    transform var(--duration-panel) var(--ease-responsive);
}

@media (prefers-reduced-motion: reduce) {
  .popover {
    transition-duration: 80ms;
  }
}
```

**Hard boundaries**

- Do not use `transition: all`.
- Do not add spring libraries or new dependencies.
- Do not alter popover focus management from this motion pass unless existing code requires it.
- Do not change layout, positioning, portal behavior, or dismissal behavior based only on this excerpt.

**Mechanical checks**

- Search for remaining `transition: all`.
- Search for hard-coded `360ms`, `420ms`, `500ms`, `400` motion durations after subsequent plans.
- Confirm CSS parses and selectors remain scoped as intended.
- Run the project’s closest style/type/build check after implementation.

**Runtime/feel checks to perform later, not performed now**

- Open/close popover repeatedly with keyboard and pointer.
- Confirm no delayed focus visibility.
- Confirm popover feels crisp rather than slow or theatrical.
- Confirm Reduced Motion still communicates state change.

**Reduced Motion behavior**

- Keep feedback.
- Shorten transition to `80ms`.
- Avoid replacing state change with no visual indication unless the product explicitly chooses that.

**Source-drift stop condition**

Stop before editing if `src/styles/motion.css` no longer contains the shown `.popover` rule, if motion tokens have been renamed, or if popover motion is now defined in a different component/style layer.

---

### Plan 2 — Replace long arbitrary entry animations for command palette and toast

**Current files/excerpts**

`src/components/CommandPalette.tsx`

```tsx
export function CommandPalette({ open }: { open: boolean }) {
  return (
    <div
      data-open={open}
      className="animate-[palette_420ms_ease-in_both]"
    >
      <SearchResults />
    </div>
  );
}
```

`src/components/toast.css`

```css
@keyframes toast-enter {
  from { top: -24px; opacity: 0; }
  to { top: 0; opacity: 1; }
}

.toast {
  animation: toast-enter 500ms ease-in forwards;
}
```

**Target behavior**

- Command palette opens with a short, calm transform/opacity transition.
- Toast enters using `transform` and `opacity`, not `top`.
- Both use semantic durations/easing.
- Both provide a Reduced Motion path that preserves feedback.
- Command palette avoids long arbitrary animation syntax for a high-frequency keyboard surface.

**Project conventions to preserve**

- Use existing semantic tokens.
- Use transform/opacity as the preferred motion properties.
- Use `80ms` in Reduced Motion, matching the existing button precedent.
- Keep the command palette optimized for keyboard-heavy repeated use.

**Ordered implementation steps**

1. Replace the command palette arbitrary animation class with a semantic class name.
   - Example target class: `commandPaletteMotion`
   - Keep `data-open={open}` because it is already present and useful.
2. Define command palette motion in the appropriate stylesheet already used by the component, or create a colocated component stylesheet only if that is the existing local convention.
3. Use `opacity` and a small `transform` delta for palette entry/exit.
   - Suggested normal duration: `var(--duration-panel)`.
   - Suggested easing: `var(--ease-responsive)`.
4. Do not change mount/unmount lifecycle unless existing code already supports exit animation.
5. Update toast keyframes:
   - Replace `top` movement with `transform: translateY(...)`.
   - Use `var(--duration-fast)` or `var(--duration-panel)` depending on toast importance.
   - For routine status feedback, prefer `var(--duration-fast)`.
6. Add Reduced Motion overrides for both command palette and toast.
7. If the command palette has existing close animation elsewhere, consolidate rather than duplicate.

**Suggested command palette shape**

```tsx
<div
  data-open={open}
  className="commandPaletteMotion"
>
  <SearchResults />
</div>
```

```css
.commandPaletteMotion {
  opacity: 0;
  transform: translateY(-4px) scale(0.99);
  transition:
    opacity var(--duration-panel) var(--ease-responsive),
    transform var(--duration-panel) var(--ease-responsive);
}

.commandPaletteMotion[data-open="true"] {
  opacity: 1;
  transform: translateY(0) scale(1);
}

@media (prefers-reduced-motion: reduce) {
  .commandPaletteMotion {
    transition-duration: 80ms;
    transform: none;
  }
}
```

**Suggested toast shape**

```css
@keyframes toast-enter {
  from {
    transform: translateY(-8px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.toast {
  animation: toast-enter var(--duration-fast) var(--ease-responsive) forwards;
}

@media (prefers-reduced-motion: reduce) {
  .toast {
    animation-duration: 80ms;
  }
}
```

**Hard boundaries**

- Do not claim the current command palette animation reruns incorrectly without runtime evidence.
- Do not change search behavior, focus trap behavior, result rendering, or keyboard shortcuts in this motion pass.
- Do not move toast position logic unless required to remove `top` from the animation.
- Do not remove feedback entirely in Reduced Motion.
- Do not introduce new global animation names that collide with existing names.

**Mechanical checks**

- Search for `animate-[palette_420ms_ease-in_both]`.
- Search for `@keyframes toast-enter`.
- Confirm no `top` animation remains in toast enter motion.
- Confirm no new hard-coded `420ms` or `500ms` remains for these paths.
- Run type/style/build checks available in the project.

**Runtime/feel checks to perform later, not performed now**

- Open command palette repeatedly using keyboard.
- Verify search input focus is visible immediately.
- Confirm palette does not feel delayed before typing.
- Trigger multiple toasts and verify feedback is noticeable but not distracting.
- Test Reduced Motion preference and confirm brief feedback remains.

**Reduced Motion behavior**

- Command palette: shorten to `80ms`; remove scale/translation if needed, keeping opacity feedback.
- Toast: shorten to `80ms`; prefer opacity-only or very small transform.
- Preserve causal feedback for open, close, and notification arrival.

**Source-drift stop condition**

Stop before editing if the command palette already imports a different motion stylesheet, if the arbitrary animation has moved into a shared animation system, or if `toast-enter` is no longer the active toast entry animation.

---

### Plan 3 — Make sortable queue drag/release motion direct and preference-aware

**Current file/excerpt**

`src/components/SortableQueue.tsx`

```tsx
function onPointerMove(event: PointerEvent) {
  queueRef.current?.style.setProperty("--drag-y", `${event.clientY}px`);
}

function onPointerUp() {
  setDragging(false);
  animateTo(nearestSlot(currentY), { duration: 400 });
}
```

**Target behavior**

- During drag: movement remains direct and immediate.
- On release: item settles to nearest slot with crisp, short motion.
- Duration uses the same semantic timing contract as the rest of the interface.
- Reduced Motion shortens or minimizes the release animation while preserving state confirmation.
- Pointer movement avoids unnecessary per-event work beyond updating the active transform input.

**Project conventions to preserve**

- Use transform-driven movement if existing CSS maps `--drag-y` into transform.
- Use semantic timing values aligned with `--duration-fast` / `--duration-panel`.
- Keep Reduced Motion feedback at approximately `80ms`.
- Do not change sorting rules or slot calculation during a motion-system pass.

**Ordered implementation steps**

1. Inspect the existing CSS that consumes `--drag-y`.
2. If `--drag-y` currently drives `transform`, keep that path.
3. If it drives layout properties, move the visual drag representation to `transform`.
4. Replace hard-coded release duration:
   - From: `animateTo(nearestSlot(currentY), { duration: 400 });`
   - To: a named duration value derived from the motion contract.
5. Prefer a shorter release duration:
   - Normal: `160ms` for small slot snaps, or `240ms` if the queue item can travel farther.
   - Reduced Motion: `80ms`.
6. Add or reuse a motion preference helper only if one already exists; otherwise keep a small local `matchMedia('(prefers-reduced-motion: reduce)')` check.
7. Consider batching pointer-move style writes with `requestAnimationFrame` only if profiling later shows event pressure; do not add complexity without evidence.

**Suggested implementation shape**

```tsx
const prefersReducedMotion =
  window.matchMedia?.("(prefers-reduced-motion: reduce)").matches ?? false;

const releaseDuration = prefersReducedMotion ? 80 : 160;

function onPointerUp() {
  setDragging(false);
  animateTo(nearestSlot(currentY), { duration: releaseDuration });
}
```

If broader queue travel needs more continuity:

```tsx
const releaseDuration = prefersReducedMotion ? 80 : 240;
```

**Hard boundaries**

- Do not change `nearestSlot(currentY)` behavior without separate interaction tests.
- Do not change queue ordering semantics.
- Do not introduce inertia, overshoot, bounce, or decorative physics for this operational surface.
- Do not claim current pointer movement is janky without profiling.
- Do not remove direct manipulation feedback in Reduced Motion.

**Mechanical checks**

- Search for `animateTo(` and other hard-coded drag durations.
- Confirm TypeScript accepts the motion preference code in the component environment.
- Confirm server-side or non-browser rendering paths are guarded if applicable.
- Confirm no layout property is animated for the dragged visual element.
- Run type/build checks after implementation.

**Runtime/feel checks to perform later, not performed now**

- Drag short and long distances.
- Release near and between slots.
- Confirm release feels attached to the pointer, not delayed.
- Confirm no bounce/overshoot unless already part of the product language.
- Confirm Reduced Motion still shows the item reaching the final slot.

**Reduced Motion behavior**

- Direct drag remains direct.
- Release snap shortens to `80ms`.
- Avoid added scale, bounce, or secondary flourish.
- Preserve final-position feedback.

**Source-drift stop condition**

Stop before editing if `animateTo` has been replaced, if `--drag-y` no longer controls drag motion, or if queue motion has moved into a shared gesture utility.

---

## 4. Recommended execution order

1. **Plan 1 first:** establish the tokenized motion contract and remove the broadest unsafe transition.
2. **Plan 2 second:** fix the highest-frequency keyboard and feedback surfaces.
3. **Plan 3 third:** tune the gesture path after the shared timing direction is clear.

Explicitly defer decorative refinements until the core contract is consistent.

---

## Explicitly unverified states

- Actual computed CSS values.
- Whether command palette mounts/unmounts or remains in DOM.
- Whether `data-open` currently controls any styles elsewhere.
- Whether toast position depends on `top` outside the animation.
- Whether `--drag-y` is consumed by `transform`, layout, or another property.
- Actual frame rate, layout cost, or input latency.
- Keyboard focus order and accessibility tree.
- Existing test/build commands.
- Browser/device behavior.
- User-tested feel or operator throughput impact.


## Output C

## 1. Recon summary

- **Stack signals**: CSS plus TSX components; motion appears in global CSS tokens, component CSS, utility-style animation classes, and pointer/JS-driven gesture code.
- **Where motion lives**:
  - Global tokens: `src/styles/motion.css`
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`
  - Inline utility animation: `src/components/CommandPalette.tsx`
  - Gesture handler / imperative animation: `src/components/SortableQueue.tsx`
- **Existing conventions**:
  - Semantic duration/easing tokens already exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
  - Correct local precedent exists in `src/components/Button.css`: transform-only transition, tokenized timing, and a Reduced Motion path that keeps feedback at `80ms`.
- **Product personality**: calm, crisp, operator-focused desktop console. Motion should be fast, causal, non-decorative, and should not tax repeated keyboard workflows.
- **Frequency map from evidence only**:
  - **Very high frequency**: command palette, button press feedback, sortable queue dragging.
  - **Medium / repeated**: popovers.
  - **Occasional but important**: toasts.
- **Evidence level**: static code excerpts only. No runtime timing, computed styles, screen recording, browser validation, device validation, accessibility tree, or user testing was performed.

---

## 2. Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose / frequency | `src/components/CommandPalette.tsx` | Command palette uses `animate-[palette_420ms_ease-in_both]`. For a keyboard-heavy, high-frequency surface, this is likely too slow and starts with the least responsive easing. | Remove or drastically shorten palette motion; prefer instant open/close or ≤80–120ms opacity-only feedback with Reduced Motion parity. |
| 2 | HIGH | Performance / easing / cohesion | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in;`. This animates unintended properties, exceeds crisp popover timing, and starts slowly. | Replace with explicit `transform`/`opacity` transitions using existing semantic tokens and responsive easing. |
| 3 | HIGH | Performance / accessibility | `src/components/toast.css` | Toast entrance animates `top` over `500ms ease-in` via keyframes. `top` is layout-affecting, duration is long for operational feedback, and no Reduced Motion path is shown. | Move toast entrance to `transform` + `opacity`, shorten to tokenized timing, and add Reduced Motion that preserves opacity feedback without positional travel. |
| 4 | MEDIUM | Gesture / interruptibility | `src/components/SortableQueue.tsx` | Pointer move writes `--drag-y` to the queue parent, and release uses fixed `duration: 400`. Static evidence does not show velocity carryover, direct element transform, or Reduced Motion branching. | Drive the dragged item directly with `transform`, use velocity-aware/spring-like settle behavior where available, and reduce motion to immediate/short settle feedback. |
| 5 | MEDIUM | Accessibility / cohesion | Multiple excerpts | Reduced Motion is present only in the button precedent. Palette, popover, toast, and queue excerpts do not show equivalent handling. | Apply the same Reduced Motion convention broadly: preserve state feedback, remove or shorten movement. |
| 6 | MEDIUM | Tokens / maintainability | `CommandPalette.tsx`, `toast.css`, `motion.css` | Motion values are split across hardcoded utility animation, hardcoded CSS animation, and semantic tokens. This weakens consistency. | Consolidate around the existing semantic tokens; add only narrowly named tokens if needed. |

---

## 3. Implementation-ready plans

### Plan 1 — Make command palette immediate and non-decorative

**Files / current excerpts**

`src/components/CommandPalette.tsx`

```tsx
export function CommandPalette({ open }: { open: boolean }) {
  return (
    <div
      data-open={open}
      className="animate-[palette_420ms_ease-in_both]"
    >
      <SearchResults />
    </div>
  );
}
```

**Target behavior**

- Command palette should feel instant for keyboard-heavy operators.
- Remove the `420ms ease-in` animation.
- Preferred target: no entrance/exit animation on the palette container.
- Acceptable fallback if visual continuity is required by nearby code: opacity-only feedback at `80ms–120ms`, no scale/slide, no `ease-in`.
- Reduced Motion should behave the same or shorter; it must not remove state feedback entirely if opacity feedback is retained.

**Project conventions**

- Use existing semantic motion tokens from `src/styles/motion.css`:
  - `--duration-fast: 160ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Follow the precedent in `src/components/Button.css`:
  - transform-specific transition
  - tokenized duration/easing
  - `@media (prefers-reduced-motion: reduce)` with `80ms`

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, remove `className="animate-[palette_420ms_ease-in_both]"` from the palette container.
2. If the element still needs styling hooks, keep `data-open={open}` but do not attach a keyframe animation.
3. If removal creates an abrupt visual discontinuity in nearby styles, add a local class such as `commandPalette` and implement opacity-only CSS:
   ```css
   .commandPalette {
     transition: opacity 120ms var(--ease-responsive);
   }

   .commandPalette[data-open="false"] {
     opacity: 0;
   }

   .commandPalette[data-open="true"] {
     opacity: 1;
   }

   @media (prefers-reduced-motion: reduce) {
     .commandPalette {
       transition-duration: 80ms;
     }
   }
   ```
4. Do not add translation, scale, blur, stagger, or delayed child animations.

**Hard boundaries**

- Do not change `SearchResults`.
- Do not change command search behavior, focus behavior, keyboard shortcuts, or open-state ownership.
- Do not introduce a motion library.
- Do not add new global tokens unless existing tokens cannot be imported or referenced from the component styling system.

**Mechanical checks**

- Search for the removed arbitrary animation string and confirm it no longer appears:
  - `animate-[palette_420ms_ease-in_both]`
- Search for any replacement `ease-in` on the command palette; none should be introduced.
- Run the project’s existing lint/typecheck/build commands if available. Do not invent new tooling.

**Runtime / feel checks for executor**

- Open and close the palette repeatedly by keyboard.
- Confirm it does not feel delayed before content becomes usable.
- In slow-motion inspection, confirm there is no visible slide/scale flourish.
- Toggle Reduced Motion and confirm feedback remains at least as immediate.

**Reduced Motion behavior**

- Same as default if animation is removed.
- If opacity feedback is retained, duration should be `80ms`.

**Source-drift stop condition**

- Stop if the command palette no longer contains the shown `data-open={open}` container or if the animation has already been replaced by a different state-management/styling pattern.

---

### Plan 2 — Normalize popover motion to explicit tokenized properties

**Files / current excerpts**

`src/styles/motion.css`

```css
:root {
  --duration-fast: 160ms;
  --duration-panel: 240ms;
  --ease-responsive: cubic-bezier(0.23, 1, 0.32, 1);
}

.popover {
  transform-origin: center;
  transition: all 360ms ease-in;
}
```

**Target behavior**

- Popovers should appear responsive and anchored, not delayed.
- Replace `transition: all` with explicit properties.
- Replace `360ms ease-in` with existing semantic timing.
- Use a trigger-aware transform origin if the component system exposes one; otherwise avoid asserting a custom origin without evidence.
- Add Reduced Motion duration consistent with the button precedent.

**Project conventions**

- Existing token to reuse:
  ```css
  --duration-fast: 160ms;
  --duration-panel: 240ms;
  --ease-responsive: cubic-bezier(0.23, 1, 0.32, 1);
  ```
- Existing correct precedent:
  ```css
  .button {
    transition: transform var(--duration-fast) var(--ease-responsive);
  }

  @media (prefers-reduced-motion: reduce) {
    .button { transition-duration: 80ms; }
  }
  ```

**Ordered steps**

1. In `src/styles/motion.css`, change `.popover` transition from:
   ```css
   transition: all 360ms ease-in;
   ```
   to:
   ```css
   transition:
     transform var(--duration-fast) var(--ease-responsive),
     opacity var(--duration-fast) var(--ease-responsive);
   ```
2. Remove `ease-in`; do not replace it with bare `ease`.
3. Review whether the popover implementation exposes a trigger-origin CSS variable. If it already exists in local code, use it:
   ```css
   transform-origin: var(--popover-transform-origin);
   ```
   If no such variable exists, keep the current origin temporarily and do not invent one.
4. Add Reduced Motion:
   ```css
   @media (prefers-reduced-motion: reduce) {
     .popover {
       transition-duration: 80ms;
     }
   }
   ```
5. Ensure no layout properties are included in the transition list.

**Hard boundaries**

- Do not change markup or popover positioning logic.
- Do not alter modal behavior; centered origins can be correct for modals.
- Do not add broad selectors that affect unrelated overlays.
- Do not introduce `transition: all` elsewhere.

**Mechanical checks**

- Confirm `src/styles/motion.css` no longer contains `.popover { ... transition: all`.
- Confirm `.popover` no longer contains `ease-in`.
- Confirm only `transform` and `opacity` are transitioned.
- Run existing CSS lint/build checks if available.

**Runtime / feel checks for executor**

- Open/close a popover from its trigger.
- Confirm it starts promptly rather than easing in slowly.
- In slow-motion inspection, confirm no unrelated property such as size, position, or color is accidentally animated.
- Toggle Reduced Motion and confirm movement is shortened while state feedback remains visible.

**Reduced Motion behavior**

- Keep feedback.
- Shorten transition duration to `80ms`.
- Do not set `transition: none` unless a specific accessibility issue is discovered.

**Source-drift stop condition**

- Stop if `.popover` is no longer defined in `src/styles/motion.css`, or if popover motion has moved to component-local styles or a JS animation layer not shown in the excerpt.

---

### Plan 3 — Rebuild toast entrance with transform/opacity and Reduced Motion

**Files / current excerpts**

`src/components/toast.css`

```css
@keyframes toast-enter {
  from { top: -24px; opacity: 0; }
  to { top: 0; opacity: 1; }
}

.toast {
  animation: toast-enter 500ms ease-in forwards;
}
```

**Target behavior**

- Toasts should communicate arrival without slow layout-affecting motion.
- Replace animated `top` with `transform: translateY(...)`.
- Shorten timing to existing semantic duration.
- Use existing responsive easing.
- Add Reduced Motion that removes vertical travel but keeps opacity feedback.

**Project conventions**

- Use existing tokens from `src/styles/motion.css`:
  ```css
  --duration-fast: 160ms;
  --duration-panel: 240ms;
  --ease-responsive: cubic-bezier(0.23, 1, 0.32, 1);
  ```
- Match the local Reduced Motion pattern from `src/components/Button.css`:
  ```css
  @media (prefers-reduced-motion: reduce) {
    .button { transition-duration: 80ms; }
  }
  ```

**Ordered steps**

1. In `src/components/toast.css`, replace the keyframes with transform/opacity:
   ```css
   @keyframes toast-enter {
     from {
       transform: translateY(-8px);
       opacity: 0;
     }
     to {
       transform: translateY(0);
       opacity: 1;
     }
   }
   ```
2. Change `.toast` animation from:
   ```css
   animation: toast-enter 500ms ease-in forwards;
   ```
   to:
   ```css
   animation: toast-enter var(--duration-panel) var(--ease-responsive) both;
   ```
3. Add Reduced Motion:
   ```css
   @media (prefers-reduced-motion: reduce) {
     @keyframes toast-enter {
       from { opacity: 0; }
       to { opacity: 1; }
     }

     .toast {
       animation-duration: 80ms;
     }
   }
   ```
4. If redefining `@keyframes` inside the media query conflicts with the project’s CSS tooling, instead create a separate `toast-enter-reduced` keyframe and assign it inside the media query.
5. Do not animate `top`, `left`, `right`, `bottom`, `margin`, `height`, or `width`.

**Hard boundaries**

- Do not change toast queueing, dismissal timing, z-index, positioning, or message content.
- Do not introduce JS for this predetermined entrance.
- Do not add bounce or playful overshoot; this is an operations console.
- Do not remove opacity feedback in Reduced Motion.

**Mechanical checks**

- Confirm `toast-enter` no longer contains `top`.
- Confirm `.toast` no longer uses `500ms` or `ease-in`.
- Confirm Reduced Motion exists in `src/components/toast.css`.
- Run existing lint/build checks if available.

**Runtime / feel checks for executor**

- Trigger one toast and several consecutive toasts.
- Confirm arrival is noticeable but not slow.
- In slow-motion inspection, confirm vertical movement is subtle and transform-based.
- Toggle Reduced Motion and confirm the toast fades in quickly without vertical travel.

**Reduced Motion behavior**

- `80ms` opacity-only feedback.
- No positional movement.

**Source-drift stop condition**

- Stop if toast animation is no longer implemented in `src/components/toast.css`, if the toast system has moved to a JS animation layer, or if the shown `.toast` selector no longer controls toast entrance.

---

## 4. Recommended execution order

1. **Plan 1 — Command palette**: highest frequency; removes likely throughput drag first.
2. **Plan 2 — Popover motion**: broad convention cleanup; eliminates `transition: all` and `ease-in`.
3. **Plan 3 — Toast entrance**: fixes layout-affecting animation and adds Reduced Motion.

**Explicitly unverified states**

- Actual command palette frequency and whether it opens by keyboard in the running product.
- Whether `.popover` is trigger-anchored, modal-like, or shared by multiple overlay types.
- Whether toast stacking, dismissal, or interruption currently causes visible restart artifacts.
- Whether `animateTo` in `SortableQueue.tsx` is custom, library-based, cancelable, or velocity-aware.
- Actual computed styles, frame rate, layout cost, focus behavior, accessibility tree, and Reduced Motion behavior in a browser.
