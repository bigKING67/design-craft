## 1. Evidence level and design read

**Evidence level:** Static source/prose only. The code proves property choices, timing, easing, missing branches, and interaction-state ownership risks. It does **not** prove actual feel, smoothness, frame rate, computed style, touch behavior, or Reduced Motion behavior.

**Reading this as:** a high-frequency web operations sheet for task-focused users, with calm utility motion, optimized for direct manipulation between `collapsed`, `half`, and `full` without disorienting or obscuring context.

## 2. Should this motion exist?

**Yes, but only as causal motion.** The sheet needs motion for:
- direct manipulation while dragging;
- a short settle from release to snap point;
- subtle feedback that the drag handle is engaged;
- state confirmation between collapsed/half/full.

**These should not animate:**
- `top` / layout position during drag or settle;
- `transition: all`;
- whole-sheet `scale(0.96)` while active;
- large spatial travel under Reduced Motion;
- decorative bounce unless user velocity clearly creates it and the product approves that feel.

## 3. Prioritized findings

**F1 — Blocker: drag is not true 1:1 direct manipulation.**  
Static proof: `pointermove` sets `sheet.style.top = event.clientY`, while `startY` is unused.  
Risk: the sheet can jump so its top aligns to the pointer instead of preserving grab offset. It may also respond to pointer movement without a committed drag state.  
Physics issue: grabbed objects should stay attached to the finger after an intent threshold, not teleport to the pointer coordinate.

**F2 — Blocker: interaction is not interruptible.**  
Static proof: `if (animating) return` on `pointerdown`; `animating` remains true until `.finished`.  
Risk: users cannot re-grab or reverse the sheet mid-settle.  
Physics issue: draggable sheets must retarget from the current presentation value and carry velocity; locking input until completion breaks direct manipulation.

**F3 — Blocker: layout-property animation and `transition: all` conflict with gesture performance.**  
Static proof: JS writes `top`; WAAPI animates `top`; CSS declares `transition: all 300ms`.  
Risk: pointer tracking may be delayed by transitions and layout work; WAAPI/CSS/inline style ownership can diverge.  
Physics issue: drag hot paths should use compositor-friendly `transform: translateY(...)` with one explicit owner.

**F4 — Blocker: release settle uses the wrong motion language.**  
Static proof: `duration: 480`, `easing: "ease-in"`, target chosen only from `sheet.offsetTop`.  
Risk: slow-start response makes the release feel unresponsive; no measured velocity or projected endpoint means quick flicks may resolve against user intent.  
Physics issue: sheet settling should start with measured release velocity and usually use a critically/near-critically damped spring, not a fixed slow ease-in.

**F5 — Blocker: accessibility and calm utility intent are not honored.**  
Static proof: no `prefers-reduced-motion`; whole sheet scales to `0.96` on `:active`.  
Risk: Reduced Motion users still get large travel; active scale compresses task content and may read as playful or unstable in an operations app.  
Physics issue: feedback should confirm grip without distorting the work surface.

## 4. Concrete design moves

1. **Pointer-down feedback:** apply subtle feedback to the drag handle/scrim affordance, not the whole sheet; e.g. handle color/weight change or tiny handle scale. Keep focus-visible independent.

2. **Intent threshold:** require about `8–12px` movement before committing drag, so taps, text selection, and controls inside the sheet are not stolen.

3. **1:1 tracking:** store `grabOffset = pointerY - currentSheetY`; during drag set `sheetY = pointerY - grabOffset`, preferably through `transform: translateY(...)`.

4. **Presentation-value interruption:** on pointerdown during a settle, cancel the active animation, read the current presentation value, and start the drag from that value with no visual jump.

5. **Velocity handoff:** keep a short pointer history with CSS px + monotonic timestamps; compute release velocity in CSS px/s and feed it into the settle animation.

6. **Projected endpoints:** if momentum targeting is approved, compute a bounded projected endpoint from current presentation value + release velocity, clamp it to valid sheet range, then choose nearest snap point. If product semantics require nearest-current-position, still use velocity for the settle but do not silently change target selection.

7. **Soft boundaries:** clamp hard safety limits, but add progressive resistance near/beyond `collapsed` and `full` instead of letting the sheet fly or stop abruptly.

8. **Reduced Motion:** preserve state feedback with immediate snap or very short opacity/color/handle-state changes; remove large travel, overshoot, rubber-band, and long settle. State labels/ARIA should still communicate collapsed/half/full.

## 5. Verified versus unverified claims

**Verified from static code:**
- `top` is mutated during pointer move.
- `top` is animated with WAAPI on release.
- CSS uses `transition: all 300ms`.
- active state scales the whole `.sheet` to `0.96`.
- `ease-in` and `480ms` are configured.
- pointerdown is ignored while `animating`.
- no Reduced Motion branch is present in the provided evidence.
- no velocity, projection, grab offset, pointer capture, boundary resistance, or drag threshold appears in the snippet.

**Unverified:**
- actual smoothness or jank;
- computed interaction between CSS transition and WAAPI in the real app;
- whether other code adds pointer capture, touch-action, clamping, ARIA, or Reduced Motion;
- real touch behavior on mobile/tablet hardware;
- frame rate, long tasks, layout cost, or compositing;
- whether nearest-position snapping is intentional product behavior.

## 6. Minimal browser/device validation plan before approval

1. Inspect computed styles for `.sheet`: animated properties, transform ownership, Reduced Motion branch, touch-action, and focus states.  
2. Browser pointer test: drag slowly between all three states; verify no jump, preserved grab offset, 1:1 tracking, and correct snap.  
3. Interruption test: release toward `full`, immediately re-grab mid-settle, reverse direction; verify no lockout or visual discontinuity.  
4. Velocity test: compare slow drag vs quick flick; verify target selection matches the approved product rule.  
5. Boundary test: drag beyond collapsed/full; verify resistance, clamping, and no context loss.  
6. Reduced Motion run: confirm large travel/overshoot is removed while state feedback remains clear.  
7. Performance trace under representative app load: confirm no layout-thrashing hot path and no visible long-task hitching.  
8. Real-device touch smoke on at least one coarse-pointer device before implementation approval.
