## Verdict

**Block — static evidence only.** The implementation is not production-ready for a calm, repeatedly used operations sheet because it breaks direct manipulation, animates layout properties, locks input during settle, lacks velocity/interruptibility, and has no Reduced Motion path.

## Prioritized findings

1. **P0 — Drag is not actually gated or captured.**  
   **Evidence:** `pointermove` always writes `sheet.style.top`, even if no valid drag started; `pointerdown` only records `startY`; no `setPointerCapture`, no active pointer id, no grab offset.  
   **Impact:** The sheet can jump to the pointer’s viewport Y, lose tracking outside bounds, and confuse taps with drags.

2. **P0 — Uses layout-position animation in the hot path.**  
   **Evidence:** drag and WAAPI animate `top`; settle reads `sheet.offsetTop`. CSS also declares `transition: all 300ms`.  
   **Impact:** This risks forced layout, broad style transitions, and poor behavior in a dense operations surface. Sheet motion should be compositor-friendly.

3. **P0 — Interaction is non-interruptible.**  
   **Evidence:** `if (animating) return;` rejects new `pointerdown` until `.finished`; animation starts from `sheet.offsetTop`, not necessarily the current visual presentation value.  
   **Impact:** A user cannot grab the sheet mid-flight; repeated daily use will feel laggy and untrustworthy.

4. **P1 — Settle physics are backwards for UI response.**  
   **Evidence:** `{ duration: 480, easing: "ease-in" }`.  
   **Impact:** `ease-in` delays the beginning of a user-triggered response; 480ms is heavy for a frequent operations control unless the distance is very large and intentional.

5. **P1 — Snap target ignores velocity and hysteresis.**  
   **Evidence:** `nearestSnapPoint(sheet.offsetTop)` only uses release position; no movement threshold, velocity samples, bounded projection, or boundary resistance.  
   **Impact:** Quick flicks and slow drags resolve the same way; small accidental motion may move the sheet.

6. **P1 — Reduced Motion requirement is absent.**  
   **Evidence:** no `prefers-reduced-motion` branch; same large spatial travel always runs.  
   **Impact:** Violates the stated requirement. Reduced Motion should preserve state feedback without long travel.

7. **P2 — Transform ownership conflicts.**  
   **Evidence:** `.sheet:active { transform: scale(0.96); }` while the interaction should ideally use `transform: translateY(...)`; `transition: all` may animate unrelated properties.  
   **Impact:** Press feedback can overwrite or fight drag transforms unless separated into nested layers.

## Concrete direct-manipulation moves

1. **Track an explicit drag session.**  
   On `pointerdown`, store `pointerId`, `startPointerY`, current sheet Y, and `grabOffset`; call `setPointerCapture(pointerId)` after intent is established.

2. **Add intent hysteresis.**  
   Require about `8–12px` vertical movement before committing to sheet drag, so clicks/taps on controls inside the sheet remain usable.

3. **Move with transform, not top.**  
   Represent sheet position as `translateY(y)` on a dedicated moving layer. Keep layout snap points as numbers, not live `offsetTop` reads during the gesture.

4. **Separate transform owners.**  
   Use an outer layer for `translateY(...)` and an inner layer for press feedback like `scale(0.98)`, or compose both transforms in one controlled value.

5. **Update on the display frame.**  
   Coalesce pointermove values and apply one transform update per animation frame; avoid layout reads/writes in the pointermove hot path.

6. **Make settle interruptible.**  
   If the user presses during settle, cancel/read the current presentation Y, preserve current velocity, and retarget from that visible position without jumping.

7. **Measure release velocity.**  
   Keep recent samples in CSS px and monotonic time; compute release velocity in CSS px/s. Use it as the initial velocity for the settle animation.

8. **Separate target semantics from physics.**  
   Keep the product’s existing collapsed/half/full target rule if nearest-current-position is intentional. If momentum targeting is desired, compute a bounded projected endpoint, clamp it, then choose the nearest valid snap point.

9. **Use calm settle motion.**  
   Prefer a critically damped or near-damped spring, or a short responsive curve. Avoid `ease-in`; use immediate response at release.

10. **Implement Reduced Motion.**  
   Under `prefers-reduced-motion: reduce`, skip large animated travel or compress it to a very short state change; preserve feedback with state labels, subtle opacity/color, focus, or a brief non-spatial affordance.

## Verified / unverified boundaries

**Verified from the supplied static snippet:**

- No visible Reduced Motion branch is present.
- Pointer capture is not used.
- Drag writes `top` directly.
- Settle animates `top`.
- CSS uses `transition: all`.
- Settle uses `480ms ease-in`.
- Input is blocked while `animating` is true.
- Release target is based on `nearestSnapPoint(sheet.offsetTop)` only.
- `:active` writes `transform: scale(...)`.

**Not verified from static code:**

- Actual frame rate, jank, or layout cost.
- Whether surrounding CSS constrains `top` safely.
- Whether `nearestSnapPoint` has hidden hysteresis or clamping.
- Whether other code handles keyboard access, ARIA state, focus management, or snap-state announcements.
- Touch-device feel, trackpad behavior, browser differences, or 60/120Hz smoothness.
- Whether product semantics require nearest-position snapping or momentum-based snapping.

## Smallest runtime validation plan

1. **Gesture correctness:** drag from each snap state; verify no jump on pickup, pointer remains captured outside sheet bounds, and taps inside the sheet are not stolen before threshold.  
2. **Interruption:** release toward half/full, grab mid-settle, reverse direction; verify the sheet starts from the visible position with no snap-back.  
3. **Targeting:** compare slow drag vs fast flick using logged release velocity in CSS px/s; confirm whether product-approved target semantics are followed.  
4. **Reduced Motion:** enable reduced motion; verify state changes remain understandable without large spatial travel.  
5. **Performance smoke:** record one drag/settle under representative table load; confirm transform-only frame updates and no repeated layout reads in the gesture path.
