## Verdict

**BLOCK — [Static evidence + product-fit risk]**  
This is not a shippable gesture sheet for a calm, repeatedly used operations app. The implementation breaks direct manipulation, animates layout properties, prevents interruption, ignores release velocity, and has no Reduced Motion path. Smoothness and device feel are **unverified** because this is a static review only.

## Prioritized findings

1. **P0 — Drag is not actually stateful direct manipulation.**  
   **[Static evidence]** `pointermove` always writes `sheet.style.top = event.clientY`, with no `dragging` flag, pointer id, threshold, or pointer capture. The sheet can move on hover/stray pointer movement and can lose tracking outside its bounds.

2. **P0 — The sheet will jump under the pointer.**  
   **[Static evidence]** `top = event.clientY` ignores the original sheet position and grab offset. `startY` is recorded but unused. A grabbed sheet should preserve where the user touched it and move by delta, not snap its top edge to the pointer.

3. **P0 — Reduced Motion requirement is unmet.**  
   **[Static evidence]** WAAPI always performs a `480ms` spatial travel animation; CSS also transitions broadly.  
   **[Product risk]** Reduced Motion should preserve collapsed/half/full feedback without large travel, e.g. instant state placement plus subtle handle/color/label feedback.

4. **P0 — Animating `top` is the wrong motion primitive.**  
   **[Static evidence]** pointer move and WAAPI both animate `top`; `offsetTop` is read during release.  
   **[Runtime risk]** This can trigger layout work and jank, especially in an operations app with dense content. Use compositor-friendly `transform: translateY(...)` for the moving layer.

5. **P0 — Interruption is blocked and also inconsistently guarded.**  
   **[Static evidence]** `pointerdown` returns while `animating`, but `pointermove` still updates `top`. There is no animation handle, cancel, retarget, or “start from current presentation value.”  
   **User impact]** If the user changes their mind mid-settle, the sheet should be immediately grabbable without a visual jump.

6. **P1 — Snap choice ignores velocity and intent.**  
   **[Static evidence]** `nearestSnapPoint(sheet.offsetTop)` only uses release position.  
   **Product risk]** A quick flick toward full/collapsed may snap back incorrectly. Sheet snap should use measured release velocity and a projected endpoint, with hysteresis around collapsed/half/full boundaries.

7. **P1 — Timing/easing feel mismatched to the product.**  
   **[Static evidence]** settle uses `480ms` and `ease-in`.  
   **Product fit]** For a repeated calm ops workflow, this is too delayed/cinematic. `ease-in` makes the beginning feel sluggish; settling should respond immediately and finish calmly.

8. **P1 — CSS creates conflicting and excessive motion.**  
   **[Static evidence]** `.sheet { transition: all 300ms; }` can animate unintended properties, including `top` and `transform`. `:active { transform: scale(0.96); }` scales the whole sheet during manipulation.  
   **Runtime risk]** Drag may feel rubbery rather than attached; press scale can fight future transform-based translation unless separated into layers.

9. **P2 — Animation lifecycle is fragile.**  
   **[Static evidence]** `fill: "forwards"` leaves an active animation effect without committing/canceling final styles. There is no cleanup on cancel, pointercancel, lost capture, route change, or rejected `finished` promise.

10. **P2 — Accessibility/state feedback is underspecified.**  
   **[Static evidence]** No keyboard equivalent, announced state, focus handling, or non-motion state feedback is shown.  
   **Product risk]** Collapsed/half/full state should be perceivable without relying on drag animation alone.

## Concrete direct-manipulation moves

1. **Use explicit sheet state.**  
   Model `collapsed | half | full` as snap states with measured pixel positions derived from viewport/container geometry.

2. **Move with transforms, not layout.**  
   Keep layout stable; apply `transform: translateY(var(--sheet-y))` to the motion layer. Avoid animating `top`.

3. **Separate transform ownership.**  
   Use nested wrappers if needed: outer wrapper owns `translateY`, inner wrapper owns subtle press/handle feedback. Do not let drag translation and active scale overwrite each other.

4. **Implement real drag state.**  
   On pointer down: cancel current settle animation, read current visual position, store pointer id, capture pointer, preserve grab offset, and start recording recent positions/timestamps.

5. **Track 1:1 after intent threshold.**  
   Use an 8–12px-ish threshold to distinguish tap/scroll from sheet drag. During drag, update from delta, not absolute `clientY`. Clamp or rubber-band beyond collapsed/full bounds.

6. **Settle from velocity, not just distance.**  
   On release, compute velocity in CSS px/s from recent samples, project the endpoint, choose the nearest intended snap point, then settle with a spring-like curve or critically damped easing. Default to no bounce for this product.

7. **Make interruption first-class.**  
   A new pointerdown during settle should stop/retarget from the current on-screen position, not the old logical target, and should not lock input.

8. **Replace broad CSS motion.**  
   Change `transition: all` to targeted transitions only for non-drag states, e.g. handle color/opacity. Disable transitions during active drag.

9. **Design Reduced Motion separately.**  
   When reduced motion is active: snap state immediately or with a very short non-spatial fade/handle highlight; avoid long travel, elastic overshoot, and large scale changes. Preserve clear collapsed/half/full feedback via label, handle state, shadow/material, or affordance change.

10. **Add cancellation and alternate input paths.**  
   Handle `pointercancel`, `lostpointercapture`, blur/visibility changes, multi-touch rejection, keyboard controls, and visible focus states.

## Verified / unverified boundaries

**Verified by static code review only:**

- Uses `top` for drag and settle animation.
- Uses `transition: all 300ms`.
- Uses `ease-in` and `480ms`.
- Does not show pointer capture, drag gating, velocity tracking, projected snap selection, interruption handling, or Reduced Motion branching.
- `startY` is unused in the shown implementation.

**Not verified:**

- Actual frame rate, smoothness, layout cost, or input latency.
- Browser-specific interaction between CSS `transition: all`, WAAPI `top`, and `fill: forwards`.
- Touch-device feel, scroll conflict, overscroll behavior, or lost pointer behavior.
- Exact snap positions and whether `nearestSnapPoint` handles viewport changes.
- Accessibility tree, keyboard behavior, focus order, or screen reader announcements.

No browser or device validation was performed.

## Smallest runtime validation plan

1. **Instrument one test page/state.**  
   Log current sheet position, active snap state, release velocity, projected endpoint, animation state, and pointer-capture status.

2. **Run five interaction checks.**  
   - Drag from each snap state: no jump on grab.  
   - Move outside sheet bounds: pointer remains captured.  
   - Slow release near midpoint: snaps predictably.  
   - Fast flick toward next state: velocity changes target.  
   - Grab during settle: no lockout and no visual jump.

3. **Run one Reduced Motion check.**  
   Enable reduced motion and verify collapsed/half/full feedback remains clear without large travel.

4. **Run one performance check.**  
   Record a short interaction trace and confirm drag/settle updates are transform/opacity-driven, with no repeated layout animation on `top`.

5. **Escalate only if needed.**  
   If browser results are ambiguous or touch feel matters for release, validate the same five checks on a real touch device before shipping.
