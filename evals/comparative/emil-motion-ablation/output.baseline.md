## Verdict

**[Static evidence] Not production-ready for a calm repeated-use operations sheet.**  
The implementation does not provide true direct manipulation, has no Reduced Motion path, animates layout properties, and can create lag, jumps, and conflicting motion. The collapsed / half / full model is only implied at release, not represented as stable interactive states during drag.

---

## Prioritized findings

### 1. Drag does not track intent reliably

**Evidence:** `startY = event.clientY` is stored but never used. `pointermove` sets `sheet.style.top = event.clientY`.

**Impact:** The sheet can jump because movement is based on absolute pointer position, not the sheet’s starting offset plus drag delta. This breaks the “attached to finger / cursor” feel.

**Fix direction:** Track:

```js
delta = event.clientY - startY
nextY = startSheetY + delta
```

Then clamp or resist beyond snap bounds.

---

### 2. Motion uses `top`, causing layout work during drag and settle

**Evidence:** `sheet.style.top = ...`, `sheet.offsetTop`, and animation keyframes use `top`.

**Impact:** `top` changes can trigger layout and paint on every pointer move. `offsetTop` also forces layout reads. This is risky for a 10,000-row operations surface where the sheet may sit over expensive content.

**Fix direction:** Use `transform: translateY(...)` for drag and snap animation. Keep snap state in JS, but render position through transform.

---

### 3. CSS transition conflicts with gesture control

**Evidence:** `.sheet { transition: all 300ms; }`

**Impact:** Every `top` change during pointermove may be transitioned, causing the sheet to lag behind the pointer. `transition: all` can also accidentally animate unrelated properties.

**Fix direction:** Remove `transition: all`. Use explicit transition only for non-drag settle:

```css
.sheet {
  transition-property: transform;
  transition-duration: var(--duration-panel);
  transition-timing-function: var(--ease-responsive);
}
.sheet[data-dragging="true"] {
  transition: none;
}
```

---

### 4. Release animation feels wrong for a responsive sheet

**Evidence:** `{ duration: 480, easing: "ease-in" }`

**Impact:** `ease-in` starts slowly and accelerates into the target, which can feel like the sheet is sliding away rather than settling. `480ms` is long for repeated operations use.

**Fix direction:** Use a responsive deceleration/ease-out style curve and shorter duration, ideally velocity-aware. Example target behavior: quick catch-up, smooth settle, no dramatic travel.

---

### 5. No Reduced Motion path

**Evidence:** No `prefers-reduced-motion` handling and no alternate state feedback.

**Impact:** Users who prefer reduced motion still get large spatial travel over 480ms plus active scaling.

**Fix direction:** In Reduced Motion:
- avoid long animated travel;
- snap position immediately or within a very short duration;
- preserve feedback with handle highlight, state label, border/color change, or subtle opacity change;
- avoid `scale(0.96)`.

---

### 6. Pointer lifecycle is incomplete

**Evidence:** There is no `dragging` flag, no pointer capture, and no pointer cancel handling.

**Impact:** `pointermove` can mutate the sheet even when a valid drag was not started. If the pointer leaves the sheet or the gesture is interrupted, state may become inconsistent.

**Fix direction:** On pointerdown:
- set `dragging = true`;
- capture the pointer;
- record pointer id, start Y, and sheet position.

On pointermove:
- ignore events unless `dragging` and pointer id matches.

On pointerup / pointercancel:
- release capture;
- settle to snap point;
- clear dragging state.

---

### 7. Snap decision ignores velocity and direction

**Evidence:** `nearestSnapPoint(sheet.offsetTop)` only uses final position.

**Impact:** A fast intentional upward or downward flick may choose the wrong snap point if the final offset is near the previous state.

**Fix direction:** Use position + velocity:
- slow drag: nearest snap point;
- fast upward drag: next more-expanded state;
- fast downward drag: next more-collapsed state.

---

### 8. Active scale fights the sheet metaphor

**Evidence:** `.sheet:active { transform: scale(0.96); }`

**Impact:** The sheet shrinks while being dragged, which can make controls move under the pointer and makes the surface feel like a button rather than a panel.

**Fix direction:** Keep the panel spatially stable. Use handle affordance feedback instead: handle color, shadow, border emphasis, or cursor change.

---

## Concrete direct-manipulation moves

1. **Represent state explicitly**
   - `collapsed`, `half`, `full`
   - expose current snap point as data/state, not only pixel position.

2. **Use transform-based positioning**
   - render with `translateY(currentY)`;
   - avoid writing `top` during drag.

3. **Separate drag from settle**
   - during drag: no transition, 1:1 pointer tracking;
   - after release: animate to snap point.

4. **Clamp with resistance**
   - hard clamp within full/collapsed bounds, or add slight resistance past edges;
   - never allow uncontrolled off-screen movement.

5. **Use pointer capture**
   - preserve drag continuity if the pointer leaves the handle/sheet.

6. **Make snap velocity-aware**
   - slow movement chooses nearest point;
   - fast flick advances one state in flick direction.

7. **Constrain gesture start area**
   - prefer handle/header drag area;
   - avoid hijacking scrollable sheet content.

8. **Add Reduced Motion behavior**
   - no large animated travel;
   - very short transform update or immediate snap;
   - visible state feedback through handle/status styling.

9. **Avoid transform conflict**
   - do not use `scale()` on the same element that uses `translateY`;
   - if visual press feedback is needed, apply it to an inner handle only.

---

## Verified / unverified boundaries

**Verified from static code:**
- `top` is mutated on every pointermove.
- `offsetTop` is read on release.
- animation duration is `480ms`.
- easing is `ease-in`.
- CSS uses `transition: all 300ms`.
- CSS applies `transform: scale(0.96)` on active.
- no Reduced Motion branch is present.
- no pointer capture, pointercancel, drag flag, or velocity logic is present.
- `startY` is assigned but unused.

**Not verified here:**
- actual frame rate or dropped frames.
- behavior on touch hardware.
- interaction with scrollable content inside the sheet.
- exact visual jank from `transition: all`.
- accessibility tree, focus order, or keyboard support.
- whether surrounding code adds missing state or Reduced Motion handling elsewhere.

---

## Smallest runtime validation plan

1. **Gesture correctness**
   - drag from collapsed to half and full;
   - confirm no initial jump;
   - confirm pointer and sheet stay visually attached.

2. **Snap behavior**
   - slow drag near boundaries chooses nearest snap;
   - fast flick moves one state in flick direction;
   - pointercancel leaves sheet in a valid state.

3. **Reduced Motion**
   - enable reduced motion;
   - confirm no long spatial animation;
   - confirm state feedback remains visible.

4. **Performance smoke**
   - drag over the populated table;
   - check for obvious lag, layout spikes, or delayed pointer tracking.

5. **Interaction safety**
   - drag from handle;
   - scroll sheet content;
   - confirm scrolling and dragging do not fight each other.
