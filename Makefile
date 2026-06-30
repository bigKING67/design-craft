.PHONY: validate score pass audit critique motion taste-review seed-dry-run upstream-report upstream-remote-report install legacy-alias-smoke release-gate

validate:
	bash scripts/validate.sh

score:
	python3 scripts/design_craft_score.py --self

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
	bash scripts/design_craft_seed_design.sh --target . --dry-run

upstream-report:
	python3 scripts/upstream_absorption_report.py

upstream-remote-report:
	python3 scripts/upstream_absorption_report.py --remote

install:
	bash scripts/install_local.sh

legacy-alias-smoke:
	bash scripts/frontend_craft_pass.sh --target skills/design-craft --mode motion --skip-route --skip-score >/dev/null
	grep -Fq 'renamed to `design-craft`' /Users/gaoqian/.agents/skills/frontend-craft/SKILL.md

release-gate: validate score pass audit critique motion taste-review seed-dry-run upstream-report upstream-remote-report install legacy-alias-smoke
	diff -qr skills/design-craft /Users/gaoqian/.agents/skills/design-craft
