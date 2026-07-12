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
