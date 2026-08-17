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

Reading this as: a calm desktop operations console for keyboard-heavy operators, optimized for fast state comprehension without decorative delay.

- **Stack signals:** React/TSX components, CSS custom properties, component CSS, and a Tailwind arbitrary animation class.
- **Where motion lives:** `src/styles/motion.css`, component-level CSS, inline style mutation in `SortableQueue`, and class-driven animation in `CommandPalette`.
- **Existing conventions:** semantic motion tokens exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`; `Button.css` is the strongest local precedent: transform-only, tokenized timing/easing, and a Reduced Motion branch.
- **Product personality:** crisp, calm, low-drama utility motion; motion should confirm causality and continuity, not create waiting time.
- **Frequency map:**
  - Very high: command palette, keyboard-triggered surfaces.
  - High/direct: sortable queue dragging.
  - Medium: popovers.
  - Occasional: toasts.
  - Local precedent: button press feedback.
- **Evidence level:** static snippet audit only. No runtime, computed-style, trace, screen recording, device, accessibility-tree, or user-test evidence was performed.

## 2. Vetted priority table

| ID | Priority | Evidence | Finding | Smallest safe correction |
|---|---:|---|---|---|
| F1 | P1 | `CommandPalette.tsx`: `animate-[palette_420ms_ease-in_both]` | High-frequency keyboard surface uses long arbitrary timing and `ease-in`, which risks delayed perceived response. Static code proves the timing/easing choice, not actual feel. | Replace with tokenized, short opacity/transform state transition; preserve instant keyboard throughput and Reduced Motion feedback. |
| F2 | P1 | `motion.css`: `.popover { transform-origin: center; transition: all 360ms ease-in; }` | Popover motion has broad property ownership, centered origin, long duration, and `ease-in`. If this is trigger-anchored UI, causality is weakened. | Use explicit `opacity, transform`; tokenized duration/easing; trigger-relative origin when the primitive exposes it. Stop if this selector is actually for centered modal content. |
| F3 | P2 | `toast.css`: `top` keyframes, `500ms ease-in` | Toast entrance animates layout position and uses a long `ease-in` keyframe. Static source proves layout-property animation risk, not dropped frames. | Move entrance to `transform: translateY(...)` + opacity, shorten to token range, and add Reduced Motion behavior. |
| F4 | P1 | `SortableQueue.tsx`: pointer move writes `--drag-y`; release `animateTo(..., { duration: 400 })` | Direct manipulation excerpt lacks visible evidence of pointer capture, grab offset, measured velocity, presentation-value interruption, or Reduced Motion settle behavior. These may exist elsewhere, so treat as an implementation risk. | Audit the full drag owner, then make drag 1:1, interruptible, transform-owned, and velocity-aware while preserving current snap semantics unless explicitly changed. |
| F5 | P2 | All snippets except `Button.css` omit Reduced Motion handling | Design authority requires a Reduced Motion path that preserves feedback; only the button precedent shows one. | Add component-specific Reduced Motion branches: reduce travel/overshoot, keep opacity/color/focus/static feedback. |
| F6 | P2 | `160ms/240ms` tokens vs `360/400/420/500ms` ad hoc values | Motion vocabulary is drifting from existing semantic tokens. | Reuse existing tokens first; introduce new semantic tokens only if repeated use justifies them. |

## 3. Implementation-ready plans

### Plan A — Normalize high-frequency overlay motion

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
<div
  data-open={open}
  className="animate-[palette_420ms_ease-in_both]"
>
```

**Target behavior**

- Command palette: immediate, keyboard-friendly state feedback; no cinematic entrance.
- Popover: explicit transform/opacity transition, responsive easing, and trigger-relative origin when available.
- All timings use existing semantic tokens unless source review proves a missing repeated semantic need.

**Project conventions**

- Reuse `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Follow the `Button.css` precedent: transform-only where possible, tokenized easing, Reduced Motion branch.
- Do not add dependencies.

**Ordered steps**

1. Confirm `src/styles/motion.css` is the correct global motion home.
2. Replace `.popover` broad transition with explicit properties:
   - `opacity`
   - `transform`
3. Change popover duration from `360ms` to `var(--duration-fast)` or `var(--duration-panel)` based on actual component size:
   - small anchored popover: `--duration-fast`
   - larger panel-like popover: `--duration-panel`
4. Before changing `transform-origin`, inspect the popover primitive/state contract:
   - if it exposes a trigger/collision origin variable, use it with a safe fallback;
   - if this selector is for centered modal-like content, stop and split modal/popover selectors instead.
5. Replace `CommandPalette` arbitrary animation class with a named class, for example `className="command-paletteMotion"`, keeping `data-open={open}`.
6. Define the command palette motion in `src/styles/motion.css` or the established component stylesheet:
   - open: `opacity: 1; transform: scale(1);`
   - closed: `opacity: 0; transform: scale(0.98);`
   - transition: `opacity var(--duration-fast) var(--ease-responsive), transform var(--duration-fast) var(--ease-responsive)`
7. Preserve `SearchResults` rendering and focus ownership; do not move data loading or keyboard handlers.
8. Add `@media (prefers-reduced-motion: reduce)`:
   - remove or minimize scale/travel;
   - keep short opacity feedback around `80ms`, matching the button precedent.

**Hard boundaries**

- Do not change command search behavior, focus restoration, keyboard shortcuts, or result ordering.
- Do not replace the popover primitive.
- Do not introduce new global animation names unless existing usage requires compatibility.
- Do not delete `palette` keyframes unless a static search proves no remaining consumers.

**Mechanical checks**

- Static search for remaining `animate-[palette`, `transition: all`, and `360ms ease-in`.
- Run the project’s closest type-check and lint scripts from the package manifest.
- If style tooling exists, run the CSS/style validation command.
- Verify no new hard-coded duration/easing values were introduced except the Reduced Motion `80ms` precedent.

**Runtime / feel checks to perform later**

- Toggle the command palette repeatedly by keyboard and ensure it does not block typing or focus.
- Open/close popovers from multiple placements and inspect computed `transform-origin`.
- Reverse open/close mid-transition.
- Use browser slow-motion animation inspection for opacity/scale sequencing.

**Reduced Motion behavior**

- Command palette and popover retain visibility/state feedback.
- Positional/scale travel is removed or minimized.
- Focus visibility remains unchanged and visible.

**Source-drift stop condition**

Stop before editing if any of these changed materially: the cited class no longer exists, `open` no longer controls visibility, `.popover` is no longer an anchored overlay, the motion tokens were renamed, or design authority changed the motion contract.

---

### Plan B — Repair toast entrance motion without layout animation

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

- Toast appears promptly and calmly.
- Movement uses transform rather than `top`.
- Timing aligns with existing motion tokens.
- Reduced Motion preserves feedback without vertical travel.

**Project conventions**

- Prefer existing `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Follow the local button precedent for Reduced Motion.
- Keep toast semantics, announcements, dismissal, and timer behavior unchanged unless the toast owner already exposes state needed for transition.

**Ordered steps**

1. Replace `top` animation with transform/opacity.
2. Prefer a transition-based entrance if the toast lifecycle exposes a mounted/open/closed state.
3. If no state attribute/class exists and adding one would require unknown lifecycle changes, use an entrance-only transform/opacity keyframe as the safe first repair.
4. Initial CSS target:
   - from: `transform: translateY(-25%); opacity: 0;`
   - to: `transform: translateY(0); opacity: 1;`
   - duration: `var(--duration-panel)` for larger toast content, otherwise `var(--duration-fast)`
   - easing: `var(--ease-responsive)`
5. If a `[data-state="closed"]` or equivalent already exists, add exit transition using the same properties instead of creating a new lifecycle model.
6. Add `@media (prefers-reduced-motion: reduce)`:
   - no vertical transform;
   - opacity transition only, approximately `80ms`.
7. Keep toast stacking, z-index, placement, ARIA live-region behavior, and dismissal controls untouched.

**Hard boundaries**

- Do not change toast copy, timeout duration, live-region semantics, or dismissal behavior.
- Do not add swipe dismissal or gesture behavior in this plan.
- Do not introduce a new toast state machine unless the current toast owner already supports state and only lacks styling.

**Mechanical checks**

- Static search confirms no `top` remains in `toast-enter`.
- Static search confirms `500ms ease-in` is removed from toast motion.
- Run closest type-check/lint/style checks available from project scripts.
- Check for remaining toast animation consumers before deleting `@keyframes toast-enter`.

**Runtime / feel checks to perform later**

- Trigger single and stacked toasts.
- Trigger toasts repeatedly in quick succession.
- Confirm no visual gap breaks pointer access to dismiss controls.
- Hide and restore the document while toast timers are active if the toast lifecycle owns timers.

**Reduced Motion behavior**

- Toast appears with opacity/static feedback.
- No vertical travel.
- Dismiss/focus/announcement behavior remains intact.

**Source-drift stop condition**

Stop before editing if `toast.css` no longer owns toast entrance styling, if `top` is being used for required layout placement rather than animation, or if the toast component has been migrated to another motion API.

---

### Plan C — Harden sortable queue drag and settle behavior

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

- Dragged item tracks the pointer 1:1 after intent is established.
- Release settles from the current on-screen value, not a stale logical value.
- Current nearest-slot behavior is preserved unless product authority explicitly approves momentum-based target selection.
- Reduced Motion removes bounce/large settle flourish but keeps direct manipulation feedback.

**Project conventions**

- Use existing animation utility `animateTo` only if it can start from current presentation value and accept or preserve velocity.
- Prefer transform-owned movement over layout-position changes.
- Do not add a new animation library unless existing primitives cannot satisfy the contract and the change is separately approved.

**Ordered steps**

1. Inspect the full drag owner around `SortableQueue.tsx` before editing.
2. Confirm whether pointer capture is set on drag start; if absent, add it when drag intent begins.
3. Preserve grab offset:
   - record pointer position and item position at drag start;
   - compute movement relative to that offset, not raw `event.clientY` alone.
4. Move `--drag-y` ownership as narrowly as possible:
   - preferred: dragged item transform owner;
   - avoid updating a broad parent variable if it invalidates a large subtree.
5. Track short time/position history using monotonic timestamps.
6. On release, calculate velocity in CSS px/s.
7. Preserve target semantics initially:
   - keep `nearestSlot(currentY)` as the snap target unless a separate product decision authorizes projected-endpoint targeting.
8. Ensure `animateTo` starts from the current rendered/presentation Y.
9. If `animateTo` cannot start from presentation value or accept velocity, stop and propose a primitive-level change rather than faking interruption with fixed-duration restart.
10. Replace fixed `duration: 400` with either:
   - existing spring/settle config if available; or
   - a bounded tokenized settle using `--duration-panel` only as a temporary non-gesture-grade fallback.
11. Ensure a new drag can interrupt an in-flight settle without visual jump.
12. Add Reduced Motion branch:
   - direct drag remains 1:1;
   - release settle is short, non-bouncy, and can snap immediately if that is the clearest feedback.

**Hard boundaries**

- Do not change queue ordering rules, slot calculation, persistence, keyboard sorting, or data model.
- Do not switch from nearest-slot to momentum-targeted slot selection without explicit approval.
- Do not combine drag translate and press scale on the same `transform` owner unless composed deliberately.
- Do not claim performance improvement without trace evidence.

**Mechanical checks**

- Type-check the component.
- Lint for pointer event cleanup and stale refs.
- Static check that pointer listeners are removed/cancelled.
- Static check that drag writes are scoped to the dragged item or documented transform owner.
- Confirm no new dependency was added.

**Runtime / feel checks to perform later**

- Drag slowly, quickly, and outside the original bounds.
- Release during movement and immediately re-grab during settle.
- Verify no jump on interruption.
- Verify grab offset is preserved.
- Verify keyboard queue operation still works.
- Test Reduced Motion mode.
- If release feel is release-critical, capture a performance trace under representative queue size.

**Reduced Motion behavior**

- User-controlled dragging remains direct.
- Release settle avoids bounce and large travel.
- State change remains understandable through position, focus, and static feedback.

**Source-drift stop condition**

Stop before editing if the cited handlers no longer own drag behavior, `animateTo` was replaced, `nearestSlot` semantics changed, keyboard sorting was added nearby and unreviewed, or queue movement is no longer transform-compatible.

## 4. Recommended execution order

1. **Plan A first:** fixes the highest-frequency keyboard and overlay motion while establishing token discipline.
2. **Plan B second:** low-risk CSS repair with clear performance/accessibility upside.
3. **Plan C third:** highest interaction complexity; should run after simpler token/RM conventions are settled.

## Explicitly unverified states

- Actual rendered timing, smoothness, frame pacing, compositing, or layout cost.
- Whether popovers are trigger-anchored, centered modal-like, or both.
- Whether command palette animation blocks focus or typing.
- Whether toast lifecycle supports open/closed transition states.
- Whether `SortableQueue` already has pointer capture, velocity tracking, grab-offset preservation, or interruption handling outside the excerpt.
- Reduced Motion behavior beyond the one provided button precedent.
- Browser, device, refresh-rate, accessibility-tree, keyboard-flow, and screen-reader behavior.


## Output B

## 1. Recon summary

- **Stack signals:** TSX components, CSS files, CSS custom-property tokens, component-local styles, and an arbitrary animation class in `className`.
- **Where motion lives:**
  - Global-ish motion tokens and shared selectors: `src/styles/motion.css`
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`
  - Component markup animation hook: `src/components/CommandPalette.tsx`
  - Pointer-driven JS animation: `src/components/SortableQueue.tsx`
- **Existing conventions visible in evidence:**
  - Semantic tokens exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`
  - Correct local precedent: `Button.css` uses explicit `transform` transition, semantic tokens, and a Reduced Motion branch that shortens rather than removes all feedback.
  - Existing authority requires crisp motion, token usage, visible focus, and Reduced Motion feedback preservation.
- **Product personality:** calm desktop operations console; motion should clarify cause/effect and state continuity while staying fast enough for repeated keyboard-heavy workflows.
- **Frequency map from snippets only:**
  - Very high: buttons, command palette
  - High: popovers
  - Medium: toasts / async feedback
  - Lower but high-salience: sortable queue drag/drop
- **Evidence level:** static snippets only. No runtime, computed-style, trace, screen recording, accessibility-tree, device, or user validation was performed.

---

## 2. Priority table

| Priority | Finding | Static evidence | Risk / product fit issue | Direction |
|---:|---|---|---|---|
| P0 | Command palette motion is long and non-tokenized | `animate-[palette_420ms_ease-in_both]` | High-frequency keyboard surface may feel delayed; arbitrary timing bypasses semantic system | Move to named/tokenized motion, shorten, add Reduced Motion path |
| P0 | Popover uses broad transition and slow ease-in | `.popover { transition: all 360ms ease-in; }` | `all` may animate unintended properties; ease-in delays feedback; no Reduced Motion branch visible | Restrict to `opacity, transform`; use existing tokens/ease |
| P1 | Toast enters via `top` over 500ms | `from { top: -24px; opacity: 0; }` and `500ms ease-in` | Slow feedback for operational alerts; position-property animation is not the crisp precedent shown elsewhere | Use stable position plus `transform`/`opacity`, tokenized duration |
| P1 | Sortable snap duration is hard-coded and slow for direct manipulation | `animateTo(..., { duration: 400 })` | Drop completion may lag user intent; no visible Reduced Motion branch | Token-align snap duration; add Reduced Motion duration branch |
| P2 | Pointer move writes style on every event | `style.setProperty("--drag-y", ...)` inside `onPointerMove` | Could over-update during drag; needs direct-manipulation smoothness without extra work | Coalesce writes with animation frame if full code confirms no existing throttle |
| P2 | Reduced Motion is inconsistent across snippets | Only `Button.css` shows `@media (prefers-reduced-motion: reduce)` | Product authority requires feedback-preserving Reduced Motion path | Apply same pattern to palette, popover, toast, sortable snap |

---

## 3. Implementation plans

### Plan A — Normalize command palette and popover overlay motion

**Files / current excerpts**

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

- Command palette and popovers should appear promptly, using small opacity/transform changes to preserve causality.
- No broad `transition: all`.
- No long `ease-in` entry on high-frequency surfaces.
- Reduced Motion should keep state feedback through short opacity/focus/visibility changes, not remove all response.

**Project conventions to follow**

- Use existing semantic tokens first:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive`
- Match the proven `Button.css` pattern: explicit animated property, tokenized duration/ease, Reduced Motion override.

**Ordered steps**

1. Read the complete versions of:
   - `src/styles/motion.css`
   - `src/components/CommandPalette.tsx`
   - any CSS file that defines `palette` keyframes or command palette classes.
2. Confirm whether `.popover` has open/closed state selectors elsewhere.
3. Replace `.popover` transition with explicit properties only:
   - `opacity`
   - `transform`
4. Use `var(--duration-fast)` for small popover transitions unless full-file evidence shows panels are intentionally used.
5. Replace the arbitrary command palette animation class with a named class or existing component class using semantic tokens.
6. Drive open/closed styling from `data-open`.
7. Ensure closed state does not trap focus or preserve interactable hidden controls; if that is already handled elsewhere, do not duplicate behavior.
8. Add Reduced Motion handling consistent with the button precedent:
   - shorten duration, e.g. `80ms`
   - avoid scale/large translation
   - preserve opacity/state feedback.

**Hard boundaries**

- Do not change search behavior, result rendering, keyboard shortcuts, focus ownership, or open/close state management unless full-file review proves motion currently owns them.
- Do not introduce new global tokens unless the complete style system lacks a suitable existing token.
- Do not add decorative bounce, overshoot, blur, or spring effects; this surface should stay operational and calm.

**Mechanical checks**

- Search for remaining `animate-[palette_420ms_ease-in_both]`.
- Search for `.popover` `transition: all`.
- Run the nearest available CSS/TS lint, type-check, and build commands after implementation.

**Runtime / feel checks to perform later, not yet performed**

- Open/close command palette repeatedly by keyboard.
- Confirm first result focus visibility is not obscured by motion.
- Open/close representative popovers.
- Check that rapid repeat invocation does not feel delayed or visually stuck.

**Reduced Motion behavior**

- Command palette: short opacity/state change; no scale or travel-heavy movement.
- Popover: short opacity change with minimal or no transform.
- Feedback remains visible.

**Source-drift stop condition**

Stop before editing if full files show an existing motion abstraction, token, animation utility, or state machine that supersedes the snippets. Re-plan against the actual abstraction rather than layering new CSS beside it.

---

### Plan B — Convert toast entry to crisp transform/opacity feedback

**File / current excerpt**

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

- Toasts should communicate arrival quickly without feeling urgent or sluggish.
- Entry should be stable-layout-oriented: use `transform` and `opacity`, not animated `top`.
- Timing should align with existing tokens.
- Reduced Motion should still provide visible arrival feedback.

**Project conventions to follow**

- Prefer `var(--duration-fast)` for quick feedback.
- Use `var(--ease-responsive)`.
- Follow `Button.css` Reduced Motion precedent by shortening duration rather than removing feedback entirely.

**Ordered steps**

1. Read the complete `src/components/toast.css`.
2. Confirm whether `.toast` positioning depends on `top` being animated or whether `top` can be a stable final value.
3. Replace keyframes with transform-based entry:
   - from: slight upward translate plus `opacity: 0`
   - to: `translateY(0)` plus `opacity: 1`
4. Set stable positioning outside the keyframes if needed, e.g. final `top` value on `.toast`.
5. Change animation duration from `500ms` to an existing token, likely `var(--duration-fast)` or at most `var(--duration-panel)` if the full design system treats toasts as panel-like.
6. Replace `ease-in` with `var(--ease-responsive)`.
7. Add `@media (prefers-reduced-motion: reduce)`:
   - reduce duration to the local precedent of `80ms`
   - remove or minimize translate distance
   - keep opacity/state feedback.

**Hard boundaries**

- Do not change toast queueing, dismissal timeout, stacking order, severity styling, or ARIA/live-region behavior unless full-file review shows motion is entangled with them.
- Do not add attention-grabbing shake, bounce, or large travel.
- Do not make Reduced Motion silent; feedback must remain perceivable.

**Mechanical checks**

- Search for other `toast-enter` definitions.
- Search for hard-coded `500ms ease-in` toast animation references.
- Run CSS lint/build or nearest project validation after implementation.

**Runtime / feel checks to perform later, not yet performed**

- Trigger one toast and a stacked sequence.
- Confirm arrival is noticeable but not distracting.
- Confirm toast text remains readable throughout entry.
- Confirm Reduced Motion still signals arrival.

**Reduced Motion behavior**

- Very short opacity transition.
- No meaningful travel.
- Same final visual state.

**Source-drift stop condition**

Stop if complete files reveal the toast position is intentionally animated for stack layout calculations or collision handling. In that case, re-plan with the owning layout logic instead of replacing keyframes in isolation.

---

### Plan C — Token-align sortable queue drag completion and reduce pointer churn

**File / current excerpt**

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

- Drag tracking should remain immediate.
- Drop-to-slot completion should be quick enough for operational throughput while preserving spatial continuity.
- Timing should use the same motion language as the rest of the interface.
- Reduced Motion should shorten the snap while preserving a clear commit state.

**Project conventions to follow**

- Prefer token-aligned durations:
  - direct manipulation completion: likely `--duration-fast` or `--duration-panel`
- Avoid decorative motion.
- Preserve feedback under Reduced Motion.

**Ordered steps**

1. Read the complete `src/components/SortableQueue.tsx`.
2. Inspect `animateTo` usage and accepted options:
   - duration units
   - easing support
   - cancellation behavior
   - current Reduced Motion handling, if any.
3. Inspect CSS that consumes `--drag-y`.
4. If no existing pointer throttling exists, coalesce `--drag-y` writes with `requestAnimationFrame`:
   - store latest `clientY`
   - write once per frame
   - cancel pending frame on pointer up/unmount.
5. Replace hard-coded `400` with a local constant derived from the design tokens or an existing shared duration constant.
6. Reduce drop snap duration to a crisp range aligned with tokens:
   - default: `160ms` to `240ms`
   - choose based on whether full code treats slot snapping as a small interaction or panel-like movement.
7. If `animateTo` supports easing, use the responsive ease equivalent.
8. Add Reduced Motion path:
   - duration around `80ms`, or immediate position commit plus visible selected/placed state if the codebase already uses that pattern.
9. Ensure pointer-up cleanup still clears dragging state and pending frame state.

**Hard boundaries**

- Do not change queue ordering rules, nearest-slot calculation, persistence, selection, keyboard behavior, or drag handles unless full-file review proves they are broken by the motion change.
- Do not remove direct visual tracking during drag.
- Do not introduce inertia or overshoot; operators need predictable placement.

**Mechanical checks**

- Search for all `animateTo(` calls to avoid inconsistent duration conventions.
- Search for hard-coded drag durations such as `400`.
- Run type-check and nearest component tests/build after implementation.
- Confirm no animation-frame leak by checking cleanup paths.

**Runtime / feel checks to perform later, not yet performed**

- Drag slowly and quickly, then release near and far from a slot.
- Confirm snap communicates final placement without delaying the next action.
- Confirm rapid repeated drags do not leave stale transforms.
- If keyboard reorder exists, confirm equivalent state feedback is preserved.

**Reduced Motion behavior**

- Drag remains directly coupled to pointer.
- Drop completion is near-immediate but still visibly commits to final slot.
- No travel amplification, bounce, or inertia.

**Source-drift stop condition**

Stop if complete code shows `animateTo` is owned by a shared animation system, physics helper, or accessibility preference layer. Update that owner or use its API instead of adding local preference/duration logic.

---

## 4. Recommended execution order

1. **Plan A first:** highest-frequency keyboard/overlay surfaces and most obvious token violation.
2. **Plan B second:** contained CSS-only improvement with clear precedent.
3. **Plan C third:** requires full interaction-code review and may touch animation scheduling.

---

## Explicitly unverified states

- Actual visual appearance, perceived speed, and interaction feel.
- Whether `palette` keyframes already exist elsewhere.
- Complete token inventory beyond the snippet.
- Actual cascade, specificity, and generated CSS output.
- Popover open/closed state model.
- Command palette focus management and keyboard behavior.
- Toast stacking, live-region behavior, and dismissal timing.
- `animateTo` API, easing support, cancellation, and ownership.
- Reduced Motion behavior outside the shown button precedent.
- Browser/device behavior, frame rate, layout cost, computed styles, and accessibility tree.


## Output C

## 1) Recon summary

- **Stack signals:** React/TSX components, plain CSS, CSS custom-property motion tokens, one Tailwind-style arbitrary animation class, and a custom/unknown `animateTo(...)` helper. No runtime motion library is proven from the excerpts.
- **Where motion lives:**  
  `src/styles/motion.css` global tokens and `.popover`; `src/components/CommandPalette.tsx` inline utility animation; `src/components/toast.css` keyframes; `src/components/SortableQueue.tsx` pointer-driven JS animation; `src/components/Button.css` local precedent.
- **Existing conventions:** semantic duration/easing tokens already exist: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`. Button precedent correctly uses transform-only feedback and a Reduced Motion duration.
- **Product personality:** calm, crisp, workday operations console. Motion should be fast, causal, low-drama, and should not tax keyboard-heavy throughput.
- **Frequency map from context/snippets:**  
  High: command palette, queue sorting/dragging.  
  Medium: popovers.  
  Occasional: toasts.  
  Baseline precedent: buttons.
- **Evidence level:** static code excerpts only. No line numbers, computed styles, runtime mount behavior, frame timing, accessibility tree, screen recording, or user/device validation available.

---

## 2) Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose, frequency, easing | `src/components/CommandPalette.tsx` | Keyboard-heavy command palette uses `palette_420ms_ease-in_both`; this is long, slow-starting, and high-frequency. | Remove entrance motion or reduce to non-spatial feedback only; preserve instant keyboard throughput. |
| 2 | HIGH | Performance, easing, physicality | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in` and `transform-origin: center`; broad property animation and slow-start easing conflict with crisp UI. | Transition only `transform, opacity`; use existing tokens; use trigger-derived origin when available. |
| 3 | HIGH | Performance, accessibility | `src/components/toast.css` | Toast animates `top` from `-24px` for `500ms ease-in`; layout property, long duration, slow start, no shown Reduced Motion path. | Animate `transform` + `opacity`, shorten to token duration, add reduced-motion fade/short duration. |
| 4 | MED-HIGH | Gesture performance, interruptibility | `src/components/SortableQueue.tsx` | Pointer move writes `--drag-y` on `queueRef`; release uses fixed `duration: 400`. Static evidence cannot prove scope, but this risks broad style recalculation and sluggish settling. | Move only the dragged item with direct transform; shorten/retarget settle; add reduced-motion snap behavior. |
| 5 | MEDIUM | Cohesion, accessibility | Multiple excerpts | Hard-coded `360ms`, `420ms`, `500ms`, `400` and `ease-in` diverge from existing tokens; Reduced Motion appears only in the button precedent. | Consolidate to semantic tokens and add Reduced Motion branches where movement remains. |

---

## 3) Implementation plans

### Plan 1 — Make overlay motion tokenized and throughput-safe

**Files / current excerpts**

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

- Command palette opens/closes without spatial animation by default; keyboard invocation should feel immediate.
- If a visual state cue is required by surrounding styles, use opacity-only feedback no longer than `80ms`; do not use transform movement.
- Popovers use only `transform` and `opacity`, no `transition: all`, no `ease-in`, and no duration above the existing token budget.
- Trigger-anchored popovers should scale from the trigger-origin custom property if the component system emits one; otherwise keep a safe fallback.

**Project conventions**

- Use existing tokens from `src/styles/motion.css`: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
- Follow the button precedent: transform-only feedback, `var(--duration-fast)`, `var(--ease-responsive)`, and a Reduced Motion duration.

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

2. In `src/components/CommandPalette.tsx`, remove the arbitrary animation class:

   ```tsx
   export function CommandPalette({ open }: { open: boolean }) {
     return (
       <div data-open={open}>
         <SearchResults />
       </div>
     );
   }
   ```

3. Search for `@keyframes palette`. If the keyframe is now unused, delete only that unused keyframe. If it is shared by other components, do not modify it in this plan.
4. Do not add new easing tokens unless another existing file already defines a semantic overlay token.

**Hard boundaries**

- Do not change command search behavior, focus management, result rendering, or mount/unmount logic.
- Do not add dependencies.
- Do not convert the command palette to a new animation library.
- If `.popover` is also used for centered modal content, stop and split the selector before changing transform origin.

**Mechanical checks**

- Confirm no `transition: all 360ms ease-in` remains in `src/styles/motion.css`.
- Confirm no `animate-[palette_420ms_ease-in_both]` remains in `src/components/CommandPalette.tsx`.
- Run the project’s existing typecheck/lint/build gates if present; exact script names are not available from the provided evidence.

**Runtime / feel checks for executor**

- Open the command palette repeatedly via keyboard: it should appear immediately, with no delayed ease-in feel.
- Open a popover slowly in animation tooling: only opacity/transform should animate.
- If trigger-origin variables are present, the popover should originate from the trigger rather than blooming from the center.

**Reduced Motion behavior**

- Command palette remains non-spatial and immediate.
- Popover keeps brief feedback at `80ms`; movement is minimized and feedback is preserved.

**Source-drift stop condition**

- Stop if either excerpt no longer matches materially, if the command palette class also contains non-motion styling, or if `.popover` is not the component class for trigger-anchored popovers.

---

### Plan 2 — Move toast entrance to compositor-safe feedback

**File / current excerpt**

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

- Toast entrance is short, crisp, and calm.
- Position is established by static layout, not animated `top`.
- Entrance uses `transform` and `opacity` only.
- Reduced Motion keeps opacity feedback while removing vertical travel.

**Project conventions**

- Reuse `--duration-panel: 240ms` for this occasional UI entrance.
- Reuse `--ease-responsive` for responsive entry.
- Mirror button precedent by shortening duration under `prefers-reduced-motion`.

**Ordered steps**

1. Replace the keyframe with transform/opacity movement:

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

2. Update `.toast` so the final position is static and the animation is tokenized:

   ```css
   .toast {
     top: 0;
     animation: toast-enter var(--duration-panel) var(--ease-responsive) both;
   }
   ```

3. Add a reduced-motion keyframe and media query:

   ```css
   @keyframes toast-enter-reduced {
     from { opacity: 0; }
     to { opacity: 1; }
   }

   @media (prefers-reduced-motion: reduce) {
     .toast {
       animation-name: toast-enter-reduced;
       animation-duration: 120ms;
     }
   }
   ```

**Hard boundaries**

- Do not alter toast content, stacking logic, dismissal timing, ARIA/live-region behavior, or z-index.
- Do not introduce blur, bounce, or decorative stagger.
- Do not change the toast’s final layout position except making `top: 0` explicit if the current keyframe was providing it.

**Mechanical checks**

- Confirm `top: -24px` no longer appears in `src/components/toast.css`.
- Confirm `animation: toast-enter 500ms ease-in forwards` no longer appears.
- Confirm a `prefers-reduced-motion: reduce` block exists in `src/components/toast.css`.
- Run existing project CSS/type/build gates if present; exact commands are not available from the evidence.

**Runtime / feel checks for executor**

- Trigger one toast: it should enter quickly without feeling delayed at the start.
- Trigger multiple toasts if supported: no layout-position animation should be visible.
- In slow playback, confirm the toast translates subtly from `-8px` to `0`, not from `top: -24px`.

**Reduced Motion behavior**

- Toast fades in over `120ms`.
- No vertical travel in Reduced Motion.

**Source-drift stop condition**

- Stop if toast positioning is no longer controlled by `top`, if the class name changed, or if a separate toast animation system already replaced this CSS.

---

### Plan 3 — Make sortable queue dragging direct, shorter, and interruptible

**File / current excerpt**

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

- During drag, only the actively dragged item moves.
- Drag movement is direct and pointer-causal, using `transform: translate3d(...)`.
- Release settle is shorter than the current `400ms`, retargetable/cancelable if the user starts another drag.
- Reduced Motion preserves drag feedback but shortens automated settling.

**Project conventions**

- Use transform-only movement, consistent with the existing button precedent.
- Use the existing responsive easing value: `cubic-bezier(0.23, 1, 0.32, 1)`.
- Prefer existing local helpers over new dependencies.

**Ordered steps**

1. Inspect the component to identify the element representing the actively dragged queue item.
2. If `queueRef` points to the whole list/container, stop using it for per-frame drag motion. Add or reuse a ref for only the dragged item.
3. Track drag start and current offset as relative movement, not absolute viewport `clientY`:

   ```tsx
   const dragStartYRef = useRef(0);
   const currentYRef = useRef(0);
   ```

4. On pointer down/start, set `dragStartYRef.current` to the starting `clientY`.
5. Replace the pointer-move write with direct transform on the dragged item:

   ```tsx
   function onPointerMove(event: PointerEvent) {
     const y = event.clientY - dragStartYRef.current;
     currentYRef.current = y;

     if (draggedItemRef.current) {
       draggedItemRef.current.style.transform = `translate3d(0, ${y}px, 0)`;
     }
   }
   ```

6. Update pointer release to use the tracked offset and a shorter settle:

   ```tsx
   function onPointerUp() {
     setDragging(false);

     const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
     const duration = prefersReducedMotion ? 80 : 220;

     animateTo(nearestSlot(currentYRef.current), {
       duration,
       easing: "cubic-bezier(0.23, 1, 0.32, 1)",
     });
   }
   ```

7. Before starting a new settle animation, cancel or retarget any in-flight settle if the existing `animateTo` helper supports it. If it does not, do not invent a new animation engine in this plan; shorten the duration and document the limitation.

**Hard boundaries**

- Do not change queue ordering rules, slot calculation, persistence, keyboard controls, or data model.
- Do not add a new gesture or animation dependency.
- Do not animate layout properties such as `top`, `left`, `height`, or `margin`.
- Do not apply the drag transform to the whole queue unless the excerpt proves `queueRef` is actually the dragged item.

**Mechanical checks**

- Confirm `setProperty("--drag-y"` no longer appears in `src/components/SortableQueue.tsx`.
- Confirm the release settle no longer uses `{ duration: 400 }`.
- Confirm the drag path writes `transform` to the dragged item only.
- Run existing TypeScript/lint/build gates if present; exact scripts are not available from the provided evidence.

**Runtime / feel checks for executor**

- Drag an item slowly: the item should track the pointer directly with no visible lag from the rest of the list.
- Release near a slot: settle should feel crisp, not languid.
- Start another drag during or immediately after settle: if the helper supports cancellation, motion should retarget instead of fighting the pointer.
- In slow playback, confirm only transform changes during drag/settle.

**Reduced Motion behavior**

- Direct manipulation remains: the item still follows the pointer.
- Automated settle is shortened to `80ms`; no bounce or decorative movement is added.

**Source-drift stop condition**

- Stop if `animateTo` does not accept an easing option and cannot be safely changed locally, if `currentY` has different semantics than drag offset, or if the component has already moved to a dedicated drag library.

---

## 4) Recommended execution order

1. **Plan 1:** highest throughput impact; removes the most visible slow-start overlay motion.
2. **Plan 2:** low-risk compositor/accessibility win for occasional feedback.
3. **Plan 3:** high-value but requires more local code inspection because `animateTo`, refs, and drag semantics are not fully shown.

## Explicitly unverified states

- Actual `DESIGN.md` contents beyond the provided summary.
- Package manager, scripts, build commands, and test gates.
- Runtime mount/unmount behavior for command palette, popovers, and toasts.
- Whether popovers receive trigger-origin CSS variables.
- Whether `queueRef` points to the whole queue or the active dragged item.
- `animateTo` API, cancellation support, easing support, and current interruption behavior.
- Actual frame rate, layout/composite cost, reduced-motion behavior, keyboard focus behavior, and accessibility-tree output.
