# Performance quality

Use this for UI performance, dashboards, charts, tables, animations, and heavy
frontend interactions.

## Default stance

Do not optimize blindly. Identify the hot path or risk first, then verify with
the smallest useful measurement: browser smoke, Web Vitals/Lighthouse signal,
DevTools/CDP metric, build output, bundle report, profiler, or targeted test.

## Frontend hot paths

Watch for:

- Large arrays mapped directly inside render without paging, virtualization, or
  memoized preparation.
- Expensive sort/filter/group computations on every render.
- Deep clones and repeated JSON parse/stringify.
- High-frequency input/scroll/resize handlers using React state.
- Layout reads and writes interleaved in loops.
- SVG/canvas/chart resize loops.
- Animating width/height/top/left/filter on many nodes.
- Images without dimensions, modern formats, lazy loading, or correct sizes.

## Dashboards and data viz

- Bound data size before rendering.
- Use server aggregation when possible.
- For tables, require pagination, virtualization, or an explicit row bound.
- For charts, verify container resize, canvas/SVG size, tooltip overflow, and
  mobile behavior.
- Avoid recomputing derived chart series inside render.
- Keep color ramps accessible and semantically consistent.

## Motion performance

- Prefer transform and opacity.
- Avoid animating layout properties on repeated elements.
- Use `will-change` sparingly and remove if it does not help.
- Respect `prefers-reduced-motion`.
- Do not make content invisible until JS animation starts.

## Bundle and dependency cost

- Check current dependencies before adding packages.
- Prefer framework-native image/font features.
- Split rarely used heavy views.
- Avoid importing whole utility/icon/chart libraries for a small subset when
  the project has alternatives.

## Delivery evidence

For performance-sensitive work, report:

- Target hot path.
- Data scale assumption.
- What was changed.
- How it was measured or why it could not be measured.
- Residual risk.
