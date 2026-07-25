## 1. Recon summary

- **Stack signals:** React/TSX components, plain CSS files, CSS custom properties, and utility-style arbitrary animation classes.
- **Where motion lives:**  
  - Global tokens: `src/styles/motion.css`  
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`  
  - Inline utility animation: `src/components/CommandPalette.tsx`  
  - Imperative drag animation: `src/components/SortableQueue.tsx`
- **Existing conventions:**  
  - Semantic duration/easing tokens exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
  - Local precedent exists for restrained transform motion and Reduced Motion handling in `Button.css`.
- **Product personality:** calm, task-oriented, desktop operations console; motion should clarify cause/effect and state continuity without decorative delay.
- **Frequency map:**  
  - Very high frequency: button press, command palette, queue drag/drop.  
  - Medium frequency: popovers.  
  - Intermittent but attention-sensitive: toast entry.
- **Evidence level:** static evidence only. No runtime behavior, computed styles, frame timing, accessibility tree, input latency, or user testing was verified.

---

## 2. Vetted priority table

| Priority | Finding | Evidence | Risk | Direction |
|---|---|---|---|---|
| P0 | Reduced Motion coverage is inconsistent | `Button.css` has a reduce path; popover, palette, toast, queue snippets do not show one | Users requesting reduced motion may still receive long entrance/snap motion | Define a shared reduced-motion contract and apply to all listed motion surfaces |
| P0 | Command palette motion appears too slow/eased for a high-frequency keyboard surface | `animate-[palette_420ms_ease-in_both]` | May make command invocation feel delayed; static evidence only, no latency measured | Use tokenized duration, responsive easing, shorter enter/exit, preserved state feedback |
| P1 | Popover uses broad transition and non-token motion | `.popover { transition: all 360ms ease-in; }` | `all` can accidentally animate layout/paint properties; 360ms ease-in may feel sluggish | Restrict to `opacity, transform`; use semantic tokens |
| P1 | Toast animates layout-affecting `top` for 500ms | `@keyframes toast-enter { from { top: -24px; ... } }` | Layout-position animation is more fragile than transform; duration is long for operational feedback | Convert to transform/opacity with shorter tokenized timing |
| P1 | Queue drop animation lacks visible Reduced Motion contract | `animateTo(nearestSlot(currentY), { duration: 400 });` | Drag/drop is high-frequency direct manipulation; 400ms snap may slow throughput | Shorten snap, use distance-aware cap, provide reduced-motion snap/near-instant settle |
| P2 | Motion definitions are split across tokens, CSS, arbitrary utility, and imperative code | Evidence spans global CSS, component CSS, TSX utility class, JS animation call | Harder to keep product motion coherent | Normalize named component states around shared tokens and local precedents |

---

## 3. Implementation plans

### Plan A — Establish a motion contract and Reduced Motion baseline

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

**Target behavior**

- All motion uses semantic duration/easing tokens unless there is a documented local reason.
- Reduced Motion does not remove all feedback; it shortens or simplifies motion while preserving state change.
- High-frequency controls favor fast transform/opacity transitions over decorative movement.

**Project conventions to preserve**

- Keep existing token names.
- Preserve the `Button.css` precedent: transform-based feedback plus shortened Reduced Motion duration.
- Do not introduce unrelated visual styling, gradients, shadows, or global resets.

**Ordered steps**

1. In `src/styles/motion.css`, add missing semantic tokens without deleting existing ones, for example:
   - `--duration-instant: 80ms`
   - `--duration-fast: 160ms`
   - `--duration-panel: 240ms`
   - optional `--duration-attention: 220ms`
   - keep `--ease-responsive`
   - add optional exit easing only if used consistently.
2. Add a global Reduced Motion token override:
   - keep feedback duration around `80ms`
   - avoid setting all durations to `0ms` unless a specific component needs no travel.
3. Replace component hard-coded durations/easings incrementally with tokens.
4. Prefer animating only `opacity` and `transform`.
5. Add a lightweight convention comment near tokens explaining:
   - command surfaces: fast
   - panels/popovers: panel duration
   - alerts/toasts: attention duration
   - direct manipulation settle: short and distance-aware.

**Hard boundaries**

- Do not change product layout, copy, component hierarchy, or data behavior.
- Do not globally disable transitions.
- Do not introduce new animation libraries based only on this evidence.
- Do not claim performance improvement until runtime measurement exists.

**Mechanical checks**

- Search for `transition: all`.
- Search for hard-coded `ms` in component CSS/TSX animation declarations.
- Search for `ease-in` on interactive surfaces.
- Confirm each edited animated component has a `prefers-reduced-motion: reduce` path or consumes a reduced token.

**Runtime/feel checks to perform later**

- Keyboard-open command palette repeatedly and confirm it feels immediate, not theatrical.
- Trigger popovers and toasts in normal and Reduced Motion modes.
- Confirm visible state feedback remains in Reduced Motion.
- Check that focus rings remain visible during and after animated state changes.

**Reduced Motion behavior**

- Use shortened transform/opacity transitions, generally around `80ms`.
- Avoid large spatial travel.
- Preserve opacity or subtle scale feedback so users still perceive state changes.

**Source-drift stop condition**

- Stop before implementation if `src/styles/motion.css` no longer owns global motion tokens, if `Button.css` has changed its Reduced Motion convention, or if a design authority file now defines different durations/easings.

---

### Plan B — Normalize command palette and popover motion

**Current excerpts**

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

`src/styles/motion.css`

```css
.popover {
  transform-origin: center;
  transition: all 360ms ease-in;
}
```

**Target behavior**

- Command palette opens quickly and causally from the user action.
- Popovers use restrained opacity/transform motion.
- Both surfaces use named CSS states instead of one-off arbitrary animation strings where practical.
- Motion is fast enough for keyboard-heavy repeated use.

**Project conventions to preserve**

- Use existing semantic tokens.
- Keep `data-open={open}` as a useful state hook.
- Preserve component API unless existing callers require otherwise.
- Follow local precedent of transform-based motion from `Button.css`.

**Ordered steps**

1. Replace the arbitrary command palette animation class with a stable class name, for example:
   - `className="commandPalette"`
   - keep `data-open={open}`.
2. Define command palette motion in an appropriate stylesheet already used by the component, or a component-local CSS file if one exists.
3. Suggested behavior:
   - closed: `opacity: 0; transform: translateY(-4px) scale(0.985); pointer-events: none;`
   - open: `opacity: 1; transform: translateY(0) scale(1); pointer-events: auto;`
   - transition: `opacity var(--duration-fast) var(--ease-responsive), transform var(--duration-fast) var(--ease-responsive)`.
4. If the component unmounts when closed elsewhere, coordinate with that lifecycle before relying on exit transitions.
5. Replace `.popover` transition with:
   - `transition-property: opacity, transform;`
   - `transition-duration: var(--duration-panel);`
   - `transition-timing-function: var(--ease-responsive);`
6. Ensure no layout-affecting properties are included in popover transition declarations.
7. Add Reduced Motion overrides for both:
   - shorter duration
   - no or minimal translation/scale.

**Hard boundaries**

- Do not alter search result rendering or filtering.
- Do not change focus management based only on the motion evidence.
- Do not assume the command palette currently has working exit animation; lifecycle is unverified.
- Do not remove `data-open` unless all styling/state consumers are checked.

**Mechanical checks**

- Confirm `animate-[palette_420ms_ease-in_both]` is gone or intentionally isolated.
- Confirm `.popover` no longer uses `transition: all`.
- Confirm no `420ms`, `360ms ease-in`, or broad `all` transition remains for these surfaces.
- Confirm Reduced Motion rules exist.

**Runtime/feel checks to perform later**

- Open command palette from keyboard repeatedly.
- Close it with the expected key/mouse path.
- Verify focus indication is visible before, during, and after the transition.
- Verify popover placement does not visually drift or animate from an unrelated origin.
- Verify Reduced Motion still communicates open/closed state without spatial travel.

**Reduced Motion behavior**

- Command palette: fade or near-instant opacity change around `80ms`; avoid scale/vertical travel.
- Popover: short opacity transition; avoid transform travel unless extremely small.

**Source-drift stop condition**

- Stop if `CommandPalette` now delegates animation to another component, portal, transition helper, or design-system primitive not shown in the excerpt.
- Stop if `.popover` is generated or owned by a third-party component stylesheet where direct edits would be overwritten.

---

### Plan C — Rework toast entry and queue drag settle for direct manipulation

**Current excerpts**

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

- Toasts enter as quick operational feedback, using transform/opacity rather than positional layout animation.
- Dragged queue items track the pointer directly while dragging and settle quickly into the nearest valid slot.
- Reduced Motion preserves feedback without long travel or delayed settle.

**Project conventions to preserve**

- Use semantic motion tokens.
- Prefer transform-based animation.
- Preserve existing queue data behavior and nearest-slot logic.
- Keep pointer interaction causality: pointer movement should map clearly to item movement.

**Ordered steps**

1. In `src/components/toast.css`, replace `top` keyframe animation with transform/opacity:
   - from: `transform: translateY(-8px); opacity: 0;`
   - to: `transform: translateY(0); opacity: 1;`
2. Reduce toast duration from `500ms ease-in` to a tokenized value:
   - likely `var(--duration-panel)` or a dedicated attention duration around `220ms`.
   - use `var(--ease-responsive)`.
3. Add Reduced Motion:
   - no vertical travel or minimal `translateY(-2px)`
   - duration around `80ms`.
4. In `SortableQueue.tsx`, keep pointer move direct, but ensure the visual consumer of `--drag-y` uses `transform`, not `top`; this is unverified from the snippet and must be checked before editing.
5. Replace fixed `duration: 400` with a shorter token-aligned value or named constant:
   - normal settle target: about `160–220ms`
   - cap duration for long distances if distance-aware duration is introduced.
6. Add Reduced Motion branch for pointer-up settle:
   - near-instant snap or very short settle around `80ms`
   - preserve final-slot feedback.
7. If `animateTo` accepts easing, use the shared responsive easing; if not, do not invent an API without checking its signature.

**Hard boundaries**

- Do not change queue sorting rules, slot calculation, or selected item state.
- Do not assume `clientY` is wrong from static evidence alone; coordinate handling needs runtime/layout context.
- Do not rewrite drag/drop architecture without validating existing constraints.
- Do not remove animation entirely for normal motion users.

**Mechanical checks**

- Confirm toast keyframes no longer animate `top`.
- Confirm `.toast` no longer uses `500ms ease-in`.
- Confirm Reduced Motion exists in `toast.css`.
- Confirm queue settle duration is not a hard-coded `400` without a named reason.
- Check `animateTo` API before adding easing or cancellation options.
- Check CSS consuming `--drag-y` before changing coordinate math.

**Runtime/feel checks to perform later**

- Trigger toasts repeatedly and verify they do not feel blocking.
- Drag queue items slowly and quickly; visual item should stay under the pointer as closely as the existing architecture allows.
- Release near and far from a slot; settle should feel causal, not delayed.
- Test cancellation/interruption if another drag starts before settle finishes.
- Test Reduced Motion for both toast and drag release.

**Reduced Motion behavior**

- Toast: short fade with no meaningful vertical travel.
- Queue: direct drag remains direct; release settles almost immediately to the target slot with clear final position.

**Source-drift stop condition**

- Stop if toast rendering has moved to a shared notification system.
- Stop if `SortableQueue` now uses a drag library, spring system, virtualization layer, or different `animateTo` contract not shown in the excerpt.

---

## 4. Recommended execution order

1. **Plan A first:** establish the shared motion and Reduced Motion contract.
2. **Plan B second:** fix high-frequency command palette and broad popover transition.
3. **Plan C third:** convert toast layout animation and tune queue settle behavior.

## Explicitly unverified states

- Actual computed styles and final CSS cascade.
- Whether command palette remains mounted while closed.
- Whether `palette` keyframes exist elsewhere.
- Whether `.popover` has open/closed state classes elsewhere.
- Whether toast positioning depends on `top` for layout.
- How `--drag-y` is consumed visually.
- `animateTo` API shape, easing support, cancellation behavior, and interruption behavior.
- Keyboard focus order, focus trapping, screen reader behavior, and accessibility tree.
- Runtime performance, frame timing, input latency, and perceived feel on real devices.
