#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${PWD}"
JSON=0

usage() {
  cat <<'EOF'
Usage:
  scripts/design_craft_doctor.sh [--target <path>] [--json]

Checks portable design-craft prerequisites without modifying files.
EOF
}

abspath() {
  python3 - "$1" <<'PY'
import sys
from pathlib import Path
print(Path(sys.argv[1]).expanduser().resolve())
PY
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="${2:?Missing value for --target}"
      shift 2
      ;;
    --json)
      JSON=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

TARGET="$(abspath "${TARGET}")"

python3 - "${ROOT_DIR}" "${TARGET}" "${JSON}" <<'PY'
import json
import os
import shutil
import sys
from pathlib import Path

root = Path(sys.argv[1])
target = Path(sys.argv[2])
emit_json = sys.argv[3] == "1"
home = Path.home()

def check(name: str, ok: bool, detail: str) -> dict:
    return {"name": name, "ok": bool(ok), "detail": detail}

route_plan = Path(os.environ.get("DESIGN_CRAFT_ROUTE_PLAN", str(home / ".codex/tools/frontend_route_plan.sh")))
quick_validate = Path(os.environ.get("SKILL_CREATOR_QUICK_VALIDATE", str(home / ".codex/skills/.system/skill-creator/scripts/quick_validate.py")))
codex_home = Path(os.environ.get("CODEX_HOME", str(home / ".codex")))
route_pack_required = [
    "AGENTS.md",
    "rules/frontend.md",
    "tools/frontend_route_plan.sh",
    "tools/frontend_agent_routing.json",
    "tools/frontend_worker_entry.sh",
    "tools/frontend_preflight_spec.json",
    "tools/frontend_preflight.py",
    "tools/frontend_preflight_verify.sh",
    "tools/agents_quality_verify.sh",
    "tools/tests/test_frontend_route_plan.sh",
    "tools/tests/test_frontend_route_contract.sh",
    "tools/tests/test_frontend_delivery_contract.sh",
    "tools/tests/test_frontend_preflight.sh",
    "tools/tests/test_frontend_preflight_spec_sync.sh",
]
route_pack_missing = [rel for rel in route_pack_required if not (codex_home / rel).is_file()]

checks = [
    check("canonical skill", (root / "skills/design-craft/SKILL.md").is_file(), str(root / "skills/design-craft/SKILL.md")),
    check("legacy alias", (root / "skills/frontend-craft/SKILL.md").is_file(), str(root / "skills/frontend-craft/SKILL.md")),
    check("codex adapter", (root / "adapters/codex/README.md").is_file(), str(root / "adapters/codex/README.md")),
    check("codex route-pack docs", (root / "adapters/codex/route-pack/README.md").is_file(), str(root / "adapters/codex/route-pack/README.md")),
    check("cursor adapter", (root / "adapters/cursor/README.md").is_file(), str(root / "adapters/cursor/README.md")),
    check("claude adapter", (root / "adapters/claude/README.md").is_file(), str(root / "adapters/claude/README.md")),
    check("pi adapter", (root / "adapters/pi/README.md").is_file(), str(root / "adapters/pi/README.md")),
    check("generic adapter", (root / "adapters/generic/README.md").is_file(), str(root / "adapters/generic/README.md")),
    check("route planner", route_plan.is_file(), str(route_plan)),
    check("codex route pack helper", (root / "scripts/design_craft_codex_route_pack.py").is_file(), str(root / "scripts/design_craft_codex_route_pack.py")),
    check("codex route pack required files", not route_pack_missing, ", ".join(route_pack_missing) if route_pack_missing else str(codex_home)),
    check("quick validator", quick_validate.is_file(), str(quick_validate)),
    check("browser evidence helper", (root / "scripts/design_craft_browser_evidence.py").is_file(), str(root / "scripts/design_craft_browser_evidence.py")),
    check("css smell scanner", (root / "scripts/design_craft_css_smell_scan.py").is_file(), str(root / "scripts/design_craft_css_smell_scan.py")),
    check("focus audit scanner", (root / "scripts/design_craft_focus_audit.py").is_file(), str(root / "scripts/design_craft_focus_audit.py")),
    check("token audit scanner", (root / "scripts/design_craft_token_audit.py").is_file(), str(root / "scripts/design_craft_token_audit.py")),
    check("python3", shutil.which("python3") is not None, shutil.which("python3") or "missing"),
    check("bash", shutil.which("bash") is not None, shutil.which("bash") or "missing"),
    check("target exists", target.exists(), str(target)),
    check("target writable", os.access(target if target.exists() else target.parent, os.W_OK), str(target)),
]

payload = {
    "root": str(root),
    "target": str(target),
    "ok": all(
        item["ok"]
        for item in checks
        if item["name"] not in {"route planner", "quick validator", "codex route pack required files"}
    ),
    "checks": checks,
}

if emit_json:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
else:
    print(f"design-craft doctor target: {target}")
    for item in checks:
        status = "found" if item["ok"] else "missing"
        print(f"- {item['name']}: {status} ({item['detail']})")
    print(f"overall_ok: {payload['ok']}")

sys.exit(0 if payload["ok"] else 1)
PY
