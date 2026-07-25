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

## Motion diagnosis

Static evidence shows a calm operations UI with a useful token precedent, but several motion paths drift into slow `ease-in`, broad/property-expensive animation, and missing visible Reduced Motion branches; the highest-risk item is the draggable queue because direct manipulation needs continuity, interruption, and velocity handling that are not proven by the snippet.

---

## 1. Recon summary

- **Stack signals:** React/TSX components, CSS stylesheets, Tailwind-style arbitrary animation class, imperative pointer handler, and an `animateTo(...)` helper.
- **Where motion lives:** `src/styles/motion.css`, component CSS, TSX class names, keyframes, pointer event handlers, and imperative settle animation.
- **Existing conventions:** semantic tokens exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`; the button precedent limits animated property ownership to `transform` and has a Reduced Motion duration of `80ms`.
- **Product personality:** calm, crisp desktop operations console; motion should explain causality and preserve state continuity without cinematic delay.
- **Frequency map:**
  - **Very high / keyboard-heavy:** command palette.
  - **High direct manipulation:** sortable queue.
  - **Repeated utility:** popovers.
  - **Occasional transient feedback:** toast.
  - **High-frequency local precedent:** button, already aligned.
- **Evidence level:** static excerpts only. No computed styles, browser observation, screen recording, performance trace, accessibility tree, or user/device validation.

---

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | `animate-[palette_420ms_ease-in_both]` on a keyboard-heavy command surface | `src/components/CommandPalette.tsx` | Static evidence shows hardcoded 420ms `ease-in` motion outside tokens. For frequent command use, this risks delayed perceived response. Reduced Motion is not shown in the excerpt. | Replace with tokenized `opacity`/small `transform` transition, `160ms` or bounded `160–200ms`, `--ease-responsive`, and an explicit Reduced Motion branch removing travel. |
| P1 | `onPointerMove` writes `--drag-y`; release calls `animateTo(nearestSlot(currentY), { duration: 400 })` | `src/components/SortableQueue.tsx` | Direct manipulation settle is duration-based in the excerpt, with no shown pointer capture, grab offset, presentation-value interruption, or measured velocity handoff. Static evidence cannot prove feel, but this is the highest interaction-risk surface. | Preserve current target semantics, add pointer capture/grab offset/velocity sampling, start settle from current presentation value, and pass measured CSS px/s velocity into a spring/interactive settle if the API supports it. |
| P2 | `transition: all 360ms ease-in; transform-origin: center;` | `src/styles/motion.css` | Broad transition ownership, slow timing for small overlay motion, `ease-in`, and centered origin are inconsistent with crisp utility overlays unless this is truly a centered surface. Reduced Motion is not shown. | Limit to `opacity, transform`, use existing tokens, set trigger-relative origin where the popover is anchored, and add Reduced Motion duration/travel reduction. |
| P2 | `top` keyframe from `-24px` to `0`; `500ms ease-in` | `src/components/toast.css` | Layout-position animation and long `ease-in` entry are a static performance/feel risk for transient feedback. No Reduced Motion branch is shown. | Keep layout position static, animate `transform: translateY(...)` plus `opacity`, use tokenized `200–240ms` max, and reduce to short fade/no travel under Reduced Motion. |
| P2 | Hardcoded `360ms`, `420ms`, `500ms`, `400` and repeated `ease-in` | Multiple excerpts | Motion vocabulary is fragmented despite existing semantic tokens and a correct local precedent. | Normalize high-frequency and utility motion to existing duration/easing tokens; allow component-specific values only when justified and bounded. |
| P3 | Button precedent is correct but isolated | `src/components/Button.css` | The codebase already contains the desired pattern, but other snippets do not reuse its property specificity and Reduced Motion shape. | Treat the button as the local implementation model: specific properties, semantic tokens, and `80ms` Reduced Motion feedback. |

---

## 3. Implementation plans

### Plan 1 — Normalize command palette and popover motion

**Current excerpts**

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

**Target behavior**

- Command palette responds immediately for keyboard users: short fade and at most tiny vertical travel.
- Popovers use specific `opacity`/`transform` transitions, not `all`.
- Existing tokens remain the primary authority: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
- Reduced Motion preserves open/closed feedback with opacity/static state, removes or neutralizes travel, and uses `80ms`.

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, replace the arbitrary keyframe class with tokenized transition classes or the project’s equivalent local class:
   - animate only `opacity` and `transform`;
   - use `var(--duration-fast)` or a bounded `160–200ms`;
   - use `var(--ease-responsive)`;
   - map `data-open=true/false` to visible/hidden visual states without introducing lifecycle changes.
2. In `src/styles/motion.css`, change `.popover` to explicit property ownership:
   - `transition-property: opacity, transform;`
   - `transition-duration: var(--duration-fast);`
   - `transition-timing-function: var(--ease-responsive);`
3. Replace hardcoded `transform-origin: center` with an anchored default only if usage confirms this selector is for anchored overlays; otherwise preserve `center` for centered surfaces and split anchored popovers into a separate selector.
4. Add a `@media (prefers-reduced-motion: reduce)` branch for `.popover` and the command palette class/state that uses `80ms` and removes positional travel.

**Hard boundaries**

- Do not change command search behavior, focus order, result rendering, keyboard shortcuts, or mount/unmount semantics.
- Do not introduce a new animation dependency.
- Do not replace project tokens with new duration/easing names unless broader token ownership is explicitly approved.

**Mechanical checks**

- Run the project’s existing type and lint gates if available.
- Static grep check after edits: no remaining `animate-[palette_420ms_ease-in_both]`; no `.popover { transition: all ... }`.
- Verify no focus outline or focus-visible style is removed.

**Runtime/feel checks to perform later, not performed here**

- Open/close command palette repeatedly via keyboard; acceptance: response starts immediately, no sluggish entry, focus remains predictable.
- Open popover from its trigger; acceptance: origin visually supports the trigger relationship.
- Interrupt open/close rapidly; acceptance: no obvious restart flash or stuck hidden state.

**Reduced Motion behavior**

- Command palette: opacity/static state feedback only, no meaningful travel, about `80ms`.
- Popover: short opacity transition or instant transform-neutral state, focus visibility unchanged.

**Source-drift stop condition**

- Stop before editing if `CommandPalette` already moved to another motion abstraction, if `palette` keyframes define required non-visual lifecycle behavior, or if `.popover` is shared with centered modals where changing origin would alter intended geometry.

---

### Plan 2 — Rework toast entry from layout travel to transform feedback

**Current excerpt**

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

**Target behavior**

- Toast appears as quick, calm feedback: opacity plus small compositor-friendly vertical transform.
- Layout position is stable outside the keyframe.
- Duration uses existing token range, preferably `--duration-panel` at most, with `--ease-responsive`.
- Reduced Motion preserves noticeability without spatial travel.

**Ordered steps**

1. Set the toast’s resting layout position outside the animation, if not already set by surrounding CSS.
2. Replace `top` keyframes with:
   - `from { transform: translateY(-8px); opacity: 0; }`
   - `to { transform: translateY(0); opacity: 1; }`
   using the smallest travel that still explains arrival.
3. Change `.toast` animation timing to `var(--duration-panel) var(--ease-responsive)` or shorter if runtime feel shows delay.
4. Add `@media (prefers-reduced-motion: reduce)`:
   - remove vertical travel;
   - use opacity/static state change around `80ms`;
   - do not suppress the toast’s informational feedback.

**Hard boundaries**

- Do not change toast placement, queueing, timeout duration, ARIA/live-region behavior, or dismissal behavior.
- Do not animate `height`, `margin`, `padding`, `top`, or `left` for entry.
- Do not add `will-change` unless a later trace shows benefit.

**Mechanical checks**

- CSS check: `toast-enter` no longer animates `top`.
- CSS check: `.toast` no longer uses `500ms ease-in`.
- Existing type/lint/build checks if available.

**Runtime/feel checks to perform later, not performed here**

- Trigger single and repeated toasts.
- Acceptance: toast is noticeable but does not feel like a banner sliding through the workspace.
- Under rapid toast creation/dismissal, no visual jump, stuck opacity, or layout shift should be observed.

**Reduced Motion behavior**

- Use fade/static appearance only; remove vertical movement.
- Keep the toast visible and perceivable; Reduced Motion must not mean “no feedback.”

**Source-drift stop condition**

- Stop if `top` animation is compensating for missing fixed/sticky positioning, if toast placement is managed by a third-party library API, or if another stylesheet already overrides `toast-enter`/`.toast` motion.

---

### Plan 3 — Make sortable queue release continuous and interruptible

**Current excerpt**

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

**Target behavior**

- Dragged item tracks 1:1 after intent threshold, without snapping away from the grab point.
- Release settle starts from the current on-screen position.
- Release velocity is measured in CSS px/s and handed into the settle animation.
- Existing target-selection semantics are preserved: keep `nearestSlot(currentY)` unless product authority explicitly approves momentum-based slot selection.
- Reduced Motion keeps direct tracking but removes bounce/overshoot and shortens settle.

**Ordered steps**

1. On pointer down, record:
   - pointer id;
   - starting pointer position in CSS pixels;
   - item/current presentation position;
   - grab offset;
   - short timestamped position history using monotonic time.
2. Use pointer capture once drag intent is confirmed; ignore unrelated pointers during the active drag.
3. On pointer move:
   - compute local drag translation from the recorded start plus grab offset;
   - update a transform-owned element, not an unconstrained parent variable, unless CSS confirms `--drag-y` only drives the dragged item’s transform.
4. Before release, compute velocity from recent samples in CSS px/s.
5. On pointer up:
   - set `dragging` false only after the presentation value is captured;
   - choose target using current project behavior: `nearestSlot(currentY)`;
   - pass measured velocity into the settle if `animateTo` supports velocity/spring parameters.
6. If `animateTo` only supports fixed duration, stop and decide whether to extend the existing helper or use an already-present animation primitive; do not silently add a new dependency.
7. Optional, separately authorized only: compute bounded projected endpoint from current position and velocity, then use it for target selection only if momentum-based queue behavior is approved.

**Hard boundaries**

- Do not change reorder semantics, slot calculation, data mutation timing, selection state, keyboard reorder behavior, or accessibility announcements.
- Do not introduce bounce by default in this operations surface.
- Do not let press feedback and drag translation compete for the same `transform`; use wrapper layers or a single composed transform owner.

**Mechanical checks**

- Type check around pointer event types and animation helper signature.
- Static checks:
  - pointer capture path exists for active drag;
  - velocity samples use consistent CSS px/s units;
  - `nearestSlot(currentY)` behavior is preserved unless explicitly changed;
  - no broad layout reads/writes are added to every pointer move.

**Runtime/feel checks to perform later, not performed here**

- Drag slowly, drag quickly, release near slot boundaries, reverse direction mid-settle, and start a new drag during settle.
- Acceptance: no jump on grab, no jump on interruption, release continues from current position, target is predictable.
- Validate under a large queue/data load before claiming performance quality.

**Reduced Motion behavior**

- Pointer tracking remains direct.
- Release uses no overshoot/bounce, minimal duration around `80ms` or immediate snap with clear static/focus state if that is the project’s accessibility choice.
- No projection-based fling in Reduced Motion unless explicitly approved.

**Source-drift stop condition**

- Stop if `animateTo` already wraps a spring with velocity support, if `--drag-y` is consumed by scoped child transforms only, if `currentY` is not the presentation value, or if queue semantics already define momentum-based target selection elsewhere.

---

## 4. Recommended execution order

1. **Plan 3 first** if sortable queue is on a core workflow: direct manipulation has the highest continuity/accessibility risk.
2. **Plan 1 second:** fixes the high-frequency command palette and repeated popover vocabulary while reinforcing tokens.
3. **Plan 2 third:** bounded polish/performance-risk reduction for transient feedback.

If implementation capacity is limited, do Plan 3 plus the command-palette part of Plan 1 before touching lower-frequency toast polish.

---

## Explicitly unverified states

- Actual animation smoothness, frame rate, compositing, layout shift, and style recalculation cost.
- Whether `.popover` is anchored, centered, shared with modals, or overridden elsewhere.
- The actual `palette` keyframes and command palette mount/unmount lifecycle.
- Whether Reduced Motion exists in other files not shown.
- Pointer capture, grab offset, keyboard reorder behavior, screen-reader announcements, and focus behavior for the queue.
- `animateTo(...)` API capabilities, current presentation-value access, and velocity/spring support.
- Toast live-region behavior, dismissal timing, stacking behavior, and real placement CSS.


## Output B

## 1. Recon summary

- **Stack signals**: React/TSX components with CSS modules/global CSS and utility-style animation classes. No confirmed motion library from the snippets.
- **Where motion lives**:
  - Global semantic motion tokens: `src/styles/motion.css`
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`
  - Inline utility animation: `src/components/CommandPalette.tsx`
  - Gesture JS: `src/components/SortableQueue.tsx`
- **Existing conventions**:
  - Tokens already exist: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
  - Correct precedent exists in `Button.css`: transform-only transition, semantic duration/easing, Reduced Motion shortened to `80ms`.
- **Product personality**: calm desktop operations console; motion should be crisp, causal, low-latency, and non-decorative.
- **Frequency map**:
  - Very high: command palette, keyboard-driven actions, sortable queue drag.
  - Medium: popovers, buttons.
  - Occasional: toasts.
- **Evidence level**: static snippet audit only. No runtime timing, computed styles, browser behavior, accessibility tree, FPS, pointer-device, or user testing was performed.

## 2. Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose / frequency | `src/components/CommandPalette.tsx` | Command palette uses `animate-[palette_420ms_ease-in_both]`. For a keyboard-heavy, high-frequency surface, a 420ms ease-in entrance risks making a primary workflow feel delayed. | Remove the entrance animation from the command palette; keep open/close causality immediate. |
| 2 | HIGH | Performance / easing | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in;`. This animates unintended properties, exceeds the existing fast/panel token scale, and uses slow-start easing. | Limit to `transform, opacity`; use existing duration/easing tokens; add Reduced Motion duration. |
| 3 | HIGH | Performance / interruptibility | `src/components/toast.css` | Toast enters by animating `top` over `500ms ease-in` via keyframes. `top` is layout-affecting, duration is long for operations feedback, and ease-in delays visibility. | Replace layout animation with transform/opacity using existing tokens; provide Reduced Motion opacity-only feedback. |
| 4 | HIGH | Gesture / direct manipulation | `src/components/SortableQueue.tsx` | Pointer move writes `--drag-y` to the queue parent; release uses fixed `duration: 400`. Static evidence suggests drag motion may be parent-style driven and release is not velocity-aware. | Drive only the active dragged element with `transform`; settle with interruptible/velocity-aware behavior or stop if `animateTo` cannot support it. |
| 5 | MEDIUM | Accessibility | Multiple snippets | Reduced Motion is shown only in the correct button precedent. Command palette, popover, toast, and sortable release snippets do not show a Reduced Motion branch. | Apply the button precedent: preserve feedback, shorten or remove movement, avoid deleting all state feedback. |
| 6 | MEDIUM | Cohesion / tokens | Multiple snippets | Motion values are split between semantic tokens and hard-coded `360ms`, `420ms`, `500ms`, `ease-in`. | Consolidate frequent UI motion around existing `--duration-fast`, `--duration-panel`, and `--ease-responsive`. |

---

## 3. Implementation plans

### Plan 1 — Remove command palette entrance latency

**Current excerpt**

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

**Target behavior**

- Opening the command palette should feel immediate for keyboard-heavy repeated use.
- Do not add a replacement entrance animation.
- Preserve `data-open={open}` because it may be used by existing visibility/focus styles outside the snippet.
- Reduced Motion behavior is the same as default: no positional/entrance animation.

**Project conventions to follow**

- Existing correct precedent: `src/components/Button.css` uses semantic motion tokens and keeps Reduced Motion feedback short.
- For this specific high-frequency command surface, prefer no animation over tokenized animation.

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, remove only the arbitrary animation class:
   ```tsx
   <div data-open={open}>
     <SearchResults />
   </div>
   ```
2. If the real file contains additional non-motion classes, keep them and remove only:
   ```tsx
   animate-[palette_420ms_ease-in_both]
   ```
3. Do not add new CSS for palette entrance/exit unless the existing file already has non-motion visibility styles requiring a class hook.

**Hard boundaries**

- Do not change `SearchResults`.
- Do not change command filtering, focus management, keyboard shortcuts, or open-state ownership.
- Do not add dependencies.
- Do not replace this with a shorter animation; the target is immediate command access.

**Mechanical checks**

- Run, if available in the project:
  ```bash
  npm run typecheck
  npm run lint
  npm run build
  ```
- Expected: no TSX syntax errors and no unused-import changes caused by the edit.

**Runtime / feel checks to perform later**

- Open the command palette repeatedly via keyboard.
- Confirm the palette appears without a slow-start visual delay.
- Confirm focus still lands where it did before.
- Confirm closing/reopening quickly does not replay an entrance animation.
- Toggle Reduced Motion and confirm behavior remains immediate.

**Reduced Motion behavior**

- No separate branch required if the animation is fully removed.
- Do not remove visible focus or open-state indication.

**Source-drift stop condition**

- Stop if `CommandPalette.tsx` no longer contains `animate-[palette_420ms_ease-in_both]`.
- Stop if the animation is now managed by a separate transition component or motion library not shown in the snippet.

---

### Plan 2 — Tokenize CSS entrances and remove layout/all-property animation

**Current excerpts**

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

**Target behavior**

- Popovers: animate only `transform` and `opacity`, using existing semantic tokens.
- Toasts: enter with compositor-friendly `transform` and `opacity`, not `top`.
- Use crisp existing timing: `--duration-fast` for small anchored UI, `--duration-panel` for toast feedback.
- Reduced Motion: preserve opacity feedback, remove positional movement, shorten to `80ms`.

**Project conventions to follow**

Use the local precedent:

```css
/* src/components/Button.css */
.button {
  transition: transform var(--duration-fast) var(--ease-responsive);
}

@media (prefers-reduced-motion: reduce) {
  .button { transition-duration: 80ms; }
}
```

**Ordered steps**

1. In `src/styles/motion.css`, replace `.popover` with:
   ```css
   .popover {
     transform-origin: var(--radix-popover-content-transform-origin, var(--transform-origin, center));
     transition:
       transform var(--duration-fast) var(--ease-responsive),
       opacity var(--duration-fast) var(--ease-responsive);
   }

   @media (prefers-reduced-motion: reduce) {
     .popover {
       transition-duration: 80ms;
     }
   }
   ```
2. If this `.popover` is actually used for centered modal content rather than trigger-anchored popovers, keep `transform-origin: center` and still replace `transition: all 360ms ease-in`.
3. In `src/components/toast.css`, replace layout keyframes with transform/opacity:
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
     animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;
   }

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
4. If redefining `@keyframes toast-enter` inside the media query conflicts with the project’s CSS tooling, instead create:
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

- Do not change toast markup, stacking logic, dismissal timing, or live-region behavior.
- Do not add new duration/easing tokens unless existing tokens are unavailable in the actual cascade.
- Do not animate `top`, `left`, `width`, `height`, `margin`, or `padding`.
- Do not use `transition: all`.

**Mechanical checks**

- Run, if available:
  ```bash
  npm run lint
  npm run build
  ```
- Search check after editing:
  ```bash
  grep -R "transition: all 360ms ease-in\|top: -24px\|500ms ease-in" src
  ```
- Expected: no remaining instances of the replaced excerpts unless unrelated and intentionally left.

**Runtime / feel checks to perform later**

- Trigger a popover and confirm it does not animate unrelated properties.
- If the popover is trigger-anchored, confirm slow-motion playback appears to originate from the trigger side, not arbitrarily from the center.
- Trigger a toast and confirm it slides a small distance while fading in, without pushing layout.
- Trigger multiple toasts quickly and confirm no obvious jump caused by `top` animation.
- Toggle Reduced Motion and confirm toast movement is removed but opacity feedback remains.

**Reduced Motion behavior**

- Popover: same properties, shortened to `80ms`.
- Toast: opacity-only, `80ms`, no vertical translation.

**Source-drift stop condition**

- Stop if `.popover` has moved to component-scoped styles not represented by `src/styles/motion.css`.
- Stop if `.toast` is no longer CSS-keyframe based or toast positioning is now controlled by a motion/transition component.

---

### Plan 3 — Make sortable drag direct, transform-only, and release-aware

**Current excerpt**

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

**Target behavior**

- During drag, only the active dragged item moves.
- Movement should be written as `transform: translate3d(...)`, not as a parent CSS variable that may invalidate descendants.
- Release should settle to `nearestSlot(currentY)` with responsive timing and interruption support.
- If the existing `animateTo` helper supports spring/velocity options, use them. If not, use the existing helper with shorter token-aligned duration and stop for a follow-up refactor rather than inventing a new animation engine.
- Reduced Motion should avoid long glide motion while preserving final placement feedback.

**Project conventions to follow**

- Existing motion precedent favors transform-only updates and semantic timing.
- Existing token values to align with:
  ```css
  --duration-fast: 160ms;
  --duration-panel: 240ms;
  --ease-responsive: cubic-bezier(0.23, 1, 0.32, 1);
  ```

**Ordered steps**

1. Locate the actual dragged item ref in `src/components/SortableQueue.tsx`.
   - If only `queueRef` exists and there is no active item element ref, add an explicit `draggedItemRef` to the element that visually follows the pointer.
2. Replace parent CSS-variable movement:
   ```tsx
   queueRef.current?.style.setProperty("--drag-y", `${event.clientY}px`);
   ```
   with a direct transform on the dragged element:
   ```tsx
   draggedItemRef.current!.style.transform = `translate3d(0, ${event.clientY}px, 0)`;
   ```
3. If the component already tracks a drag origin, use delta instead of absolute viewport Y:
   ```tsx
   const nextY = event.clientY - dragStartYRef.current;
   draggedItemRef.current!.style.transform = `translate3d(0, ${nextY}px, 0)`;
   ```
4. Track last pointer sample for release velocity:
   ```tsx
   lastPointerSampleRef.current = { y: event.clientY, time: performance.now() };
   ```
   Update velocity from the previous sample before overwriting it.
5. Replace fixed release duration:
   ```tsx
   animateTo(nearestSlot(currentY), { duration: 400 });
   ```
   with the best supported option:
   ```tsx
   animateTo(nearestSlot(currentY), {
     type: "spring",
     duration: 0.5,
     bounce: 0.2,
     velocity: releaseVelocityYRef.current
   });
   ```
6. If `animateTo` does not support spring options, use:
   ```tsx
   animateTo(nearestSlot(currentY), {
     duration: 240,
     easing: "cubic-bezier(0.23, 1, 0.32, 1)"
   });
   ```
   and create no new animation abstraction in this pass.
7. Add or reuse a Reduced Motion check. If the project has no hook/helper, use `window.matchMedia("(prefers-reduced-motion: reduce)").matches` at the interaction boundary:
   ```tsx
   const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
   ```
   Then release with:
   ```tsx
   animateTo(nearestSlot(currentY), { duration: 80 });
   ```

**Hard boundaries**

- Do not change queue ordering rules.
- Do not change pointer capture, selection, keyboard reordering, or persistence behavior.
- Do not add a new motion dependency.
- Do not move every child on pointer move.
- Do not implement physics if `animateTo` cannot support interruption or velocity; stop and report that helper capability is the blocker.

**Mechanical checks**

- Run, if available:
  ```bash
  npm run typecheck
  npm run lint
  npm run build
  ```
- Search check after editing:
  ```bash
  grep -R "setProperty(\"--drag-y\"" src/components/SortableQueue.tsx
  ```
- Expected: no parent `--drag-y` pointer-move write remains in this component.

**Runtime / feel checks to perform later**

- Drag an item slowly and confirm it stays directly under the pointer.
- Drag quickly and release; confirm the item settles toward the nearest slot without a fixed-feeling 400ms glide.
- Interrupt by starting a second drag quickly after release; confirm motion does not visibly restart from zero.
- Use performance tools while dragging and confirm no broad child style recalculation is caused by parent CSS-variable updates.
- Toggle Reduced Motion and confirm release movement is shortened while final placement remains clear.

**Reduced Motion behavior**

- Pointer following remains direct because it is user-controlled.
- Release animation shortens to `80ms` or snaps to final transform if that is the project’s existing Reduced Motion convention.
- Do not remove focus, selection, or placement feedback.

**Source-drift stop condition**

- Stop if `SortableQueue.tsx` no longer contains `setProperty("--drag-y"` or `animateTo(nearestSlot(currentY), { duration: 400 })`.
- Stop if `animateTo` is imported from an external helper whose options are unknown and cannot be confirmed from source.

---

## 4. Recommended execution order

1. **Plan 1 — Command palette**: highest workflow impact, smallest safe change.
2. **Plan 2 — CSS entrances**: removes `transition: all`, layout animation, hard-coded slow values, and missing Reduced Motion paths.
3. **Plan 3 — Sortable queue**: highest interaction complexity; execute after confirming `animateTo` capabilities.

## Explicitly unverified states

- Actual rendered appearance, frame rate, interruption behavior, and computed styles.
- Whether `.popover` is always trigger-anchored or sometimes used like a centered modal.
- Whether command palette visibility/focus is controlled elsewhere.
- Whether toast stacking/dismissal logic exists outside `toast.css`.
- Whether `animateTo` supports spring, velocity, cancellation, or Reduced Motion options.
- Package manager and exact available validation scripts.
- Browser support targets for any CSS feature choices.


## Output C

## 1. Recon summary

- **Stack signals:** React/TSX components, plain CSS, CSS custom properties, Tailwind-style arbitrary animation utility, and JS-driven drag animation.
- **Where motion currently lives:**
  - Global/system CSS: `src/styles/motion.css`
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`
  - Inline utility class in TSX: `src/components/CommandPalette.tsx`
  - Pointer/JS animation logic: `src/components/SortableQueue.tsx`
- **Existing conventions from evidence:**
  - Semantic tokens exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
  - Correct local precedent exists in `Button.css`: transform-only transition, tokenized timing/easing, `prefers-reduced-motion` fallback to `80ms`.
- **Product personality:** calm, crisp, continuity-preserving, optimized for repeated desktop use and keyboard-heavy operators.
- **Frequency map:**
  - Very frequent: buttons, command palette.
  - Frequent/contextual: popovers.
  - Intermittent but attention-grabbing: toasts.
  - Intensive during task bursts: sortable queue drag/reorder.
- **Evidence level:** static code-only audit. No runtime, computed style, accessibility tree, trace, screen recording, or user validation was performed.

---

## 2. Vetted priority table

| Priority | Finding | Evidence | Risk to product goal | Recommendation |
|---:|---|---|---|---|
| P0 | Reduced Motion is not consistently implemented | `Button.css` has `prefers-reduced-motion`; popover, palette, toast, and queue snippets do not show it | Operators who request reduced motion may still get long spatial motion | Apply the button precedent: preserve feedback, shorten to `80ms`, reduce spatial travel |
| P0 | Motion bypasses semantic tokens | `360ms`, `420ms`, `500ms`, `400`, `ease-in` appear outside tokens | Inconsistent feel; hard to govern system-wide | Replace hardcoded values with existing duration/easing conventions |
| P1 | Layout-affecting or broad animation is present | `.popover { transition: all ... }`; toast animates `top` | Can create unnecessary layout work and unpredictable property animation | Restrict to `transform` and `opacity`; never use `transition: all` |
| P1 | Several entrance motions are likely too slow for high-frequency ops UI | `420ms`, `500ms`, `400ms`, `ease-in` | Motion may delay perceived response and reduce throughput | Use `--duration-fast` for feedback and `--duration-panel` for larger surfaces |
| P1 | Command palette motion is hidden in an arbitrary class | `className="animate-[palette_420ms_ease-in_both]"` | Harder to audit, theme, reduce, and align with system rules | Move to named class/CSS using tokens and data state |
| P2 | Drag release uses hardcoded settle timing | `animateTo(nearestSlot(currentY), { duration: 400 })` | Direct manipulation may feel disconnected on release | Tokenize settle duration; preserve 1:1 drag, shorten/reduce release motion |

---

## 3. Implementation plans

### Plan A — Normalize overlay and command-palette motion

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

- Popovers and command palette feel immediate, calm, and causally connected.
- Animate only `opacity` and `transform`.
- Use existing semantic timing/easing.
- Support both opening and closing states through `data-open`.
- Reduced Motion preserves visible state feedback without long spatial movement.

**Project conventions to follow**

- Prefer `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Follow the `Button.css` precedent for reduced motion: `80ms`.
- Do not introduce decorative bounce, overshoot, or unrelated visual styling.

**Ordered steps**

1. Replace `.popover` transition with explicit properties only:
   - `opacity`
   - `transform`
2. Replace `360ms ease-in` with existing tokens.
   - Use `--duration-fast` for small popovers.
   - Use `--duration-panel` only if the popover is visually panel-like or large.
3. Move command palette animation out of the arbitrary TSX class into a named CSS class.
4. Keep `data-open={open}` as the state hook.
5. Define closed/open styles using transform and opacity, for example:
   - closed: slightly translated or scaled, transparent
   - open: neutral transform, opaque
6. Add `@media (prefers-reduced-motion: reduce)`:
   - duration `80ms`
   - remove or minimize spatial travel
   - preserve opacity/state feedback
7. Ensure focus styling is untouched.

**Hard boundaries**

- Do not change command palette contents, search behavior, result ordering, focus target, or keyboard shortcuts.
- Do not add new motion tokens unless the existing design authority explicitly allows it.
- Do not replace semantic state with mount/unmount behavior unless already supported elsewhere.

**Mechanical checks**

- No `transition: all` remains for `.popover`.
- No `420ms`, `360ms`, or `ease-in` remains for these overlay motions.
- Command palette class is named and auditable.
- Reduced Motion branch exists for the new class.
- Only `opacity` and `transform` are animated.

**Runtime / feel checks for later validation**

- Open and close command palette repeatedly from keyboard.
- Confirm motion does not delay text input readiness.
- Confirm focus remains visible during and after open.
- Confirm popover opening preserves anchor causality.
- Confirm Reduced Motion still gives clear state change without spatial travel.

**Reduced Motion behavior**

- Use `80ms`.
- Prefer opacity-only or near-zero transform distance.
- No spring, bounce, or long slide.

**Source-drift stop condition**

Stop and re-plan if `CommandPalette` now conditionally unmounts, uses a transition library, has focus-management changes, or if `motion.css` token names differ from the excerpt.

---

### Plan B — Convert toast entrance to compositor-safe feedback

**File / current excerpt**

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

- Toast appears promptly without layout-position animation.
- Motion communicates arrival, not decoration.
- Duration and easing match the system.
- Reduced Motion keeps feedback but removes meaningful travel.

**Project conventions to follow**

- Use semantic duration/easing tokens.
- Prefer transform/opacity.
- Match the `Button.css` reduced-motion duration precedent.

**Ordered steps**

1. Replace `top` animation with `transform`.
2. Use a smaller travel distance than the current `24px` unless design authority requires otherwise.
   - Example target: `translateY(-8px)` to `translateY(0)`.
3. Replace `500ms ease-in` with:
   - `var(--duration-fast)` or `var(--duration-panel)` depending on toast prominence.
   - For an ops console, prefer `--duration-fast` unless toasts are large/persistent.
4. Use `var(--ease-responsive)`.
5. Use `both` or keep `forwards` only if the existing final-state behavior requires it.
6. Add Reduced Motion media query:
   - duration `80ms`
   - opacity transition only, or near-zero travel.

**Hard boundaries**

- Do not change toast placement, stacking, dismissal timing, content, or severity styling.
- Do not add attention-grabbing bounce/shake.
- Do not alter ARIA/live-region behavior unless separately audited.

**Mechanical checks**

- `toast-enter` no longer animates `top`.
- `.toast` no longer uses `500ms ease-in`.
- Animation uses existing duration/easing tokens.
- Reduced Motion branch exists.
- Final visual state remains `opacity: 1` and neutral transform.

**Runtime / feel checks for later validation**

- Trigger one toast and multiple stacked toasts.
- Confirm the toast does not visually push surrounding layout.
- Confirm appearance is noticeable but not slow.
- Confirm Reduced Motion still makes the toast arrival perceivable.

**Reduced Motion behavior**

- `80ms`.
- Opacity-first.
- No meaningful vertical travel.

**Source-drift stop condition**

Stop and re-plan if toast positioning has moved to a portal, animation library, JS timer system, or if multiple toast variants use separate keyframes not shown here.

---

### Plan C — Tokenize sortable queue drag settlement while preserving direct manipulation

**File / current excerpt**

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

- During drag: item follows pointer directly with minimal latency.
- On release: item settles to nearest slot quickly and predictably.
- JS animation duration aligns with the CSS motion system.
- Reduced Motion shortens settlement but still preserves state continuity.

**Project conventions to follow**

- Preserve transform-based motion if the CSS consuming `--drag-y` already uses transform.
- Align JS duration with existing semantic token values:
  - normal settle: equivalent to `--duration-panel` / `240ms`
  - reduced settle: `80ms`
- Use the responsive easing if the animation API supports easing.

**Ordered steps**

1. Locate the CSS that consumes `--drag-y`.
2. Confirm it drives `transform`, not `top`, `margin`, or layout positioning.
3. If it currently drives layout, change the consumer to transform-based movement.
4. Keep pointer-move updates outside React state during active drag.
5. Consider coalescing pointer writes with `requestAnimationFrame` only if later profiling shows excessive pointer work.
6. Replace hardcoded `duration: 400` with a named duration aligned to the motion tokens.
7. Add Reduced Motion detection for the release animation:
   - normal: approximately `240ms`
   - reduced: `80ms`
8. If `animateTo` supports easing, pass the responsive easing equivalent.
9. Keep `nearestSlot(currentY)` behavior unchanged.

**Hard boundaries**

- Do not change sorting rules, slot calculation, persistence, selection, or keyboard reorder behavior.
- Do not add physics, bounce, overshoot, or inertia.
- Do not introduce React state updates on every pointer move.
- Do not assume `event.clientY` is wrong without inspecting the CSS coordinate system.

**Mechanical checks**

- No hardcoded `duration: 400` remains for queue settlement.
- Reduced Motion branch exists for release animation.
- Pointer-move path still performs only narrow imperative updates.
- Drag movement is transform-backed after checking the CSS consumer.
- Slot calculation remains unchanged.

**Runtime / feel checks for later validation**

- Drag slowly, quickly, and across multiple slots.
- Confirm item remains visually attached to pointer.
- Release near slot boundaries and verify predictable settle.
- Confirm no delayed snap after pointer up.
- Confirm Reduced Motion release is short but still understandable.
- Confirm keyboard-heavy workflows are not disrupted.

**Reduced Motion behavior**

- Preserve direct drag response.
- Shorten release settlement to `80ms`.
- Avoid bounce, inertia, or large animated travel beyond the required slot correction.

**Source-drift stop condition**

Stop and re-plan if `animateTo` comes from a library with its own duration units/easing model, if `currentY` is derived differently than expected, or if `--drag-y` is no longer the active movement variable.

---

## 4. Recommended execution order

1. **Plan A first:** fixes the highest-frequency operator surfaces and removes the least governable arbitrary animation.
2. **Plan B second:** small, isolated, high-confidence compositor-safety improvement.
3. **Plan C third:** higher interaction risk; inspect the consuming CSS and animation API before changing.

---

## Explicitly unverified states

- Actual computed styles and final cascade order.
- Whether `palette` keyframes already exist elsewhere.
- Whether popover has separate open/closed state styles.
- Whether command palette is mounted while closed or conditionally rendered elsewhere.
- Whether toast container positioning depends on `top` animation side effects.
- Whether `--drag-y` is consumed by `transform` or by layout properties.
- Whether `animateTo` duration is milliseconds and whether it supports easing.
- Actual frame timing, input latency, focus behavior, screen-reader behavior, or user comfort.
- Reduced Motion behavior at runtime.
