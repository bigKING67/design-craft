#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

upstreams=(
  "taste-skill"
  "impeccable"
  "emilkowalski-skills"
)

before_lines=()
for name in "${upstreams[@]}"; do
  before_lines+=("${name}:$(git -C "upstreams/${name}" rev-parse HEAD 2>/dev/null || true)")
done

git submodule update --init --remote \
  upstreams/taste-skill \
  upstreams/impeccable \
  upstreams/emilkowalski-skills

python3 - <<'PY'
import json
import subprocess
from pathlib import Path

upstreams = {
    "taste-skill": {
        "repo": "https://github.com/Leonxlnx/taste-skill.git",
        "path": "upstreams/taste-skill",
        "license": "MIT",
    },
    "impeccable": {
        "repo": "https://github.com/pbakaus/impeccable.git",
        "path": "upstreams/impeccable",
        "license": "Apache-2.0",
    },
    "emilkowalski-skills": {
        "repo": "https://github.com/emilkowalski/skills.git",
        "path": "upstreams/emilkowalski-skills",
        "license": "MIT",
    },
}

for meta in upstreams.values():
    meta["commit"] = subprocess.check_output(
        ["git", "-C", meta["path"], "rev-parse", "HEAD"],
        text=True,
    ).strip()

Path("upstreams.lock.json").write_text(
    json.dumps({"upstreams": upstreams}, indent=2) + "\n",
    encoding="utf-8",
)
PY

for line in "${before_lines[@]}"; do
  name="${line%%:*}"
  before="${line#*:}"
  after="$(git -C "upstreams/${name}" rev-parse HEAD)"
  echo "${name}: ${before:-none} -> ${after}"
done
echo "Updated upstreams.lock.json. Review upstream changes before changing skills/design-craft."
