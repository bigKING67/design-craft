## 1. Evidence level and design read

**Evidence level: L0 static source critique only.** Evidence is limited to the supplied JS/CSS and product context. No browser, device, frame timeline, computed style, pointer trace, or Reduced Motion validation was performed.

**Reading this as:** a web operations bottom sheet for repeated daily staff use, with calm utility motion, optimized for keeping task context while moving between `collapsed`, `half`, and `full`.

**Verdict: Block implementation approval.** The interaction has the right product need—stateful direct manipulation—but the current motion model breaks causality, interruption, accessibility, and likely performance.

## 2. Should this motion exist?

**Yes, but only as causal motion.**

Should exist:
- Immediate pointer-down acknowledgement.
- 1:1 drag tracking after intent is clear.
- Short settle motion to the chosen snap point.
- Non-spatial state feedback in Reduced Motion.

Should not animate:
- Continuous drag via `transition: all`.
- Layout `top` during every pointer move.
- Full-sheet `scale(0.96)` while manipulating operational content.
- Long `480ms ease-in` settling.
- Any decorative bounce, shrink, or travel that delays repeated work.

## 3. Prioritized findings

1. **Blocking: drag is not true direct manipulation.**  
   Evidence: `pointermove` writes `sheet.style.top = event.clientY` directly; `startY` is recorded but unused. There is no drag flag, no intent threshold, no grab offset, and no pointer capture.  
   Reasoning: the sheet can snap its top edge to the pointer instead of preserving the finger’s relative grab point, which breaks object permanence.

2. **Blocking: the dragged property is layout-bound and globally transitioned.**  
   Evidence: JS mutates `top`; CSS has `transition: all 300ms`; WAAPI also animates `top`.  
   Reasoning: drag should track the pointer 1:1. A transition on `top` can make the sheet chase the pointer, while layout animation risks jank in a data-heavy operations app.

3. **Blocking: interaction is non-interruptible.**  
   Evidence: `animating` rejects `pointerdown` during settle; animation starts from `sheet.offsetTop`, not a guaranteed current presentation value.  
   Reasoning: a sheet must be grabbable mid-flight. Locking input until `.finished` makes the UI feel modal and can lose the user’s sense of control.

4. **Blocking: settle physics are backwards for user response.**  
   Evidence: `{ duration: 480, easing: "ease-in" }`; target uses `nearestSnapPoint(sheet.offsetTop)` only.  
   Reasoning: `ease-in` delays the start—the moment users most need confirmation. There is no measured release velocity, no velocity handoff, and no authorized projected endpoint behavior.

5. **Blocking: Reduced Motion is absent.**  
   Evidence: no `prefers-reduced-motion` branch.  
   Reasoning: the product explicitly requires state feedback without large spatial travel. Current code always performs positional travel and active scaling.

## 4. Concrete design moves

1. **Pointer-down feedback:**  
   On valid handle/sheet pointer-down, add a subtle pressed state immediately: handle color/opacity or a very small handle-only scale, not full-sheet shrink. Keep focus-visible independent.

2. **1:1 tracking:**  
   After an `8–12px` intent threshold, set `dragging = true`, call `setPointerCapture`, preserve `grabOffsetY = pointerY - currentSheetY`, and render `translateY(pointerY - grabOffsetY)`.

3. **Use transform ownership:**  
   Replace drag/settle animation of `top` with compositor-friendly `transform: translateY(...)`. If press feedback also uses transform, separate wrapper layers: outer translates, inner provides handle/press feedback.

4. **Presentation-value interruption:**  
   On new pointer-down during settle, cancel the running animation, read the current on-screen/presentation Y, start the drag from that value, and carry the current velocity instead of waiting for `.finished`.

5. **Velocity handoff:**  
   Track recent pointer samples with monotonic timestamps; compute release velocity in CSS px/s. Feed bounded release velocity into the settle spring even if target selection remains nearest snap point.

6. **Projected endpoints:**  
   Treat momentum targeting as a product decision. Candidate: compute a bounded projected endpoint from current Y + release velocity, then choose nearest snap point to that projection only if fast-flick semantics are approved.

7. **Soft boundaries:**  
   Clamp normal motion to valid snap range, but apply progressive resistance beyond `collapsed`/`full` instead of a hard stop. Remove elastic overshoot for this calm utility surface unless testing proves it improves control.

8. **Reduced Motion path:**  
   Under `prefers-reduced-motion: reduce`, avoid large animated travel and elastic settling. Snap state promptly, preserve context with handle/state label, shadow/outline change, and a short opacity/color transition if useful.

## 5. Verified versus unverified claims

**Verified from static code:**
- `top` is mutated during pointer move.
- `top` is animated with WAAPI on pointer up.
- CSS uses `transition: all 300ms`.
- CSS uses `.sheet:active { transform: scale(0.96); }`.
- Settle uses `480ms ease-in`.
- `animating` blocks pointer-down during animation.
- No Reduced Motion branch is shown.
- No pointer capture, velocity sampling, threshold, or boundary handling is shown.

**Unverified / cannot be claimed from this evidence:**
- Actual frame rate, jank, or layout cost.
- Whether `transition: all` applies in computed styles after full cascade.
- Touch behavior on real hardware.
- Whether other code wraps this snippet with missing drag guards.
- Whether snap points are visually correct.
- Whether animation fill creates visible state mismatch in this app.
- Whether users perceive the motion as slow; the static code only makes it a strong risk.

## 6. Minimal browser/device validation plan before approval

1. **Desktop Chrome/Edge pointer test:** verify pointer-down feedback, grab-offset preservation, 1:1 tracking, and no movement on hover-only pointermove.  
2. **Interruption test:** start a settle animation, grab mid-flight, confirm no visual jump and no input lock.  
3. **Velocity test:** slow drag versus quick flick; record release velocity, projected endpoint, selected snap point, and final state.  
4. **Boundary test:** drag beyond collapsed/full; confirm progressive resistance and predictable return.  
5. **Reduced Motion run:** enable `prefers-reduced-motion`; confirm reduced spatial travel while state feedback remains clear.  
6. **Performance trace:** profile under representative app load; confirm transform-only frame updates and no layout thrash in the gesture hot path.  
7. **Touch hardware pass:** validate on at least one real touch device or trackpad/touchscreen laptop; gesture feel cannot be approved from static code alone.  
8. **Keyboard/focus check:** ensure sheet state changes and controls remain reachable without pointer gestures.
