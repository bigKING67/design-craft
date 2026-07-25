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

- **Stack signals**: React/TSX components, plain CSS, semantic CSS custom properties, Tailwind-style arbitrary animation class in `CommandPalette`, and an unknown JS `animateTo(...)` helper for drag release.
- **Where motion lives**:
  - Global tokens/rules: `src/styles/motion.css`
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`
  - Inline/utility animation: `src/components/CommandPalette.tsx`
  - Pointer-driven JS motion: `src/components/SortableQueue.tsx`
- **Existing conventions**:
  - Tokens: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
  - Correct precedent: button press uses `transform`, semantic duration/easing tokens, and `prefers-reduced-motion` keeps feedback at `80ms`.
- **Product personality**: calm, crisp, low-latency desktop operations UI. Motion should clarify cause/effect, not decorate or delay frequent work.
- **Frequency map**:
  - Very high: command palette, likely keyboard-triggered.
  - Medium/high: popovers in operational workflows.
  - Medium: sortable queue dragging when used.
  - Occasional: toasts.
- **Evidence level**: static snippet audit only. No runtime timing, computed style, browser validation, accessibility tree, performance trace, or device gesture validation was performed.

---

## 2. Vetted priority table

| # | Severity | Location | Evidence | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | `src/components/CommandPalette.tsx` | `animate-[palette_420ms_ease-in_both]` | High-frequency keyboard UI is animated for `420ms` with `ease-in`, delaying the exact action operators expect to feel instant. | Remove command palette entrance/exit animation; rely on immediate open state and visible focus. |
| 2 | HIGH | `src/components/SortableQueue.tsx` | `setProperty("--drag-y", ...)` on `queueRef`; `animateTo(..., { duration: 400 })` | Drag motion is likely routed through a parent CSS variable and release uses a fixed `400ms` tween; this risks style recalculation, weak direct manipulation, and no velocity continuity. | Move the dragged item with direct `transform`; release with velocity-aware spring if supported; reduced motion snaps/settles quickly. |
| 3 | HIGH | `src/styles/motion.css` | `.popover { transform-origin: center; transition: all 360ms ease-in; }` | Popovers use `transition: all`, slow `ease-in`, over-budget duration, and center origin for a trigger-anchored surface. | Restrict to `transform, opacity`; use existing tokens; source origin from trigger/positioner; add reduced-motion duration. |
| 4 | MEDIUM | `src/components/toast.css` | `top` keyframes; `500ms ease-in` | Toast enter animates layout property `top`, lasts too long for operations UI, starts slowly, and lacks reduced-motion handling. | Animate `transform` + `opacity` only; shorten to `--duration-panel`; reduced motion keeps opacity feedback without vertical travel. |
| 5 | MEDIUM | Cross-cutting snippets | Button uses tokens/reduced motion; other excerpts bypass them | Motion system is inconsistent: semantic tokens exist, but several components hard-code `360/420/500ms`, `ease-in`, arbitrary classes, or no reduced-motion path. | Consolidate high-traffic motion onto existing tokens and the button precedent. |

---

## 3. Implementation-ready plans

### Plan 1 — Make command palette instant

**Files / current excerpt**

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

- Opening/closing the command palette should be immediate.
- No `420ms`, no `ease-in`, no keyframe/utility entrance motion.
- Feedback should come from state continuity and visible focus, not panel motion.
- Reduced Motion behavior is identical because the baseline has no movement.

**Project conventions**

- Prefer existing semantic tokens and local precedents when motion remains.
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

1. In `src/components/CommandPalette.tsx`, remove the arbitrary animation class.
2. Target shape:

```tsx
export function CommandPalette({ open }: { open: boolean }) {
  return (
    <div data-open={open}>
      <SearchResults />
    </div>
  );
}
```

3. If another stylesheet depends on the removed class/keyframe only for visibility, replace that dependency with explicit open/closed state styling, not animation.
4. If a `palette` keyframe exists only for this component and becomes unused, remove it in the same change; if it is shared elsewhere, stop and report the shared usage.

**Hard boundaries**

- Do not change `SearchResults`.
- Do not add a new animation, fade, scale, or transition as a substitute.
- Do not change command behavior, keyboard shortcuts, search state, or focus management.
- If the class is required for mount/unmount correctness rather than decoration, stop and report before editing further.

**Mechanical checks**

- Search confirms `animate-[palette_420ms_ease-in_both]` is gone.
- Search confirms this component no longer references `420ms` or `ease-in`.
- Run the closest available lint/typecheck/build command if present.

**Runtime/feel checks for executor**

- Open via keyboard repeatedly: palette appears immediately with no perceptible easing delay.
- Close/reopen rapidly: no animation queues, no delayed visual state.
- Confirm visible focus remains clear on open.
- With Reduced Motion enabled: behavior is the same and still understandable.

**Reduced Motion behavior**

- No movement in either mode.
- Preserve focus visibility and state indication.

**Source-drift stop condition**

- Stop if the current file no longer contains the provided excerpt or if command palette visibility depends on the animation class for correctness.

---

### Plan 2 — Retokenize popover and toast motion

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

- Popovers feel responsive and causally connected to their trigger.
- Toasts enter without layout animation.
- Motion uses existing semantic duration/easing tokens.
- Reduced Motion keeps opacity/state feedback but removes vertical movement.

**Project conventions**

- Use:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Follow the button precedent: transform-only motion, tokenized duration/easing, `80ms` reduced-motion duration.

**Ordered steps**

1. In `src/styles/motion.css`, replace the popover rule with transform/opacity-only transitions:

```css
.popover {
  transform-origin: var(--popover-transform-origin, var(--transform-origin, center));
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

2. Verify the popover implementation can set `--popover-transform-origin` or `--transform-origin` from its trigger/positioning system. If not, stop and report rather than leaving all trigger popovers centered by default.
3. If `.popover` is actually used for centered modal surfaces, do not apply this change globally. Split trigger-anchored popovers from centered dialogs first.
4. In `src/components/toast.css`, replace layout animation with transform/opacity:

```css
@keyframes toast-enter {
  from {
    transform: translateY(-24px);
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

**Hard boundaries**

- Do not introduce new duration/easing tokens unless the existing tokens are unavailable.
- Do not animate `top`, `left`, `width`, `height`, margin, or padding.
- Do not use `transition: all`.
- Do not change toast content, dismissal behavior, stacking logic, or ARIA behavior.
- Do not change modal/dialog origin unless the surface is confirmed trigger-anchored.

**Mechanical checks**

- Search confirms no `transition: all` remains on `.popover`.
- Search confirms no `.toast` enter animation uses `top`.
- Search confirms these excerpts no longer use `360ms ease-in` or `500ms ease-in`.
- Run lint/typecheck/build if available.

**Runtime/feel checks for executor**

- Popover: at slow playback, motion originates from the trigger/anchor, not the center.
- Popover: rapid open/close feels responsive and does not start with a sluggish delay.
- Toast: at slow playback, the element moves via transform; surrounding layout should not be pushed by the enter animation.
- Reduced Motion: popover still changes state quickly; toast fades in without vertical travel.

**Reduced Motion behavior**

- Popover: shorten transition to `80ms`.
- Toast: remove vertical movement; keep `80ms` opacity feedback.

**Source-drift stop condition**

- Stop if `.popover` is shared by centered modals/dialogs.
- Stop if no trigger-origin variable can be provided by the current popover implementation.
- Stop if toast mounting/unmounting is controlled by JS that conflicts with the proposed animation timing.

---

### Plan 3 — Make sortable queue drag direct and velocity-aware

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

- While dragging, the dragged item follows the pointer directly with `transform`.
- Do not update a parent CSS variable for every pointer move.
- On release, settle to the nearest slot with velocity continuity if the existing animation helper supports it.
- Reduced Motion preserves direct dragging but avoids a long animated glide on release.

**Project conventions**

- Use transform-based motion like the button precedent.
- Use existing durations where fixed timing is unavoidable:
  - normal small UI feedback: `--duration-fast` / `160ms`
  - reduced motion: `80ms`
- Do not add a new animation dependency.

**Ordered steps**

1. Identify the actual dragged element ref. If only `queueRef` exists and there is no per-item dragged ref, add the smallest local ref needed for the active dragged item.
2. Replace parent CSS variable updates with direct transform on the dragged element:

```tsx
function onPointerMove(event: PointerEvent) {
  const deltaY = event.clientY - dragStartY.current;
  draggedItemRef.current?.style.setProperty(
    "transform",
    `translate3d(0, ${deltaY}px, 0)`
  );
}
```

3. Track release velocity from recent pointer samples:

```tsx
const now = performance.now();
const dy = event.clientY - lastPointerY.current;
const dt = Math.max(now - lastPointerTime.current, 1);
velocityY.current = dy / dt;
lastPointerY.current = event.clientY;
lastPointerTime.current = now;
```

4. Replace fixed release timing:

```tsx
function onPointerUp() {
  setDragging(false);

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const targetY = nearestSlot(currentY);

  if (reduceMotion) {
    animateTo(targetY, { duration: 80 });
    return;
  }

  animateTo(targetY, {
    type: "spring",
    duration: 0.5,
    bounce: 0.2,
    velocity: velocityY.current,
  });
}
```

5. If `animateTo` does not support spring, bounce, or velocity options, stop and report. Do not approximate with another long fixed-duration tween.
6. Remove any CSS that consumes `--drag-y` for the dragged item once direct transform is in place.

**Hard boundaries**

- Do not change queue ordering rules.
- Do not change `nearestSlot(...)` behavior.
- Do not add a physics/gesture dependency.
- Do not animate layout properties.
- Do not apply transforms to the whole queue when only one item is being dragged.
- Do not invent a spring API if the existing `animateTo` helper cannot support it.

**Mechanical checks**

- Search confirms `setProperty("--drag-y"` is removed from `SortableQueue`.
- Search confirms `{ duration: 400 }` is removed from drag release.
- Typecheck confirms refs and pointer state are valid.
- Lint confirms no stale refs/state are left behind.

**Runtime/feel checks for executor**

- Drag slowly: item remains directly under the pointer with no laggy catch-up.
- Drag quickly and release: item settles in the direction/speed implied by the release, not as a generic fixed tween.
- Interrupt/re-drag during settlement: motion retargets from the current visual position.
- Reduced Motion: drag remains direct; release settles quickly without a long glide or bounce.

**Reduced Motion behavior**

- Direct pointer tracking remains because it is user-controlled feedback.
- Release animation uses `80ms` and no bounce/overshoot.

**Source-drift stop condition**

- Stop if there is no stable dragged-item element to transform directly.
- Stop if `animateTo` cannot accept spring/velocity options.
- Stop if current queue virtualization or layout measurement depends on `--drag-y` globally.

---

## 4. Recommended execution order

1. **Command palette instant open** — highest-frequency, smallest change, biggest throughput win.
2. **Popover/toast retokenization** — removes several systemic anti-patterns: `ease-in`, overlong UI durations, `transition: all`, layout animation, missing reduced-motion paths.
3. **Sortable queue drag** — high impact but requires source confirmation around refs, `animateTo`, and queue layout.

## Explicitly unverified states

- Whether `.popover` is trigger-anchored everywhere or shared with centered modal/dialog UI.
- Whether a positioning library exposes a transform-origin CSS variable.
- Whether `palette` keyframes exist elsewhere or affect mount/unmount behavior.
- Whether `animateTo` supports spring, velocity, interruptibility, or reduced-motion branching.
- Whether the sortable queue is virtualized or has layout measurement constraints.
- Actual frame rate, input latency, compositing behavior, focus behavior, screen-reader announcements, and perceived feel on real hardware.


## Output B

## 1. Recon summary

- **Stack signals:** React/TSX components, CSS modules/global CSS, Tailwind-style arbitrary animation class in `CommandPalette`, imperative JS animation call in `SortableQueue`.
- **Where motion lives:** semantic tokens in `src/styles/motion.css`; component CSS in `toast.css` and `Button.css`; inline utility animation in `CommandPalette.tsx`; imperative gesture settle in `SortableQueue.tsx`.
- **Existing conventions:** `--duration-fast`, `--duration-panel`, `--ease-responsive`; correct local precedent animates only `transform`, uses semantic tokens, and shortens duration under `prefers-reduced-motion`.
- **Product personality:** calm, crisp, utilitarian desktop operations surface; motion should explain causality and preserve continuity, not add cinematic delay.
- **Frequency map:**  
  - High frequency: buttons, command palette, queue dragging.  
  - Medium frequency: popovers.  
  - Episodic: toasts.  
- **Evidence level:** static snippets only. No runtime feel, computed styles, trace, accessibility tree, browser, device, or user validation was performed.

## 2. Priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | `animate-[palette_420ms_ease-in_both]` | `src/components/CommandPalette.tsx` | Command palette uses a long, accelerating entry for a keyboard-heavy surface. Static evidence also shows no local Reduced Motion branch. | Move to named CSS using semantic duration/easing tokens; make open/closed states retargetable; reduce travel and duration under Reduced Motion. |
| P1 | `transition: all 360ms ease-in; transform-origin: center;` | `src/styles/motion.css` | Popover motion is broad, slow, accelerating, and center-origin by default. For anchored overlays this risks weak causality; static evidence does not prove actual placement. | Limit transitioned properties, use existing tokens, and make origin trigger-aware where the component can supply placement. |
| P1 | `animateTo(nearestSlot(currentY), { duration: 400 })` | `src/components/SortableQueue.tsx` | Drag settle appears fixed-duration and does not show velocity handoff, pointer capture, grab offset, or Reduced Motion behavior. Static evidence cannot prove gesture feel, but this is the highest-risk direct-manipulation path. | Preserve current target semantics, add measured release velocity and presentation-value settle; add Reduced Motion non-elastic settle. |
| P2 | `@keyframes` changes `top`; `.toast { animation: ... 500ms ease-in }` | `src/components/toast.css` | Toast enter animates layout-position property with long ease-in timing and no shown Reduced Motion path. Static evidence cannot prove dropped frames. | Animate `transform` + `opacity`, shorten to panel/fast token range, and reduce vertical travel under Reduced Motion. |
| P2 | Multiple hard-coded durations/easings: `360ms ease-in`, `420ms ease-in`, `500ms ease-in`, `400` | Multiple | Motion language is fragmented despite existing semantic tokens and a correct local precedent. | Route transient UI through the existing motion tokens; add only narrowly scoped new tokens if current tokens are insufficient. |
| P3 | Correct precedent exists: transform-only button with Reduced Motion duration | `src/components/Button.css` | Good local pattern is not propagated to overlays, toast, and gesture settle. | Use the button pattern as the minimum convention: explicit animated properties, semantic timing, Reduced Motion feedback retained. |

## 3. Implementation plans

### Plan 1 — Normalize command palette and popover transient motion

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

- Command palette opens immediately enough for keyboard-heavy use: short opacity/transform transition, no long accelerating delay.
- Popovers animate only properties that communicate entrance/exit, typically `opacity` and `transform`.
- Anchored overlays should originate from the trigger or placement when that information exists; centered origin is acceptable only for genuinely centered surfaces.
- Reduced Motion keeps state feedback through opacity/color/static state, with little or no spatial travel.

**Project conventions**

- Use `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Follow the local precedent from `src/components/Button.css`: explicit property transition, transform-based feedback, Reduced Motion override.

**Ordered steps**

1. In `src/styles/motion.css`, replace `.popover` broad transition with explicit properties, for example:
   - `transition-property: opacity, transform;`
   - `transition-duration: var(--duration-panel);`
   - `transition-timing-function: var(--ease-responsive);`
2. Do not keep `transition: all`; if other properties currently rely on it, split them into explicit transitions before removal.
3. Change `.popover` origin from unconditional `center` to a placement-aware value only if the component already exposes placement/origin data. If not, keep behavior stable and add a narrow variable contract such as `transform-origin: var(--popover-origin, center);`.
4. In `src/components/CommandPalette.tsx`, remove the arbitrary animation class and use a named class or data-state styles controlled by `data-open={open}`.
5. Define command palette styles in the existing relevant stylesheet location, using `opacity` plus small `translateY`/scale if needed; avoid keyframe restart unless mount/unmount lifecycle requires it.
6. Add `@media (prefers-reduced-motion: reduce)` for both popover and palette: duration around the existing reduced precedent, with spatial movement removed or reduced to a minimal transform.

**Hard boundaries**

- Do not redesign command palette layout, search behavior, focus management, or result rendering.
- Do not add a motion library for this plan.
- Do not introduce new global animation tokens unless existing tokens cannot express the required distinction.
- Do not claim trigger-relative origin is fixed until the actual popover placement API is inspected.

**Mechanical checks**

- Run the project’s existing type check for the TSX change.
- Run the project’s existing CSS/lint/build gate.
- Grep/check that `CommandPalette.tsx` no longer contains `animate-[palette_420ms_ease-in_both]`.
- Grep/check that `.popover` no longer uses `transition: all`.

**Runtime/feel checks to perform later**

- Open/close the command palette repeatedly via keyboard; acceptance: no perceived delay before results become available, no restart jump on rapid toggle.
- Open popovers from each supported placement; acceptance: motion appears anchored to the trigger where placement data exists.
- Check interrupted open/close sequences; acceptance: transition retargets from current visual state.

**Reduced Motion behavior**

- Palette/popover should still communicate open/closed state through opacity or immediate visibility.
- Remove large travel and avoid delayed keyframe entrance.
- Keep focus indicators visible and unaffected by motion reduction.

**Source-drift stop condition**

- Stop before editing if `CommandPalette` no longer renders the shown `data-open` wrapper, if `.popover` is no longer defined in `src/styles/motion.css`, or if motion tokens are renamed/removed.

---

### Plan 2 — Convert toast entrance from layout animation to tokenized transform feedback

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

- Toasts enter briskly without layout-position animation.
- Motion communicates arrival from the notification region but does not feel like a slow banner slide.
- Repeated toasts should not depend on a long keyframe that restarts from an unrelated position.
- Reduced Motion preserves visibility feedback without vertical travel.

**Project conventions**

- Prefer `transform` and `opacity`.
- Use `--duration-panel` or `--duration-fast`; avoid hard-coded `500ms ease-in`.
- Match the existing reduced-duration precedent from `Button.css`.

**Ordered steps**

1. In `src/components/toast.css`, change `@keyframes toast-enter` from `top` animation to `transform` and `opacity`, for example:
   - `from { transform: translateY(-8px); opacity: 0; }`
   - `to { transform: translateY(0); opacity: 1; }`
2. Change `.toast` timing to a semantic token:
   - `animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;`
3. Confirm the toast’s static positioning still owns `top`/placement outside the animation. If `top` is only present in the keyframe, add stable positioning separately before removing animated `top`.
4. Add `@media (prefers-reduced-motion: reduce)`:
   - reduce duration to the local reduced precedent,
   - remove or nearly remove `translateY`,
   - keep opacity feedback.
5. If toast exit animation exists elsewhere, align it with the same property set and Reduced Motion rule; do not invent an exit path if none exists.

**Hard boundaries**

- Do not change toast copy, stacking, dismissal timing, z-index, or notification semantics.
- Do not claim frame-rate improvement without trace evidence.
- Do not add `will-change` unless later profiling proves it helps.

**Mechanical checks**

- Run existing CSS/lint/build gate.
- Static check: `toast-enter` should no longer animate `top`.
- Static check: `.toast` should no longer contain `500ms ease-in`.

**Runtime/feel checks to perform later**

- Trigger single and multiple toasts; acceptance: toast appears promptly, from a short travel distance, without obvious layout jump.
- Trigger toasts while other page content is busy; acceptance requires browser observation or trace, not static inference.
- Verify toast does not block keyboard workflow or focus visibility.

**Reduced Motion behavior**

- Toast appears with short opacity feedback.
- Vertical travel is removed or reduced to a barely perceptible amount.
- State remains understandable; toast must not become invisible until animation completes.

**Source-drift stop condition**

- Stop before editing if toast positioning has moved out of `src/components/toast.css`, if `toast-enter` is already replaced, or if the toast component relies on animated `top` for stacking logic.

---

### Plan 3 — Make queue drag settle interruptible and velocity-aware without changing slot semantics

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

- While dragging, the item tracks the pointer in a clear coordinate space without jumping.
- Release settlement starts from the current on-screen value and carries measured release velocity.
- Existing target selection, `nearestSlot(currentY)`, is preserved unless product authority explicitly approves momentum-based target selection.
- Reduced Motion removes elastic/large travel while retaining deterministic slot placement feedback.

**Project conventions**

- Direct manipulation may use imperative animation, but it must not fight CSS transform ownership.
- Use semantic duration/easing where fixed timing remains necessary.
- Preserve calm operations-console motion: no playful bounce unless already authorized.

**Ordered steps**

1. Inspect the full `SortableQueue.tsx` before editing to identify:
   - coordinate space of `currentY`,
   - how `--drag-y` is consumed,
   - whether the dragged element uses `transform`, `top`, or another property,
   - whether pointer capture and grab offset already exist outside the excerpt.
2. On pointer down/start, capture:
   - pointer id,
   - starting pointer `clientY`,
   - element presentation `y`,
   - grab offset,
   - short movement history with monotonic timestamps.
3. On pointer move, update drag position in component-local CSS pixels, not raw viewport `clientY`, unless existing CSS explicitly expects viewport coordinates.
4. Ensure only one owner composes transforms. If press/drag/settle all write `transform`, split wrapper layers or compose a single transform string.
5. On pointer up, compute release velocity in CSS px/s from recent samples.
6. Keep current target rule initially:
   - `target = nearestSlot(currentY)` or the equivalent current semantic.
   - Feed measured velocity into `animateTo` if the API supports it.
   - If the API does not support velocity, replace or wrap it with a spring/WAAPI mechanism that can start from current presentation value and velocity.
7. Add an explicit authorization checkpoint before momentum target selection:
   - compute bounded projected endpoint only as an experiment,
   - do not use it to choose a slot unless approved by product/runtime evidence.
8. Add Reduced Motion branch:
   - no overshoot,
   - shorter settle,
   - deterministic transform/position update,
   - same final slot.

**Hard boundaries**

- Do not change queue ordering rules, nearest-slot semantics, persistence, selection, or keyboard behavior.
- Do not add a new animation dependency unless existing primitives cannot read current value and accept initial velocity.
- Do not replace slot targeting with momentum projection by default.
- Do not claim touch/device feel correctness without later runtime validation.

**Mechanical checks**

- Run existing type check.
- Run existing unit tests covering queue reorder behavior, if present.
- Add or update tests only if the project already has a suitable test layer for reorder math; otherwise keep this as implementation plus runtime validation.
- Static check that release velocity is measured with units documented in code comments or helper names.
- Static check that Reduced Motion branch exists for the settle path.

**Runtime/feel checks to perform later**

- Drag slowly, release near slot boundary; acceptance: current nearest-slot behavior is preserved.
- Flick and release; acceptance: item settles from current visual position without a jump and without input lockout.
- Interrupt a settling item by grabbing it again; acceptance: no snap back to old logical target.
- Drag outside original bounds; acceptance depends on pointer capture or equivalent behavior.
- Measure under realistic list size before claiming performance quality.

**Reduced Motion behavior**

- Item still lands in the correct slot.
- Remove bounce/elasticity and large secondary motion.
- Keep immediate state feedback through position change, selection/drag state styling, or other non-vestibular cue.

**Source-drift stop condition**

- Stop before editing if `animateTo` has a different signature than assumed, if `nearestSlot(currentY)` is no longer the release target, if `--drag-y` is not used for visual drag position, or if another module owns drag physics.

## 4. Recommended execution order

1. **Plan 3: SortableQueue** — highest interaction risk because direct manipulation needs continuity, interruption, and velocity handling.
2. **Plan 1: Command palette + popover** — high-frequency keyboard/overlay motion and broad `transition: all` cleanup.
3. **Plan 2: Toast** — bounded but worthwhile cleanup from layout-position animation to transform/opacity.

## Explicitly unverified states

- Actual frame rate, paint/layout cost, compositor behavior, and style recalculation scope.
- Real keyboard throughput impact of the command palette animation.
- Popover placement/origin behavior and whether `center` is currently intentional for some surfaces.
- Toast stacking, exit animation, and whether animated `top` is coupled to layout logic.
- Sortable queue pointer capture, grab offset, current-value interruption, transform ownership, and animation API capabilities outside the excerpt.
- Actual Reduced Motion behavior in browser settings.
- Accessibility-tree behavior, focus order, focus visibility during transitions, and screen-reader timing.


## Output C

## 1. Recon summary

**Stack signals**
- React/TSX components with CSS files.
- CSS custom properties for semantic motion tokens:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Mixed motion implementation styles:
  - global CSS selector: `.popover`
  - component class animation: `animate-[palette_420ms_ease-in_both]`
  - component CSS keyframes: `toast-enter`
  - imperative pointer animation: `animateTo(...)`

**Where motion currently lives**
- `src/styles/motion.css`: shared duration/easing tokens plus `.popover`.
- `src/components/CommandPalette.tsx`: inline utility animation string.
- `src/components/toast.css`: keyframe animation using `top`.
- `src/components/SortableQueue.tsx`: pointer-driven custom property and hardcoded snap animation.
- `src/components/Button.css`: good local precedent for semantic tokens and Reduced Motion.

**Existing conventions**
- Prefer `transform` over layout properties.
- Prefer semantic duration/easing tokens over literal durations/easings.
- Reduced Motion should preserve feedback, not erase it.
- Existing local precedent uses:
  - `transition: transform var(--duration-fast) var(--ease-responsive);`
  - `@media (prefers-reduced-motion: reduce) { ... transition-duration: 80ms; }`

**Product personality**
- Calm desktop operations surface.
- Motion should clarify causality and state continuity.
- Motion should not slow high-frequency keyboard workflows.
- Avoid decorative, delayed, or “presentation” motion.

**Frequency map, based only on component roles**
- Very high frequency: buttons, command palette open/close, popovers.
- Medium frequency: toasts/status feedback.
- Episodic but interaction-sensitive: sortable queue drag/snap.
- Unknown: exact invocation counts, user paths, mount/unmount behavior, and whether these components appear in dense table workflows.

**Evidence level**
- Static code evidence only.
- No runtime, computed-style, animation trace, browser, device, accessibility-tree, screen recording, or user testing evidence.
- All performance and accessibility risks below are implementation risks, not observed runtime failures.

---

## 2. Priority table

| Priority | Finding | Static evidence | Risk | Target |
|---:|---|---|---|---|
| P0 | Motion system is inconsistent across files | `360ms ease-in`, `420ms ease-in`, `500ms ease-in`, `400`, plus tokenized button precedent | Operators may experience uneven timing and delayed feedback across frequent UI actions | Standardize around existing semantic tokens: `--duration-fast`, `--duration-panel`, `--ease-responsive`, with `80ms` Reduced Motion precedent |
| P0 | Reduced Motion exists only in the button evidence | `Button.css` has `prefers-reduced-motion`; other excerpts do not | Users requesting reduced motion may still receive long entrance/snap animations | Add Reduced Motion branches to palette, popover, toast, and sortable snap while preserving state feedback |
| P1 | `.popover` uses `transition: all` | `transition: all 360ms ease-in;` | Future style changes may accidentally animate layout, color, size, or shadow | Restrict to `transform, opacity` or the exact properties intentionally animated |
| P1 | Toast animates layout property `top` | `from { top: -24px; opacity: 0; } to { top: 0; opacity: 1; }` | Layout-position animation can be harder to reason about and less composited than transform-based feedback | Use `transform: translateY(...)` plus opacity |
| P1 | Command palette uses hardcoded arbitrary animation | `className="animate-[palette_420ms_ease-in_both]"` | Keyboard-heavy entry point may feel slower than the system’s own panel duration | Move to named class/data-state CSS using `--duration-panel` and responsive easing |
| P2 | Sortable queue snap is hardcoded and pointer updates are ungoverned | `setProperty("--drag-y", event.clientY)` and `animateTo(... { duration: 400 })` | Direct manipulation may feel detached if the dragged item does not track pointer/snap with system timing | Use transform-backed drag variables, requestAnimationFrame coalescing, tokenized snap duration, and Reduced Motion snap behavior |

---

## 3. Implementation plans

### Plan A — Normalize shared motion tokens and popover behavior

**Files and current excerpts**

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
- Popovers should open/close crisply using only intentional composited properties.
- Timing should align with the panel token, not a longer hardcoded duration.
- Reduced Motion should still show state change, but with shortened duration.

**Project conventions to preserve**
- Keep existing token names.
- Follow the button precedent: transform-based feedback, semantic duration/easing, `80ms` Reduced Motion.
- Do not introduce decorative bounce, overshoot, blur, or shadow animation.

**Ordered steps**
1. Replace `.popover` transition from `all 360ms ease-in` to explicit properties.
2. Use `var(--duration-panel)` and `var(--ease-responsive)`.
3. Add a Reduced Motion branch using `80ms`.
4. Do not change selector naming unless existing markup requires a different selector.
5. If open/closed states already exist elsewhere, only wire timing/easing to those states; do not invent new visibility logic without checking consumers.

**Implementation target shape**

```css
.popover {
  transform-origin: center;
  transition:
    transform var(--duration-panel) var(--ease-responsive),
    opacity var(--duration-panel) var(--ease-responsive);
}

@media (prefers-reduced-motion: reduce) {
  .popover {
    transition-duration: 80ms;
  }
}
```

**Hard boundaries**
- Do not use `transition: all`.
- Do not animate layout properties such as `top`, `left`, `width`, `height`, or margins.
- Do not remove visible focus styles.
- Do not change popover mounting, focus behavior, dismissal behavior, or z-index policy as part of this motion pass.

**Mechanical checks**
- Search for remaining `transition: all`.
- Search for hardcoded `360ms`, `ease-in`, and unrelated popover animation overrides.
- Run the closest available CSS/lint/type/build checks.

**Runtime/feel checks to perform later**
- Verify open and close both communicate state change.
- Verify keyboard-triggered popovers do not feel delayed.
- Verify Reduced Motion still shows a short state transition.
- Verify computed transition properties are limited to `transform` and `opacity`.

**Reduced Motion behavior**
- Preserve feedback with `80ms` transition duration.
- Avoid full removal unless a later accessibility review confirms instant state change is preferable.

**Source-drift stop condition**
- Stop before editing if `.popover` is no longer in `src/styles/motion.css`, if it already has state-specific transitions elsewhere, or if consumers depend on non-transform animated properties.

---

### Plan B — Convert command palette and toast to semantic, transform-based motion

**Files and current excerpts**

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
- Command palette: quick, calm state continuity for a high-frequency keyboard surface.
- Toast: transient feedback should enter without layout-position animation.
- Both should use semantic durations/easing and Reduced Motion.
- Motion should clarify “appeared from here / changed state” without delaying task flow.

**Project conventions to preserve**
- Use existing duration/easing tokens.
- Use transform/opacity.
- Keep existing component structure and `SearchResults`.
- Keep `data-open={open}` as the state hook unless current codebase already uses another state convention.

**Ordered steps**
1. Replace the command palette arbitrary animation class with a named class, for example `className="command-palette"`.
2. Move palette motion into CSS using `[data-open="true"]` and `[data-open="false"]` if the component remains mounted.
3. Use `opacity` and a small `translateY` or `scale` only; avoid large travel.
4. Set duration to `var(--duration-panel)` and easing to `var(--ease-responsive)`.
5. Convert toast keyframes from `top` to `transform: translateY(...)` plus opacity.
6. Set toast duration to `var(--duration-fast)` or `var(--duration-panel)` based on actual visibility need:
   - prefer `--duration-fast` if it is purely status feedback,
   - use `--duration-panel` only if toast carries important reviewable state.
7. Add Reduced Motion branches for both.

**Implementation target shape**

Command palette CSS target:

```css
.command-palette {
  opacity: 0;
  transform: translateY(-4px);
  transition:
    transform var(--duration-panel) var(--ease-responsive),
    opacity var(--duration-panel) var(--ease-responsive);
}

.command-palette[data-open="true"] {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  .command-palette {
    transition-duration: 80ms;
    transform: none;
  }
}
```

Toast CSS target:

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
- Do not change command execution, search result rendering, focus placement, or dismissal rules.
- Do not add decorative scale if it makes text feel unstable.
- Do not animate `top` for toast.
- Do not claim the palette is accessible based only on this change; focus management is unverified.

**Mechanical checks**
- Search for `animate-[palette_420ms_ease-in_both]`.
- Search for `@keyframes toast-enter`.
- Search for `top:` inside toast animation.
- Search for remaining `500ms`, `420ms`, and `ease-in` in these files.
- Run lint/type/build checks available for the project.

**Runtime/feel checks to perform later**
- Open/close command palette repeatedly by keyboard.
- Confirm the palette appears responsive and does not block fast command entry.
- Trigger multiple toasts and verify motion does not stack into visual noise.
- Emulate Reduced Motion and confirm feedback remains perceptible but brief.

**Reduced Motion behavior**
- Palette: keep opacity feedback, remove travel, shorten to `80ms`.
- Toast: keep short fade/appearance feedback, shorten to `80ms`.

**Source-drift stop condition**
- Stop if the palette animation is defined elsewhere by a framework config, if `open=false` unmounts the component immediately, or if toast position relies on the `top` property for layout rather than only animation.

---

### Plan C — Make sortable queue drag/snap feel directly manipulated and tokenized

**File and current excerpt**

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
- During drag, the item should track the pointer directly with no transition lag.
- On release, snap should be short, causal, and aligned with system timing.
- Reduced Motion should remove prolonged travel while preserving final-slot feedback.
- Pointer updates should avoid excessive style writes when events fire rapidly.

**Project conventions to preserve**
- Use transform-backed custom properties where possible.
- Use existing duration/easing tokens or constants derived from them.
- Keep current queue ordering, nearest-slot calculation, and pointer capture behavior unchanged unless separately audited.

**Ordered steps**
1. Inspect the CSS consumer of `--drag-y` before editing.
2. Confirm whether `--drag-y` expects viewport `clientY` or a local delta.
3. If it is currently absolute viewport position, convert to a local drag delta only if all consumers can be updated safely.
4. Coalesce pointer style writes with `requestAnimationFrame`:
   - store latest pointer value,
   - write once per frame,
   - cancel pending frame on pointer up/unmount.
5. Ensure active dragging has no transition on the dragged transform.
6. Replace `duration: 400` with a token-aligned duration:
   - default snap: `240ms` equivalent to `--duration-panel`,
   - shorter snap for small distances if existing animation helper supports it,
   - Reduced Motion snap: `80ms` or immediate final transform plus brief state highlight.
7. If `animateTo` accepts easing, use the responsive easing equivalent.
8. If `animateTo` cannot consume CSS tokens, centralize numeric constants near the component with names matching the semantic tokens.

**Implementation target shape**

```tsx
const SNAP_DURATION_MS = 240;
const REDUCED_MOTION_SNAP_DURATION_MS = 80;

// Example only; final wiring depends on existing motion helper APIs.
function onPointerMove(event: PointerEvent) {
  latestDragY.current = event.clientY;

  if (dragFrame.current == null) {
    dragFrame.current = requestAnimationFrame(() => {
      dragFrame.current = null;
      queueRef.current?.style.setProperty("--drag-y", `${latestDragY.current}px`);
    });
  }
}

function onPointerUp() {
  setDragging(false);

  if (dragFrame.current != null) {
    cancelAnimationFrame(dragFrame.current);
    dragFrame.current = null;
  }

  animateTo(nearestSlot(currentY), {
    duration: prefersReducedMotion ? REDUCED_MOTION_SNAP_DURATION_MS : SNAP_DURATION_MS,
  });
}
```

**Hard boundaries**
- Do not change sorting semantics.
- Do not change `nearestSlot(currentY)` behavior without separate tests.
- Do not add inertial/fling behavior; it risks reducing precision in an operations tool.
- Do not use springy overshoot for queue placement unless later user testing validates it.
- Do not claim performance improvement without trace evidence.

**Mechanical checks**
- Find the CSS rule using `--drag-y`.
- Find all `animateTo(...)` calls with hardcoded durations.
- Check for cleanup of animation frames on pointer cancel/up/unmount.
- Run type checks and relevant interaction tests if present.

**Runtime/feel checks to perform later**
- Drag slowly and quickly; the item should remain attached to the pointer.
- Release near slot boundaries; snap should clearly resolve to the intended slot.
- Confirm no transition is applied while actively dragging.
- Emulate Reduced Motion; drag remains direct, release is brief or immediate.
- If performance tooling is available, check for avoidable layout work during pointer movement.

**Reduced Motion behavior**
- Keep direct pointer tracking.
- Shorten release snap to `80ms` or snap immediately while preserving a non-motion state cue such as selected/focused/placed styling.
- Avoid long travel animation after release.

**Source-drift stop condition**
- Stop if `--drag-y` is not transform-backed, if `animateTo` has changed signature, if pointer state is managed by another abstraction, or if the component already has a Reduced Motion hook elsewhere.

---

## 4. Recommended execution order

1. **Plan A first**: establishes the shared contract and removes the highest-risk global `transition: all`.
2. **Plan B second**: fixes high-frequency keyboard/transient feedback and removes layout-based toast motion.
3. **Plan C third**: requires more implementation inspection because pointer math, CSS consumers, and animation helper behavior are unverified.

## Explicitly unverified states

- Actual rendered CSS cascade and computed styles.
- Whether command palette remains mounted when `open=false`.
- Whether `.popover` has separate open/closed selectors elsewhere.
- Whether toast `top` is used for layout positioning outside animation.
- Whether `--drag-y` is consumed by `transform` or by layout-affecting properties.
- Whether `animateTo` supports easing, cancellation, or Reduced Motion configuration.
- Focus management, focus trap behavior, and accessibility-tree output.
- Frame timing, layout/repaint cost, and input latency during drag.
- Real Reduced Motion behavior in browser/device settings.
- User perception of “too fast,” “too slow,” or “clear enough” without runtime review or user testing.
