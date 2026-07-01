# Cursor unverified

- Host: Cursor
- Version observed: `3.9.16`
- Date: 2026-07-01
- Status: unverified
- Reason: `cursor` exists locally, but `cursor agent --help` attempted to
  install `cursor-agent` via `https://cursor.com/install` and timed out during
  preflight. No same-prompt Cursor agent output was collected for this release.

Do not count Cursor as a verified cross-agent behavior host until a real Cursor
agent run records an output and score JSON for this same benchmark prompt.
