from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass(frozen=True)
class MaturityContext:
    root: Path
    profile: str
    phase: str
    baseline_path: Path | None


@dataclass(frozen=True)
class MaturityGateResult:
    gate_id: str
    status: str
    duration_ms: float
    evidence: Any
    error: str

    @property
    def passed(self) -> bool:
        return self.status == "passed"


GateRunner = Callable[[MaturityContext], MaturityGateResult]
