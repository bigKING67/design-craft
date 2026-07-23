# Performance benchmarks

The benchmark runner measures executable behavior rather than documentation or
keyword presence. It uses only the Python standard library and creates every
mutable fixture under one `TemporaryDirectory`. Installer cases override both
`DESIGN_CRAFT_SKILL_ROOT` and `DESIGN_CRAFT_BACKUP_ROOT`; they never read or
write the active `~/.agents` installation.

## Suites

The smoke suite records:

- portable route selection and strict Codex route-pack validation;
- 1k and 10k file-tree hashing;
- validation registry load, full lint, evidence validation, and package
  validation;
- explicit incremental validation for exactly 1, 10, and 100 changed files;
- bounded digest-cache cold, warm, and overflow behavior, including hit, miss,
  eviction, and maximum-entry counters;
- atomic installation into an isolated root;
- after-switch rollback timing with byte-for-byte restoration verification;
- live-lock contention with a zero-second timeout, including proof that no
  install target was created;
- two operational npm release-package builds whose size and SHA-256 must match.

The full suite adds the 100k-file tree, increases sample counts, and repeats the
installer and release-package cases. Native evidence collection and final
release certification are intentionally not benchmark fixtures: those require
real current-source workflow or device evidence and must not be fabricated for
timing.

```bash
python3 -m tools.design_craft benchmark --scale smoke --json
python3 -m tools.design_craft benchmark --scale full --json
```

The suite does not create or update a formal baseline. A caller may explicitly
write a disposable result and compare two controlled runs:

```bash
tmp_dir="$(mktemp -d -t design-craft-benchmark.XXXXXX)"
python3 -m tools.design_craft benchmark \
  --scale smoke \
  --output "$tmp_dir/base.json" \
  --json >/dev/null
python3 -m tools.design_craft benchmark \
  --scale smoke \
  --baseline "$tmp_dir/base.json" \
  --json
```

Do not commit a result as a release baseline until base and head have run on the
same controlled runner. The comparison fails closed when schema, scale,
runner, Python, platform, policy, metric set, sample count, numeric timing, or
specialized safety metadata is missing or inconsistent.

`.github/workflows/benchmark.yml` runs the smoke suite for pushes and pull
requests, and the full suite for the nightly schedule or an explicit manual
dispatch. Each run uploads the complete result JSON; smoke artifacts are kept
for 30 days and full artifacts for 90 days. These artifacts are execution
evidence, not automatically promoted release baselines. Baseline promotion
still requires controlled same-runner comparison and review.

For comparable results, a regression fails only when p95 is both more than 15%
slower and more than 50 ms slower. Cache, rollback, lock-contention, temporary
root, and deterministic-bundle assertions are correctness contracts rather
than timing thresholds; violating one invalidates the result before timing is
compared.
