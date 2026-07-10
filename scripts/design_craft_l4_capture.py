#!/usr/bin/env python3
"""Compatibility wrapper for the portable design-craft runtime."""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "design-craft" / "scripts" / "design_craft_l4_capture.py"
os.environ.setdefault("DESIGN_CRAFT_SOURCE_ROOT", str(ROOT))
if not SCRIPT.is_file():
    raise SystemExit(f"portable runtime is missing: {SCRIPT}")
os.execv(sys.executable, [sys.executable, str(SCRIPT), *sys.argv[1:]])
