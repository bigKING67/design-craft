# Engineering quality

Use this when changing frontend code, components, state, data flow, or
interactions.

## Code elegance

- Express business intent in names and boundaries.
- Keep components small enough to understand, not artificially tiny.
- Separate domain decisions from visual primitives.
- Prefer explicit props over hidden global behavior.
- Avoid "temporary" boolean props that encode multiple concepts.
- Add comments only for non-obvious constraints, not for line-by-line narration.

## Component boundaries

Split when:

- A child has a distinct responsibility or lifecycle.
- A piece is reused with the same intent in at least two places.
- A heavy interactive leaf should be isolated from server/static layout.
- Testing or state ownership becomes clearer.

Do not split merely to reduce file length if cohesion is still high.

## State and data

- Keep state near the owner.
- Use URL/query state when it is navigation state.
- Use server/cache state for fetched data; avoid duplicating it into local
  state without a reason.
- Do not use React state for high-frequency scroll/pointer values.
- Validate external API data at the boundary when shape is uncertain.

## Errors and observability

- Loading, empty, error, permission, and partial-data states are UI states, not
  afterthoughts.
- Do not swallow errors to make UI appear successful.
- If fallback behavior exists, make it visible and traceable.
- Surface enough context in logs or telemetry for diagnosis without leaking
  secrets.

## Dependencies

- Check `package.json` before importing.
- Prefer existing project libraries and primitives.
- Do not add a large dependency for a simple local behavior.
- One icon family per surface unless the project already mixes families.
- For design systems, use official packages when the brief clearly maps to one
  and the project can accept the dependency.

## Review checklist

- Does this make the main task easier to understand?
- Did we change only the necessary surface?
- Are naming and module boundaries stable beyond this patch?
- Is there an observable failure path?
- Is there a simpler native/browser/framework feature?
