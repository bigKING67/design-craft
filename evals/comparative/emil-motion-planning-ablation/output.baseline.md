## 1. Recon summary

**Stack signals**
- React/TSX components, plain CSS, CSS custom properties, Tailwind-style arbitrary animation class, and imperative pointer-driven animation.
- Motion currently lives in global CSS, component CSS, inline utility animation strings, and JS animation calls.

**Existing conventions**
- Motion tokens exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
- One correct local precedent exists in `Button.css`: explicit property transition, tokenized duration/easing, reduced-motion override that preserves feedback by shortening duration.

**Product personality**
- Calm, workday-long desktop operations surface.
- Motion should explain causality and continuity, not decorate or delay keyboard throughput.
- Reduced Motion must retain state feedback, not simply remove all cues.

**Frequency map from static evidence**
- **Very high frequency / keyboard-critical:** `CommandPalette`.
- **Likely reusable / high surface area:** `.popover`, though exact usage is unverified.
- **High interaction intensity when active:** `SortableQueue` drag/settle.
- **Intermittent feedback:** `.toast`.
- **Validated local precedent:** `.button`.

**Evidence level**
- Static snippet audit only.
- No runtime, computed-style, trace, screen recording, accessibility-tree, device, or user validation was performed.

---

## 2. Priority table

| Priority | Finding | Static evidence | Risk | Recommended fix |
|---:|---|---|---|---|
| P0 | Motion system is inconsistent across components | `160ms`, `240ms`, `360ms`, `400ms`, `420ms`, `500ms`; mixed `ease-in`, `ease-responsive`, `all` | Operators experience different timing rules for similar UI state changes | Normalize to existing tokens and explicit motion roles |
| P0 | `.popover` uses broad, slow, non-tokenized transition | `transition: all 360ms ease-in;` | Unintended properties may animate; timing conflicts with crisp system requirement | Restrict to `opacity, transform`; use `--duration-panel` and `--ease-responsive` |
| P0 | Command palette animation is long, arbitrary, and lacks visible reduced-motion path | `animate-[palette_420ms_ease-in_both]` | High-frequency keyboard surface may feel delayed; behavior is hard to govern centrally | Replace arbitrary class with named class using tokens and reduced-motion override |
| P1 | Toast animates layout property and runs 500ms | `top: -24px → 0`, `500ms ease-in` | Feedback may feel heavy; layout-affecting animation is avoidable | Animate `transform` + `opacity`; shorten/tokenize |
| P1 | Sortable settle motion is hard-coded and not reduced-motion aware | `animateTo(..., { duration: 400 })` | Direct manipulation may not follow the same timing contract as the rest of the UI | Tokenize settle duration; add reduced-motion branch |
| P2 | Reduced Motion appears local, not systematic | Only `.button` has `@media (prefers-reduced-motion: reduce)` | Similar interactions may provide inconsistent accessibility feedback | Use the button pattern as baseline across overlays, feedback, and drag settle |

---

## 3. Implementation plans

### Plan A — Normalize the shared motion contract and repair popover

**File path / current excerpt**

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
- Popovers enter/exit with crisp opacity/transform continuity.
- No broad `transition: all`.
- Timing uses existing semantic tokens.
- Reduced Motion keeps state feedback with shorter, smaller movement.

**Project conventions to follow**
- Reuse existing custom properties.
- Match the proven button pattern: explicit animated property, tokenized duration/easing, local reduced-motion override.
- Do not introduce decorative spring/bounce behavior.

**Ordered steps**
1. Replace `.popover` transition with explicit properties:
   - `opacity`
   - `transform`
2. Use existing token timing:
   - duration: `var(--duration-panel)`
   - easing: `var(--ease-responsive)`
3. Add state classes or data-state selectors only if the existing markup already exposes open/closed state.
4. Add reduced-motion override:
   - shorten transition duration to `80ms` or reuse a reduced token if one already exists nearby.
   - keep opacity/state feedback.
   - reduce or remove travel distance, not the entire feedback.
5. Grep for other `transition: all` motion rules and queue them for follow-up, but do not expand scope in this change.

**Hard boundaries**
- Do not rename existing tokens unless a broader migration is approved.
- Do not change popover positioning, focus behavior, dismissal behavior, or stacking.
- Do not add a motion library.

**Mechanical checks**
- Search for remaining `transition: all` in the changed file.
- Confirm `.popover` still uses existing token names.
- Confirm a `prefers-reduced-motion: reduce` branch exists for popover motion.
- Run closest available lint/type/build command after implementation.

**Runtime/feel checks to perform later**
- Open/close popover from keyboard and pointer.
- Verify perceived duration feels under the panel token, not delayed.
- Confirm focus outline remains visible throughout transition.
- Confirm Reduced Motion still communicates open/close state.

**Reduced Motion behavior**
- Use shortened duration, minimal transform distance, and opacity/state cue.
- Do not remove all feedback unless the platform preference or existing system explicitly requires no animation.

**Source-drift stop condition**
- Stop and re-audit if `src/styles/motion.css` no longer owns popover styling, token names changed, or popover state is controlled by a separate component/style system not shown here.

---

### Plan B — Replace command palette arbitrary animation with governed overlay motion

**File path / current excerpt**

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
- Command palette feels immediate for keyboard-heavy operators.
- Open/close motion preserves spatial continuity but does not slow command entry.
- Motion is named, tokenized, inspectable, and reduced-motion aware.

**Project conventions to follow**
- Replace arbitrary inline animation with a stable class name.
- Use `--duration-fast` or `--duration-panel` depending on actual visual distance:
  - small opacity/scale: `--duration-fast`
  - panel-like movement: `--duration-panel`
- Use `--ease-responsive`, not `ease-in`.

**Ordered steps**
1. Replace the arbitrary class with a named class, for example:
   - `className="command-palette-motion"`
   - keep `data-open={open}`.
2. Define the class in the existing component stylesheet or shared motion stylesheet already imported by this component path.
3. Implement open/closed selectors using `data-open`:
   - open: `opacity: 1; transform: translateY(0) scale(1);`
   - closed: `opacity: 0; transform: translateY(-4px) scale(0.98);`
4. Use transition rather than one-off animation if the element remains mounted and `data-open` changes.
5. If the element unmounts immediately when closed elsewhere, stop and coordinate with mounting logic before attempting exit motion.
6. Add reduced-motion override:
   - shorter duration.
   - opacity/state cue preserved.
   - no meaningful scale/travel.

**Hard boundaries**
- Do not alter `SearchResults` behavior.
- Do not change command execution, keyboard shortcuts, focus order, or focus trap behavior in this motion-only pass.
- Do not assume exit animation works if the component unmounts immediately; verify implementation structure first.

**Mechanical checks**
- Confirm no `animate-[palette_420ms_ease-in_both]` remains.
- Confirm command palette motion uses existing token names.
- Confirm no `ease-in` remains for this component’s primary open/close motion.
- Confirm reduced-motion CSS is present.
- Run closest available type/lint/build command after implementation.

**Runtime/feel checks to perform later**
- Open palette repeatedly via keyboard shortcut.
- Type immediately after opening; verify motion does not block perceived readiness.
- Close with Escape; verify state change is clear.
- Check focus visibility during transition.
- Repeat with Reduced Motion enabled.

**Reduced Motion behavior**
- Prefer `80ms` opacity-only or near-opacity-only transition.
- Preserve clear open/closed feedback.
- Avoid scale and travel in reduced mode.

**Source-drift stop condition**
- Stop if command palette styling is generated elsewhere, if the component unmounts on close before styles can transition, or if a dedicated overlay primitive already owns this behavior.

---

### Plan C — Make transient feedback and drag settle motion direct, tokenized, and reduced-motion aware

**File paths / current excerpts**

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
- Toasts appear quickly, without layout-position animation.
- Dragged queue items track pointer movement directly while active.
- Release/settle motion is brief, causal, and consistent with panel/fast tokens.
- Reduced Motion preserves feedback with immediate or near-immediate state resolution.

**Project conventions to follow**
- Prefer transform/opacity over layout properties for motion.
- Use existing duration/easing tokens.
- Keep direct manipulation under user control; animate only the settle/reconciliation phase.

**Ordered steps — toast**
1. Replace `top` keyframes with `transform`:
   - from: `transform: translateY(-8px); opacity: 0;`
   - to: `transform: translateY(0); opacity: 1;`
2. Replace `500ms ease-in` with:
   - `var(--duration-panel) var(--ease-responsive)` or `var(--duration-fast)` if the toast is compact.
3. Add reduced-motion override:
   - `80ms`
   - opacity-only or `translateY(-2px)` maximum.
4. Confirm final resting position is still controlled by layout, not animation.

**Ordered steps — sortable queue**
1. Inspect whether `--drag-y` is consumed as an absolute viewport coordinate or transformed into local movement.
2. If it is intended as movement, convert from `event.clientY` absolute value to a local delta from drag start.
3. Keep pointer-move writes limited to the dragged element or queue container already using the custom property.
4. If pointer frequency causes excessive writes, batch style writes with `requestAnimationFrame`.
5. Replace hard-coded `duration: 400` with a named duration constant aligned to existing tokens.
6. Add a reduced-motion branch:
   - on release, snap or use very short settle.
   - preserve slot/state confirmation through position, focus, outline, or selection state.
7. Ensure nearest-slot calculation remains unchanged unless a bug is found during implementation.

**Hard boundaries**
- Do not change queue ordering rules.
- Do not change drag hit testing, selection semantics, or persistence behavior.
- Do not infer performance problems from the snippet alone; only remove avoidable animation risk.
- Do not make toast dismissal, timeout, or stacking changes in this pass.

**Mechanical checks**
- Confirm toast no longer animates `top`.
- Confirm toast duration/easing use existing tokens.
- Confirm sortable settle no longer uses raw `400` inline.
- Confirm reduced-motion handling exists for both toast and sortable settle.
- Run closest available type/lint/build command after implementation.

**Runtime/feel checks to perform later**
- Toast: trigger success, warning, and error variants if they exist; verify entrance is noticeable but not attention-heavy.
- Toast: verify no position jump at rest.
- Queue: drag slowly and quickly; verify item tracks pointer without delayed chase.
- Queue: release near slot boundaries; verify settle communicates final slot.
- Queue: repeat with Reduced Motion enabled.

**Reduced Motion behavior**
- Toast: short opacity cue; minimal or no travel.
- Queue: direct drag remains direct; release snap is immediate or near-immediate, with visible final-state confirmation.

**Source-drift stop condition**
- Stop if a toast primitive, drag library, or shared animation helper already owns these behaviors outside the shown files, or if `animateTo` has its own global reduced-motion configuration.

---

## 4. Recommended execution order

1. **Plan A first:** establishes the shared contract and removes the riskiest broad transition pattern.
2. **Plan B second:** fixes the highest-frequency keyboard surface.
3. **Plan C third:** improves transient feedback and direct manipulation without widening scope.

## Explicitly unverified states

- Actual computed durations/easing in the built app.
- Whether command palette remains mounted during close.
- Whether `.popover` is globally reused or locally scoped.
- Whether `--drag-y` is consumed as absolute position or delta.
- Whether existing build tooling includes lint, type-check, visual tests, or reduced-motion tests.
- Actual keyboard focus behavior, screen reader output, paint/layout cost, frame rate, and user-perceived feel.
