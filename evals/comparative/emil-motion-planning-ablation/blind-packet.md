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

# Blind scorecard

Grade anonymized raw outputs. Do not reward brand, tone, or skill-name mentions.

| Criterion | Weight | Full-credit evidence |
|---|---:|---|
| Evidence honesty and recon | 15 | Maps the static motion surface and labels every runtime/feel claim as unverified. |
| Project conventions | 10 | Reuses the supplied tokens and correct local precedent instead of inventing a parallel system. |
| Purpose and frequency | 10 | Prioritizes keyboard/high-frequency restraint and causal feedback over decoration. |
| Technical accuracy | 15 | Correctly diagnoses property cost, origin, interruption, pointer tracking, and keyframe/transition tradeoffs without framework myths. |
| Prioritization | 10 | Vets and ranks a small set by user impact, frequency, confidence, and cost. |
| Plan self-containment | 20 | Plans include exact paths/excerpts, target behavior, steps, boundaries, and drift stop conditions. |
| Verification quality | 10 | Gives targeted mechanical plus browser/slow-motion/interruption feel checks without claiming they ran. |
| Accessibility and performance | 10 | Provides Reduced Motion behavior and measured performance checks while preserving useful feedback. |

Total: 100.


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

Diagnosis: the motion system has a solid local precedent, but several high-value surfaces bypass it with long `ease-in` timings, broad property ownership, layout-position animation, and no static evidence of equivalent Reduced Motion handling.

## 1. Recon summary

- **Stack signals:** TSX components plus CSS; React-like component model; CSS keyframes/transitions; Tailwind-style arbitrary animation class; one imperative drag/settle path via `animateTo(...)`.
- **Where motion lives:**
  - Global tokens: `src/styles/motion.css`
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`
  - Component class animation: `src/components/CommandPalette.tsx`
  - Pointer-driven interaction: `src/components/SortableQueue.tsx`
- **Existing conventions:**
  - Tokens: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
  - Correct local precedent: button uses transform-only motion, tokenized timing/easing, and a Reduced Motion branch that preserves feedback.
- **Product personality:** calm desktop operations console; motion should be crisp, quiet, causal, and throughput-preserving.
- **Frequency map:**
  - Very high: command palette, buttons, keyboard-heavy workflows.
  - High/direct manipulation: sortable queue drag/reorder.
  - Medium: popovers/dropdowns depending on use.
  - Occasional but repeatable: toasts.
- **Evidence level:** static snippets only. No computed style, runtime trace, frame-rate measurement, screen recording, browser validation, accessibility-tree inspection, or user testing was performed.

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | Static source | `src/components/CommandPalette.tsx` | Command palette uses `animate-[palette_420ms_ease-in_both]` on a keyboard-heavy surface. The duration/easing are outside the local crisp-token precedent. | Replace with tokenized opacity/transform transition or tokenized animation using `--duration-fast`/`--duration-panel` and `--ease-responsive`; add Reduced Motion behavior that preserves open/close feedback without spatial travel. |
| P1 | Static source | `src/components/SortableQueue.tsx` | Direct manipulation has a fixed `animateTo(..., { duration: 400 })`; supplied evidence does not show pointer capture, grab offset, velocity handoff, projected snap, interruption, transform ownership, or Reduced Motion. | Rework settle behavior around explicit gesture state, current presentation value, measured velocity, projected nearest slot, and Reduced Motion no-overshoot settle. Runtime validation required. |
| P2 | Static source | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in` and `transform-origin: center`; broad transition ownership and delayed-start easing conflict with crisp operations-console motion. | Limit properties to `opacity, transform`; use existing tokens; set trigger-relative origin when this is an anchored popover, preserving `center` only for genuinely centered overlays. |
| P2 | Static source | `src/components/toast.css` | Toast animates `top` from `-24px` to `0` over `500ms ease-in`; this is a layout-property animation risk and slow for workday feedback. | Convert to `transform: translateY(...)` plus opacity; shorten to tokenized timing/easing; add Reduced Motion crossfade/static-position feedback. |
| P2 | Static source | Multiple excerpts | Hard-coded `360ms`, `420ms`, `500ms`, `400` and `ease-in` appear beside existing semantic tokens. | Normalize listed motion to existing tokens first; only add new semantic tokens if repeated needs remain after component fixes. |
| P3 | Static source | `src/components/Button.css` | Positive precedent: transform-only active feedback with tokenized timing and Reduced Motion. | Preserve as reference; use its pattern as the implementation baseline for other small feedback motion. |

## 3. Implementation-ready plans

### Plan A — Normalize command palette and popover motion

**Current excerpts**

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

- Command palette opens/closes immediately enough for keyboard-heavy operators.
- Use opacity plus a very small transform only if it helps state continuity.
- Popovers transition only owned visual properties.
- Easing should feel responsive at the start, using `--ease-responsive`.
- Durations should use `--duration-fast` for small overlays or `--duration-panel` where panel scale requires slightly more continuity.

**Project conventions**

- Reuse `--duration-fast`, `--duration-panel`, `--ease-responsive`.
- Follow the button precedent: transform-only where possible, tokenized transition, Reduced Motion branch.
- Preserve visible focus and do not delay keyboard interaction.

**Ordered steps**

1. Inspect actual palette CSS/keyframes for `palette`; stop if it already encodes a broader state contract not shown here.
2. Replace `animate-[palette_420ms_ease-in_both]` with a state-driven class or CSS selector tied to `data-open`.
3. Implement palette open/closed styles using only `opacity` and `transform`.
4. Use `var(--duration-fast)` for the first pass; allow `var(--duration-panel)` only if the palette is visually large and runtime review shows `160ms` is too abrupt.
5. In `.popover`, replace `transition: all 360ms ease-in` with explicit properties, e.g. `opacity var(--duration-fast) var(--ease-responsive), transform var(--duration-fast) var(--ease-responsive)`.
6. Audit `.popover` positioning in source before changing `transform-origin`.
   - If anchored to a trigger, set origin from the trigger/placement mechanism or a placement class.
   - If truly centered, keep `center`.
7. Add Reduced Motion rules for palette and popover: remove/reduce translate/scale travel while preserving opacity or instant state feedback.
8. Search for remaining hard-coded palette/popover `ease-in`, `420ms`, `360ms`, and `transition: all` instances in these files.

**Hard boundaries**

- Do not change `SearchResults` data behavior.
- Do not alter focus management, keyboard shortcuts, or open/close state semantics.
- Do not introduce a new animation library.
- Do not replace semantic tokens with one-off cubic-beziers.
- Do not assert trigger-relative origin until actual placement source is inspected.

**Mechanical checks**

- Static search: no `animate-[palette_420ms_ease-in_both]` remains.
- Static search: `.popover` no longer uses `transition: all`.
- Static search: new motion uses existing duration/easing tokens.
- Run the project’s closest available type/lint/build checks after identifying scripts.

**Runtime/feel checks to perform later**

- Keyboard open/close palette repeatedly; confirm no perceived waiting before content is usable.
- Verify focus ring remains visible throughout open/close.
- Open popovers from each placement; confirm origin matches the trigger relationship.
- Test rapid open/close interruption for visual jumps.

**Reduced Motion behavior**

- Palette/popover should avoid meaningful spatial travel.
- Preserve feedback through opacity, immediate state change, focus, border, or background state.
- Do not remove feedback entirely.

**Source-drift stop condition**

- Stop before editing if `CommandPalette` no longer contains the cited arbitrary animation class, if `.popover` transition/origin have already changed materially, or if the motion tokens in `src/styles/motion.css` have been renamed/redefined.

---

### Plan B — Rebuild toast entrance as transform/opacity feedback

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

- Toasts should appear promptly without cinematic delay.
- Entrance should communicate arrival while avoiding layout-position animation.
- Motion should stay calm and non-blocking for repeated operational feedback.

**Project conventions**

- Use existing tokens from `src/styles/motion.css`.
- Prefer `transform` and `opacity`.
- Add Reduced Motion behavior equivalent to the button precedent.

**Ordered steps**

1. Inspect toast positioning CSS around `.toast` before editing; confirm whether `top` is also used for static placement.
2. Keep static placement separate from animation state.
3. Replace keyframe `top` changes with `transform: translateY(...)` and `opacity`.
4. Use `var(--duration-panel)` only if the toast travels a visible distance; otherwise use `var(--duration-fast)`.
5. Replace `ease-in` with `var(--ease-responsive)`.
6. Ensure final state is stable without requiring animated `top`.
7. Add `@media (prefers-reduced-motion: reduce)` branch:
   - no vertical travel, or at most a very small transform;
   - shorter duration or immediate transform;
   - opacity/static state feedback preserved.
8. Search for other toast animation declarations before assuming this is the only toast path.

**Hard boundaries**

- Do not change toast queueing, dismissal timing, z-index, or content.
- Do not animate layout properties for the entrance.
- Do not add `will-change` unless runtime measurement shows benefit.
- Do not make toasts invisible until JavaScript starts.

**Mechanical checks**

- Static search: `toast-enter` no longer animates `top`.
- Static search: `.toast` no longer uses `500ms ease-in`.
- Static search: Reduced Motion branch exists for toast motion.
- Run the project’s closest available CSS/lint/build checks after identifying scripts.

**Runtime/feel checks to perform later**

- Trigger one toast and several consecutive toasts.
- Confirm toast placement does not shift surrounding layout.
- Confirm entrance is noticeable but does not steal attention from keyboard work.
- Confirm dismissal behavior, if separately animated, remains coherent.

**Reduced Motion behavior**

- Remove vertical travel.
- Preserve arrival feedback through opacity or immediate static presentation.
- Keep dismissal feedback similarly restrained if dismissal animation exists.

**Source-drift stop condition**

- Stop before editing if `toast-enter` no longer animates `top`, if `.toast` no longer owns entrance animation, or if toast positioning depends on `top` in a way that requires a broader layout decision.

---

### Plan C — Make sortable queue settle interaction physically coherent

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

- Dragged queue item tracks the pointer 1:1 after drag intent is established.
- Release settles to a slot based on current position plus measured velocity/projection, not only the last logical value.
- Interruption starts from the current on-screen value without jumping.
- Reduced Motion removes large travel/overshoot while preserving clear reorder feedback.

**Project conventions**

- Preserve existing component API unless source inspection proves a safer internal boundary.
- Prefer transform ownership for drag movement.
- Avoid broad style recalculation in hot pointer paths where possible.
- Do not add dependencies unless existing project animation utilities cannot read current value/velocity and the tradeoff is approved.

**Ordered steps**

1. Inspect the full component before editing:
   - item DOM structure;
   - how `--drag-y` is consumed;
   - whether transform is also used for press/hover;
   - `animateTo` implementation/signature;
   - how `currentY` is updated.
2. Define the coordinate space explicitly: CSS pixels relative to the queue/container, not raw viewport `clientY`, unless current CSS proves viewport coordinates are intended.
3. On pointer down, store:
   - active pointer id;
   - initial pointer position;
   - item start position;
   - grab offset;
   - recent pointer samples with timestamps.
4. Use pointer capture once drag intent is confirmed.
5. During pointer move, update only the active item’s transform/presentation value where possible; avoid parent-level variables if they invalidate a large subtree.
6. Track velocity from recent samples in CSS px/s.
7. On pointer up/cancel:
   - release pointer capture;
   - compute projected endpoint from current presentation position and velocity;
   - choose `nearestSlot(projectedEndpoint)`;
   - settle from current presentation value, not from stale `currentY`.
8. Replace fixed `duration: 400` with an existing spring/settle primitive if available; otherwise use bounded tokenized duration as a fallback with no bounce.
9. Add Reduced Motion branch:
   - no overshoot/bounce;
   - shortest practical settle;
   - clear static reorder/focus/selection feedback preserved.
10. Add cancellation handling for pointer cancel/lost capture.

**Hard boundaries**

- Do not change queue ordering business rules.
- Do not alter item identity/keying without a separate data-flow review.
- Do not block input until settle animation completes.
- Do not let drag translate and press scale compete for the same raw `transform` string without a composed owner or wrapper split.
- Do not claim gesture quality without runtime interaction testing.

**Mechanical checks**

- Static search: no remaining hard-coded `duration: 400` settle for this interaction unless justified as fallback.
- Type/lint check for pointer event types and cleanup paths.
- Unit or component test, if available, for nearest-slot selection and cancel/up paths.
- Static inspection confirms pointer capture cleanup and no leaked active pointer state.

**Runtime/feel checks to perform later**

- Drag slowly, quickly, and outside queue bounds.
- Release with low and high velocity; confirm projected slot selection feels causal.
- Interrupt a settle by grabbing again; confirm no visual jump.
- Verify keyboard/focus behavior for the reordered item remains visible.
- Check under realistic queue length; measure if pointer updates touch large subtrees.

**Reduced Motion behavior**

- Maintain direct manipulation while dragging.
- On release, use immediate or very short no-overshoot settle.
- Preserve reorder confirmation through position, focus, outline, or static state feedback.

**Source-drift stop condition**

- Stop before editing if `--drag-y` is no longer the drag presentation channel, if `animateTo` signature/semantics differ from the excerpt, if queue coordinates are already container-relative with velocity support, or if a separate drag library owns this interaction.

## 4. Recommended execution order

1. **Plan A:** fixes the highest-frequency keyboard/overlay motion and establishes the tokenized pattern.
2. **Plan B:** low-risk CSS-only correction for toast feedback and layout-animation risk.
3. **Plan C:** highest interaction complexity; do after the token/Reduced Motion pattern is settled, with dedicated runtime validation time.

## Explicitly unverified states

- Actual rendered durations/easing after CSS cascade.
- Whether `palette` keyframes exist elsewhere and what properties they animate.
- Popover placement model and whether `center` origin is intentional.
- Toast queueing/dismissal behavior and final computed positioning.
- Sortable queue DOM size, transform ownership, `animateTo` behavior, and gesture feel.
- Reduced Motion behavior beyond the shown button precedent.
- Frame pacing, compositing, layout shifts, accessibility-tree behavior, and keyboard/focus runtime behavior.


## Output B

## 1. Recon summary

- **Stack signals:** React/TSX components, CSS modules or colocated CSS, global CSS tokens, Tailwind-style arbitrary animation utility, imperative drag animation.
- **Where motion lives:**  
  - Global motion/tokens: `src/styles/motion.css`  
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`  
  - JSX utility class: `src/components/CommandPalette.tsx`  
  - Imperative interaction code: `src/components/SortableQueue.tsx`
- **Existing conventions:** Semantic CSS tokens exist for duration/easing:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
  - Existing Reduced Motion precedent shortens feedback rather than removing it: `.button { transition-duration: 80ms; }`
- **Product personality:** Calm, crisp, workday operations console. Motion should clarify cause/effect and preserve state continuity without feeling decorative or delaying keyboard-heavy workflows.
- **Frequency map from component roles, not runtime data:**
  - High frequency: buttons, command palette, queue sorting/dragging.
  - Medium frequency: popovers.
  - Intermittent but attention-sensitive: toasts.
- **Evidence level:** Static excerpt audit only. No runtime behavior, computed styles, browser validation, device testing, accessibility-tree inspection, performance trace, or user testing was performed.

---

## 2. Vetted priority table

| Priority | Finding | Evidence | Risk | Recommended direction |
|---|---|---|---|---|
| P0 | Reduced Motion is not consistently represented across shown motion surfaces | Only `Button.css` excerpt includes `@media (prefers-reduced-motion: reduce)` | Users requesting reduced motion may still receive long/large animations | Add per-surface Reduced Motion paths that preserve feedback with shorter/fewer transforms |
| P1 | Popover uses broad, slow, non-tokenized transition | `.popover { transition: all 360ms ease-in; }` | `all` may animate unintended properties; 360ms ease-in can feel sluggish for operational UI | Restrict to opacity/transform, use existing tokens/ease, add Reduced Motion |
| P1 | Command palette uses arbitrary 420ms ease-in animation | `className="animate-[palette_420ms_ease-in_both]"` | Long keyboard-invoked motion may slow perceived throughput; bypasses token convention | Replace with semantic class/tokenized duration and state-driven open/close behavior |
| P1 | Sortable queue settle animation uses hardcoded 400ms | `animateTo(nearestSlot(currentY), { duration: 400 });` | Drag/drop completion may feel delayed; no shown Reduced Motion branch | Use token-equivalent duration/ease; shorten or simplify in Reduced Motion |
| P2 | Toast animates layout property over 500ms | `from { top: -24px; ... }` and `animation: ... 500ms ease-in` | Layout-affecting animation and long ease-in may feel heavy for feedback | Animate transform/opacity with tokenized timing; shorten in Reduced Motion |
| P2 | A correct local precedent exists but is not generalized | `Button.css` uses `var(--duration-fast)` and `var(--ease-responsive)` | Motion style may drift component-by-component | Treat button pattern as the local implementation precedent |

---

## 3. Implementation plans

### Plan A — Normalize global/component CSS motion tokens for popovers and toasts

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

- Popovers feel immediate and causal: small opacity/scale/translate transition, not a broad `all` transition.
- Toasts enter clearly without layout-property animation.
- Motion uses existing semantic duration/easing tokens.
- Reduced Motion keeps feedback visible but shorter/subtler.

**Project conventions to preserve**

- Reuse existing CSS variables instead of introducing one-off durations.
- Follow the existing button precedent: tokenized timing plus Reduced Motion override.
- Keep focus visibility untouched.
- Avoid broad global changes beyond the affected selectors/keyframes.

**Ordered steps**

1. In `src/styles/motion.css`, replace `.popover` transition from `all 360ms ease-in` to explicit properties, for example:
   - `opacity var(--duration-panel) var(--ease-responsive)`
   - `transform var(--duration-panel) var(--ease-responsive)`
2. Confirm whether `.popover` has existing open/closed state selectors elsewhere before adding new state selectors. If state selectors are absent, stop and inspect the real component before inventing state names.
3. In `src/components/toast.css`, replace `top` keyframe movement with `transform: translateY(...)`.
4. Reduce toast duration to `var(--duration-panel)` or `var(--duration-fast)` depending on existing toast density in the real codebase.
5. Add `@media (prefers-reduced-motion: reduce)` overrides:
   - Popover: shorter duration, minimal transform or opacity-only.
   - Toast: shorter duration, opacity plus very small translate or opacity-only.
6. Do not remove opacity changes; Reduced Motion should still communicate feedback.

**Hard boundaries**

- Do not rename selectors without checking all usages.
- Do not introduce new token names unless the existing tokens are insufficient after inspecting the full style system.
- Do not animate layout properties such as `top`, `left`, `width`, or `height` for these entrances unless a verified existing pattern requires it.
- Do not change toast placement, stacking, z-index, or dismissal behavior.

**Mechanical checks**

- Search for `.popover`, `toast-enter`, and `.toast` usages before changing selectors.
- Run the closest available CSS/frontend validation command, likely one of:
  - lint
  - type-check
  - build
- Re-read the final diff to ensure no unrelated style changes were included.

**Runtime/feel checks to perform later**

- Verify popover open/close feels under roughly a quarter second.
- Verify toast entry is noticeable but not attention-grabbing.
- Verify no focus outline is hidden or delayed.
- Verify repeated toasts do not feel sluggish.

**Reduced Motion behavior**

- Use shorter duration, approximately matching the existing `80ms` precedent.
- Preserve opacity or instant positional continuity; do not silently remove feedback.

**Source-drift stop condition**

- Stop if the real files no longer contain the shown selectors/keyframes or if `.popover`/`.toast` state is controlled by a different abstraction not present in the excerpts.

---

### Plan B — Make command palette motion semantic, state-driven, and keyboard-fast

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

- Command palette opens with crisp, calm continuity appropriate for keyboard-heavy users.
- Timing follows project motion tokens instead of an arbitrary utility duration.
- Open/closed visual state is controlled by `data-open`, CSS selectors, or an existing animation utility pattern.
- Reduced Motion keeps open/close feedback but shortens/simplifies it.

**Project conventions to preserve**

- Existing semantic tokens from `src/styles/motion.css`.
- Existing Reduced Motion precedent from `src/components/Button.css`.
- Do not reduce keyboard throughput or delay search input availability.
- Do not alter command palette data loading, search behavior, focus management, or result rendering.

**Ordered steps**

1. Inspect the full `CommandPalette.tsx` file and any palette-related CSS/keyframes before implementation.
2. Replace the arbitrary `animate-[palette_420ms_ease-in_both]` with a named class or existing local style hook, for example a semantic class such as `command-palette`.
3. Use `data-open={open}` as the state source if that is already the component contract.
4. Define or update CSS so `[data-open="true"]` uses tokenized opacity/transform transition around `var(--duration-panel)` and `var(--ease-responsive)`.
5. Define the closed state explicitly if the component remains mounted while closed.
6. Add Reduced Motion override with shorter duration and reduced transform distance.
7. Ensure the palette contents remain interactable according to the existing open/closed behavior; do not invent accessibility behavior from the snippet alone.

**Hard boundaries**

- Do not change focus trapping, keyboard shortcuts, selected result state, or search result logic.
- Do not assume whether the palette unmounts when closed; verify in the real file first.
- Do not add a delayed mount/unmount pattern unless the existing component already supports it.
- Do not use long entrance animation for a keyboard-invoked command surface.

**Mechanical checks**

- Search for `palette`, `CommandPalette`, `data-open`, and arbitrary `animate-[palette` usage.
- Confirm the CSS file where palette styles should live before adding styles.
- Run type-check/lint/build as available.
- Confirm no Tailwind build constraints are violated if replacing arbitrary utilities with CSS classes.

**Runtime/feel checks to perform later**

- Open via keyboard shortcut and verify the input is usable immediately.
- Reopen repeatedly and check that motion feels crisp rather than ceremonial.
- Verify close transition does not block the next command.
- Verify focus indication remains visible.

**Reduced Motion behavior**

- Shorten to the local Reduced Motion precedent, approximately `80ms`.
- Prefer opacity plus minimal transform, or opacity-only if movement is uncomfortable.
- Preserve state feedback; do not make open/close visually ambiguous.

**Source-drift stop condition**

- Stop if `CommandPalette.tsx` no longer contains the arbitrary animation class or if palette styling is centralized in a design-system primitive that should be changed instead.

---

### Plan C — Tokenize and reduce sortable queue drag-settle motion

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

- Drag movement remains direct and responsive.
- Drop/settle animation preserves spatial continuity but does not delay the operator.
- Hardcoded `400` duration is replaced with a token-aligned value or nearby local constant.
- Reduced Motion shortens or simplifies settle behavior while preserving final-position feedback.

**Project conventions to preserve**

- Existing timing vocabulary: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
- Existing pattern that Reduced Motion still provides feedback.
- Pointer interaction code should stay minimal and avoid broad refactors.

**Ordered steps**

1. Inspect the full `SortableQueue.tsx` file to identify:
   - Where `currentY` is updated.
   - What `animateTo` is imported from.
   - Whether `animateTo` accepts easing.
   - Whether a Reduced Motion hook/helper already exists.
2. Inspect CSS consuming `--drag-y` to verify it drives `transform` rather than layout properties.
3. Replace `{ duration: 400 }` with a token-aligned constant, likely equivalent to `--duration-panel` for settle or `--duration-fast` for small snaps.
4. If `animateTo` accepts easing, pass the existing responsive easing equivalent.
5. Add a Reduced Motion branch:
   - Short duration, approximately `80ms`, or immediate snap if the animation library cannot safely shorten.
   - Preserve final slot update and visual confirmation.
6. Keep pointer-move update path direct; do not add expensive calculations inside `onPointerMove`.

**Hard boundaries**

- Do not rewrite drag architecture unless the current implementation cannot support reduced motion.
- Do not change sorting semantics, nearest-slot logic, or queue data state.
- Do not introduce new global event listeners without checking cleanup.
- Do not assume performance problems from the snippet alone; verify before optimizing beyond the duration/easing issue.

**Mechanical checks**

- Search for `animateTo`, `--drag-y`, `nearestSlot`, and `prefers-reduced-motion`.
- Type-check after changes.
- If tests exist for sorting/reordering, run the closest relevant test.
- Re-read diff for accidental behavior changes to queue ordering.

**Runtime/feel checks to perform later**

- Drag an item slowly and quickly; verify the item tracks pointer intent.
- Drop between nearby slots and distant slots; verify snap is clear but not slow.
- Verify keyboard or non-pointer reorder paths, if present, still communicate state.
- Verify Reduced Motion path still shows the item reaching the final slot.

**Reduced Motion behavior**

- Prefer shortened settle rather than removing all feedback.
- If reduced path snaps immediately, ensure final placement is visibly clear through position/state/focus styling.

**Source-drift stop condition**

- Stop if `animateTo` does not accept duration/easing options as shown, or if `--drag-y` is not used for visual movement in the current implementation.

---

## 4. Recommended execution order

1. **Plan A first:** establishes the shared CSS precedent and fixes the broadest token/RM drift in popover and toast motion.
2. **Plan B second:** command palette is likely high-frequency and keyboard-critical; align it after CSS conventions are clarified.
3. **Plan C third:** sortable drag needs slightly more implementation inspection because behavior depends on `animateTo`, pointer state, and CSS consumption of `--drag-y`.

## Explicitly unverified states

- No browser, device, screen reader, accessibility-tree, computed-style, trace, or user testing was performed.
- Actual component mounting/unmounting behavior is unknown.
- Existing palette keyframes and Tailwind configuration are unknown.
- Whether `animateTo` supports easing or Reduced Motion branching is unknown.
- Whether `--drag-y` is consumed by `transform` or layout-affecting properties is unknown.
- Existing global Reduced Motion helpers, if any, were not shown.
- Existing focus behavior and keyboard interaction behavior were not validated.

Applied frontend and quality delivery guardrails; this is an implementation roadmap only, with no file edits performed.


## Output C

## 1. Recon summary

- **Stack signals**: React/TSX components plus CSS. Tailwind-style arbitrary animation utility appears in `CommandPalette.tsx`. No runtime motion library is proven from the evidence.
- **Where motion lives**:
  - Global motion tokens in `src/styles/motion.css`.
  - Component CSS in `src/components/toast.css` and `src/components/Button.css`.
  - Inline utility class in `src/components/CommandPalette.tsx`.
  - Imperative pointer/settle code in `src/components/SortableQueue.tsx`.
- **Existing conventions**:
  - Tokens: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`.
  - Correct local precedent: button press uses `transform`, tokenized duration/easing, and a reduced-motion duration of `80ms`.
- **Product personality**: calm, crisp, workday operations console. Motion should explain causality/state continuity, not decorate or delay throughput.
- **Frequency map**:
  - Command palette: likely very high-frequency, keyboard-heavy; should be instant or near-instant.
  - Sortable queue: likely high-frequency during queue work; gesture response must preserve continuity.
  - Popovers: likely frequent operational controls; should be short and anchored.
  - Toasts: occasional feedback; can animate, but should be fast and non-layout.
- **Evidence level**: static snippets only. No runtime behavior, computed styles, trace, accessibility tree, browser/device validation, or user testing was performed.

## 2. Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose / frequency | `src/components/CommandPalette.tsx` | Command palette uses `animate-[palette_420ms_ease-in_both]`. For a keyboard-heavy console, a 420ms ease-in entrance is too slow for a high-frequency command surface. | Remove the entrance animation; make open/close immediate. |
| 2 | HIGH | Easing / performance / cohesion | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in;`. This is slow, starts sluggishly, and may animate unintended properties. | Limit transition to `transform, opacity`; use existing tokens and ≤200ms timing. |
| 3 | MEDIUM | Physicality / origin | `src/styles/motion.css` | `.popover` uses `transform-origin: center;`. For trigger-anchored popovers, center origin can break spatial causality. Static evidence does not prove the popover is modal-like. | Use trigger-provided origin variables when available, with safe fallback. |
| 4 | MEDIUM | Performance / easing / accessibility | `src/components/toast.css` | Toast enter animates `top` for `500ms ease-in`; this is layout-affecting and longer than the existing panel token. No reduced-motion branch is shown. | Animate `transform` + `opacity`, use `--duration-panel` and `--ease-responsive`, add reduced-motion fade-only path. |
| 5 | MEDIUM | Gesture / interruptibility | `src/components/SortableQueue.tsx` | Drag move writes `--drag-y` imperatively, and release uses fixed `duration: 400`. Static evidence does not show how `--drag-y` is consumed, but the settle motion is likely not velocity-aware. | Move only the dragged item/layer via transform; use interruptible spring settle if supported; shorten/no-bounce path for reduced motion. |

No additive “missed opportunity” is justified from these snippets alone.

---

## 3. Implementation plans

### Plan 1 — Make the command palette immediate

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

- Opening/closing the command palette must not wait on a 420ms animation.
- Keyboard invocation should reveal the command surface immediately.
- Reduced Motion behavior is identical: no movement and no delayed entrance.

**Project conventions**

- Follow the existing crisp-motion direction and semantic token use.
- Do not replace this with another long transition.
- Existing correct precedent: `src/components/Button.css` uses tokenized transform feedback and reduced-motion timing, but command palette frequency is higher than a button press and should be more direct.

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, confirm the current wrapper still contains only the animation utility shown above.
2. Remove the `className="animate-[palette_420ms_ease-in_both]"` prop.
3. Leave `data-open={open}` intact.
4. Leave `<SearchResults />`, focus handling, open-state logic, keyboard shortcuts, and markup structure unchanged.

**Target excerpt**

```tsx
export function CommandPalette({ open }: { open: boolean }) {
  return (
    <div data-open={open}>
      <SearchResults />
    </div>
  );
}
```

**Hard boundaries**

- Do not add a replacement animation.
- Do not alter search result rendering, keyboard behavior, focus management, ARIA attributes, or mounting logic.
- Do not remove `data-open`; other styles may depend on it.

**Mechanical checks**

- Run the project’s existing TypeScript and lint checks, if available.
- Search for `palette_420ms_ease-in_both`; expected result after edit: no remaining usage unless deliberately defined elsewhere for unrelated code.

**Runtime / feel checks to perform after implementation**

- Trigger the palette repeatedly with the keyboard shortcut.
- Confirm the palette is available immediately, without a slow fade/slide.
- Confirm visible focus is preserved when opened.
- Toggle Reduced Motion and confirm behavior remains immediate.

**Reduced Motion behavior**

- Same as default: no autonomous movement.

**Source-drift stop condition**

- Stop if the file no longer matches this structure, if the animation class is gone already, or if the class also carries required non-motion styling. Report drift instead of improvising.

---

### Plan 2 — Normalize popover and toast motion to tokenized transform/opacity

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

- Popovers feel responsive and only animate properties intended for motion.
- Trigger-anchored popovers use a trigger-provided transform origin when available.
- Toasts enter with compositor-friendly movement and opacity, not `top`.
- Reduced Motion keeps feedback but removes positional movement.

**Project conventions**

- Reuse existing tokens:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Follow the local reduced-motion precedent from `src/components/Button.css`:
  - reduced duration: `80ms`.

**Ordered steps**

1. In `src/styles/motion.css`, replace the `.popover` rule with explicit transform/opacity transitions.
2. Use trigger-origin variables with fallback, so the rule works with common anchored-popover implementations without requiring a new dependency.
3. Add a reduced-motion branch that shortens the existing transition rather than removing feedback.
4. In `src/components/toast.css`, change `toast-enter` to animate `transform` and `opacity`.
5. Add a separate reduced-motion keyframe that fades only.
6. Change `.toast` to use existing duration/easing tokens.
7. Do not add new global tokens unless the existing tokens are missing in the real file.

**Target excerpts**

`src/styles/motion.css`

```css
.popover {
  transform-origin: var(
    --radix-popover-content-transform-origin,
    var(--transform-origin, center)
  );
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

`src/components/toast.css`

```css
@keyframes toast-enter {
  from {
    transform: translate3d(0, -24px, 0);
    opacity: 0;
  }
  to {
    transform: translate3d(0, 0, 0);
    opacity: 1;
  }
}

@keyframes toast-enter-reduced {
  from { opacity: 0; }
  to { opacity: 1; }
}

.toast {
  animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;
}

@media (prefers-reduced-motion: reduce) {
  .toast {
    animation-name: toast-enter-reduced;
    animation-duration: 80ms;
  }
}
```

**Hard boundaries**

- Do not change toast positioning outside the keyframes unless required by existing layout.
- Do not change toast lifetime, stacking, dismissal, copy, icons, or severity styling.
- Do not change popover markup or component API.
- Do not introduce a new motion library.

**Mechanical checks**

- Run existing lint/build checks if available.
- Confirm there is no remaining `transition: all 360ms ease-in` in `src/styles/motion.css`.
- Confirm `@keyframes toast-enter` no longer animates `top`.
- Confirm all referenced tokens exist in the final CSS cascade.

**Runtime / feel checks to perform after implementation**

- Open a popover at slow animation playback and confirm it does not animate unrelated properties.
- If the popover is trigger-anchored, confirm it appears to grow from the trigger side when the origin variable is present.
- Trigger a toast and confirm it enters quickly without pushing layout during the animation.
- Toggle Reduced Motion and confirm the toast fades without vertical travel.

**Reduced Motion behavior**

- Popover: keep brief opacity/transform feedback at `80ms`.
- Toast: fade-only at `80ms`; no translate movement.

**Source-drift stop condition**

- Stop if `.popover` is actually used for centered modal content rather than anchored popovers.
- Stop if toast positioning depends on animating `top` for layout correctness.
- Stop if `--duration-fast`, `--duration-panel`, or `--ease-responsive` are absent or renamed in the real file.

---

### Plan 3 — Make sortable queue release motion interruptible and input-connected

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

- While dragging, the item should track the pointer directly.
- The dragged item/layer should move via `transform`, not a parent-level CSS variable that may invalidate unrelated descendants.
- Release-to-slot should preserve continuity with an interruptible settle.
- Reduced Motion should still allow direct pointer tracking, but the autonomous settle should be very short and non-bouncy.

**Project conventions**

- Use existing token direction where CSS is involved: transform-only motion, crisp durations, reduced path preserving feedback.
- Do not add a new dependency.
- If the existing `animateTo` helper already supports spring-style options, use it; otherwise stop and report that the helper needs an adapter rather than faking a spring with a long tween.

**Ordered steps**

1. Open the full `src/components/SortableQueue.tsx`.
2. Identify the exact element that visually moves during drag.
3. If the code already has a ref for the dragged row or drag layer, use that ref for pointer-move transforms.
4. Replace parent-level `queueRef.current?.style.setProperty("--drag-y", ...)` with a transform write on only the moving element/layer.
5. Track recent pointer velocity from the last two pointer move events.
6. Replace the fixed `duration: 400` release with:
   - default: spring-style settle `{ type: "spring", duration: 0.5, bounce: 0.2, velocity: <trackedYVelocity> }` if supported by `animateTo`;
   - reduced motion: `{ duration: 80 }` or the closest supported non-bouncy equivalent.
7. Clear any inline transform after the item has settled, if the current implementation expects layout to own the final position.

**Representative target shape**

```tsx
function onPointerMove(event: PointerEvent) {
  const nextY = event.clientY;
  updateDragVelocity(nextY, performance.now());
  draggedItemRef.current?.style.setProperty(
    "transform",
    `translate3d(0, ${nextY - dragStartY}px, 0)`
  );
}

function onPointerUp() {
  setDragging(false);

  const target = nearestSlot(currentY);
  animateTo(
    target,
    prefersReducedMotion()
      ? { duration: 80 }
      : { type: "spring", duration: 0.5, bounce: 0.2, velocity: dragVelocityY }
  );
}
```

**Hard boundaries**

- Do not change queue ordering logic.
- Do not change `nearestSlot` behavior.
- Do not alter keyboard sorting behavior, if present.
- Do not introduce a dependency for springs.
- Do not keep the fixed `400`ms settle if the helper supports an interruptible spring.
- Do not implement a custom animation loop unless the file already uses one.

**Mechanical checks**

- Run existing TypeScript/lint checks if available.
- Confirm no pointer-move path writes `--drag-y` to the queue root unless another non-motion purpose is found.
- Confirm release no longer uses `{ duration: 400 }` as the default settle path.
- Confirm reduced-motion detection is safe for the rendering environment used by the app.

**Runtime / feel checks to perform after implementation**

- Drag slowly and quickly; the item should remain visually attached to the pointer.
- Release near a slot; it should settle without a sluggish 400ms glide.
- Start a second drag before the previous settle visually completes; it should not jump back to an old start point.
- Toggle Reduced Motion; direct dragging still follows the pointer, while release settles quickly without bounce.

**Reduced Motion behavior**

- User-driven drag movement remains direct because it is input-controlled.
- Autonomous release animation uses `80ms` and no bounce.

**Source-drift stop condition**

- Stop if there is no per-item or drag-layer ref to target.
- Stop if `animateTo` does not support spring, velocity, or reduced-duration options.
- Stop if `--drag-y` is consumed by a broader layout algorithm rather than visual motion.

---

## 4. Recommended execution order

1. **Plan 1 — Command palette immediate**: highest throughput impact, smallest scope.
2. **Plan 2 — Popover/toast normalization**: fixes shared timing, easing, performance, and reduced-motion issues.
3. **Plan 3 — Sortable queue release**: highest interaction complexity; do after simpler token/CSS fixes.

## Explicitly unverified states

- Actual framework version, package scripts, and build tooling.
- Whether `.popover` is always trigger-anchored or sometimes modal-like.
- Whether command palette mounting/focus behavior depends on the animation class.
- Whether toast stacking/dismissal has additional CSS not shown.
- How `--drag-y` is consumed.
- Whether `animateTo` supports spring, velocity, or reduced-duration options.
- Actual computed styles, performance traces, accessibility tree, keyboard focus behavior, and user-perceived feel.
