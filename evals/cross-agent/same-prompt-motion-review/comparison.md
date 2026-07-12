# Current comparison

| Host | Status | Score | Requested runtime | Evidence |
| --- | --- | ---: | --- | --- |
| Codex | verified | 98 | `gpt-5.6-sol` / `max` | `codex-output.md`, `run.codex.json`, `score.codex.json` |
| Pi | verified | 100 | `codex/gpt-5.5` / `high` | `pi-output.md`, `run.pi.json`, `score.pi.json` |
| Cursor | unverified | - | unavailable | Cursor Agent is installed but not authenticated. |
| Claude | unverified | - | `opus` and `sonnet` attempted | Authentication is visible after adapter repair, but repeated API calls ended with `ECONNRESET`; no output or run manifest was admitted. |

These are current-source v3 scores recorded on 2026-07-12. Historical Codex/Pi
v2 evidence remains under
`evals/cross-agent/history/2026-07-11-v2/same-prompt-motion-review/` and is not
used for current certification.
