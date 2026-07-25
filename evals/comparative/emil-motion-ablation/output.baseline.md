## Verdict

**Not production-ready for a calm, repeated-use operations sheet.**  
**Evidence:** the implementation animates and drags `top`, combines WAAPI with `transition: all`, lacks pointer capture / drag state / reduced-motion handling, and uses a long `ease-in` settle. The result is likely to feel laggy, imprecise, and hard to interrupt.

---

## Prioritized findings

### P0 — Drag is not actually gated to an active gesture
**Evidence:** `pointermove` always runs:

```js
sheet.addEventListener("pointermove", (event) => {
  sheet.style.top = `${event.clientY}px`;
});
```

There is no `isDragging`, no `pointerId`, and no `setPointerCapture`. Any pointer move over the sheet can move it, including after `pointerdown` was ignored because `animating` was true.

**Impact:** accidental jumps, broken multi-pointer behavior, lost drags when the pointer leaves the sheet, and poor trust for repeated operations use.

---

### P0 — Motion is layout-driven instead of transform-driven
**Evidence:** drag and animation mutate `top`; snap reads `sheet.offsetTop`.

```js
sheet.style.top = `${event.clientY}px`;
nearestSnapPoint(sheet.offsetTop);
sheet.animate([{ top: ... }, { top: ... }])
```

**Impact:** `top` changes can trigger layout; `offsetTop` can force layout reads. This is risky for a dense operations app, especially near a large table or drawer.

---

### P0 — CSS and JS animation conflict
**Evidence:**

```css
.sheet { transition: all 300ms; }
```

while JS also updates `top` continuously and uses `sheet.animate(...)`.

**Impact:** direct manipulation may lag behind the pointer because `top` changes are also transitioned. `transition: all` can animate unrelated properties and create surprising motion when state/classes change.

---

### P1 — Reduced Motion requirement is unmet
**Evidence:** no `prefers-reduced-motion` branch; snap always uses:

```js
{ duration: 480, easing: "ease-in" }
```

**Impact:** users requesting reduced motion still get large spatial travel. The product requirement says state feedback must remain without large travel.

---

### P1 — Snap behavior ignores velocity, direction, and state intent
**Evidence:** target is based only on current `offsetTop`:

```js
const target = nearestSnapPoint(sheet.offsetTop);
```

**Impact:** a fast intentional fling toward full/closed can be misread if release position is near another snap. Calm does not mean inert; the sheet should respect the user’s drag momentum and direction.

---

### P1 — Animation is not safely interruptible
**Evidence:** `animating = true` blocks `pointerdown`, but `pointermove` still mutates the sheet. The `.finished` promise has no cancellation/error handling.

```js
).finished.then(() => {
  animating = false;
});
```

**Impact:** if the animation is canceled/replaced, the flag can get stuck. Users may be unable to re-grab the sheet during a settle, which makes the component feel non-physical.

---

### P2 — Easing and duration feel wrong for a sheet settle
**Evidence:** `duration: 480`, `easing: "ease-in"`.

**Impact:** `ease-in` starts slowly and accelerates into the destination, which can feel like the sheet is pulled away from the user at the end. A sheet settle usually needs quick response and deceleration into rest.

---

### P2 — `:active` scale harms precision
**Evidence:**

```css
.sheet:active { transform: scale(0.96); }
```

**Impact:** scaling the whole panel during drag compresses content, changes perceived hit targets, and conflicts with transform-based sheet movement. For an operations app, this is decorative feedback at the cost of control.

---

### P2 — No clamping or bounds protection shown
**Evidence:** `sheet.style.top = event.clientY`.

**Impact:** the sheet can be dragged outside valid collapsed/half/full ranges unless hidden elsewhere. Direct manipulation should expose limits clearly, not allow arbitrary sheet placement.

---

## Concrete direct-manipulation moves

1. **Use transform, not `top`.**  
   Keep the sheet positioned by layout once, then move it with:

   ```css
   transform: translate3d(0, var(--sheet-y), 0);
   ```

2. **Remove `transition: all`.**  
   Use a narrow transition only when settling:

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

3. **Track an actual gesture.**  
   On `pointerdown`: store `pointerId`, `startY`, `startOffset`, set `isDragging = true`, and call `setPointerCapture`.

4. **Clamp during drag.**  
   Compute:

   ```js
   nextOffset = clamp(startOffset + event.clientY - startY, fullY, collapsedY);
   ```

   Apply via transform/CSS variable, ideally batched with `requestAnimationFrame`.

5. **Use velocity-aware snap selection.**  
   On release, choose collapsed/half/full using:
   - current offset,
   - drag direction,
   - release velocity,
   - hysteresis around the current state.

6. **Make settle interruptible.**  
   A new pointerdown should cancel the current animation and continue from the visual position, not wait for a flag.

7. **Replace whole-sheet scale with local feedback.**  
   Prefer handle affordance, shadow density, header compression, or subtle opacity/border changes. Do not scale the full content surface.

8. **Add reduced-motion behavior.**  
   Under `prefers-reduced-motion: reduce`, avoid long travel:
   - snap immediately or within ~80ms,
   - keep visible state feedback through handle, shadow, label, or boundary change,
   - avoid large animated spatial distance.

9. **Add touch behavior explicitly.**  
   Use an appropriate `touch-action` on the drag handle/sheet so vertical dragging does not fight page scroll.

---

## Verified / unverified boundaries

### Verified from static code
- Uses `top` for drag and animation.
- Reads `offsetTop` for snap.
- Has `transition: all 300ms`.
- Has `:active { transform: scale(0.96) }`.
- Has no visible reduced-motion branch.
- Has no visible `isDragging`, `pointerId`, pointer capture, clamping, velocity, or cancellation handling.

### Not verified
- Real snap-point math.
- Actual DOM positioning and containment.
- Browser-specific WAAPI behavior.
- Performance under the real 10,000-row table.
- Touchpad/touch/stylus behavior.
- Screen reader, keyboard, and focus behavior.
- Visual polish on real devices.

---

## Smallest runtime validation plan

1. **Pointer correctness:** drag from collapsed → half → full; verify the sheet moves only after active pointerdown, follows the pointer, clamps to valid bounds, and still works if the pointer leaves the sheet.

2. **Interruptibility:** release toward a snap, then immediately re-grab mid-animation; verify it continues from the current visual position without jumping or locking.

3. **Reduced Motion:** enable reduced motion; verify state changes still show feedback but avoid long spatial travel.

4. **Performance smoke:** record a drag near the real dense table; verify no repeated layout-heavy work per frame and no visible hitching.

5. **State persistence:** after each snap, verify the durable state is exactly collapsed, half, or full, not just a visually filled animation state.
