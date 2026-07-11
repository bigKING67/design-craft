# Codex frontend route pack

This pack documents how to keep the local Codex frontend routing layer
auditable and portable without copying all of `~/.codex` into this repository.

`design-craft` treats the local Codex route planner and platform detector as
runtime authority for task tiering, `web|ios|android|adaptive` resolution,
skill candidates, and browser/native evidence policy. The source files still
live in the Codex home directory; this adapter provides a safe manifest/export
workflow for migration or backup.

## Manifest authority

The only file-list authority is:

```text
~/.codex/tools/frontend_route_pack_manifest.json
```

The route-pack helper selects entries with `route_pack=true`; the global
snapshot selects entries with `snapshot=true`. Every required route-pack file
must also be snapshot-covered. The helper rejects an unknown manifest schema,
duplicate or unsafe paths, invalid field types, and a manifest that does not
include itself as a required route-pack file.

The current required route-pack core includes:

```text
AGENTS.md
rules/frontend.md
agents/worker.toml
tools/frontend_route_pack_manifest.json
tools/frontend_route_plan.sh
tools/frontend_route_core.py
tools/frontend_route_authority.py
tools/frontend_route_browser.py
tools/frontend_route_delivery.py
tools/frontend_route_runtime.py
tools/frontend_route_telemetry.py
tools/frontend_platform_detect.py
tools/frontend_agent_routing.json
tools/frontend_agent_routing.schema.json
tools/frontend_route_schema_validate.py
tools/frontend_worker_entry.sh
tools/frontend_worker_route_core.py
tools/frontend_worker_payload_core.py
tools/frontend_preflight_spec.json
tools/frontend_preflight.py
tools/frontend_preflight_run.sh
tools/frontend_preflight_verify.sh
tools/agents_quality_verify.sh
tools/tests/test_frontend_route_plan.sh
tools/tests/test_frontend_route_telemetry.sh
tools/tests/test_frontend_route_contract.sh
tools/tests/test_frontend_delivery_contract.sh
tools/tests/test_frontend_preflight.sh
tools/tests/test_frontend_preflight_spec_sync.sh
```

Optional helpers, such as preflight policy/report/log scripts, are included
when their manifest entries use `route_pack=true` and the files are present.

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
- manifest schema, selected/required counts, and required snapshot coverage
- routing JSON Schema validation plus V2 semantics and stale-model checks
- split authority, browser, delivery, runtime, and telemetry module contracts
- browser/runtime tool parity probes for external and local contexts
- a verified `gpt-5.6-sol/max` environment-runtime truth probe with session
  discovery disabled
- an unauthorized GPT-5.6 `ultra` runtime-conflict denial probe
- a privacy-safe telemetry self-check that remains isolated from inherited test
  context
- PRODUCT.md/codebase platform detection and native-runtime evidence boundaries
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
Strict route probes also disable route telemetry writes and current-session
discovery, so an audit neither pollutes production latency history nor reads the
caller's session JSONL.

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
├── tools/frontend_route_pack_manifest.json
├── tools/frontend_route_core.py
├── tools/frontend_worker_route_core.py
├── tools/frontend_worker_payload_core.py
├── tools/frontend_agent_routing.schema.json
├── tools/frontend_route_schema_validate.py
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
bash ~/.codex/tools/tests/test_frontend_route_telemetry.sh
bash ~/.codex/tools/tests/test_frontend_delivery_contract.sh
bash ~/.codex/tools/tests/test_frontend_route_contract.sh
bash ~/.codex/tools/tests/test_frontend_preflight_spec_sync.sh
bash ~/.codex/tools/tests/test_frontend_preflight.sh
bash ~/.codex/tools/frontend_preflight_verify.sh
bash ~/.codex/tools/agents_quality_verify.sh --fast
```

## Runtime truth and privacy boundary

Runtime model/reasoning resolution uses this evidence order:

```text
paired CODEX_EFFECTIVE_MODEL / CODEX_EFFECTIVE_REASONING
> current CODEX_THREAD_ID session's latest turn_context model/effort
> config.toml candidate values, explicitly unverified
```

Session discovery reads only `turn_context` records and only the `model`,
`effort`, `turn_id`, and `current_date` fields. Route output discloses only a
Codex-home-relative evidence path and marks `contains_prompt_data=false`; it
does not return prompts, messages, tool payloads, or absolute home paths.

## Route telemetry boundary

The planner appends a fixed privacy-safe event schema to
`~/.codex/logs/frontend_route_telemetry.jsonl` by default. Events contain only
bounded enums, booleans, counts, and millisecond timings. They do not contain
task prose, source code, PRODUCT/DESIGN paths, tokens, credentials, or session
content. The default log rotates at 2 MB with seven retained files.

Use `FRONTEND_ROUTE_TELEMETRY_CONTEXT=prod|test|ci` to isolate histories and
`FRONTEND_ROUTE_TELEMETRY_LOG_ENABLED=0` for probes or tests that should not
write. Summarize production latency and quality with:

```bash
python3 ~/.codex/tools/frontend_route_telemetry.py \
  --include-rotated \
  --context prod \
  --min-events 6 \
  --max-p95-ms 1000 \
  --json
```

The summary reports p50/p95/max durations, route/tier/platform/tool/runtime
source distributions, parse errors, and the privacy marker. The general route
test and release route smoke disable telemetry; the dedicated telemetry test
owns append, context, rotation, summary, and self-check coverage.

## Screenshot policy boundary

The route pack owns the operational screenshot decision:

```text
screenshot_evidence_level = none | optional | required
```

Global rules should state the principle. The route planner should decide the
actual evidence level from task surface, intent, scope, reference fidelity,
responsive risk, motion risk, and page-level visual impact.

## Platform and runtime boundary

The route pack resolves platform in this order:

```text
explicit --platform
> nearest PRODUCT.md ## Platform
> codebase detection
> default web
```

`surface=mobile` does not imply native. Web shells remain `web`; React
Native/Expo, Flutter, KMP, and real iOS plus Android targets resolve to
`adaptive`. Route output exposes `platform_source`, confidence, signals,
contradictions, `runtime_validation_kind`, `native_validation_required`, and
`preferred_runtime_tool`. Static scan/fixture success is never simulator,
emulator, or device proof.

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
