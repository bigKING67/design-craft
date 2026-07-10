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
For `0.4.0`, Codex and Pi are observed for the dashboard, gesture-motion, and
native-adaptive benchmarks. Cursor and Claude remain explicitly unverified
because runnable outputs were not collected in this release.

Validate the recorded runs with:

```bash
python3 scripts/design_craft_cross_agent_validate.py \
  --observed-task evals/cross-agent/same-prompt-dashboard-review
python3 scripts/design_craft_cross_agent_validate.py \
  --observed-task evals/cross-agent/same-prompt-motion-review
python3 scripts/design_craft_cross_agent_validate.py \
  --observed-task evals/cross-agent/same-prompt-native-adaptive-review
```
