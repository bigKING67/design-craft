## Evidence-labeled verdict

**Verdict: Block for production gesture motion.**  
[E: code] The sheet is moved and animated with `top`, `offsetTop`, `transition: all`, fixed `480ms ease-in`, and an `animating` input lock.  
[E: product] This is a repeated-use operations surface with collapsed / half / full states and a Reduced Motion requirement.  
[Assessment] The implementation will likely feel laggy, jumpy, non-interruptible, and expensive under table/editor load; it also lacks a reduced-motion contract.

## Prioritized findings

### P0 — Direct manipulation is not actually 1:1
- [E: code] `pointermove` sets `sheet.style.top = event.clientY` regardless of whether a drag is active.
- [E: code] `startY` is captured but never used, so grab offset is not preserved.
- [E: code] `event.clientY` is viewport-relative, while `top` is relative to the positioned containing block.
- [Impact] The sheet can jump under the pointer, move without an intentional drag, and snap from the wrong coordinate space.
- [Fix] Track `isDragging`, `pointerId`, `startPointerY`, `startSheetY`, and use `current = startSheetY + deltaY`, clamped to valid sheet bounds.

### P0 — CSS transition fights the drag
- [E: code] `.sheet { transition: all 300ms; }`
- [E: code] Drag updates `top` on every `pointermove`.
- [Impact] Each drag frame may be eased by CSS instead of staying attached to the pointer; `all` also risks animating unrelated properties.
- [Fix] Disable settle transitions while dragging; animate only explicit properties. Prefer `transform: translateY(...)` for drag and settle.

### P0 — Non-interruptible settle breaks gesture feel
- [E: code] `if (animating) return` blocks new drags while the settle animation is running.
- [E: code] The animation starts from `sheet.offsetTop`, not necessarily the current presented visual value if interrupted.
- [Impact] Users cannot grab the sheet mid-flight; repeated operators will feel the UI ignoring them.
- [Fix] Allow interruption: cancel/retarget the current animation from the current visual position and hand off measured release velocity.

### P0 — Reduced Motion requirement is unmet
- [E: code] No `prefers-reduced-motion` branch.
- [E: product] Reduced Motion must preserve state feedback without large spatial travel.
- [Impact] The current implementation still performs large `top` travel and a 480ms spatial animation.
- [Fix] In reduced motion, avoid long sheet travel where possible: snap state immediately or use a very short opacity/border/handle/status change, while keeping collapsed / half / full state clear.

### P1 — Layout-property animation is a performance risk
- [E: code] `sheet.style.top`, `sheet.offsetTop`, and WAAPI `{ top: ... }`.
- [Impact] `top` mutation and `offsetTop` reads can trigger layout work; this is risky in a dense operations app with large tables and drawers.
- [Fix] Keep the sheet’s logical snap state in JS, but render movement through `transform: translate3d(0, y, 0)`.

### P1 — Timing/easing is wrong for a grabbed object
- [E: code] `{ duration: 480, easing: "ease-in" }`.
- [Impact] `ease-in` delays the first visible response after release; fixed duration ignores drag distance and velocity.
- [Fix] Use a critically damped or near-critically damped spring-like settle, or a shorter distance-aware `ease-out`/drawer curve. Preserve velocity on release.

### P1 — Snap selection ignores velocity and boundaries
- [E: code] `nearestSnapPoint(sheet.offsetTop)` uses only release position.
- [Impact] A fast flick may choose the “nearest” state instead of the intended next state.
- [Fix] Measure recent pointer samples in CSS px/s; compute a bounded projected endpoint; choose collapsed / half / full from that endpoint only if momentum targeting is desired, otherwise keep nearest-position but still hand off velocity to the settle.

### P1 — Pointer lifecycle is incomplete
- [E: code] No `setPointerCapture`, `pointercancel`, `lostpointercapture`, pointer-id filtering, or intent threshold.
- [Impact] The sheet can lose tracking when the pointer leaves the element; scroll/tap conflicts are likely.
- [Fix] Capture the pointer after an 8–12px vertical intent threshold, ignore secondary pointers, and clean up on cancel/lost capture.

### P2 — Press feedback is applied to the wrong object
- [E: code] `.sheet:active { transform: scale(0.96); }`
- [Impact] Scaling the entire sheet during drag feels like the panel is shrinking, not being grabbed. It also conflicts with the recommended `transform`-based translate unless composed carefully.
- [Fix] Put press feedback on the drag handle or use separate wrapper layers: outer wrapper owns `translateY`, inner handle owns subtle press feedback.

### P2 — State and animation completion are fragile
- [E: code] `.finished.then(...)` has no cancellation/error path.
- [E: code] `fill: "forwards"` holds the animation result but does not clearly commit the final logical state.
- [Impact] A canceled animation can leave `animating` stuck or visual and logical positions mismatched.
- [Fix] Commit the final snap state explicitly, clear/cancel animations safely, and keep DOM state attributes such as `data-state="half"` in sync.

## Concrete direct-manipulation moves

1. **Use a single position model**
   - Store snap points as CSS-pixel Y values or percentages resolved once per layout.
   - Render with `transform: translateY(var(--sheet-y))`, not `top`.

2. **Separate drag, settle, and state**
   - `dragging`: no transition, pointer-owned position.
   - `settling`: spring/WAAPI transform animation from current visual value.
   - `settled`: committed `collapsed | half | full` state.

3. **Preserve grab offset**
   - On pointerdown: record `startPointerY` and current sheet Y.
   - On move: `nextY = clamp(startSheetY + event.clientY - startPointerY, minY, maxY)`.

4. **Make release physical but bounded**
   - Keep the last few pointer samples.
   - Calculate release velocity in CSS px/s.
   - Use either nearest snap from current position or an authorized projected endpoint; clamp to collapsed / half / full.

5. **Make the sheet interruptible**
   - If a new drag starts during settle, cancel the running animation and begin from the current visual transform, not the old target.

6. **Replace broad CSS**
   - Before: `transition: all 300ms`.
   - After: explicit transition only for non-gesture visual feedback, e.g. `box-shadow`, `background-color`, or handle affordance.
   - Do not transition drag position during pointer tracking.

7. **Reduced Motion contract**
   - Normal: transform-based settle with velocity-aware response.
   - Reduced: no elastic travel, no long glide; snap quickly and confirm state through handle position, label, shadow/border, or short color/opacity feedback.

8. **Accessible state parity**
   - Provide keyboard controls for collapsed / half / full.
   - Expose current state textually.
   - Keep focus visible and do not rely on `:active` motion as the only feedback.

## Verified / unverified boundaries

- **Verified from static code:** layout-property animation, broad transition, missing reduced-motion branch, missing pointer capture/cancel handling, unused `startY`, fixed `ease-in` settle, input lock while animating.
- **Inferred risk, not runtime-proven:** jank severity, exact jump distance, whether CSS transition visibly lags pointer tracking, and whether `offsetTop` mismatches the visual position in the target browser.
- **Not validated:** real browser behavior, touch-device feel, 60Hz/120Hz smoothness, reduced-motion OS setting behavior, screen-reader output, keyboard flow, or performance under the 10,000-row table load.

## Smallest runtime validation plan

1. **Desktop pointer smoke**
   - Drag from handle and sheet body.
   - Verify no jump on pointerdown, no movement before drag intent, and tracking continues outside the sheet.

2. **Interruption check**
   - Release toward half/full, then grab mid-settle.
   - Expected: no input lock, no visual jump, retargets from current position.

3. **Snap behavior check**
   - Slow drag near thresholds and fast flick between collapsed / half / full.
   - Record whether target choice matches the intended contract.

4. **Reduced Motion check**
   - Enable `prefers-reduced-motion`.
   - Expected: state still changes clearly, but large spatial glide/elastic motion is removed or sharply shortened.

5. **Performance check**
   - Test while the dense table/editor surface is populated.
   - Inspect for layout thrash from `top`/`offsetTop`; target compositor-driven transform updates.
