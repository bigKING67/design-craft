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

**Stack signals**
- CSS custom properties are already present for motion timing/easing.
- Component styling appears mixed: global CSS, component CSS, and utility/arbitrary animation classes.
- React/TSX components use state/data attributes for UI state.

**Where motion lives**
- `src/styles/motion.css`: global motion tokens and `.popover`.
- `src/components/CommandPalette.tsx`: inline arbitrary animation class.
- `src/components/toast.css`: keyframes and toast animation.
- `src/components/SortableQueue.tsx`: imperative drag/update animation.
- `src/components/Button.css`: local precedent for tokenized, reduced-motion-aware interaction.

**Existing conventions**
- Semantic tokens:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Good precedent:
  - animate `transform`
  - use semantic duration/easing tokens
  - reduced motion shortens feedback to `80ms` rather than removing it entirely

**Product personality**
- Calm, crisp, workday-long desktop console.
- Motion should explain causality and state continuity without delaying keyboard-heavy workflows.

**Frequency map**
- Highest frequency: sortable queue drag/release, command palette, button feedback.
- Medium frequency: popovers.
- Lower frequency but attention-sensitive: toast entry.

**Evidence level**
- Static excerpt audit only.
- No runtime, computed-style, browser, device, trace, accessibility-tree, or user-test validation was performed.
- Findings below are implementation risks inferred from source snippets, not observed runtime defects.

---

## 2. Vetted priority table

| Priority | Finding | Static evidence | Why it matters | Target |
|---|---|---|---|---|
| P0 | Reduced Motion coverage is inconsistent | Button has a reduced path; popover, command palette, toast, and sortable release snippets do not show one | Existing design authority requires reduced motion while preserving feedback | Add explicit reduced-motion behavior to each motion surface |
| P0 | High-use motion uses slow/ease-in timing | Command palette `420ms ease-in`; drag release `400`; toast `500ms ease-in`; popover `360ms ease-in` | Ease-in and long durations can feel delayed for keyboard-heavy operators | Move frequent UI to `160ms–240ms` with `--ease-responsive` |
| P1 | Popover uses `transition: all` | `.popover { transition: all 360ms ease-in; }` | Over-broad transitions are hard to control and can accidentally animate layout/color/etc. | Restrict to `opacity, transform` or proven properties only |
| P1 | Toast animates `top` | `from { top: -24px; } to { top: 0; }` | Layout-affecting animation is less suitable than transform/opacity for crisp feedback | Use `transform: translateY(...)` plus opacity |
| P1 | Arbitrary animation string bypasses motion conventions | `animate-[palette_420ms_ease-in_both]` | Timing/easing becomes harder to govern and audit | Move palette motion to named class/keyframes or stateful CSS using tokens |
| P2 | Pointer move updates are unframed in snippet | `style.setProperty("--drag-y", ...)` on every pointer move | Pointer-heavy paths need guardrails to avoid unnecessary per-event work | Gate writes with `requestAnimationFrame` if current CSS uses transform |

---

## 3. Implementation plans

### Plan A — Normalize shared motion contract and popover behavior

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
- Popovers feel crisp and causal, not delayed.
- Only intentional visual properties animate.
- Reduced Motion keeps state feedback but minimizes travel/duration.

**Project conventions to preserve**
- Reuse existing semantic tokens.
- Match the button precedent: tokenized `transform`, responsive easing, reduced path at `80ms`.
- Do not introduce new global tokens unless inspection proves the existing set is insufficient.

**Ordered steps**
1. Inspect actual `.popover` usage and state selectors before editing.
2. Confirm whether open/closed state is represented by class, data attribute, ARIA state, mounted/unmounted behavior, or framework wrapper.
3. Replace broad transition with explicit properties, likely:
   - `transition-property: opacity, transform;`
   - `transition-duration: var(--duration-panel);`
   - `transition-timing-function: var(--ease-responsive);`
4. If state selectors exist, ensure closed/open styles use small transform distance and opacity only.
5. Add a reduced-motion rule:
   - duration `80ms`
   - preserve opacity/state feedback
   - remove or greatly reduce spatial travel
6. Search for other `transition: all` motion surfaces and decide whether they are in scope or should become follow-up findings.

**Hard boundaries**
- Do not alter popover placement, focus management, layering, keyboard behavior, or dismissal behavior.
- Do not change semantic tokens globally if that would affect unrelated components without review.
- Do not add spring/bounce motion; product personality is calm and operational.

**Mechanical checks**
- Static search for:
  - `transition: all`
  - `ease-in`
  - `.popover`
  - `prefers-reduced-motion`
- Run the closest CSS/frontend validation command available in the project.
- Verify no syntax errors in CSS.

**Runtime / feel checks to perform later**
- Open/close popover with keyboard and pointer.
- Confirm motion communicates appearance/disappearance without lag.
- Confirm focus ring remains visible throughout transition.
- Confirm no unexpected properties animate.

**Reduced Motion behavior**
- Keep opacity/state feedback.
- Use `80ms`.
- Avoid scale/translation or reduce it to near-zero.

**Source-drift stop condition**
- Stop and re-plan if `.popover` is owned by an external primitive with generated state classes, if placement depends on transform, or if another motion-token file already supersedes `src/styles/motion.css`.

---

### Plan B — Convert command palette and toast to tokenized transform/opacity motion

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
- Command palette opens/closes quickly enough for keyboard-heavy workflows.
- Toasts appear with clear feedback but avoid layout-position animation.
- Both use semantic durations/easing and have Reduced Motion behavior.

**Project conventions to preserve**
- Use `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Prefer named CSS/state classes over arbitrary one-off animation strings.
- Keep feedback present under Reduced Motion.

**Ordered steps**
1. Inspect existing imports for palette styling and toast CSS loading.
2. For `CommandPalette.tsx`, replace the arbitrary animation class with a stable class name plus `data-open={open}`.
3. Define palette state motion in the appropriate existing stylesheet:
   - open: opacity `1`, transform none or very small settle
   - closed: opacity `0`, small translate/scale only if it supports continuity
   - duration: likely `var(--duration-panel)` for panel appearance
   - easing: `var(--ease-responsive)`
4. Ensure closing behavior is compatible with mount/unmount semantics. If the component unmounts immediately elsewhere, do not fake an exit animation without confirming lifecycle support.
5. For `toast.css`, replace `top` keyframes with transform/opacity:
   - from: `transform: translateY(-8px); opacity: 0;`
   - to: `transform: translateY(0); opacity: 1;`
   - duration: likely `var(--duration-panel)` or `var(--duration-fast)` depending on existing toast density
6. Add `@media (prefers-reduced-motion: reduce)` for both:
   - `80ms`
   - opacity feedback retained
   - no or minimal translation

**Hard boundaries**
- Do not change search result rendering, command execution, focus trap, keyboard shortcuts, or toast content/lifetime.
- Do not introduce delayed animations that block input readiness.
- Do not rely on runtime-only class generation unless the project already supports it safely.

**Mechanical checks**
- Search for:
  - `animate-[palette`
  - `@keyframes toast-enter`
  - `animation:`
  - `ease-in`
- Run type-check/lint for TSX changes.
- Run CSS/build validation if available.

**Runtime / feel checks to perform later**
- Open command palette repeatedly via keyboard shortcut.
- Type immediately after opening; confirm input readiness is not visually or functionally delayed.
- Trigger a toast during active work; confirm it is noticeable but not theatrical.
- Test Reduced Motion setting and confirm feedback remains visible.

**Reduced Motion behavior**
- Palette: opacity transition only, `80ms`; no meaningful scale/slide.
- Toast: opacity transition only or near-zero transform, `80ms`.
- Feedback remains visible; no silent disappearance.

**Source-drift stop condition**
- Stop and re-plan if palette animation is defined elsewhere by the utility build config, if exit animation requires a presence/lifecycle wrapper not shown, or if toast positioning uses `top` for layout rather than visual entry.

---

### Plan C — Make sortable queue drag/release crisp, framed, and reduced-motion-aware

**Files / current excerpts**

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
- Drag movement stays directly coupled to pointer position.
- Release-to-slot communicates continuity without slowing throughput.
- Pointer-heavy updates avoid unnecessary work.
- Reduced Motion preserves snap feedback with shorter duration or instant positional resolution plus visible state change.

**Project conventions to preserve**
- Use token-equivalent timing: `160ms` or `240ms`, not `400ms`, unless later testing proves otherwise.
- Prefer transform-driven movement.
- Maintain keyboard and pointer usability.

**Ordered steps**
1. Inspect the full component and any related CSS consuming `--drag-y`.
2. Confirm whether `--drag-y` feeds `transform` only. If it affects layout properties, rework CSS first or stop.
3. Frame pointer writes:
   - store latest `clientY`
   - schedule one `requestAnimationFrame`
   - write `--drag-y` once per frame
   - cancel pending frame on cleanup/unmount
4. Shorten release animation:
   - default target: `var(--duration-fast)` equivalent, or numeric `160` if the animation API requires milliseconds
   - use responsive easing if the API supports easing
5. Add or route Reduced Motion behavior:
   - release duration `80ms` or immediate snap if the animation system cannot express a short reduced path
   - retain visible selected/dragging/drop state feedback
6. Ensure `setDragging(false)` timing does not remove visual continuity before the release animation can run. If current behavior depends on it, adjust only after inspecting actual state flow.

**Hard boundaries**
- Do not change sorting rules, nearest-slot logic, data order persistence, selection state, or pointer capture behavior unless inspection identifies a direct bug.
- Do not add inertia, bounce, overshoot, or decorative physics.
- Do not introduce global drag abstractions for this local fix.

**Mechanical checks**
- Type-check the component.
- Search for cleanup-sensitive APIs:
  - `requestAnimationFrame`
  - `cancelAnimationFrame`
  - `animateTo`
  - `--drag-y`
- Confirm no stale frame callback can write after unmount.
- Confirm animation duration units match the animation helper contract.

**Runtime / feel checks to perform later**
- Drag slowly and quickly through the queue.
- Release near slot boundaries.
- Confirm snap is legible but not sluggish.
- Confirm repeated drags do not leave stale transforms.
- Confirm Reduced Motion still gives clear drop confirmation.

**Reduced Motion behavior**
- Pointer tracking remains direct.
- Release snap uses `80ms` maximum, or immediate movement with non-motion feedback if required.
- No long glide, bounce, or overshoot.

**Source-drift stop condition**
- Stop and re-plan if `animateTo` is a physics/spring helper that does not accept duration as shown, if `currentY` is derived asynchronously in a way not visible here, or if `--drag-y` is consumed by layout properties rather than transform.

---

## 4. Recommended execution order

1. **Plan A first** — establishes the shared motion contract and fixes the broadest CSS risk.
2. **Plan B second** — brings high-visibility command palette and toast motion into the same system.
3. **Plan C third** — handles the highest-interaction pointer path after confirming full component behavior.

---

## Explicitly unverified states

- Actual rendered timing, easing, and computed styles.
- Whether shown CSS is imported on every relevant surface.
- Whether components mount/unmount in ways that permit exit motion.
- Whether `--drag-y` is consumed by transform, layout, or both.
- Whether `animateTo` accepts duration/easing exactly as implied.
- Keyboard focus behavior during palette/popover transitions.
- Reduced Motion behavior in an actual OS/browser setting.
- Performance characteristics under real pointer movement.
- Visual feel on target displays or with real operator workflows.

Applied the required quality and frontend planning constraints; no files were edited.


## Output B

Reading this as: a calm desktop operations console for keyboard-heavy support and revenue operators, optimized for fast state comprehension without decorative delay.

## 1. Recon summary

- **Stack signals:** React/TSX components, CSS modules/global CSS, Tailwind-style arbitrary animation class, CSS custom-property tokens, at least one JS animation helper: `animateTo(...)`.
- **Where motion lives:**  
  `src/styles/motion.css`, `src/components/CommandPalette.tsx`, `src/components/toast.css`, `src/components/SortableQueue.tsx`, `src/components/Button.css`.
- **Existing conventions:** semantic duration/easing tokens exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`; correct local precedent uses transform-only transition and a `prefers-reduced-motion` branch in `Button.css`.
- **Product personality:** crisp, quiet, operational, throughput-first. Motion should confirm cause/effect and preserve continuity, not perform.
- **Frequency map:**
  - Very high: command palette, buttons, keyboard-triggered actions.
  - High/direct manipulation: sortable queue drag/reorder.
  - Medium: popovers.
  - Occasional but interruptible: toasts.
- **Evidence level:** static snippets only. No runtime, computed-style, trace, browser, device, accessibility-tree, or user-test validation was performed.

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | Static source | `src/components/CommandPalette.tsx` | Command palette uses `animate-[palette_420ms_ease-in_both]`: long, ease-in, arbitrary value on a high-frequency keyboard surface; no Reduced Motion branch shown. | Replace with tokenized open/closed transition using `--duration-fast` or bounded `--duration-panel`, `--ease-responsive`, explicit properties, and reduced spatial motion. |
| P1 | Static source | `src/components/SortableQueue.tsx` | Drag/reorder code shows pointer-position CSS variable updates and a fixed `animateTo(..., { duration: 400 })`; no evidence of pointer capture, grab offset, velocity, projected snap, interruption, transform ownership, or Reduced Motion. | Implement/check a direct-manipulation contract before tuning duration: 1:1 tracking, pointer capture, presentation-value retargeting, velocity-aware snap, reduced overshoot/travel. |
| P2 | Static source | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in` and `transform-origin: center`; broad property ownership, slower-than-needed timing, delayed response curve, and likely wrong origin for anchored overlays. | Transition only `opacity`/`transform`, use existing responsive easing, shorten to overlay range, and set trigger-relative origin unless the popover is actually centered. |
| P2 | Static source | `src/components/toast.css` | Toast animates `top` over `500ms ease-in`; this is a layout-property animation risk and slow delayed entry for operational feedback. | Animate `transform` + `opacity` with existing tokens; keep feedback visible in Reduced Motion via short fade/static position. |
| P2 | Static source | Multiple snippets | Reduced Motion precedent exists only in `Button.css`; other meaningful movement snippets do not show equivalent handling. | Add component-scoped `prefers-reduced-motion` branches that remove large travel/scale while preserving opacity/color/state feedback. |
| P3 | Static source | Multiple snippets | Motion vocabulary is fragmented: `160ms`, `240ms` tokens coexist with hardcoded `360ms`, `420ms`, `500ms`, `400`. | Consolidate around semantic tokens and component-specific exceptions only when justified by runtime checks. |

## 3. Implementation-ready plans

### Plan 1 — Tokenize and calm transient overlay motion

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
  <SearchResults />
</div>
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

- Overlays and transient feedback feel immediate and calm.
- Entry starts responsive, settles quickly, and uses existing semantic tokens.
- No `transition: all` for these surfaces.
- No layout-position animation for toast entry.
- Command palette does not impose cinematic delay on keyboard-heavy users.
- Reduced Motion preserves state feedback without meaningful travel.

**Project conventions to use**

- `--duration-fast: 160ms`
- `--duration-panel: 240ms`
- `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Existing local Reduced Motion pattern from `src/components/Button.css`.

**Ordered steps**

1. In `src/styles/motion.css`, replace `.popover` broad transition with explicit properties, for example `opacity, transform`, using `var(--duration-fast)` or `var(--duration-panel)` depending on popover size.
2. Change `.popover` easing from `ease-in` to `var(--ease-responsive)`.
3. Replace default `transform-origin: center` with a trigger-relative origin if the component has placement/origin variables; keep `center` only for genuinely centered overlays.
4. In `src/components/CommandPalette.tsx`, remove the arbitrary `animate-[palette_420ms_ease-in_both]` class.
5. Implement open/closed styling via stable classes or `data-open` selectors using explicit `opacity`/`transform` transitions and existing tokens.
6. In `src/components/toast.css`, replace `top` keyframe movement with transform-based entry, e.g. `translateY(...)` plus `opacity`.
7. Shorten toast duration to the project token range, preferably `--duration-panel` at most unless runtime checks prove it feels abrupt.
8. Add `@media (prefers-reduced-motion: reduce)` branches for popover, command palette, and toast: remove or sharply reduce translate/scale; keep short opacity/state feedback.

**Hard boundaries**

- Do not change search behavior, command execution, focus management, or toast lifecycle timing.
- Do not add an animation dependency.
- Do not introduce new global motion tokens unless existing tokens cannot express the needed behavior.
- Do not modify `src/components/Button.css` except as a reference check.
- Do not claim performance improvement without runtime measurement.

**Mechanical checks**

- Inspect actual package scripts first.
- Run the closest available checks, in this order when present:
  - type check for TSX changes,
  - lint,
  - build or CSS pipeline check.
- Also grep for removed arbitrary animation names to ensure no orphaned `palette` keyframe/class dependency remains.

**Runtime / feel checks to perform later**

- Open/close command palette repeatedly via keyboard.
- Open/close popovers from different trigger positions.
- Fire multiple toasts in succession.
- Verify no visible delayed start from ease-in behavior.
- Verify focus remains visible and not hidden by entry animation.
- Use DevTools animation inspection or computed styles to confirm only intended properties animate.

**Reduced Motion behavior**

- Command palette: no scale/travel; immediate visibility or very short opacity transition.
- Popover: no origin-based scale travel; opacity/state feedback remains.
- Toast: appears in final position with short fade or static state change; no vertical slide.

**Source-drift stop condition**

Stop before editing if:
- `--duration-fast`, `--duration-panel`, or `--ease-responsive` were renamed/removed;
- `CommandPalette` no longer uses the shown arbitrary animation class;
- toast positioning no longer uses `top`;
- a newer design authority explicitly defines different overlay/toast motion.


### Plan 2 — Repair sortable queue drag/reorder as direct manipulation

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
- Reorder settle animation begins from the current on-screen value, not a reset target.
- Snap target accounts for release velocity/projected endpoint, not only current release position.
- Drag remains interruptible; user can grab/reverse without waiting for a fixed animation to finish.
- Reduced Motion removes elastic/large travel while preserving clear item placement feedback.

**Project conventions to use**

- Keep existing `animateTo(...)` only if it supports current-value retargeting and velocity/interrupt semantics.
- Use transform-based movement, not layout properties, for per-frame drag visuals.
- Keep motion calm: no unnecessary bounce for a serious operations queue.

**Ordered steps**

1. Inspect the full `SortableQueue.tsx` implementation before editing:
   - where `currentY` is defined,
   - how `--drag-y` is consumed,
   - whether `animateTo` can read current presentation value,
   - whether pointer capture already exists elsewhere.
2. On pointer down/start, store:
   - active pointer id,
   - initial pointer position,
   - item start position,
   - grab offset,
   - short timestamped position history.
3. Use pointer capture once drag intent is confirmed so movement continues outside the original bounds.
4. On pointer move, compute translation in a defined coordinate space, preferably CSS pixels relative to the queue/item container, not raw viewport `clientY` unless the CSS consumer expects viewport coordinates.
5. Ensure one explicit transform owner:
   - either one composed transform string,
   - or nested wrappers separating drag translate from press/settle transforms.
6. On pointer up, compute release velocity from recent samples.
7. Choose the destination slot from a projected endpoint, then call the animation primitive with current position and velocity if supported.
8. If `animateTo` cannot support interruption/presentation-value starts, replace only this local settle path with a minimal internal primitive or project-approved existing helper; do not add a dependency by default.
9. Add Reduced Motion behavior:
   - no elastic overshoot,
   - shorter settle,
   - direct placement or minimal transform,
   - clear selected/dropped state via static styling.

**Hard boundaries**

- Do not change queue ordering semantics, persistence, data loading, or keyboard reordering behavior.
- Do not introduce a gesture library unless existing primitives cannot meet interruption/velocity requirements and the dependency is explicitly approved.
- Do not animate layout properties in the drag hot path.
- Do not allocate large objects or perform expensive DOM reads on every pointer move.
- Do not lock input while the settle animation completes.

**Mechanical checks**

- Type check the component.
- Run lint for event-handler and ref usage.
- Run existing interaction/unit tests if present for queue ordering.
- Add or update tests only if the project already has a nearby pattern for pointer/reorder behavior.

**Runtime / feel checks to perform later**

- Drag slowly, quickly, and outside the original queue bounds.
- Release near a boundary with low and high velocity.
- Interrupt the settle animation by grabbing the item mid-flight.
- Verify no jump on drag start; grab offset is preserved.
- Verify pointer cancellation and lost-capture paths reset state.
- Check behavior in a long queue if that state exists.

**Reduced Motion behavior**

- Drag still tracks directly under user control.
- Release settle uses minimal/no overshoot and short duration.
- Placement confirmation remains visible via position/state styling, not large motion.

**Source-drift stop condition**

Stop before editing if:
- `onPointerMove`, `onPointerUp`, `currentY`, or `animateTo` signatures differ materially from the excerpt;
- `--drag-y` is no longer the visual movement mechanism;
- queue reordering has moved to a shared drag abstraction;
- product/design authority explicitly forbids animated reorder settling.


### Plan 3 — Consolidate Reduced Motion as a component-level contract

**Files / current excerpts**

Correct precedent:

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

Uncovered meaningful motion shown in:

- `src/styles/motion.css` — `.popover`
- `src/components/CommandPalette.tsx` — command palette entry animation
- `src/components/toast.css` — toast entry animation
- `src/components/SortableQueue.tsx` — drag settle animation

**Target behavior**

- Every meaningful motion surface shown has a Reduced Motion branch.
- Reduced Motion does not erase feedback; it removes large spatial travel, long duration, and elastic/vestibular effects.
- The branch is local to each component/style file unless the project already has a centralized motion accessibility layer.

**Project conventions to use**

- Follow the local `@media (prefers-reduced-motion: reduce)` precedent.
- Use existing semantic tokens where possible.
- Preserve visible focus and state feedback.

**Ordered steps**

1. Inventory only the cited files first; do not start a full-codebase sweep unless requested.
2. Add component-local Reduced Motion rules for popover, command palette, and toast.
3. In `SortableQueue.tsx`, route the settle behavior through a reduced-motion condition if one already exists; otherwise add the smallest local check compatible with project patterns.
4. For CSS components, reduce duration and remove/reduce translate/scale.
5. For JS-driven settle, avoid bounce/projection exaggeration under Reduced Motion; keep direct placement or a short settle.
6. Confirm focus-visible styles remain independent of motion changes.

**Hard boundaries**

- Do not globally disable all transitions.
- Do not remove press/focus feedback.
- Do not change color, spacing, or layout tokens unrelated to motion accessibility.
- Do not create a new shared utility unless at least two existing files already use or clearly need the same abstraction.

**Mechanical checks**

- CSS syntax/build check through the project’s normal pipeline.
- Type check if a JS/TS reduced-motion hook or condition is added.
- Lint for unused classes/hooks.

**Runtime / feel checks to perform later**

- Emulate `prefers-reduced-motion: reduce`.
- Repeat command palette open/close, popover open/close, toast entry, and queue settle.
- Confirm feedback remains perceivable without large movement.
- Confirm no focus outline is removed or delayed.

**Reduced Motion behavior**

- Popover/command palette: static final position, short opacity/state transition only.
- Toast: no vertical travel; short fade or immediate final state.
- Sortable queue: direct manipulation unchanged while dragging; settle uses minimal distance/time and no bounce.

**Source-drift stop condition**

Stop before editing if:
- a centralized Reduced Motion system already exists and these components should use it instead;
- `Button.css` no longer contains the cited precedent;
- any cited component has been refactored away;
- the design authority changes the Reduced Motion requirement.

## 4. Recommended execution order

1. **Plan 1 first** — highest breadth-to-risk ratio: removes slow/ease-in/arbitrary/layout-motion patterns from overlays and toasts while aligning with existing tokens.
2. **Plan 3 alongside or immediately after Plan 1** — ensures accessibility parity and prevents token cleanup from leaving Reduced Motion incomplete.
3. **Plan 2 last but before release if queue reordering is core workflow** — direct manipulation needs real interaction validation and should not be guessed from static snippets.

## Explicitly unverified states

- Actual rendered smoothness, frame rate, compositing, layout shift, and paint cost.
- Whether `transition: all` currently animates expensive properties in practice.
- Whether `palette` keyframes include transform, opacity, scale, or other properties.
- Whether `animateTo` supports interruption, current-value starts, velocity, or cancellation.
- Pointer capture, grab offset, keyboard reorder parity, and long-list behavior.
- Actual Reduced Motion behavior outside the shown `Button.css` precedent.
- Focus management and accessibility-tree behavior.
- Browser/device-specific feel.

Basis: evidence-only frontend, accessibility, performance, and motion-planning guardrails were applied; no files were edited and no runtime validation was performed.


## Output C

## 1) Recon summary

- **Stack signals**: React/TSX components plus plain CSS. Motion appears via CSS transitions, CSS keyframes, utility-style arbitrary animation class syntax, and imperative pointer/settle animation code.
- **Where motion lives**:
  - Global tokens and shared selectors: `src/styles/motion.css`
  - Component-local CSS: `src/components/toast.css`, `src/components/Button.css`
  - Component markup/classes: `src/components/CommandPalette.tsx`
  - Gesture code: `src/components/SortableQueue.tsx`
- **Existing conventions**:
  - Tokens exist: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`.
  - Correct local precedent exists in `Button.css`: transform-only transition, tokenized duration/easing, subtle active scale, and a Reduced Motion override that preserves feedback.
- **Product personality**: calm desktop operations console. Motion should be crisp, causal, and quiet; it should not delay keyboard-heavy workflows.
- **Frequency map from evidence/product context**:
  - Very high: command palette, buttons, keyboard-triggered task switching.
  - High: popovers and sortable queue manipulation.
  - Occasional: toasts.
- **Evidence level**: static snippet audit only. No computed styles, runtime behavior, browser/device validation, accessibility-tree review, performance trace, or user test was performed.

## 2) Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose / duration / easing | `src/components/CommandPalette.tsx` | `animate-[palette_420ms_ease-in_both]` is long and ease-in on a keyboard-heavy surface. Static evidence indicates the command palette open state is animated; that conflicts with throughput-first usage. | Remove the open/close animation, or reduce to non-blocking feedback only if required by design. Prefer instant availability and visible focus continuity. |
| 2 | HIGH | Performance / easing / cohesion | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in;`. This is over the existing panel token, starts slowly, and may animate unintended properties. | Replace with explicit `transform`/`opacity` transitions using existing tokens: `var(--duration-panel)` or faster, `var(--ease-responsive)`. |
| 3 | MEDIUM | Physicality / origin | `src/styles/motion.css` | `.popover { transform-origin: center; }` is suspect for trigger-anchored popovers. If this selector is used for true centered modal content, this part is exempt. | Use a trigger-provided origin variable when available; otherwise keep center only for modal-like surfaces. |
| 4 | HIGH | Performance / accessibility | `src/components/toast.css` | Toast entry animates `top` for `500ms ease-in`. `top` is layout-affecting, duration is long for UI feedback, and the excerpt shows no Reduced Motion path. | Animate `transform` + `opacity` instead, shorten to `var(--duration-panel)`, use `var(--ease-responsive)`, and reduce movement under Reduced Motion. |
| 5 | MEDIUM | Gesture performance / interruptibility | `src/components/SortableQueue.tsx` | Pointer move writes `--drag-y` on `queueRef.current`; pointer up settles with fixed `duration: 400`. Static evidence suggests parent-level style invalidation risk and a long fixed settle for a drag interaction. | Drive `transform` directly on the dragged item, settle with a shorter tokenized transform animation or existing spring support, and add Reduced Motion handling. |
| 6 | MEDIUM | Accessibility / cohesion | Multiple excerpts except `Button.css` | The correct Reduced Motion precedent appears only in `Button.css`; other shown motion paths do not show equivalent handling. | Add local Reduced Motion behavior to each affected motion surface while preserving opacity/focus feedback. |

## 3) Implementation-ready plans

### Plan 1 — Tokenize and de-risk CSS popover/toast motion

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

- Popovers feel immediate and causal: explicit `transform`/`opacity` only, no `transition: all`, no `ease-in`.
- Toasts enter without layout animation: `translate3d`/`opacity`, shorter duration, no delayed ease-in start.
- Reduced Motion keeps feedback but removes travel.

**Project conventions**

- Reuse existing tokens:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Follow the local precedent:

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

1. In `src/styles/motion.css`, change `.popover` from `transition: all 360ms ease-in;` to explicit properties:

```css
.popover {
  transform-origin: var(--popover-transform-origin, center);
  transition:
    transform var(--duration-panel) var(--ease-responsive),
    opacity var(--duration-panel) var(--ease-responsive);
}
```

2. If the implementation already exposes a trigger-origin CSS variable for popovers, replace `--popover-transform-origin` with that existing variable. Do not invent a library-specific variable unless it already exists in the codebase.

3. In `src/components/toast.css`, replace `top` keyframes with transform/opacity keyframes:

```css
@keyframes toast-enter {
  from {
    transform: translate3d(0, -8px, 0);
    opacity: 0;
  }
  to {
    transform: translate3d(0, 0, 0);
    opacity: 1;
  }
}

.toast {
  animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;
}
```

4. Add Reduced Motion handling in `src/components/toast.css`:

```css
@media (prefers-reduced-motion: reduce) {
  @keyframes toast-enter {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .toast {
    animation-duration: 160ms;
  }
}
```

5. If redefining `@keyframes toast-enter` inside media queries conflicts with project CSS tooling, use a separate `toast-enter-reduced` keyframe instead.

**Hard boundaries**

- Do not change toast markup, queue logic, command palette logic, or unrelated component styles.
- Do not add dependencies.
- Do not remove focus styles or semantic state attributes.
- Do not convert all durations globally; only touch the shown selectors/keyframes.

**Mechanical checks**

- Search changed files and confirm:
  - No `transition: all` remains on `.popover`.
  - No `ease-in` remains in the edited popover/toast motion.
  - `toast-enter` no longer animates `top`.
  - A `prefers-reduced-motion: reduce` branch exists for toast motion.
- Run the project’s existing lint/type/style checks if available.

**Runtime / feel checks for executor**

- Open a popover slowly via DevTools animation playback if possible; confirm it does not appear to grow from the wrong spatial origin.
- Trigger several toasts; confirm entry starts promptly and does not visibly slide a large distance.
- Toggle Reduced Motion; confirm toast feedback remains visible through opacity but vertical travel is removed.

**Reduced Motion behavior**

- Toast: opacity-only, `160ms`.
- Popover: keep opacity/short transform unless existing design authority requires transform removal; if movement feels spatially distracting, reduce to opacity-only at `160ms`.

**Source-drift stop condition**

- Stop if `.popover` is actually used only for centered modal content, because `transform-origin: center` may be intentional.
- Stop if toast positioning depends on animated `top` for layout rather than visual entry; report the dependency instead of patching around it.

---

### Plan 2 — Remove command palette entrance delay

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

- Command palette content is available immediately when opened.
- Keyboard focus and result continuity do the feedback work; motion must not delay operator throughput.
- No `ease-in` or 420ms entrance animation on the palette wrapper.

**Project conventions**

- Use crisp semantic motion only where it preserves state continuity.
- Existing tokenized precedent favors `160ms` transform feedback for buttons, not long open animations.
- Reduced Motion should preserve feedback rather than remove all state indication.

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, remove the arbitrary animation class from the palette wrapper:

```tsx
export function CommandPalette({ open }: { open: boolean }) {
  return (
    <div data-open={open}>
      <SearchResults />
    </div>
  );
}
```

2. If class composition is required in the real file, remove only `animate-[palette_420ms_ease-in_both]` and preserve unrelated classes.

3. Find the `palette` keyframes definition only if it becomes unused after this change. If it is used nowhere else, remove it in the same change; if it is shared, leave it and report the remaining usage.

4. Ensure focus-visible styling remains intact. Do not replace animation with blur, scale, or delayed opacity.

**Hard boundaries**

- Do not alter `SearchResults`.
- Do not change command execution, search state, keyboard handling, or open/close state ownership.
- Do not add a replacement animation unless product/design explicitly requires one.
- Do not remove `data-open={open}` if CSS or tests depend on it.

**Mechanical checks**

- Confirm `CommandPalette.tsx` no longer contains `animate-[palette_420ms_ease-in_both]`.
- Confirm no new `ease-in` command palette animation was introduced.
- Confirm TypeScript/JSX still parses.
- Run the closest existing typecheck/lint command if available.

**Runtime / feel checks for executor**

- Open the command palette repeatedly from the keyboard; confirm results are visible and usable immediately.
- Rapidly open/close; confirm there is no stale entrance animation continuing after state changes.
- Confirm focus remains visible on the intended input/result.

**Reduced Motion behavior**

- Same as default: no entrance motion.
- Preserve visible focus and open-state feedback through styling, not movement.

**Source-drift stop condition**

- Stop if the actual file no longer uses this class or if palette opening is controlled by a separate animation wrapper not shown here.
- Stop if tests or design comments explicitly document the 420ms animation as a required deliberate behavior; report that conflict.

---

### Plan 3 — Make sortable queue dragging direct, shorter, and reduced-motion aware

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

- During drag, only the dragged item moves via compositor-friendly `transform`.
- Pointer movement does not write a parent CSS variable that can affect the whole queue.
- On release, the item settles to `nearestSlot(currentY)` quickly and causally.
- Reduced Motion shortens or removes travel while preserving state feedback.

**Project conventions**

- Prefer transform-only motion, as shown by `Button.css`.
- Use existing duration/easing tokens where CSS is involved:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Do not introduce new motion libraries.

**Ordered steps**

1. Identify the actual ref for the dragged queue item. If only `queueRef` exists and there is no item-level ref or selector, add the smallest local ref needed for the active dragged element.

2. Replace the parent CSS-variable write:

```tsx
queueRef.current?.style.setProperty("--drag-y", `${event.clientY}px`);
```

with a direct transform write on the dragged item, using a delta rather than raw viewport `clientY` if the surrounding code tracks a drag origin:

```tsx
draggedItemRef.current?.style.setProperty(
  "transform",
  `translate3d(0, ${dragDeltaY}px, 0)`
);
```

3. If the existing code genuinely expects absolute `clientY`, first convert it to local queue/item coordinates. Do not pass raw viewport coordinates into `translateY`.

4. On pointer up, reduce fixed settle duration from `400` to a value no longer than `240ms` if `animateTo` is duration-based:

```tsx
animateTo(nearestSlot(currentY), { duration: 240 });
```

5. If `animateTo` already supports spring-style options and carries velocity, prefer the existing spring API with subtle bounce. Do not add a dependency to get spring behavior.

6. Add Reduced Motion branching using the project’s existing preference hook/helper if one exists. If none exists, use `window.matchMedia("(prefers-reduced-motion: reduce)")` behind a client-side guard in this component’s existing browser-only event path.

7. Under Reduced Motion, snap or use a very short settle, for example:

```tsx
animateTo(nearestSlot(currentY), { duration: 80 });
```

and avoid decorative overshoot/bounce.

**Hard boundaries**

- Do not rewrite sorting algorithms.
- Do not change queue data shape, item identity, persistence, or nearest-slot calculation.
- Do not add dependencies.
- Do not introduce global CSS variables for per-frame drag position.
- Do not remove keyboard accessibility or focus indication for sortable items.

**Mechanical checks**

- Confirm `onPointerMove` no longer writes `--drag-y` to `queueRef.current`.
- Confirm drag movement is applied as `transform` on the active item.
- Confirm release duration is not `400`.
- Confirm a Reduced Motion branch exists for release animation.
- Run the project’s closest typecheck/lint command if available.

**Runtime / feel checks for executor**

- Drag an item slowly; confirm the item tracks the pointer without visible offset jumps.
- Release near two slots; confirm it settles to the nearest slot without a long glide.
- Interrupt with rapid drags; confirm motion retargets cleanly and does not restart from an unrelated position.
- Toggle Reduced Motion; confirm the queue still communicates the final placement but avoids long travel or bounce.

**Reduced Motion behavior**

- Pointer tracking remains direct because it is user-controlled.
- Release animation shortens to `80ms` or snaps immediately if even short travel is distracting.
- Preserve focus/selection/placement feedback.

**Source-drift stop condition**

- Stop if `animateTo` is not a visual animation helper or if it does not target the dragged item’s transform.
- Stop if the queue intentionally uses `--drag-y` for multiple coordinated item transforms; report the dependency and propose a larger coordinated refactor instead.

## 4) Recommended execution order

1. **Plan 2 — Command palette**: highest throughput impact, smallest surface.
2. **Plan 1 — Popover/toast CSS**: removes broad `transition: all`, layout animation, long ease-in timing, and adds Reduced Motion coverage.
3. **Plan 3 — Sortable queue**: higher interaction risk; do after the simpler token/CSS corrections.

## Explicitly unverified states

- Actual package scripts, lint/typecheck commands, and CSS tooling behavior.
- Whether `.popover` is ever used for centered modal-like content.
- Whether trigger-origin CSS variables already exist.
- Whether `palette` keyframes are shared elsewhere.
- Whether `animateTo` supports easing, springs, velocity, cancellation, or Reduced Motion hooks.
- Actual computed durations/easings after cascade.
- Runtime feel, frame pacing, accessibility tree, keyboard focus behavior, and device/browser-specific performance.

Governance applied: frontend quality, reduced-motion/accessibility, and evidence-limited delivery discipline.
