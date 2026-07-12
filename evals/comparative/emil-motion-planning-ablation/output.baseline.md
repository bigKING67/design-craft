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
