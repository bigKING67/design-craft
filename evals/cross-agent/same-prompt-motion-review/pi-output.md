## 1. Evidence level and design read

**Evidence level:** static-source review only. The prompt explicitly provides no pointer trace, computed styles, frame timeline, Reduced Motion run, responsive run, or real-device touch test.

**Design read:** Reading this as a high-frequency web operations bottom sheet for task workers, with calm utility motion, optimized for moving between `collapsed`, `half`, and `full` without losing context or breaking direct manipulation.

**Verdict:** **Block approval.** The current motion model works against a draggable sheet: it locks interruption, animates layout, lags behind the pointer, ignores velocity, and has no Reduced Motion path.

---

## 2. Should this motion exist?

**Yes, but only in service of causality:**

- **Should animate:** the settle from release position to the chosen snap point; small pointer-down affordance on the handle/sheet; state feedback after snapping.
- **Should not animate:** the drag tracking itself. While the user is dragging, the sheet should follow the pointer 1:1 with no CSS transition.
- **Should not animate broadly:** `transition: all`, layout `top`, and large `scale(0.96)` on the whole sheet.
- **Reduced Motion:** should preserve state confirmation, but remove long spatial travel, bounce, and large sheet movement where possible.

---

## 3. Prioritized blocking findings

1. **Input lockout breaks direct manipulation**
   - `if (animating) return;` prevents grabbing the sheet mid-settle.
   - A sheet must be interruptible from its current presentation value; otherwise it feels like a playback animation, not an object under the user’s hand.

2. **Drag is not 1:1**
   - `.sheet { transition: all 300ms; }` means every `top` change during `pointermove` may be eased instead of tracking the pointer.
   - `sheet.style.top = event.clientY` also ignores grab offset and coordinate space, so the sheet can jump under the pointer.

3. **Wrong animated property and conflicting motion ownership**
   - Animating `top` is layout-affecting and risky on a frequently used operations surface.
   - `transition: all` also makes unrelated properties animate accidentally.
   - The interaction needs a single explicit motion owner, ideally `transform: translateY(...)`, with press feedback composed separately.

4. **Release physics are non-causal**
   - Snap target is based on `sheet.offsetTop`, not measured release velocity or projected endpoint.
   - A fast flick and a slow drag ending at the same position would choose the same target, which contradicts user intent.

5. **Reduced Motion is absent**
   - The code always performs a `480ms` spatial animation with `ease-in`.
   - For repeated work use, Reduced Motion must provide state feedback without large travel or delayed movement.

---

## 4. Concrete design moves

1. **Pointer-down feedback**
   - Give immediate, subtle feedback on the drag handle or sheet header, not the whole task surface.
   - Replace `scale(0.96)` with something calmer: handle highlight, cursor/grip state, or `scale(0.99–0.985)` on a dedicated handle layer.

2. **1:1 tracking**
   - On drag start, record `grabOffset = pointerY - currentSheetY`.
   - During drag, set `sheetY = pointerY - grabOffset`.
   - Disable transitions during active drag.

3. **Use transform, not top**
   - Drive movement with `transform: translateY(...)`.
   - Avoid `transition: all`; restrict transitions to named properties only.

4. **Presentation-value interruption**
   - If the sheet is settling and the user touches it, cancel/read the active animation at the current visual position.
   - Start the new drag from that current presentation value, not from the previous logical snap state.

5. **Velocity handoff**
   - Track recent pointer samples with timestamps.
   - On release, compute velocity in CSS px/s.
   - Start the settle animation with that velocity rather than restarting from zero.

6. **Projected endpoint snap selection**
   - Choose `collapsed`, `half`, or `full` from a projected endpoint, not only the release position.
   - This lets a confident flick to full/closed feel intentional even if the finger releases before crossing the midpoint.

7. **Soft boundaries**
   - Add an `8–12px` intent threshold so taps do not become drags.
   - Beyond `full`/`collapsed`, apply resistance/rubber-banding instead of hard clipping or unrestricted travel.

8. **Reduced Motion path**
   - Respect `prefers-reduced-motion`.
   - Remove long settle travel and bounce; use immediate snap or very short, low-distance state change.
   - Preserve feedback through handle color, shadow/outline, label/state affordance, or brief opacity/color transition.

---

## 5. Verified vs. unverified claims

**Verified from static code:**

- `animating` blocks pointer-down during animation.
- Pointer movement writes `style.top` directly.
- Snap target uses `nearestSnapPoint(sheet.offsetTop)`.
- WAAPI animates `top` for `480ms` with `ease-in`.
- CSS uses `transition: all 300ms`.
- CSS active state scales the sheet to `0.96`.
- No visible Reduced Motion branch is present in the provided evidence.
- No visible velocity, projected endpoint, pointer capture, grab offset, drag threshold, or soft-boundary logic is present.

**Unverified / runtime-only:**

- Actual perceived lag, jank, or frame rate.
- Whether CSS transition and WAAPI conflict in the target browser.
- Exact `offsetTop` behavior after `fill: "forwards"` in this implementation context.
- Touch behavior on real devices.
- Scroll/container coordinate issues.
- Whether the scale feedback feels disorienting in practice.
- Reduced Motion behavior in a real user setting.

---

## 6. Minimal validation plan before approval

1. **Desktop browser pointer test**
   - Verify pointer-down feedback, grab offset, 1:1 tracking, interruption during settle, and snap correctness.

2. **Touch device or touch simulator pass**
   - Verify finger tracking, pointer capture, cancellation, and boundary resistance.

3. **Motion trace**
   - Record drag and release at normal speed and slowed playback.
   - Check that drag frames are not transitioned/eased.

4. **Velocity cases**
   - Test slow drag near midpoint, fast flick upward, fast flick downward, and release near each snap boundary.

5. **Reduced Motion run**
   - Enable `prefers-reduced-motion`.
   - Confirm state feedback remains clear without large animated travel.

6. **Responsive/container check**
   - Test at small, medium, and tall viewport heights to confirm snap points and coordinate space remain correct.

**References applied:** `design-craft`, `motion-quality.md`, and `interaction-physics.md`.
