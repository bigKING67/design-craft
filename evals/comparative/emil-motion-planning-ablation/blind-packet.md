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

## 1. Recon summary

**Stack signals**
- React/TSX components with CSS files.
- Global semantic motion tokens exist in `src/styles/motion.css`.
- Component-local CSS is used for buttons/toasts.
- Utility/arbitrary animation syntax appears in `CommandPalette.tsx`.

**Where motion currently lives**
- Global tokens and `.popover`: `src/styles/motion.css`
- Component-local animation: `src/components/toast.css`
- Inline utility animation: `src/components/CommandPalette.tsx`
- Imperative drag/snap behavior: `src/components/SortableQueue.tsx`
- Good local precedent: `src/components/Button.css`

**Existing conventions**
- Preferred tokens:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Correct precedent uses `transform`, semantic duration/easing, and a Reduced Motion override to `80ms`.

**Product personality**
- Calm desktop operations console.
- Keyboard-heavy, repeated daily use.
- Motion should explain cause/effect and state continuity, not feel decorative or delay throughput.

**Frequency map**
- Very high frequency: button press, drag movement, queue sorting.
- High frequency: command palette open/close, popovers.
- Medium frequency: toasts.
- Lower tolerance for slow/ease-in motion on command, drag, and repeated overlay interactions.

**Evidence level**
- Static code excerpts only.
- No runtime, computed-style, trace, screen recording, accessibility-tree, device, or user validation was performed.

---

## 2. Vetted priority table

| Priority | Finding | Evidence | Risk | Recommended direction |
|---:|---|---|---|---|
| P0 | Popover uses broad, slow, non-token transition | `.popover { transition: all 360ms ease-in; }` | `all` may animate unintended/layout properties; `360ms ease-in` feels delayed for repeated ops use | Limit to `opacity, transform`; use existing tokens; add Reduced Motion |
| P0 | Drag/snap path uses hardcoded duration and high-frequency direct writes | `setProperty("--drag-y", ...)`; `animateTo(..., { duration: 400 })` | Direct manipulation path may feel laggy/inconsistent; no visible Reduced Motion policy | Keep drag immediate; snap with semantic duration; coalesce pointer updates; reduced snap duration |
| P1 | Command palette bypasses semantic tokens | `animate-[palette_420ms_ease-in_both]` | Slow command surface; arbitrary duration/easing; no visible Reduced Motion path | Move to named class/CSS using tokens; ensure open/closed states are explicit |
| P1 | Toast animates layout property | `top: -24px → 0`; `500ms ease-in` | Layout-affecting animation and slow entrance for operational feedback | Use `transform: translateY(...)` + `opacity`; tokenized duration/easing; reduced path |
| P2 | Reduced Motion exists only in local precedent | Button has media query; other snippets do not | Inconsistent accessibility behavior | Standardize reduced behavior across overlay, toast, command palette, queue snap |
| P2 | Motion governance is fragmented | Global CSS, local CSS, arbitrary utility, imperative JS | Drift risk and inconsistent feel | Use global semantic tokens and small component-local classes; avoid arbitrary one-off timings |

---

## 3. Implementation plans

### Plan A — Normalize transient overlay motion: popover + command palette

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
- Popovers and command palette should feel immediate, calm, and causally connected.
- Opening: subtle opacity + transform using `--duration-panel` and `--ease-responsive`.
- Closing: same properties, not slower than opening.
- Avoid `transition: all`.
- Avoid arbitrary one-off animation strings for core surfaces.
- Reduced Motion keeps feedback but compresses duration to `80ms`.

**Project conventions to preserve**
- Use existing semantic tokens from `src/styles/motion.css`.
- Follow the button precedent: transform-only motion, tokenized duration/easing, reduced duration.
- Do not introduce decorative spring/bounce behavior.
- Do not alter search result rendering or command behavior.

**Ordered steps**
1. In `src/styles/motion.css`, replace `.popover` transition with explicit properties:
   - `opacity`
   - `transform`
2. Keep `transform-origin: center` unless another anchored origin is already defined elsewhere.
3. Add stateful selectors for popover visibility if the app already uses attributes/classes for open state.
   - Preferred shape: `[data-open="true"]` / `[data-open="false"]`
   - Stop if current app uses a different state convention.
4. Replace `transition: all 360ms ease-in` with:
   - `transition-property: opacity, transform;`
   - `transition-duration: var(--duration-panel);`
   - `transition-timing-function: var(--ease-responsive);`
5. In `src/components/CommandPalette.tsx`, remove the arbitrary animation class.
6. Add a stable class, for example `className="command-palette"` while preserving `data-open={open}`.
7. Define command palette motion in the appropriate existing stylesheet, preferably near other motion/component styles:
   - closed: slightly offset/scaled with lower opacity
   - open: `transform: translateY(0) scale(1); opacity: 1`
8. Add a Reduced Motion media query that sets duration to `80ms` and removes distance-heavy transform.

**Hard boundaries**
- Do not change focus management, search behavior, keyboard shortcuts, or result ordering in this plan.
- Do not add new animation libraries.
- Do not add new global tokens unless the existing three are insufficient after inspecting the real file.
- Do not convert the command palette to mount/unmount differently unless existing lifecycle requires it.

**Mechanical checks**
- Search for remaining `transition: all` in touched files.
- Search for remaining `animate-[palette_420ms_ease-in_both]`.
- Confirm all new durations use `var(--duration-fast)`, `var(--duration-panel)`, or `80ms` inside Reduced Motion.
- Confirm animated properties are limited to `opacity` and `transform`.

**Runtime/feel checks to perform later**
- Open/close command palette repeatedly via keyboard.
- Confirm it does not feel slower than task flow.
- Confirm focus ring remains visible during and after animation.
- Confirm popover opening preserves anchor causality.
- Confirm reduced-motion setting still gives clear state change without broad movement.

**Reduced Motion behavior**
- Duration: `80ms`.
- Keep opacity feedback.
- Remove or minimize translate/scale distance.
- Do not make the state change invisible.

**Source-drift stop condition**
- Stop before implementation if `.popover` has additional unseen state rules, if `palette` keyframes are defined elsewhere with required behavior, or if `CommandPalette` class composition is controlled by a shared utility not shown here.

---

### Plan B — Make toast entrance layout-safe and operationally faster

**Current excerpt**

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
- Toast should appear promptly as feedback, not drift slowly into place.
- Animate compositor-friendly properties:
  - `transform`
  - `opacity`
- Use semantic timing and easing.
- Preserve clear feedback in Reduced Motion.

**Project conventions to preserve**
- Existing token names and button precedent.
- Calm, crisp, non-decorative motion.
- No change to toast content, role, timeout, stacking, or dismissal behavior in this plan.

**Ordered steps**
1. Replace keyframe `top` animation with `transform`.
2. Use an entrance offset equivalent in feel to the current `-24px`, but via:
   - `transform: translateY(-8px)` or `translateY(-12px)`
   - avoid the full `-24px` unless product feel requires a stronger entrance.
3. Replace `500ms ease-in` with tokenized timing:
   - likely `var(--duration-fast)` for a simple toast entrance
   - `var(--ease-responsive)` for responsive arrival
4. Keep `opacity: 0 → 1`.
5. Add Reduced Motion media query:
   - duration `80ms`
   - either no vertical offset or a very small one.
6. If toast exit animation exists elsewhere, align its properties and timing with the new entrance model.

**Hard boundaries**
- Do not change toast positioning model outside the animation.
- Do not alter notification semantics, live-region behavior, timers, stacking, or dismissal.
- Do not introduce long easing or bounce.
- Do not animate `top`, `left`, `right`, `bottom`, `height`, or `margin`.

**Mechanical checks**
- Confirm `@keyframes toast-enter` no longer contains `top`.
- Confirm `.toast` no longer uses `500ms ease-in`.
- Confirm animation uses existing duration/easing tokens.
- Confirm Reduced Motion override exists in `src/components/toast.css`.

**Runtime/feel checks to perform later**
- Trigger single toast and stacked toasts.
- Confirm entrance is noticeable but not attention-heavy.
- Confirm no layout jump is visible.
- Confirm repeated toasts do not feel sluggish.
- Confirm Reduced Motion mode still communicates arrival.

**Reduced Motion behavior**
- Use `80ms`.
- Prefer opacity-only or near-zero translate.
- Preserve feedback; do not silently appear without any perceptible state change unless required by user settings.

**Source-drift stop condition**
- Stop if toast positioning relies on the animated `top` value for final layout, if there are coordinated stack animations not shown, or if another stylesheet overrides `.toast` animation.

---

### Plan C — Stabilize sortable queue direct manipulation and snap motion

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
- During drag: movement should track pointer directly and immediately.
- On release: snap should be short, causal, and token-consistent.
- Reduced Motion should shorten snap while preserving positional feedback.
- High-frequency pointer movement should avoid unnecessary repeated style writes.

**Project conventions to preserve**
- Prefer transform-driven motion.
- Prefer semantic timing.
- Keep operations-console feel: no playful bounce, overshoot, or elastic effects.
- Do not change queue ordering rules.

**Ordered steps**
1. Inspect the CSS using `--drag-y`.
2. Confirm the variable drives `transform`, not layout properties.
   - If it drives `top`, `margin`, or layout, convert the rendered moving item to use `transform`.
3. Replace raw pointer-move style writes with requestAnimationFrame coalescing:
   - store latest pointer value
   - schedule one frame
   - write `--drag-y` once per animation frame
4. Prefer storing drag delta rather than absolute `clientY` if the CSS represents visual translation.
   - Current `event.clientY` is viewport-relative; verify whether downstream CSS expects absolute or relative input.
5. Replace hardcoded snap duration `400` with a semantic duration:
   - default snap: `240ms` / panel duration equivalent
   - if snap distance is tiny, consider `160ms`
6. Add a reduced-motion branch for snap duration:
   - `80ms`
7. Ensure pointer-up cancels any pending frame before or during snap handoff to avoid stale writes.
8. Ensure the same final slot calculation is preserved:
   - `nearestSlot(currentY)` should remain the source of final position unless a bug is found separately.

**Hard boundaries**
- Do not rewrite the drag-and-drop model.
- Do not change queue data mutation, item identity, nearest-slot math, or persistence behavior.
- Do not add physics unless already present in the animation utility.
- Do not introduce animation that delays the actual committed reorder.

**Mechanical checks**
- Search touched queue styles for layout-property animation.
- Confirm no hardcoded `400` remains for queue snap unless justified by a named constant.
- Confirm reduced-motion detection is centralized or at least consistent with CSS media query behavior.
- Confirm pointer-move writes are frame-coalesced.
- Confirm pending animation frame is cleaned up on pointer up/cancel/unmount.

**Runtime/feel checks to perform later**
- Drag slowly and quickly through multiple slots.
- Release near and far from target slot.
- Confirm no visible lag between pointer and item.
- Confirm snap does not block rapid follow-up actions.
- Confirm keyboard or non-pointer sorting path, if present, remains understandable.
- Confirm Reduced Motion shortens the snap but still makes the final placement clear.

**Reduced Motion behavior**
- Drag remains direct.
- Release snap duration becomes `80ms`.
- Avoid long travel animations; if distance is large, prefer immediate placement with a brief opacity/position confirmation rather than a slow glide.

**Source-drift stop condition**
- Stop if `animateTo` is a shared utility with global duration policy, if `--drag-y` participates in complex layout calculations, or if the queue already has unshown accessibility/keyboard drag behavior coupled to the current timing.

---

## 4. Recommended execution order

1. **Plan A first** — fixes the broadest convention drift: `transition: all`, arbitrary command palette timing, and missing Reduced Motion coverage for common overlays.
2. **Plan C second** — addresses the highest-frequency interaction path where latency and causality matter most.
3. **Plan B third** — contained, low-risk improvement for notification feedback and layout-safe animation.

## Explicitly unverified states

- Actual computed styles.
- Existence and contents of `palette` keyframes.
- Whether components mount/unmount or remain in DOM while closed.
- Focus management, focus trap behavior, and accessibility tree.
- Actual use of `--drag-y` in CSS.
- Behavior of `animateTo`.
- Toast stacking, live-region semantics, dismissal timing, and exit animation.
- Browser performance, frame rate, layout/recalc cost, and paint behavior.
- Device-specific feel, reduced-motion runtime behavior, and user testing outcomes.


## Output B

## 1. Recon summary

- **Stack signals**: React/TSX components, plain CSS, semantic CSS custom-property tokens, utility-style arbitrary animation classes, imperative pointer/animation code.
- **Where motion lives**:
  - Global tokens and shared selectors: `src/styles/motion.css`
  - Component-local CSS: `src/components/toast.css`, `src/components/Button.css`
  - Inline utility animation: `src/components/CommandPalette.tsx`
  - Gesture/reorder logic: `src/components/SortableQueue.tsx`
- **Existing conventions**:
  - Durations: `--duration-fast: 160ms`, `--duration-panel: 240ms`
  - Easing: `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
  - Correct precedent: button press uses `transform`, semantic tokens, and `prefers-reduced-motion` with `80ms`.
- **Product personality**: crisp, calm, low-latency operations UI. Motion should clarify state and causality, not decorate or delay repeated workflows.
- **Frequency map from product context + snippets**:
  - Very high: command palette, keyboard-triggered actions.
  - High: queue sorting/dragging during operational triage.
  - Medium: popovers.
  - Occasional: toasts.
- **Evidence level**: static code excerpt only. No runtime, computed style, trace, screen recording, accessibility tree, or user testing was performed.

---

## 2. Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose / frequency / latency | `src/components/CommandPalette.tsx` | A likely high-frequency keyboard surface animates with `420ms ease-in`. This delays the exact response operators need to feel immediate. | Remove the command palette entrance animation; keep open/closed state instantaneous. |
| 2 | HIGH | Performance / easing / cohesion | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in`; this can animate unintended properties, exceeds the existing fast/panel token rhythm, and starts slowly. | Restrict to `transform, opacity`; use existing duration/easing tokens; add reduced-motion duration. |
| 3 | MEDIUM | Physicality / origin | `src/styles/motion.css` | `.popover { transform-origin: center; }` is suspicious for trigger-anchored UI. Static evidence does not prove all `.popover` usage is trigger-anchored, so this is conditional. | Use a trigger-origin custom property only if the component already exposes one; otherwise stop and escalate. |
| 4 | HIGH | Performance / accessibility / interruptibility | `src/components/toast.css` | Toast entry animates `top` for `500ms ease-in` via keyframes and has no shown reduced-motion path. `top` is layout-affecting; keyframes are poorer for rapidly changing stacks. | Animate `transform`/`opacity`, cap to existing panel timing, add reduced-motion opacity-only feedback. |
| 5 | HIGH | Gesture / performance / accessibility | `src/components/SortableQueue.tsx` | Pointer move writes a CSS custom property on the queue container; release uses a fixed `400ms` animation. Static evidence does not show velocity, interruptibility, or reduced-motion handling. | Move active item with direct transform, shorten/retarget release motion, add reduced-motion branch. |

No additive “missed opportunity” is supportable from the static snippets alone.

---

# Plan 1 — Make command palette opening immediate

- **Severity**: HIGH  
- **Category**: Purpose / frequency / latency  
- **Estimated scope**: 1 file, small TSX edit

## Current evidence

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

## Target behavior

The command palette should appear/disappear immediately when `open` changes. It is a high-frequency keyboard surface; motion here should not delay task throughput.

Target excerpt:

```tsx
// src/components/CommandPalette.tsx — target
export function CommandPalette({ open }: { open: boolean }) {
  return (
    <div data-open={open}>
      <SearchResults />
    </div>
  );
}
```

If the real file contains additional non-motion classes, preserve them and remove only the `animate-[palette_420ms_ease-in_both]` class.

## Project conventions to follow

- Use semantic shared tokens for motion only where motion is justified.
- Existing correct precedent: `src/components/Button.css` uses `transform`, `--duration-fast`, `--ease-responsive`, and a reduced-motion duration.
- Do not introduce a new palette animation token for this surface.

## Ordered steps

1. Open `src/components/CommandPalette.tsx`.
2. Remove `animate-[palette_420ms_ease-in_both]` from the `className`.
3. If `className` becomes empty, remove the `className` prop entirely.
4. Do not change `data-open`, `SearchResults`, focus management, keyboard handling, or markup hierarchy.
5. Search for the `palette` keyframe or utility definition. If it is used nowhere else, leave deletion as a separate cleanup only if project conventions allow dead CSS removal.

## Hard boundaries

- Do **not** add a replacement fade, scale, slide, blur, or stagger.
- Do **not** alter search result rendering or keyboard behavior.
- Do **not** change open-state semantics beyond removing the animation class.

## Mechanical checks

- Confirm `src/components/CommandPalette.tsx` no longer contains `420ms`, `ease-in`, or `animate-[palette`.
- Run the project’s existing lint/type-check command if available.
- If no scripts are known, at minimum ensure the TSX still parses and the component signature is unchanged.

## Runtime / feel checks for executor

- Open/close the command palette repeatedly using the keyboard shortcut.
- Confirm it responds immediately, with no visible entrance delay.
- Confirm focus still lands where it did before.
- In reduced-motion mode, confirm behavior is identical and still immediate.

## Reduced Motion behavior

No separate reduced-motion branch is needed because the motion is removed for all users.

## Source-drift stop condition

Stop and report instead of editing if:
- The animation class is also responsible for visibility/layout, not just motion.
- The component has been rewritten to use a different animation system.
- Removing the class would remove required styling unrelated to motion.

---

# Plan 2 — Normalize popover and toast entrance motion

- **Severity**: HIGH  
- **Category**: Performance / easing / accessibility / cohesion  
- **Estimated scope**: 2 CSS files

## Current evidence

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

## Target behavior

- Popovers transition only compositor-safe properties.
- Toasts enter using `transform` and `opacity`, not `top`.
- Both use existing semantic tokens.
- Reduced Motion preserves opacity feedback while removing movement.

Target excerpt:

```css
/* src/styles/motion.css — target */
:root {
  --duration-fast: 160ms;
  --duration-panel: 240ms;
  --ease-responsive: cubic-bezier(0.23, 1, 0.32, 1);
}

.popover {
  transform-origin: var(--popover-transform-origin, center);
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

```css
/* src/components/toast.css — target */
.toast {
  top: 0;
  opacity: 1;
  transform: translate3d(0, 0, 0);
  transition:
    transform var(--duration-panel) var(--ease-responsive),
    opacity var(--duration-panel) var(--ease-responsive);
}

@starting-style {
  .toast {
    opacity: 0;
    transform: translate3d(0, -8px, 0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .toast {
    transition-duration: 80ms;
    transform: none;
  }

  @starting-style {
    .toast {
      opacity: 0;
      transform: none;
    }
  }
}
```

## Project conventions to follow

- Reuse existing `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Match the local button precedent: animate `transform`; use `80ms` in reduced-motion mode.
- Do not create parallel hard-coded duration/easing values.

## Ordered steps

1. In `src/styles/motion.css`, replace `.popover { transition: all 360ms ease-in; }` with explicit `transform` and `opacity` transitions using `--duration-fast` and `--ease-responsive`.
2. Replace `transform-origin: center` with `transform-origin: var(--popover-transform-origin, center)`.
3. If actual popover code already exposes a trigger-origin variable, set `--popover-transform-origin` there. If no such source exists, leave the fallback and report that trigger-origin wiring needs component context.
4. Add the reduced-motion media query for `.popover` with `transition-duration: 80ms`.
5. In `src/components/toast.css`, remove `@keyframes toast-enter`.
6. Replace `.toast { animation: toast-enter 500ms ease-in forwards; }` with the target transition-based block.
7. Add the `@starting-style` block and reduced-motion override.
8. Preserve existing toast placement rules not shown in the snippet.

## Hard boundaries

- Do **not** animate `top`, `left`, `width`, `height`, `margin`, or `padding`.
- Do **not** introduce new dependencies.
- Do **not** change toast lifetime, stacking logic, dismissal behavior, or ARIA/live-region behavior.
- Do **not** assume every `.popover` is trigger-anchored unless the component evidence confirms it.

## Mechanical checks

- `src/styles/motion.css` should no longer contain `transition: all` or `360ms ease-in`.
- `src/components/toast.css` should no longer contain `@keyframes toast-enter`, `top: -24px`, `500ms`, or `ease-in`.
- Confirm both files include a `prefers-reduced-motion: reduce` path.
- Run the project’s existing lint/build checks if available.

## Runtime / feel checks for executor

- Open a popover slowly and confirm no unintended color/layout properties animate.
- If trigger-origin wiring exists, confirm scale/opacity appears connected to the trigger rather than the viewport center.
- Trigger a toast and confirm it moves only slightly, settles within the panel-duration rhythm, and does not feel delayed.
- In reduced-motion mode, confirm toast movement is removed but opacity feedback remains.

## Reduced Motion behavior

- Popover: keep a short `80ms` transition.
- Toast: remove translate movement; keep opacity feedback at `80ms`.

## Source-drift stop condition

Stop and report instead of editing if:
- Toast mounting is not compatible with `@starting-style` and requires a JS-mounted state.
- `.toast` relies on the keyframe’s final `top: 0` for layout in a way not represented elsewhere.
- `.popover` has been replaced by a component-scoped animation system.
- The project already has a different reduced-motion utility that should be reused.

---

# Plan 3 — Make sortable queue drag motion direct, shorter, and reduced-motion aware

- **Severity**: HIGH  
- **Category**: Gesture / performance / accessibility  
- **Estimated scope**: 1 TSX file, possible local CSS adjustment if `--drag-y` is consumed nearby

## Current evidence

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

## Target behavior

- Pointer movement should update only the actively dragged item’s transform, not a queue-level custom property that may invalidate a larger subtree.
- Release motion should be shorter and interruptible where the existing animation adapter supports it.
- Reduced Motion should preserve slot feedback but shorten/remove travel.

Target release shape:

```tsx
// src/components/SortableQueue.tsx — target shape
function onPointerUp() {
  setDragging(false);

  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  animateTo(
    nearestSlot(currentY),
    prefersReducedMotion
      ? { duration: 80 }
      : { type: "spring", duration: 0.5, bounce: 0.2 }
  );
}
```

Target pointer-move principle:

```tsx
// target principle: apply transform to the active dragged item, not queue container
draggedItemRef.current?.style.setProperty(
  "transform",
  `translate3d(0, ${currentDragY}px, 0)`
);
```

`currentDragY` must be the existing drag delta or rendered drag offset, not blindly `event.clientY` if that value is viewport-relative.

## Project conventions to follow

- Existing CSS precedent favors `transform` over layout properties.
- Existing reduced-motion precedent uses `80ms`.
- Use existing animation infrastructure; do not add a new animation dependency for this change.

## Ordered steps

1. Open `src/components/SortableQueue.tsx`.
2. Locate where `--drag-y` is consumed. If it controls many children from the queue root, replace that pattern with a ref/style update on the actively dragged row/item.
3. Add or reuse an existing `draggedItemRef` for the active item only.
4. During `onPointerMove`, compute or reuse the current drag delta and set `transform: translate3d(0, <delta>, 0)` on the dragged item.
5. Remove the queue-root write: `queueRef.current?.style.setProperty("--drag-y", ...)`.
6. In `onPointerUp`, replace `{ duration: 400 }` with:
   - `{ duration: 80 }` when `prefers-reduced-motion: reduce` matches.
   - `{ type: "spring", duration: 0.5, bounce: 0.2 }` if the existing `animateTo` adapter supports spring configs.
7. If `animateTo` does not support spring configs, use the existing closest interruptible/retargetable option. If none exists, reduce normal duration to `240` and report the lack of an interruptible adapter as follow-up.
8. Ensure cleanup clears the dragged item’s inline `transform` after it reaches the slot.

## Hard boundaries

- Do **not** add dependencies.
- Do **not** rewrite queue ordering, selection, keyboard controls, or data persistence.
- Do **not** use `top`, `left`, margin, or padding for drag movement.
- Do **not** apply transform to the whole queue unless the whole queue is intentionally moving.

## Mechanical checks

- `src/components/SortableQueue.tsx` should no longer contain `style.setProperty("--drag-y"` inside `onPointerMove`.
- `duration: 400` should be removed from the release path.
- A reduced-motion branch using `80` should exist.
- Drag movement should be expressed as `transform` / `translate3d`.

## Runtime / feel checks for executor

- Drag one item through a dense queue and confirm only the active item follows the pointer.
- Release near a slot and confirm the item settles without a long glide.
- Interrupt by dragging again quickly and confirm motion retargets rather than fighting the pointer.
- In reduced-motion mode, confirm the item still communicates final placement but with minimal travel and `80ms` timing.

## Reduced Motion behavior

- During active drag, direct manipulation should still track the pointer.
- On release, settle with `80ms` timing and avoid decorative bounce.

## Source-drift stop condition

Stop and report instead of editing if:
- `animateTo` does not accept either duration or spring-like options as shown.
- `--drag-y` is already scoped to only the active item despite being set on `queueRef`.
- The queue has keyboard reorder behavior coupled to the same motion path and the effect is unclear from code.

---

## Recommended execution order

1. **Plan 1 — Command palette**: highest frequency, smallest safe change.
2. **Plan 2 — Popover/toast CSS**: removes broad unsafe motion patterns and aligns with existing tokens.
3. **Plan 3 — Sortable queue**: highest interaction complexity; should be handled after the simpler token/cohesion fixes.

## Explicitly unverified states

- Actual route/component hierarchy.
- Whether `.popover` is always trigger-anchored.
- Whether `palette` keyframes are used elsewhere.
- Package scripts for lint/type-check/build.
- Runtime feel, frame pacing, computed styles, browser support, and reduced-motion behavior.
- Accessibility tree, focus management, live-region behavior, and keyboard reorder behavior.
- Whether `animateTo` supports spring or velocity-aware options.


## Output C

## 1. Recon summary

Reading this as a calm desktop operations console for keyboard-heavy support/revenue operators, where motion should explain state continuity without becoming latency.

- **Stack signals:** React/TSX components, CSS modules/global CSS, Tailwind-style arbitrary animation class, and an imperative `animateTo(...)` path for drag settling.
- **Where motion lives:**  
  `src/styles/motion.css` tokens + `.popover`; `CommandPalette.tsx` inline animation class; `toast.css` keyframes; `SortableQueue.tsx` pointer-driven style mutation and release animation; `Button.css` as the clean local precedent.
- **Existing conventions:** semantic tokens exist: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`. The button precedent correctly uses transform-only motion, semantic tokens, and a Reduced Motion duration of `80ms`.
- **Product personality:** crisp, quiet, utility-first, low-drama. Ease should feel responsive; long ease-in entrances are mismatched for repeated work.
- **Frequency map:**  
  High: command palette, buttons, drag/reorder queue.  
  Medium: popovers.  
  Occasional but burst-prone: toasts/status feedback.  
- **Evidence level:** static excerpts only. No runtime smoothness, computed cascade, actual keyframe definitions beyond shown snippets, browser behavior, accessibility tree, user testing, trace, or device feel was verified.

---

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | `animate-[palette_420ms_ease-in_both]` | `src/components/CommandPalette.tsx` | Command palette is likely high-frequency/keyboard-driven, but uses a long hard-coded ease-in keyframe. Static evidence shows delayed-feeling timing risk, not observed lag. | Replace with tokenized state transition using opacity + small transform, `--duration-fast`/`--ease-responsive`, and Reduced Motion opacity-only/80ms. |
| P1 | `animateTo(nearestSlot(currentY), { duration: 400 })` | `src/components/SortableQueue.tsx` | Direct manipulation release is fixed-duration and shown without velocity handoff, presentation-value retargeting, pointer capture, grab offset, or Reduced Motion path. | Preserve `nearestSlot` target semantics, but settle from current presentation value with measured CSS px/s velocity and an interruptible spring/settle primitive. |
| P2 | `top: -24px` → `top: 0`; `500ms ease-in` | `src/components/toast.css` | Toast entrance animates a layout property and uses a long ease-in. This is a performance and perceived-response risk; no dropped frames are proven. | Keep static positioning, animate `transform: translateY(...)` + opacity, use `--duration-panel` or faster, and add opacity-only Reduced Motion. |
| P2 | `transition: all 360ms ease-in`; `transform-origin: center` | `src/styles/motion.css` | Popover owns all properties and uses center-origin/ease-in. For anchored overlays this risks mismatched causality; actual anchor usage is unverified. | Limit transition to `opacity, transform`; use existing tokens; set trigger-relative origin where available, with center only for truly centered overlays. |
| P2 | Hard-coded `360/400/420/500ms` and `ease-in` appear beside semantic tokens | Multiple snippets | Motion vocabulary is fragmented despite a correct button precedent. This increases drift and makes Reduced Motion harder to keep consistent. | Normalize transient UI to `--duration-fast`, larger panels to `--duration-panel`, and `--ease-responsive`; keep exceptions documented locally. |

---

## 3. Implementation plans

### Plan A — Tokenize high-frequency overlays: command palette + popover

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

- Command palette opens/closes immediately enough for keyboard repetition.
- Motion is subtle: opacity plus small vertical/scale change, not a long keyframe.
- Popovers transition only transform/opacity and originate from their trigger when the component has anchor data.
- Existing token names remain the source of timing/easing truth.

**Project conventions to preserve**

- Use `--duration-fast`, `--duration-panel`, `--ease-responsive`.
- Follow the button precedent: transform-only, tokenized, Reduced Motion `80ms`.
- Do not introduce a new animation library for this plan.

**Ordered steps**

1. Confirm the pasted excerpts still match `src/styles/motion.css` and `src/components/CommandPalette.tsx`.
2. Locate any existing `@keyframes palette` or command-palette CSS. If it already encodes open/close, focus, or Reduced Motion behavior, stop and reconcile instead of replacing blindly.
3. Replace the arbitrary palette animation class with a stable class, for example `className="command-palette"`, while preserving `data-open={open}`.
4. Add or update CSS so closed/open states are driven by `data-open`:
   - closed: `opacity: 0; transform: translateY(-4px) scale(0.98);`
   - open: `opacity: 1; transform: translateY(0) scale(1);`
   - transition: `opacity var(--duration-fast) var(--ease-responsive), transform var(--duration-fast) var(--ease-responsive)`
5. For `.popover`, replace `transition: all 360ms ease-in` with explicit transform/opacity transitions using existing tokens.
6. Change `.popover` origin to `var(--popover-origin, center)` or an existing anchor-origin variable if one already exists. Do not invent anchor math without component evidence.
7. Add Reduced Motion branch: remove translate/scale travel, keep opacity feedback at `80ms`.

**Hard boundaries**

- Do not change search behavior, result rendering, keyboard shortcut wiring, focus ownership, or mount/unmount semantics unless the current component already requires it.
- Do not animate layout properties.
- Do not add new global token names unless multiple components demonstrably need them.

**Mechanical checks**

- Search changed files for remaining `palette_420ms`, `transition: all`, and `ease-in` on these surfaces.
- Run existing local checks if available: lint, type-check, and build. If script names differ or are absent, record that rather than inventing a pass.

**Runtime/feel checks to perform after implementation**

- Keyboard open/close repeat: no visible restart jump.
- Open while results are long/empty/loading if those states exist.
- Confirm focus indicator remains visible during and after transition.
- Inspect with motion slowed in devtools before final tuning.
- No browser/device validation has been performed for this audit.

**Reduced Motion behavior**

- `transform: none` or no spatial delta.
- `opacity` may transition for state feedback.
- Duration `80ms`, matching the button precedent.

**Source-drift stop condition**

Stop before editing if `CommandPalette` no longer renders the shown `data-open` wrapper, if `palette` keyframes already provide state-specific Reduced Motion behavior, or if `.popover` is shared by centered modal content where `center` origin is intentional.

---

### Plan B — Repair toast entrance to avoid layout animation and long ease-in

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

- Toast appears as a quick status confirmation, not a slow banner.
- Final layout position remains stable; only transform/opacity animate.
- Bursts of toasts should not require layout-property animation.

**Project conventions to preserve**

- Use existing semantic duration/easing tokens.
- Keep the toast’s existing placement and stacking model unless current CSS proves the keyframe is the only positioning source.
- Reduced Motion must preserve feedback, not remove the toast state change.

**Ordered steps**

1. Confirm `src/components/toast.css` still contains the shown `toast-enter` and `.toast` animation.
2. Inspect nearby toast positioning rules. If `top: 0` is only defined inside the keyframe, move the final `top` value into the static `.toast` positioning rule before changing the animation.
3. Replace keyframes with transform-based movement:
   - from: `transform: translateY(-24px); opacity: 0;`
   - to: `transform: translateY(0); opacity: 1;`
4. Change `.toast` timing to a semantic token:
   - preferred initial value: `animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;`
   - if toasts are used for rapid autosave/status feedback, test `--duration-fast` instead.
5. Add Reduced Motion keyframes or branch:
   - no translate movement
   - opacity-only feedback
   - `80ms`
6. If an exit animation exists elsewhere, align it separately; do not invent one in this plan.

**Hard boundaries**

- Do not change toast dismissal timers, live-region behavior, severity colors, stacking order, or message content.
- Do not claim performance improvement until runtime/trace evidence exists.
- Do not add `will-change` unless a measured problem remains.

**Mechanical checks**

- Verify `@keyframes toast-enter` no longer animates `top`.
- Search `toast.css` for hard-coded `500ms ease-in`.
- Run existing lint/build checks if available.

**Runtime/feel checks to perform after implementation**

- Trigger one toast and a burst of toasts.
- Check top-of-viewport placement does not jump before animation starts.
- Verify screen-reader/live-region behavior is unchanged if applicable.
- Check Reduced Motion OS/browser setting.
- No runtime behavior has been verified in this audit.

**Reduced Motion behavior**

- Toast still appears.
- Use opacity-only transition at `80ms`.
- No vertical travel, bounce, parallax, or delayed entrance.

**Source-drift stop condition**

Stop if toast positioning/stacking depends on animated `top` for collision management, if there is already a shared toast transition utility, or if the component has entered/exiting lifecycle requirements not visible in the excerpt.

---

### Plan C — Make `SortableQueue` release motion interruptible and velocity-aware

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

- Dragged content tracks 1:1 in a clear coordinate space.
- Release settles from the current on-screen position.
- Release velocity is measured in CSS px/s and passed into the settle animation.
- Existing target-selection semantics remain `nearestSlot(currentY)` unless product behavior explicitly authorizes momentum-based target selection.

**Project conventions to preserve**

- Keep transform-based drag via CSS variable if current CSS uses `--drag-y` for transform.
- Keep current queue ordering/data persistence behavior.
- Use Reduced Motion to remove elastic/large travel while preserving direct manipulation feedback.

**Ordered steps**

1. Confirm the shown handlers still exist in `src/components/SortableQueue.tsx`.
2. Inspect the CSS consumer of `--drag-y`. Stop if it drives layout properties instead of transform; plan a CSS ownership fix first.
3. Inspect `animateTo` API:
   - Can it cancel an active animation?
   - Can it read or start from current presentation value?
   - Can it accept spring/velocity parameters?
   - What velocity units does it expect?
4. On pointer down, store:
   - `pointerId`
   - start client position
   - current presentation Y
   - grab offset / queue-local origin
   - short sample history using monotonic timestamps
5. Use pointer capture after drag intent is established so movement remains tracked outside the original bounds.
6. On pointer move, compute queue-local/presentation delta instead of writing raw `event.clientY` directly. Update `--drag-y` through one explicit transform owner.
7. Keep hot-path work minimal: no layout reads or React state updates on every pointer move unless already batched safely.
8. On pointer up:
   - release pointer capture
   - read current presentation Y
   - compute release velocity in CSS px/s from recent samples
   - choose target with existing `nearestSlot(currentY)` behavior
   - call an interruptible settle from current Y to target with initial velocity
9. If momentum-based snap targeting is later authorized, compute a bounded projected endpoint separately and use it only for target choice; do not bundle that semantic change into this repair.
10. Cancel/retarget any in-flight settle when a new drag begins, starting from the current presentation value.

**Hard boundaries**

- Do not change which item/slot is selected unless separately approved.
- Do not block pointer input until animation completion.
- Do not introduce a large animation dependency without confirming existing project dependency policy.
- Do not combine drag translate and press scale on the same `transform` owner unless composed explicitly.

**Mechanical checks**

- Type-check the handler changes.
- Search for remaining fixed drag settle `duration: 400` on this path.
- Verify `--drag-y` is written in one coordinate convention.
- Run existing lint/type/build checks if available.

**Runtime/feel checks to perform after implementation**

- Drag slowly, flick quickly, reverse direction before release, and grab again mid-settle.
- Drag outside queue bounds and confirm capture/cleanup.
- Verify no visual jump on pointer down or interruption.
- Test long queues if this component can render many items.
- Check 60Hz and high-refresh displays if release feel is critical.
- No such runtime checks were performed for this audit.

**Reduced Motion behavior**

- Keep direct pointer tracking; it is user-controlled feedback.
- Remove bounce/elastic overshoot.
- Use short no-overshoot settle, or immediate snap with visible state confirmation if the product prefers.
- Clamp or ignore release velocity in Reduced Motion if it causes large travel.

**Source-drift stop condition**

Stop if `animateTo` already handles presentation-value interruption and velocity internally, if `nearestSlot` already uses projected endpoints, if `--drag-y` is not the active transform driver, or if pointer handlers have moved into a shared gesture abstraction.

---

## 4. Recommended execution order

1. **Plan A first:** fixes the most visible token drift and the high-frequency command surface while also correcting popover defaults.
2. **Plan B second:** small, isolated repair with clear performance-risk reduction and Reduced Motion parity.
3. **Plan C third:** highest interaction complexity; requires API inspection and runtime feel validation before approval.

## Explicitly unverified states

- Actual computed styles and cascade.
- Existence or contents of `@keyframes palette`.
- Whether global Reduced Motion rules already cover these components.
- Command palette mount/unmount behavior, focus management, and accessibility semantics.
- Popover anchoring model and whether `center` origin is intentional for some usages.
- Toast stacking, live-region behavior, and dismissal lifecycle.
- `SortableQueue` CSS transform ownership, pointer capture, grab offset, current coordinate system, `animateTo` capabilities, and release feel.
- Frame rate, layout cost, paint/composite behavior, device feel, and user perception.
