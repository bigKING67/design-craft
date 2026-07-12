#!/usr/bin/env python3
"""Check or apply design-craft GitHub branch/tag rulesets."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


SCHEMA = "design-craft.github-governance.v1"
MAIN_RULESET = "design-craft-main"
TAG_RULESET = "design-craft-release-tags"
ROOT = Path(__file__).resolve().parents[1]
ACTIONS_PERMISSIONS = {
    "enabled": True,
    "allowed_actions": "selected",
    "sha_pinning_required": True,
}
SELECTED_ACTIONS = {
    "github_owned_allowed": False,
    "verified_allowed": False,
    "patterns_allowed": [
        "actions/checkout@*",
        "actions/github-script@*",
        "actions/setup-java@*",
        "actions/setup-node@*",
        "actions/setup-python@*",
        "actions/upload-artifact@*",
        "android-actions/setup-android@*",
        "gradle/actions/setup-gradle@*",
        "reactivecircus/android-emulator-runner@*",
    ],
}


def required_checks() -> list[dict[str, str]]:
    checks = [
        {"context": f"{os_name} / Node {node} / Python {python}"}
        for os_name in ("ubuntu-latest", "macos-latest")
        for node in ("22", "24")
        for python in ("3.11", "3.12", "3.13")
    ]
    checks.extend(
        (
            {"context": "android-fixture-build"},
            {"context": "windows-portable"},
            {"context": "lint"},
            {"context": "contract-tests"},
        )
    )
    return checks


def desired_rulesets() -> dict[str, dict]:
    return {
        MAIN_RULESET: {
            "name": MAIN_RULESET,
            "target": "branch",
            "enforcement": "active",
            "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
            "rules": [
                {"type": "deletion"},
                {"type": "non_fast_forward"},
                {
                    "type": "required_status_checks",
                    "parameters": {
                        "strict_required_status_checks_policy": True,
                        "do_not_enforce_on_create": True,
                        "required_status_checks": required_checks(),
                    },
                },
            ],
            "bypass_actors": [],
        },
        TAG_RULESET: {
            "name": TAG_RULESET,
            "target": "tag",
            "enforcement": "active",
            "conditions": {"ref_name": {"include": ["refs/tags/v*"], "exclude": []}},
            "rules": [{"type": "deletion"}, {"type": "non_fast_forward"}],
            "bypass_actors": [],
        },
    }


def run(command: list[str], *, input_value: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        input=input_value,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


def repository() -> str:
    result = run(["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"])
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError(result.stderr.strip() or "cannot resolve GitHub repository")
    return result.stdout.strip()


def ruleset_detail(repo: str, ruleset_id: int) -> dict:
    result = run(["gh", "api", f"repos/{repo}/rulesets/{ruleset_id}"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"cannot read ruleset {ruleset_id}")
    return json.loads(result.stdout)


def api_object(repo: str, suffix: str) -> dict:
    result = run(["gh", "api", f"repos/{repo}/{suffix}"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"cannot read {suffix}")
    payload = json.loads(result.stdout)
    if not isinstance(payload, dict):
        raise RuntimeError(f"GitHub {suffix} response must be an object")
    return payload


def validate_actions_permissions(
    permissions: dict,
    selected: dict,
) -> list[str]:
    errors: list[str] = []
    for key, expected in ACTIONS_PERMISSIONS.items():
        if permissions.get(key) != expected:
            errors.append(f"actions permissions {key} must be {expected!r}")
    for key in ("github_owned_allowed", "verified_allowed"):
        if selected.get(key) is not SELECTED_ACTIONS[key]:
            errors.append(f"selected actions {key} must be false")
    observed_patterns = selected.get("patterns_allowed")
    if not isinstance(observed_patterns, list) or sorted(observed_patterns) != sorted(
        SELECTED_ACTIONS["patterns_allowed"]
    ):
        errors.append("selected action patterns do not match the reviewed workflow allowlist")
    return errors


def workflow_action_patterns() -> set[str]:
    patterns: set[str] = set()
    for workflow in sorted((ROOT / ".github/workflows").glob("*.yml")):
        for line in workflow.read_text(encoding="utf-8").splitlines():
            marker = "uses:"
            if marker not in line:
                continue
            action = line.split(marker, 1)[1].strip().split()[0]
            if action.startswith("./") or "@" not in action:
                continue
            repository = action.split("@", 1)[0]
            patterns.add(f"{repository}@*")
    return patterns


def normalize_rule_types(payload: dict) -> set[str]:
    return {
        str(item.get("type"))
        for item in payload.get("rules", [])
        if isinstance(item, dict)
    }


def validate_ruleset(observed: dict, expected: dict) -> list[str]:
    errors: list[str] = []
    name = expected["name"]
    for field in ("target", "enforcement"):
        if observed.get(field) != expected.get(field):
            errors.append(f"{name}: {field} must be {expected.get(field)}")
    if observed.get("conditions") != expected.get("conditions"):
        errors.append(f"{name}: ref-name conditions do not match policy")
    if observed.get("bypass_actors") != []:
        errors.append(f"{name}: bypass_actors must be empty")
    expected_types = normalize_rule_types(expected)
    observed_types = normalize_rule_types(observed)
    if not expected_types.issubset(observed_types):
        errors.append(f"{name}: missing rule types {sorted(expected_types - observed_types)}")
    if name == MAIN_RULESET:
        expected_contexts = {item["context"] for item in required_checks()}
        observed_contexts: set[str] = set()
        strict = False
        do_not_enforce_on_create = False
        for rule in observed.get("rules", []):
            if isinstance(rule, dict) and rule.get("type") == "required_status_checks":
                parameters = rule.get("parameters", {})
                strict = parameters.get("strict_required_status_checks_policy") is True
                do_not_enforce_on_create = (
                    parameters.get("do_not_enforce_on_create") is True
                )
                observed_contexts = {
                    item.get("context")
                    for item in parameters.get("required_status_checks", [])
                    if isinstance(item, dict)
                }
        if not strict:
            errors.append(f"{name}: required status checks must require an up-to-date branch")
        if not do_not_enforce_on_create:
            errors.append(
                f"{name}: required status checks must set do_not_enforce_on_create=true"
            )
        if observed_contexts != expected_contexts:
            errors.append(f"{name}: required status check contexts do not match Validate")
    return errors


def fetch_rulesets(repo: str) -> list[dict]:
    result = run(["gh", "api", f"repos/{repo}/rulesets"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "cannot list repository rulesets")
    payload = json.loads(result.stdout)
    if not isinstance(payload, list):
        raise RuntimeError("GitHub rulesets response must be an array")
    return payload


def inspect(repo: str) -> dict:
    expected = desired_rulesets()
    summaries = fetch_rulesets(repo)
    by_name = {item.get("name"): item for item in summaries if isinstance(item, dict)}
    observed: dict[str, dict | None] = {}
    errors: list[str] = []
    for name, contract in expected.items():
        summary = by_name.get(name)
        if not summary or not isinstance(summary.get("id"), int):
            observed[name] = None
            errors.append(f"missing GitHub ruleset: {name}")
            continue
        detail = ruleset_detail(repo, summary["id"])
        observed[name] = detail
        errors.extend(validate_ruleset(detail, contract))
    actions_permissions = api_object(repo, "actions/permissions")
    selected_actions = (
        api_object(repo, "actions/permissions/selected-actions")
        if actions_permissions.get("allowed_actions") == "selected"
        else {}
    )
    errors.extend(validate_actions_permissions(actions_permissions, selected_actions))
    return {
        "schema": SCHEMA,
        "repository": repo,
        "ok": not errors,
        "rulesets": observed,
        "actions_permissions": actions_permissions,
        "selected_actions": selected_actions,
        "errors": errors,
    }


def apply(repo: str) -> dict:
    expected = desired_rulesets()
    summaries = fetch_rulesets(repo)
    by_name = {item.get("name"): item for item in summaries if isinstance(item, dict)}
    for name, payload in expected.items():
        summary = by_name.get(name)
        if summary and isinstance(summary.get("id"), int):
            endpoint = f"repos/{repo}/rulesets/{summary['id']}"
            method = "PUT"
        else:
            endpoint = f"repos/{repo}/rulesets"
            method = "POST"
        result = run(
            ["gh", "api", "--method", method, endpoint, "--input", "-"],
            input_value=json.dumps(payload),
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or f"cannot apply ruleset {name}")
    for suffix, payload in (
        ("actions/permissions", ACTIONS_PERMISSIONS),
        ("actions/permissions/selected-actions", SELECTED_ACTIONS),
    ):
        result = run(
            ["gh", "api", "--method", "PUT", f"repos/{repo}/{suffix}", "--input", "-"],
            input_value=json.dumps(payload),
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or f"cannot apply {suffix}")
    return inspect(repo)


def run_self_check() -> None:
    rulesets = desired_rulesets()
    expected = rulesets[MAIN_RULESET]
    if len(required_checks()) != 16:
        raise RuntimeError(
            "governance contract must cover 12 matrix jobs plus Android, Windows, lint, and contract tests"
        )
    if validate_ruleset(expected, expected):
        raise RuntimeError("governance self-check rejected the desired ruleset")
    invalid = json.loads(json.dumps(expected))
    invalid["rules"] = [{"type": "deletion"}]
    if not validate_ruleset(invalid, expected):
        raise RuntimeError("governance self-check accepted missing status checks")
    invalid_bypass = json.loads(json.dumps(expected))
    invalid_bypass["bypass_actors"] = [
        {"actor_id": 1, "actor_type": "RepositoryRole", "bypass_mode": "always"}
    ]
    if not any("bypass_actors" in error for error in validate_ruleset(invalid_bypass, expected)):
        raise RuntimeError("governance self-check accepted a main-branch bypass actor")
    invalid_create = json.loads(json.dumps(expected))
    for rule in invalid_create["rules"]:
        if rule.get("type") == "required_status_checks":
            rule["parameters"]["do_not_enforce_on_create"] = False
    if not any(
        "do_not_enforce_on_create" in error
        for error in validate_ruleset(invalid_create, expected)
    ):
        raise RuntimeError("governance self-check accepted status checks on branch creation")
    tag_expected = rulesets[TAG_RULESET]
    invalid_tag = json.loads(json.dumps(tag_expected))
    invalid_tag["bypass_actors"] = [
        {"actor_id": 5, "actor_type": "Integration", "bypass_mode": "always"}
    ]
    if not any(
        "bypass_actors" in error
        for error in validate_ruleset(invalid_tag, tag_expected)
    ):
        raise RuntimeError("governance self-check accepted a release-tag bypass actor")
    if workflow_action_patterns() != set(SELECTED_ACTIONS["patterns_allowed"]):
        raise RuntimeError("selected action allowlist does not match workflow usage")
    if validate_actions_permissions(ACTIONS_PERMISSIONS, SELECTED_ACTIONS):
        raise RuntimeError("governance self-check rejected desired Actions permissions")
    invalid_permissions = dict(ACTIONS_PERMISSIONS, sha_pinning_required=False)
    if not any(
        "sha_pinning_required" in error
        for error in validate_actions_permissions(invalid_permissions, SELECTED_ACTIONS)
    ):
        raise RuntimeError("governance self-check accepted disabled SHA pinning")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm-external-write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.check:
        run_self_check()
        print("github_governance_self_check=ok")
        return 0
    if not shutil.which("gh"):
        print("gh is required", file=sys.stderr)
        return 2
    if args.apply and not args.confirm_external_write:
        parser.error("--apply requires --confirm-external-write")
    try:
        repo = repository()
        payload = apply(repo) if args.apply else inspect(repo)
    except (RuntimeError, json.JSONDecodeError) as exc:
        payload = {
            "schema": SCHEMA,
            "repository": None,
            "ok": False,
            "rulesets": {},
            "actions_permissions": None,
            "selected_actions": None,
            "errors": [str(exc)],
        }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    elif payload["ok"]:
        print("GitHub governance verified")
    else:
        print("\n".join(payload["errors"]), file=sys.stderr)
    return 0 if payload["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
