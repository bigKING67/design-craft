# Motion benchmark comparison

Observed on 2026-07-11 against clean `design-craft 0.5.0` source commit
`e3a6bc6` and skill tree `ebbd7a36...`.

| Host | Status | Score | Runtime |
|---|---:|---:|---|
| Codex | verified | 98 | `codex-cli 0.144.1`, `gpt-5.6-sol`, high reasoning |
| Pi | verified | 94 | `pi 0.80.3`, `deepseek/deepseek-v4-pro`, high thinking |
| Cursor | unverified | N/A | Installed CLI is not logged in |
| Claude | unverified | N/A | OAuth status exists, but usable inference is not verified |

Codex and Pi both labeled the evidence as static, called runtime behavior
unverified, rejected `transition: all`, and proposed concrete design moves.

- **Codex** was stronger on pointer lifecycle, grab-offset preservation,
  presentation-value interruption, velocity continuity, projected endpoints,
  `fill: forwards` state drift, and acceptance tests.
- **Pi** found the main direct-manipulation issues and supplied a useful runtime
  plan. Its press-scale example competes with translate tracking on the same
  `transform`, and its endpoint projection was more prescriptive than the
  available evidence justified.
- **Cursor** is unverified because no real Cursor run was collected.
- **Claude** is unverified because no real Claude run was collected.

The comparison demonstrates current-source Codex/Pi value without claiming
identical output, browser/device behavior, or unobserved Cursor/Claude
portability.
