## Motion Critique: Gesture-Sheet Interaction

**Design read**: Web ops app for repeat daily use by operators. Drag a bottom sheet between `collapsed`, `half`, and `full` states. Calm utility UI — motion only to preserve causality and direct manipulation. No entertainment.

**Mode**: `critique` (read-only, no edits, no browser/device claims).

**References applied**: `motion-quality.md`, `interaction-physics.md`, `product-context.md`, `product-design-principles.md`, `design-move-library.md`.

---

### 1. Evidence level

**Static source only.** No pointer trace, computed-style snapshot, frame timeline, Reduced Motion run, responsive run, or real-device touch test. The implementation evidence is two code blocks (JS event handlers + CSS). This caps every finding at *reasoned from source* — nothing below is confirmed at runtime.

---

### 2. Should this motion exist?

**Yes, but not all of it.** A draggable bottom sheet needs:

- **Must animate**: pointer-down feedback, 1:1 tracking, and a settle animation after release. These preserve causality and direct manipulation.
- **Must not animate**: The 480ms `ease-in` snap is decorative and slow. The 300ms `transition: all` fights the JS animation and adds layout thrash. The `:active` scale is harmless in intent but wrongly timed and wrongly eased for a daily-use tool.

---

### 3. Prioritized findings

#### 🔴 P0 — Block-level

| # | Finding | Reasoning |
|---|---------|-----------|
| **P0.1** | `transition: all 300ms` on `.sheet` | Animates every CSS property over 300ms — including `top`, which `pointermove` sets directly and the snap `.animate()` also sets via WAAPI. This creates a CSS-transition vs. WAAPI-animation fight. `all` also triggers layout recalculation for `width`, `height`, `padding`, `margin` on any sheet change. Performance anti-pattern per `motion-quality.md`. |
| **P0.2** | No `prefers-reduced-motion` anywhere | A block-level violation per `motion-quality.md`. The sheet must replace large spatial travel with a cross-fade or instant state switch when the user has Reduced Motion on. The 480ms snap with `ease-in` and the `scale(0.96)` press effect are both undamped spatial motion with no reduced path. |
| **P0.3** | `animating` flag blocks all input during snap | Violates the *presentation-value interruption* contract from `interaction-physics.md` ("never lock input until a transition completes"). If the user grabs the sheet mid-snap, they are ignored for up to 480ms. For a daily-use ops tool where the sheet is the primary interaction surface, this is a direct-manipulation regression. |
| **P0.4** | `ease-in` for 480ms snap duration | `motion-quality.md`: "Avoid `ease-in` for UI interactions; it delays the moment users watch most." The sheet accelerates slowly and only visibly moves at the end, making it feel sluggish. Combined with 480ms duration, this is both the wrong curve and too slow. |

#### 🟡 P1 — Direct-manipulation failures

| # | Finding | Reasoning |
|---|---------|-----------|
| **P1.1** | No grab-offset preservation | `pointermove` sets `sheet.style.top = event.clientY`. This snaps the top of the sheet to the pointer's Y coordinate, regardless of where the user grabbed. If the sheet is at Y=400 and the user touches at Y=350 (50px below the top), the sheet jumps to Y=350 on first move. `interaction-physics.md`: "Preserve the grab offset; never jump the object center under the finger." |
| **P1.2** | No velocity measurement or handoff | `pointerup` calls `nearestSnapPoint(sheet.offsetTop)` without any velocity history. A flick that carries momentum toward `full` at release will snap to `half` if the release position is closer to `half`. `interaction-physics.md`: "Choose a snap target from the projected endpoint, not only the release point." |
| **P1.3** | No projected endpoint | Related to P1.2. The snap decision is purely position-based. The formula `projection(v, d) = (v / 1000) * d / (1 - d)` is entirely absent. |
| **P1.4** | Animates `top` (layout property) | `motion-quality.md`: "Avoid animating layout properties such as `top`." The snap uses WAAPI on `top`, which triggers layout on every frame. Should use `transform: translateY()`. |
| **P1.5** | No pointer capture | `setPointerCapture` is never called. If the user drags beyond the sheet bounds or the pointer leaves the sheet edge, tracking is lost. `interaction-physics.md`: "Use pointer capture or the native gesture equivalent so tracking continues outside the original bounds." |

#### 🟠 P2 — Interaction physics gaps

| # | Finding | Reasoning |
|---|---------|-----------|
| **P2.1** | No hysteresis / intent threshold | `pointerdown` begins tracking immediately without requiring any movement threshold. Every tap becomes a micro-drag. `interaction-physics.md`: "Require roughly 8-12px of movement before committing a drag direction so taps remain taps." |
| **P2.2** | No soft boundaries or rubber-banding | Dragging beyond `collapsed` or `full` has no resistance — the sheet can be dragged arbitrarily far and then snaps hard on release. `interaction-physics.md`: "Use progressive resistance beyond a boundary instead of a hard stop." |
| **P2.3** | No multi-touch guard | Additional touch points after the initial drag are not ignored. Can cause interference on real devices. `interaction-physics.md`: "Ignore additional touch points after the initial drag begins." |
| **P2.4** | Snaps from release position, not current presentation value | If the sheet is mid-snap (though input is locked — P0.3), the next snap would jump from the logical target, not where it currently appears. This is moot because of P0.3, but if interruption is fixed, this becomes a follow-up bug. |

#### 🟢 P3 — Feedback timing

| # | Finding | Reasoning |
|---|---------|-----------|
| **P3.1** | `:active` scale delayed by CSS transition | `.sheet { transition: all 300ms }` means the `scale(0.96)` is eased over 300ms. Press feedback should be 100-160ms per `motion-quality.md`. The feedback arrives too slowly and feels disconnected from the touch. |
| **P3.2** | `:active` pseudo-class is unreliable for touch feedback | Browser `:active` timing varies across devices and does not guarantee feedback on `pointerdown`. `interaction-physics.md` says "Show press feedback on pointer/touch down, not only on click/up." A dedicated `pointerdown` class or WAAPI-driven press state is needed. |
| **P3.3** | `scale(0.96)` is within acceptable range | The magnitude (0.96) is inside the 0.90-0.97 band per `motion-quality.md`. The problem is timing and trigger, not the value. |

---

### 4. Concrete design moves

#### 4.1 Pointer-down feedback

- **Remove** `transition: all 300ms` from `.sheet` entirely.
- **Add** a short `pointerdown`-driven press state:
  ```css
  .sheet {
    transition: transform 120ms ease-out;
  }
  .sheet.pressed {
    transform: scale(0.96);
  }
  ```
  Toggle `.pressed` on `pointerdown`/`pointerup`. This gives crisp 120ms feedback and cleans up when the drag starts. Gate with `@media (hover: none) and (pointer: coarse)` or apply universally — the ops tool needs press feedback on all input modes.

#### 4.2 1:1 tracking

- **Store grab offset** on `pointerdown`:
  ```js
  grabOffset = event.clientY - sheet.getBoundingClientRect().top;
  ```
- **Track with offset** on `pointermove`:
  ```js
  const clampedY = clampWithRubberBand(event.clientY - grabOffset, minY, maxY);
  sheet.style.transform = `translateY(${clampedY}px)`;
  ```
- Use `transform: translateY()` instead of `top` to stay on the compositor.
- **Call `sheet.setPointerCapture(event.pointerId)`** on `pointerdown` after the hysteresis threshold.
- **Add 8px hysteresis** before committing to drag. Until then, treat it as a potential tap.

#### 4.3 Presentation-value interruption

- **Drop the `animating` guard.** Never lock input.
- On `pointerdown` during a snap animation:
  1. Read the current on-screen `translateY` from the computed transform (or maintain a tracked value).
  2. Cancel the running animation (`sheet.getAnimations().forEach(a => a.cancel())`).
  3. Start a new drag with that presentation value as the origin and zero initial velocity.
- This satisfies `interaction-physics.md`: "retarget from the current on-screen presentation value, not the previous logical target."

#### 4.4 Velocity handoff and projected endpoints

- **Store last N pointer events** (positions and timestamps) in a ring buffer during tracking.
- **Compute release velocity**: average velocity over the last ~3-5 events.
- **Project endpoint**:
  ```js
  const projected = currentY + (releaseVelocity / 1000) * 0.998 / (1 - 0.998);
  const target = nearestSnapPoint(projected);
  ```
- Use `d = 0.998` for scroll-like momentum per `interaction-physics.md`.
- Clamp projection so a wild flick cannot target a state the sheet cannot reach.

#### 4.5 Snap animation (settle spring)

- Replace WAAPI `animate([{top}, {top}], { duration: 480, easing: "ease-in" })` with a spring or spring-equivalent WAAPI:
  ```js
  sheet.animate(
    [{ transform: `translateY(${currentY}px)` }, { transform: `translateY(${target}px)` }],
    {
      duration: 350,
      easing: "cubic-bezier(0.32, 0.72, 0, 1)", // --ease-drawer
      fill: "forwards",
    },
  );
  ```
- **Duration: 350ms** (within 200-500ms for drawers, tightened for daily repeat use).
- **Easing: `ease-drawer` curve** (`cubic-bezier(0.32, 0.72, 0, 1)`) per `motion-quality.md`. This gives a responsive settle with natural deceleration.
- If the release velocity is high enough to carry to a boundary, increase damping (shorter effective settle) to avoid the sheet feeling floaty.

#### 4.6 Soft boundaries

- Apply **progressive resistance** when dragging beyond `collapsed` or `full`:
  ```js
  const overshoot = clampedY - boundaryY;
  const resisted = (overshoot * viewportHeight * 0.55) / (viewportHeight + 0.55 * Math.abs(overshoot));
  ```
  This is the rubber-band function from `interaction-physics.md` with `constant = 0.55`.
- On release beyond a boundary, use a **spring with higher damping** (~1.0, critically damped) to pull back to the nearest valid snap point cleanly.
- Set a **distance threshold beyond which dragging away cancels the gesture** (e.g., >30% of the sheet height past a boundary), snapping to the boundary-adjacent snap point.

#### 4.7 Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  .sheet {
    transition: transform 0ms;      /* instant tracking */
  }
  .sheet.pressed {
    transition: opacity 150ms;      /* keep causal feedback */
    transform: none;
    opacity: 0.85;
  }
  /* Snap settle: instant or cross-fade */
  .sheet.settling {
    transition: opacity 200ms;
  }
}
```

In JS: when `prefers-reduced-motion` is active, skip the spring animation. On `pointerup`, snap instantly to the chosen target. Use a brief opacity cross-fade (150-200ms) to signal the state change without spatial travel. This preserves the *causal feedback* contract from `motion-quality.md` while removing the large positional movement that Reduced Motion users should not experience.

---

### 5. Verified vs. unverified claims

| Claim | Status |
|-------|--------|
| `transition: all 300ms` conflicts with WAAPI `animate()` on `top` | **Unverified.** Reasoned from source. Requires DevTools animation inspector or frame timeline to confirm compounding. |
| `ease-in` 480ms feels sluggish | **Unverified.** Reasoned from easing curve shape. Requires pointer-trace timing on real device. |
| `animating` flag blocks mid-snap regrabs | **Verified from source.** The guard is on line 4. |
| Grab-offset jump on first `pointermove` | **Unverified.** Reasoned from `event.clientY` assigned directly as `top`. Confirmation requires a computed-style trace after the first move event. |
| No velocity / projection logic | **Verified from source.** `nearestSnapPoint` receives only `sheet.offsetTop`. |
| No `prefers-reduced-motion` anywhere | **Verified from source.** Zero occurrences in both blocks. |
| No pointer capture | **Verified from source.** No `setPointerCapture` call. |
| No soft boundaries | **Verified from source.** `top` is set unbounded in `pointermove`. |
| `:active` scale transitioned at 300ms | **Unverified.** Reasoned from CSS cascade. `transition: all 300ms` covers `transform`, and `.sheet:active { transform: scale(0.96) }` triggers it. Browser DevTools "Animations" panel would confirm the actual transition duration. |
| Animating `top` causes layout thrash | **Unverified.** Not confirmed by Performance panel or layout-shift recording. Reasoned from the well-established compositor vs. layout pipeline model. |

---

### 6. Minimal validation plan before implementation approval

1. **Browser DevTools — Animation inspector**:
   - Open the sheet, record a drag-and-release.
   - Confirm whether the CSS `transition: all 300ms` and WAAPI `animate()` are fighting (look for double entries or conflicting keyframes on `top`).
   - Verify the actual duration of the `scale(0.96)` press effect under `:active`.

2. **Browser DevTools — Performance panel**:
   - Record a full drag cycle. Check for `Layout` / `Recalculate Style` events on every `pointermove` frame (confirms `top` layout thrash).
   - After switching to `transform: translateY()`, re-record and confirm layout events drop to near zero.

3. **Real touch device** (phone or tablet with touch screen):
   - Test grab-offset: touch near the bottom of the sheet → verify the sheet does NOT jump.
   - Test interruption: drag → release → regrab mid-snap → verify seamless continuation.
   - Test velocity: flick up fast → verify the sheet targets `full` even if release position is closer to `half`.
   - Test boundary rubber-banding: drag past `full` → verify progressive resistance, not a hard stop.
   - Test multi-touch: place a second finger during drag → verify it is ignored.

4. **Reduced Motion**:
   - Enable `prefers-reduced-motion: reduce` in OS settings or DevTools rendering emulation.
   - Drag and release → verify instant snap (or opacity cross-fade ≤200ms) with no spatial travel animation.

5. **Refresh rate check**:
   - Test on both 60Hz and 120Hz displays. The `pointermove` hot path (reading `getBoundingClientRect()`, mutation, velocity buffer) should stay under the frame budget on 60Hz.

---

### Verdict

**Block.** The current implementation has four P0 regressions (`transition: all` fight, no Reduced Motion, locked input during snap, `ease-in` 480ms) and six P1/P2 direct-manipulation failures (grab-offset jump, no velocity, no projection, `top` animation, no pointer capture, no hysteresis). No amount of visual polish can fix a sheet that jumps under the finger, ignores mid-snap regrabs, and fails to dismiss on a flick. Return to implementation with the design moves above and complete the validation plan on real touch hardware before re-review.
