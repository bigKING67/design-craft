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

## 1. Recon summary

- **Stack signals**: React/TSX components, plain CSS, CSS custom-property motion tokens, Tailwind-style arbitrary animation class, and a bespoke `animateTo(...)` gesture settle helper. No motion library is evidenced.
- **Where motion lives**:
  - Global tokens/selectors: `src/styles/motion.css`
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`
  - Inline utility class: `src/components/CommandPalette.tsx`
  - Pointer-driven JS: `src/components/SortableQueue.tsx`
- **Existing conventions**:
  - Semantic durations: `--duration-fast: 160ms`, `--duration-panel: 240ms`
  - Responsive curve: `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
  - Correct local precedent: button press uses transform-only feedback, tokenized timing, and a Reduced Motion override.
- **Product personality**: calm, crisp desktop operations console. Motion should be causal and nearly invisible, not decorative or throughput-reducing.
- **Frequency map**:
  - Very high: `CommandPalette`, keyboard-driven workflow surfaces.
  - High during interaction: `SortableQueue` pointer movement/settle.
  - Medium/high: popovers in an operations console.
  - Occasional: toasts.
  - Existing good precedent: buttons.
- **Evidence level**: static snippets only. No runtime, computed-style, trace, screen recording, accessibility-tree, device, browser, or user validation was performed. Line numbers are unavailable from the supplied evidence.

## 2. Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose/frequency, easing | `src/components/CommandPalette.tsx` | High-frequency keyboard UI uses `animate-[palette_420ms_ease-in_both]`. Static evidence shows a long `ease-in` animation on a likely repeated command surface. | Remove open/close animation from the command palette; preserve instant state/focus feedback. |
| 2 | HIGH | Performance, easing, cohesion | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in;`. This bypasses tokens, may animate unintended properties, exceeds small-popover timing, and starts slowly. | Replace with explicit `transform, opacity` transitions using existing duration/easing tokens. |
| 3 | MEDIUM | Physicality/origin | `src/styles/motion.css` | `.popover { transform-origin: center; }` is suspicious for trigger-anchored popovers. Static evidence does not prove which popover primitive is used. | Use a trigger-origin CSS variable with safe fallback; stop if the component is actually a centered modal-like surface. |
| 4 | MEDIUM | Performance, accessibility | `src/components/toast.css` | Toast entry animates `top` for `500ms ease-in` and has no evidenced Reduced Motion path. | Animate `transform` + `opacity`, shorten timing, and add Reduced Motion that keeps opacity feedback without vertical travel. |
| 5 | HIGH | Gesture performance, interruptibility | `src/components/SortableQueue.tsx` | Pointer movement writes `--drag-y` on `queueRef.current`; settle uses fixed `duration: 400`. This is risky for high-frequency drag because parent CSS-var writes can fan out style recalculation and fixed tweens may not preserve gesture continuity. | Drive the dragged element’s `transform` directly; shorten or spring/retarget settle; add Reduced Motion branch. |
| 6 | MEDIUM | Cohesion/accessibility | Cross-cutting snippets | Button shows the desired tokenized + Reduced Motion precedent, while popover, palette, toast, and queue bypass it. | Standardize on existing tokens and local Reduced Motion behavior rather than one-off timings/classes. |

## 3. Implementation plans

### Plan 1 — Tokenize CSS entrances and remove layout animation

**Files/current excerpts**

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

- Popovers feel immediate and anchored, with explicit `transform`/`opacity` transitions only.
- Toasts enter with composited movement, not `top`, and complete quickly.
- Reduced Motion keeps feedback through opacity while removing vertical travel where possible.

**Project conventions**

- Reuse existing semantic tokens from `src/styles/motion.css`.
- Follow the correct precedent in `src/components/Button.css`:

```css
.button {
  transition: transform var(--duration-fast) var(--ease-responsive);
}

@media (prefers-reduced-motion: reduce) {
  .button { transition-duration: 80ms; }
}
```

**Ordered steps**

1. In `src/styles/motion.css`, replace the `.popover` block with explicit properties:

```css
.popover {
  transform-origin: var(--radix-popover-content-transform-origin, var(--transform-origin, center));
  transition:
    transform var(--duration-panel) var(--ease-responsive),
    opacity var(--duration-panel) var(--ease-responsive);
}
```

2. Add a Reduced Motion override in `src/styles/motion.css`:

```css
@media (prefers-reduced-motion: reduce) {
  .popover {
    transition:
      opacity 80ms var(--ease-responsive),
      transform 80ms var(--ease-responsive);
  }
}
```

3. In `src/components/toast.css`, replace the toast keyframes with transform-based movement:

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
  animation: toast-enter 200ms var(--ease-responsive) forwards;
}
```

4. Add a Reduced Motion override to `src/components/toast.css`:

```css
@media (prefers-reduced-motion: reduce) {
  @keyframes toast-enter {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .toast {
    animation-duration: 120ms;
  }
}
```

**Hard boundaries**

- Do not change popover markup, placement logic, z-index, focus handling, or visibility state.
- Do not introduce new tokens unless existing token names are absent in the real file.
- Do not animate `top`, `left`, `width`, `height`, margin, or padding.
- If `.popover` is confirmed to be a centered modal rather than a trigger-anchored popover, stop and do not change `transform-origin`.
- If either exact current excerpt is not present, stop and report source drift.

**Mechanical checks**

- Search targeted CSS for `transition: all`, `360ms ease-in`, `500ms ease-in`, and `top:` inside `toast-enter`; none should remain in these excerpts.
- Run the project’s existing lint/typecheck/build commands if available. If package scripts are unknown, record that mechanical validation is limited to static inspection.

**Runtime/feel checks**

- Open/close a popover repeatedly and confirm it starts promptly rather than easing in slowly.
- In slow playback, confirm popover motion uses its trigger-origin when the underlying primitive exposes one; otherwise it should safely fall back without breaking.
- Trigger a toast and confirm it slides a short distance without pushing layout.
- No browser/device validation was performed as part of this audit; these are executor checks.

**Reduced Motion behavior**

- Popover: shortened feedback, no long travel.
- Toast: opacity feedback remains; vertical movement is removed.

**Source-drift stop condition**

- Stop if the supplied `.popover`, `toast-enter`, or `.toast` snippets no longer match closely enough to make the edits mechanically.

---

### Plan 2 — Remove command palette open animation

**File/current excerpt**

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

- Command palette state changes should not be slowed by decorative entrance motion.
- Opening from keyboard should feel instant and preserve focus/causality.
- Reduced Motion path is identical to default because there is no movement to reduce.

**Project conventions**

- Existing design direction favors crisp motion and visible focus.
- Use the button precedent only for tactile press feedback, not for high-frequency palette open/close animation.
- Do not add new animation tokens for this surface.

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, remove the arbitrary animation utility from the wrapper:

```tsx
export function CommandPalette({ open }: { open: boolean }) {
  return (
    <div data-open={open}>
      <SearchResults />
    </div>
  );
}
```

2. If the real component has additional class names not shown, remove only `animate-[palette_420ms_ease-in_both]` and preserve all layout, theme, focus-ring, and state classes.
3. Search for the `palette` keyframes or Tailwind animation definition. If it is unused after this change, remove only that unused palette animation definition in the same change; otherwise leave it.

**Hard boundaries**

- Do not change command search behavior, keyboard shortcuts, focus management, result rendering, or open-state logic.
- Do not replace the removed animation with fade, scale, blur, or stagger.
- Do not add a dependency or motion library.
- If the component depends on animation end events for mounting/unmounting, stop and report; do not improvise.

**Mechanical checks**

- Search for `animate-[palette_420ms_ease-in_both]`; it should not remain on the command palette.
- Type-check the TSX file with the project’s existing command if available.
- If unused keyframes are removed, search for `palette` references before deleting.

**Runtime/feel checks**

- Open the command palette via keyboard several times in a row.
- Confirm the palette is available immediately and search input focus is not delayed.
- Confirm there is no visual “wait” before the first typed character appears.
- Confirm visible focus remains intact.

**Reduced Motion behavior**

- Same as default: no movement animation.
- Any existing focus/selection feedback should remain visible.

**Source-drift stop condition**

- Stop if the exact animation class is absent, renamed, or tied to lifecycle cleanup logic.

---

### Plan 3 — Make sortable drag motion direct, interruptible, and reduced-motion aware

**File/current excerpt**

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

- During drag, update only the actively dragged element or drag layer with `transform`.
- Avoid parent-level CSS-variable writes for every pointer move.
- Settle should feel continuous from the drag and should not use a slow fixed 400ms UI tween.
- Reduced Motion should preserve final placement feedback with shorter, gentler movement.

**Project conventions**

- Prefer transform-only motion, as shown by the button precedent.
- Use existing timing tokens where practical:
  - fast feedback: `160ms`
  - panel/settle ceiling: `240ms`
  - responsive curve: `cubic-bezier(0.23, 1, 0.32, 1)`

**Ordered steps**

1. Inspect the real `SortableQueue.tsx` for the dragged item ref or drag-layer element.
2. If a dragged element ref exists, change pointer movement from parent CSS-var writes to direct transform writes:

```tsx
function onPointerMove(event: PointerEvent) {
  draggedItemRef.current?.style.setProperty(
    "transform",
    `translate3d(0, ${event.clientY}px, 0)`
  );
}
```

3. If the current coordinate system expects a delta rather than viewport `clientY`, preserve the existing math and apply only the resulting Y value through `translate3d(0, ${y}px, 0)`.
4. Replace the fixed 400ms settle with a shorter token-aligned duration unless an existing spring helper is already present:

```tsx
function onPointerUp() {
  setDragging(false);
  animateTo(nearestSlot(currentY), {
    duration: 240,
    easing: "cubic-bezier(0.23, 1, 0.32, 1)",
  });
}
```

5. If `animateTo` already supports spring parameters and the project has an existing spring convention, use that existing convention instead of inventing one. Otherwise keep the explicit 240ms responsive settle.
6. Add a Reduced Motion branch using the project’s existing reduced-motion helper if present. If no helper exists, use `window.matchMedia("(prefers-reduced-motion: reduce)")` at the interaction boundary and shorten settle:

```tsx
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

animateTo(nearestSlot(currentY), {
  duration: prefersReducedMotion ? 80 : 240,
  easing: "cubic-bezier(0.23, 1, 0.32, 1)",
});
```

**Hard boundaries**

- Do not change sorting rules, nearest-slot calculation, queue data, keyboard ordering, or persistence.
- Do not add a new animation library.
- Do not apply transforms to the whole queue if only one item is dragged.
- Do not keep both `--drag-y` parent updates and direct element transforms.
- If there is no stable dragged element or drag-layer ref, stop and report that a safe implementation requires identifying the active visual element first.

**Mechanical checks**

- Search this file for `style.setProperty("--drag-y"`; it should be removed or no longer used for per-pointer drag motion.
- Search for `duration: 400` in sortable settle code; it should be replaced for this interaction.
- Run existing type-check/lint commands if available.

**Runtime/feel checks**

- Drag an item slowly and quickly; confirm the dragged item tracks the pointer without moving unrelated children through inherited CSS variables.
- Release near a slot; confirm settle is crisp and does not feel like a delayed glide.
- Interrupt by starting another drag quickly after release; confirm no stale transform remains on the previous item.
- In slow playback, confirm only transform changes during drag/settle.

**Reduced Motion behavior**

- Drag tracking remains direct because it is user-controlled.
- Programmatic settle duration shortens to `80ms`; avoid extra bounce or decorative travel.

**Source-drift stop condition**

- Stop if `animateTo` does not accept `duration`/`easing`, if the coordinate system is unclear, or if no dragged element/ref can be identified safely.

## 4. Recommended execution order

1. **Plan 2 — Command palette**: highest throughput impact, smallest safest change.
2. **Plan 1 — CSS entrances**: removes broad `transition: all`, slow `ease-in`, and layout animation from shared/component CSS.
3. **Plan 3 — Sortable queue**: important but requires inspecting real drag structure and `animateTo` API before editing.

## Explicitly unverified states

- Actual line numbers, package manager, build scripts, Tailwind config, keyframe definitions, and whether the palette animation is referenced elsewhere.
- Whether `.popover` is backed by a trigger-origin primitive or is actually used for centered modal-like content.
- Actual command palette mount/unmount lifecycle and focus behavior.
- Actual toast stacking/dismiss behavior.
- Actual sortable DOM structure, drag-layer refs, coordinate math, and `animateTo` API.
- Runtime performance, computed styles, accessibility tree, browser behavior, and device feel.

Internal frontend/accessibility and quality planning guardrails were applied. No files were edited or created.


## Output B

## 1. Recon summary

**One-sentence diagnosis:** the motion system has a good local precedent, but several higher-frequency or state-continuity surfaces bypass it with long `ease-in`, broad-property, layout-property, or direct-manipulation motion that is not shown to have a Reduced Motion equivalent.

- **Stack signals:** React/TSX components, CSS modules/global CSS, CSS custom-property motion tokens, Tailwind-style arbitrary animation utility, and imperative JS animation for drag settle.
- **Where motion lives:**  
  - `src/styles/motion.css`: global tokens and `.popover` transition.  
  - `src/components/CommandPalette.tsx`: inline utility animation class.  
  - `src/components/toast.css`: keyframe animation.  
  - `src/components/SortableQueue.tsx`: pointer-driven CSS variable updates plus `animateTo(...)`.  
  - `src/components/Button.css`: correct local precedent.
- **Existing conventions:** `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`, explicit property transitions, transform-based press feedback, and a `prefers-reduced-motion` branch.
- **Product personality:** calm, crisp, workday desktop utility; motion should clarify causality and state continuity without adding waiting time.
- **Frequency map:**  
  - Very high: command palette, buttons, keyboard-triggered actions.  
  - High/interactive: sortable queue drag.  
  - Medium: popovers.  
  - Occasional but visible: toasts.  
- **Evidence level:** static snippets only. No runtime behavior, computed styles, frame pacing, accessibility tree, user testing, or browser/device validation was performed.

---

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | Static source | `src/components/CommandPalette.tsx` | `animate-[palette_420ms_ease-in_both]` is long, arbitrary, and `ease-in` for a likely keyboard-heavy surface; it also bypasses shown semantic tokens. | Replace with tokenized opacity/transform state transition around `160–240ms` using `--ease-responsive`; add Reduced Motion branch that preserves feedback without travel. |
| P1 | Static source | `src/components/SortableQueue.tsx` | Direct manipulation settles with `animateTo(nearestSlot(currentY), { duration: 400 })`; snippet does not show grab offset, pointer capture, presentation-value interruption, velocity handling, or Reduced Motion behavior. | Preserve `nearestSlot(...)` semantics, but make drag coordinate space, transform ownership, interruption, and settle behavior explicit; shorten/tokenize or use existing spring primitive if available. |
| P2 | Static source | `src/components/toast.css` | Toast enters by animating `top` over `500ms ease-in`; this is a layout-property animation risk and slower than existing motion tokens. | Animate `transform` + `opacity` instead; use `--duration-panel` or shorter with `--ease-responsive`; add Reduced Motion opacity-only feedback. |
| P2 | Static source | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in`; broad property ownership plus slow-start easing conflicts with crisp tokenized precedent. | Transition only `opacity`/`transform`; use existing duration/easing tokens; verify whether origin should be trigger-relative before changing `transform-origin`. |
| P2 | Static source | Multiple snippets | Reduced Motion is shown only for `.button`; meaningful movement in palette, toast, popover, and queue has no shown equivalent path. | Add per-surface Reduced Motion branches that remove large spatial movement while preserving opacity/color/focus/static state feedback. |
| P3 | Static source | Multiple snippets | Motion vocabulary is fragmented: `160ms`, `240ms`, `360ms`, `400ms`, `420ms`, `500ms`, `ease-in`, `ease-responsive`. | Normalize to existing semantic tokens first; introduce new tokens only if repeated use cases are proven. |

---

## 3. Implementation-ready plans

### Plan A — Tokenize high-frequency overlay motion: command palette + popover

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

```css
/* src/components/Button.css - existing correct local precedent */
.button {
  transition: transform var(--duration-fast) var(--ease-responsive);
}
```

**Target behavior**

- Command palette opens/closes crisply with no long delayed-feeling entrance.
- Popover motion is bounded to visual properties only.
- Existing tokens remain the motion authority.
- Focus visibility and keyboard flow are not altered.
- Reduced Motion removes spatial travel but keeps clear state feedback.

**Project conventions to follow**

- Use `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Prefer explicit `transition-property` over `transition: all`.
- Reuse the button precedent: transform-based feedback, tokenized timing, Reduced Motion branch.

**Ordered steps**

1. Inspect the actual `palette` keyframes before editing; confirm whether they animate only `opacity`/`transform` or something else.
2. In `src/components/CommandPalette.tsx`, replace the arbitrary animation class with a stable class name, for example `className="command-palette-motion"`, while preserving `data-open={open}`.
3. In `src/styles/motion.css`, add tokenized selectors for the command palette:
   - `[data-open="true"]`: `opacity: 1`, `transform: translateY(0) scale(1)`.
   - `[data-open="false"]`: `opacity: 0`, small `translateY(...)` or scale only if the component remains mounted.
   - transition only `opacity` and `transform`.
4. Replace `.popover { transition: all 360ms ease-in; }` with explicit `opacity`/`transform` transitions using existing tokens.
5. For `.popover`, verify whether it is a trigger-anchored popover or a centered overlay:
   - Trigger-anchored: use the positioning primitive’s transform-origin variable if present.
   - Truly centered modal-like overlay: retaining `center` is acceptable.
6. Add `@media (prefers-reduced-motion: reduce)` for both surfaces:
   - remove or minimize `transform` travel;
   - keep short opacity/color feedback;
   - do not hide focus indicators.

**Hard boundaries**

- Do not change `SearchResults`.
- Do not change command execution, focus trapping, Escape behavior, or keyboard shortcuts.
- Do not introduce a new animation dependency.
- Do not invent a transform-origin variable unless the positioning library exposes one.
- Do not alter layout, z-index, or data loading.

**Mechanical checks**

- Search for remaining `palette_420ms_ease-in_both`.
- Search for `.popover` still using `transition: all`.
- Run the closest available static checks, such as type-check, lint, or build.
- Confirm no new hard-coded motion values were added unless intentionally justified.

**Runtime/feel checks to perform later**

- Toggle command palette repeatedly by keyboard.
- Reverse open/close mid-transition.
- Check focus ring remains visible during and after transition.
- Open popovers from different placements if collision/side placement exists.
- Confirm no claim of smoothness until observed in a browser.

**Reduced Motion behavior**

- Palette/popover should avoid positional travel.
- Keep a short opacity or static state change so the user still receives feedback.
- Focus visibility must remain unchanged.

**Source-drift stop condition**

Stop before editing if the `data-open` contract changed, the `palette` animation is no longer present, motion tokens were renamed, `.popover` is no longer the active selector, or authority now defines a different overlay motion language.

---

### Plan B — Repair toast entry to avoid layout-property motion and add Reduced Motion

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

- Toast entry remains noticeable but calm and quick.
- Movement preserves “arrived from above” causality without animating `top`.
- Reduced Motion keeps feedback without vertical travel.
- Existing toast placement and stacking semantics are not changed.

**Project conventions to follow**

- Use existing semantic duration/easing tokens.
- Prefer `transform` and `opacity` for visual motion.
- Keep transient UI motion shorter than current `500ms`.

**Ordered steps**

1. Confirm whether `.toast` already has a static `top` or positioning rule elsewhere; do not remove placement.
2. Rewrite `@keyframes toast-enter` to use `transform: translateY(-24px)` and `opacity: 0` to `transform: translateY(0)` and `opacity: 1`.
3. Change `.toast` animation timing from `500ms ease-in` to a tokenized value, preferably `var(--duration-panel) var(--ease-responsive)` unless a smaller existing toast token exists.
4. Add a Reduced Motion branch:
   - either use an opacity-only keyframe;
   - or set animation duration to a very short tokenized duration and remove transform travel.
5. If exit animation exists elsewhere, align it separately; do not invent a lifecycle rewrite from this snippet alone.

**Hard boundaries**

- Do not change toast queueing, ARIA announcements, dismissal timing, or stacking layout unless those files are explicitly in scope.
- Do not change `top`/positioning used for final placement; only remove `top` from the animation keyframes.
- Do not add blur, bounce, or decorative overshoot.

**Mechanical checks**

- Search `toast-enter` and confirm it no longer animates `top`.
- Search for hard-coded `500ms ease-in` in toast CSS.
- Run available CSS/lint/build checks.
- Confirm the Reduced Motion branch is present in `src/components/toast.css` or the project’s established motion stylesheet.

**Runtime/feel checks to perform later**

- Trigger one toast and multiple rapid toasts.
- Verify the toast appears promptly and remains readable.
- Reverse/dismiss during entry if dismissal exists.
- Validate with Reduced Motion enabled.
- Do not claim frame-rate improvement without tracing or representative observation.

**Reduced Motion behavior**

- No vertical travel.
- Preserve feedback through opacity or immediate visible state.
- Keep announcements and focus behavior unchanged.

**Source-drift stop condition**

Stop before editing if toast positioning has moved to another component, `toast-enter` is unused, a toast animation API replaces this CSS, or a newer design authority defines a different transient notification pattern.

---

### Plan C — Make sortable queue drag settle explicit, interruptible, and reduced-motion safe

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

- Drag tracks in a clearly defined coordinate space.
- The dragged item does not jump under the pointer.
- Release settle starts from the current on-screen value.
- Existing `nearestSlot(currentY)` target-selection semantics are preserved unless product authority explicitly approves momentum-based target selection.
- Reduced Motion avoids long travel/elasticity while preserving the final slot update and state feedback.

**Project conventions to follow**

- Use existing motion tokens where fixed durations remain.
- Keep transform ownership explicit.
- Treat direct manipulation separately from decorative CSS transitions.
- Preserve current queue ordering semantics.

**Ordered steps**

1. Locate the full `SortableQueue.tsx` implementation and the CSS consuming `--drag-y`.
2. Confirm coordinate space:
   - whether `clientY` is converted relative to the queue/container;
   - how `currentY` is derived;
   - whether scrolling affects the calculation.
3. Confirm pointer lifecycle:
   - pointer capture on drag start;
   - pointer release/cancel cleanup;
   - ignored secondary pointers if relevant.
4. Add or verify grab-offset preservation so the item remains attached to the original contact point rather than snapping to `event.clientY`.
5. Identify transform ownership:
   - if drag uses `translateY`, do not let press/hover scale overwrite it;
   - use wrapper layers or composed transform if needed.
6. Replace or parameterize `duration: 400`:
   - if existing animation primitive supports springs/current value, settle from the presentation value;
   - otherwise use a shorter tokenized fallback and document limitation.
7. Optionally measure release velocity in CSS px/s for animation handoff only.
   - Do not use projected endpoint to change `nearestSlot(...)` target selection unless explicitly authorized.
8. Add Reduced Motion behavior:
   - no elastic overshoot;
   - either immediate snap with static highlight/state feedback or very short non-vestibular transition.

**Hard boundaries**

- Do not change `nearestSlot(...)` semantics by default.
- Do not change queue data model, persistence, sorting rules, or revenue/support workflow behavior.
- Do not add a new physics/animation library unless already present and approved.
- Do not mix this with unrelated visual restyling.
- Do not claim touch/device feel from source inspection.

**Mechanical checks**

- Type-check the component.
- Verify pointer cleanup paths compile.
- Search for conflicting writes to `--drag-y` or `transform`.
- Confirm Reduced Motion branch is reachable.
- Confirm no global queue CSS variable update was broadened unnecessarily.

**Runtime/feel checks to perform later**

- Drag slowly, quickly, and outside the original item bounds.
- Release while moving and while stationary.
- Start a new drag during settle; verify no visual jump.
- Test with page/container scroll if the queue can scroll.
- Test Reduced Motion.
- If touch support matters, validate on representative hardware before approving feel.

**Reduced Motion behavior**

- Preserve drag functionality.
- Remove bounce, large animated settle, and decorative elasticity.
- Keep slot change clear through immediate placement, focus/state styling, or short opacity/color feedback.

**Source-drift stop condition**

Stop before editing if `animateTo(...)` API changed, `nearestSlot(currentY)` is no longer the target rule, drag CSS no longer uses `--drag-y`, pointer handlers moved, or a different gesture abstraction owns the queue interaction.

---

## 4. Recommended execution order

1. **Plan A** first: fixes the highest-frequency keyboard/overlay motion and reinforces token conventions.
2. **Plan B** second: localized CSS repair with clear accessibility and performance-risk reduction.
3. **Plan C** third: highest interaction complexity; do it when runtime validation time is available. If the sortable queue is core all-day work, move it before Plan B.

## Explicitly unverified states

- Actual `palette` keyframes and whether the command palette unmounts on close.
- Whether `.popover` is trigger-anchored, centered, or shared by multiple overlay types.
- Toast stacking, exit animation, dismissal timing, ARIA behavior, and visibility-timer behavior.
- `SortableQueue` coordinate system, transform consumption, pointer capture, grab offset, item count, scroll behavior, and animation API capabilities.
- Actual `DESIGN.md` text beyond the provided summary.
- Runtime smoothness, frame pacing, compositing, layout shift, focus order, accessibility tree behavior, and real Reduced Motion behavior.


## Output C

No files were edited. This is a static-evidence audit only.

## 1. Recon summary

**Stack signals**
- React/TSX components with CSS styling.
- Global CSS motion tokens in `src/styles/motion.css`.
- Component-scoped CSS in `src/components/toast.css` and `src/components/Button.css`.
- Utility-style arbitrary animation class in `CommandPalette.tsx`, likely compiled by the styling pipeline.
- Imperative pointer animation in `SortableQueue.tsx`.

**Where motion currently lives**
- Shared tokens: `src/styles/motion.css`.
- Local component precedent: `src/components/Button.css`.
- Inline/arbitrary component animation: `src/components/CommandPalette.tsx`.
- Component keyframes: `src/components/toast.css`.
- Imperative drag/snap behavior: `src/components/SortableQueue.tsx`.

**Existing conventions**
- Semantic duration tokens exist:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
- Semantic easing exists:
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Correct local precedent uses:
  - transform-only transition
  - tokenized duration/easing
  - Reduced Motion override that preserves feedback at `80ms`

**Product personality**
- Calm, crisp, desktop operations console.
- Motion should clarify cause/effect and state continuity.
- Motion should not create delay for keyboard-heavy support/revenue workflows.

**Frequency map, based only on component roles**
- Very high frequency: buttons, command palette, sortable queue interactions.
- Medium/high frequency: popovers.
- Intermittent but attention-sensitive: toasts.
- No runtime frequency measurement was performed.

**Evidence level**
- Static snippets only.
- No computed styles, browser validation, device testing, traces, accessibility tree, screen recording, or user testing.

---

## 2. Priority table

| Priority | Finding | Static evidence | Why it matters | Target direction |
|---:|---|---|---|---|
| P0 | Motion contract is fragmented | Tokens exist, but palette/toast/drag use hardcoded `420ms`, `500ms`, `400`, `ease-in`, and arbitrary animation syntax | Inconsistent tempo can make a workday console feel less predictable | Route common UI motion through existing semantic tokens and Reduced Motion convention |
| P0 | Popover uses broad transition and slow accelerating ease | `.popover { transition: all 360ms ease-in; }` | `all` can animate unintended properties; `ease-in` delays perceived response | Restrict to `opacity, transform`; use `--duration-panel` or `--duration-fast` and `--ease-responsive` |
| P0 | Command palette animation is long, hardcoded, and not visibly Reduced Motion-aware | `animate-[palette_420ms_ease-in_both]` | Command palette is likely high-frequency for keyboard operators; 420ms may feel like throughput friction | Use tokenized transform/opacity state transition; add Reduced Motion path preserving open/close feedback |
| P1 | Toast enters by animating layout property | `@keyframes toast-enter { from { top: -24px; ... } }` and `500ms ease-in` | Animating `top` is less aligned with transform-only precedent; 500ms may overemphasize transient feedback | Animate `transform` + `opacity`; shorten to token duration; Reduced Motion uses brief opacity/position confirmation |
| P1 | Sortable queue snap duration is hardcoded and pointer updates are direct per event | `setProperty("--drag-y", ...)`; `animateTo(... { duration: 400 })` | Drag/drop is task-critical; motion should track causality without lingering | Use frame-coalesced updates if needed; reduce snap duration; honor Reduced Motion with near-immediate settle |
| P2 | Focus continuity is an explicit requirement but not evidenced here | No focus excerpts provided | Keyboard-heavy workflows depend on visible focus through animated state changes | Treat focus as a required implementation checkpoint, not as a proven defect from these snippets |

---

## 3. Implementation plans

### Plan A — Normalize overlay motion for popovers and command palette

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
- Popovers and command palette open/close with short, crisp opacity/transform motion.
- No `transition: all`.
- No hardcoded long overlay durations.
- Command palette remains responsive for keyboard-heavy use.
- Reduced Motion still communicates state change, but with minimal duration/displacement.

**Project conventions to apply**
- Use `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Follow the button precedent: transform-based motion, tokenized timing, `80ms` Reduced Motion path.
- Preserve visible focus; do not hide outlines during animation.

**Ordered steps**
1. Inspect actual full contents of:
   - `src/styles/motion.css`
   - `src/components/CommandPalette.tsx`
   - any existing `palette` keyframes or `.popover` state selectors.
2. Replace `.popover` broad transition with explicit properties only:
   - `opacity`
   - `transform`
3. Change popover timing from `360ms ease-in` to tokenized timing:
   - default candidate: `var(--duration-panel) var(--ease-responsive)`
   - if popovers are tiny/contextual, use `var(--duration-fast)`.
4. Replace the arbitrary command palette animation class with a stable class, for example:
   - `className="command-palette"`
   - keep `data-open={open}`.
5. Add tokenized state styles in the existing motion stylesheet or the component’s existing style location, depending on actual project conventions:
   - closed: slightly translated/scaled and transparent
   - open: neutral transform and opaque
6. Add Reduced Motion overrides:
   - duration `80ms`
   - remove or minimize translate/scale
   - preserve opacity/state feedback.
7. Re-check that focus styles are not removed or visually obscured by the new styles.

**Hard boundaries**
- Do not redesign command palette layout.
- Do not change search behavior, keyboard handling, filtering, or focus management unless existing code requires a className merge.
- Do not introduce a new animation library.
- Do not create new global tokens unless existing tokens are insufficient after inspecting the full file.

**Mechanical checks**
- Search for remaining instances of:
  - `transition: all`
  - `420ms`
  - `360ms`
  - `ease-in`
  - `animate-[palette`
- Run the closest available type/lint/build check for the frontend.
- Confirm CSS syntax compiles under the project’s styling pipeline.

**Runtime / feel checks to perform later**
- Open/close command palette by keyboard repeatedly.
- Confirm perceived response starts immediately.
- Confirm focus remains visible before, during, and after open/close.
- Open/close popovers in dense UI areas and confirm no sluggishness or surprise property animation.

**Reduced Motion behavior**
- Keep state change visible.
- Prefer opacity-only or near-opacity-only transition.
- Use `80ms` duration, matching the existing button precedent.

**Source-drift stop condition**
- Stop before editing if:
  - `.popover` is used for multiple unrelated components with incompatible state models.
  - `palette` keyframes are shared elsewhere.
  - the command palette unmounts immediately on close, making close-state CSS impossible without component lifecycle changes.

---

### Plan B — Rework toast enter motion to transform/opacity

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
- Toast appears promptly without animating layout-position properties.
- Motion is noticeable enough for feedback but not dominant.
- Toast movement is shorter and calmer.
- Reduced Motion keeps feedback through a brief opacity change or instant positional state.

**Project conventions to apply**
- Use existing duration/easing tokens.
- Prefer `transform` over `top`.
- Keep Reduced Motion feedback instead of removing it entirely.

**Ordered steps**
1. Inspect full `src/components/toast.css` for positioning, stacking, exit animations, and variants.
2. Replace keyframe movement from `top` to `transform`, for example:
   - from: `transform: translateY(-8px); opacity: 0;`
   - to: `transform: translateY(0); opacity: 1;`
3. Replace `500ms ease-in` with:
   - `var(--duration-panel) var(--ease-responsive)` for standard toast entrance, or
   - `var(--duration-fast)` if toasts are frequent and should feel more immediate.
4. Ensure `.toast` has a stable final transform state.
5. Add a Reduced Motion override:
   - shorten to `80ms`
   - remove translate distance or reduce it to zero
   - preserve opacity feedback.
6. If there is an exit animation in the full file, align it with the same token/easing system.

**Hard boundaries**
- Do not change toast copy, severity styling, queueing, dismissal logic, or stacking behavior.
- Do not alter layout offsets unless current `top` animation is also being used as static positioning.
- Do not add decorative bounce, spring, overshoot, or attention-grabbing motion.

**Mechanical checks**
- Search for:
  - `toast-enter`
  - `.toast`
  - `top: -24px`
  - `500ms`
- Confirm no remaining toast keyframe animates `top`.
- Run the closest available CSS/build/lint check.

**Runtime / feel checks to perform later**
- Trigger success, error, and neutral toasts if available.
- Confirm toast does not feel delayed.
- Confirm stacked toasts, if supported, do not visually jump.
- Confirm dismissal timing still reads clearly.

**Reduced Motion behavior**
- Toast should appear in final position.
- Use `80ms` opacity feedback or equivalent minimal confirmation.
- Do not silently remove all feedback.

**Source-drift stop condition**
- Stop before editing if:
  - `top` is used by JS to calculate stacking or collision.
  - the same keyframes are reused for non-toast surfaces.
  - there are multiple toast systems and this file is not the active one.

---

### Plan C — Make sortable queue drag/snap motion throughput-safe

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
- Drag motion tracks pointer causality directly.
- Drop/snap motion is brief and clear, not lingering.
- Pointer movement updates avoid unnecessary per-event style work where practical.
- Reduced Motion preserves final-placement feedback with minimal interpolation.

**Project conventions to apply**
- Align timing with existing semantic durations:
  - likely `--duration-fast` for snap feedback
  - avoid hardcoded `400`.
- Keep interaction responsive for high-throughput queue operations.
- Preserve keyboard/focus behavior if sortable controls support it.

**Ordered steps**
1. Inspect full `src/components/SortableQueue.tsx` for:
   - `currentY` source of truth
   - `animateTo` implementation/import
   - cleanup on unmount
   - pointer capture/release
   - keyboard sorting support
   - CSS use of `--drag-y`.
2. Search for all `animateTo(` calls to understand duration conventions.
3. If pointer events are frequent and direct style writes are not already coalesced elsewhere, introduce requestAnimationFrame coalescing around the CSS variable update.
4. Ensure pending animation frame is cancelled on pointer up and unmount.
5. Replace hardcoded snap duration:
   - default candidate: `160ms`
   - use the existing token value if `animateTo` accepts numeric milliseconds only.
6. Add or route through an existing Reduced Motion signal:
   - reduced: `0–80ms` snap, no long interpolation
   - still update final slot visibly.
7. Confirm `nearestSlot(currentY)` still receives the correct final coordinate after any coalescing change.

**Hard boundaries**
- Do not rewrite sorting architecture.
- Do not change item ordering semantics.
- Do not introduce virtualization or a drag/drop dependency.
- Do not change persistence, queue data model, or revenue/support workflow logic.
- Do not claim performance improvement without measurement.

**Mechanical checks**
- Search for:
  - `--drag-y`
  - `onPointerMove`
  - `onPointerUp`
  - `animateTo(`
  - `duration: 400`
- Type-check the component.
- Confirm cleanup paths for animation frames and pointer state.

**Runtime / feel checks to perform later**
- Drag slowly, quickly, and across multiple slots.
- Drop near slot boundaries.
- Confirm snap feels causal and does not delay the next operation.
- Confirm keyboard sorting/focus state, if present, remains visible and predictable.
- Check Reduced Motion mode separately.

**Reduced Motion behavior**
- Drag should still follow the pointer.
- Drop should settle immediately or within `80ms`.
- Preserve final-slot confirmation through position, focus, or non-motion visual state.

**Source-drift stop condition**
- Stop before editing if:
  - `animateTo` uses physics parameters rather than milliseconds.
  - `currentY` is not the same coordinate space as `event.clientY`.
  - `--drag-y` drives layout instead of transform.
  - sorting already has an animation abstraction that should be used instead.

---

## 4. Recommended execution order

1. **Plan A first** — establishes the shared overlay motion contract and removes the most obvious hardcoded/high-frequency mismatch.
2. **Plan B second** — low-risk improvement that aligns toast feedback with transform/token conventions.
3. **Plan C third** — highest interaction sensitivity; inspect more code before changing because drag state, coordinates, and animation utilities may have hidden coupling.

## Explicitly unverified states

- No browser/device validation was performed.
- No computed CSS was inspected.
- No runtime animation timing was measured.
- No performance trace was captured.
- No accessibility tree or screen reader behavior was checked.
- No actual focus-ring behavior was verified.
- No user frequency analytics or task-throughput data was available.
- No source outside the provided snippets was inspected.

Planning guardrails applied: smallest-change, evidence-first implementation discipline; frontend accessibility, focus, and Reduced Motion constraints.
