# Pi observed output

- Agent: Pi CLI
- Version: `pi 0.80.3`
- Date: 2026-07-10
- Command summary: `pi --no-session --no-tools --skill <repo>/skills/design-craft -p @prompt.md`
- Skill path observed: `/Users/gaoqian/Documents/sixseven/codeproject/design-craft/skills/design-craft`
- Evidence boundary: read-only prompt/source review; runtime behavior remains unverified.
- Benchmark contract: output includes concrete design move recommendations.

## Output

**Evidence level and design read**
**Evidence**: static source only (JS + CSS). No pointer traces, computed-style snapshots, frame timelines, Reduced Motion runs, or real-device touch logs. This is a desk review; all claims about interaction feel are inferred from code semantics and known motion heuristics.

**Design intent**: the sheet should feel like a direct-manipulation object that the user drags and releases. The motion’s job is to preserve causality (I dragged it, it went there) and affordance (the panel is snappable). The code betrays that intent in several ways, described below.

---

**Should this motion exist?**
Yes, the core motion—snapping to a stable state after release—should exist. It confirms the action and provides a predictable resting point. The CSS `transition: all 300ms` and the `:active` scale-down should *not* animate in the current form because they fight with the JS-driven snap and introduce a redundant, uncalibrated layer of motion.

---

**Prioritized findings**
1. **Broken 1:1 tracking** — `sheet.style.top = ${event.clientY}px` moves the sheet relative to the viewport, not relative to the grab point. This breaks direct manipulation: the sheet jumps to the pointer’s absolute Y, losing the offset between finger and panel edge.
2. **Conflicting motion layers** — CSS `transition: all 300ms` runs on every `top` change during `pointermove`, fighting the browser’s pointer-following and adding latency. The JS `sheet.animate()` also produces a top animation; the two compete and the weaker one loses in unpredictable ways.
3. **Wrong easing for snap** — `easing: "ease-in"` makes the snap start slow and then accelerate, which feels like the panel is lagging before slamming into the target. A decelerating curve (ease-out) is expected for gravity/snap.
4. **No interruption handling** — `animating` flag blocks input during the snap animation. If the user reaches for the panel before it lands, the panel ignores the pointer, destroying the illusion of a physical object.
5. **Static snap target** — `nearestSnapPoint` is computed once at pointer-up. If the user drags and releases slowly near a boundary, the panel may snap to the wrong point because the code doesn’t account for velocity.
6. **No Reduced Motion strategy** — the code ignores `prefers-reduced-motion`. The snap animation uses a fixed 480ms and travels a large distance, violating the accessibility requirement.
7. **Scale-down `:active` is a cheap trick** — `transform: scale(0.96)` shrinks the entire sheet, shifting layout and content, and adds no spring or resistance. It feels like a bug, not a deliberate press state.

---

**Concrete design moves**

*Pointer-down feedback*
- **Design move**: replace `:active` scale with a subtle, local indicator: lift the sheet 2–4px (shadow increase + translateY) and apply a 100ms ease-out transition. The content must not reflow.

*1:1 tracking*
- **Design move**: on pointer-down, record `offset = event.clientY - sheet.offsetTop`. On pointer-move, set `sheet.style.top = event.clientY - offset`. This keeps the grab point locked to the finger.
- **Design move**: disable CSS transitions on the sheet during the drag phase (e.g., toggle a `dragging` class that removes `transition`).

*Presentation-value interruption*
- **Design move**: replace the `animating` flag with a spring-based animation system (or the Web Animations API’s `currentTime`/`playbackRate` control). On pointer-down during a snap, immediately cancel the animation, read the current computed `top`, and transfer control to the drag. The user must never feel a dead panel.

*Velocity handoff and projected endpoints*
- **Design move**: track pointer velocity over the last 3–5 move events. When the user releases, project the endpoint using the current position plus velocity * a time constant (e.g., 0.3s). Choose the snap point that is closest to the *projected* endpoint, not the release position.

*Soft boundaries*
- **Design move**: clamp the drag position to `[collapsed, full]` with a small rubber-band overshoot (e.g., 20px) that returns on release. This gives physical feedback that the panel can’t go further.

*Reduced Motion*
- **Design move**: for `prefers-reduced-motion: reduce`, skip the spring/velocity-based snap animation entirely. Instead, instantly set the final `top` value and use a 200ms opacity or background-color flash to provide state feedback without spatial travel.

---

**Verified versus unverified claims**
- **Verified**: the static code contains a CSS `transition: all 300ms`, a JS `sheet.animate` with `ease-in`, and a `:active` scale transform. These are observable in the source.
- **Unverified**: all interaction-physics judgments (e.g., “the tracking is broken,” “the easing feels wrong”) are **unverified** because no pointer-trace data, frame-by-frame timeline, or real-device test was performed. The velocity-handoff suggestion is also **unverified** without a prototype run.

---

**Minimal browser/device validation plan before implementation approval**
1. **Record pointer traces** — capture pointerdown/move/up events with timestamps and computed `top` values for slow, fast, and boundary-crossing drags.
2. **Capture frame timelines** — use Chrome DevTools Performance panel or a frame-by-frame screenshot to verify that the sheet follows the pointer with zero visible lag during drag and that the snap animation completes without jank.
3. **Run Reduced Motion** — enable `prefers-reduced-motion: reduce` and confirm that the snap is instantaneous and that a state-change indicator (e.g., flash) appears.
4. **Test interruption** — start a snap, then touch the panel again before it lands. Verify the snap stops and the panel immediately follows the new touch.
5. **Multi-device touch** — test on a real touch device (phone/tablet) to confirm the grab-point offset is correct and that no native scroll or browser gesture interference occurs.

Only after the above evidence is collected should the motion be approved for production.
