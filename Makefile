DESIGN_CRAFT_SKILL_ROOT ?= $(HOME)/.agents/skills
SKILL_CREATOR_QUICK_VALIDATE ?= $(HOME)/.codex/skills/.system/skill-creator/scripts/quick_validate.py
export PYTHONDONTWRITEBYTECODE := 1

.PHONY: validate validate-portable skill-quick-validate score maturity-portable maturity-local pass audit critique motion taste-review seed-dry-run route-smoke doctor platform-scan-check codex-route-pack-check init-dry-run active-scope-check cross-agent-check cross-agent-observed-check cross-agent-motion-observed-check cross-agent-native-observed-check l4-capture-check real-l4-check smell-smoke static-review-smoke upstream-report upstream-remote-report install install-with-legacy legacy-alias-smoke release-gate-local release-gate

validate:
	bash scripts/validate.sh

validate-portable:
	bash scripts/validate.sh --portable

skill-quick-validate:
	python3 "$(SKILL_CREATOR_QUICK_VALIDATE)" skills/design-craft
	python3 "$(SKILL_CREATOR_QUICK_VALIDATE)" skills/frontend-craft

score:
	python3 scripts/design_craft_score.py --self

maturity-portable:
	python3 scripts/design_craft_maturity.py --profile portable --min-score 95

maturity-local: install
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
	bash scripts/design_craft_route.sh --target "$$tmp_dir" --surface dashboard --intent visual-refine --scope page >/dev/null

doctor:
	bash scripts/design_craft_doctor.sh --target . --json >/dev/null

platform-scan-check:
	@set -e; for platform in ios android adaptive; do python3 scripts/design_craft_platform_scan.py --target "evals/fixtures/platforms/$$platform/valid" --json --strict >/dev/null; if python3 scripts/design_craft_platform_scan.py --target "evals/fixtures/platforms/$$platform/invalid" --json --strict >/dev/null 2>&1; then echo "$$platform invalid platform fixture unexpectedly passed" >&2; exit 1; fi; done

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

cross-agent-motion-observed-check:
	python3 scripts/design_craft_cross_agent_validate.py --observed-task evals/cross-agent/same-prompt-motion-review >/dev/null

cross-agent-native-observed-check:
	python3 scripts/design_craft_cross_agent_validate.py --observed-task evals/cross-agent/same-prompt-native-adaptive-review >/dev/null

l4-capture-check:
	python3 scripts/design_craft_l4_capture.py --check >/dev/null

real-l4-check:
	@case_dir="evals/product-ui-taste/before-after/data""hub-live""-center-review-workbench"; \
	python3 scripts/design_craft_l4_case_validate.py --case-dir "$$case_dir" --strict >/dev/null

smell-smoke:
	python3 scripts/design_craft_css_smell_scan.py --target evals/fixtures/css-smells --json >/dev/null
	python3 scripts/design_craft_focus_audit.py --target evals/fixtures/focus-smells --json >/dev/null
	python3 scripts/design_craft_token_audit.py --target evals/fixtures/token-smells --json >/dev/null
	python3 scripts/design_craft_static_review.py --target evals/fixtures --json >/dev/null

static-review-smoke:
	python3 scripts/design_craft_static_review.py --target evals/fixtures --json >/dev/null

upstream-report:
	python3 scripts/upstream_absorption_report.py

upstream-remote-report:
	python3 scripts/upstream_absorption_report.py --remote --fail-on-unreviewed

install:
	bash scripts/install_local.sh

install-with-legacy:
	bash scripts/install_local.sh --include-legacy-alias

legacy-alias-smoke:
	bash scripts/frontend_craft_pass.sh --target skills/design-craft --mode motion --skip-route --skip-score >/dev/null
	grep -Fq 'renamed to `design-craft`' skills/frontend-craft/SKILL.md

release-gate-local: validate-portable skill-quick-validate score maturity-portable pass audit critique motion taste-review seed-dry-run route-smoke doctor platform-scan-check codex-route-pack-check init-dry-run active-scope-check cross-agent-check cross-agent-observed-check l4-capture-check real-l4-check smell-smoke upstream-report upstream-remote-report maturity-local legacy-alias-smoke
	diff -qr skills/design-craft "$(DESIGN_CRAFT_SKILL_ROOT)/design-craft"

release-gate: release-gate-local
