# Codex frontend route pack

This pack documents how to keep the local Codex frontend routing layer
auditable and portable without copying all of `~/.codex` into this repository.

`design-craft` treats the local Codex route planner as runtime authority for
frontend task tiering, skill candidates, browser validation, and screenshot
evidence policy. The source files still live in the Codex home directory; this
adapter provides a safe manifest/export workflow for migration or backup.

## Whitelisted files

The route pack tracks only frontend-routing files:

```text
AGENTS.md
rules/frontend.md
agents/worker.toml
tools/frontend_route_plan.sh
tools/frontend_agent_routing.json
tools/frontend_worker_entry.sh
tools/frontend_preflight_spec.json
tools/frontend_preflight.py
tools/frontend_preflight_run.sh
tools/frontend_preflight_verify.sh
tools/agents_quality_verify.sh
tools/tests/test_frontend_route_plan.sh
tools/tests/test_frontend_route_contract.sh
tools/tests/test_frontend_delivery_contract.sh
tools/tests/test_frontend_preflight.sh
tools/tests/test_frontend_preflight_spec_sync.sh
```

Optional helpers, such as preflight policy/report/log scripts, are included in
the manifest and export when present.

The pack intentionally excludes credentials, browser profiles, MCP state,
session logs, caches, and unrelated Codex configuration.

## Audit current local state

```bash
python3 scripts/design_craft_codex_route_pack.py --strict
```

This prints:

- schema version
- source root
- required-file status
- missing required files, if any
- V2 routing semantics and stale-model checks
- redacted runtime model/profile compatibility from `config.toml`
- bundled model-catalog compatibility for configured reasoning levels

For machine-readable evidence:

```bash
python3 scripts/design_craft_codex_route_pack.py --strict --json
```

The JSON manifest records file paths, size, SHA-256, executable bit, whether
each file is required, and a redacted `semantic_validation` result. It reads
only model/profile fields from `config.toml`; credentials, MCP settings,
provider URLs, browser state, and unrelated configuration are never exported.

## Export a migration bundle

Write a whitelisted copy outside the repo:

```bash
python3 scripts/design_craft_codex_route_pack.py \
  --strict \
  --export-dir /tmp/design-craft-codex-route-pack
```

The export writes:

```text
/tmp/design-craft-codex-route-pack/
├── AGENTS.md
├── agents/worker.toml
├── rules/frontend.md
├── tools/...
└── codex-route-pack.manifest.json
```

Use `--dry-run` before writing:

```bash
python3 scripts/design_craft_codex_route_pack.py \
  --export-dir /tmp/design-craft-codex-route-pack \
  --dry-run
```

## Validate after restore

After restoring the bundle into another Codex home, run:

```bash
bash ~/.codex/tools/tests/test_frontend_route_plan.sh
bash ~/.codex/tools/tests/test_frontend_delivery_contract.sh
bash ~/.codex/tools/tests/test_frontend_route_contract.sh
bash ~/.codex/tools/tests/test_frontend_preflight_spec_sync.sh
bash ~/.codex/tools/tests/test_frontend_preflight.sh
bash ~/.codex/tools/frontend_preflight_verify.sh
bash ~/.codex/tools/agents_quality_verify.sh --fast
```

## Screenshot policy boundary

The route pack owns the operational screenshot decision:

```text
screenshot_evidence_level = none | optional | required
```

Global rules should state the principle. The route planner should decide the
actual evidence level from task surface, intent, scope, reference fidelity,
responsive risk, motion risk, and page-level visual impact.

## Model and delegation boundary

The route pack validates these V2 invariants:

- the main agent owns every tier by default
- route files use `agent_model=inherit` instead of pinning a model version
- tier alone never sets `subagent_required=true`
- parallel work requires at least two independent tasks, bounded write scopes,
  clear benefit, and user or project authorization
- unavailable delegation falls back to `continue_main_and_report`
- `worker.toml` inherits model and reasoning from the parent/runtime profile
- explicit reasoning overrides support `low` through `max`; GPT-5.6 `ultra`
  remains runtime-profile-only because its model-catalog semantics include
  automatic task delegation
- configured runtime models and reasoning levels exist in the bundled Codex
  model catalog
