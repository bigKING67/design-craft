# Evaluation layout

`evals/` separates executable specifications, current machine evidence,
fixtures, and immutable history.

- `specs/`: reusable human-readable evaluation prompts and expected behavior.
- `fixtures/`: deterministic scanner, route, platform, and L4 test inputs.
- `golden-tasks/`: stable replayable task cards.
- `comparative/`: current comparative contracts and derived scorecards;
  archived observed runs live under `comparative/history/`.
- `cross-agent/`: current host status and score contracts; archived observed
  runs live under `cross-agent/history/`.
- `native-runtime/`: native fixtures and evidence contracts, with its own
  history boundary.
- `product-ui-taste/`: calibrated product UI evaluation cases.
- `history/`: retired repository-level narrative logs that cannot satisfy a
  current gate.

Current machine truth must be JSON validated by the owning schema or contract.
Markdown may define a spec, render a deterministic view from that JSON, or
preserve immutable history; it must not become a second writable status store.
