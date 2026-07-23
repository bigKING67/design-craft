from __future__ import annotations

import json
from argparse import Namespace
from pathlib import Path

from .contract import compare_results
from .runner import run_suite


def run_benchmark(args: Namespace) -> int:
    current = run_suite(args.scale)
    if args.output:
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    payload: dict[str, object] = current
    if args.baseline:
        baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
        payload = compare_results(baseline, current)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        if args.baseline:
            print(f"benchmark regression: {'pass' if payload['ok'] else 'fail'}")
            for error in payload.get("errors", []):
                print(f"- {error}")
        else:
            print(f"benchmark suite completed: {len(current['metrics'])} metrics")
    return 0 if payload.get("ok", True) else 1
