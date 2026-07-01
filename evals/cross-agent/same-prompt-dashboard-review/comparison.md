# Same-prompt dashboard review comparison

## Summary

The 0.3.0 dashboard benchmark has real observed outputs for Codex and Pi only.
Cursor and Claude remain explicitly unverified for this release.

| Host | Status | Score | Notes |
|---|---:|---:|---|
| Codex | verified | 94 | Strong evidence labeling, explicit verified/unverified boundary, and concrete design moves. |
| Pi | verified | 91 | Strong critique and validation plan; slightly stricter score band and less detailed implementation anatomy than Codex. |
| Cursor | unverified | N/A | `cursor agent --help` attempted `cursor-agent` install and timed out; no agent output collected. |
| Claude | unverified | N/A | CLI present, but quota was unavailable; no agent output collected. |

## Common behavior

- Both verified hosts treated the task as L0 prompt-only evidence.
- Both diagnosed the 12-card KPI grid as card soup rather than a decision
  surface.
- Both rejected the decorative chart and generic right rail as weak operational
  fit.
- Both proposed executable design moves: lead/support/action queue, task-first
  table, diagnostic chart, contextual rail, and semantic state color.
- Both avoided claiming browser, responsive, focus, loading, empty, or error
  behavior as verified.

## Boundary

This comparison supports the claim that Codex and Pi can apply the same
`design-craft` dashboard prompt consistently enough for a 0.3.0 smoke benchmark.
It does not support any claim that Cursor or Claude behavior is stable, because
their same-prompt outputs were not collected.
