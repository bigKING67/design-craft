## 1. Recon summary

- **Stack signals**: CSS plus TSX components; motion appears in global CSS tokens, component CSS, utility-style animation classes, and pointer/JS-driven gesture code.
- **Where motion lives**:
  - Global tokens: `src/styles/motion.css`
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`
  - Inline utility animation: `src/components/CommandPalette.tsx`
  - Gesture handler / imperative animation: `src/components/SortableQueue.tsx`
- **Existing conventions**:
  - Semantic duration/easing tokens already exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
  - Correct local precedent exists in `src/components/Button.css`: transform-only transition, tokenized timing, and a Reduced Motion path that keeps feedback at `80ms`.
- **Product personality**: calm, crisp, operator-focused desktop console. Motion should be fast, causal, non-decorative, and should not tax repeated keyboard workflows.
- **Frequency map from evidence only**:
  - **Very high frequency**: command palette, button press feedback, sortable queue dragging.
  - **Medium / repeated**: popovers.
  - **Occasional but important**: toasts.
- **Evidence level**: static code excerpts only. No runtime timing, computed styles, screen recording, browser validation, device validation, accessibility tree, or user testing was performed.

---

## 2. Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose / frequency | `src/components/CommandPalette.tsx` | Command palette uses `animate-[palette_420ms_ease-in_both]`. For a keyboard-heavy, high-frequency surface, this is likely too slow and starts with the least responsive easing. | Remove or drastically shorten palette motion; prefer instant open/close or ≤80–120ms opacity-only feedback with Reduced Motion parity. |
| 2 | HIGH | Performance / easing / cohesion | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in;`. This animates unintended properties, exceeds crisp popover timing, and starts slowly. | Replace with explicit `transform`/`opacity` transitions using existing semantic tokens and responsive easing. |
| 3 | HIGH | Performance / accessibility | `src/components/toast.css` | Toast entrance animates `top` over `500ms ease-in` via keyframes. `top` is layout-affecting, duration is long for operational feedback, and no Reduced Motion path is shown. | Move toast entrance to `transform` + `opacity`, shorten to tokenized timing, and add Reduced Motion that preserves opacity feedback without positional travel. |
| 4 | MEDIUM | Gesture / interruptibility | `src/components/SortableQueue.tsx` | Pointer move writes `--drag-y` to the queue parent, and release uses fixed `duration: 400`. Static evidence does not show velocity carryover, direct element transform, or Reduced Motion branching. | Drive the dragged item directly with `transform`, use velocity-aware/spring-like settle behavior where available, and reduce motion to immediate/short settle feedback. |
| 5 | MEDIUM | Accessibility / cohesion | Multiple excerpts | Reduced Motion is present only in the button precedent. Palette, popover, toast, and queue excerpts do not show equivalent handling. | Apply the same Reduced Motion convention broadly: preserve state feedback, remove or shorten movement. |
| 6 | MEDIUM | Tokens / maintainability | `CommandPalette.tsx`, `toast.css`, `motion.css` | Motion values are split across hardcoded utility animation, hardcoded CSS animation, and semantic tokens. This weakens consistency. | Consolidate around the existing semantic tokens; add only narrowly named tokens if needed. |

---

## 3. Implementation-ready plans

### Plan 1 — Make command palette immediate and non-decorative

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

**Target behavior**

- Command palette should feel instant for keyboard-heavy operators.
- Remove the `420ms ease-in` animation.
- Preferred target: no entrance/exit animation on the palette container.
- Acceptable fallback if visual continuity is required by nearby code: opacity-only feedback at `80ms–120ms`, no scale/slide, no `ease-in`.
- Reduced Motion should behave the same or shorter; it must not remove state feedback entirely if opacity feedback is retained.

**Project conventions**

- Use existing semantic motion tokens from `src/styles/motion.css`:
  - `--duration-fast: 160ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Follow the precedent in `src/components/Button.css`:
  - transform-specific transition
  - tokenized duration/easing
  - `@media (prefers-reduced-motion: reduce)` with `80ms`

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, remove `className="animate-[palette_420ms_ease-in_both]"` from the palette container.
2. If the element still needs styling hooks, keep `data-open={open}` but do not attach a keyframe animation.
3. If removal creates an abrupt visual discontinuity in nearby styles, add a local class such as `commandPalette` and implement opacity-only CSS:
   ```css
   .commandPalette {
     transition: opacity 120ms var(--ease-responsive);
   }

   .commandPalette[data-open="false"] {
     opacity: 0;
   }

   .commandPalette[data-open="true"] {
     opacity: 1;
   }

   @media (prefers-reduced-motion: reduce) {
     .commandPalette {
       transition-duration: 80ms;
     }
   }
   ```
4. Do not add translation, scale, blur, stagger, or delayed child animations.

**Hard boundaries**

- Do not change `SearchResults`.
- Do not change command search behavior, focus behavior, keyboard shortcuts, or open-state ownership.
- Do not introduce a motion library.
- Do not add new global tokens unless existing tokens cannot be imported or referenced from the component styling system.

**Mechanical checks**

- Search for the removed arbitrary animation string and confirm it no longer appears:
  - `animate-[palette_420ms_ease-in_both]`
- Search for any replacement `ease-in` on the command palette; none should be introduced.
- Run the project’s existing lint/typecheck/build commands if available. Do not invent new tooling.

**Runtime / feel checks for executor**

- Open and close the palette repeatedly by keyboard.
- Confirm it does not feel delayed before content becomes usable.
- In slow-motion inspection, confirm there is no visible slide/scale flourish.
- Toggle Reduced Motion and confirm feedback remains at least as immediate.

**Reduced Motion behavior**

- Same as default if animation is removed.
- If opacity feedback is retained, duration should be `80ms`.

**Source-drift stop condition**

- Stop if the command palette no longer contains the shown `data-open={open}` container or if the animation has already been replaced by a different state-management/styling pattern.

---

### Plan 2 — Normalize popover motion to explicit tokenized properties

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

- Popovers should appear responsive and anchored, not delayed.
- Replace `transition: all` with explicit properties.
- Replace `360ms ease-in` with existing semantic timing.
- Use a trigger-aware transform origin if the component system exposes one; otherwise avoid asserting a custom origin without evidence.
- Add Reduced Motion duration consistent with the button precedent.

**Project conventions**

- Existing token to reuse:
  ```css
  --duration-fast: 160ms;
  --duration-panel: 240ms;
  --ease-responsive: cubic-bezier(0.23, 1, 0.32, 1);
  ```
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

1. In `src/styles/motion.css`, change `.popover` transition from:
   ```css
   transition: all 360ms ease-in;
   ```
   to:
   ```css
   transition:
     transform var(--duration-fast) var(--ease-responsive),
     opacity var(--duration-fast) var(--ease-responsive);
   ```
2. Remove `ease-in`; do not replace it with bare `ease`.
3. Review whether the popover implementation exposes a trigger-origin CSS variable. If it already exists in local code, use it:
   ```css
   transform-origin: var(--popover-transform-origin);
   ```
   If no such variable exists, keep the current origin temporarily and do not invent one.
4. Add Reduced Motion:
   ```css
   @media (prefers-reduced-motion: reduce) {
     .popover {
       transition-duration: 80ms;
     }
   }
   ```
5. Ensure no layout properties are included in the transition list.

**Hard boundaries**

- Do not change markup or popover positioning logic.
- Do not alter modal behavior; centered origins can be correct for modals.
- Do not add broad selectors that affect unrelated overlays.
- Do not introduce `transition: all` elsewhere.

**Mechanical checks**

- Confirm `src/styles/motion.css` no longer contains `.popover { ... transition: all`.
- Confirm `.popover` no longer contains `ease-in`.
- Confirm only `transform` and `opacity` are transitioned.
- Run existing CSS lint/build checks if available.

**Runtime / feel checks for executor**

- Open/close a popover from its trigger.
- Confirm it starts promptly rather than easing in slowly.
- In slow-motion inspection, confirm no unrelated property such as size, position, or color is accidentally animated.
- Toggle Reduced Motion and confirm movement is shortened while state feedback remains visible.

**Reduced Motion behavior**

- Keep feedback.
- Shorten transition duration to `80ms`.
- Do not set `transition: none` unless a specific accessibility issue is discovered.

**Source-drift stop condition**

- Stop if `.popover` is no longer defined in `src/styles/motion.css`, or if popover motion has moved to component-local styles or a JS animation layer not shown in the excerpt.

---

### Plan 3 — Rebuild toast entrance with transform/opacity and Reduced Motion

**Files / current excerpts**

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

- Toasts should communicate arrival without slow layout-affecting motion.
- Replace animated `top` with `transform: translateY(...)`.
- Shorten timing to existing semantic duration.
- Use existing responsive easing.
- Add Reduced Motion that removes vertical travel but keeps opacity feedback.

**Project conventions**

- Use existing tokens from `src/styles/motion.css`:
  ```css
  --duration-fast: 160ms;
  --duration-panel: 240ms;
  --ease-responsive: cubic-bezier(0.23, 1, 0.32, 1);
  ```
- Match the local Reduced Motion pattern from `src/components/Button.css`:
  ```css
  @media (prefers-reduced-motion: reduce) {
    .button { transition-duration: 80ms; }
  }
  ```

**Ordered steps**

1. In `src/components/toast.css`, replace the keyframes with transform/opacity:
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
2. Change `.toast` animation from:
   ```css
   animation: toast-enter 500ms ease-in forwards;
   ```
   to:
   ```css
   animation: toast-enter var(--duration-panel) var(--ease-responsive) both;
   ```
3. Add Reduced Motion:
   ```css
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
4. If redefining `@keyframes` inside the media query conflicts with the project’s CSS tooling, instead create a separate `toast-enter-reduced` keyframe and assign it inside the media query.
5. Do not animate `top`, `left`, `right`, `bottom`, `margin`, `height`, or `width`.

**Hard boundaries**

- Do not change toast queueing, dismissal timing, z-index, positioning, or message content.
- Do not introduce JS for this predetermined entrance.
- Do not add bounce or playful overshoot; this is an operations console.
- Do not remove opacity feedback in Reduced Motion.

**Mechanical checks**

- Confirm `toast-enter` no longer contains `top`.
- Confirm `.toast` no longer uses `500ms` or `ease-in`.
- Confirm Reduced Motion exists in `src/components/toast.css`.
- Run existing lint/build checks if available.

**Runtime / feel checks for executor**

- Trigger one toast and several consecutive toasts.
- Confirm arrival is noticeable but not slow.
- In slow-motion inspection, confirm vertical movement is subtle and transform-based.
- Toggle Reduced Motion and confirm the toast fades in quickly without vertical travel.

**Reduced Motion behavior**

- `80ms` opacity-only feedback.
- No positional movement.

**Source-drift stop condition**

- Stop if toast animation is no longer implemented in `src/components/toast.css`, if the toast system has moved to a JS animation layer, or if the shown `.toast` selector no longer controls toast entrance.

---

## 4. Recommended execution order

1. **Plan 1 — Command palette**: highest frequency; removes likely throughput drag first.
2. **Plan 2 — Popover motion**: broad convention cleanup; eliminates `transition: all` and `ease-in`.
3. **Plan 3 — Toast entrance**: fixes layout-affecting animation and adds Reduced Motion.

**Explicitly unverified states**

- Actual command palette frequency and whether it opens by keyboard in the running product.
- Whether `.popover` is trigger-anchored, modal-like, or shared by multiple overlay types.
- Whether toast stacking, dismissal, or interruption currently causes visible restart artifacts.
- Whether `animateTo` in `SortableQueue.tsx` is custom, library-based, cancelable, or velocity-aware.
- Actual computed styles, frame rate, layout cost, focus behavior, accessibility tree, and Reduced Motion behavior in a browser.
