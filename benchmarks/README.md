# Performance benchmarks

The benchmark runner measures executable behavior rather than documentation or
keyword presence. It uses only the Python standard library and creates every
mutable fixture under one `TemporaryDirectory`. Installer cases override both
`DESIGN_CRAFT_SKILL_ROOT` and `DESIGN_CRAFT_BACKUP_ROOT`; they never read or
write the active `~/.agents` installation.

## Suites

The smoke suite records:

- portable route selection and the isolated Codex route-pack self-check;
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

The full suite adds the 100k-file tree and records at least 20 samples for every
metric so p95 is not a single maximum observation. Release maturity runs this
suite without competing maturity gates. Native evidence collection and final
release certification are intentionally not benchmark fixtures: those require
real current-source workflow or device evidence and must not be fabricated for
timing.

The route-pack benchmark deliberately uses its built-in temporary self-check
fixture. It must not read the operator's `~/.codex` tree, so local and CI runs
measure the same portable contract instead of leaking host configuration.

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
same controlled runner family. Result schema v2 records a stable hard identity
(`os`, `arch`, runner image family, Python major/minor, and benchmark policy)
separately from diagnostic drift (kernel string, runner image patch, and Python
patch). Kernel or hosted-image patch rotation therefore does not masquerade as a
performance regression, while a real OS, architecture, image-family, or Python
minor change still fails closed. Collect at least three full runs before
promoting a hosted-runner baseline. At least two real artifacts must form a
reproducible cluster under `compare_results`; never synthesize an average or
promote the fastest isolated artifact. Record the selected run URL and artifact
SHA-256 in the promotion PR.

The v1 reader remains available only for reviewed transition. A v1 comparison
emits an explicit warning because the old result did not bind a runner image
family. Do not edit an old baseline in place. Migrate it to a new file with the
reviewed identity values, then commit both provenance and the new baseline:

```bash
python3 -m tools.design_craft benchmark \
  --migrate-v1 benchmarks/baselines/v0.5.0-linux-x86_64-python3.13.json \
  --runner-image ubuntu-24.04 \
  --image-version <recorded-image-version> \
  --node-version <recorded-node-version> \
  --output benchmarks/baselines/v0.5.0-linux-x86_64-python3.13-v2.json
```

The comparison fails closed when schema, scale, stable runner identity, policy,
metric set, sample count, numeric timing, or specialized safety metadata is
missing or inconsistent.

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
