.PHONY: validate score pass audit critique taste-review seed-dry-run upstream-report upstream-remote-report install release-gate

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

taste-review:
	bash scripts/frontend_craft_taste_review.sh --target skills/frontend-craft --context "release smoke" --evidence-level L0 >/dev/null

seed-dry-run:
	bash scripts/frontend_craft_seed_design.sh --target . --dry-run

upstream-report:
	python3 scripts/upstream_absorption_report.py

upstream-remote-report:
	python3 scripts/upstream_absorption_report.py --remote

install:
	bash scripts/install_local.sh

release-gate: validate score pass audit critique taste-review seed-dry-run upstream-report upstream-remote-report install
	diff -qr skills/frontend-craft /Users/gaoqian/.agents/skills/frontend-craft
