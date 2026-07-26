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

- **Stack signals:** React/TSX components, plain CSS, CSS custom properties, utility-class animation syntax, and an imperative pointer/animation path for drag sorting.
- **Where motion lives:**  
  - Global motion tokens: `src/styles/motion.css`  
  - Component CSS/keyframes: `src/components/toast.css`, `src/components/Button.css`  
  - Inline utility animation: `src/components/CommandPalette.tsx`  
  - Imperative gesture handling: `src/components/SortableQueue.tsx`
- **Existing conventions:**  
  - Durations: `--duration-fast: 160ms`, `--duration-panel: 240ms`  
  - Primary responsive curve: `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`  
  - Correct local precedent: button press uses `transform`, tokenized timing/easing, and a reduced-motion override that preserves feedback.
- **Product personality:** calm, crisp, high-throughput desktop operations UI. Motion should clarify cause/effect and state continuity, not add delay or decoration.
- **Frequency map:**  
  - Very high: `CommandPalette` for keyboard-heavy operators.  
  - High/dynamic: `SortableQueue` drag/reorder.  
  - Medium: `.popover` interactions.  
  - Occasional: `.toast` notifications.  
  - Local precedent: `.button:active` likely frequent and currently aligned.
- **Evidence level:** static snippet audit only. No runtime timing, computed style, device, trace, screen recording, accessibility-tree, or user validation was performed.

---

## 2. Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose, frequency, duration | `src/components/CommandPalette.tsx` | High-frequency keyboard surface uses `animate-[palette_420ms_ease-in_both]`. Static evidence shows a slow `ease-in` animation on a command surface operators may invoke repeatedly. | Remove the open/close animation or reduce to non-spatial instant/near-instant feedback. Do not delay search availability. |
| 2 | HIGH | Easing, performance, cohesion | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in;`. This bypasses existing tokens, animates unintended properties, exceeds the small-popover budget, and starts slowly. | Restrict to `transform, opacity`; use existing duration/easing tokens; add reduced-motion override. |
| 3 | MEDIUM | Physicality, causality | `src/styles/motion.css` | `.popover { transform-origin: center; }` is suspicious for trigger-anchored popovers. Static evidence cannot confirm trigger geometry, but the class name indicates anchored UI rather than a centered modal. | Prefer a trigger-origin variable when available; keep a safe fallback only if no origin source exists. |
| 4 | HIGH | Performance, accessibility | `src/components/toast.css` | Toast enters by animating `top` from `-24px` to `0` over `500ms ease-in`. This is layout-affecting, slow for UI feedback, and has no shown reduced-motion path. | Replace `top` animation with `transform: translateY(...)` + opacity, tokenized timing, and reduced-motion opacity-only feedback. |
| 5 | HIGH | Gesture, interruptibility | `src/components/SortableQueue.tsx` | Drag path writes `--drag-y` during pointer move and settles with `animateTo(..., { duration: 400 })`. Static evidence shows fixed-duration settling rather than velocity-aware direct manipulation. | Drive the dragged item with direct `transform` updates; settle with existing spring/velocity support if present; avoid fixed 400ms tween. |
| 6 | MEDIUM | Accessibility, cohesion | Multiple snippets | Only the button excerpt shows `prefers-reduced-motion`. Palette, popover, toast, and queue snippets do not show reduced-motion behavior. | Add per-component reduced-motion branches that preserve opacity/focus/state feedback while dropping or shortening spatial movement. |

---

## 3. Implementation-ready plans

### Plan 1 — Make popover motion tokenized, specific, and reduced-motion aware

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

**Target behavior**

- Popovers feel immediate and crisp.
- Only `transform` and `opacity` transition.
- Duration uses existing tokens.
- Easing uses the existing responsive curve.
- Reduced Motion keeps feedback but removes/shortens spatial motion.

**Project conventions to preserve**

```css
/* src/components/Button.css - existing correct local precedent */
.button {
  transition: transform var(--duration-fast) var(--ease-responsive);
}

@media (prefers-reduced-motion: reduce) {
  .button { transition-duration: 80ms; }
}
```

**Ordered steps**

1. In `src/styles/motion.css`, replace the `.popover` rule with:

   ```css
   .popover {
     transform-origin: var(--popover-transform-origin, center);
     transition:
       transform var(--duration-fast) var(--ease-responsive),
       opacity var(--duration-fast) var(--ease-responsive);
   }

   @media (prefers-reduced-motion: reduce) {
     .popover {
       transition:
         opacity 80ms var(--ease-responsive);
     }
   }
   ```

2. If the project already exposes a popover trigger-origin custom property, use that existing property name instead of `--popover-transform-origin`.

3. Do not invent geometry math from the CSS file alone. If no trigger-origin source exists in the actual popover implementation, keep the fallback and report the missing origin hook separately.

**Hard boundaries**

- Do not change popover markup, positioning, focus behavior, or portal behavior.
- Do not add dependencies.
- Do not use `transition: all`.
- Do not introduce a second easing system when `--ease-responsive` already exists.

**Mechanical checks**

- Confirm `src/styles/motion.css` no longer contains `.popover { ... transition: all ... }`.
- Confirm `.popover` transition properties are only `transform` and `opacity` in normal motion.
- Confirm a `prefers-reduced-motion: reduce` override exists for `.popover`.
- Run the existing frontend lint/type/build checks if available; do not add scripts.

**Runtime/feel checks for executor**

- Open and close a popover repeatedly.
- At slow playback, confirm the popover does not start sluggishly.
- If trigger-origin support exists, confirm it appears to originate from the trigger, not the screen center.
- Toggle Reduced Motion and confirm spatial movement is removed or greatly reduced while opacity/state feedback remains.

**Reduced Motion behavior**

- Normal: transform + opacity over `var(--duration-fast)`.
- Reduced: opacity-only over `80ms`.

**Source-drift stop condition**

- Stop if `.popover` no longer exists, if motion tokens were renamed, or if the popover implementation already defines a different trigger-origin contract. Report the new current excerpt instead of improvising.

---

### Plan 2 — Remove slow command-palette animation from the high-frequency keyboard path

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

- Opening the command palette does not wait on decorative motion.
- Search results and focus behavior are available immediately.
- The `open` state remains visible through existing rendering/state logic.
- Reduced Motion path is naturally identical because the high-frequency animation is removed.

**Project conventions to preserve**

- Keep semantic state via `data-open={open}`.
- Follow the product requirement for crisp motion and visible focus.
- Do not replace this with another long animation or custom curve.

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, remove the arbitrary animation class:

   ```tsx
   export function CommandPalette({ open }: { open: boolean }) {
     return (
       <div data-open={open}>
         <SearchResults />
       </div>
     );
   }
   ```

2. If other non-motion classes exist in the real file, preserve them and remove only `animate-[palette_420ms_ease-in_both]`.

3. Search for the `palette` keyframes or equivalent animation definition. If it is now unused, remove only that unused keyframe definition.

4. Do not add a replacement entrance animation unless product/design explicitly reclassifies this as an occasional surface rather than a high-frequency keyboard tool.

**Hard boundaries**

- Do not change command search behavior, result ordering, focus management, keyboard shortcuts, or open/close state ownership.
- Do not add transitions to child result rows as compensation.
- Do not remove `data-open={open}` unless the full component proves it is unused and tests cover the change.

**Mechanical checks**

- Confirm `CommandPalette.tsx` no longer contains `420ms`, `ease-in`, or `animate-[palette`.
- Confirm no remaining command-palette open animation exceeds `80ms`.
- Confirm TypeScript/JSX still compiles.
- Run existing frontend lint/type/build checks if available; do not add scripts.

**Runtime/feel checks for executor**

- Invoke the command palette repeatedly by keyboard.
- Confirm the palette is ready for typing immediately.
- Confirm no delayed search-result reveal blocks task throughput.
- Toggle Reduced Motion and confirm behavior is still immediate and state feedback remains clear.

**Reduced Motion behavior**

- Same as normal: no spatial command-palette animation.
- Preserve focus ring, selected result state, and open/closed state indicators.

**Source-drift stop condition**

- Stop if the class no longer exists, if the animation class also carries required visibility styles through a generated system, or if the palette is now unmounted/remounted by a different component. Report the current open/close mechanism before changing behavior.

---

### Plan 3 — Replace layout/fixed-duration dynamic movement with transform-based, interruptible motion

**Current excerpts**

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

**Target behavior**

- Toast entry uses compositor-friendly `transform` + `opacity`, not `top`.
- Toast timing is short and tokenized.
- Dragging updates the actual moving item with direct transform writes, not a parent CSS variable that may invalidate a wider subtree.
- Reorder settle uses velocity-aware spring behavior if the existing animation utility supports it; otherwise stop and flag the utility gap.
- Reduced Motion keeps opacity/state feedback and avoids spatial movement.

**Project conventions to preserve**

```css
.button {
  transition: transform var(--duration-fast) var(--ease-responsive);
}

@media (prefers-reduced-motion: reduce) {
  .button { transition-duration: 80ms; }
}
```

**Ordered steps**

1. In `src/components/toast.css`, replace the `top` keyframe with transform/opacity entry:

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

2. If the project supports `@starting-style` for mounted toast entry, prefer a transition version:

   ```css
   .toast {
     transform: translateY(0);
     opacity: 1;
     transition:
       transform var(--duration-panel) var(--ease-responsive),
       opacity var(--duration-panel) var(--ease-responsive);
   }

   @starting-style {
     .toast {
       transform: translateY(-24px);
       opacity: 0;
     }
   }

   @media (prefers-reduced-motion: reduce) {
     .toast {
       transform: none;
       transition: opacity 80ms var(--ease-responsive);
     }

     @starting-style {
       .toast {
         opacity: 0;
       }
     }
   }
   ```

   Use this transition version only if browser support/fallback policy is already acceptable for the project.

3. In `src/components/SortableQueue.tsx`, change the drag move path so the dragged item receives a direct transform update. The final code should follow this shape, adapted to the actual dragged element ref:

   ```tsx
   function onPointerMove(event: PointerEvent) {
     draggedItemRef.current?.style.setProperty(
       "transform",
       `translate3d(0, ${event.clientY}px, 0)`
     );
   }
   ```

   If the real code stores deltas rather than absolute viewport coordinates, use the existing delta value instead of `event.clientY`.

4. Replace the fixed `400` settle duration with the existing project’s spring/velocity option if `animateTo` supports one. Target shape:

   ```tsx
   function onPointerUp() {
     setDragging(false);
     animateTo(nearestSlot(currentY), {
       type: "spring",
       duration: 0.5,
       bounce: 0.2,
       velocity: currentVelocity,
     });
   }
   ```

5. If `animateTo` does not support spring or velocity, do not invent a new animation system in this change. Stop and report that the queue needs an animation utility decision.

**Hard boundaries**

- Do not change queue ordering rules, nearest-slot calculation, selection state, or persistence behavior.
- Do not add a new animation dependency.
- Do not animate `top`, `left`, `width`, `height`, margin, or padding.
- Do not keep the fixed `duration: 400` settle for drag release.
- Do not claim velocity support unless the actual `animateTo` API supports it.

**Mechanical checks**

- Confirm `toast.css` no longer animates `top`.
- Confirm toast normal motion is `transform` + `opacity`.
- Confirm toast has a `prefers-reduced-motion` branch.
- Confirm `SortableQueue.tsx` no longer drives drag position only through `queueRef.current?.style.setProperty("--drag-y", ...)`.
- Confirm no fixed `{ duration: 400 }` remains in queue release motion.
- Run existing frontend lint/type/build checks if available; do not add scripts.

**Runtime/feel checks for executor**

- Trigger multiple toasts and confirm entry is quick, not sluggish.
- In slow playback, confirm toast movement is vertical transform, not layout jump.
- Drag a queue item, reverse direction mid-drag, and confirm motion follows the pointer without lag.
- Release with small and larger velocity; confirm settle feels connected rather than a fixed-time glide.
- Toggle Reduced Motion and confirm toast uses opacity-only feedback and queue drag remains direct while nonessential settle movement is reduced.

**Reduced Motion behavior**

- Toast: opacity-only, `80ms`.
- Queue: direct pointer tracking remains because it is input feedback; nonessential release animation should be shortened or simplified. If a spring branch exists, use lower/no bounce and shorter travel feedback.

**Source-drift stop condition**

- Stop if toast styling moved, if `toast-enter` no longer exists, if `queueRef` is not involved in drag positioning, or if `animateTo` has a different API than shown. Report the new excerpts before changing behavior.

---

## 4. Recommended execution order

1. **Plan 2 — Command palette:** highest throughput impact; removes delay from a frequent keyboard path with minimal scope.
2. **Plan 1 — Popover:** fixes broad token/easing/performance debt likely shared by many small interactions.
3. **Plan 3 — Toast and sortable queue:** addresses performance and direct-manipulation quality; queue work may require checking the existing animation utility before implementation.

## Explicitly unverified states

- Actual command-palette mount/unmount behavior, focus timing, and whether the animation class also affects visibility.
- The definition of `palette` keyframes.
- Whether `.popover` is trigger-anchored, modal-like, library-backed, or manually positioned.
- Whether a trigger-origin custom property already exists.
- Toast stacking, dismissal, interrupt behavior, and DOM structure.
- Whether `--drag-y` is consumed by one element or a larger subtree.
- The `animateTo` API, spring support, and velocity availability.
- Existing package scripts, CI gates, browser support policy, and computed Reduced Motion behavior.


## Output B

## 1. Recon summary

**Stack signals**
- React/TSX components, plain CSS, CSS custom properties, Tailwind-style arbitrary animation class, and imperative pointer-driven animation.
- Motion currently lives in global CSS, component CSS, inline utility animation strings, and JS animation calls.

**Existing conventions**
- Motion tokens exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
- One correct local precedent exists in `Button.css`: explicit property transition, tokenized duration/easing, reduced-motion override that preserves feedback by shortening duration.

**Product personality**
- Calm, workday-long desktop operations surface.
- Motion should explain causality and continuity, not decorate or delay keyboard throughput.
- Reduced Motion must retain state feedback, not simply remove all cues.

**Frequency map from static evidence**
- **Very high frequency / keyboard-critical:** `CommandPalette`.
- **Likely reusable / high surface area:** `.popover`, though exact usage is unverified.
- **High interaction intensity when active:** `SortableQueue` drag/settle.
- **Intermittent feedback:** `.toast`.
- **Validated local precedent:** `.button`.

**Evidence level**
- Static snippet audit only.
- No runtime, computed-style, trace, screen recording, accessibility-tree, device, or user validation was performed.

---

## 2. Priority table

| Priority | Finding | Static evidence | Risk | Recommended fix |
|---:|---|---|---|---|
| P0 | Motion system is inconsistent across components | `160ms`, `240ms`, `360ms`, `400ms`, `420ms`, `500ms`; mixed `ease-in`, `ease-responsive`, `all` | Operators experience different timing rules for similar UI state changes | Normalize to existing tokens and explicit motion roles |
| P0 | `.popover` uses broad, slow, non-tokenized transition | `transition: all 360ms ease-in;` | Unintended properties may animate; timing conflicts with crisp system requirement | Restrict to `opacity, transform`; use `--duration-panel` and `--ease-responsive` |
| P0 | Command palette animation is long, arbitrary, and lacks visible reduced-motion path | `animate-[palette_420ms_ease-in_both]` | High-frequency keyboard surface may feel delayed; behavior is hard to govern centrally | Replace arbitrary class with named class using tokens and reduced-motion override |
| P1 | Toast animates layout property and runs 500ms | `top: -24px → 0`, `500ms ease-in` | Feedback may feel heavy; layout-affecting animation is avoidable | Animate `transform` + `opacity`; shorten/tokenize |
| P1 | Sortable settle motion is hard-coded and not reduced-motion aware | `animateTo(..., { duration: 400 })` | Direct manipulation may not follow the same timing contract as the rest of the UI | Tokenize settle duration; add reduced-motion branch |
| P2 | Reduced Motion appears local, not systematic | Only `.button` has `@media (prefers-reduced-motion: reduce)` | Similar interactions may provide inconsistent accessibility feedback | Use the button pattern as baseline across overlays, feedback, and drag settle |

---

## 3. Implementation plans

### Plan A — Normalize the shared motion contract and repair popover

**File path / current excerpt**

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
- Popovers enter/exit with crisp opacity/transform continuity.
- No broad `transition: all`.
- Timing uses existing semantic tokens.
- Reduced Motion keeps state feedback with shorter, smaller movement.

**Project conventions to follow**
- Reuse existing custom properties.
- Match the proven button pattern: explicit animated property, tokenized duration/easing, local reduced-motion override.
- Do not introduce decorative spring/bounce behavior.

**Ordered steps**
1. Replace `.popover` transition with explicit properties:
   - `opacity`
   - `transform`
2. Use existing token timing:
   - duration: `var(--duration-panel)`
   - easing: `var(--ease-responsive)`
3. Add state classes or data-state selectors only if the existing markup already exposes open/closed state.
4. Add reduced-motion override:
   - shorten transition duration to `80ms` or reuse a reduced token if one already exists nearby.
   - keep opacity/state feedback.
   - reduce or remove travel distance, not the entire feedback.
5. Grep for other `transition: all` motion rules and queue them for follow-up, but do not expand scope in this change.

**Hard boundaries**
- Do not rename existing tokens unless a broader migration is approved.
- Do not change popover positioning, focus behavior, dismissal behavior, or stacking.
- Do not add a motion library.

**Mechanical checks**
- Search for remaining `transition: all` in the changed file.
- Confirm `.popover` still uses existing token names.
- Confirm a `prefers-reduced-motion: reduce` branch exists for popover motion.
- Run closest available lint/type/build command after implementation.

**Runtime/feel checks to perform later**
- Open/close popover from keyboard and pointer.
- Verify perceived duration feels under the panel token, not delayed.
- Confirm focus outline remains visible throughout transition.
- Confirm Reduced Motion still communicates open/close state.

**Reduced Motion behavior**
- Use shortened duration, minimal transform distance, and opacity/state cue.
- Do not remove all feedback unless the platform preference or existing system explicitly requires no animation.

**Source-drift stop condition**
- Stop and re-audit if `src/styles/motion.css` no longer owns popover styling, token names changed, or popover state is controlled by a separate component/style system not shown here.

---

### Plan B — Replace command palette arbitrary animation with governed overlay motion

**File path / current excerpt**

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
- Command palette feels immediate for keyboard-heavy operators.
- Open/close motion preserves spatial continuity but does not slow command entry.
- Motion is named, tokenized, inspectable, and reduced-motion aware.

**Project conventions to follow**
- Replace arbitrary inline animation with a stable class name.
- Use `--duration-fast` or `--duration-panel` depending on actual visual distance:
  - small opacity/scale: `--duration-fast`
  - panel-like movement: `--duration-panel`
- Use `--ease-responsive`, not `ease-in`.

**Ordered steps**
1. Replace the arbitrary class with a named class, for example:
   - `className="command-palette-motion"`
   - keep `data-open={open}`.
2. Define the class in the existing component stylesheet or shared motion stylesheet already imported by this component path.
3. Implement open/closed selectors using `data-open`:
   - open: `opacity: 1; transform: translateY(0) scale(1);`
   - closed: `opacity: 0; transform: translateY(-4px) scale(0.98);`
4. Use transition rather than one-off animation if the element remains mounted and `data-open` changes.
5. If the element unmounts immediately when closed elsewhere, stop and coordinate with mounting logic before attempting exit motion.
6. Add reduced-motion override:
   - shorter duration.
   - opacity/state cue preserved.
   - no meaningful scale/travel.

**Hard boundaries**
- Do not alter `SearchResults` behavior.
- Do not change command execution, keyboard shortcuts, focus order, or focus trap behavior in this motion-only pass.
- Do not assume exit animation works if the component unmounts immediately; verify implementation structure first.

**Mechanical checks**
- Confirm no `animate-[palette_420ms_ease-in_both]` remains.
- Confirm command palette motion uses existing token names.
- Confirm no `ease-in` remains for this component’s primary open/close motion.
- Confirm reduced-motion CSS is present.
- Run closest available type/lint/build command after implementation.

**Runtime/feel checks to perform later**
- Open palette repeatedly via keyboard shortcut.
- Type immediately after opening; verify motion does not block perceived readiness.
- Close with Escape; verify state change is clear.
- Check focus visibility during transition.
- Repeat with Reduced Motion enabled.

**Reduced Motion behavior**
- Prefer `80ms` opacity-only or near-opacity-only transition.
- Preserve clear open/closed feedback.
- Avoid scale and travel in reduced mode.

**Source-drift stop condition**
- Stop if command palette styling is generated elsewhere, if the component unmounts on close before styles can transition, or if a dedicated overlay primitive already owns this behavior.

---

### Plan C — Make transient feedback and drag settle motion direct, tokenized, and reduced-motion aware

**File paths / current excerpts**

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
- Toasts appear quickly, without layout-position animation.
- Dragged queue items track pointer movement directly while active.
- Release/settle motion is brief, causal, and consistent with panel/fast tokens.
- Reduced Motion preserves feedback with immediate or near-immediate state resolution.

**Project conventions to follow**
- Prefer transform/opacity over layout properties for motion.
- Use existing duration/easing tokens.
- Keep direct manipulation under user control; animate only the settle/reconciliation phase.

**Ordered steps — toast**
1. Replace `top` keyframes with `transform`:
   - from: `transform: translateY(-8px); opacity: 0;`
   - to: `transform: translateY(0); opacity: 1;`
2. Replace `500ms ease-in` with:
   - `var(--duration-panel) var(--ease-responsive)` or `var(--duration-fast)` if the toast is compact.
3. Add reduced-motion override:
   - `80ms`
   - opacity-only or `translateY(-2px)` maximum.
4. Confirm final resting position is still controlled by layout, not animation.

**Ordered steps — sortable queue**
1. Inspect whether `--drag-y` is consumed as an absolute viewport coordinate or transformed into local movement.
2. If it is intended as movement, convert from `event.clientY` absolute value to a local delta from drag start.
3. Keep pointer-move writes limited to the dragged element or queue container already using the custom property.
4. If pointer frequency causes excessive writes, batch style writes with `requestAnimationFrame`.
5. Replace hard-coded `duration: 400` with a named duration constant aligned to existing tokens.
6. Add a reduced-motion branch:
   - on release, snap or use very short settle.
   - preserve slot/state confirmation through position, focus, outline, or selection state.
7. Ensure nearest-slot calculation remains unchanged unless a bug is found during implementation.

**Hard boundaries**
- Do not change queue ordering rules.
- Do not change drag hit testing, selection semantics, or persistence behavior.
- Do not infer performance problems from the snippet alone; only remove avoidable animation risk.
- Do not make toast dismissal, timeout, or stacking changes in this pass.

**Mechanical checks**
- Confirm toast no longer animates `top`.
- Confirm toast duration/easing use existing tokens.
- Confirm sortable settle no longer uses raw `400` inline.
- Confirm reduced-motion handling exists for both toast and sortable settle.
- Run closest available type/lint/build command after implementation.

**Runtime/feel checks to perform later**
- Toast: trigger success, warning, and error variants if they exist; verify entrance is noticeable but not attention-heavy.
- Toast: verify no position jump at rest.
- Queue: drag slowly and quickly; verify item tracks pointer without delayed chase.
- Queue: release near slot boundaries; verify settle communicates final slot.
- Queue: repeat with Reduced Motion enabled.

**Reduced Motion behavior**
- Toast: short opacity cue; minimal or no travel.
- Queue: direct drag remains direct; release snap is immediate or near-immediate, with visible final-state confirmation.

**Source-drift stop condition**
- Stop if a toast primitive, drag library, or shared animation helper already owns these behaviors outside the shown files, or if `animateTo` has its own global reduced-motion configuration.

---

## 4. Recommended execution order

1. **Plan A first:** establishes the shared contract and removes the riskiest broad transition pattern.
2. **Plan B second:** fixes the highest-frequency keyboard surface.
3. **Plan C third:** improves transient feedback and direct manipulation without widening scope.

## Explicitly unverified states

- Actual computed durations/easing in the built app.
- Whether command palette remains mounted during close.
- Whether `.popover` is globally reused or locally scoped.
- Whether `--drag-y` is consumed as absolute position or delta.
- Whether existing build tooling includes lint, type-check, visual tests, or reduced-motion tests.
- Actual keyboard focus behavior, screen reader output, paint/layout cost, frame rate, and user-perceived feel.


## Output C

## 1. Recon summary

**Motion diagnosis:** the excerpts show a calm operations product with a useful local motion precedent, but several high-frequency or task-critical motions bypass the token system, use slow `ease-in` timing, animate broad/layout properties, and lack an explicit Reduced Motion path.

- **Stack signals:** React/TSX components, CSS modules/files, global CSS variables, Tailwind-style arbitrary animation class, and at least one JS animation helper (`animateTo`).
- **Where motion lives:**  
  - Global tokens: `src/styles/motion.css`  
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`  
  - Inline/class motion: `src/components/CommandPalette.tsx`  
  - Pointer/gesture logic: `src/components/SortableQueue.tsx`
- **Existing conventions:** semantic duration/easing tokens exist:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
  - Correct local precedent: button animates only `transform`, uses tokens, and has a Reduced Motion branch.
- **Product personality:** crisp, calm, utility-first desktop operations console; motion should clarify causality without adding perceived latency.
- **Frequency map:**  
  - **Very high:** command palette, keyboard-triggered flows, buttons.  
  - **High/repeated:** popovers, sortable queue manipulation.  
  - **Occasional but noticeable:** toasts.  
- **Evidence level:** static snippets only. No runtime smoothness, interruption quality, computed styles, accessibility-tree behavior, device feel, or performance trace is verified.

---

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | `className="animate-[palette_420ms_ease-in_both]"` | `src/components/CommandPalette.tsx` | Command palette uses a long, arbitrary, `ease-in` animation on a likely high-frequency keyboard surface; no Reduced Motion branch is shown. | Move to named/tokenized CSS state styles, target ~160–200ms, use responsive ease, preserve instant keyboard feedback, add Reduced Motion behavior. |
| P1 | `animateTo(nearestSlot(currentY), { duration: 400 })` | `src/components/SortableQueue.tsx` | Drag settle appears fixed-duration and release-position based; snippet does not show pointer capture, grab offset, measured velocity, interruption from presentation value, or Reduced Motion handling. | Preserve existing `nearestSlot` target semantics, but implement measured release velocity, presentation-value retargeting, pointer capture, and reduced settle motion. |
| P2 | `transition: all 360ms ease-in; transform-origin: center;` | `src/styles/motion.css` | Popover owns all transitioned properties, uses slow-start easing, and has centered origin that may be wrong for trigger-anchored overlays. Static evidence cannot prove which properties change. | Replace with explicit `opacity, transform`; use existing duration/easing tokens; make origin trigger-aware if the positioning layer exposes an origin variable. |
| P2 | `top: -24px → top: 0`, `500ms ease-in` | `src/components/toast.css` | Toast entry animates a layout property and uses a slow 500ms ease-in. This is a performance and feel risk; static evidence does not prove dropped frames. | Animate `transform` + `opacity`, reduce to tokenized 160–240ms, add Reduced Motion branch. |
| P2 | Multiple literals/arbitrary motion values: `360ms`, `420ms`, `500ms`, `400` | Multiple excerpts | Motion vocabulary is fragmented despite existing tokens and a correct local precedent. | Route common UI motion through semantic tokens and reserve literals for documented exceptions. |
| P3 | Button has Reduced Motion precedent; other excerpts do not | `src/components/Button.css` versus others | Reduced Motion behavior is inconsistent in supplied snippets. Shorter duration alone is not a complete path for spatial motion. | For overlays/toasts/drag settle, remove or minimize travel while preserving opacity/color/static state feedback. |

---

## 3. Implementation-ready plans

### Plan A — Tokenize and tighten overlay motion: popover + command palette

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
<div
  data-open={open}
  className="animate-[palette_420ms_ease-in_both]"
>
```

**Target behavior**

- Popovers and palette feel immediate, crisp, and causal.
- Only `opacity` and `transform` are animated unless a specific property is intentionally added.
- Command palette does not impose a long keyboard-path delay.
- Reduced Motion keeps visibility/state feedback without meaningful travel.

**Project conventions to use**

- Use `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Follow the button precedent: explicit animated property, semantic tokens, Reduced Motion branch.
- Preserve visible focus; do not replace focus feedback with motion.

**Ordered steps**

1. In `src/styles/motion.css`, add/standardize named overlay motion rules for `.popover` and a command-palette class.
2. Replace `.popover { transition: all 360ms ease-in; }` with explicit properties, for example:
   - `opacity var(--duration-fast) var(--ease-responsive)`
   - `transform var(--duration-fast) var(--ease-responsive)`
3. Replace `transform-origin: center` with a trigger-aware origin only if the positioning primitive exposes one; otherwise use a safe fallback such as `var(--popover-transform-origin, center)` and document the fallback.
4. In `src/components/CommandPalette.tsx`, replace the arbitrary animation class with the named class while preserving `data-open={open}`.
5. Define closed/open state selectors using `data-open`, e.g. opacity and a very small scale/translate only when open/closed state is known.
6. Add a `prefers-reduced-motion: reduce` branch:
   - remove scale/translate travel;
   - keep short opacity or color/state transition, around the local 80ms precedent;
   - preserve focus visibility.

**Hard boundaries**

- Do not change command search behavior, result ordering, focus model, or keyboard shortcuts.
- Do not introduce a new animation library for these CSS-state overlays.
- Do not change button motion except as a reference for consistency.
- Do not assume the popover is trigger-anchored unless the component/positioning code proves it.

**Mechanical checks**

- Search for remaining `animate-[palette_` and `.popover { transition: all`.
- Search for new `ease-in` on overlay enter paths.
- Run the project’s closest static checks if available: type-check, lint, CSS lint/build.
- Confirm no focus-visible selector was removed.

**Runtime/feel checks required later, not performed here**

- Open/close command palette repeatedly by keyboard.
- Reverse open/close mid-transition.
- Inspect popover origin for each placement/collision side.
- Confirm no interaction is blocked while animation plays.

**Reduced Motion behavior**

- No scale/position travel for palette/popover.
- Opacity or static state feedback remains.
- Focus ring remains visible and unaffected.

**Source-drift stop condition**

Stop before editing if `CommandPalette` no longer uses `data-open`, `.popover` is owned by a third-party primitive with different state attributes, the token names changed, or the style authority no longer defines crisp tokenized motion as the target.

---

### Plan B — Convert toast entrance from layout keyframes to tokenized transform/opacity

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

- Toast entry is quick enough for operations work and does not feel like a blocking banner.
- Motion communicates arrival without layout-position animation.
- Toast Reduced Motion preserves noticeability without vertical travel.

**Project conventions to use**

- Use existing duration/easing tokens.
- Prefer `transform` and `opacity`.
- Follow local Reduced Motion precedent from button CSS.

**Ordered steps**

1. Replace `top` animation in `@keyframes toast-enter` with `transform: translateY(...)` and `opacity`.
2. Reduce duration from `500ms` to a tokenized value:
   - default start: `var(--duration-panel)` if the toast is more banner-like;
   - use `var(--duration-fast)` if it is small and frequent.
3. Replace `ease-in` with `var(--ease-responsive)`.
4. If the toast component has explicit lifecycle state such as `data-state="open"` / `closed`, prefer transitions over one-shot keyframes so repeated triggers can retarget more naturally.
5. Add a Reduced Motion branch:
   - no vertical transform;
   - short opacity transition or immediate opacity change;
   - keep any icon/color/status semantics intact.
6. If toast stacking exists, verify the CSS does not create animated gaps that break pointer hit regions.

**Hard boundaries**

- Do not change toast copy, severity colors, dismissal semantics, timers, or announcement behavior.
- Do not infer stacked-toast behavior from this CSS alone.
- Do not claim performance improvement until runtime is measured.

**Mechanical checks**

- Search `toast-enter` for remaining `top:` animation.
- Search `toast.css` for `500ms ease-in`.
- Run the project’s CSS/static checks if available.
- Verify no severity/focus/dismiss selectors were removed.

**Runtime/feel checks required later, not performed here**

- Trigger multiple toasts quickly.
- Dismiss during entry.
- Check document hidden/visible behavior if timers exist.
- Confirm screen-reader announcement behavior if toast is announced.
- Toggle Reduced Motion and confirm arrival feedback remains.

**Reduced Motion behavior**

- Remove vertical travel.
- Preserve visibility through opacity/static state.
- Keep dismissal and focus behavior unchanged.

**Source-drift stop condition**

Stop before editing if toast markup lacks a stable `.toast` class, the lifecycle is controlled by a library with required animation hooks, or toast positioning depends on `top` for actual layout rather than visual entry.

---

### Plan C — Make sortable queue drag settle interruptible and direct-manipulation safe

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

- Dragged item tracks the pointer without snapping unexpectedly.
- Release settle starts from the current on-screen value.
- Existing `nearestSlot(currentY)` target semantics are preserved unless product owners explicitly approve momentum-based target selection.
- Reduced Motion removes bounce/large settle travel while keeping reorder feedback.

**Project conventions to use**

- Use existing motion tokens when CSS timing is involved.
- Avoid broad parent style invalidation on large trees where possible.
- Preserve calm, non-bouncy operations-console motion.

**Ordered steps**

1. On pointer down, record:
   - pointer id;
   - initial pointer Y;
   - item’s current visual Y;
   - grab offset between pointer and item origin.
2. Call pointer capture once drag intent is established, so movement continues outside the original bounds.
3. On pointer move:
   - compute local drag Y using the recorded offset, not raw `event.clientY`;
   - update only the dragged item or a narrow wrapper, not a broad queue parent, unless current CSS proves the variable is scoped narrowly;
   - coalesce writes through `requestAnimationFrame` if pointer events are high frequency.
4. Maintain a short timestamped sample history in CSS pixels and monotonic time.
5. On pointer up:
   - compute release velocity in CSS px/s;
   - preserve `nearestSlot(currentY)` as the target rule for the first implementation;
   - pass current presentation Y and bounded release velocity into the settle animation if `animateTo` supports it.
6. If `animateTo` cannot start from presentation value or accept velocity, replace only the settle primitive with an existing project-approved animation mechanism; do not add a new dependency without approval.
7. Add cancellation handling for pointer cancel/lost capture.
8. Add Reduced Motion branch:
   - no elastic overshoot;
   - immediate or very short settle;
   - static selected/reordered feedback remains visible.

**Hard boundaries**

- Do not change queue ordering rules, nearest-slot semantics, persistence, selection, or keyboard reorder behavior.
- Do not add momentum-based target selection by default.
- Do not introduce bounce unless explicitly authorized and verified.
- Do not make source-wide animation abstractions from this one component.

**Mechanical checks**

- Type-check `PointerEvent` handling.
- Verify pointer capture cleanup paths exist.
- Search for competing writers to `--drag-y` or the dragged element’s `transform`.
- Run unit tests for reorder logic if present.
- Run lint/type-check/build if available.

**Runtime/feel checks required later, not performed here**

- Drag slowly and release.
- Flick quickly and release.
- Reverse direction during settle.
- Drag outside original bounds.
- Trigger pointer cancel/lost capture.
- Test keyboard reorder path still works.
- Verify Reduced Motion settle.

**Reduced Motion behavior**

- Keep direct tracking while dragging; it is causal input feedback.
- On release, remove bounce/overshoot and minimize settle duration.
- Preserve clear final-slot feedback through static position, color, outline, or status text.

**Source-drift stop condition**

Stop before editing if `animateTo` already has a spring/presentation-value API not shown here, `currentY` is no longer the release coordinate, `--drag-y` is consumed by multiple descendants, or queue ordering semantics changed from nearest-slot to a different rule.

---

## 4. Recommended execution order

1. **Plan A first:** highest frequency and easiest cohesion win; establishes shared overlay vocabulary.
2. **Plan B second:** small, isolated correction from layout/slow toast motion to tokenized transient feedback.
3. **Plan C third:** highest interaction complexity; requires careful runtime feel verification and should not be rushed from static evidence alone.

## Explicitly unverified states

- Actual visual smoothness, frame pacing, compositing, and layout cost.
- Whether popovers are trigger-anchored, centered, or library-positioned.
- Command palette focus trapping/restoration and keyboard timing.
- Toast lifecycle, stacking, timers, dismissal, and announcements.
- Sortable queue grab offset, pointer capture, transform ownership, velocity behavior, and keyboard reorder parity.
- Reduced Motion behavior outside the button excerpt.
- Computed styles, browser support, device refresh rate, and real operator perception.
