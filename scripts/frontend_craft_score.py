#!/usr/bin/env python3
"""Legacy compatibility wrapper for design_craft_score.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


target = Path(__file__).resolve().parents[1] / "scripts" / "design_craft_score.py"
result = subprocess.run([sys.executable, str(target), *sys.argv[1:]], check=False)
raise SystemExit(result.returncode)
