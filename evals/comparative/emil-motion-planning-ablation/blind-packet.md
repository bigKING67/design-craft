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

- **Stack signals**: React/TSX components plus CSS/Tailwind-style arbitrary animation classes. Motion appears to be mostly CSS transitions/keyframes with some JS-driven gesture animation.
- **Where motion lives**:
  - Global tokens and shared classes: `src/styles/motion.css`
  - Component-local animation CSS: `src/components/toast.css`, `src/components/Button.css`
  - Inline utility animation: `src/components/CommandPalette.tsx`
  - Gesture JS: `src/components/SortableQueue.tsx`
- **Existing conventions**:
  - Tokens exist: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`.
  - Correct local precedent exists in `Button.css`: transform-only transition, tokenized duration/easing, and a Reduced Motion branch that shortens rather than removes feedback.
- **Product personality**: calm desktop operations console. Motion should be crisp, causal, and low-latency; decorative or sluggish motion is a throughput cost.
- **Frequency map from provided context**:
  - Very high frequency / keyboard-heavy: command palette.
  - High sensitivity / direct manipulation: sortable queue drag/release.
  - Occasional but visible: popovers and toasts.
  - Correct precedent: button press feedback.
- **Evidence level**: static snippet audit only. Findings below are based on explicit code values/properties shown. No runtime feel, computed style, browser trace, accessibility tree, or device validation was performed.

---

## 2. Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose / frequency | `src/components/CommandPalette.tsx` | Command palette uses `animate-[palette_420ms_ease-in_both]`. For keyboard-heavy operators, a 420ms ease-in entrance delays a high-frequency action. | Remove the entrance animation or reduce it to immediate state change; preserve focus/visibility without motion. |
| 2 | HIGH | Performance / easing / cohesion | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in;`. This animates unintended properties, exceeds existing token rhythm, and starts slowly. | Transition only `transform` and `opacity` using existing tokens; add Reduced Motion handling. |
| 3 | HIGH | Gesture / interruptibility | `src/components/SortableQueue.tsx` | Pointer move writes `--drag-y` on the queue root, and release uses fixed `duration: 400`. Static evidence suggests parent-wide style recalculation risk and non-velocity-aware release. | Drive transform on the dragged item, preserve velocity into release, use a spring-like settle if supported, and branch for Reduced Motion. |
| 4 | MEDIUM | Performance / accessibility | `src/components/toast.css` | Toast animates `top` from `-24px` to `0` over `500ms ease-in`; this is layout-affecting, slow, and has no shown Reduced Motion path. | Animate `transform` + `opacity` with existing panel duration/easing; Reduced Motion should keep opacity feedback and remove travel. |
| 5 | MEDIUM | Reduced Motion coverage | Multiple snippets | Only `Button.css` shows `prefers-reduced-motion`. Popover, command palette, toast, and queue snippets do not. | Copy the button precedent: preserve feedback, shorten/remove movement, avoid disabling all state indication. |
| 6 | MEDIUM | Token cohesion | `CommandPalette.tsx`, `toast.css`, `motion.css` | Motion values are hand-authored: `420ms ease-in`, `500ms ease-in`, `360ms ease-in`, despite available semantic tokens. | Route common UI motion through existing duration/easing tokens and avoid arbitrary one-off values. |

---

## 3. Implementation plans

### Plan 1 — Remove delayed command-palette motion

**Exact file/current excerpt**

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

- Opening/closing the command palette must feel immediate for keyboard-heavy repeated use.
- Remove the 420ms ease-in animation from the palette container.
- Do not add replacement decorative motion.
- Preserve `data-open={open}` because it may be used by styling/tests.
- Preserve focus behavior and search result rendering.

**Project conventions to follow**

- Existing motion tokens prefer crisp durations and `--ease-responsive`.
- Existing correct precedent: `src/components/Button.css` keeps subtle transform feedback and Reduced Motion support.
- For this specific high-frequency keyboard surface, the preferred motion is no entrance animation.

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, remove only the arbitrary animation class:
   ```tsx
   <div data-open={open}>
     <SearchResults />
   </div>
   ```
2. If removing `className` would break existing class composition in the real file, keep the other classes and remove only:
   ```tsx
   animate-[palette_420ms_ease-in_both]
   ```
3. Search for the `palette` keyframe/animation definition. If it is now unused, remove it only if it is local to the command palette and not referenced elsewhere.
4. Do not replace this with a shorter transition unless product/design review explicitly requests one.

**Hard boundaries**

- Do not change command search logic, shortcut handling, focus management, or result rendering.
- Do not add a motion library.
- Do not add enter/exit state machines.
- If the palette relies on the animation class for visibility, mounting, or pointer-event state, stop and report source drift instead of guessing.

**Mechanical checks**

- Confirm no `animate-[palette_420ms_ease-in_both]` remains in `src/components/CommandPalette.tsx`.
- Search targeted files for `palette_420ms` / `@keyframes palette`; remove only confirmed dead local code.
- Run the project’s existing lint/typecheck gate if available.

**Runtime/feel checks for executor**

- Open the palette via keyboard shortcut repeatedly.
- Confirm it appears immediately without a slow fade/slide.
- Confirm search input focus is not delayed.
- Confirm closing/reopening rapidly does not show stale transitional states.

**Reduced Motion behavior**

- No special branch required if the animation is removed.
- Reduced Motion users should receive the same immediate state change.

**Source-drift stop condition**

- Stop if the real component has additional class composition, visibility styles, or transition hooks not shown here and the animation class cannot be removed independently.

---

### Plan 2 — Tokenize and de-risk popover/toast motion

**Exact files/current excerpts**

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

- Popovers: transition only compositor-safe properties; use existing duration/easing tokens; avoid `transition: all`; include Reduced Motion duration reduction.
- Toasts: enter using `transform` and `opacity`, not `top`; use existing `--duration-panel` and `--ease-responsive`; Reduced Motion keeps opacity feedback and removes vertical travel.
- Keep the calm operations-console feel: quick, legible, not bouncy.

**Project conventions to follow**

- Use existing tokens:
  ```css
  --duration-fast: 160ms;
  --duration-panel: 240ms;
  --ease-responsive: cubic-bezier(0.23, 1, 0.32, 1);
  ```
- Follow the existing button precedent:
  ```css
  @media (prefers-reduced-motion: reduce) {
    .button { transition-duration: 80ms; }
  }
  ```

**Ordered steps**

1. In `src/styles/motion.css`, replace the popover transition with explicit properties:
   ```css
   .popover {
     transform-origin: center;
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
2. If the real popover is trigger-anchored and the component system exposes a trigger-origin CSS variable, replace `center` with that variable. If no such variable exists in the codebase, keep `center` rather than inventing geometry.
3. In `src/components/toast.css`, replace layout animation with transform animation:
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
       from {
         transform: none;
         opacity: 0;
       }
       to {
         transform: none;
         opacity: 1;
       }
     }

     .toast {
       animation-duration: 80ms;
     }
   }
   ```
4. If redefining `@keyframes toast-enter` inside the media query conflicts with the project’s CSS tooling, create a separate reduced-motion keyframe:
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

- Do not change toast placement, stacking logic, dismissal timing, or content.
- Do not animate `top`, `left`, `width`, `height`, `margin`, or `padding`.
- Do not introduce new token names unless the existing token file explicitly requires aliases.
- Do not change `.button`; it is the correct precedent.

**Mechanical checks**

- Confirm targeted files no longer contain:
  - `transition: all`
  - `360ms ease-in`
  - `500ms ease-in`
  - `from { top:`
- Confirm popover/toast use `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Run existing lint/build/style checks if available.

**Runtime/feel checks for executor**

- Trigger popovers repeatedly and confirm there is no sluggish start.
- Trigger a toast and confirm it slides/fades quickly without layout jump.
- In slow-motion DevTools playback, confirm the toast moves via `transform`, not `top`.
- Toggle Reduced Motion and confirm toast movement is removed while fade feedback remains.

**Reduced Motion behavior**

- Popover: duration shortens to `80ms`; no extra travel should be added.
- Toast: movement removed; opacity feedback remains over `80ms`.

**Source-drift stop condition**

- Stop if `.popover` or `.toast` are not the real rendered classes, or if visibility/positioning depends on the removed animation properties.

---

### Plan 3 — Make sortable queue drag directly manipulated and motion-safe

**Exact file/current excerpt**

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

- During drag, the actively dragged item follows the pointer directly.
- Do not drive child movement through a parent-level CSS variable unless the real implementation proves that only one isolated element depends on it.
- On release, settle to the nearest slot with interruptible, velocity-aware motion if the existing `animateTo` helper supports it.
- Reduced Motion should avoid travel animation while preserving the committed reorder/state feedback.

**Project conventions to follow**

- Existing motion is token-based and crisp.
- For direct manipulation, visual response should track input immediately.
- Fixed 400ms release is too slow for a throughput-focused queue unless justified elsewhere in code.

**Ordered steps**

1. Inspect the real `SortableQueue.tsx` around the drag refs/state before editing.
2. Identify the dragged item element ref. If none exists, add a local ref to the dragged item only; do not attach movement styles to the queue root.
3. Replace parent CSS-variable updates with direct dragged-item transform updates. Target pattern:
   ```tsx
   function onPointerMove(event: PointerEvent) {
     const nextY = event.clientY;
     currentY = nextY;

     draggedItemRef.current?.style.setProperty(
       "transform",
       `translate3d(0, ${nextY - dragStartY}px, 0)`
     );
   }
   ```
   Use the real state/ref names from the file; do not invent parallel drag state if equivalents already exist.
4. Track release velocity using the last pointer positions/timestamps:
   ```tsx
   const velocityY = (currentY - previousY) / Math.max(1, now - previousTime);
   ```
5. On pointer up, project the target slightly by velocity before selecting the nearest slot:
   ```tsx
   const projectedY = currentY + velocityY * 120;
   const targetSlot = nearestSlot(projectedY);
   ```
6. If `animateTo` supports spring-style options, replace fixed duration with:
   ```tsx
   animateTo(targetSlot, {
     type: "spring",
     duration: 0.5,
     bounce: 0.2,
     velocity: velocityY
   });
   ```
7. If `animateTo` does not support spring or velocity, reduce the fixed settle duration to the existing panel token equivalent if the helper accepts tokenized duration, or `240` ms if it requires a number:
   ```tsx
   animateTo(targetSlot, { duration: 240 });
   ```
   Do not add a new animation dependency.
8. Add a Reduced Motion branch using `window.matchMedia("(prefers-reduced-motion: reduce)")` or the project’s existing reduced-motion helper if one exists:
   - normal motion: drag follows pointer and settles with spring/short tween.
   - reduced motion: commit to `nearestSlot(currentY)` immediately or with an `80ms` opacity/color/state cue, but no travel animation.

**Hard boundaries**

- Do not rewrite queue data modeling or reorder semantics.
- Do not add dependencies.
- Do not change keyboard reordering behavior unless it already shares this animation path.
- Do not introduce bounce beyond `0.2`.
- If multiple queue children intentionally depend on `--drag-y` for collision/preview positioning, stop and split this into a larger queue-motion design task.

**Mechanical checks**

- Confirm `queueRef.current?.style.setProperty("--drag-y"` is removed or proven isolated.
- Confirm the dragged element receives `transform: translate3d(...)`.
- Confirm no layout property is animated for drag settle.
- Confirm `duration: 400` is removed from the release path or justified by an explicit existing design comment.
- Run existing typecheck/lint gate if available.

**Runtime/feel checks for executor**

- Drag slowly: item should stay under the pointer without visible lag.
- Drag quickly and release: settle should continue the release direction rather than stopping then restarting.
- Interrupt by dragging again during settle: motion should retarget cleanly, not jump from the original start.
- Toggle Reduced Motion: reordering should remain understandable without travel animation.

**Reduced Motion behavior**

- Pointer tracking can remain direct while the user is actively dragging.
- Release animation should be removed or shortened to `80ms` non-spatial feedback.
- State continuity should be preserved through slot highlight, opacity, or final placement—not through long movement.

**Source-drift stop condition**

- Stop if the real queue uses a drag library, virtualization, collision engine, or CSS-variable choreography not visible in the snippet. In that case, produce a smaller follow-up plan for that concrete implementation rather than applying this generic refactor.

---

## 4. Recommended execution order

1. **Command palette** — highest throughput impact and smallest safe change.
2. **Popover/toast tokenization** — removes broad `transition: all`, layout animation, slow ease-in, and adds Reduced Motion coverage.
3. **Sortable queue** — highest craft payoff but most source-dependent; execute only after inspecting the real drag implementation.

## Explicitly unverified states

- Actual framework/library choices beyond React/CSS/Tailwind-style class evidence.
- Whether `.popover` is trigger-anchored, modal-like, or used for multiple component types.
- Whether the command palette animation controls visibility or only decorative entrance.
- Whether `animateTo` supports spring, velocity, cancellation, or tokenized durations.
- Actual focus behavior, keyboard shortcut flow, accessibility tree, frame rate, layout cost, and user-perceived feel.
- Existing package scripts, lint/typecheck/build commands, and CSS tooling support for media-scoped keyframes.


## Output B

## 1. Recon summary

**Motion diagnosis:** the snippets show a useful local precedent for crisp transform-based feedback, but several higher-frequency or state-continuity surfaces drift into long `ease-in`, keyframed, layout-property, or non-interruptible-looking motion that is risky for a calm keyboard-heavy operations console.

- **Stack signals:** React/TSX components, CSS custom-property tokens, plain CSS transitions/keyframes, Tailwind-style arbitrary animation utility, and a JS `animateTo(...)` gesture settle call.
- **Where motion lives:** `src/styles/motion.css`, component-level TSX class strings, component CSS files, pointer handlers, and local component CSS precedents.
- **Existing conventions evidenced:** `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`, transform-based button press, and a local `prefers-reduced-motion` branch.
- **Product personality:** calm, crisp, low-latency utility motion; motion should explain state/causality, not add ceremony.
- **Frequency map:** buttons and command palette = high-frequency; sortable queue = repeated direct manipulation; popovers = regular overlays; toasts = occasional status feedback.
- **Evidence level:** static excerpts only. No runtime smoothness, computed styles, keyframe definitions beyond shown CSS, accessibility tree, screen recording, trace, or device validation was performed.

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | `animate-[palette_420ms_ease-in_both]` | `src/components/CommandPalette.tsx` | High-frequency keyboard surface uses a long one-off `ease-in` animation; static evidence does not show a Reduced Motion path. | Replace with state-driven opacity/very small transform using `--duration-fast`/`--duration-panel` and `--ease-responsive`; Reduced Motion keeps feedback without travel. |
| P1 | `animateTo(nearestSlot(currentY), { duration: 400 })` and pointer move writes `--drag-y` | `src/components/SortableQueue.tsx` | Direct manipulation excerpt does not evidence pointer capture, grab offset, presentation-value interruption, or measured release velocity; fixed-duration settle risks discontinuity. | Define coordinate space, preserve grab offset, track px/s velocity, settle from current presentation value, pass velocity into the settle; preserve existing nearest-slot target unless momentum targeting is explicitly authorized. |
| P2 | `transition: all 360ms ease-in` | `src/styles/motion.css` | Popover motion owns all properties, uses slow-start easing, and uses center origin without evidence that every popover is centered. | Limit to `opacity, transform`, use responsive token timing/easing, and make origin trigger-relative or split centered modal usage from anchored popovers. |
| P2 | `top: -24px` to `top: 0`; `500ms ease-in` | `src/components/toast.css` | Toast entrance animates a layout property and is longer/slower than the evidenced panel token; no Reduced Motion branch shown. | Move final position to static style; animate `transform` + `opacity` with token duration/easing; Reduced Motion uses short fade/static state. |
| P2 | Button has RM branch; other snippets do not show one | Multiple | Reduced Motion convention appears local, not evidenced across overlay, toast, palette, or drag settle motion. | Add component-scoped RM branches that remove large travel/elasticity but preserve opacity/color/focus/static feedback. |
| P3 | `360ms`, `420ms`, `500ms`, `400` alongside `160ms`/`240ms` tokens | Multiple | Motion vocabulary is drifting into one-off values that can make the console feel inconsistent. | Prefer existing semantic tokens; add a new semantic token only if repeated use cannot be represented by `fast`/`panel`. |

## 3. Implementation plans

### Plan A — Normalize popover and toast motion around tokenized transform/opacity

**Current excerpts**

- `src/styles/motion.css`
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

- `src/components/toast.css`
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

- Popovers respond immediately and feel anchored to their trigger unless the component is truly centered.
- Toasts enter as status feedback without layout-position animation.
- Motion uses existing `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Reduced Motion removes vertical travel and preserves feedback through opacity/static final state.

**Project conventions to preserve**

- Keep semantic CSS tokens.
- Keep localized `prefers-reduced-motion` behavior like the button precedent.
- Prefer `transform`/`opacity`; avoid `transition: all`.

**Ordered steps**

1. Inspect all `.popover` consumers before editing.
2. If `.popover` is used only for anchored overlays, change origin to a trigger-aware value, e.g. `var(--popover-origin, top center)`.
3. If `.popover` is also used for centered dialogs, split the centered case rather than forcing all popovers away from `center`.
4. Replace `transition: all 360ms ease-in` with explicit `opacity` and `transform` transitions using existing tokens.
5. In `toast.css`, move final placement such as `top: 0` into the base `.toast` rule if the component relies on it.
6. Replace toast keyframe `top` movement with `transform: translateY(...)` plus opacity.
7. Add `@media (prefers-reduced-motion: reduce)` branches for `.popover` and `.toast`.

**Hard boundaries**

- Do not change toast lifecycle, stacking, dismissal timing, or z-index behavior.
- Do not introduce a motion library.
- Do not globally alter the existing token values.
- Do not change centered overlay origins unless consumer inspection proves they are popovers, not dialogs.

**Mechanical checks**

- Run the project’s configured lint/type-check/build commands.
- Search for remaining `transition: all`, `500ms ease-in`, and `top` inside animation keyframes touching these files.
- Confirm CSS parses after any keyframe/media additions.

**Runtime/feel checks required later, not performed here**

- Trigger popovers from keyboard and pointer; confirm response starts immediately.
- Trigger stacked and repeated toasts; confirm no visible layout jump.
- Emulate Reduced Motion; confirm toast/popover still communicate state without vertical travel.
- Inspect computed animation properties to verify `top` is not animated.

**Reduced Motion behavior**

- Popover: no scale/travel, short opacity transition or immediate final state.
- Toast: no vertical translation; short opacity/status appearance, final position stable.

**Source-drift stop condition**

- Stop before editing if `.popover`, `.toast`, token names, or toast positioning no longer match the excerpts, or if `.popover` consumers mix anchored overlays and centered dialogs without a clear class split.

---

### Plan B — Retune command palette motion for high-frequency keyboard use

**Current excerpt**

- `src/components/CommandPalette.tsx`
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

- Opening/closing feels immediate and does not slow keyboard throughput.
- Motion is state-driven from `open`, not a long always-applied arbitrary keyframe.
- Entry/exit uses opacity and minimal vertical/scale change only if it improves spatial continuity.
- Reduced Motion removes travel while preserving open/closed feedback.

**Project conventions to preserve**

- Use existing duration/easing tokens.
- Keep the component API unchanged: `CommandPalette({ open })`.
- Preserve search results rendering and command behavior.
- Preserve visible focus requirements; do not hide focus with animation styles.

**Ordered steps**

1. Locate the `palette` keyframe definition, if any, before replacing the class.
2. Replace `animate-[palette_420ms_ease-in_both]` with state-based classes or a local CSS class keyed by `data-open`.
3. Use `--duration-fast` for very small feedback or `--duration-panel` only if the palette is panel-sized.
4. Use `--ease-responsive`; do not use `ease-in` for the first response.
5. For closed state, add only safe visual/pointer behavior that matches existing lifecycle conventions, e.g. opacity/transform and possibly `pointer-events: none`.
6. Add a Reduced Motion branch: duration around the button precedent’s reduced path and no translation/scale.
7. Remove the obsolete `palette` keyframe only if no other component uses it.

**Hard boundaries**

- Do not redesign the command palette.
- Do not add focus trapping or command routing changes in this motion-only pass unless existing tests require a small compatibility adjustment.
- Do not convert mount/unmount lifecycle without confirming how the palette is currently opened and closed.
- Do not add a dependency.

**Mechanical checks**

- Run configured lint/type-check/build.
- Search for other references to `palette` before deleting or renaming any keyframe.
- Verify no arbitrary `420ms ease-in` palette animation remains.

**Runtime/feel checks required later, not performed here**

- Open via keyboard shortcut repeatedly; response should begin immediately.
- Type during/after open; input should not be blocked by animation.
- Close via Escape and reopen quickly; no keyframe restart flash or stale closed visual.
- Emulate Reduced Motion; confirm no travel and preserved open/closed feedback.

**Reduced Motion behavior**

- No translate/scale.
- Short opacity transition or immediate state change.
- Focus ring remains visible and is not delayed.

**Source-drift stop condition**

- Stop if the component no longer uses the shown `className`, if `open` no longer controls visibility, if the palette keyframe is shared by unrelated surfaces, or if the project has a newer command-palette motion convention.

---

### Plan C — Repair sortable queue direct manipulation and settle continuity

**Current excerpt**

- `src/components/SortableQueue.tsx`
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

- Dragged item tracks 1:1 with the pointer after intent is established.
- No jump on grab, move, release, or interruption.
- Release animation starts from the current presentation value and inherits measured velocity.
- Existing target semantics stay `nearestSlot(currentY)` unless product authority explicitly approves momentum-based target selection.
- Reduced Motion removes elastic/throw effects but keeps direct manipulation and clear slot feedback.

**Project conventions to preserve**

- Keep current queue ordering rules and nearest-slot behavior by default.
- Keep React state for logical dragging state, not per-frame pointer position.
- Use transform-driven visual movement where existing CSS allows.
- Avoid synchronous layout work in the pointer-move hot path.

**Ordered steps**

1. Inspect queue markup/CSS to identify the actual transform owner for the dragged item.
2. If press feedback and drag both write `transform`, split into wrapper layers or compose transforms in one explicit owner.
3. On pointer down, capture pointer, record pointer id, container/item bounds, current presentation y, and grab offset.
4. Establish coordinate space in CSS pixels: `clientY - containerTop - grabOffsetY` or the project’s equivalent local coordinate.
5. Track a short movement history with monotonic timestamps; compute release velocity in CSS px/s.
6. On pointer move, update only the dragged visual transform/CSS variable, preferably batched to the display frame.
7. On pointer up/cancel, release pointer capture and compute current presentation y.
8. Choose target with existing `nearestSlot(currentY)` unless momentum target selection is separately authorized.
9. Pass measured release velocity into the settle animation API if supported; if the API lacks velocity support, replace only the settle primitive with a compatible spring/WAAPI approach after confirming dependency policy.
10. Add interruption handling so a new drag starts from the current on-screen value, not the last logical target.
11. Add Reduced Motion branch: no bounce/elastic overshoot, shortened settle, static slot highlight retained.

**Hard boundaries**

- Do not change persistence, queue data model, slot calculation semantics, or destructive reorder thresholds.
- Do not silently switch to projected-endpoint target selection.
- Do not lock pointer input until a settle completes.
- Do not add broad parent CSS-variable updates if the queue contains many descendants without measuring style recalculation.

**Mechanical checks**

- Run configured lint/type-check/build and any component tests around reorder behavior.
- Add or update unit tests for coordinate conversion, nearest-slot target preservation, and velocity calculation if the project has test infrastructure.
- Verify pointer-cancel path is handled, not only pointer-up.

**Runtime/feel checks required later, not performed here**

- Drag from different grab points; item should not snap under the pointer.
- Drag outside original bounds; pointer capture should preserve tracking.
- Release slowly and quickly; settle should begin from current position with no jump.
- Interrupt mid-settle with a new drag; no reset to previous logical target.
- Test Reduced Motion; no elastic throw, but drag and slot state remain understandable.
- If momentum targeting is proposed later, compare projected endpoint behavior separately from velocity handoff.

**Reduced Motion behavior**

- User-controlled drag remains 1:1.
- Release settle is short, non-bouncy, and may snap nearly immediately.
- Slot/focus/selection feedback remains visible through static highlight, opacity, or color.

**Source-drift stop condition**

- Stop if `animateTo` already supports a different velocity API, if `currentY` is no longer the release position, if CSS no longer uses `--drag-y`, or if product rules define non-nearest reorder targeting.

## 4. Recommended execution order

1. **Plan A first** to re-anchor the shared motion vocabulary and remove the clearest CSS risks.
2. **Plan B next** because command palette is high-frequency and keyboard-heavy.
3. **Plan C last** because direct manipulation requires the most runtime feel validation and may depend on animation API capabilities.

## Explicitly unverified states

- Actual `palette` keyframe definition and whether it is shared.
- Computed CSS for `.popover`, `.toast`, and queue transform ownership.
- Popover consumer types: anchored overlay vs centered dialog.
- Toast base positioning, stacking, lifecycle, and repeated-trigger behavior.
- `animateTo` implementation, interruption behavior, and velocity support.
- Pointer capture, grab offset, pointer-cancel, and multi-pointer handling outside the shown snippet.
- Runtime smoothness, frame pacing, layout/paint/composite cost, and behavior under representative load.
- Accessibility tree, focus management, keyboard trap behavior, and screen-reader timing.
- Reduced Motion behavior beyond the shown button precedent.


## Output C

## 1. Recon summary

- **Stack signals:** React/TSX components, plain CSS files, CSS custom properties, and utility-style arbitrary animation classes.
- **Where motion lives:**  
  - Global tokens: `src/styles/motion.css`  
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`  
  - Inline utility animation: `src/components/CommandPalette.tsx`  
  - Imperative drag animation: `src/components/SortableQueue.tsx`
- **Existing conventions:**  
  - Semantic duration/easing tokens exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
  - Local precedent exists for restrained transform motion and Reduced Motion handling in `Button.css`.
- **Product personality:** calm, task-oriented, desktop operations console; motion should clarify cause/effect and state continuity without decorative delay.
- **Frequency map:**  
  - Very high frequency: button press, command palette, queue drag/drop.  
  - Medium frequency: popovers.  
  - Intermittent but attention-sensitive: toast entry.
- **Evidence level:** static evidence only. No runtime behavior, computed styles, frame timing, accessibility tree, input latency, or user testing was verified.

---

## 2. Vetted priority table

| Priority | Finding | Evidence | Risk | Direction |
|---|---|---|---|---|
| P0 | Reduced Motion coverage is inconsistent | `Button.css` has a reduce path; popover, palette, toast, queue snippets do not show one | Users requesting reduced motion may still receive long entrance/snap motion | Define a shared reduced-motion contract and apply to all listed motion surfaces |
| P0 | Command palette motion appears too slow/eased for a high-frequency keyboard surface | `animate-[palette_420ms_ease-in_both]` | May make command invocation feel delayed; static evidence only, no latency measured | Use tokenized duration, responsive easing, shorter enter/exit, preserved state feedback |
| P1 | Popover uses broad transition and non-token motion | `.popover { transition: all 360ms ease-in; }` | `all` can accidentally animate layout/paint properties; 360ms ease-in may feel sluggish | Restrict to `opacity, transform`; use semantic tokens |
| P1 | Toast animates layout-affecting `top` for 500ms | `@keyframes toast-enter { from { top: -24px; ... } }` | Layout-position animation is more fragile than transform; duration is long for operational feedback | Convert to transform/opacity with shorter tokenized timing |
| P1 | Queue drop animation lacks visible Reduced Motion contract | `animateTo(nearestSlot(currentY), { duration: 400 });` | Drag/drop is high-frequency direct manipulation; 400ms snap may slow throughput | Shorten snap, use distance-aware cap, provide reduced-motion snap/near-instant settle |
| P2 | Motion definitions are split across tokens, CSS, arbitrary utility, and imperative code | Evidence spans global CSS, component CSS, TSX utility class, JS animation call | Harder to keep product motion coherent | Normalize named component states around shared tokens and local precedents |

---

## 3. Implementation plans

### Plan A — Establish a motion contract and Reduced Motion baseline

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

`src/components/Button.css`

```css
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

**Target behavior**

- All motion uses semantic duration/easing tokens unless there is a documented local reason.
- Reduced Motion does not remove all feedback; it shortens or simplifies motion while preserving state change.
- High-frequency controls favor fast transform/opacity transitions over decorative movement.

**Project conventions to preserve**

- Keep existing token names.
- Preserve the `Button.css` precedent: transform-based feedback plus shortened Reduced Motion duration.
- Do not introduce unrelated visual styling, gradients, shadows, or global resets.

**Ordered steps**

1. In `src/styles/motion.css`, add missing semantic tokens without deleting existing ones, for example:
   - `--duration-instant: 80ms`
   - `--duration-fast: 160ms`
   - `--duration-panel: 240ms`
   - optional `--duration-attention: 220ms`
   - keep `--ease-responsive`
   - add optional exit easing only if used consistently.
2. Add a global Reduced Motion token override:
   - keep feedback duration around `80ms`
   - avoid setting all durations to `0ms` unless a specific component needs no travel.
3. Replace component hard-coded durations/easings incrementally with tokens.
4. Prefer animating only `opacity` and `transform`.
5. Add a lightweight convention comment near tokens explaining:
   - command surfaces: fast
   - panels/popovers: panel duration
   - alerts/toasts: attention duration
   - direct manipulation settle: short and distance-aware.

**Hard boundaries**

- Do not change product layout, copy, component hierarchy, or data behavior.
- Do not globally disable transitions.
- Do not introduce new animation libraries based only on this evidence.
- Do not claim performance improvement until runtime measurement exists.

**Mechanical checks**

- Search for `transition: all`.
- Search for hard-coded `ms` in component CSS/TSX animation declarations.
- Search for `ease-in` on interactive surfaces.
- Confirm each edited animated component has a `prefers-reduced-motion: reduce` path or consumes a reduced token.

**Runtime/feel checks to perform later**

- Keyboard-open command palette repeatedly and confirm it feels immediate, not theatrical.
- Trigger popovers and toasts in normal and Reduced Motion modes.
- Confirm visible state feedback remains in Reduced Motion.
- Check that focus rings remain visible during and after animated state changes.

**Reduced Motion behavior**

- Use shortened transform/opacity transitions, generally around `80ms`.
- Avoid large spatial travel.
- Preserve opacity or subtle scale feedback so users still perceive state changes.

**Source-drift stop condition**

- Stop before implementation if `src/styles/motion.css` no longer owns global motion tokens, if `Button.css` has changed its Reduced Motion convention, or if a design authority file now defines different durations/easings.

---

### Plan B — Normalize command palette and popover motion

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
.popover {
  transform-origin: center;
  transition: all 360ms ease-in;
}
```

**Target behavior**

- Command palette opens quickly and causally from the user action.
- Popovers use restrained opacity/transform motion.
- Both surfaces use named CSS states instead of one-off arbitrary animation strings where practical.
- Motion is fast enough for keyboard-heavy repeated use.

**Project conventions to preserve**

- Use existing semantic tokens.
- Keep `data-open={open}` as a useful state hook.
- Preserve component API unless existing callers require otherwise.
- Follow local precedent of transform-based motion from `Button.css`.

**Ordered steps**

1. Replace the arbitrary command palette animation class with a stable class name, for example:
   - `className="commandPalette"`
   - keep `data-open={open}`.
2. Define command palette motion in an appropriate stylesheet already used by the component, or a component-local CSS file if one exists.
3. Suggested behavior:
   - closed: `opacity: 0; transform: translateY(-4px) scale(0.985); pointer-events: none;`
   - open: `opacity: 1; transform: translateY(0) scale(1); pointer-events: auto;`
   - transition: `opacity var(--duration-fast) var(--ease-responsive), transform var(--duration-fast) var(--ease-responsive)`.
4. If the component unmounts when closed elsewhere, coordinate with that lifecycle before relying on exit transitions.
5. Replace `.popover` transition with:
   - `transition-property: opacity, transform;`
   - `transition-duration: var(--duration-panel);`
   - `transition-timing-function: var(--ease-responsive);`
6. Ensure no layout-affecting properties are included in popover transition declarations.
7. Add Reduced Motion overrides for both:
   - shorter duration
   - no or minimal translation/scale.

**Hard boundaries**

- Do not alter search result rendering or filtering.
- Do not change focus management based only on the motion evidence.
- Do not assume the command palette currently has working exit animation; lifecycle is unverified.
- Do not remove `data-open` unless all styling/state consumers are checked.

**Mechanical checks**

- Confirm `animate-[palette_420ms_ease-in_both]` is gone or intentionally isolated.
- Confirm `.popover` no longer uses `transition: all`.
- Confirm no `420ms`, `360ms ease-in`, or broad `all` transition remains for these surfaces.
- Confirm Reduced Motion rules exist.

**Runtime/feel checks to perform later**

- Open command palette from keyboard repeatedly.
- Close it with the expected key/mouse path.
- Verify focus indication is visible before, during, and after the transition.
- Verify popover placement does not visually drift or animate from an unrelated origin.
- Verify Reduced Motion still communicates open/closed state without spatial travel.

**Reduced Motion behavior**

- Command palette: fade or near-instant opacity change around `80ms`; avoid scale/vertical travel.
- Popover: short opacity transition; avoid transform travel unless extremely small.

**Source-drift stop condition**

- Stop if `CommandPalette` now delegates animation to another component, portal, transition helper, or design-system primitive not shown in the excerpt.
- Stop if `.popover` is generated or owned by a third-party component stylesheet where direct edits would be overwritten.

---

### Plan C — Rework toast entry and queue drag settle for direct manipulation

**Current excerpts**

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

- Toasts enter as quick operational feedback, using transform/opacity rather than positional layout animation.
- Dragged queue items track the pointer directly while dragging and settle quickly into the nearest valid slot.
- Reduced Motion preserves feedback without long travel or delayed settle.

**Project conventions to preserve**

- Use semantic motion tokens.
- Prefer transform-based animation.
- Preserve existing queue data behavior and nearest-slot logic.
- Keep pointer interaction causality: pointer movement should map clearly to item movement.

**Ordered steps**

1. In `src/components/toast.css`, replace `top` keyframe animation with transform/opacity:
   - from: `transform: translateY(-8px); opacity: 0;`
   - to: `transform: translateY(0); opacity: 1;`
2. Reduce toast duration from `500ms ease-in` to a tokenized value:
   - likely `var(--duration-panel)` or a dedicated attention duration around `220ms`.
   - use `var(--ease-responsive)`.
3. Add Reduced Motion:
   - no vertical travel or minimal `translateY(-2px)`
   - duration around `80ms`.
4. In `SortableQueue.tsx`, keep pointer move direct, but ensure the visual consumer of `--drag-y` uses `transform`, not `top`; this is unverified from the snippet and must be checked before editing.
5. Replace fixed `duration: 400` with a shorter token-aligned value or named constant:
   - normal settle target: about `160–220ms`
   - cap duration for long distances if distance-aware duration is introduced.
6. Add Reduced Motion branch for pointer-up settle:
   - near-instant snap or very short settle around `80ms`
   - preserve final-slot feedback.
7. If `animateTo` accepts easing, use the shared responsive easing; if not, do not invent an API without checking its signature.

**Hard boundaries**

- Do not change queue sorting rules, slot calculation, or selected item state.
- Do not assume `clientY` is wrong from static evidence alone; coordinate handling needs runtime/layout context.
- Do not rewrite drag/drop architecture without validating existing constraints.
- Do not remove animation entirely for normal motion users.

**Mechanical checks**

- Confirm toast keyframes no longer animate `top`.
- Confirm `.toast` no longer uses `500ms ease-in`.
- Confirm Reduced Motion exists in `toast.css`.
- Confirm queue settle duration is not a hard-coded `400` without a named reason.
- Check `animateTo` API before adding easing or cancellation options.
- Check CSS consuming `--drag-y` before changing coordinate math.

**Runtime/feel checks to perform later**

- Trigger toasts repeatedly and verify they do not feel blocking.
- Drag queue items slowly and quickly; visual item should stay under the pointer as closely as the existing architecture allows.
- Release near and far from a slot; settle should feel causal, not delayed.
- Test cancellation/interruption if another drag starts before settle finishes.
- Test Reduced Motion for both toast and drag release.

**Reduced Motion behavior**

- Toast: short fade with no meaningful vertical travel.
- Queue: direct drag remains direct; release settles almost immediately to the target slot with clear final position.

**Source-drift stop condition**

- Stop if toast rendering has moved to a shared notification system.
- Stop if `SortableQueue` now uses a drag library, spring system, virtualization layer, or different `animateTo` contract not shown in the excerpt.

---

## 4. Recommended execution order

1. **Plan A first:** establish the shared motion and Reduced Motion contract.
2. **Plan B second:** fix high-frequency command palette and broad popover transition.
3. **Plan C third:** convert toast layout animation and tune queue settle behavior.

## Explicitly unverified states

- Actual computed styles and final CSS cascade.
- Whether command palette remains mounted while closed.
- Whether `palette` keyframes exist elsewhere.
- Whether `.popover` has open/closed state classes elsewhere.
- Whether toast positioning depends on `top` for layout.
- How `--drag-y` is consumed visually.
- `animateTo` API shape, easing support, cancellation behavior, and interruption behavior.
- Keyboard focus order, focus trapping, screen reader behavior, and accessibility tree.
- Runtime performance, frame timing, input latency, and perceived feel on real devices.
