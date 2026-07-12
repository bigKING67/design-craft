## 1. Recon summary

- **Stack signals:** React/TSX components, CSS modules or colocated CSS, global CSS tokens, Tailwind-style arbitrary animation utility, imperative drag animation.
- **Where motion lives:**  
  - Global motion/tokens: `src/styles/motion.css`  
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`  
  - JSX utility class: `src/components/CommandPalette.tsx`  
  - Imperative interaction code: `src/components/SortableQueue.tsx`
- **Existing conventions:** Semantic CSS tokens exist for duration/easing:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
  - Existing Reduced Motion precedent shortens feedback rather than removing it: `.button { transition-duration: 80ms; }`
- **Product personality:** Calm, crisp, workday operations console. Motion should clarify cause/effect and preserve state continuity without feeling decorative or delaying keyboard-heavy workflows.
- **Frequency map from component roles, not runtime data:**
  - High frequency: buttons, command palette, queue sorting/dragging.
  - Medium frequency: popovers.
  - Intermittent but attention-sensitive: toasts.
- **Evidence level:** Static excerpt audit only. No runtime behavior, computed styles, browser validation, device testing, accessibility-tree inspection, performance trace, or user testing was performed.

---

## 2. Vetted priority table

| Priority | Finding | Evidence | Risk | Recommended direction |
|---|---|---|---|---|
| P0 | Reduced Motion is not consistently represented across shown motion surfaces | Only `Button.css` excerpt includes `@media (prefers-reduced-motion: reduce)` | Users requesting reduced motion may still receive long/large animations | Add per-surface Reduced Motion paths that preserve feedback with shorter/fewer transforms |
| P1 | Popover uses broad, slow, non-tokenized transition | `.popover { transition: all 360ms ease-in; }` | `all` may animate unintended properties; 360ms ease-in can feel sluggish for operational UI | Restrict to opacity/transform, use existing tokens/ease, add Reduced Motion |
| P1 | Command palette uses arbitrary 420ms ease-in animation | `className="animate-[palette_420ms_ease-in_both]"` | Long keyboard-invoked motion may slow perceived throughput; bypasses token convention | Replace with semantic class/tokenized duration and state-driven open/close behavior |
| P1 | Sortable queue settle animation uses hardcoded 400ms | `animateTo(nearestSlot(currentY), { duration: 400 });` | Drag/drop completion may feel delayed; no shown Reduced Motion branch | Use token-equivalent duration/ease; shorten or simplify in Reduced Motion |
| P2 | Toast animates layout property over 500ms | `from { top: -24px; ... }` and `animation: ... 500ms ease-in` | Layout-affecting animation and long ease-in may feel heavy for feedback | Animate transform/opacity with tokenized timing; shorten in Reduced Motion |
| P2 | A correct local precedent exists but is not generalized | `Button.css` uses `var(--duration-fast)` and `var(--ease-responsive)` | Motion style may drift component-by-component | Treat button pattern as the local implementation precedent |

---

## 3. Implementation plans

### Plan A — Normalize global/component CSS motion tokens for popovers and toasts

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

- Popovers feel immediate and causal: small opacity/scale/translate transition, not a broad `all` transition.
- Toasts enter clearly without layout-property animation.
- Motion uses existing semantic duration/easing tokens.
- Reduced Motion keeps feedback visible but shorter/subtler.

**Project conventions to preserve**

- Reuse existing CSS variables instead of introducing one-off durations.
- Follow the existing button precedent: tokenized timing plus Reduced Motion override.
- Keep focus visibility untouched.
- Avoid broad global changes beyond the affected selectors/keyframes.

**Ordered steps**

1. In `src/styles/motion.css`, replace `.popover` transition from `all 360ms ease-in` to explicit properties, for example:
   - `opacity var(--duration-panel) var(--ease-responsive)`
   - `transform var(--duration-panel) var(--ease-responsive)`
2. Confirm whether `.popover` has existing open/closed state selectors elsewhere before adding new state selectors. If state selectors are absent, stop and inspect the real component before inventing state names.
3. In `src/components/toast.css`, replace `top` keyframe movement with `transform: translateY(...)`.
4. Reduce toast duration to `var(--duration-panel)` or `var(--duration-fast)` depending on existing toast density in the real codebase.
5. Add `@media (prefers-reduced-motion: reduce)` overrides:
   - Popover: shorter duration, minimal transform or opacity-only.
   - Toast: shorter duration, opacity plus very small translate or opacity-only.
6. Do not remove opacity changes; Reduced Motion should still communicate feedback.

**Hard boundaries**

- Do not rename selectors without checking all usages.
- Do not introduce new token names unless the existing tokens are insufficient after inspecting the full style system.
- Do not animate layout properties such as `top`, `left`, `width`, or `height` for these entrances unless a verified existing pattern requires it.
- Do not change toast placement, stacking, z-index, or dismissal behavior.

**Mechanical checks**

- Search for `.popover`, `toast-enter`, and `.toast` usages before changing selectors.
- Run the closest available CSS/frontend validation command, likely one of:
  - lint
  - type-check
  - build
- Re-read the final diff to ensure no unrelated style changes were included.

**Runtime/feel checks to perform later**

- Verify popover open/close feels under roughly a quarter second.
- Verify toast entry is noticeable but not attention-grabbing.
- Verify no focus outline is hidden or delayed.
- Verify repeated toasts do not feel sluggish.

**Reduced Motion behavior**

- Use shorter duration, approximately matching the existing `80ms` precedent.
- Preserve opacity or instant positional continuity; do not silently remove feedback.

**Source-drift stop condition**

- Stop if the real files no longer contain the shown selectors/keyframes or if `.popover`/`.toast` state is controlled by a different abstraction not present in the excerpts.

---

### Plan B — Make command palette motion semantic, state-driven, and keyboard-fast

**Current excerpt**

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

- Command palette opens with crisp, calm continuity appropriate for keyboard-heavy users.
- Timing follows project motion tokens instead of an arbitrary utility duration.
- Open/closed visual state is controlled by `data-open`, CSS selectors, or an existing animation utility pattern.
- Reduced Motion keeps open/close feedback but shortens/simplifies it.

**Project conventions to preserve**

- Existing semantic tokens from `src/styles/motion.css`.
- Existing Reduced Motion precedent from `src/components/Button.css`.
- Do not reduce keyboard throughput or delay search input availability.
- Do not alter command palette data loading, search behavior, focus management, or result rendering.

**Ordered steps**

1. Inspect the full `CommandPalette.tsx` file and any palette-related CSS/keyframes before implementation.
2. Replace the arbitrary `animate-[palette_420ms_ease-in_both]` with a named class or existing local style hook, for example a semantic class such as `command-palette`.
3. Use `data-open={open}` as the state source if that is already the component contract.
4. Define or update CSS so `[data-open="true"]` uses tokenized opacity/transform transition around `var(--duration-panel)` and `var(--ease-responsive)`.
5. Define the closed state explicitly if the component remains mounted while closed.
6. Add Reduced Motion override with shorter duration and reduced transform distance.
7. Ensure the palette contents remain interactable according to the existing open/closed behavior; do not invent accessibility behavior from the snippet alone.

**Hard boundaries**

- Do not change focus trapping, keyboard shortcuts, selected result state, or search result logic.
- Do not assume whether the palette unmounts when closed; verify in the real file first.
- Do not add a delayed mount/unmount pattern unless the existing component already supports it.
- Do not use long entrance animation for a keyboard-invoked command surface.

**Mechanical checks**

- Search for `palette`, `CommandPalette`, `data-open`, and arbitrary `animate-[palette` usage.
- Confirm the CSS file where palette styles should live before adding styles.
- Run type-check/lint/build as available.
- Confirm no Tailwind build constraints are violated if replacing arbitrary utilities with CSS classes.

**Runtime/feel checks to perform later**

- Open via keyboard shortcut and verify the input is usable immediately.
- Reopen repeatedly and check that motion feels crisp rather than ceremonial.
- Verify close transition does not block the next command.
- Verify focus indication remains visible.

**Reduced Motion behavior**

- Shorten to the local Reduced Motion precedent, approximately `80ms`.
- Prefer opacity plus minimal transform, or opacity-only if movement is uncomfortable.
- Preserve state feedback; do not make open/close visually ambiguous.

**Source-drift stop condition**

- Stop if `CommandPalette.tsx` no longer contains the arbitrary animation class or if palette styling is centralized in a design-system primitive that should be changed instead.

---

### Plan C — Tokenize and reduce sortable queue drag-settle motion

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

- Drag movement remains direct and responsive.
- Drop/settle animation preserves spatial continuity but does not delay the operator.
- Hardcoded `400` duration is replaced with a token-aligned value or nearby local constant.
- Reduced Motion shortens or simplifies settle behavior while preserving final-position feedback.

**Project conventions to preserve**

- Existing timing vocabulary: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
- Existing pattern that Reduced Motion still provides feedback.
- Pointer interaction code should stay minimal and avoid broad refactors.

**Ordered steps**

1. Inspect the full `SortableQueue.tsx` file to identify:
   - Where `currentY` is updated.
   - What `animateTo` is imported from.
   - Whether `animateTo` accepts easing.
   - Whether a Reduced Motion hook/helper already exists.
2. Inspect CSS consuming `--drag-y` to verify it drives `transform` rather than layout properties.
3. Replace `{ duration: 400 }` with a token-aligned constant, likely equivalent to `--duration-panel` for settle or `--duration-fast` for small snaps.
4. If `animateTo` accepts easing, pass the existing responsive easing equivalent.
5. Add a Reduced Motion branch:
   - Short duration, approximately `80ms`, or immediate snap if the animation library cannot safely shorten.
   - Preserve final slot update and visual confirmation.
6. Keep pointer-move update path direct; do not add expensive calculations inside `onPointerMove`.

**Hard boundaries**

- Do not rewrite drag architecture unless the current implementation cannot support reduced motion.
- Do not change sorting semantics, nearest-slot logic, or queue data state.
- Do not introduce new global event listeners without checking cleanup.
- Do not assume performance problems from the snippet alone; verify before optimizing beyond the duration/easing issue.

**Mechanical checks**

- Search for `animateTo`, `--drag-y`, `nearestSlot`, and `prefers-reduced-motion`.
- Type-check after changes.
- If tests exist for sorting/reordering, run the closest relevant test.
- Re-read diff for accidental behavior changes to queue ordering.

**Runtime/feel checks to perform later**

- Drag an item slowly and quickly; verify the item tracks pointer intent.
- Drop between nearby slots and distant slots; verify snap is clear but not slow.
- Verify keyboard or non-pointer reorder paths, if present, still communicate state.
- Verify Reduced Motion path still shows the item reaching the final slot.

**Reduced Motion behavior**

- Prefer shortened settle rather than removing all feedback.
- If reduced path snaps immediately, ensure final placement is visibly clear through position/state/focus styling.

**Source-drift stop condition**

- Stop if `animateTo` does not accept duration/easing options as shown, or if `--drag-y` is not used for visual movement in the current implementation.

---

## 4. Recommended execution order

1. **Plan A first:** establishes the shared CSS precedent and fixes the broadest token/RM drift in popover and toast motion.
2. **Plan B second:** command palette is likely high-frequency and keyboard-critical; align it after CSS conventions are clarified.
3. **Plan C third:** sortable drag needs slightly more implementation inspection because behavior depends on `animateTo`, pointer state, and CSS consumption of `--drag-y`.

## Explicitly unverified states

- No browser, device, screen reader, accessibility-tree, computed-style, trace, or user testing was performed.
- Actual component mounting/unmounting behavior is unknown.
- Existing palette keyframes and Tailwind configuration are unknown.
- Whether `animateTo` supports easing or Reduced Motion branching is unknown.
- Whether `--drag-y` is consumed by `transform` or layout-affecting properties is unknown.
- Existing global Reduced Motion helpers, if any, were not shown.
- Existing focus behavior and keyboard interaction behavior were not validated.

Applied frontend and quality delivery guardrails; this is an implementation roadmap only, with no file edits performed.
