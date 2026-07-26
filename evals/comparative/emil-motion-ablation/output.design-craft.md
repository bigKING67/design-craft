## Evidence-labeled verdict

**Verdict: Block for production.**  
[Static evidence] The sheet is moved with `top` on every `pointermove`, has `transition: all 300ms`, settles with `480ms ease-in`, lacks visible Reduced Motion handling, and uses a global `animating` lock.  
[Product evidence] This is a repeatedly used operations surface with collapsed / half / full states; the motion should feel immediate, interruptible, calm, and state-preserving. This implementation is likely to feel laggy, non-direct, and fragile.

## Prioritized findings

1. **P0 — Drag is not truly direct manipulation.**  
   [Static] `pointermove` always writes `sheet.style.top = event.clientY`; `startY` is recorded but unused. There is no dragging flag, grab offset, pointer capture, direction threshold, or boundary clamp.  
   [Impact] The sheet can jump to the pointer, move without an intentional drag, lose tracking outside the element, and collide with page scrolling or accidental taps.

2. **P0 — `transition: all` fights the drag.**  
   [Static] `.sheet { transition: all 300ms; }` applies while `top` is updated during pointer moves.  
   [Impact] Each drag frame can be eased instead of staying 1:1 under the pointer, creating lag. It also risks animating unrelated future property changes.

3. **P0 — Layout-property animation is a performance risk.**  
   [Static] The hot path writes `top`; release animation also animates `top`; `pointerup` reads `sheet.offsetTop`.  
   [Impact] This can trigger layout work during the most latency-sensitive part of the interaction. A sheet should generally move with `transform: translateY(...)`.

4. **P0 — The motion is not safely interruptible.**  
   [Static] `animating` blocks `pointerdown`, but `pointermove` still writes `top`; the settle animation is not canceled or retargeted from the current presentation value.  
   [Impact] A user cannot confidently grab the sheet mid-settle. Competing pointer writes and WAAPI animation may create jumps.

5. **P1 — Settle timing/easing is wrong for repeated operations work.**  
   [Static] `{ duration: 480, easing: "ease-in" }`.  
   [Impact] `ease-in` delays the response at the start and accelerates late; 480ms can feel heavy for a high-frequency operations control. The settle should feel responsive, usually shorter or spring-like, and start from release velocity.

6. **P1 — Snap selection ignores velocity and intent.**  
   [Static] `nearestSnapPoint(sheet.offsetTop)` uses current layout position only.  
   [Impact] A quick flick toward half/full/collapsed may be ignored if the release point is closer to another state. If product semantics allow momentum, target choice should consider measured release velocity or a bounded projected endpoint.

7. **P1 — Reduced Motion requirement is unmet in the supplied code.**  
   [Static] No `prefers-reduced-motion` branch or alternate feedback path is shown.  
   [Product] Reduced Motion must preserve state feedback without large spatial travel.  
   [Impact] Users requesting reduced motion may still get full-distance sheet travel.

8. **P2 — Press feedback is too broad and may conflict with sheet movement.**  
   [Static] `.sheet:active { transform: scale(0.96); }`.  
   [Impact] Scaling the whole sheet can make dense content feel unstable. If translation later moves to `transform`, scale and translate need separate wrapper layers or one composed transform owner.

## Concrete direct-manipulation moves

- Replace `top` movement with one position owner: `translate3d(0, ypx, 0)` on a sheet transform layer.
- Remove `transition: all`; transition only explicit non-gesture properties, or disable transition while dragging.
- On `pointerdown`: capture `pointerId`, record start pointer Y, current sheet Y, snap state, and grab offset; cancel any active settle from the current on-screen value.
- On `pointermove`: only respond while dragging the captured pointer; after an `8–12px` intent threshold, update via `requestAnimationFrame`; clamp to collapsed/full bounds with optional soft resistance.
- On `pointerup/cancel`: compute release velocity from recent samples in CSS px/s; choose target by the product’s snap rule, optionally using a bounded projected endpoint if momentum targeting is desired.
- Settle with an interruptible spring or equivalent retargetable animation; default to no bounce for this calm operations context.
- Keep press feedback on a handle or inner affordance, not the whole sheet content; if scale remains, separate it from the translate layer.
- Add Reduced Motion behavior: snap state with no large travel, or use a very short opacity/elevation/color/handle-state change while preserving collapsed/half/full feedback.
- Ensure non-pointer operation: keyboard controls for moving between collapsed/half/full, visible focus, state labels, and focus continuity after state changes.

## Verified / unverified boundaries

**Verified from static code only**
- `top` is mutated during drag and animated on release.
- `transition: all 300ms` applies to the sheet.
- Release animation uses `480ms ease-in`.
- `startY` is unused.
- No pointer capture, velocity sampling, bounds, drag flag, or Reduced Motion branch appears in the supplied snippet.
- The animation lock does not provide clean interruption semantics.

**Not verified**
- Actual frame rate, perceived smoothness, touch-device feel, scroll interaction, snap-point geometry, or final rendered behavior.
- Whether other omitted code provides keyboard support, ARIA/state announcements, focus management, bounds, or Reduced Motion.
- Whether the sheet is inside a layout where `top` has additional constraints or compensating styles.

## Smallest runtime validation plan

1. Verify drag attachment: pointer down, move slowly, leave/re-enter sheet bounds, release from collapsed/half/full.
2. Verify interruption: flick to a snap point, grab mid-settle, reverse direction; confirm no jump or input lock.
3. Verify snap intent: slow drag near thresholds and fast flicks in both directions; record chosen target and release velocity.
4. Verify Reduced Motion: emulate `prefers-reduced-motion`; confirm no large spatial travel while collapsed/half/full state feedback remains clear.
5. Verify performance risk: record one drag under normal app load; check for layout work during pointer moves and dropped frames.
