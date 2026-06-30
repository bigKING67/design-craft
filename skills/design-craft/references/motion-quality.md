# Motion quality

Use this when a task touches animation, transitions, hover/press feedback,
toasts, popovers, drawers, gestures, page transitions, perceived performance, or
when the user says motion feels weird, slow, flashy, dizzy, or janky.

This is a local `design-craft` fusion of Emil Kowalski-style design engineering
motion rules with the existing project-authority workflow. It is not a universal
animation aesthetic. Live runtime behavior, scoped project rules, product
context, and `DESIGN.md` still win.

## First question: should this animate?

Motion needs a reason. Valid reasons:

- Spatial consistency: preserve where something came from or where it goes.
- State indication: show a clear state change.
- Explanation: make a concept understandable.
- Feedback: confirm the interface heard an input.
- Jarring-change prevention: avoid abrupt add/remove/swap behavior.

Frequency decides restraint:

| Frequency | Decision |
| --- | --- |
| 100+ times/day, keyboard shortcuts, command palette toggles | No animation. |
| Tens/day, hover effects, list navigation | Remove or drastically reduce. |
| Occasional, modals, drawers, toasts | Standard animation. |
| Rare or first-time, onboarding, feedback, celebrations | Delight is allowed. |

If the purpose is only "looks cool" and the user will see it often, delete or
reduce the motion.

## Timing and easing

Default UI motion should feel responsive, not cinematic.

| Element | Duration |
| --- | --- |
| Button or press feedback | `100-160ms` |
| Tooltip or small popover | `125-200ms` |
| Dropdown or select | `150-250ms` |
| Modal or drawer | `200-500ms` |
| Marketing or explanatory motion | Can be longer when it does not block use |

Rules:

- Most UI animations should stay under `300ms`.
- Use strong `ease-out` for entering, exiting, and user-triggered response.
- Use `ease-in-out` for objects moving or morphing on screen.
- Use `ease` for simple hover/color changes.
- Use `linear` only for constant motion such as spinners, progress, or marquees.
- Avoid `ease-in` for UI interactions; it delays the moment users watch most.

Useful custom curves:

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
```

Do not invent curves from scratch when a known curve fits. Tune to the product
personality: a professional dashboard should be crisp; a playful tool can carry
more bounce.

## Physicality

- Never enter from `scale(0)`. Start from `scale(0.9-0.97)` plus opacity so the
  element feels present before it grows.
- Popovers, dropdowns, and tooltips should scale from their trigger, not the
  center. Use framework transform-origin variables when available.
- Modals are the exception: centered overlays can keep `transform-origin:
  center`.
- Pressable elements should usually have subtle active feedback, such as
  `transform: scale(0.97)` over about `160ms`.
- Group entrances should stagger by `30-80ms` only when the sequence helps
  comprehension; never block interaction while a stagger plays.

## Interruptibility

Rapidly-triggered UI should retarget smoothly.

- Prefer CSS transitions for dynamic add/remove/toggle UI; transitions can
  interrupt and retarget.
- Avoid keyframes for toasts, toggles, and anything users can trigger rapidly;
  keyframes tend to restart from zero.
- Use springs for drag, velocity, gesture reversal, and "alive" decorative
  motion.
- Keep bounce subtle (`0.1-0.3`) and avoid it in serious, data-dense surfaces.
- Use `@starting-style` for entry animation when browser support allows; use a
  mounted/data attribute fallback only when needed.

## Gesture craft

- Dismiss by velocity as well as distance; a quick flick should count.
- Apply damping or friction beyond natural boundaries instead of hard stops.
- Capture pointer events once a drag starts.
- Ignore additional touch points after the initial drag begins.
- Test gesture motion on a real device when the result depends on touch feel.

## Performance

- Prefer animating `transform` and `opacity`.
- Avoid animating layout properties such as `width`, `height`, `margin`,
  `padding`, `top`, and `left`, especially on repeated elements.
- Avoid `transition: all` and broad Tailwind `transition-all` on large surfaces
  or hot paths.
- Use `will-change` sparingly; remove it if it does not improve measured
  smoothness.
- Avoid updating a CSS variable on a parent to drive child transforms in large
  trees; it can trigger broad style recalculation.
- Predetermined motion should prefer CSS or WAAPI. JS/rAF-driven motion and
  animation libraries are appropriate for dynamic, gesture-driven, or
  interruptible cases, but measure under load when smoothness matters.
- Never make content inaccessible or invisible until JavaScript animation starts.

## Accessibility

- Honor `prefers-reduced-motion`. Reduced motion means gentler and less
  positional movement, not necessarily zero change; opacity/color transitions
  that aid comprehension can remain.
- Gate hover motion with `@media (hover: hover) and (pointer: fine)` so touch
  devices do not get sticky hover behavior.
- Keep focus-visible states clear even when hover/press motion is reduced.

## Review format

For a motion review, use:

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` | `transition: transform 180ms var(--ease-out)` | Limit animated properties and keep the response crisp. |
| `scale(0)` entry | `scale(0.95)` plus opacity | Elements should not appear from nothing. |
| `ease-in` dropdown | strong `ease-out` | Users need immediate response at the start. |

Then give a verdict:

- **Block**: feel-breaking regression, animation on high-frequency/keyboard
  action, `scale(0)`, `ease-in` UI motion, obvious layout-property animation, or
  missing reduced-motion behavior on movement.
- **Approve**: purpose is clear, frequency is appropriate, timing/easing are
  within bounds, motion is interruptible where needed, performance risk is
  controlled, and accessibility is handled.

## Debugging checklist

- Slow motion: temporarily increase duration 2-5x or use DevTools animation
  inspector.
- Frame-by-frame: inspect easing, transform-origin, opacity/transform sync, and
  color crossfades.
- Under load: test while the page is loading or while data-heavy views render.
- Real devices: verify drawers, swipe, and touch gestures on hardware when
  possible.
