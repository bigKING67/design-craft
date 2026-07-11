# Motion Review: Gesture Sheet Interaction

## 1. Evidence Level and Design Read

**Evidence level:** `L0 static` — prompt and static source code only. No pointer trace, computed style, frame timeline, Reduced Motion run, responsive run, or real-device touch test. This is a design read from source, useful for flagging structural defects but incapable of verifying gesture feel.

**Design read:** Reading this as a **web operations app bottom sheet** for a **repeat daily user**, with **calm utility UI**, optimized for **dragging between collapsed/half/full states without losing task context**. Motion exists only to preserve causality and direct manipulation.

**Authority order:** No project-level `PRODUCT.md`, `DESIGN.md`, or `AGENTS.md` found in the working directory. Product context is taken directly from the prompt. References applied: `interaction-physics.md` → `motion-quality.md` → `product-design-principles.md`.

---

## 2. Should This Motion Exist?

**Yes — conditionally.** The sheet must move because the primary job *is* dragging between states. But two motion elements should not exist in their current form:

| What | Verdict | Why |
|------|---------|-----|
| CSS `transition: all 300ms` | **Remove entirely** | Fires on every style change. The user will interact with this sheet 100+ times/day — that tier mandates "remove or drastically reduce." The `all` keyword hits layout, paint, and composite for *every* changed property. In a drag path, it also fights the JS-driven position. |
| 480ms `ease-in` settle animation | **Redesign** | The settle-to-snap-point motion itself is valid (state indication, spatial consistency), but `ease-in` is the wrong direction and 480ms is too long. |
| `:active` `scale(0.96)` | **Keep, but supplement** | This is the one motion element that's directionally correct — press feedback on a draggable surface. But it's CSS-only and needs a JS pointerdown complement. |

---

## 3. Prioritized Findings

### 🔴 BLOCK — Feel-breaking regressions

**F1. `ease-in` on a UI interaction**
> *"Avoid `ease-in` for UI interactions; it delays the moment users watch most."* — `motion-quality.md`

`ease-in` starts slow and accelerates toward the end. When a user releases a sheet, they expect the fastest movement *immediately* — their gesture was the trigger, and the sheet should respond right away. `ease-in` does the opposite: it hesitates at the start and rushes at the end. This inverts the user's mental model of cause and effect.

**F2. Animating `top` (a layout property)**
> *"Avoid animating layout properties such as `width`, `height`, `margin`, `padding`, `top`, and `left`, especially on repeated elements."* — `motion-quality.md`
> *"Drive frame updates with compositor-friendly properties or native transforms."* — `interaction-physics.md`

`top` triggers layout recalculation on every frame. During pointer tracking at 60+ Hz, this causes repeated synchronous reflow — the single most expensive path in browser rendering. Every `pointermove` event does `sheet.style.top = ...`, which forces layout. The snap animation does the same via WAAPI keyframes keyed to `top`. Both paths must use `transform: translateY()`.

**F3. Input locked during animation (`if (animating) return`)**
> *"Never lock input until a transition completes."* — `interaction-physics.md`

If the user grabs the sheet mid-settle, the `animating` guard silently drops the gesture. The user's pointerdown is swallowed, the sheet continues its 480ms journey to the previous target, and only after `finished.then(...)` resets `animating` can they try again. This is a direct violation of the Agency principle — the user loses control.

**F4. No pointer capture**
> *"Use pointer capture or the native gesture equivalent so tracking continues outside the original bounds."* — `interaction-physics.md*

`pointermove` is listened on `sheet` itself. If the user's finger drifts outside the sheet bounds (very likely during a fast drag), tracking stops dead. The sheet freezes at the last known position until the finger re-enters the sheet's hit area.

**F5. No `prefers-reduced-motion` handling**
> *"Reduced Motion removes large travel...while preserving causal feedback through short cross-fades, color, scale, or static state change."* — `interaction-physics.md`*

Zero media query or JS check for the user's OS-level Reduced Motion preference. The 480ms `ease-in` travel and `transition: all 300ms` both constitute the "large spatial travel" that Reduced Motion specifically asks to remove. The prompt states accessibility as an explicit requirement.

---

### 🟠 HIGH — Interaction-physics defects

**F6. No grab-offset preservation**
> *"Preserve the grab offset; never jump the object center under the finger."* — `interaction-physics.md`*

`startY` is recorded but never compared against the sheet's current position. If the user touches 40px from the sheet's top edge, the sheet should track with that 40px offset preserved. Instead, the code writes `sheet.style.top = event.clientY`, which forces the sheet's top edge to the finger position — a visual jump on every drag start. This feels like the sheet "snapping" to the finger instead of being held at the grab point.

**F7. No velocity tracking or projected-endpoint snap targeting**
> *"Track a short time/position history so release velocity is measured."* — `interaction-physics.md`*
> *"Choose a snap target from the projected endpoint, not only the release point."* — `interaction-physics.md`*

`nearestSnapPoint(sheet.offsetTop)` uses only the current position at release. A quick upward flick that would naturally carry the sheet past the next snap point will re-settle to the nearest static snap. The user must drag all the way past the midpoint between snaps — velocity is ignored entirely.

The projection formula from `interaction-physics.md` is:
```
projectedEndpoint = current + projection(releaseVelocity, 0.998)
target = nearestSnapPoint(projectedEndpoint)
```

**F8. CSS transition conflict with JS animation**
> *"CSS transitions are acceptable for simple state changes that do not need to be grabbed. A draggable sheet...needs a spring/animation primitive."* — `interaction-physics.md`*

`.sheet { transition: all 300ms; }` runs during the JS `sheet.animate()` call. When the WAAPI animation sets `top`, the CSS transition also tries to interpolate `top` — along with every other property. The result is two competing interpolation engines fighting over the same property, producing unpredictable visual behavior depending on which engine wins the cascade at each frame.

**F9. No hysteresis / drag-intent threshold**
> *"Require roughly 8-12px/pt/dp of movement before committing a drag direction so taps remain taps."* — `interaction-physics.md`*

Any `pointermove` after `pointerdown`, no matter how tiny, begins dragging. A tap — which involves microscopic pointer movement — will trigger a 1-2px sheet jump before the `pointerup` fires. This also makes the sheet "sticky" during clicks on any interactive elements inside it.

---

### 🟡 MEDIUM — Polish gaps

**F10. No soft boundaries / rubber-banding**
> *"Use progressive resistance beyond a boundary instead of a hard stop."* — `interaction-physics.md`*

Dragging past `collapsed` or beyond `full` has no resistance. The sheet moves 1:1 past its natural limits and then snaps back — a hard wall feel. The rubber-band function from `interaction-physics.md` would give it the expected progressive resistance:
```
(overshoot * dimension * constant) / (dimension + constant * abs(overshoot))
```

**F11. `transition: all 300ms` — the `all` keyword**
> *"Avoid `transition: all` and broad Tailwind `transition-all` on large surfaces or hot paths."* — `motion-quality.md`*

The `all` keyword means every property change on `.sheet` triggers a 300ms transition — including properties set by the drag loop. Even if JS weren't fighting it, this would animate every incidental style change. Must be scoped to specific properties like `transform`, `opacity`, and only on the non-dragging states.

**F12. Duration 480ms vs. frequency tier**
> *"100+ times/day → No animation."* "Tens/day → Remove or drastically reduce."* — `motion-quality.md`*

The user drags this sheet repeatedly throughout the day. Even if we treat the settle as "tens/day," the 480ms duration is at the upper bound of the modal/drawer range (200-500ms). For a calm utility tool optimized for preserving task context, the settle should be 200-250ms — fast enough to feel responsive, long enough to read the direction.

**F13. No cancel gesture**
No way to cancel a drag: no Escape key handler, no drag-away-to-cancel zone, no distance threshold for cancellation. A mistaken drag must either commit or be released with unpredictable snap behavior.

---

## 4. Concrete Design Moves

### Pointer-down feedback

```
Current: CSS :active { transform: scale(0.96) } only
Move:    Add JS pointerdown handler that adds a .pressed class
         with scale(0.97) + a subtle background shade change
         over 100–120ms ease-out. Remove on pointerup/cancel.
Why:     :active has inconsistent behavior across browsers and
         input types. JS-managed press state is reliable and can
         integrate with pointer capture lifecycle.
```

### 1:1 tracking

```
Current: sheet.style.top = event.clientY  (no grab offset, layout property)
Move:    On pointerdown, compute: grabOffset = event.clientY - sheet.getBoundingClientRect().top
         On pointermove: sheet.style.transform = `translateY(${event.clientY - grabOffset}px)`
         setPointerCapture(event.pointerId) after drag threshold is met
Why:     Preserves the physical grab point. Uses compositor-only transform.
         Pointer capture keeps tracking alive outside sheet bounds.
```

### Presentation-value interruption

```
Current: if (animating) return;  → drops the gesture
Move:    If a settle spring is running when pointerdown fires:
         1. Read the current computed translateY (presentation value)
         2. Measure the spring's instantaneous velocity
         3. Cancel the spring
         4. Begin new 1:1 drag from the current on-screen position
         → No guard; the user can always grab.
Why:     "retarget from the current on-screen presentation value,
         not the previous logical target" — interaction-physics.md
```

### Velocity handoff

```
Current: nearestSnapPoint(sheet.offsetTop) uses position only
Move:    Track last ~5 pointermove events (time + y). On release:
         releaseVelocity = (last.y - first.y) / (last.time - first.time)  // px/ms
         projection = releaseVelocity * 0.998 / (1 - 0.998)  // or similar
         projectedEndpoint = currentY + projection
         target = nearestSnapPoint(projectedEndpoint)
Why:     A quick flick should carry the sheet to the next snap point
         without requiring the user to drag all the way there.
```

### Projected endpoints

```
Move:    Use d ≈ 0.998 for a scroll-like momentum feel (matches
         natural flick decay). Clamp projection to [collapsed, full]
         bounds. If projected endpoint is within ~20% of the next
         snap, commit to it. Otherwise, settle to nearest.
```

### Soft boundaries

```
Move:    When dragY < collapsedY or dragY > fullY:
         overshoot = dragY - boundaryY
         resistance = (overshoot * viewportHeight * 0.55) /
                       (viewportHeight + 0.55 * abs(overshoot))
         clampedY = boundaryY + resistance
Why:     Progressive resistance feels physical. The default
         constant 0.55 from interaction-physics.md is a starting
         point; tune with real touch evidence.
```

### Reduced Motion

```
Move:    Add @media (prefers-reduced-motion: reduce) { ... }
         Inside:
         - Remove the 200-250ms settle animation entirely
         - Replace with a 100ms opacity crossfade or a subtle
           background-shade change at the snap boundary
         - Keep :active scale(0.97) — it's small, local, and
           causal; it does not constitute "large spatial travel"
         - The sheet should snap to target state instantly but
           communicate the change through non-motion feedback
         Also add a JS matchMedia listener so programmatic
         animation (spring) is skipped when Reduced Motion is active.
Why:     "Reduced Motion removes large travel, parallax, elastic
         overshoot, and looping motion while preserving causal
         feedback through short cross-fades, color, scale, or
         static state change." — interaction-physics.md
```

---

## 5. Verified vs. Unverified Claims

| Claim | Status | Evidence |
|-------|--------|----------|
| `ease-in` is the wrong easing for UI snap | **Verified** (source) | `motion-quality.md` explicitly prohibits `ease-in` for UI interactions. The easing curve math is directionally incorrect for post-gesture settle. |
| `top` is a layout property and should be `transform` | **Verified** (source + browser spec) | Both references call this out. CSS `top` triggers layout; `transform` is compositor-only. This is a well-established browser performance invariant. |
| `transition: all` is an anti-pattern | **Verified** (source) | Explicitly called out in `motion-quality.md`. |
| Input lock breaks direct manipulation | **Verified** (design contract) | `interaction-physics.md`: "Never lock input until a transition completes." |
| No Reduced Motion handling | **Verified** (source) | Zero `prefers-reduced-motion` media queries or JS checks present in the provided code. |
| 480ms is too long for daily-use tool | **Verified** (motion-quality.md frequency table) | "100+ times/day → No animation." The settle should be at most 200-250ms. |
| Grab offset is missing | **Verified** (source) | `startY` recorded but never used as offset. `sheet.style.top = event.clientY` confirms the finger-to-top-edge jump. |
| Velocity tracking and projection are missing | **Verified** (source) | No event history buffer. `nearestSnapPoint` called with position only. |
| CSS transition conflicts with WAAPI animation | **Verified** (source reasoning) | Both engines target `top` simultaneously. Browser behavior is spec-defined but unpredictable in practice when both are active. |
| No hysteresis threshold | **Verified** (source) | Any `pointermove` starts dragging. No px/dp gate. |
| Gesture "feels responsive" or "feels broken" | **Unverified** | No pointer trace, frame timeline, or device test. These are structural predictions only. |
| The rubber-band constant 0.55 is correct for this surface | **Unverified** | Tuning requires real interaction evidence per `interaction-physics.md`. |
| Sheet performs at 60fps or drops frames during drag | **Unverified** | No frame budget measurement. The `top` animation on pointermove is a known performance risk but frame drops are unmeasured. |
| Reduced Motion behavior works correctly | **Unverified** | No Reduced Motion run was performed. |
| Touch device behavior (vs. mouse) | **Unverified** | No real-device touch test. `pointermove` frequency, palm rejection, and scroll conflict are unmeasured. |
| The 480ms `ease-in` + `transition: all 300ms` interaction actually produces a visual conflict | **Unverified** | Predicted from source but not observed in DevTools animation inspector or frame recording. |

---

## 6. Minimal Browser/Device Validation Plan

Before implementation approval, the following must be verified:

### Phase 1 — Desktop browser, DevTools (minimum bar)

1. **Animation inspector**: Open DevTools → Animations panel. Trigger the settle animation. Confirm `ease-in` is observable, measure actual frame count at 480ms duration, and capture the easing curve shape.

2. **Performance trace**: Record a Performance trace while dragging. Look for:
   - Recurring `Layout` (purple) blocks on every `pointermove` — confirms `top` reflow
   - `Recalculate Style` spikes
   - Frame budget violations (>16ms per frame)

3. **Computed style check**: During drag, inspect computed `top` vs `transform`. Confirm `top` is being written.

4. **Reduced Motion toggle**: Enable `prefers-reduced-motion: reduce` in DevTools rendering panel. Trigger the sheet. Observe that the 480ms animation still plays. Confirm no media query exists.

5. **Rapid re-grab test**: Drag and release → immediately pointerdown again during the settle. Observe that the second grab is silently dropped. Repeat 5 times quickly to confirm the input-lock behavior.

### Phase 2 — Touch device (release-critical)

6. **Real touch device**: Test on an actual phone or tablet (not DevTools touch simulation). Verify:
   - Grab offset — does the sheet jump when you touch it?
   - Pointer capture — does tracking continue when your finger leaves the sheet's visual bounds?
   - Velocity flick — does a fast upward flick carry the sheet to the next snap, or does it settle to the nearest position?
   - Tap behavior — does a quick tap cause a micro-jump?
   - Rubber banding — does dragging past `collapsed` or `full` feel like hitting a wall?

7. **Scroll conflict**: If the sheet contains scrollable content, test whether a vertical drag starts the sheet or scrolls the content. This is a known conflict for gesture sheets without intent disambiguation.

### Phase 3 — Accessibility verification

8. **System Reduced Motion**: Enable system-level Reduce Motion on macOS/iOS. Verify the sheet snap is instantaneous or uses short non-travel feedback. Verify keyboard navigation still reaches the sheet controls.

### Tools

| Check | Tool |
|-------|------|
| Easing curve, frame count | Chrome DevTools Animation panel |
| Layout thrashing | Chrome DevTools Performance panel |
| Computed style | Chrome DevTools Elements → Computed |
| Reduced Motion | DevTools Rendering → `prefers-reduced-motion: reduce` |
| Touch feel (pointer capture, velocity, offset) | Real mobile device + remote debugging |
| Scroll conflict | Real mobile device |

---

## Verdict

**BLOCK — do not approve.** This implementation has five feel-breaking regressions (F1–F5) that would be immediately noticeable to a daily user: the sheet hesitates on release, drops gestures mid-animation, stops tracking when the finger leaves the surface, hits layout on every frame, and ignores the user's Reduced Motion preference. The `top` animation and `ease-in` choice alone would cause measurable jank. The missing velocity handoff, grab offset, and pointer capture mean the sheet does not feel like a directly manipulated object — it feels like a sluggish, easily-broken proxy.

The `:active { scale(0.96) }` is the single element that is directionally correct. Everything else needs to be rebuilt from the interaction-physics primitives: pointer capture, grab-offset-preserving 1:1 tracking on `transform: translateY()`, a 200-250ms spring (damping 0.8, response 0.3s) with `ease-out` or spring dynamics, velocity-projected snap targeting, input always available for interruption, ~10px drag threshold, progressive boundary resistance, and a `prefers-reduced-motion` path that replaces spatial travel with opacity/color feedback.

**All structural findings (F1–F11) are verified from static source evidence against the design-craft references. Gesture feel, frame performance, touch-device behavior, scroll-conflict resolution, and rubber-band tuning remain unverified and require the validation plan above.**
