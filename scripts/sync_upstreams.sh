#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

before_taste="$(git -C upstreams/taste-skill rev-parse HEAD 2>/dev/null || true)"
before_impeccable="$(git -C upstreams/impeccable rev-parse HEAD 2>/dev/null || true)"

git submodule update --init --remote upstreams/taste-skill upstreams/impeccable

after_taste="$(git -C upstreams/taste-skill rev-parse HEAD)"
after_impeccable="$(git -C upstreams/impeccable rev-parse HEAD)"

python3 - "${after_taste}" "${after_impeccable}" <<'PY'
import json
import sys
from pathlib import Path

taste, impeccable = sys.argv[1], sys.argv[2]
payload = {
    "upstreams": {
        "taste-skill": {
            "repo": "https://github.com/Leonxlnx/taste-skill.git",
            "path": "upstreams/taste-skill",
            "license": "MIT",
            "commit": taste,
        },
        "impeccable": {
            "repo": "https://github.com/pbakaus/impeccable.git",
            "path": "upstreams/impeccable",
            "license": "Apache-2.0",
            "commit": impeccable,
        },
    }
}
Path("upstreams.lock.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
PY

echo "taste-skill: ${before_taste:-none} -> ${after_taste}"
echo "impeccable: ${before_impeccable:-none} -> ${after_impeccable}"
echo "Updated upstreams.lock.json. Review upstream changes before changing skills/frontend-craft."
