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
tools/frontend_route_plan.sh
tools/frontend_agent_routing.json
tools/frontend_worker_entry.sh
tools/frontend_preflight_spec.json
tools/frontend_preflight.py
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

For machine-readable evidence:

```bash
python3 scripts/design_craft_codex_route_pack.py --strict --json
```

The JSON manifest records file paths, size, SHA-256, executable bit, and whether
each file is required.

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
