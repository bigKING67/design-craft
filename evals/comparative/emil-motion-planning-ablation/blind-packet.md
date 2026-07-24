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

Motion diagnosis: the shown system has one good local precedent, but the active surface snippets drift toward slow `ease-in`, ad-hoc durations, keyframe restarts, layout-property motion, and under-specified Reduced Motion for high-frequency operator workflows.

- **Stack signals**: React/TSX components, CSS custom-property tokens, component CSS, Tailwind-style arbitrary animation class, imperative pointer/animation code via `animateTo(...)`.
- **Where motion lives**:
  - Global tokens and `.popover`: `src/styles/motion.css`
  - Command palette entry/visibility: `src/components/CommandPalette.tsx`
  - Toast keyframes: `src/components/toast.css`
  - Drag/reorder gesture: `src/components/SortableQueue.tsx`
  - Correct local precedent: `src/components/Button.css`
- **Existing conventions**:
  - Semantic tokens: `--duration-fast`, `--duration-panel`, `--ease-responsive`
  - Preferred property pattern: transform-only transition
  - Reduced Motion precedent: shorten to `80ms` while preserving feedback
- **Product personality**: calm, crisp, non-decorative desktop operations motion; motion should explain causality without taxing keyboard-heavy repeated use.
- **Frequency map**:
  - Very high: command palette, buttons, queue dragging/reordering
  - Medium/high: popovers in operational workflows
  - Occasional: toasts
- **Evidence level**: static snippets only. No runtime smoothness, frame pacing, computed styles, browser behavior, focus behavior, or accessibility-tree state was verified.

## 2. Vetted priority table

| Priority | Evidence | Finding | Smallest safe correction |
|---|---|---|---|
| P1 | `CommandPalette.tsx`: `animate-[palette_420ms_ease-in_both]` | High-frequency keyboard surface uses slow ad-hoc keyframe timing and `ease-in`, which delays perceived response by design. Reduced Motion path is not shown. | Replace with tokenized opacity/very small transform transition, `var(--duration-fast)`, `var(--ease-responsive)`, and an explicit Reduced Motion branch. |
| P1 | `SortableQueue.tsx`: pointer move writes `--drag-y`; release uses `animateTo(..., { duration: 400 })` | Direct manipulation lacks demonstrated pointer capture, grab offset, presentation-value interruption, measured release velocity, and velocity handoff. Static evidence cannot prove feel, but the release API shown is fixed-duration. | Preserve existing `nearestSlot(currentY)` target semantics, but measure release velocity in CSS px/s and feed it into an interruptible settle primitive if the API supports it. |
| P2 | `motion.css`: `.popover { transform-origin: center; transition: all 360ms ease-in; }` | Broad `transition: all`, non-token duration/easing, and center origin are risky for anchored overlays. Static evidence does not prove anchoring, so origin must be conditional. | Transition only intended properties; use tokens; preserve center fallback via `var(--popover-origin, center)`. |
| P2 | `toast.css`: `top` keyframe over `500ms ease-in` | Toast entry animates a layout-position property and uses slow `ease-in`; no Reduced Motion branch is shown. Static evidence indicates performance/accessibility risk, not measured jank. | Keep layout position static, animate `transform` + `opacity`, tokenize duration/easing, add Reduced Motion opacity-only/short branch. |
| P2 | Button has Reduced Motion precedent; other shown motion does not | Reduced Motion handling is inconsistent across meaningful motion surfaces in the snippets. | Add local `prefers-reduced-motion: reduce` branches that remove/reduce spatial travel while keeping opacity/static state feedback. |
| P3 | Multiple hard-coded values: `360ms`, `420ms`, `500ms`, `400`, `ease-in` | Motion vocabulary is fragmenting away from semantic tokens and the product’s crisp-motion authority. | Normalize to existing tokens first; introduce no new token unless repeated need remains after implementation. |

## 3. Implementation plans

### Plan A — Normalize popover and command-palette overlay motion

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

- Popovers and command palette respond immediately and calmly.
- Use existing `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Avoid `transition: all`.
- Command palette should use minimal travel because it is keyboard-heavy.
- Reduced Motion should preserve open/closed feedback without meaningful spatial movement.

**Project conventions**

- Follow the button precedent: transform-based motion, semantic tokens, `80ms` Reduced Motion.
- Do not introduce decorative bounce, large scale, or new easing tokens.

**Ordered steps**

1. In `src/styles/motion.css`, replace `.popover` with property-specific transitions:

   ```css
   .popover {
     transform-origin: var(--popover-origin, center);
     transition:
       transform var(--duration-panel) var(--ease-responsive),
       opacity var(--duration-fast) var(--ease-responsive);
   }
   ```

2. Add a command-palette motion class in the existing loaded motion stylesheet, only if that stylesheet is confirmed global/imported:

   ```css
   .commandPaletteMotion {
     opacity: 1;
     transform: translateY(0) scale(1);
     transition:
       opacity var(--duration-fast) var(--ease-responsive),
       transform var(--duration-fast) var(--ease-responsive);
   }

   .commandPaletteMotion[data-open="false"] {
     opacity: 0;
     transform: translateY(-4px) scale(0.99);
   }
   ```

3. In `src/components/CommandPalette.tsx`, replace the arbitrary animation class:

   ```tsx
   className="commandPaletteMotion"
   ```

4. Add Reduced Motion in `src/styles/motion.css`:

   ```css
   @media (prefers-reduced-motion: reduce) {
     .popover,
     .commandPaletteMotion {
       transition-duration: 80ms;
     }

     .commandPaletteMotion,
     .commandPaletteMotion[data-open="false"] {
       transform: none;
     }
   }
   ```

**Hard boundaries**

- Do not change `SearchResults`.
- Do not change command filtering, focus management, keyboard shortcuts, or open/close state semantics.
- Do not invent new duration/easing tokens for this pass.
- Do not force popover origin away from `center` unless the component provides trigger-relative origin data.

**Mechanical checks**

- Run the project’s type check and lint commands if available, e.g. `npm run typecheck` and `npm run lint`.
- Search for remaining `animate-[palette_420ms_ease-in_both]` references.
- Search for `.popover` overrides that depend on `transition: all`.

**Runtime/feel checks to perform later**

- Open/close the command palette repeatedly via keyboard.
- Interrupt open/close rapidly.
- Verify the palette feels immediate and does not visually lag input.
- Verify popover opacity/transform still transition where expected.
- No browser/device validation was performed for this audit.

**Reduced Motion behavior**

- Palette: no translate/scale travel; opacity/state feedback remains over `80ms`.
- Popover: shortened transition; no additional travel introduced by this plan.

**Source-drift stop condition**

Stop before editing if `CommandPalette` no longer uses `data-open`, if the palette animation class has already been replaced, if `src/styles/motion.css` is not loaded globally, or if `.popover` has component-specific transition/property ownership elsewhere.

---

### Plan B — Convert toast entry from layout motion to tokenized transform feedback

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

- Toast appears promptly without animating `top`.
- Motion explains arrival but does not feel cinematic.
- Layout position remains stable; visual entrance uses `transform` and `opacity`.
- Reduced Motion uses opacity/static state feedback only.

**Project conventions**

- Use existing `--duration-panel` or `--duration-fast`; start with `--duration-panel` because toasts are occasional but should still be crisp.
- Use `--ease-responsive`.
- Match the button precedent for Reduced Motion duration: `80ms`.

**Ordered steps**

1. Replace keyframes in `src/components/toast.css`:

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

2. Ensure the resting layout position is owned outside the animation:

   ```css
   .toast {
     top: 0;
     animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;
   }
   ```

3. Add Reduced Motion:

   ```css
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

**Hard boundaries**

- Do not change toast content, dismissal timing, queueing, stacking, or ARIA/live-region behavior in this motion pass.
- Do not add `will-change` unless later measurement shows a benefit.
- Do not change positioning strategy beyond keeping the final `top: 0` state stable.

**Mechanical checks**

- Run CSS lint if available.
- Search for code that expects `toast-enter` to animate `top`.
- Confirm no duplicate `@keyframes toast-enter` definitions conflict.

**Runtime/feel checks to perform later**

- Trigger single and multiple toasts.
- Verify stacking still appears in the correct position.
- Verify no visual jump at animation end.
- Verify rapid toast creation does not restart unrelated existing toasts unexpectedly.
- No runtime behavior was observed during this audit.

**Reduced Motion behavior**

- Remove vertical travel.
- Preserve a short opacity fade so users still receive arrival feedback.
- Keep final layout and visibility unchanged.

**Source-drift stop condition**

Stop before editing if toast positioning/stacking has moved to another file, if `.toast` already has transform ownership for another purpose, or if `top` animation is intentionally part of a documented stacking algorithm.

---

### Plan C — Harden SortableQueue drag settle and interruption semantics

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

- Dragged item remains attached to the pointer without jumps.
- Release settle starts from the current presentation value.
- Existing target selection, `nearestSlot(currentY)`, is preserved unless product authority explicitly approves momentum-based target changes.
- Release velocity is measured in CSS px/s and handed into the settle animation where the animation API supports it.
- Reduced Motion removes elastic/large travel while preserving clear reorder state feedback.

**Project conventions**

- Prefer transform-driven movement.
- Keep high-frequency operator motion crisp and non-bouncy.
- Do not replace product semantics with physics semantics without explicit approval.

**Ordered steps**

1. Inspect the existing pointer-down path before editing. It must identify dragged item, pointer id, start Y, current presentation Y, and grab offset. If missing, add those before changing release behavior.
2. On pointer down after drag intent is confirmed:
   - call pointer capture on the active element if supported;
   - store `pointerId`;
   - store grab offset and starting presentation position;
   - initialize a short sample buffer using CSS pixels and monotonic timestamps.
3. On pointer move:
   - ignore events from non-active pointers;
   - compute movement relative to the stored start/grab offset, not raw `event.clientY` alone;
   - update the transform owner for the dragged item, not a broad parent variable, unless current CSS proves the parent variable is intentionally scoped;
   - keep hot-path work to style update/sample append only.
4. On pointer up/cancel:
   - release pointer capture;
   - compute release velocity from recent samples in CSS px/s;
   - set `dragging` false only after the visual owner can continue from the current presentation value;
   - choose target with existing `nearestSlot(currentY)` semantics;
   - call the animation primitive with current position and initial velocity.
5. If `animateTo` accepts only `{ duration: 400 }` and cannot accept current value/velocity, stop and introduce an adapter or supported primitive in a separate reviewed change rather than faking velocity handoff.
6. Optional, separately authorized only: compute a bounded projected endpoint for target selection, then choose the nearest slot to that endpoint. Do not make this the default plan.

**Hard boundaries**

- Do not change queue ordering rules, slot calculation semantics, persistence, selection, or keyboard reorder behavior.
- Do not add bounce by default.
- Do not add dependencies unless existing animation utilities cannot support presentation-value interruption and velocity handoff.
- Do not use global document listeners as a substitute for pointer capture unless compatibility requires a documented fallback.

**Mechanical checks**

- Run type check and lint, e.g. `npm run typecheck` and `npm run lint`, if those scripts exist.
- Add or update unit tests for `nearestSlot` preservation if slot logic is testable.
- Add pure tests for release-velocity calculation if extracted.

**Runtime/feel checks to perform later**

- Drag slowly, drag quickly, release near slot boundaries.
- Interrupt a settle by grabbing the item mid-animation.
- Move pointer outside the original item bounds while dragging.
- Cancel pointer interaction and verify state recovers.
- Verify no visual jump on pointer down, move, release, or interruption.
- Performance check under a populated queue should confirm no avoidable broad style recalculation; this was not measured here.

**Reduced Motion behavior**

- Keep direct tracking while dragging, because it is functional feedback.
- On release, use immediate or very short non-elastic settle, around the established `80ms` Reduced Motion precedent.
- Remove projection/overshoot/elastic effects.
- Preserve visible selected/dragging/drop-target state through static styling or opacity/color feedback.

**Source-drift stop condition**

Stop before editing if the pointer-down code already implements capture/grab offset/velocity, if `--drag-y` is consumed by CSS in a way that cannot be moved to the dragged item safely, if `animateTo` already wraps a spring with velocity support, or if target selection is documented as momentum-based rather than nearest-slot.

## 4. Recommended execution order

1. **Plan C first** if queue reordering is central to operator throughput; direct manipulation has the highest feel and correctness risk.
2. **Plan A second** to remove the most visible high-frequency token drift from keyboard and overlay workflows.
3. **Plan B third** as a bounded, low-risk cleanup for transient feedback.

Explicitly unverified states:

- Actual `palette` keyframes and whether they animate transform, opacity, or layout.
- Whether `src/styles/motion.css` is globally loaded.
- Popover anchoring, placement, and whether `center` is intentional for modal-like cases.
- Toast positioning, stacking, live-region behavior, and dismissal lifecycle.
- `animateTo` API capabilities.
- Existing pointer-down/cancel logic in `SortableQueue`.
- Computed styles, focus behavior, Reduced Motion behavior, frame pacing, and perceived smoothness.


## Output B

## 1. Recon summary

**Stack signals**
- React/TSX components with CSS modules/files and global motion tokens.
- CSS custom properties already exist for motion semantics:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Utility-style arbitrary animation appears in `CommandPalette.tsx`.
- Motion currently lives in a mix of global CSS, component CSS, inline style mutation, and component class strings.

**Where motion lives**
- `src/styles/motion.css`: global tokens plus `.popover`.
- `src/components/CommandPalette.tsx`: hard-coded animation utility.
- `src/components/toast.css`: local keyframes and animation.
- `src/components/SortableQueue.tsx`: pointer-driven CSS variable updates and imperative snap animation.
- `src/components/Button.css`: strongest local precedent for tokenized, transform-only, reduced-motion-aware interaction.

**Existing conventions**
- Preferred: semantic duration/easing tokens, transform-based movement, visible interaction feedback, and reduced-motion duration shortening.
- Confirmed good precedent:
  - `transition: transform var(--duration-fast) var(--ease-responsive);`
  - reduced motion keeps feedback but shortens duration to `80ms`.

**Product personality**
- Calm, crisp, desktop operations UI.
- Motion should explain causality and state continuity without adding delay.
- Keyboard-heavy users need quick state changes, predictable focus, and no theatrical animation.

**Frequency map**
- Very frequent: buttons, pointer drag in sortable queue, command palette.
- Frequent/contextual: popovers.
- Background/episodic: toast entrance.
- Highest risk areas are high-frequency or task-blocking motion: command palette and sortable queue.

**Evidence level**
- Static snippet audit only.
- No runtime validation, computed styles, accessibility tree, trace, device testing, or user testing was performed.
- Findings below are limited to what is directly supported by the excerpts.

---

## 2. Priority table

| Priority | Area | Finding | Evidence | Risk | Recommended direction |
|---:|---|---|---|---|---|
| P0 | Reduced Motion coverage | Reduced Motion is present only in the button precedent; other shown motion paths have no reduced-motion branch. | `.button` has media query; `.popover`, palette, toast, queue snippets do not. | Users requesting reduced motion may still receive long or spatial motion. | Apply reduced-motion behavior to every motion path while preserving feedback. |
| P0 | Command palette | Uses hard-coded `420ms ease-in` animation in component class. | `className="animate-[palette_420ms_ease-in_both]"` | Palette is likely high-frequency and task-blocking; hard-coded slow ease-in conflicts with crisp operations feel. | Move to semantic class/tokens, shorter panel duration, state-specific enter/exit. |
| P1 | Popover | Uses `transition: all 360ms ease-in`. | `.popover { transition: all 360ms ease-in; }` | `all` can unintentionally animate layout/color/etc.; 360ms ease-in feels delayed for operational UI. | Restrict to `opacity, transform`; use existing duration/easing tokens. |
| P1 | Toast | Animates `top` for 500ms with `ease-in`. | `@keyframes toast-enter { from { top: -24px; ... } }` | Layout-position animation and long duration are poor fit for lightweight feedback. | Use `transform: translateY(...)` + opacity; reduce duration. |
| P1 | Sortable queue | Pointer move writes CSS var directly; snap uses hard-coded 400ms. | `setProperty("--drag-y", ...)`; `animateTo(..., { duration: 400 })` | Drag feedback and snap duration may feel detached from direct manipulation. | Use transform-driven movement, frame-bounded updates, tokenized snap, reduced-motion snap. |
| P2 | Motion consistency | Durations/easings are fragmented across CSS and TSX. | `160ms`, `240ms`, `360ms`, `400`, `420ms`, `500ms`; mixed `ease-in`. | Inconsistent feel across repeated workflows. | Centralize semantic motion choices and remove arbitrary one-off timings. |

---

## 3. Implementation plans

### Plan A — Normalize overlay/disclosure motion: popover + command palette

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
- Popovers and command palette should feel immediate, explain open/close causality, and avoid sluggish task blocking.
- Use opacity + transform only.
- Use semantic tokens instead of hard-coded `360ms`, `420ms`, and `ease-in`.
- Preserve visible state feedback under Reduced Motion with a short duration, not instant disappearance unless required.

**Project conventions to follow**
- Reuse `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Follow the button precedent: transform-based motion and `80ms` reduced-motion duration.
- Avoid `transition: all`.
- Avoid arbitrary animation strings for core repeated UI.

**Ordered steps**
1. In `src/styles/motion.css`, replace `.popover` transition with explicit properties:
   - `opacity var(--duration-fast) var(--ease-responsive)`
   - `transform var(--duration-fast) var(--ease-responsive)`
2. Keep `transform-origin: center` only if the visual treatment still needs centered scale; otherwise choose an origin that matches trigger geometry.
3. Add state selectors for `.popover[data-open="true"]` and `.popover[data-open="false"]`, or align with the existing state API if already present outside the snippet.
4. Use a small transform delta:
   - closed: slight translate/scale plus `opacity: 0`
   - open: `transform: translateY(0) scale(1); opacity: 1`
5. Replace the command palette arbitrary animation class with a named class, for example `className="commandPaletteMotion"`, while preserving `data-open={open}`.
6. Define command palette motion in the appropriate component CSS or shared motion CSS:
   - open: opacity to `1`, transform to settled state.
   - closed: opacity to `0`, transform to a small offset/scale.
   - duration: `var(--duration-panel)` for panel-scale movement.
   - easing: `var(--ease-responsive)`.
7. Add Reduced Motion branch:
   - keep opacity/state feedback.
   - reduce duration to `80ms`.
   - remove or nearly eliminate spatial travel/scale.

**Hard boundaries**
- Do not change command search behavior, result rendering, focus management, or keyboard shortcuts in this motion pass.
- Do not introduce new timing constants unless a new semantic token is explicitly approved.
- Do not animate layout properties, dimensions, or `all`.
- Do not remove `data-open`; it is useful for state styling and testing.

**Mechanical checks**
- Search for remaining `transition: all` in touched motion files.
- Search for `animate-[palette_420ms_ease-in_both]` and confirm it is removed.
- Confirm no new hard-coded overlay durations like `360ms`, `400ms`, `420ms`, or `500ms` are introduced.
- Run the closest static checks available for TSX/CSS formatting and type safety.

**Runtime/feel checks to perform later**
- Open and close command palette repeatedly by keyboard.
- Confirm it feels responsive rather than delayed.
- Confirm close motion does not trap attention.
- Confirm popover origin visually relates to its trigger.
- Confirm focus indicator remains visible before, during, and after the motion.

**Reduced Motion behavior**
- Duration: `80ms`.
- Prefer opacity-only or minimal transform.
- Feedback remains visible; state change should not become ambiguous.

**Source-drift stop condition**
- Stop before implementation if `CommandPalette` already uses another animation/state library outside the excerpt, or if `.popover` is generated/owned by a third-party component contract not shown here.

---

### Plan B — Convert toast entrance to compositor-safe feedback

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
- Toasts should appear as lightweight confirmation, not a slow event.
- Entrance should be short, calm, and compositor-friendly.
- Movement should preserve causality from the top area without animating `top`.

**Project conventions to follow**
- Use existing semantic tokens.
- Prefer transform + opacity.
- Use `var(--ease-responsive)`.
- Keep Reduced Motion feedback with shorter duration.

**Ordered steps**
1. Replace keyframes that animate `top` with keyframes that animate `transform`.
2. Suggested shape:
   - from: `transform: translateY(-8px); opacity: 0;`
   - to: `transform: translateY(0); opacity: 1;`
3. Replace `500ms ease-in` with a semantic duration:
   - likely `var(--duration-fast)` for transient feedback.
4. Replace `ease-in` with `var(--ease-responsive)`.
5. Add `@media (prefers-reduced-motion: reduce)`:
   - animation duration `80ms`.
   - reduce translation to `0` or a very small offset.
6. Ensure the toast’s final positioning is set by normal layout/static styles, not by the animation’s final `top`.

**Hard boundaries**
- Do not change toast queueing, dismissal timing, message content, severity styling, or live-region behavior in this pass.
- Do not rely on `forwards` to establish required layout position.
- Do not animate `top`, `left`, `right`, `bottom`, width, height, or margins.

**Mechanical checks**
- Confirm `toast-enter` no longer contains `top`.
- Confirm `.toast` no longer uses `500ms ease-in`.
- Confirm final position is represented outside the keyframe if positioning is required.
- Confirm Reduced Motion branch exists in `src/components/toast.css`.

**Runtime/feel checks to perform later**
- Trigger success, warning, and error toasts if those variants exist.
- Confirm the toast feels informative, not attention-grabbing.
- Confirm multiple toasts do not create excessive motion.
- Confirm reduced-motion mode still communicates arrival.

**Reduced Motion behavior**
- Use `80ms`.
- Prefer opacity-only.
- If movement remains, keep it very small and non-essential.

**Source-drift stop condition**
- Stop if toast positioning depends on the `top` animation to reach its final layout state; first separate static positioning from entrance animation.

---

### Plan C — Make sortable queue drag and snap feel directly manipulated

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
- Dragged item should track pointer movement directly.
- Reorder snap should be quick and causal, not a separate slow animation.
- Timing should use semantic project motion values.
- Reduced Motion should preserve the snap/placement feedback while minimizing travel animation.

**Project conventions to follow**
- Use transform-driven movement via CSS variable.
- Tokenize duration and easing.
- Follow the local precedent of shortened `80ms` Reduced Motion.
- Keep high-frequency pointer work lightweight.

**Ordered steps**
1. Confirm `--drag-y` is consumed by `transform`, not by `top` or layout-position properties. If not, move the visual displacement to `transform: translateY(...)`.
2. Change the CSS variable meaning if needed from absolute viewport `clientY` to a local delta, for example `--drag-y: ${deltaY}px`, so the transform maps to item movement rather than page position.
3. Bound pointer updates to animation frames:
   - store latest pointer value.
   - schedule one visual write per frame.
   - avoid multiple style writes in the same frame.
4. Replace `animateTo(nearestSlot(currentY), { duration: 400 })` with a token-aligned duration:
   - likely `var(--duration-panel)` or a JS constant mapped to the same `240ms` value.
5. Use the shared easing equivalent of `--ease-responsive` for the snap animation if the animation API accepts easing.
6. Add a Reduced Motion path:
   - snap duration `80ms`.
   - no overshoot/bounce.
   - still clearly lands in the nearest slot.
7. Ensure `setDragging(false)` does not remove the visual dragged state before the snap target is applied, unless the animation system already handles handoff.

**Hard boundaries**
- Do not redesign sorting rules, hit testing, item identity, persistence, or keyboard reordering in this pass.
- Do not add physics/bounce unless explicitly approved; this product needs calm causality.
- Do not block pointer handling with expensive layout reads inside `onPointerMove`.
- Do not claim performance improvement until measured later.

**Mechanical checks**
- Confirm no hard-coded `duration: 400` remains in this component.
- Confirm the drag visual path uses transform-based CSS.
- Confirm pointer move does not perform repeated layout reads/writes beyond the intended CSS variable update.
- Confirm Reduced Motion can be determined by the same mechanism used elsewhere in the app or by a local media-query-backed utility.

**Runtime/feel checks to perform later**
- Drag slowly, quickly, and across multiple slots.
- Release near slot boundaries and confirm the snap target feels predictable.
- Confirm dragged item does not lag behind the pointer in ordinary use.
- Confirm reduced-motion mode lands clearly without unnecessary spatial travel.
- Confirm keyboard users have an equivalent clear reorder state if keyboard sorting exists.

**Reduced Motion behavior**
- Direct manipulation during active drag can remain because it is user-controlled.
- Programmatic snap should shorten to `80ms`.
- Avoid bounce, overshoot, or decorative easing.

**Source-drift stop condition**
- Stop if `animateTo` comes from an animation system with its own token integration, cancellation behavior, or reduced-motion handling not visible in the snippet; inspect that contract before changing durations.

---

## 4. Recommended execution order

1. **Plan A first**: fixes the most visible consistency issues and removes hard-coded task-blocking overlay motion.
2. **Plan B second**: small, contained conversion from layout-position animation to transform animation.
3. **Plan C third**: highest interaction complexity; should be implemented after token/easing conventions are settled.

## Explicitly unverified states

- Actual rendered timing, easing feel, and computed styles.
- Whether `palette` keyframes exist elsewhere and what they animate.
- Whether `.popover` is attached to a specific component library or generated markup.
- Whether toast has live-region semantics, dismissal timing, stacking behavior, or severity variants.
- Whether `--drag-y` currently drives `transform` or layout properties.
- Whether `animateTo` already handles cancellation, easing, Reduced Motion, or token mapping.
- Actual performance, frame rate, input latency, focus behavior, and accessibility-tree output.


## Output C

## 1) Recon summary

- **Stack signals:** React/TSX components plus CSS; motion is expressed through CSS tokens, component CSS, utility-style animation classes, and imperative JS gesture code. No motion library is evidenced.
- **Where motion lives:**  
  - Global tokens: `src/styles/motion.css`  
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`  
  - Inline utility animation: `src/components/CommandPalette.tsx`  
  - Gesture handler / imperative animation: `src/components/SortableQueue.tsx`
- **Existing conventions:** Semantic tokens already exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`. `Button.css` is the strongest local precedent: transform-only feedback, tokenized duration/easing, and `prefers-reduced-motion` shortening to `80ms`.
- **Product personality:** Calm, crisp, task-throughput-oriented desktop operations UI. Motion should clarify causality and feedback, not add delay or ornament.
- **Frequency map:**  
  - Very high: command palette, buttons, keyboard-triggered actions.  
  - High/bursty: sortable queue dragging.  
  - Medium: popovers.  
  - Occasional: toasts.
- **Evidence level:** Static snippets only. No runtime lifecycle, computed styles, screen recording, trace, accessibility tree, device, or browser validation was performed.

## 2) Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose / frequency / easing | `src/components/CommandPalette.tsx` | Command palette declares `animate-[palette_420ms_ease-in_both]`. For a keyboard-heavy, high-frequency surface, this is both slow and delayed by `ease-in`; it also bypasses existing motion tokens. | Remove command-palette entrance motion or reduce to effectively immediate non-spatial feedback; do not animate keyboard throughput paths. |
| 2 | HIGH | Performance / easing / cohesion | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in;`. `all` can animate unintended properties, `360ms` exceeds the stated crisp UI budget, and `ease-in` delays response. | Restrict to `transform, opacity`; use existing semantic duration/easing tokens; add reduced-motion handling. |
| 3 | HIGH | Performance / accessibility | `src/components/toast.css` | Toast entrance animates `top` for `500ms ease-in`. `top` is layout-affecting, `500ms` is slow for operational feedback, and no reduced-motion path is shown. | Animate `transform` + `opacity` instead; shorten to tokenized panel duration; reduce motion to opacity-only `80ms`. |
| 4 | HIGH | Gesture / interruptibility / performance | `src/components/SortableQueue.tsx` | Drag updates write `--drag-y` on `queueRef`; release uses fixed `duration: 400`. Static evidence does not show direct element transforms, velocity preservation, or reduced-motion branching. | During drag, update the dragged element’s transform directly; on release, use a shorter token-aligned settle or existing spring-capable helper; branch for reduced motion. |
| 5 | MEDIUM | Cohesion / tokens | Multiple snippets | Hardcoded `360ms`, `420ms`, `500ms`, `400`, `ease-in`, and utility animation syntax diverge from the existing semantic token precedent. | Consolidate motion values around existing `--duration-fast`, `--duration-panel`, and `--ease-responsive`; avoid parallel one-off timings. |

## 3) Implementation-ready plans

### Plan 1 — Tokenize and de-layout popover/toast motion

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

- Popovers and toasts should feel immediate, crisp, and operational.
- No `transition: all`.
- No animated `top`.
- Use existing semantic tokens:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Reduced Motion keeps feedback but removes spatial travel where possible.

**Project conventions**

Use `src/components/Button.css` as the local precedent:

```css
.button {
  transition: transform var(--duration-fast) var(--ease-responsive);
}

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
    transform var(--duration-panel) var(--ease-responsive),
    opacity var(--duration-panel) var(--ease-responsive);
}
```

2. In the same file, add Reduced Motion handling:

```css
@media (prefers-reduced-motion: reduce) {
  .popover {
    transition-duration: 80ms;
  }
}
```

3. In `src/components/toast.css`, replace the layout-moving keyframes:

```css
@keyframes toast-enter {
  from { transform: translateY(-24px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.toast {
  animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;
}
```

4. Add an opacity-only reduced-motion keyframe:

```css
@keyframes toast-enter-reduced {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (prefers-reduced-motion: reduce) {
  .toast {
    animation-name: toast-enter-reduced;
    animation-duration: 80ms;
    animation-timing-function: var(--ease-responsive);
  }
}
```

**Hard boundaries**

- Do not change toast markup, queue behavior, command palette behavior, or button styles.
- Do not add new dependencies.
- Do not introduce new duration/easing tokens unless the existing files already require token expansion.
- Do not change `transform-origin: center` unless the actual popover implementation exposes trigger-origin data; if so, use the existing local origin variable only.

**Mechanical checks**

- Search for remaining bad patterns in these files:
  - `transition: all`
  - `500ms ease-in`
  - `360ms ease-in`
  - `from { top:`
- Run the existing project lint/typecheck/build commands if present; do not add scripts.

**Runtime / feel checks for executor**

- Trigger a toast and confirm it enters via vertical transform + opacity, not by reflowing from `top`.
- Trigger a popover and confirm it feels responsive, not delayed at the start.
- At slow animation playback, confirm no unrelated properties animate on `.popover`.
- Toggle Reduced Motion and confirm toast movement is removed while opacity feedback remains.

**Reduced Motion behavior**

- Popover transition duration becomes `80ms`.
- Toast uses opacity-only `80ms`; no `translateY`.

**Source-drift stop condition**

Stop if either current excerpt is no longer present or if toast/popover state styles depend on `top` as a positioning contract rather than only as an entrance animation.

---

### Plan 2 — Remove high-frequency command palette entrance animation

**File / current excerpt**

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

- Opening/closing the command palette should not impose a `420ms` animated delay on a keyboard-heavy workflow.
- Preserve state continuity through immediate visibility, focus, selection highlight, and content stability rather than spatial entrance motion.
- No `ease-in` animation on this high-frequency path.

**Project conventions**

- For frequent feedback, prefer the local button precedent: short, transform-only, tokenized motion.
- For command palette specifically, target no entrance motion rather than merely a nicer curve.

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

2. Search for the `palette` keyframes or utility reference:
   - `animate-[palette_420ms_ease-in_both]`
   - `@keyframes palette`
   - `palette_420ms`
3. If the palette keyframe is used only by `CommandPalette`, remove the unused keyframe definition.
4. If the keyframe is shared elsewhere, do not remove it; only remove this command-palette usage.

**Hard boundaries**

- Do not change `SearchResults`.
- Do not change keyboard handling, focus management, search behavior, or open-state semantics.
- Do not replace the removed animation with another entrance animation.
- Do not add a motion library or new CSS token.

**Mechanical checks**

- Confirm no remaining `animate-[palette_420ms_ease-in_both]`.
- Confirm `CommandPalette` still renders `data-open={open}`.
- Run existing typecheck/lint commands if available.

**Runtime / feel checks for executor**

- Open the command palette repeatedly from the keyboard.
- Confirm it appears immediately and does not feel like it waits before becoming usable.
- Confirm focus indication and result selection remain visible.
- Toggle Reduced Motion and confirm behavior is equivalent, not broken or hidden.

**Reduced Motion behavior**

- Same as default: no entrance motion. Feedback should come from visible focus/selection/state, not movement.

**Source-drift stop condition**

Stop if `CommandPalette` no longer contains the exact arbitrary animation class or if the component’s visibility depends on that class for correctness rather than decoration.

---

### Plan 3 — Make sortable drag direct and shorten release settling

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

- Dragging should track the pointer directly with no parent-wide style-variable churn.
- Release should settle crisply and remain interruptible-feeling.
- Avoid a fixed `400ms` settle for an operational queue.
- Reduced Motion should shorten or eliminate the animated settle while preserving the final position update.

**Project conventions**

- Match the existing token values:
  - Fast feedback: `160ms`
  - Panel-scale movement: `240ms`
  - Responsive curve: `cubic-bezier(0.23, 1, 0.32, 1)`
- Do not add dependencies.

**Ordered steps**

1. Inspect this component for the dragged item element/ref and for where `--drag-y` is consumed.
2. If a dragged item element/ref exists, update that element directly during pointer move:

```tsx
function onPointerMove(event: PointerEvent) {
  draggedItemRef.current?.style.setProperty(
    "transform",
    `translate3d(0, ${event.clientY}px, 0)`
  );
}
```

3. If the component currently needs a delta rather than absolute viewport `clientY`, use the existing drag-start/current-position variables to write the same final transform as `translate3d(0, ${deltaY}px, 0)`.
4. Replace the fixed release duration with a token-aligned duration:

```tsx
function onPointerUp() {
  setDragging(false);
  animateTo(nearestSlot(currentY), {
    duration: prefersReducedMotion ? 80 : 240,
    easing: "cubic-bezier(0.23, 1, 0.32, 1)",
  });
}
```

5. If the existing `animateTo` helper already supports spring-style settling and velocity input, prefer that existing API instead of the duration/easing object:

```tsx
animateTo(nearestSlot(currentY), {
  type: "spring",
  duration: 0.5,
  bounce: 0.2,
  velocity: currentVelocity,
});
```

6. If `prefersReducedMotion` is not already available in this component, derive it without a new dependency using `window.matchMedia("(prefers-reduced-motion: reduce)")`, guarded for environments where `window` is unavailable.

**Hard boundaries**

- Do not rewrite the sorting algorithm.
- Do not change `nearestSlot(currentY)` behavior.
- Do not add a drag-and-drop library.
- Do not drive transforms through a parent CSS variable if a direct dragged element ref exists.
- If no dragged item ref exists and adding one would require restructuring the component tree, stop and report instead of improvising.

**Mechanical checks**

- Confirm no remaining parent write of `queueRef.current?.style.setProperty("--drag-y", ...)` for active drag motion.
- Confirm no remaining `{ duration: 400 }` release settle in `SortableQueue`.
- Confirm TypeScript accepts the `animateTo` options actually supported by the local helper.
- Run existing typecheck/lint commands if available.

**Runtime / feel checks for executor**

- Drag an item slowly and quickly; confirm the item remains visually attached to the pointer.
- Release near a slot and confirm the settle is crisp, not leisurely.
- Interrupt by starting another drag soon after release; confirm the UI does not visibly restart from an unrelated position.
- Toggle Reduced Motion and confirm the item still reaches the correct slot with minimal movement.

**Reduced Motion behavior**

- During direct dragging, pointer tracking remains direct because it is user-controlled.
- On release, settle duration becomes `80ms` or immediate if the local animation helper cannot produce a short non-spatial settle safely.

**Source-drift stop condition**

Stop if `animateTo` does not accept duration/easing or spring options, if `--drag-y` is part of layout calculations rather than only visual translation, or if the dragged element cannot be identified without restructuring.

## 4) Recommended execution order

1. **Plan 1:** Fixes shared CSS motion problems and creates the clearest local pattern for crisp, tokenized, reduced-motion-safe behavior.
2. **Plan 2:** Removes the highest-frequency delay from the keyboard-heavy command path.
3. **Plan 3:** Improves the most interaction-sensitive gesture path; execute after inspecting the actual `animateTo` API and drag DOM structure.

## Explicitly unverified states

- Actual component mount/unmount lifecycle.
- Whether `.popover` is always trigger-anchored or sometimes modal-like.
- Whether `palette` keyframes exist elsewhere.
- How `--drag-y` is consumed.
- `animateTo` API shape and whether it supports easing, spring, or velocity.
- Computed styles, frame rate, layout cost, focus behavior, accessibility tree, and Reduced Motion behavior at runtime.
- Any browser, device, trace, screen-recording, or user-test result.
