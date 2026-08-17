#!/usr/bin/env python3
"""Run isolated unittest cases concurrently with deterministic reporting."""

from __future__ import annotations

import argparse
import concurrent.futures
import subprocess
import sys
import unittest
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class TestResult:
    test_id: str
    returncode: int
    stdout: str
    stderr: str


def iter_test_ids(suite: unittest.TestSuite) -> list[str]:
    test_ids: list[str] = []
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            test_ids.extend(iter_test_ids(test))
        else:
            test_ids.append(test.id())
    return test_ids


def collect_test_ids(targets: list[str]) -> list[str]:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    loader = unittest.defaultTestLoader
    test_ids: list[str] = []
    for target in targets:
        test_ids.extend(iter_test_ids(loader.loadTestsFromName(target)))
    return sorted(set(test_ids))


def run_test(test_id: str) -> TestResult:
    result = subprocess.run(
        [sys.executable, "-m", "unittest", test_id],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    return TestResult(test_id, result.returncode, result.stdout, result.stderr)


def run_tests(test_ids: list[str], jobs: int) -> list[TestResult]:
    workers = min(max(1, jobs), len(test_ids))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(run_test, test_ids))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="+", help="unittest module, class, or method")
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be at least 1")

    test_ids = collect_test_ids(args.targets)
    if not test_ids:
        print("no tests found", file=sys.stderr)
        return 2

    results = run_tests(test_ids, args.jobs)
    failures = [result for result in results if result.returncode != 0]
    if failures:
        for result in failures:
            print(f"FAILED: {result.test_id}", file=sys.stderr)
            detail = result.stderr.strip() or result.stdout.strip() or "test failed"
            print(detail, file=sys.stderr)
        return 1

    print(
        f"parallel unittest verified: tests={len(results)}, "
        f"jobs={min(args.jobs, len(results))}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
