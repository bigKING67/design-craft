.PHONY: validate score audit install release-gate

validate:
	bash scripts/validate.sh

score:
	python3 scripts/frontend_craft_score.py --self

audit:
	bash scripts/frontend_craft_audit.sh --target . --mode audit --skip-route

install:
	bash scripts/install_local.sh

release-gate: validate score audit install
	diff -qr skills/frontend-craft /Users/gaoqian/.agents/skills/frontend-craft
