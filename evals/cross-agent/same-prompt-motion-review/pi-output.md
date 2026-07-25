## 1. Evidence level and design read

**Evidence level:** static-code critique only. The snippet proves explicit animation values, CSS rules, and missing branches inside the provided scope; it does **not** prove runtime smoothness, device feel, frame rate, computed styles, or touch-browser behavior.

**Design read:** Reading this as a calm web operations surface for repeat daily use, optimized for moving a bottom sheet between task-preserving states with direct manipulation, low surprise, and Reduced Motion safety.

## 2. Should this motion exist?

**Yes, but narrowly.** Motion should exist to preserve causality:

- the sheet follows the pointer during drag;
- release settles to a snap point;
- state change remains legible.

**These parts should not animate:**

- pointer-tracking itself should not be eased or delayed;
- `transition: all` should not animate arbitrary properties;
- `:active { transform: scale(0.96) }` should not shrink the sheet during drag;
- Reduced Motion should not use large spatial travel as the main feedback;
- background/task context should not be disturbed unless explicitly required.

## 3. Prioritized findings

### P0 — Drag is not 1:1 direct manipulation

`pointermove` sets `sheet.style.top = event.clientY`, while `.sheet { transition: all 300ms; }` can cause pointer-driven movement to lag behind the finger/cursor.

Why it matters: a sheet drag is a physical manipulation model. During active drag, the sheet should track the pointer immediately, not chase it through a transition.

### P0 — Input is locked during animation instead of interruptible

`if (animating) return;` blocks a new drag while the settle animation is running.

Why it matters: direct-manipulation surfaces must be interruptible. If the user grabs the sheet mid-flight, the sheet should continue from its current presentation value, not ignore input or jump to stale state.

### P0 — Release physics are causally wrong

The settle uses `duration: 480` and `easing: "ease-in"` with no release velocity.

Why it matters: `ease-in` starts slowly after the user releases, which feels like the sheet loses momentum. A gesture handoff should preserve measured release velocity and then settle.

### P1 — Coordinate model is unstable

`startY` is recorded but unused; `top = clientY` ignores the grab offset, sheet origin, container bounds, and current sheet position.

Why it matters: the sheet may jump so that its top aligns with the pointer rather than preserving where the user grabbed it.

### P1 — Motion ownership conflicts

CSS `transition: all`, WAAPI `animate({ top })`, inline `style.top`, `offsetTop`, and `transform: scale()` all compete.

Why it matters: mixed ownership makes interruption, final state, accessibility, and performance harder to reason about. It also risks layout work from animating `top`.

## 4. Concrete design moves

1. **Pointer-down feedback:** use subtle handle/drag affordance feedback only: cursor change, handle color, tiny elevation/token change, or “grabbed” state. Avoid whole-sheet scale.

2. **Capture and drag state:** on `pointerdown`, set an active drag flag, call pointer capture, store `pointerId`, grab offset, current position, and bounds. Ignore unrelated pointer moves.

3. **1:1 tracking:** while dragging, disable transitions and update a single owned presentation property, preferably `transform: translateY(...)`, with position derived from `initialSheetY + pointerDeltaY`.

4. **Presentation-value interruption:** if a settle is running, sample the current visual position, cancel the animation, commit that value as the new drag start, then continue without a jump.

5. **Velocity handoff:** record recent pointer samples in explicit units, e.g. `px/ms` or `px/s`; on release, compute release velocity, choose a snap target separately, and pass that velocity into the settle animation/spring after unit conversion.

6. **Projected endpoints:** use a bounded projected endpoint for target selection, e.g. `projectedY = clamp(currentY + velocityPxPerMs * projectionMs, minY, maxY)`, then apply snap thresholds/hysteresis. Do not let projection escape the sheet bounds.

7. **Soft boundaries:** when dragging beyond collapsed/full limits, apply resistance/rubber-banding visually, then settle back inside bounds. Keep the actual committed state clamped.

8. **Reduced Motion:** preserve state feedback without large travel: shorten/near-instant settles, use opacity/outline/handle/state label changes, and avoid overshoot, bounce, or long spatial easing.

## 5. Verified vs unverified claims

**Verified from the snippet:**

- animation duration is `480ms`;
- easing is `ease-in`;
- animated property is `top`;
- CSS uses `transition: all 300ms`;
- active state scales the sheet to `0.96`;
- `animating` blocks `pointerdown`;
- `startY` is assigned but not used in the shown code;
- no Reduced Motion branch is shown;
- no velocity measurement is shown;
- no pointer capture, pointer cancel, or lost-capture handling is shown.

**Unverified / runtime-dependent:**

- actual perceived lag;
- frame rate or layout jank;
- whether `transition: all` affects the WAAPI animation in the final cascade;
- final computed `top`/transform state after `fill: "forwards"`;
- touch behavior on real devices;
- scroll conflict behavior;
- responsive behavior across sheet heights;
- screen reader, keyboard, and Reduced Motion runtime behavior.

## 6. Minimal browser/device validation plan before approval

1. **Desktop browser pointer trace:** confirm no jump on grab, 1:1 tracking during drag, and interruption during settle.

2. **Touch device or touch-emulation smoke:** verify pointer capture, scroll conflict, release behavior, and pointer-cancel handling.

3. **Reduced Motion run:** enable `prefers-reduced-motion: reduce`; confirm state feedback remains clear without long spatial travel.

4. **Frame/performance check:** inspect whether dragging uses layout-affecting `top` or compositor-friendly transform, and verify no visible stutter during repeated drags.

5. **Responsive states:** test collapsed, half, and full at small and large viewport heights, including content overflow.

6. **Accessibility pass:** keyboard/focus path to the sheet controls or snap states, visible focus, target size, and non-motion state indication.
