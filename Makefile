DESIGN_CRAFT_SKILL_ROOT ?= $(HOME)/.agents/skills
SKILL_CREATOR_QUICK_VALIDATE ?= $(HOME)/.codex/skills/.system/skill-creator/scripts/quick_validate.py
INSTALL_ARGS ?=
export PYTHONDONTWRITEBYTECODE := 1

.PHONY: validate validate-portable package-check public-repo-check workflow-check skill-quick-validate score maturity-portable maturity-local pass audit critique motion taste-review seed-dry-run route-smoke doctor platform-scan-check native-runtime-probe native-runtime-check codex-route-pack-check init-dry-run active-scope-check cross-agent-check cross-agent-observed-check cross-agent-four-host-check cross-agent-motion-observed-check cross-agent-native-observed-check l4-capture-check historical-l4-metadata-check real-l4-check smell-smoke static-review-smoke upstream-report upstream-freshness-audit upstream-remote-report sync-status sync-status-remote install install-with-legacy install-verify legacy-alias-smoke release-contract-check github-release-check release-gate-source publish-local release-gate-local release-gate release-readiness certification-install-check release-certify-prepublish release-certify-publish release-certify-internal release-certify release-tag-verify

validate:
	bash scripts/validate.sh

validate-portable:
	bash scripts/validate.sh --portable

package-check:
	python3 scripts/design_craft_package_validate.py --check --validate

public-repo-check:
	python3 scripts/design_craft_public_repo_validate.py --check --validate

workflow-check:
	python3 scripts/design_craft_workflow_validate.py --check --validate

skill-quick-validate:
	python3 "$(SKILL_CREATOR_QUICK_VALIDATE)" skills/design-craft
	python3 "$(SKILL_CREATOR_QUICK_VALIDATE)" skills/frontend-craft

score:
	python3 scripts/design_craft_score.py --self

maturity-portable:
	python3 scripts/design_craft_maturity.py --profile portable --min-score 95

maturity-local:
	python3 scripts/design_craft_maturity.py --profile local --min-score 95

pass:
	bash scripts/design_craft_pass.sh --target . --mode audit --skip-route

audit:
	bash scripts/design_craft_audit.sh --target . --mode audit --skip-route

critique:
	bash scripts/design_craft_audit.sh --target . --mode critique --skip-route

motion:
	bash scripts/design_craft_pass.sh --target skills/design-craft --mode motion --skip-route --skip-score

taste-review:
	bash scripts/design_craft_taste_review.sh --target skills/design-craft --context "release smoke" --evidence-level L0 >/dev/null

seed-dry-run:
	@tmp_dir="$$(mktemp -d -t design-craft-seed-dry-run.XXXXXX)" && trap 'rm -rf "$$tmp_dir"' EXIT && bash scripts/design_craft_seed_design.sh --target "$$tmp_dir" --dry-run

route-smoke:
	@tmp_dir="$$(mktemp -d -t design-craft-route-smoke.XXXXXX)"; \
	trap 'rm -rf "$$tmp_dir"' EXIT; \
	{ \
	  printf '%s\n' '# Project Design Authority'; \
	  printf '%s\n' ''; \
	  printf '%s\n' '## Typography System'; \
	  printf '%s\n' 'Readable typography contract.'; \
	  printf '%s\n' ''; \
	  printf '%s\n' '## Color Palette'; \
	  printf '%s\n' 'Token-backed color system.'; \
	  printf '%s\n' ''; \
	  printf '%s\n' '## Motion Language'; \
	  printf '%s\n' 'Calm interaction language.'; \
	  printf '%s\n' ''; \
	  printf '%s\n' '## Component Grammar'; \
	  printf '%s\n' 'Reusable component rules.'; \
	} > "$$tmp_dir/DESIGN.md"; \
		FRONTEND_ROUTE_TELEMETRY_LOG_ENABLED=0 FRONTEND_RUNTIME_SESSION_DISCOVERY=0 \
		  bash scripts/design_craft_route.sh --target "$$tmp_dir" --surface dashboard --intent visual-refine --scope page >/dev/null

doctor:
	bash scripts/design_craft_doctor.sh --target . --json >/dev/null

platform-scan-check:
	@set -e; for platform in ios android adaptive; do python3 scripts/design_craft_platform_scan.py --target "evals/fixtures/platforms/$$platform/valid" --json --strict >/dev/null; if python3 scripts/design_craft_platform_scan.py --target "evals/fixtures/platforms/$$platform/invalid" --json --strict >/dev/null 2>&1; then echo "$$platform invalid platform fixture unexpectedly passed" >&2; exit 1; fi; done

native-runtime-probe:
	python3 scripts/design_craft_native_runtime_validate.py --write-probe evals/native-runtime/environment-probe.json --json

native-runtime-check:
	python3 scripts/design_craft_native_runtime_validate.py --validate --require ios --require android --require-real-device --require-current-source --json

codex-route-pack-check:
	python3 scripts/design_craft_codex_route_pack.py --check >/dev/null
	python3 scripts/design_craft_codex_route_pack.py --strict >/dev/null

init-dry-run:
	@tmp_dir="$$(mktemp -d -t design-craft-init.XXXXXX)"; \
	trap 'rm -rf "$$tmp_dir"' EXIT; \
	bash scripts/design_craft_init_agent.sh --agent codex --target "$$tmp_dir" --scope project --dry-run >/dev/null; \
	bash scripts/design_craft_init_agent.sh --agent cursor --target "$$tmp_dir" --scope project --with-rule --dry-run >/dev/null; \
	bash scripts/design_craft_init_agent.sh --agent claude --target "$$tmp_dir" --scope project --dry-run >/dev/null; \
	bash scripts/design_craft_init_agent.sh --agent pi --target "$$tmp_dir" --scope project --dry-run >/dev/null; \
	bash scripts/design_craft_init_agent.sh --agent generic --target "$$tmp_dir" --scope project --dry-run >/dev/null

active-scope-check:
	python3 scripts/design_craft_active_scope_validate.py --root . >/dev/null

cross-agent-check:
	python3 scripts/design_craft_cross_agent_validate.py --root evals/cross-agent >/dev/null

cross-agent-observed-check:
	python3 scripts/design_craft_cross_agent_validate.py --observed-task evals/cross-agent/same-prompt-dashboard-review >/dev/null
	python3 scripts/design_craft_cross_agent_validate.py --observed-task evals/cross-agent/same-prompt-motion-review >/dev/null
	python3 scripts/design_craft_cross_agent_validate.py --observed-task evals/cross-agent/same-prompt-native-adaptive-review >/dev/null

cross-agent-four-host-check:
	@set -e; for task in same-prompt-dashboard-review same-prompt-motion-review same-prompt-native-adaptive-review; do python3 scripts/design_craft_cross_agent_validate.py --observed-task "evals/cross-agent/$$task" --require-host codex --require-host pi --require-host cursor --require-host claude --require-schema-v2 --require-current-source; done

cross-agent-motion-observed-check:
	python3 scripts/design_craft_cross_agent_validate.py --observed-task evals/cross-agent/same-prompt-motion-review >/dev/null

cross-agent-native-observed-check:
	python3 scripts/design_craft_cross_agent_validate.py --observed-task evals/cross-agent/same-prompt-native-adaptive-review >/dev/null

l4-capture-check:
	python3 scripts/design_craft_l4_capture.py --check >/dev/null

historical-l4-metadata-check:
	@case_dir="evals/product-ui-taste/before-after/data""hub-live""-center-review-workbench"; \
	python3 scripts/design_craft_l4_case_validate.py --case-dir "$$case_dir" --strict >/dev/null

real-l4-check:
	@case_dir="evals/product-ui-taste/before-after/data""hub-live""-center-review-workbench"; \
	python3 scripts/design_craft_l4_case_validate.py --case-dir "$$case_dir" --strict --require-existing-files >/dev/null

smell-smoke:
	python3 scripts/design_craft_css_smell_scan.py --target evals/fixtures/css-smells --json >/dev/null
	python3 scripts/design_craft_focus_audit.py --target evals/fixtures/focus-smells --json >/dev/null
	python3 scripts/design_craft_token_audit.py --target evals/fixtures/token-smells --json >/dev/null
	python3 scripts/design_craft_static_review.py --target evals/fixtures --json >/dev/null

static-review-smoke:
	python3 scripts/design_craft_static_review.py --target evals/fixtures --json >/dev/null

upstream-report:
	python3 scripts/upstream_absorption_report.py

upstream-freshness-audit:
	python3 scripts/upstream_absorption_report.py --remote-details --fail-on-unreviewed

upstream-remote-report: upstream-freshness-audit

sync-status:
	python3 scripts/design_craft_sync_status.py

sync-status-remote:
	python3 scripts/design_craft_sync_status.py --remote

install:
	bash scripts/install_local.sh $(INSTALL_ARGS)

install-with-legacy:
	bash scripts/install_local.sh --include-legacy-alias $(INSTALL_ARGS)

install-verify:
	python3 scripts/design_craft_install_verify.py --source skills/design-craft --installed "$(DESIGN_CRAFT_SKILL_ROOT)/design-craft" --expected-name design-craft --expected-version "$$(cat VERSION)" --require-metadata
	@if [ -d "$(DESIGN_CRAFT_SKILL_ROOT)/frontend-craft" ]; then python3 scripts/design_craft_install_verify.py --source skills/frontend-craft --installed "$(DESIGN_CRAFT_SKILL_ROOT)/frontend-craft" --expected-name frontend-craft --expected-version "$$(cat VERSION)" --require-metadata; fi

legacy-alias-smoke:
	bash scripts/frontend_craft_pass.sh --target skills/design-craft --mode motion --skip-route --skip-score >/dev/null
	grep -Fq 'renamed to `design-craft`' skills/frontend-craft/SKILL.md

release-contract-check:
	python3 scripts/design_craft_release_verify.py

release-gate-source: validate-portable package-check public-repo-check workflow-check skill-quick-validate score maturity-portable pass audit critique motion taste-review seed-dry-run route-smoke doctor platform-scan-check codex-route-pack-check init-dry-run active-scope-check cross-agent-check cross-agent-observed-check l4-capture-check historical-l4-metadata-check smell-smoke upstream-report legacy-alias-smoke release-contract-check

publish-local: release-gate-source
	bash scripts/install_local.sh $(INSTALL_ARGS)
	python3 scripts/design_craft_maturity.py --profile local --min-score 95
	$(MAKE) install-verify

release-gate-local: publish-local

release-gate: release-gate-local

release-readiness: release-gate
	python3 scripts/upstream_absorption_report.py --remote-details --fail-on-unreviewed

certification-install-check:
	bash scripts/design_craft_certification_install_check.sh

release-certify-prepublish:
	python3 scripts/design_craft_release_verify.py --certify
	$(MAKE) release-gate-source
	python3 scripts/upstream_absorption_report.py --remote-details --fail-on-unreviewed
	$(MAKE) real-l4-check
	$(MAKE) cross-agent-four-host-check
	$(MAKE) native-runtime-check
	$(MAKE) certification-install-check

release-certify-publish:
	bash scripts/install_local.sh $(INSTALL_ARGS)
	$(MAKE) install-verify
	python3 scripts/design_craft_maturity.py --profile local --min-score 100

release-certify-internal:
	$(MAKE) release-certify-prepublish
	$(MAKE) release-certify-publish

release-certify:
	bash scripts/design_craft_release_certify.sh certify

github-release-check:
	python3 scripts/design_craft_github_checks.py

release-tag-verify:
	bash scripts/design_craft_release_certify.sh tag
