#!/usr/bin/env python3
"""Compatibility wrapper for the portable design-craft platform scanner."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "skills/design-craft/scripts/design_craft_platform_scan.py"

if not SCRIPT.is_file():
    raise SystemExit(f"portable platform scanner is missing: {SCRIPT}")

result = subprocess.run([sys.executable, str(SCRIPT), *sys.argv[1:]], check=False)
raise SystemExit(result.returncode)
