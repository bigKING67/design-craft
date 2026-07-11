# Cross-agent benchmark evals

Use this directory to compare how Codex, Cursor, Claude, Pi, or another
Agent Skills-compatible client applies `design-craft` to the same prompt.

The goal is not identical prose. The goal is stable behavior:

- Reads or respects project style authority.
- Selects the relevant references without loading everything.
- Avoids generic redesign over project context.
- Produces an evidence-labeled design read or critique.
- Separates verified from unverified claims.
- Gives executable design moves when asked for implementation direction.
- Does not over-modify unrelated code.

Template directories are scaffolding only; they are not completed benchmarks.

Validate active benchmark task definitions with:

```bash
python3 scripts/design_craft_cross_agent_validate.py --root evals/cross-agent
```

The validator checks active `same-prompt-*` task directories, not `_template/`.

Observed benchmark outputs are intentionally host-specific. A host only counts
as verified after it runs the same prompt and records an output plus score JSON.
Legacy v1 Codex and Pi artifacts remain the documented 95/100 baseline for the
dashboard, gesture-motion, and native-adaptive benchmarks. The validator treats
each of Codex, Pi, Cursor,
and Claude independently: a host must provide both a real output and score JSON,
or retain an explicit unverified note. A partial pair is rejected, and a stale
unverified note is rejected after evidence is recorded.

As of 2026-07-11, Cursor Agent is installed but not logged in. Claude Code's
configured custom API base is unreachable; a command-scoped official-endpoint
override connects but rejects the existing bearer with HTTP 401. Those host
preflights are evidence of the current blockers, not observed benchmark output.

Validate the recorded runs with:

```bash
python3 scripts/design_craft_cross_agent_validate.py \
  --observed-task evals/cross-agent/same-prompt-dashboard-review
python3 scripts/design_craft_cross_agent_validate.py \
  --observed-task evals/cross-agent/same-prompt-motion-review
python3 scripts/design_craft_cross_agent_validate.py \
  --observed-task evals/cross-agent/same-prompt-native-adaptive-review
```

Require specific hosts when collecting a release-evidence tranche:

```bash
python3 scripts/design_craft_cross_agent_validate.py \
  --observed-task evals/cross-agent/same-prompt-native-adaptive-review \
  --require-host codex \
  --require-host pi \
  --require-host cursor \
  --require-host claude
```

Certified 100/100 evidence additionally requires schema v2 and a current skill
version/tree. `make cross-agent-four-host-check` applies this contract to every
active observed task and stops on the first failure:

```bash
python3 scripts/design_craft_cross_agent_validate.py \
  --observed-task evals/cross-agent/same-prompt-native-adaptive-review \
  --require-host codex \
  --require-host pi \
  --require-host cursor \
  --require-host claude \
  --require-schema-v2 \
  --require-current-source
```

Create v2 score JSON with `scripts/design_craft_cross_agent_record.py`. Copy
`_template/criteria.json`, assign each criterion an earned value within its
scorecard weight, and preserve the exact `<host>-output.md`. The recorder
computes the score and records hashes for the prompt, scorecard, output, and
skill tree plus the source commit, version, model, reasoning profile, host
version, and runner OS. Host-home paths are stored with a `~/` prefix rather
than a public absolute path. Do not backfill model, version, or reasoning fields
onto an older run; deterministic path redaction does not alter the observed
output or score.
