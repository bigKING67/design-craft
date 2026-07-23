from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from ..repo import REPO_ROOT
from .integrity import repository_head, repository_version


OBSERVATION_SCHEMA = "design-craft.github-run-observation.v1"
RUN_KEYS = {
    "id",
    "attempt",
    "workflow",
    "workflow_name",
    "event",
    "head_branch",
    "head_sha",
    "status",
    "conclusion",
    "url",
    "repository",
}
WORKFLOW_BINDING_KEYS = {
    "repository",
    "run_id",
    "run_attempt",
    "url",
    "event",
    "head_sha",
    "ref",
}


@dataclass(frozen=True)
class RunContract:
    kind: str
    workflow_path: str
    workflow_name: str
    event: str
    workflow_file: str

    def head_branch(self, version: str) -> str:
        return f"v{version}" if self.kind == "native" else "main"

    def ref(self, version: str) -> str:
        prefix = "tags" if self.kind == "native" else "heads"
        return f"refs/{prefix}/{self.head_branch(version)}"


RUN_CONTRACTS = {
    "native": RunContract(
        kind="native",
        workflow_path=".github/workflows/native-runtime.yml",
        workflow_name="Native runtime evidence",
        event="push",
        workflow_file="native-runtime.yml",
    ),
    "physical": RunContract(
        kind="physical",
        workflow_path=".github/workflows/physical-device.yml",
        workflow_name="Physical device evidence",
        event="workflow_dispatch",
        workflow_file="physical-device.yml",
    ),
}
NATIVE_WORKFLOW_PATH = RUN_CONTRACTS["native"].workflow_path
NATIVE_WORKFLOW_NAME = RUN_CONTRACTS["native"].workflow_name
PHYSICAL_WORKFLOW_PATH = RUN_CONTRACTS["physical"].workflow_path
PHYSICAL_WORKFLOW_NAME = RUN_CONTRACTS["physical"].workflow_name


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


def _json_output(result: subprocess.CompletedProcess[str], label: str) -> object:
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"cannot query {label}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid JSON from {label}: {exc}") from exc


def repository_name(explicit: str | None = None) -> str:
    if explicit:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", explicit):
            raise ValueError("GitHub repository must be owner/name")
        return explicit
    if not shutil.which("gh"):
        raise RuntimeError("gh CLI is required to inspect GitHub workflow runs")
    result = _run(
        ["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"]
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError(result.stderr.strip() or "cannot resolve GitHub repository")
    return repository_name(result.stdout.strip())


def _expected_run_values(expected_run: dict[str, object]) -> dict[str, object]:
    return {
        "id": expected_run.get("databaseId", expected_run.get("id")),
        "attempt": expected_run.get("attempt"),
        "workflow_name": expected_run.get(
            "workflowName", expected_run.get("workflow_name")
        ),
        "event": expected_run.get("event"),
        "head_branch": expected_run.get(
            "headBranch", expected_run.get("head_branch")
        ),
        "head_sha": expected_run.get("headSha", expected_run.get("head_sha")),
        "status": expected_run.get("status"),
        "conclusion": expected_run.get("conclusion"),
        "url": expected_run.get("url"),
    }


def validate_run(
    observed: dict[str, object],
    *,
    kind: str,
    expected_run: dict[str, object] | None = None,
    version: str | None = None,
    head: str | None = None,
) -> list[str]:
    contract = RUN_CONTRACTS[kind]
    errors: list[str] = []
    expected_version = version or repository_version()
    expected_head = head or repository_head()
    label = f"{kind} GitHub run"
    if set(observed) != RUN_KEYS:
        errors.append(
            f"{label} fields mismatch expected={sorted(RUN_KEYS)} "
            f"actual={sorted(observed)}"
        )
    run_id = observed.get("id")
    if not isinstance(run_id, int) or isinstance(run_id, bool) or run_id <= 0:
        errors.append(f"{label} id must be a positive integer")
    attempt = observed.get("attempt")
    if not isinstance(attempt, int) or isinstance(attempt, bool) or attempt <= 0:
        errors.append(f"{label} attempt must be a positive integer")
    if observed.get("workflow") != contract.workflow_path:
        errors.append(f"{label} workflow must be {contract.workflow_path}")
    if observed.get("workflow_name") != contract.workflow_name:
        errors.append(f"{label} workflow_name must be {contract.workflow_name}")
    if observed.get("event") != contract.event:
        errors.append(f"{label} event must be {contract.event}")
    expected_branch = contract.head_branch(expected_version)
    if observed.get("head_branch") != expected_branch:
        errors.append(f"{label} head_branch must be {expected_branch}")
    if observed.get("head_sha") != expected_head:
        errors.append(f"{label} head_sha must match current HEAD")
    if observed.get("status") != "completed":
        errors.append(f"{label} status must be completed")
    if observed.get("conclusion") != "success":
        errors.append(f"{label} conclusion must be success")
    repository = observed.get("repository")
    if not isinstance(repository, str) or not re.fullmatch(
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository
    ):
        errors.append(f"{label} repository must be owner/name")
    expected_url = (
        f"https://github.com/{repository}/actions/runs/{run_id}"
        if isinstance(repository, str)
        and isinstance(run_id, int)
        and not isinstance(run_id, bool)
        else None
    )
    if observed.get("url") != expected_url:
        errors.append(f"{label} url must match repository and run id")
    if expected_run is not None:
        for key, expected_value in _expected_run_values(expected_run).items():
            if expected_value is not None and observed.get(key) != expected_value:
                errors.append(f"{label} {key} must match the selected workflow run")
    return errors


def latest_native_tag_run(repository: str) -> dict[str, object]:
    head = repository_head()
    tag = f"v{repository_version()}"
    result = _run(
        [
            "gh",
            "run",
            "list",
            "--repo",
            repository_name(repository),
            "--workflow",
            RUN_CONTRACTS["native"].workflow_file,
            "--commit",
            head,
            "--limit",
            "20",
            "--json",
            (
                "attempt,databaseId,status,conclusion,headSha,headBranch,url,event,"
                "createdAt,workflowName"
            ),
        ]
    )
    payload = _json_output(result, "native-runtime.yml runs")
    if not isinstance(payload, list):
        raise RuntimeError("native-runtime.yml run list must be an array")
    matching = [
        item
        for item in payload
        if isinstance(item, dict)
        and item.get("headSha") == head
        and item.get("headBranch") == tag
        and item.get("event") == "push"
    ]
    matching.sort(key=lambda item: str(item.get("createdAt", "")), reverse=True)
    if not matching:
        raise RuntimeError(f"native-runtime.yml has no tag-push run for {tag} at {head}")
    latest = matching[0]
    if latest.get("status") != "completed" or latest.get("conclusion") != "success":
        raise RuntimeError(
            "latest native-runtime.yml tag-push run is not completed/success: "
            + str(latest.get("url", "unknown run"))
        )
    return latest


def observe_run(
    kind: str,
    run_id: str | int,
    *,
    repository: str | None = None,
    require_latest: bool | None = None,
) -> dict[str, object]:
    contract = RUN_CONTRACTS[kind]
    raw_id = str(run_id)
    if not re.fullmatch(r"[1-9][0-9]*", raw_id):
        raise ValueError(f"{kind} GitHub run id must contain only decimal digits")
    repo = repository_name(repository)
    view = _json_output(
        _run(
            [
                "gh",
                "run",
                "view",
                raw_id,
                "--repo",
                repo,
                "--json",
                (
                    "attempt,conclusion,databaseId,event,headBranch,headSha,status,"
                    "url,workflowName"
                ),
            ]
        ),
        f"GitHub run {raw_id}",
    )
    api = _json_output(
        _run(["gh", "api", f"repos/{repo}/actions/runs/{raw_id}"]),
        f"GitHub run API {raw_id}",
    )
    if not isinstance(view, dict) or not isinstance(api, dict):
        raise RuntimeError("GitHub run observation must be an object")
    observed: dict[str, object] = {
        "id": view.get("databaseId"),
        "attempt": view.get("attempt"),
        "workflow": api.get("path"),
        "workflow_name": view.get("workflowName"),
        "event": view.get("event"),
        "head_branch": view.get("headBranch"),
        "head_sha": view.get("headSha"),
        "status": view.get("status"),
        "conclusion": view.get("conclusion"),
        "url": view.get("url"),
        "repository": repo,
    }
    errors = validate_run(observed, kind=kind)
    if api.get("id") != observed["id"]:
        errors.append("gh run view and Actions API disagree on run id")
    if api.get("run_attempt") != observed["attempt"]:
        errors.append("gh run view and Actions API disagree on run attempt")
    if api.get("html_url") != observed["url"]:
        errors.append("gh run view and Actions API disagree on run url")
    if api.get("name") not in {None, contract.workflow_name}:
        errors.append("gh run view and Actions API disagree on workflow name")
    for api_key, observed_key in (
        ("event", "event"),
        ("head_branch", "head_branch"),
        ("head_sha", "head_sha"),
        ("status", "status"),
        ("conclusion", "conclusion"),
    ):
        if api.get(api_key) != observed[observed_key]:
            errors.append(
                f"gh run view and Actions API disagree on {observed_key}"
            )
    api_repository = api.get("repository")
    if (
        not isinstance(api_repository, dict)
        or api_repository.get("full_name") != observed["repository"]
    ):
        errors.append("Actions API repository does not match the selected repository")
    latest_required = kind == "native" if require_latest is None else require_latest
    if latest_required:
        if kind != "native":
            raise ValueError("only native tag runs support latest-run enforcement")
        latest = latest_native_tag_run(repo)
        if latest.get("databaseId") != observed["id"]:
            errors.append("selected run is not the latest successful native tag-push run")
        errors.extend(validate_run(observed, kind=kind, expected_run=latest))
    if errors:
        raise RuntimeError("; ".join(errors))
    return observed


def observation_document(kind: str, run: dict[str, object]) -> dict[str, object]:
    errors = validate_run(run, kind=kind)
    if errors:
        raise ValueError("; ".join(errors))
    return {
        "schema": OBSERVATION_SCHEMA,
        "kind": kind,
        "source_commit": repository_head(),
        "run": run,
    }


def load_observation(path: Path, *, expected_kind: str) -> dict[str, object]:
    if path.is_symlink() or not path.is_file():
        raise FileNotFoundError(f"GitHub run observation is missing or unsafe: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    expected_keys = {"schema", "kind", "source_commit", "run"}
    if not isinstance(payload, dict) or set(payload) != expected_keys:
        raise ValueError("GitHub run observation document fields are invalid")
    if payload.get("schema") != OBSERVATION_SCHEMA:
        raise ValueError(f"GitHub run observation must use {OBSERVATION_SCHEMA}")
    if payload.get("kind") != expected_kind:
        raise ValueError(f"GitHub run observation kind must be {expected_kind}")
    if payload.get("source_commit") != repository_head():
        raise ValueError("GitHub run observation source_commit must match current HEAD")
    run = payload.get("run")
    if not isinstance(run, dict):
        raise ValueError("GitHub run observation run must be an object")
    errors = validate_run(run, kind=expected_kind)
    if errors:
        raise ValueError("; ".join(errors))
    return run


def workflow_binding(run: dict[str, object], *, kind: str) -> dict[str, object]:
    version = repository_version()
    contract = RUN_CONTRACTS[kind]
    return {
        "repository": run.get("repository"),
        "run_id": run.get("id"),
        "run_attempt": run.get("attempt"),
        "url": run.get("url"),
        "event": run.get("event"),
        "head_sha": run.get("head_sha"),
        "ref": contract.ref(version),
    }


def validate_workflow_binding(
    binding: object, run: dict[str, object], *, kind: str, label: str
) -> list[str]:
    if not isinstance(binding, dict):
        return [f"{label} workflow binding must be an object"]
    errors: list[str] = []
    if set(binding) != WORKFLOW_BINDING_KEYS:
        errors.append(
            f"{label} workflow fields mismatch expected={sorted(WORKFLOW_BINDING_KEYS)} "
            f"actual={sorted(binding)}"
        )
    expected = workflow_binding(run, kind=kind)
    for field, value in expected.items():
        if binding.get(field) != value:
            errors.append(f"{label} workflow {field} does not match selected {kind} run")
    return errors


__all__ = [
    "NATIVE_WORKFLOW_NAME",
    "NATIVE_WORKFLOW_PATH",
    "OBSERVATION_SCHEMA",
    "PHYSICAL_WORKFLOW_NAME",
    "PHYSICAL_WORKFLOW_PATH",
    "RUN_CONTRACTS",
    "RUN_KEYS",
    "latest_native_tag_run",
    "load_observation",
    "observation_document",
    "observe_run",
    "validate_run",
    "validate_workflow_binding",
    "workflow_binding",
]
