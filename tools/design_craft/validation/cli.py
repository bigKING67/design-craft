from __future__ import annotations

import json
from argparse import Namespace
from dataclasses import asdict

from .registry import load_registry, select_gates
from .runner import run_gates


OUTPUT_SCHEMA = "design-craft.validation-run.v1"


def run_validate(args: Namespace) -> int:
    gates = select_gates(load_registry(), args.profile)
    if args.list:
        payload = {
            "schema": OUTPUT_SCHEMA,
            "profile": args.profile,
            "status": "listed",
            "gates": [gate.gate_id for gate in gates],
        }
        if args.json:
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            for gate in gates:
                print(gate.gate_id)
        return 0

    results = run_gates(gates, jobs=args.jobs)
    passed = all(result.passed for result in results)
    payload = {
        "schema": OUTPUT_SCHEMA,
        "profile": args.profile,
        "status": "passed" if passed else "failed",
        "gate_count": len(results),
        "duration_ms": round(sum(result.duration_ms for result in results), 3),
        "results": [asdict(result) for result in results],
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for result in results:
            marker = "+" if result.passed else "-"
            print(f"{marker} {result.gate_id}: {result.status} ({result.duration_ms:.3f} ms)")
            if not result.passed and result.stderr_summary:
                print(result.stderr_summary)
        print(f"validation {payload['status']}: {len(results)} gates")
    return 0 if passed else 1
