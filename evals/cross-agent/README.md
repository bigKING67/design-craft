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
Legacy v2 Codex and Pi artifacts are preserved as self-contained snapshots
under `history/2026-07-11-v2/`. They are historical baseline evidence only and
are excluded from active release validation because the active prompts,
scorecards, runner, and score contract changed. The validator treats each of
Codex, Pi, Cursor, and Claude independently: a host must provide both a real
output and score JSON, or retain an explicit unverified note. A partial pair is
rejected, and a stale unverified note is rejected after evidence is recorded.

As of 2026-07-12, Codex and Pi have current-source v3 score/run-v2 evidence for
all three active tasks, bound to Skill source commit `f04e105`. Cursor remains
unverified because its installed CLI is not logged in. Claude remains
unverified because its valid OAuth session still returns `ECONNRESET` during a
controlled read-only request. Environment preflights are status only, not
observed benchmark output. Do not restore historical outputs to active
directories or edit their hashes; rerun the controlled host instead.

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

Certified 100/100 evidence additionally requires score schema v3, run-manifest
schema v2, a current skill tree, and a current runner/adapter contract hash.
`make cross-agent-four-host-check` applies this contract to every active
observed task and stops on the first failure:

```bash
python3 scripts/design_craft_cross_agent_validate.py \
  --observed-task evals/cross-agent/same-prompt-native-adaptive-review \
  --require-host codex \
  --require-host pi \
  --require-host cursor \
  --require-host claude \
  --require-current-schema \
  --require-current-source
```

Capture the exact prompt and read-only invocation first:

```bash
python3 scripts/design_craft_cross_agent_run.py \
  --task-dir evals/cross-agent/same-prompt-motion-review \
  --host codex \
  --model <model> \
  --reasoning-profile <profile> \
  --skill-root skills/design-craft
```

The runner copies that exact tree into a repo-external isolated project skill
path for the selected host, records the copied tree hash and redacted path, runs
the host read-only, verifies a content-level source-worktree fingerprint, and
only then transactionally publishes `<host>-output.md` plus `run.<host>.json`.
Do not point a certified run at a stale user-level install.

Then create v3 score JSON with `scripts/design_craft_cross_agent_record.py` and
the generated `run.<host>.json`. Copy `_template/criteria.json`, assign each
criterion an earned value within its
scorecard weight, and preserve the exact `<host>-output.md`. The recorder
computes the score and records hashes for the prompt, scorecard, output, run
manifest, skill tree, and runner/adapter contract plus the source commit,
version, model, reasoning profile, host version, and runner OS. Canonical repo
paths use `$DESIGN_CRAFT_HOME`; installed host paths use a home-relative form.
Do not backfill v3 fields onto an older run.
