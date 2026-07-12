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

Applied quality and frontend guardrails; no files were edited and no runtime/browser validation was performed.

## 1. Recon summary

**Stack signals**
- CSS modules/global CSS plus TSX components.
- Utility-style arbitrary animation class appears in `CommandPalette.tsx`.
- Motion tokens exist in `src/styles/motion.css`.
- Component-local CSS exists in `Button.css` and `toast.css`.

**Where motion lives**
- Global semantic tokens: `src/styles/motion.css`
- Component CSS: `src/components/toast.css`, `src/components/Button.css`
- Inline utility animation: `src/components/CommandPalette.tsx`
- Imperative animation: `src/components/SortableQueue.tsx`

**Existing conventions**
- Tokenized duration/easing precedent:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Correct local precedent:
  - Button uses `transform`
  - Button uses semantic tokens
  - Button has a Reduced Motion path preserving feedback via shorter duration

**Product personality**
- Calm desktop operations console.
- Keyboard-heavy, throughout-the-day use.
- Motion should clarify cause/effect and continuity without adding wait time or visual noise.
- Crisp, responsive, low-amplitude transitions fit better than slow entrance effects.

**Frequency map from static evidence**
- High frequency: button press feedback, command palette open/close, popovers, sortable queue drag/snap.
- Medium frequency: toast entry, depending on notification volume.
- Potentially continuous: sortable queue pointer movement.
- State-continuity critical: command palette, popovers, sortable queue.
- Feedback critical: button active, toast entry.

**Evidence level**
- Static source excerpts only.
- No runtime, computed-style, performance trace, screen recording, accessibility-tree, device, or user-test evidence.
- Findings below are source-evidence-based risks, not confirmed runtime failures.

---

## 2. Vetted priority table

| Priority | Surface | Finding | Evidence | Risk | Intended fix |
|---:|---|---|---|---|---|
| P0 | Shared motion conventions | Motion tokens exist but are not consistently used | `motion.css` defines tokens; palette/toast/sort hard-code timing/easing | Inconsistent feel and harder Reduced Motion coverage | Route all common UI motion through semantic tokens |
| P0 | Command palette | Hard-coded `420ms ease-in` arbitrary animation | `className="animate-[palette_420ms_ease-in_both]"` | High-frequency keyboard surface may feel delayed; no shown Reduced Motion path | Use panel token duration/easing; add reduced path that preserves open/close feedback |
| P1 | Popover | `transition: all 360ms ease-in` | `.popover { transition: all 360ms ease-in; }` | Unbounded property animation; duration/easing conflicts with token convention | Transition only `opacity, transform` with existing tokens |
| P1 | Toast | Animates `top` for `500ms ease-in` | `@keyframes toast-enter { from { top: -24px; ... } }` | Layout-affecting property and slow entrance on operational feedback | Use `transform` + `opacity`, shorter tokenized duration |
| P1 | Sortable queue | Drag/snap timing is hard-coded and imperative path lacks visible reduced-motion branch in excerpt | `setProperty("--drag-y", ...)`; `animateTo(..., { duration: 400 })` | Continuous interaction could feel laggy or over-animated; accessibility behavior unknown | Tokenize snap, add reduced snap duration/behavior, verify transform-only application |
| P2 | Reduced Motion coverage | Only button excerpt shows Reduced Motion precedent | Button has `@media`; other snippets do not | Users requesting reduced motion may still get full entrance/drag animations | Add per-surface reduced branches that shorten/remove travel while preserving feedback |

---

## 3. Implementation plans

### Plan A — Consolidate semantic motion primitives and fix popover baseline

**Exact file path/current excerpt**

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
- Popovers feel immediate but not abrupt.
- Only composited properties animate: `opacity` and `transform`.
- Timing aligns with existing semantic tokens.
- Reduced Motion preserves state feedback with shortened duration and minimal/no travel.

**Project conventions to preserve**
- Keep existing token names unless real files show a stronger naming convention.
- Match the local button precedent:
  - transform-based motion
  - tokenized duration/easing
  - Reduced Motion branch that shortens duration rather than removing feedback entirely

**Ordered steps**
1. Open the real `src/styles/motion.css` before editing.
2. Confirm the shown tokens still exist and check for additional motion tokens nearby.
3. Replace popover `transition: all 360ms ease-in` with explicit properties:
   - `opacity`
   - `transform`
4. Use existing tokens:
   - likely `var(--duration-panel)` for open/close panel-like movement
   - `var(--ease-responsive)` for responsive easing
5. Keep `transform-origin: center` unless actual popover placement code indicates a better contextual origin.
6. Add or extend a `@media (prefers-reduced-motion: reduce)` block for `.popover`.
7. In reduced mode, shorten duration, avoid large scale/translate deltas if present elsewhere, and preserve opacity/state feedback.
8. Do not introduce new global motion tokens unless at least two modified surfaces need the same missing semantic.

**Hard boundaries**
- Do not change popover layout, positioning, z-index, focus handling, or open/closed state logic.
- Do not convert global CSS architecture.
- Do not use `transition: all`.
- Do not add decorative bounce, spring, blur, or overshoot.

**Mechanical checks**
- Search for `.popover` definitions/usages before changing to avoid conflicting transitions.
- Check CSS syntax.
- Run the closest available static checks after implementation, such as lint/typecheck/build if configured.
- Verify no new hard-coded `360ms`, `ease-in`, or `transition: all` remains for `.popover`.

**Runtime/feel checks to perform later**
- Open/close popovers from mouse and keyboard.
- Confirm focus ring remains visible throughout transition.
- Confirm no delayed pointer/keyboard usability while the popover is entering.
- Confirm the transition communicates continuity without drawing attention.

**Reduced Motion behavior**
- Recommended: `transition-duration: 80ms` or nearest existing reduced token if present.
- Keep opacity feedback.
- Avoid spatial travel if actual open/close styles include translate/scale.

**Source-drift stop condition**
- Stop and reassess if `motion.css` already contains newer motion tokens, a broader animation system, or `.popover` is no longer defined as shown.

---

### Plan B — Tokenize high-frequency entrances: command palette and toast

**Exact file paths/current excerpts**

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
- Command palette opens/closes crisply for keyboard-heavy use.
- Toasts enter clearly without slow drift.
- Both use semantic token timing/easing.
- Toast motion uses transform/opacity, not `top`.
- Reduced Motion keeps feedback but removes or minimizes travel.

**Project conventions to preserve**
- Use `--duration-panel` for panel-like command palette movement.
- Use `--duration-fast` or a nearby existing feedback token for toast entry if present.
- Use `--ease-responsive`.
- Preserve `data-open={open}` as a useful state hook.
- Keep existing component structure unless real files require a local CSS class.

**Ordered steps**
1. Inspect real `CommandPalette.tsx` imports and styling conventions.
2. Find where `palette` keyframes are defined, if at all.
3. Replace the arbitrary hard-coded animation class with a named class or existing project motion utility that can use CSS variables.
4. Define palette motion using `opacity` plus small `transform` only, for example a short translate/scale that reinforces origin without feeling theatrical.
5. Wire open/closed styles to `data-open` if the component remains mounted.
6. Inspect real `toast.css` for other toast states before changing.
7. Rewrite `toast-enter` to use `transform: translateY(...)` and `opacity`.
8. Replace `500ms ease-in` with semantic duration/easing.
9. Add Reduced Motion branches for both surfaces.
10. Keep visual/state semantics intact: command palette still renders `SearchResults`; toast still enters and remains visible.

**Hard boundaries**
- Do not change search behavior, command execution, filtering, selection, or keyboard navigation.
- Do not alter toast queueing, dismissal timing, ARIA/live-region behavior, or notification content.
- Do not introduce extra wrapper elements unless required by current styling.
- Do not add delayed animations that block interaction.
- Do not remove feedback entirely in Reduced Motion.

**Mechanical checks**
- Search for `animate-[palette`, `@keyframes palette`, and `toast-enter`.
- Ensure no remaining hard-coded `420ms ease-in` or `500ms ease-in` on these surfaces.
- Ensure keyframes animate only `opacity` and `transform`.
- Run typecheck/lint/build if available.
- Confirm CSS selectors match actual mounted class names.

**Runtime/feel checks to perform later**
- Open command palette repeatedly via keyboard shortcut.
- Type immediately after opening; confirm perceived readiness is not delayed by animation.
- Move through search results with keyboard while open.
- Trigger one and multiple toasts; confirm entry is noticeable but not attention-grabbing.
- Confirm motion does not obscure text legibility.

**Reduced Motion behavior**
- Command palette:
  - Use near-instant opacity feedback, around 80ms if consistent with button precedent.
  - Remove scale/translate or reduce to negligible distance.
- Toast:
  - Keep opacity transition or very short transform.
  - Avoid vertical travel from `-24px`.
  - Preserve arrival feedback so notifications do not appear without context.

**Source-drift stop condition**
- Stop and reassess if the real command palette uses a transition library, exit animations, portal lifecycle, or already has centralized animation definitions not visible in the excerpt.
- Stop if toast positioning depends on animated `top` for layout correctness; first identify the layout contract.

---

### Plan C — Make sortable queue drag/snap motion responsive and accessible

**Exact file path/current excerpt**

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
- Drag follows pointer directly without decorative lag.
- Snap to slot communicates causality and final placement.
- Snap timing is shorter and tokenized.
- Reduced Motion preserves final-placement feedback while minimizing animated travel.
- Pointer-move path avoids unnecessary React renders and avoids layout-dependent animation where possible.

**Project conventions to preserve**
- Imperative pointer update is acceptable for continuous drag if it avoids React re-render churn.
- Align snap duration with existing tokens:
  - likely `--duration-panel` if slot movement is panel-like
  - shorter if actual distance is small
- Match responsive easing convention.

**Ordered steps**
1. Inspect full `SortableQueue.tsx` before editing.
2. Identify:
   - how `--drag-y` is consumed in CSS/style
   - whether it drives `transform`, `top`, layout, or calculations
   - where `currentY` is updated
   - what `animateTo` implementation accepts
3. If `--drag-y` is consumed by transform, keep the pointer path but consider requestAnimationFrame coalescing only if current code writes more than necessary.
4. If `--drag-y` is consumed by layout properties, migrate consumption to transform-based movement before tuning duration.
5. Replace hard-coded `duration: 400` with a semantic duration or local constant derived from motion tokens/config.
6. Add Reduced Motion handling at the snap call site or inside `animateTo`, whichever is the narrower reusable boundary.
7. Ensure pointer-up always lands on `nearestSlot(currentY)` even when animation is shortened.
8. Preserve drag state cleanup and pointer capture/release behavior if present.

**Hard boundaries**
- Do not change queue ordering rules, nearest-slot calculation, persistence, or business state.
- Do not introduce React state updates on every pointer move unless already proven cheap.
- Do not add physics/spring behavior unless the project already uses it.
- Do not make Reduced Motion skip the final state update.
- Do not modify unrelated sortable/list components without evidence of shared code.

**Mechanical checks**
- Search for `--drag-y`, `animateTo`, `nearestSlot`, and `prefers-reduced-motion`.
- Confirm TypeScript types for any new duration/reduced-motion helper.
- Confirm pointer handlers still remove listeners/cleanup as before.
- Run typecheck and any component/unit tests if available.
- Confirm no hard-coded `duration: 400` remains for this snap path unless retained with documented reason in code.

**Runtime/feel checks to perform later**
- Drag slowly and quickly; item should track the pointer without visible lag.
- Release near slot boundaries; snap should clarify final placement.
- Drag with keyboard alternative if one exists; confirm focus and order feedback remain clear.
- Test long queues and rapid repeated drags for perceived responsiveness.
- Check Reduced Motion setting: final placement should be immediate or near-immediate, not absent.

**Reduced Motion behavior**
- On release, use immediate placement or very short duration, around 80ms if matching existing button precedent.
- Avoid long spatial interpolation.
- Preserve any visual confirmation of drop/final state through focus, outline, opacity, or short transform feedback.

**Source-drift stop condition**
- Stop and reassess if `animateTo` is a shared abstraction with existing global defaults, if queue movement already uses a motion library, or if `--drag-y` no longer controls visual position as implied.

---

## 4. Recommended execution order

1. **Plan A first** — establish safe global motion baseline and remove `transition: all` from popovers.
2. **Plan B second** — fix the most visible high-frequency entrance patterns: command palette and toast.
3. **Plan C third** — tune sortable queue after inspecting the full imperative drag path, because it has the highest interaction complexity.

## Explicitly unverified states

- Actual computed durations/easings in browser.
- Whether `palette` keyframes exist and what they animate.
- Whether `.popover` has separate open/closed transform or opacity rules.
- Whether toast layout depends on `top`.
- Whether `--drag-y` is consumed by `transform`, `top`, or another property.
- Whether `animateTo` is local or shared.
- Whether Reduced Motion is already centralized elsewhere.
- Keyboard focus behavior, screen-reader behavior, and visual focus persistence.
- Runtime performance, layout/recalc cost, frame pacing, and device-specific feel.


## Output B

## 1. Recon summary

**Diagnosis:** the snippets show a calm, utility-oriented console with solid token precedent, but several high-frequency or repeated motions use slow `ease-in`, broad property ownership, layout-property animation, or incomplete direct-manipulation evidence.

- **Stack signals:** web frontend with TSX components, CSS modules/global CSS, Tailwind-style arbitrary animation class, imperative pointer handling, and a JS `animateTo(...)` primitive.
- **Where motion lives:**  
  `src/styles/motion.css` tokens + global `.popover`; `src/components/CommandPalette.tsx` class-level animation; `src/components/toast.css` keyframes; `src/components/SortableQueue.tsx` pointer/settle logic; `src/components/Button.css` local precedent.
- **Existing conventions:** semantic durations `--duration-fast: 160ms`, `--duration-panel: 240ms`; responsive ease token `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`; Reduced Motion precedent keeps feedback but shortens duration to `80ms`; button uses explicit `transform` transition only.
- **Product personality:** calm desktop operations console; motion should be crisp, causal, low-drama, and throughput-preserving.
- **Frequency map:**  
  High: command palette, buttons, sortable queue.  
  Common: popovers.  
  Occasional but repeated: toasts.  
  Direct manipulation: sortable queue drag/snap.
- **Evidence level:** static snippets only. No runtime, computed style, animation trace, screen recording, accessibility tree, or user testing was performed.

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
| --- | --- | --- | --- | --- |
| P1 | Static | `src/components/CommandPalette.tsx` | High-frequency keyboard surface uses `animate-[palette_420ms_ease-in_both]`: slow duration, delayed-start easing, arbitrary value, and no shown Reduced Motion branch. | Replace with tokenized, explicit opacity/transform transition around `160–240ms` using `--ease-responsive`; Reduced Motion keeps feedback with opacity/static state and short duration. |
| P1 | Static | `src/components/SortableQueue.tsx` | Direct manipulation excerpt shows raw `clientY` CSS-var updates and fixed `animateTo(..., { duration: 400 })`; no evidence of grab offset, pointer capture, velocity handoff, projected snap, or interruption from presentation value. | Audit full component, then implement 1:1 local-coordinate drag with capture/offset/sampled velocity and token/spring-based settle; Reduced Motion removes overshoot/long travel. |
| P2 | Static | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in` and `transform-origin: center`; broad ownership and delayed response are mismatched for common anchored overlays. | Limit to `opacity, transform`; use `--duration-fast` or `--duration-panel` + `--ease-responsive`; use trigger-aware origin unless confirmed centered. |
| P2 | Static | `src/components/toast.css` | Toast enters by animating `top` for `500ms ease-in`; this is a layout-property animation risk and slower than existing panel token. | Animate `transform` + `opacity` instead; use `--duration-panel` + `--ease-responsive`; Reduced Motion removes vertical travel while preserving appearance feedback. |
| P3 | Static | Cross-snippet | Motion vocabulary is split between semantic tokens, arbitrary Tailwind animation, raw milliseconds, and component keyframes. | During the fixes above, normalize to existing semantic tokens rather than adding a new motion system. |
| Positive precedent | Static | `src/components/Button.css` | Button already demonstrates explicit property transition, semantic token use, and Reduced Motion preservation. | Treat as local pattern for similar micro-feedback. |

## 3. Implementation plans

### Plan A — Tokenize and shorten overlay motion

**Files/current excerpts**

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

**Target behavior**

- Popovers and command palette respond immediately and settle calmly.
- Use existing tokens: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
- Animate only `opacity` and `transform`.
- Command palette, as a keyboard-heavy surface, should not spend `420ms` entering.
- Reduced Motion preserves open/closed feedback without spatial travel.

**Project conventions**

- Follow the button precedent: explicit animated property, semantic duration token, Reduced Motion override.
- Do not introduce new animation libraries or new global timing vocabulary unless repeated usage proves it necessary.

**Ordered steps**

1. In `src/styles/motion.css`, change `.popover` from `transition: all 360ms ease-in` to explicit properties, for example:
   ```css
   transition:
     opacity var(--duration-fast) var(--ease-responsive),
     transform var(--duration-fast) var(--ease-responsive);
   ```
2. Re-evaluate `transform-origin: center` before keeping it.  
   - If the popover is anchored to a trigger, set origin from existing placement data/custom properties if available.  
   - Keep `center` only for truly centered overlays.
3. Replace `CommandPalette.tsx` arbitrary animation class with a named class or existing utility pattern that uses:
   - normal motion: `opacity` plus very small `transform` delta, `160–240ms`, `--ease-responsive`;
   - no long keyframe restart for repeated open/close.
4. Add or reuse a Reduced Motion media block:
   ```css
   @media (prefers-reduced-motion: reduce) {
     .popover,
     .command-palette-motion {
       transition-duration: 80ms;
       transform: none;
     }
   }
   ```
   Use the actual class name selected in step 3.
5. Confirm focus styles remain visible and are not hidden behind delayed animation.

**Hard boundaries**

- Do not change `SearchResults` behavior, search data loading, command execution, keyboard bindings, or focus ownership.
- Do not add dependencies.
- Do not globally redefine existing tokens without a broader design-system decision.

**Mechanical checks**

- Run the project’s existing type check for `CommandPalette.tsx`.
- Run the existing CSS/lint/build gate that covers `src/styles/motion.css`.
- Search for the old arbitrary class and confirm no stale `palette_420ms_ease-in_both` usage remains unless intentionally documented.

**Runtime/feel checks to perform later**

- Open/close command palette repeatedly by keyboard.
- Interrupt open with close and close with open.
- Verify no visible focus loss and no delayed input readiness.
- Check popover open/close from representative trigger positions.

**Reduced Motion behavior**

- No slide/scale travel.
- Opacity or instant state change still confirms open/closed state.
- Focus indicator remains visible.

**Source-drift stop condition**

Stop before editing if `palette` keyframes are defined elsewhere with behavior not shown here, if `.popover` is also used for centered modal content, or if `DESIGN.md`/tokens have changed materially from the provided excerpt.

---

### Plan B — Convert toast entry from layout motion to transform motion

**Files/current excerpt**

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
- Motion communicates arrival but does not distract operators.
- Use `--duration-panel: 240ms` and `--ease-responsive`.
- Reduced Motion removes vertical travel while preserving feedback.

**Project conventions**

- Use semantic duration/easing tokens from `src/styles/motion.css`.
- Match the button precedent: explicit motion property and Reduced Motion branch.
- Keep toast stacking/positioning logic separate from entry animation.

**Ordered steps**

1. Keep layout position as static CSS outside the keyframe, if needed:
   ```css
   .toast {
     top: 0;
   }
   ```
   Only do this if the existing layout requires `top`.
2. Replace keyframes with transform/opacity:
   ```css
   @keyframes toast-enter {
     from { transform: translateY(-8px); opacity: 0; }
     to { transform: translateY(0); opacity: 1; }
   }
   ```
3. Change animation timing:
   ```css
   .toast {
     animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;
   }
   ```
4. Add Reduced Motion:
   ```css
   @media (prefers-reduced-motion: reduce) {
     @keyframes toast-enter {
       from { opacity: 0; transform: none; }
       to { opacity: 1; transform: none; }
     }

     .toast {
       animation-duration: 80ms;
     }
   }
   ```
5. If exit animation exists elsewhere, align it to the same property set; do not create an enter/exit mismatch.

**Hard boundaries**

- Do not alter toast queueing, timeout duration, ARIA/live-region behavior, severity styling, or dismissal behavior.
- Do not animate height, margin, top, or left for the entry effect.
- Do not claim performance improvement without a later trace; this plan only removes a known static risk.

**Mechanical checks**

- Run CSS lint/build gate.
- Search for `toast-enter` references and confirm all consumers still receive the expected animation name.
- Verify no duplicate `@keyframes toast-enter` definitions conflict.

**Runtime/feel checks to perform later**

- Trigger one toast, then several in quick succession.
- Confirm entry feels prompt and non-blocking.
- Confirm stacking does not jump when multiple toasts appear.
- Confirm keyboard focus is not moved unexpectedly.

**Reduced Motion behavior**

- Toast still appears/fades in.
- No vertical movement.
- Duration shortened to match existing local precedent.

**Source-drift stop condition**

Stop before editing if `top` is dynamically used for stacked toast positioning in a way that the keyframe intentionally coordinates, if there is already a separate Reduced Motion toast branch, or if token names differ from the provided excerpt.

---

### Plan C — Make sortable queue drag and snap physically accountable

**Files/current excerpt**

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

- Dragged item tracks the pointer in the correct local coordinate space.
- The item does not jump on grab.
- Drag remains tracked after pointer leaves the original bounds.
- Release chooses a slot from current position plus measured velocity/projection, not only a stale logical value.
- Settle motion is interruptible from current presentation value.
- Reduced Motion keeps direct manipulation but removes overshoot and long animated travel.

**Project conventions**

- Preserve throughput for operators; avoid decorative bounce.
- Prefer transform-based movement and direct style writes for pointer-move hot path.
- Use existing `--duration-fast`, `--duration-panel`, and `--ease-responsive` if the existing `animateTo` primitive is duration-based.
- Use existing animation primitive if it supports springs/current-value/velocity; do not add a heavy dependency by default.

**Ordered steps**

1. Inspect the full component before editing:
   - pointer down handler;
   - CSS consuming `--drag-y`;
   - definition/import of `animateTo`;
   - how `currentY` is updated;
   - list size and render path.
2. On pointer down, record:
   - active `pointerId`;
   - queue/container bounding rect;
   - item starting presentation Y;
   - grab offset between pointer and item origin;
   - recent `{time, y}` samples.
   Call `setPointerCapture(pointerId)` if not already present.
3. On pointer move:
   - ignore non-active pointers;
   - compute local pointer Y, not raw viewport `clientY`;
   - subtract grab offset;
   - write a transform-owned value, for example `--drag-y: <localY>px`;
   - update velocity samples without React state on every frame.
4. On pointer up/cancel:
   - release pointer capture when held;
   - compute velocity in CSS px/s from recent samples;
   - compute a projected endpoint and choose `nearestSlot(projectedEndpoint)`;
   - start settle from the current presentation value.
5. Replace fixed `400ms` settle:
   - if `animateTo` supports spring/velocity: use critically damped or near-critically damped settle with supplied velocity and no decorative bounce;
   - if it only supports duration/easing: use `var(--duration-panel)`/`240ms` as the initial cap and document that true velocity handoff requires the existing primitive to support it.
6. Ensure transform ownership is explicit if press feedback and drag both use `transform`; use wrapper layers or a composed transform so one does not overwrite the other.
7. Add Reduced Motion handling:
   - direct drag remains 1:1;
   - release snap is instant or `80ms`;
   - no overshoot, elastic travel, or long glide.

**Hard boundaries**

- Do not rewrite queue ordering data structures unless the current drag state requires it.
- Do not add a new animation package unless the existing primitive cannot read current value or accept velocity and the team approves the dependency.
- Do not move sorting, persistence, or revenue/support workflow logic.
- Do not use React state for every pointer-move frame unless the current architecture already proves it is cheap.

**Mechanical checks**

- Run TypeScript check covering `SortableQueue.tsx`.
- Run lint for pointer event typing and hook dependency correctness.
- Run existing unit/component tests for queue ordering if present.
- Search for all `--drag-y` consumers and confirm transform ownership is clear.

**Runtime/feel checks to perform later**

- Grab item near top, center, and bottom; verify no jump.
- Drag outside queue bounds; verify tracking continues until release/cancel.
- Release slowly near a boundary and quickly with a flick; verify projected slot selection feels causal.
- Interrupt a settling item by grabbing again; verify no visual jump.
- Test with keyboard reorder path if one exists; it must remain usable.

**Reduced Motion behavior**

- Drag still directly follows pointer.
- Snap has no overshoot and uses instant or very short settle.
- Static slot highlight or clear final placement preserves feedback.

**Source-drift stop condition**

Stop before editing if `animateTo` already handles current-value interruption and velocity under a different API, if `--drag-y` is intentionally viewport-based in CSS, if pointer capture/grab offset already exists outside the excerpt, or if the queue is virtualized in a way that changes coordinate ownership.

## 4. Recommended execution order

1. **Plan A** first: fixes high-frequency keyboard overlay and common popover vocabulary while reinforcing tokens.
2. **Plan B** second: small, isolated, high-confidence conversion from layout motion to transform/opacity.
3. **Plan C** third: highest interaction complexity; requires full-source inspection and runtime feel validation.

## Explicitly unverified states

- Actual rendered smoothness, frame rate, compositing, and layout cost.
- Whether popovers are anchored or centered in real usage.
- Whether `palette` keyframes exist elsewhere and what properties they animate.
- Whether command palette remains input-ready during animation.
- Whether toast stacking uses `top` dynamically.
- Whether `SortableQueue` already implements pointer capture, grab offset, velocity, cancellation, or keyboard reordering outside the excerpt.
- Actual Reduced Motion behavior in browser settings.
- Accessibility-tree behavior, focus order, screen-reader announcement timing, and live-region behavior.


## Output C

## 1. Recon summary

- **Stack signals**: React/TSX components, plain CSS, CSS custom-property motion tokens, utility-class animation syntax in `CommandPalette`.
- **Where motion lives**: `src/styles/motion.css`, component CSS files, inline/utility animation classes, and pointer gesture handlers.
- **Existing conventions**:
  - Tokens: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`.
  - Correct local precedent: button animates only `transform`, uses semantic tokens, and keeps a reduced-motion path with shortened feedback.
- **Product personality**: calm desktop operations console; motion should be crisp, causal, and non-decorative.
- **Frequency map, inferred from supplied context only**:
  - Very high: command palette, keyboard-driven actions, buttons.
  - Medium/high: sortable queue drag/reorder, popovers.
  - Occasional: toasts.
- **Evidence level**: static snippets only. No runtime, computed-style, trace, browser, device, accessibility-tree, or user validation was performed.

## 2. Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---|---|---|---|---|
| 1 | HIGH | Purpose, frequency, easing | `src/components/CommandPalette.tsx` | Command palette uses `animate-[palette_420ms_ease-in_both]`; for a keyboard-heavy surface this is likely a high-frequency action, and the 420ms `ease-in` entrance works against throughput. | Remove the palette animation class; preserve open state and focus behavior. |
| 2 | HIGH | Performance, easing, cohesion | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in`; this can animate unintended properties, exceeds the existing panel token, and duplicates non-token timing/easing. | Limit transition to `transform, opacity`; use `--duration-panel` and `--ease-responsive`. |
| 3 | HIGH | Performance, easing, accessibility | `src/components/toast.css` | Toast entrance animates `top` from `-24px` to `0` over `500ms ease-in`; `top` is layout-affecting, duration is long for operational feedback, and no reduced-motion branch is shown. | Animate `transform` + `opacity`, use existing tokens, add reduced-motion fade-only behavior. |
| 4 | MEDIUM | Gesture performance, interruptibility | `src/components/SortableQueue.tsx` | Pointer move writes `--drag-y` on `queueRef`; release uses fixed `duration: 400`. Static evidence cannot prove jank, but this pattern risks broad style recalculation and non-velocity-aware settling. | Move drag transform updates to the dragged item where possible; use shorter/spring-like settle behavior only if supported by existing helper. |
| 5 | MEDIUM | Accessibility | Multiple snippets | Reduced-motion handling is visible only in `Button.css`; palette, popover, toast, and queue excerpts do not show equivalent paths. | Add movement-reduced but feedback-preserving branches per component. |
| 6 | MEDIUM | Token cohesion | Multiple snippets | Durations/easings are hand-authored as `360ms`, `420ms`, `500ms`, and `ease-in` despite existing semantic tokens. | Standardize operational UI motion on existing duration/easing tokens unless a local reason is documented. |

---

## 3. Implementation-ready plans

### Plan 1 — Remove command-palette entrance animation

**Files/current excerpt**

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

- Opening/closing the command palette should be immediate from the user’s perspective.
- Preserve `data-open={open}` and all existing children.
- Do not add replacement movement, fade, scale, delay, or stagger.
- Reduced Motion behavior is identical to default because the high-frequency animation is removed.

**Project conventions**

- Follow the calm operations-console direction: motion only when it protects causality.
- Reuse the local precedent that high-frequency feedback should be short and purposeful; do not introduce a parallel animation token here.

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, remove only the arbitrary animation class.
2. If the actual file contains additional non-motion classes not shown in the excerpt, preserve them and remove only `animate-[palette_420ms_ease-in_both]`.
3. Preferred target for the provided excerpt:

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

- Do not change `SearchResults`.
- Do not change command filtering, focus management, keyboard shortcuts, or open-state logic.
- Do not replace this with a shorter animation unless product/design explicitly asks for one.
- Do not add dependencies.

**Mechanical checks**

- Search for `palette_420ms_ease-in_both`; it should no longer appear in `CommandPalette`.
- Search for `animate-[palette` to confirm no stale utility animation remains unless another component intentionally uses it.
- Run the project’s existing typecheck/lint command if available.

**Runtime/feel checks for executor**

- Open the command palette repeatedly from the keyboard.
- Confirm it appears without perceptible delay.
- Confirm focus still lands where it did before.
- Confirm closing/reopening rapidly does not show a restarted entrance animation.

**Reduced Motion behavior**

- No separate branch required for this component after removal.
- Do not remove any existing focus, active, or selection feedback.

**Source-drift stop condition**

- If `className` contains layout, visibility, or positioning classes beyond the shown animation class, stop before deleting the whole attribute; remove only the animation token and report the drift.

---

### Plan 2 — Normalize popover motion to explicit tokenized properties

**Files/current excerpt**

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

- Popover motion should be crisp and bounded to compositor-friendly properties.
- Use existing semantic tokens.
- Avoid `transition: all`.
- Avoid `ease-in`.
- Do not assert a trigger-origin fix unless the actual component/library exposes a transform-origin variable.

**Project conventions**

- Use existing tokens from `:root`.
- Match the button precedent: transition a specific transform-related property using tokenized duration/easing.

**Ordered steps**

1. In `src/styles/motion.css`, replace the `.popover` transition with explicit properties:

```css
.popover {
  transform-origin: center;
  transition:
    transform var(--duration-panel) var(--ease-responsive),
    opacity var(--duration-panel) var(--ease-responsive);
}
```

2. Do not add new duration/easing tokens for this change.
3. Inspect the actual popover implementation only enough to determine whether `.popover` is centered or trigger-anchored.
4. If and only if the implementation already exposes a safe transform-origin custom property, update `transform-origin` to use it with a center fallback, for example:

```css
transform-origin: var(--transform-origin, center);
```

5. If no such variable exists in the actual code, keep `transform-origin: center;` and leave origin refinement for a separate task.

**Hard boundaries**

- Do not change popover markup.
- Do not change positioning logic.
- Do not alter z-index, focus trap, dismissal, keyboard behavior, or portal behavior.
- Do not introduce library-specific variables unless they already exist in this project’s actual code.

**Mechanical checks**

- Search `src/styles/motion.css` for `transition: all`; the `.popover` rule should not use it.
- Search the edited rule for `ease-in`; it should use `var(--ease-responsive)`.
- Confirm `--duration-panel` and `--ease-responsive` remain defined in `:root`.

**Runtime/feel checks for executor**

- Open and close a popover at normal speed.
- In slow animation playback, confirm only opacity/transform animate.
- Confirm the popover does not feel delayed at the start of opening.
- If origin was changed, confirm it visually expands from the correct anchor; if that cannot be verified, revert the origin part only.

**Reduced Motion behavior**

Add a reduced-motion branch if no broader global branch already covers `.popover`:

```css
@media (prefers-reduced-motion: reduce) {
  .popover {
    transition:
      opacity 80ms var(--ease-responsive),
      transform 80ms var(--ease-responsive);
  }
}
```

- Keep feedback present.
- Do not add large movement in reduced motion.

**Source-drift stop condition**

- If `.popover` has state selectors, data attributes, or multiple transition definitions not shown here, stop and report before replacing the rule wholesale.

---

### Plan 3 — Make toast entrance compositor-friendly and reduced-motion safe

**Files/current excerpt**

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

- Toasts should enter quickly without animating layout-affecting properties.
- Use transform and opacity only.
- Use existing motion tokens.
- Reduced Motion keeps opacity feedback but removes vertical travel.

**Project conventions**

- Use existing `--duration-panel` and `--ease-responsive`.
- Follow the button precedent: preserve feedback under reduced motion instead of disabling all response.

**Ordered steps**

1. Replace the keyframes so they animate `transform` and `opacity`, not `top`:

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
```

2. Replace the `.toast` animation timing:

```css
.toast {
  animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;
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
    animation: toast-enter-reduced 80ms var(--ease-responsive) forwards;
  }
}
```

4. If the actual `.toast` rule already sets `transform` for positioning, stop and report instead of overwriting it; the executor must compose transforms safely.

**Hard boundaries**

- Do not change toast creation/removal timing.
- Do not change stacking, timeout, ARIA/live-region behavior, or message content.
- Do not animate `top`, `left`, `right`, `bottom`, `height`, `margin`, or `padding`.
- Do not add new dependencies.

**Mechanical checks**

- Search `src/components/toast.css` for `top: -24px` inside keyframes; it should be gone.
- Search the toast animation for `500ms` and `ease-in`; both should be gone.
- Confirm `prefers-reduced-motion` exists in `toast.css`.

**Runtime/feel checks for executor**

- Trigger a toast.
- Confirm it appears promptly and does not feel like it waits before moving.
- In slow animation playback, confirm the toast translates vertically and fades, with no layout jump.
- Trigger multiple toasts if the product supports stacking; confirm existing stacking behavior is unchanged.
- Toggle reduced motion and confirm the toast fades in without vertical travel.

**Reduced Motion behavior**

- Default: `translateY(-24px)` to `translateY(0)` plus opacity over `--duration-panel`.
- Reduced: opacity-only over `80ms`.
- Feedback remains visible in both modes.

**Source-drift stop condition**

- If toast positioning depends on `top` being animated for layout or stacking calculations, stop and report; do not preserve the layout animation as-is.

---

## 4. Recommended execution order

1. **Plan 1: Command palette** — highest throughput impact, smallest surface area.
2. **Plan 3: Toast** — removes layout animation and adds missing reduced-motion behavior.
3. **Plan 2: Popover** — broad token/performance cleanup; origin refinement should be conditional on actual code.

## Explicitly unverified states

- No browser, device, computed-style, trace, screen-recording, accessibility-tree, or user testing was performed.
- Actual component library, package scripts, Tailwind configuration, and full CSS cascade are unknown.
- Popover anchoring behavior is not verified from the excerpt.
- Sortable queue helper semantics, dragged-element structure, and reduced-motion support are not verified.
- Any executor should stop on source drift rather than improvising beyond these snippets.

Guardrails applied: quality-first planning, frontend accessibility, token reuse, performance-safe motion, and reduced-motion preservation.
