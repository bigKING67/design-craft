# Same-prompt dashboard review comparison

## Summary

Observed on 2026-07-11 against clean `design-craft 0.5.0` source commit
`e3a6bc6` and skill tree `ebbd7a36...`. Codex and Pi have current-source v2
records; Cursor and Claude remain explicitly unverified.

| Host | Status | Score | Notes |
|---|---:|---:|---|
| Codex | verified | 97 | `codex-cli 0.144.1`, `gpt-5.6-sol`, high reasoning; strongest on decision hierarchy, operational state, and validation boundaries. |
| Pi | verified | 96 | `pi 0.80.3`, `deepseek/deepseek-v4-pro`, high thinking; concise exception-first redesign with a few inferred table details. |
| Cursor | unverified | N/A | `cursor-agent` is installed but not logged in; no current-source output exists. |
| Claude | unverified | N/A | CLI reports OAuth state, but a usable inference response has not been verified; no current-source output exists. |

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

This comparison supports current-source Codex/Pi dashboard behavior only. It
does not certify Cursor or Claude, rendered dashboard quality, browser states,
responsive behavior, accessibility, or production implementation quality.
