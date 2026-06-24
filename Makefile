.PHONY: validate score pass audit critique seed-dry-run upstream-report install release-gate

validate:
	bash scripts/validate.sh

score:
	python3 scripts/frontend_craft_score.py --self

pass:
	bash scripts/frontend_craft_pass.sh --target . --mode audit --skip-route

audit:
	bash scripts/frontend_craft_audit.sh --target . --mode audit --skip-route

critique:
	bash scripts/frontend_craft_audit.sh --target . --mode critique --skip-route

seed-dry-run:
	bash scripts/frontend_craft_seed_design.sh --target . --dry-run

upstream-report:
	python3 scripts/upstream_absorption_report.py

install:
	bash scripts/install_local.sh

release-gate: validate score pass audit critique seed-dry-run upstream-report install
	diff -qr skills/frontend-craft /Users/gaoqian/.agents/skills/frontend-craft
