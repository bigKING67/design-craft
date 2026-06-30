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
