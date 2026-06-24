.PHONY: validate score audit upstream-report install release-gate

validate:
	bash scripts/validate.sh

score:
	python3 scripts/frontend_craft_score.py --self

audit:
	bash scripts/frontend_craft_audit.sh --target . --mode audit --skip-route

upstream-report:
	python3 scripts/upstream_absorption_report.py

install:
	bash scripts/install_local.sh

release-gate: validate score audit upstream-report install
	diff -qr skills/frontend-craft /Users/gaoqian/.agents/skills/frontend-craft
