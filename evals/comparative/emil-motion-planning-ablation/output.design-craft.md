## 1. Recon summary

**Motion diagnosis:** the snippets show a useful local precedent for crisp transform-based feedback, but several higher-frequency or state-continuity surfaces drift into long `ease-in`, keyframed, layout-property, or non-interruptible-looking motion that is risky for a calm keyboard-heavy operations console.

- **Stack signals:** React/TSX components, CSS custom-property tokens, plain CSS transitions/keyframes, Tailwind-style arbitrary animation utility, and a JS `animateTo(...)` gesture settle call.
- **Where motion lives:** `src/styles/motion.css`, component-level TSX class strings, component CSS files, pointer handlers, and local component CSS precedents.
- **Existing conventions evidenced:** `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`, transform-based button press, and a local `prefers-reduced-motion` branch.
- **Product personality:** calm, crisp, low-latency utility motion; motion should explain state/causality, not add ceremony.
- **Frequency map:** buttons and command palette = high-frequency; sortable queue = repeated direct manipulation; popovers = regular overlays; toasts = occasional status feedback.
- **Evidence level:** static excerpts only. No runtime smoothness, computed styles, keyframe definitions beyond shown CSS, accessibility tree, screen recording, trace, or device validation was performed.

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | `animate-[palette_420ms_ease-in_both]` | `src/components/CommandPalette.tsx` | High-frequency keyboard surface uses a long one-off `ease-in` animation; static evidence does not show a Reduced Motion path. | Replace with state-driven opacity/very small transform using `--duration-fast`/`--duration-panel` and `--ease-responsive`; Reduced Motion keeps feedback without travel. |
| P1 | `animateTo(nearestSlot(currentY), { duration: 400 })` and pointer move writes `--drag-y` | `src/components/SortableQueue.tsx` | Direct manipulation excerpt does not evidence pointer capture, grab offset, presentation-value interruption, or measured release velocity; fixed-duration settle risks discontinuity. | Define coordinate space, preserve grab offset, track px/s velocity, settle from current presentation value, pass velocity into the settle; preserve existing nearest-slot target unless momentum targeting is explicitly authorized. |
| P2 | `transition: all 360ms ease-in` | `src/styles/motion.css` | Popover motion owns all properties, uses slow-start easing, and uses center origin without evidence that every popover is centered. | Limit to `opacity, transform`, use responsive token timing/easing, and make origin trigger-relative or split centered modal usage from anchored popovers. |
| P2 | `top: -24px` to `top: 0`; `500ms ease-in` | `src/components/toast.css` | Toast entrance animates a layout property and is longer/slower than the evidenced panel token; no Reduced Motion branch shown. | Move final position to static style; animate `transform` + `opacity` with token duration/easing; Reduced Motion uses short fade/static state. |
| P2 | Button has RM branch; other snippets do not show one | Multiple | Reduced Motion convention appears local, not evidenced across overlay, toast, palette, or drag settle motion. | Add component-scoped RM branches that remove large travel/elasticity but preserve opacity/color/focus/static feedback. |
| P3 | `360ms`, `420ms`, `500ms`, `400` alongside `160ms`/`240ms` tokens | Multiple | Motion vocabulary is drifting into one-off values that can make the console feel inconsistent. | Prefer existing semantic tokens; add a new semantic token only if repeated use cannot be represented by `fast`/`panel`. |

## 3. Implementation plans

### Plan A — Normalize popover and toast motion around tokenized transform/opacity

**Current excerpts**

- `src/styles/motion.css`
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

- `src/components/toast.css`
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

- Popovers respond immediately and feel anchored to their trigger unless the component is truly centered.
- Toasts enter as status feedback without layout-position animation.
- Motion uses existing `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Reduced Motion removes vertical travel and preserves feedback through opacity/static final state.

**Project conventions to preserve**

- Keep semantic CSS tokens.
- Keep localized `prefers-reduced-motion` behavior like the button precedent.
- Prefer `transform`/`opacity`; avoid `transition: all`.

**Ordered steps**

1. Inspect all `.popover` consumers before editing.
2. If `.popover` is used only for anchored overlays, change origin to a trigger-aware value, e.g. `var(--popover-origin, top center)`.
3. If `.popover` is also used for centered dialogs, split the centered case rather than forcing all popovers away from `center`.
4. Replace `transition: all 360ms ease-in` with explicit `opacity` and `transform` transitions using existing tokens.
5. In `toast.css`, move final placement such as `top: 0` into the base `.toast` rule if the component relies on it.
6. Replace toast keyframe `top` movement with `transform: translateY(...)` plus opacity.
7. Add `@media (prefers-reduced-motion: reduce)` branches for `.popover` and `.toast`.

**Hard boundaries**

- Do not change toast lifecycle, stacking, dismissal timing, or z-index behavior.
- Do not introduce a motion library.
- Do not globally alter the existing token values.
- Do not change centered overlay origins unless consumer inspection proves they are popovers, not dialogs.

**Mechanical checks**

- Run the project’s configured lint/type-check/build commands.
- Search for remaining `transition: all`, `500ms ease-in`, and `top` inside animation keyframes touching these files.
- Confirm CSS parses after any keyframe/media additions.

**Runtime/feel checks required later, not performed here**

- Trigger popovers from keyboard and pointer; confirm response starts immediately.
- Trigger stacked and repeated toasts; confirm no visible layout jump.
- Emulate Reduced Motion; confirm toast/popover still communicate state without vertical travel.
- Inspect computed animation properties to verify `top` is not animated.

**Reduced Motion behavior**

- Popover: no scale/travel, short opacity transition or immediate final state.
- Toast: no vertical translation; short opacity/status appearance, final position stable.

**Source-drift stop condition**

- Stop before editing if `.popover`, `.toast`, token names, or toast positioning no longer match the excerpts, or if `.popover` consumers mix anchored overlays and centered dialogs without a clear class split.

---

### Plan B — Retune command palette motion for high-frequency keyboard use

**Current excerpt**

- `src/components/CommandPalette.tsx`
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

- Opening/closing feels immediate and does not slow keyboard throughput.
- Motion is state-driven from `open`, not a long always-applied arbitrary keyframe.
- Entry/exit uses opacity and minimal vertical/scale change only if it improves spatial continuity.
- Reduced Motion removes travel while preserving open/closed feedback.

**Project conventions to preserve**

- Use existing duration/easing tokens.
- Keep the component API unchanged: `CommandPalette({ open })`.
- Preserve search results rendering and command behavior.
- Preserve visible focus requirements; do not hide focus with animation styles.

**Ordered steps**

1. Locate the `palette` keyframe definition, if any, before replacing the class.
2. Replace `animate-[palette_420ms_ease-in_both]` with state-based classes or a local CSS class keyed by `data-open`.
3. Use `--duration-fast` for very small feedback or `--duration-panel` only if the palette is panel-sized.
4. Use `--ease-responsive`; do not use `ease-in` for the first response.
5. For closed state, add only safe visual/pointer behavior that matches existing lifecycle conventions, e.g. opacity/transform and possibly `pointer-events: none`.
6. Add a Reduced Motion branch: duration around the button precedent’s reduced path and no translation/scale.
7. Remove the obsolete `palette` keyframe only if no other component uses it.

**Hard boundaries**

- Do not redesign the command palette.
- Do not add focus trapping or command routing changes in this motion-only pass unless existing tests require a small compatibility adjustment.
- Do not convert mount/unmount lifecycle without confirming how the palette is currently opened and closed.
- Do not add a dependency.

**Mechanical checks**

- Run configured lint/type-check/build.
- Search for other references to `palette` before deleting or renaming any keyframe.
- Verify no arbitrary `420ms ease-in` palette animation remains.

**Runtime/feel checks required later, not performed here**

- Open via keyboard shortcut repeatedly; response should begin immediately.
- Type during/after open; input should not be blocked by animation.
- Close via Escape and reopen quickly; no keyframe restart flash or stale closed visual.
- Emulate Reduced Motion; confirm no travel and preserved open/closed feedback.

**Reduced Motion behavior**

- No translate/scale.
- Short opacity transition or immediate state change.
- Focus ring remains visible and is not delayed.

**Source-drift stop condition**

- Stop if the component no longer uses the shown `className`, if `open` no longer controls visibility, if the palette keyframe is shared by unrelated surfaces, or if the project has a newer command-palette motion convention.

---

### Plan C — Repair sortable queue direct manipulation and settle continuity

**Current excerpt**

- `src/components/SortableQueue.tsx`
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

- Dragged item tracks 1:1 with the pointer after intent is established.
- No jump on grab, move, release, or interruption.
- Release animation starts from the current presentation value and inherits measured velocity.
- Existing target semantics stay `nearestSlot(currentY)` unless product authority explicitly approves momentum-based target selection.
- Reduced Motion removes elastic/throw effects but keeps direct manipulation and clear slot feedback.

**Project conventions to preserve**

- Keep current queue ordering rules and nearest-slot behavior by default.
- Keep React state for logical dragging state, not per-frame pointer position.
- Use transform-driven visual movement where existing CSS allows.
- Avoid synchronous layout work in the pointer-move hot path.

**Ordered steps**

1. Inspect queue markup/CSS to identify the actual transform owner for the dragged item.
2. If press feedback and drag both write `transform`, split into wrapper layers or compose transforms in one explicit owner.
3. On pointer down, capture pointer, record pointer id, container/item bounds, current presentation y, and grab offset.
4. Establish coordinate space in CSS pixels: `clientY - containerTop - grabOffsetY` or the project’s equivalent local coordinate.
5. Track a short movement history with monotonic timestamps; compute release velocity in CSS px/s.
6. On pointer move, update only the dragged visual transform/CSS variable, preferably batched to the display frame.
7. On pointer up/cancel, release pointer capture and compute current presentation y.
8. Choose target with existing `nearestSlot(currentY)` unless momentum target selection is separately authorized.
9. Pass measured release velocity into the settle animation API if supported; if the API lacks velocity support, replace only the settle primitive with a compatible spring/WAAPI approach after confirming dependency policy.
10. Add interruption handling so a new drag starts from the current on-screen value, not the last logical target.
11. Add Reduced Motion branch: no bounce/elastic overshoot, shortened settle, static slot highlight retained.

**Hard boundaries**

- Do not change persistence, queue data model, slot calculation semantics, or destructive reorder thresholds.
- Do not silently switch to projected-endpoint target selection.
- Do not lock pointer input until a settle completes.
- Do not add broad parent CSS-variable updates if the queue contains many descendants without measuring style recalculation.

**Mechanical checks**

- Run configured lint/type-check/build and any component tests around reorder behavior.
- Add or update unit tests for coordinate conversion, nearest-slot target preservation, and velocity calculation if the project has test infrastructure.
- Verify pointer-cancel path is handled, not only pointer-up.

**Runtime/feel checks required later, not performed here**

- Drag from different grab points; item should not snap under the pointer.
- Drag outside original bounds; pointer capture should preserve tracking.
- Release slowly and quickly; settle should begin from current position with no jump.
- Interrupt mid-settle with a new drag; no reset to previous logical target.
- Test Reduced Motion; no elastic throw, but drag and slot state remain understandable.
- If momentum targeting is proposed later, compare projected endpoint behavior separately from velocity handoff.

**Reduced Motion behavior**

- User-controlled drag remains 1:1.
- Release settle is short, non-bouncy, and may snap nearly immediately.
- Slot/focus/selection feedback remains visible through static highlight, opacity, or color.

**Source-drift stop condition**

- Stop if `animateTo` already supports a different velocity API, if `currentY` is no longer the release position, if CSS no longer uses `--drag-y`, or if product rules define non-nearest reorder targeting.

## 4. Recommended execution order

1. **Plan A first** to re-anchor the shared motion vocabulary and remove the clearest CSS risks.
2. **Plan B next** because command palette is high-frequency and keyboard-heavy.
3. **Plan C last** because direct manipulation requires the most runtime feel validation and may depend on animation API capabilities.

## Explicitly unverified states

- Actual `palette` keyframe definition and whether it is shared.
- Computed CSS for `.popover`, `.toast`, and queue transform ownership.
- Popover consumer types: anchored overlay vs centered dialog.
- Toast base positioning, stacking, lifecycle, and repeated-trigger behavior.
- `animateTo` implementation, interruption behavior, and velocity support.
- Pointer capture, grab offset, pointer-cancel, and multi-pointer handling outside the shown snippet.
- Runtime smoothness, frame pacing, layout/paint/composite cost, and behavior under representative load.
- Accessibility tree, focus management, keyboard trap behavior, and screen-reader timing.
- Reduced Motion behavior beyond the shown button precedent.
