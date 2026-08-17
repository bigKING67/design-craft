from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.design_craft.repo import REPO_ROOT


SCRIPT = REPO_ROOT / "skills/design-craft/scripts/design_craft_shadow_lab.py"


def command(cwd: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    environment = dict(os.environ)
    environment.update(
        {
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_TERMINAL_PROMPT": "0",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    return subprocess.run(
        list(arguments),
        cwd=cwd,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )


def git(repo: Path, *arguments: str) -> bytes:
    completed = command(repo, "git", "-c", "core.fsmonitor=false", *arguments)
    if completed.returncode != 0:
        raise AssertionError(completed.stderr.decode(errors="replace"))
    return completed.stdout


def run_cli(cwd: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    return command(cwd, sys.executable, str(SCRIPT), *arguments)


class ShadowLabCliTests(unittest.TestCase):
    def test_prepare_verify_and_confirmed_cleanup_preserve_dirty_source(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            parent = Path(raw)
            repo = parent / "source"
            repo.mkdir()
            git(repo, "init", "--quiet")
            git(repo, "config", "user.name", "Design Craft Tests")
            git(repo, "config", "user.email", "design-craft-tests@example.invalid")
            (repo / "screen.tsx").write_text("export const state = 'base';\n")
            git(repo, "add", "screen.tsx")
            git(repo, "commit", "--quiet", "-m", "fixture")
            (repo / "screen.tsx").write_text("export const state = 'user-wip';\n")
            (repo / "untracked-user-file.txt").write_text("private wip\n")
            baseline_status = git(
                repo,
                "status",
                "--porcelain=v1",
                "-z",
                "--untracked-files=all",
            )
            baseline_diff = git(repo, "diff", "--no-ext-diff", "--binary", "HEAD", "--")

            prepared = run_cli(
                REPO_ROOT,
                "prepare",
                "--source",
                str(repo),
                "--ref",
                "HEAD",
                "--output-root",
                str(parent / "labs"),
            )
            self.assertEqual(prepared.returncode, 0, prepared.stderr.decode())
            payload = json.loads(prepared.stdout)
            manifest_path = Path(payload["manifest"]["isolation"]["manifest_path"])
            worktree = Path(payload["manifest"]["isolation"]["worktree"])
            self.assertEqual(
                (worktree / "screen.tsx").read_text(),
                "export const state = 'base';\n",
            )
            self.assertFalse((worktree / "untracked-user-file.txt").exists())

            refused = run_cli(
                REPO_ROOT, "cleanup", "--manifest", str(manifest_path)
            )
            self.assertEqual(refused.returncode, 2)
            self.assertTrue(manifest_path.is_file())

            verified = run_cli(REPO_ROOT, "verify", "--manifest", str(manifest_path))
            self.assertEqual(verified.returncode, 0, verified.stderr.decode())
            self.assertTrue(json.loads(verified.stdout)["source"]["source_unchanged"])

            cleaned = run_cli(
                REPO_ROOT,
                "cleanup",
                "--manifest",
                str(manifest_path),
                "--confirm",
            )
            self.assertEqual(cleaned.returncode, 0, cleaned.stderr.decode())
            self.assertFalse(manifest_path.parent.exists())
            self.assertEqual(
                baseline_status,
                git(
                    repo,
                    "status",
                    "--porcelain=v1",
                    "-z",
                    "--untracked-files=all",
                ),
            )
            self.assertEqual(
                baseline_diff,
                git(repo, "diff", "--no-ext-diff", "--binary", "HEAD", "--"),
            )

    def test_cli_rejects_non_empty_unowned_output_root(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            parent = Path(raw)
            repo = parent / "source"
            repo.mkdir()
            git(repo, "init", "--quiet")
            git(repo, "config", "user.name", "Design Craft Tests")
            git(repo, "config", "user.email", "design-craft-tests@example.invalid")
            (repo / "app.txt").write_text("fixture\n")
            git(repo, "add", "app.txt")
            git(repo, "commit", "--quiet", "-m", "fixture")
            output_root = parent / "labs"
            output_root.mkdir(mode=0o700)
            (output_root / "not-owned.txt").write_text("leave me alone\n")

            completed = run_cli(
                REPO_ROOT,
                "prepare",
                "--source",
                str(repo),
                "--output-root",
                str(output_root),
            )

            self.assertEqual(completed.returncode, 2)
            self.assertIn("non-empty", json.loads(completed.stdout)["error"])
            self.assertEqual((output_root / "not-owned.txt").read_text(), "leave me alone\n")

    def test_cli_fails_closed_on_a_malformed_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            manifest = Path(raw) / ".design-craft-shadow-lab.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema": "design-craft.shadow-lab-manifest.v1",
                        "source": [],
                        "isolation": {},
                    }
                )
            )

            completed = run_cli(
                REPO_ROOT, "verify", "--manifest", str(manifest)
            )

            self.assertEqual(completed.returncode, 2)
            payload = json.loads(completed.stdout)
            self.assertIn("source must be an object", payload["error"])
            self.assertNotIn("Traceback", completed.stderr.decode())


if __name__ == "__main__":
    unittest.main()
