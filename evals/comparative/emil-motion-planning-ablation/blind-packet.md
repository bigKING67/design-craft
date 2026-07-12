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

## 1) Recon summary

- **Stack signals**: React/TSX components plus CSS/Tailwind-style utility animation strings. No motion library is evidenced. Gesture code appears custom JS via pointer handlers and an `animateTo(...)` helper.
- **Where motion lives**:
  - Global tokens and popover motion: `src/styles/motion.css`
  - Component-local utility animation: `src/components/CommandPalette.tsx`
  - Component-local keyframes: `src/components/toast.css`
  - Gesture release animation: `src/components/SortableQueue.tsx`
  - Correct local precedent: `src/components/Button.css`
- **Existing conventions**:
  - Tokens already exist: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`.
  - Correct precedent uses `transform` only, tokenized duration/easing, and a `prefers-reduced-motion` path that shortens rather than removes feedback.
- **Product personality**: calm desktop operations console. Motion should be crisp, causal, low-decoration, and should not tax keyboard-heavy workflows.
- **Frequency map from evidence**:
  - Very high: `CommandPalette` open/close, likely keyboard-driven.
  - High: `SortableQueue` drag/reorder interactions for operators managing queues.
  - Medium: `.popover` if used for menus/filters/details.
  - Occasional but attention-sensitive: `.toast`.
  - High but already aligned: `.button`.
- **Evidence level**: static snippet audit only. No runtime timing, computed styles, DOM structure, browser trace, accessibility tree, or user testing was performed.

---

## 2) Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---|---|---|---|---|
| 1 | HIGH | Purpose / frequency | `src/components/CommandPalette.tsx` | `animate-[palette_420ms_ease-in_both]` adds a long, slow-starting animation to a likely keyboard-heavy surface. Static evidence only confirms the class, not the actual keyframes. | Remove the command palette entrance animation or reduce to non-moving instant feedback; preserve `data-open`. |
| 2 | HIGH | Performance / easing | `src/components/toast.css` | Toast entry animates `top` from `-24px` to `0`, uses `500ms ease-in`, and has no shown Reduced Motion branch. This combines layout-affecting motion, slow duration, and slow-start easing. | Use compositor-only `transform` + `opacity`, tokenized easing/duration, and reduced-motion opacity-only feedback. |
| 3 | HIGH | Gesture / interruptibility | `src/components/SortableQueue.tsx` | Drag release uses `animateTo(nearestSlot(currentY), { duration: 400 })`; fixed-duration tweening is a poor fit for interrupted, velocity-carrying gesture completion. Pointer move writes a CSS variable on `queueRef.current`, which may broaden style recalculation depending on CSS usage. | Drive the dragged item with direct `transform`; release with an interruptible spring or velocity-aware helper; reduce duration and support Reduced Motion. |
| 4 | MEDIUM | Cohesion / tokens | `src/styles/motion.css`, `CommandPalette.tsx`, `toast.css`, `SortableQueue.tsx` | Motion values are inconsistent with existing tokens: `360ms ease-in`, `420ms ease-in`, `500ms ease-in`, `400`. | Replace local ad hoc timings with `--duration-fast`, `--duration-panel`, and `--ease-responsive` or equivalent JS constants derived from them. |
| 5 | MEDIUM | Physicality / performance | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in` and `transform-origin: center`. For trigger-anchored popovers, center origin weakens causality; `transition: all` is overbroad. | Transition only `transform`/`opacity`, shorten timing, use responsive easing, and prefer trigger-provided transform origin with a safe fallback. |
| 6 | MEDIUM | Accessibility | All shown animated surfaces except `Button.css` | Only the button excerpt shows a Reduced Motion path. Other snippets show movement without an evidenced reduced-motion branch. | Add reduced-motion behavior that preserves feedback while removing or shortening spatial movement. |

---

## 3) Implementation-ready plans

### Plan 1 — Tokenize and constrain CSS entrances for popovers and toasts

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

- Popovers respond crisply and only animate compositor-safe properties.
- Trigger-anchored popovers scale from a trigger-provided origin when available; fallback remains safe.
- Toast entry uses `transform` + `opacity`, not `top`.
- Toast duration stays under the existing panel budget.
- Reduced Motion preserves opacity feedback while dropping vertical travel.

**Project conventions**

- Use existing tokens:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Follow the correct local precedent in `src/components/Button.css`: transform-only transition, semantic tokens, explicit Reduced Motion override.

**Ordered steps**

1. In `src/styles/motion.css`, replace `.popover` transition:
   ```css
   .popover {
     transform-origin: var(
       --popover-transform-origin,
       var(--radix-popover-content-transform-origin, var(--transform-origin, center))
     );
     transition:
       transform var(--duration-fast) var(--ease-responsive),
       opacity var(--duration-fast) var(--ease-responsive);
   }
   ```
2. In `src/components/toast.css`, replace layout-moving keyframes with compositor-safe keyframes:
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
     animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;
   }
   ```
3. Add a Reduced Motion branch in `src/components/toast.css`:
   ```css
   @media (prefers-reduced-motion: reduce) {
     @keyframes toast-enter {
       from { opacity: 0; }
       to { opacity: 1; }
     }

     .toast {
       animation-duration: var(--duration-fast);
     }
   }
   ```
4. If `toast.css` does not have access to variables from `src/styles/motion.css`, stop and wire the existing global stylesheet import rather than duplicating token values locally.

**Hard boundaries**

- Do not change toast markup, queue behavior, command palette behavior, or button behavior.
- Do not introduce new animation libraries.
- Do not add new global tokens unless the existing tokens are genuinely unavailable.
- Do not use `transition: all`.
- Do not animate `top`, `left`, `width`, `height`, margin, or padding for these entrances.

**Mechanical checks**

- Confirm no edited selector still contains `transition: all`.
- Confirm `toast-enter` no longer contains `top`.
- Confirm edited CSS references existing tokens instead of new hard-coded `360ms`, `500ms`, or `ease-in`.
- Run the project’s existing lint/typecheck/build command if present. If scripts are unknown, at minimum run whitespace/static checks such as `git diff --check`.

**Runtime / feel checks for executor**

- Open a popover and confirm it appears immediately responsive, not slow-starting.
- If the popover is trigger-anchored, slow animation playback and confirm growth comes from the trigger side when the positioning system provides an origin.
- Trigger a toast and confirm it slides a short distance only, without pushing layout during the animation.
- Toggle Reduced Motion and confirm toast movement is removed while opacity feedback remains.

**Reduced Motion behavior**

- Popover transition remains short and compositor-safe.
- Toast drops spatial movement and keeps a brief opacity fade.

**Source-drift stop condition**

- Stop if `.popover`, `.toast`, or `@keyframes toast-enter` no longer match the supplied structure, if tokens are renamed, or if toast positioning relies on `top` for non-animation layout semantics that are not shown here.

---

### Plan 2 — Remove command palette entrance motion from the keyboard path

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

- Opening the command palette should not wait on a decorative entrance animation.
- The component should preserve `data-open={open}` for state styling and tests.
- Keyboard-heavy operators should get immediate state continuity and visible focus, not a 420ms slow-start entrance.
- Reduced Motion is naturally satisfied because the entrance motion is removed.

**Project conventions**

- Existing design authority favors crisp motion and visible focus.
- Existing local motion precedent uses short durations and responsive easing only where motion adds feedback.
- For a command palette, frequency and throughput outweigh decorative entry motion.

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
2. If the removed `className` was the only styling hook for layout or visibility, stop and inspect the real palette styling before replacing it. Do not hide/show the palette by inventing new CSS without confirming existing state styles.
3. If the project requires a class for styling, use an existing non-motion class already present in the codebase; do not create a new animation class.
4. Search for the `palette` keyframes or utility usage. If unused after this change, remove only the dead palette keyframes in the same commit; otherwise leave shared definitions untouched.

**Hard boundaries**

- Do not alter `SearchResults`.
- Do not change focus management, keyboard shortcuts, search behavior, or open-state ownership.
- Do not add a shorter replacement animation unless product/design explicitly requires it.
- Do not replace this with opacity, scale, blur, or delayed mount motion.

**Mechanical checks**

- Confirm `CommandPalette.tsx` no longer includes `animate-[palette_420ms_ease-in_both]`.
- Confirm `data-open={open}` remains.
- Confirm TypeScript/JSX syntax passes the project’s existing check.
- Run the closest existing project check; if scripts are unknown, run `git diff --check` and the repository’s normal typecheck once discovered.

**Runtime / feel checks for executor**

- Open the command palette via keyboard repeatedly and confirm it appears immediately.
- Confirm there is no perceptible “waiting for the palette” effect.
- Confirm focus remains visible and lands where it did before the change.
- Toggle Reduced Motion and confirm behavior is equivalent, with no movement introduced.

**Reduced Motion behavior**

- Same as default: no command palette entrance motion.
- Feedback must come from immediate visibility and focus, not spatial animation.

**Source-drift stop condition**

- Stop if the current `className` contains additional non-motion classes not shown in the excerpt, if `animate-[palette_420ms_ease-in_both]` is generated dynamically, or if visibility depends on that exact class.

---

### Plan 3 — Make sortable queue drag release interruptible and gesture-appropriate

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

- During drag, update the dragged item’s `transform` directly, not a broad parent CSS variable, unless the real CSS proves the variable is scoped only to the dragged element.
- On release, settle to the nearest slot with interruptible, velocity-aware motion rather than a fixed 400ms tween.
- Reduced Motion should snap or use a very short non-bouncy settle while preserving state feedback.
- The queue should feel causal: dragged item follows input, then settles without a hard, slow glide.

**Project conventions**

- Prefer transform-only motion, as shown by the button precedent.
- Use existing duration/easing tokens where CSS is involved.
- Keep support-operator throughput high; drag motion should clarify position, not add delay.

**Ordered steps**

1. Inspect the actual CSS that consumes `--drag-y`.
   - If it only affects the active dragged item’s transform, this part may be acceptable.
   - If it affects descendants or multiple rows, replace parent variable writes with direct style updates on the dragged element.
2. Introduce a ref for the actively dragged row if one does not already exist:
   ```tsx
   const draggedItemRef = useRef<HTMLElement | null>(null);
   ```
   Use the project’s actual row element type and existing ref pattern.
3. Replace broad pointer-move style mutation with direct transform mutation on the dragged element:
   ```tsx
   function onPointerMove(event: PointerEvent) {
     draggedItemRef.current?.style.setProperty(
       "transform",
       `translateY(${event.clientY}px)`
     );
   }
   ```
   If the current coordinate system expects a delta rather than viewport `clientY`, keep the existing coordinate math and apply the result to `translateY(...)`; do not blindly change coordinate semantics.
4. Replace fixed release timing:
   ```tsx
   animateTo(nearestSlot(currentY), { duration: 400 });
   ```
   with the project’s existing spring/interruptible API if available. Target values:
   ```tsx
   animateTo(nearestSlot(currentY), {
     type: "spring",
     duration: 0.5,
     bounce: 0.2,
   });
   ```
5. If `animateTo` does not support spring options, stop and update/replace the helper deliberately rather than passing unsupported options.
6. Add or reuse Reduced Motion detection. Target behavior:
   ```tsx
   const prefersReducedMotion = /* project’s existing reduced-motion hook or media query */;
   animateTo(nearestSlot(currentY), prefersReducedMotion
     ? { duration: 80 }
     : { type: "spring", duration: 0.5, bounce: 0.2 }
   );
   ```
7. Ensure pointer-up can interrupt an in-flight settle before starting the next one, using the existing animation cancellation mechanism if present.

**Hard boundaries**

- Do not rewrite queue ordering logic.
- Do not change `nearestSlot(currentY)` semantics unless a bug is proven.
- Do not introduce a new animation dependency.
- Do not change data persistence, selection, keyboard ordering, or row rendering outside the minimum ref/style path.
- Do not pass spring options to `animateTo` if its API does not support them.

**Mechanical checks**

- Confirm pointer-move animation writes to `transform` on the dragged element or prove the existing CSS variable is strictly scoped.
- Confirm fixed `{ duration: 400 }` is gone from drag release.
- Confirm Reduced Motion has an explicit branch.
- Run existing typecheck/lint. If unavailable, run `git diff --check` and the closest TS/JS parser check available in the project.

**Runtime / feel checks for executor**

- Drag a row slowly and confirm it tracks the pointer without laggy easing during active drag.
- Release near a slot and confirm the row settles naturally without a long 400ms glide.
- Start a second drag while a settle is in progress and confirm motion retargets rather than fighting the pointer.
- Toggle Reduced Motion and confirm release snaps or settles very briefly without bounce.

**Reduced Motion behavior**

- Active drag still follows the pointer.
- Release uses an immediate or very short non-bouncy settle, preserving positional feedback without expressive motion.

**Source-drift stop condition**

- Stop if `animateTo` is not the actual release mechanism, if `--drag-y` is required by broader layout calculations, if row refs already use a different abstraction, or if Reduced Motion infrastructure already exists under a different API that must be reused.

---

## 4) Recommended execution order

1. **Plan 2 — Command palette**: highest throughput impact and smallest safe change.
2. **Plan 1 — Popover/toast CSS**: removes slow easing, layout animation, and overbroad transitions using existing conventions.
3. **Plan 3 — Sortable queue**: highest interaction complexity; do after simpler token/performance cleanup because it requires API confirmation around `animateTo`.

## Explicitly unverified states

- The actual `palette` keyframes are not shown.
- Whether `.popover` is always trigger-anchored, or sometimes used as a centered modal, is unverified.
- Whether CSS variables from `src/styles/motion.css` are available inside `toast.css` is unverified.
- The implementation and supported options of `animateTo(...)` are unverified.
- The CSS consumer of `--drag-y` is unverified.
- No browser, device, performance trace, computed-style inspection, accessibility-tree inspection, or user validation was performed.

Applied frontend quality constraints: reuse existing tokens, avoid speculative rewrites, preserve accessibility and Reduced Motion feedback, and keep fixes scoped to evidenced motion surfaces.


## Output B

Planning guardrails applied: quality-first scope control, frontend accessibility, token reuse, and reduced-motion preservation.

## 1. Recon summary

**Stack signals**
- CSS custom properties in `:root` for motion tokens.
- Component-local CSS files plus shared motion CSS.
- TSX components with class-based animation hooks.
- Utility-style arbitrary animation class in `CommandPalette`.
- Imperative pointer/animation logic in `SortableQueue`.

**Where motion currently lives**
- `src/styles/motion.css`: global duration/easing tokens and `.popover`.
- `src/components/CommandPalette.tsx`: inline animation class.
- `src/components/toast.css`: keyframes and `.toast`.
- `src/components/SortableQueue.tsx`: pointer-driven drag state and snap animation.
- `src/components/Button.css`: local precedent that appears aligned with the stated design authority.

**Existing conventions**
- Tokens: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive`.
- Preferred precedent: transform-only button feedback, tokenized duration/ease, explicit reduced-motion branch.
- Stated authority: crisp motion, semantic tokens, visible focus, reduced-motion feedback preservation.

**Product personality**
- Calm desktop operations console.
- Keyboard-heavy, throughput-sensitive users.
- Motion should clarify causality and continuity, not perform decorative delay.

**Frequency map from snippets only**
- Very high: buttons, popovers, command palette.
- High during interaction: sortable drag/snap.
- Intermittent but attention-grabbing: toasts.
- Evidence does not include actual usage counts.

**Evidence level**
- Static snippet audit only.
- No runtime, browser, computed-style, trace, device, accessibility-tree, or user-test evidence.

---

## 2. Priority table

| Priority | Finding | Static evidence | Risk to product goal | Recommended direction | Confidence |
|---:|---|---|---|---|---|
| P0 | Motion token drift | `420ms`, `500ms`, `400`, `360ms ease-in` outside existing token pattern | Slower, inconsistent feedback across frequent workflows | Normalize to `--duration-fast`, `--duration-panel`, `--ease-responsive`; use JS equivalents only where necessary | High |
| P0 | Reduced Motion coverage is incomplete in shown excerpts | Only `Button.css` shows `@media (prefers-reduced-motion: reduce)` | Users requesting reduced motion may still receive long spatial animations | Add reduced-motion branches for popover, palette, toast, sortable snap | High |
| P1 | Broad transition on popover | `.popover { transition: all 360ms ease-in; }` | Unintended properties may animate; duration/ease feel less responsive | Scope to `opacity, transform`; use tokens; avoid `all` | High |
| P1 | Layout-position toast animation | `@keyframes toast-enter { from { top: -24px; ... } }` | Position-property animation can be less predictable and less crisp | Animate `transform` + `opacity`; keep final layout stable | High |
| P1 | Command palette hardcoded arbitrary animation | `animate-[palette_420ms_ease-in_both]` | Central operator surface may feel delayed; reduced-motion path not visible | Replace with named class/state using data attribute and tokens | Medium-high |
| P2 | Drag snap hardcoded and potentially long | `animateTo(..., { duration: 400 })` | Drag release may feel sluggish for queue operators | Shorten/tokenize snap; honor reduced motion; verify transform-only consumption of `--drag-y` | Medium |

---

## 3. Implementation plans

### Plan A — Establish shared motion baseline and fix popover

**Exact file path / current excerpt**

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
- Popovers open/close crisply and causally.
- Only `opacity` and `transform` animate.
- Duration/ease use existing semantic tokens.
- Reduced Motion still gives feedback, but with minimal spatial movement and shorter duration.

**Project conventions to follow**
- Keep existing token names.
- Follow `Button.css` precedent: transform-based feedback, tokenized timing, explicit reduced-motion override.
- Preserve visible focus styles; do not remove outlines or focus rings.

**Ordered steps**
1. Confirm where `src/styles/motion.css` is imported before editing.
2. Replace `.popover` transition from `all 360ms ease-in` to scoped properties:
   - `transition-property: opacity, transform`
   - `transition-duration: var(--duration-fast)` or `var(--duration-panel)` only if popovers are panel-scale.
   - `transition-timing-function: var(--ease-responsive)`
3. Change `transform-origin: center` to a contextual default such as `var(--popover-origin, top center)` if placement can set it; otherwise keep stable origin and avoid inventing placement logic.
4. Add a reduced-motion branch:
   - shorten to `80ms`, matching local button precedent.
   - avoid scale/large translate if such states exist elsewhere.
5. Grep for other `.popover` state selectors before finalizing so open/closed transforms remain compatible.

**Hard boundaries**
- Do not introduce a new animation library.
- Do not animate layout properties.
- Do not change popover positioning, portal behavior, focus trapping, or keyboard handling.
- Do not create broad global selectors beyond the existing `.popover` surface.

**Mechanical checks**
- Search for `transition: all`, `.popover`, and `prefers-reduced-motion`.
- Run nearest lint/typecheck/build commands available in project scripts.
- Re-read final diff to ensure only motion-related CSS changed.

**Runtime/feel checks to perform later, not claimed here**
- Keyboard-open and mouse-open popover.
- Confirm focus indicator remains visible throughout open/close.
- Confirm no delayed close blocks rapid operator actions.
- Confirm reduced-motion preference shortens/preserves feedback.

**Reduced Motion behavior**
- Keep opacity feedback.
- Limit or remove spatial transform.
- Use approximately `80ms` based on existing button precedent.

**Source-drift stop condition**
- Stop if `.popover` is now owned by another component stylesheet, generated CSS, or a placement library with its own origin/animation contract.

---

### Plan B — Normalize command palette and toast motion

**Exact file paths / current excerpts**

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
- Command palette feels immediate enough for keyboard-heavy workflows.
- Toasts enter clearly without layout-position animation.
- Both use existing duration/easing tokens.
- Both have explicit reduced-motion behavior that preserves state feedback.

**Project conventions to follow**
- Use existing tokens: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
- Prefer named CSS classes/state selectors over arbitrary hardcoded animation values.
- Use `data-open` as the semantic state hook already present.
- Keep feedback calm: opacity plus small transform, no decorative bounce.

**Ordered steps**
1. In `CommandPalette.tsx`, replace the arbitrary animation class with a stable class name while preserving `data-open={open}`.
   - Example target shape: `className="command-palette"` if global CSS is acceptable in the existing style system.
   - If the project uses CSS modules or a class merge utility, follow that local pattern instead.
2. Add or update CSS for the palette in the appropriate existing stylesheet:
   - closed state: slightly offset/transparent if mounted while closed.
   - open state via `[data-open="true"]`: `opacity: 1; transform: translateY(0) scale(1)`.
   - transition: `opacity, transform` using `var(--duration-panel)` and `var(--ease-responsive)`.
   - use faster exit if existing state model supports it; do not invent lifecycle behavior.
3. In `toast.css`, replace `top` keyframe movement with transform movement:
   - from: `transform: translateY(-8px); opacity: 0`
   - to: `transform: translateY(0); opacity: 1`
4. Change `.toast` duration/ease from `500ms ease-in` to tokenized timing:
   - likely `var(--duration-panel) var(--ease-responsive)` for notification entrance.
5. Add reduced-motion media rules for both palette and toast:
   - `80ms` duration.
   - opacity-only or near-zero translate.
6. Ensure final visible/end state is unchanged: toast still lands at the same layout position; palette still reflects `open`.

**Hard boundaries**
- Do not change command search behavior, result rendering, focus management, or keyboard shortcuts.
- Do not change toast stacking, z-index, dismissal behavior, or announcement semantics.
- Do not add new global naming conventions without checking existing CSS organization.
- Do not use `display` animation or delay input availability.

**Mechanical checks**
- Search for `palette_`, `toast-enter`, `500ms`, `420ms`, and `ease-in`.
- Confirm no duplicate keyframe names conflict.
- Run nearest lint/typecheck/build command.
- If CSS modules are present, verify class binding compile path.

**Runtime/feel checks to perform later, not claimed here**
- Open command palette repeatedly from keyboard shortcut.
- Type immediately after open and verify motion does not obscure input readiness.
- Trigger multiple toasts and verify stacking still reads cleanly.
- Verify reduced-motion preference shortens motion while preserving entrance feedback.

**Reduced Motion behavior**
- Palette: short opacity transition; remove or minimize translate/scale.
- Toast: short opacity transition; avoid vertical travel.
- Preserve feedback that a surface appeared; do not make changes invisible.

**Source-drift stop condition**
- Stop if the command palette now has enter/exit lifecycle handling elsewhere, or if toast position is controlled by a library that depends on `top` keyframes.

---

### Plan C — Make sortable queue drag release responsive and reduced-motion aware

**Exact file path / current excerpt**

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
- Drag follows pointer directly.
- Release snap preserves spatial continuity but completes quickly.
- Reduced Motion avoids long spatial travel while still confirming the item settled.
- Motion remains transform-driven if `--drag-y` is consumed by CSS.

**Project conventions to follow**
- Align snap timing with `--duration-fast` / `--duration-panel` semantics.
- Use local button precedent for reduced-motion duration around `80ms`.
- Keep pointer interaction responsive; do not add decorative easing.

**Ordered steps**
1. Inspect the full component and related CSS for:
   - how `--drag-y` is consumed.
   - what `animateTo` accepts.
   - whether reduced-motion handling already exists.
2. If `--drag-y` feeds `top`, `margin`, or layout-affecting properties, convert consumption to `transform` before tuning duration.
3. Replace hardcoded `400` with a token-aligned duration:
   - normal snap: no more than `var(--duration-panel)` equivalent, likely `240ms`.
   - if the snap is very small/frequent, prefer `160ms`.
4. Add reduced-motion detection near the animation boundary:
   - if `animateTo` has built-in reduced-motion support, use that.
   - otherwise use `matchMedia('(prefers-reduced-motion: reduce)')` and pass `80ms` or immediate snap plus non-spatial feedback.
5. Consider `requestAnimationFrame` batching for `style.setProperty` only if inspection shows pointermove churn or layout reads in the same path.
6. Preserve `setDragging(false)` semantics unless full-file inspection shows it causes premature visual state loss.

**Hard boundaries**
- Do not rewrite queue ordering logic.
- Do not change nearest-slot calculation without a separate behavior bug.
- Do not change pointer capture, accessibility semantics, or persistence side effects unless directly required.
- Do not add drag inertia, bounce, overshoot, or decorative physics.

**Mechanical checks**
- Search for `--drag-y`, `animateTo`, `duration: 400`, `nearestSlot`, and reduced-motion handling.
- Run nearest typecheck/lint.
- If tests exist for sorting/reordering, run the smallest relevant test set.

**Runtime/feel checks to perform later, not claimed here**
- Drag slowly and quickly; release near and far from slot.
- Verify no perceptible lag on pointer follow.
- Verify snap does not delay the next keyboard/mouse operation.
- Verify reduced-motion preference avoids long travel but still indicates settlement.

**Reduced Motion behavior**
- Directly settle or use approximately `80ms`.
- Preserve final placement feedback through position commit, opacity, outline, or other non-spatial state already available.
- Avoid long animated translation between slots.

**Source-drift stop condition**
- Stop if `animateTo` is a shared abstraction with global timing policy, or if queue drag motion is controlled by another state machine not shown in the excerpt.

---

## 4. Recommended execution order

1. **Plan A first**: fixes the shared motion baseline and removes the riskiest broad transition.
2. **Plan B second**: brings the two most visible hardcoded component animations onto tokens and reduced-motion behavior.
3. **Plan C third**: requires full-file inspection of drag logic and should follow after baseline timing decisions are settled.

## Explicitly unverified states

- Actual rendered timing and easing.
- Whether CSS files are globally loaded or module-scoped.
- Actual command palette mount/unmount lifecycle.
- Actual popover open/closed selectors and placement logic.
- How `--drag-y` is consumed.
- What `animateTo` supports.
- Focus visibility during animated states.
- Reduced-motion behavior in browser.
- Performance under real queue size or pointer frequency.
- User perception, operator throughput impact, and device/browser variance.


## Output C

Diagnosis: the system already has a good crisp-motion precedent, but several transient and direct-manipulation paths bypass it with long `ease-in`, broad/property-heavy motion, and incomplete Reduced Motion coverage.

## 1. Recon summary

- **Stack signals:** React/TSX components, CSS files, Tailwind-style arbitrary animation class, inline style mutation for drag, and a custom `animateTo(...)` helper.
- **Where motion lives:**  
  - Global tokens and `.popover`: `src/styles/motion.css`  
  - Component animation class: `src/components/CommandPalette.tsx`  
  - Toast keyframes: `src/components/toast.css`  
  - Direct manipulation: `src/components/SortableQueue.tsx`  
  - Correct local precedent: `src/components/Button.css`
- **Existing conventions:**  
  - Tokens: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`  
  - Preferred property precedent: explicit `transform`, not `all`  
  - Reduced Motion precedent: preserve feedback, shorten to `80ms`
- **Product personality:** calm, workday operations console; motion should be crisp, causal, and non-performative.
- **Frequency map:**  
  - High-frequency / keyboard-heavy: command palette, buttons  
  - Repeated operational overlays: popovers  
  - Occasional but potentially repeated: toasts  
  - Direct manipulation: sortable queue drag/reorder
- **Evidence level:** static excerpts only. No runtime behavior, computed styles, traces, screen recordings, accessibility-tree output, or user testing were observed.

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | Static | `src/components/CommandPalette.tsx` | `animate-[palette_420ms_ease-in_both]` conflicts with high-frequency keyboard use and token precedent; `ease-in` delays initial response by definition. | Replace arbitrary long keyframe with tokenized opacity/very small transform transition; add Reduced Motion branch. |
| P1 | Static | `src/components/SortableQueue.tsx` | Drag release uses fixed `duration: 400` with no visible velocity, projection, pointer capture, grab-offset, or interruption contract in the excerpt. | Audit/implement direct-manipulation physics: capture pointer, preserve offset, track velocity, snap from projected endpoint, settle interruptibly. |
| P2 | Static | `src/components/toast.css` | Toast animates `top` for `500ms ease-in`; this is a layout-property animation risk and is slower than the project’s panel token. | Animate `transform` + `opacity` with existing tokens; Reduced Motion removes vertical travel but keeps feedback. |
| P2 | Static | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in` and `transform-origin: center`; broad property ownership and non-token timing diverge from local precedent. | Restrict to `opacity, transform`; use project tokens; verify whether origin should be trigger-relative before changing it. |
| P2 | Static | Multiple excerpts | Reduced Motion is only proven for `.button`; other meaningful motion excerpts do not show a Reduced Motion path. | Add per-component Reduced Motion branches that preserve state feedback without spatial travel. |

## 3. Implementation plans

### Plan 1 — Normalize command palette and popover transient motion

**Evidence level:** static only.

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

- Command palette opens/closes immediately enough for keyboard-heavy use.
- Motion uses existing tokens: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
- Palette feedback is primarily opacity plus a tiny scale/translate, not a long entrance.
- Popover transitions only own `opacity` and `transform`.
- Popover origin is trigger-relative if the component has a positioning contract for it; otherwise preserve current origin and only fix timing/property scope.

**Project conventions**

- Follow the button precedent: explicit transform transition, semantic tokens, Reduced Motion duration of `80ms`.
- Preserve visible focus and keyboard throughput.
- Do not introduce decorative bounce.

**Ordered steps**

1. In `src/styles/motion.css`, replace `.popover` transition with explicit properties:

   ```css
   .popover {
     transform-origin: var(--popover-transform-origin, center);
     transition:
       opacity var(--duration-panel) var(--ease-responsive),
       transform var(--duration-panel) var(--ease-responsive);
   }
   ```

2. Before relying on `--popover-transform-origin`, inspect the popover implementation:
   - If a trigger-relative origin variable already exists, map it to `--popover-transform-origin`.
   - If no such positioning signal exists, keep `center` and do not invent geometry.

3. Replace the command palette arbitrary animation with a named class, for example:

   ```tsx
   <div
     data-open={open}
     className="commandPalette"
   >
   ```

4. Add the command palette motion rule in the existing motion stylesheet or the component’s established stylesheet, whichever is already imported for this component:

   ```css
   .commandPalette {
     opacity: 1;
     transform: scale(1);
     transition:
       opacity var(--duration-fast) var(--ease-responsive),
       transform var(--duration-fast) var(--ease-responsive);
   }

   .commandPalette[data-open="false"] {
     opacity: 0;
     transform: scale(0.98);
     pointer-events: none;
   }
   ```

5. Add Reduced Motion coverage:

   ```css
   @media (prefers-reduced-motion: reduce) {
     .popover,
     .commandPalette {
       transition-duration: 80ms;
     }

     .commandPalette,
     .commandPalette[data-open="false"] {
       transform: none;
     }
   }
   ```

**Hard boundaries**

- Do not change `SearchResults`.
- Do not change command execution, focus trapping, keyboard shortcuts, or palette mounting semantics.
- Do not add dependencies.
- Do not add new duration/easing tokens unless a broader token migration is explicitly approved.

**Mechanical checks**

- Run the closest existing checks after inspecting package scripts:
  - type check, if present
  - lint, if present
  - component/unit tests touching command palette or popover, if present
- Verify there are no remaining references to `animate-[palette_420ms_ease-in_both]`.

**Runtime/feel checks to perform later**

- Open/close palette repeatedly by keyboard.
- Interrupt open with close and close with open.
- Confirm focus remains visible and usable throughout.
- Open popover from each supported side/alignment and confirm origin feels spatially attached if trigger-origin data exists.

**Reduced Motion behavior**

- Palette: no scale/positional travel; short opacity feedback remains.
- Popover: no added spatial travel beyond existing open/closed state; duration capped to `80ms`.

**Source-drift stop condition**

Stop before editing if:
- `CommandPalette` no longer contains the cited arbitrary animation.
- `.popover` already has explicit tokenized properties.
- the popover is actually a centered modal-like surface rather than an anchored transient surface.
- `DESIGN.md` or local tokens have replaced the cited motion contract.

---

### Plan 2 — Convert toast entry from layout travel to tokenized transform feedback

**Evidence level:** static only.

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

- Toast entry remains noticeable but calm.
- Vertical travel is small and compositor-friendly.
- Timing uses existing `--duration-panel` and `--ease-responsive`.
- Reduced Motion removes vertical travel while keeping opacity confirmation.

**Project conventions**

- Use existing semantic tokens.
- Prefer `transform` and `opacity`.
- Preserve the toast’s final layout, stacking, live-region behavior, dismissal timing, and focus behavior.

**Ordered steps**

1. Replace `top` animation with transform-based keyframes:

   ```css
   @keyframes toast-enter {
     from {
       transform: translateY(var(--toast-enter-y, -8px));
       opacity: 0;
     }
     to {
       transform: translateY(0);
       opacity: 1;
     }
   }
   ```

2. Replace the toast animation rule:

   ```css
   .toast {
     animation: toast-enter var(--duration-panel) var(--ease-responsive) both;
   }
   ```

3. Add Reduced Motion behavior:

   ```css
   @media (prefers-reduced-motion: reduce) {
     .toast {
       --toast-enter-y: 0px;
       animation-duration: 80ms;
     }
   }
   ```

4. Inspect for existing toast exit animations. If an exit exists, apply the same principles there: no layout-property animation, no long `ease-in`, no large travel in Reduced Motion.

**Hard boundaries**

- Do not change toast positioning model except removing animated `top`.
- Do not change stacking order, auto-dismiss duration, ARIA/live-region behavior, or toast content.
- Do not add new animation libraries.
- Do not make the toast invisible until JavaScript starts.

**Mechanical checks**

- CSS parse/build check through the project’s existing frontend build or lint command.
- Search for remaining `top` animation inside `toast.css`.
- Search for duplicate `toast-enter` definitions before editing.

**Runtime/feel checks to perform later**

- Trigger one toast and multiple consecutive toasts.
- Confirm entry feels prompt and does not visually push layout.
- Confirm auto-dismiss and manual dismiss still work.
- Confirm no toast content becomes unreachable during animation.

**Reduced Motion behavior**

- Toast fades in over `80ms`.
- No vertical movement.
- State feedback is preserved through opacity and final placement.

**Source-drift stop condition**

Stop before editing if:
- `toast-enter` no longer matches the cited keyframes.
- toast positioning depends on animated `top` for final layout rather than entry effect.
- a separate toast lifecycle system already owns entry/exit animation.

---

### Plan 3 — Rework sortable queue release around direct-manipulation physics

**Evidence level:** static only.

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

- Dragged item tracks the pointer 1:1 after intent is established.
- Grab offset is preserved; the item does not jump under the pointer.
- Pointer capture keeps the drag active outside the original bounds.
- Release chooses a slot from projected endpoint, not only the release position.
- Release animation starts from the current presented position and measured velocity.
- Reduced Motion keeps direct tracking but removes elastic/large settle effects.

**Project conventions**

- Preserve throughput and precision for operators.
- Use existing animation utilities first.
- Keep drag work out of React render loops where possible.
- Avoid broad CSS variable updates on large parent trees if the variable affects many descendants.

**Ordered steps**

1. Inspect the full component for:
   - pointer-down handler
   - item identity and active dragged element
   - `currentY` source
   - `nearestSlot(...)`
   - `animateTo(...)` implementation/signature
   - CSS consuming `--drag-y`

2. On pointer down, create a drag session ref:

   ```ts
   {
     pointerId,
     containerTop,
     grabOffsetY,
     currentY,
     samples: Array<{ y: number; t: number }>
   }
   ```

   Cache layout measurements once at drag start, not on every move.

3. Call pointer capture on the interactive drag target once drag intent is confirmed:

   ```ts
   event.currentTarget.setPointerCapture(event.pointerId);
   ```

4. On pointer move:
   - Ignore non-active pointer IDs.
   - Compute list-local CSS pixels, not raw viewport `clientY`:

     ```ts
     const y = event.clientY - containerTop - grabOffsetY;
     ```

   - Update only the dragged item’s transform owner, for example via a local CSS variable on that item, not a parent variable that may invalidate the full queue.
   - Track recent samples using monotonic timestamps for velocity.

5. On pointer up:
   - Release pointer capture.
   - Compute velocity in CSS px/s from recent samples.
   - Project endpoint from current position and velocity.
   - Choose `nearestSlot(projectedY)`.
   - Start the settle animation from the current presentation value.
   - Pass velocity to the animation primitive if supported.

6. Replace fixed `duration: 400` with an interruptible settle:
   - preferred: existing spring/physics API with no or minimal overshoot
   - acceptable fallback only if no spring exists: bounded tokenized duration based on distance, using `--ease-responsive`, while marking velocity handoff as not fully satisfied

7. Ensure a new drag during the settle cancels/retargets from the current visible position, not the previous logical target.

**Hard boundaries**

- Do not change queue ordering data semantics.
- Do not change keyboard reorder behavior, if present.
- Do not add an animation dependency unless the existing `animateTo` helper cannot be extended locally and the dependency decision is explicitly approved.
- Do not combine press scale and drag translate on the same uncoordinated `transform` owner; use wrapper layers or one composed transform.

**Mechanical checks**

- Type check the component.
- Run existing tests for queue ordering/reordering, if present.
- Add or update unit tests for `nearestSlot(projectedY)` if the function is testable.
- Static check that the drag hot path does not call React state setters on every pointer move.

**Runtime/feel checks to perform later**

- Drag slowly across slots.
- Flick quickly toward a neighboring and a farther slot.
- Release, then immediately re-grab during settle; confirm no jump.
- Move pointer outside the item while dragging; confirm capture keeps tracking.
- Confirm grab offset is preserved.
- Test under a long queue if that state exists.

**Reduced Motion behavior**

- Direct pointer tracking remains; direct manipulation is not removed.
- Release settle uses no bounce/overshoot and a short duration.
- Large elastic travel, decorative recoil, or parallax is disabled.
- Slot change feedback remains visible through final position/state styling.

**Source-drift stop condition**

Stop before editing if:
- `animateTo` already implements velocity-aware interruption and the excerpt is stale.
- `--drag-y` is not used for the dragged item’s transform.
- the queue is not reorderable direct manipulation in current source.
- `nearestSlot` semantics changed from pixel position to index/data-based snapping.

## 4. Recommended execution order

1. **Plan 1:** fixes the highest-frequency keyboard/overlay motion and aligns the system with existing tokens.  
2. **Plan 2:** isolated, low-risk cleanup that removes layout-property toast motion.  
3. **Plan 3:** highest interaction complexity; do after the token/overlay cleanup because it needs runtime feel validation and possibly animation-helper inspection.

## Explicitly unverified states

- Actual imported CSS order and selector specificity.
- Whether `palette` keyframes exist elsewhere.
- Computed durations/easing in the browser.
- Real smoothness, frame pacing, layout shift, or paint/composite cost.
- Focus trap behavior, keyboard focus visibility, and accessibility-tree output.
- Actual Reduced Motion behavior outside the button excerpt.
- Pointer capture, grab offset, interruption, velocity handoff, and touch/device feel for the sortable queue.
- Toast ARIA/live-region behavior and dismissal lifecycle.

No files were edited; this is an evidence-bound implementation roadmap only.
