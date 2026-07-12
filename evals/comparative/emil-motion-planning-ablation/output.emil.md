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
