from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.design_craft.repo import REPO_ROOT


class InstallerIntegrationTests(unittest.TestCase):
    def _run_installer(
        self,
        install_root: Path,
        backup_root: Path,
        *args: str,
        extra_env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment.update(
            {
                "DESIGN_CRAFT_SKILL_ROOT": str(install_root),
                "DESIGN_CRAFT_BACKUP_ROOT": str(backup_root),
                "PYTHONDONTWRITEBYTECODE": "1",
            }
        )
        if extra_env:
            environment.update(extra_env)
        return subprocess.run(
            ["bash", str(REPO_ROOT / "scripts/install_local.sh"), *args],
            cwd=REPO_ROOT,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

    def _snapshot(self, root: Path) -> list[tuple[str, str, bytes]]:
        if not root.exists():
            return []
        snapshot: list[tuple[str, str, bytes]] = []
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                snapshot.append((relative, "symlink", os.readlink(path).encode()))
            elif path.is_dir():
                snapshot.append((relative, "directory", b""))
            else:
                snapshot.append((relative, "file", path.read_bytes()))
        return snapshot

    def test_install_writes_verified_canonical_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            install_root = root / "skills"
            backup_root = root / "backups"

            result = self._run_installer(install_root, backup_root)

            self.assertEqual(result.returncode, 0, result.stderr)
            installed = install_root / "design-craft"
            self.assertTrue((installed / "SKILL.md").is_file())
            metadata = json.loads(
                (installed / ".design-craft-install.json").read_text(encoding="utf-8")
            )
            self.assertEqual(metadata["schema"], "design-craft.install.v2")
            self.assertEqual(metadata["skill_name"], "design-craft")
            self.assertEqual(metadata["version"], (REPO_ROOT / "VERSION").read_text().strip())
            self.assertTrue(metadata["source_tree_sha256"])

    def test_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            before = self._snapshot(root)

            result = self._run_installer(root / "skills", root / "backups", "--dry-run")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("dry_run: no files changed", result.stdout)
            self.assertEqual(self._snapshot(root), before)

    def test_backup_failpoint_restores_previous_target(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            install_root = root / "skills"
            target = install_root / "design-craft"
            target.mkdir(parents=True)
            (target / "user-file.txt").write_text("preserve\n", encoding="utf-8")

            result = self._run_installer(
                install_root,
                root / "backups",
                extra_env={"DESIGN_CRAFT_INSTALL_TEST_FAIL_AFTER_BACKUP": "1"},
            )

            self.assertEqual(result.returncode, 97)
            self.assertEqual((target / "user-file.txt").read_text(), "preserve\n")
            self.assertFalse((target / "SKILL.md").exists())

    def test_post_switch_failpoint_restores_previous_target(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            install_root = root / "skills"
            target = install_root / "design-craft"
            target.mkdir(parents=True)
            (target / "user-file.txt").write_text("preserve\n", encoding="utf-8")

            result = self._run_installer(
                install_root,
                root / "backups",
                extra_env={"DESIGN_CRAFT_INSTALL_TEST_FAIL_AFTER_SWITCH": "1"},
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((target / "user-file.txt").read_text(), "preserve\n")
            self.assertFalse((target / "SKILL.md").exists())

    def test_live_and_stale_install_locks(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            install_root = root / "skills"
            backup_root = root / "backups"
            lock = install_root / ".design-craft-install.lock"
            lock.mkdir(parents=True)
            (lock / "pid").write_text(f"{os.getpid()}\n", encoding="utf-8")

            blocked = self._run_installer(
                install_root, backup_root, "--lock-timeout", "0"
            )
            self.assertNotEqual(blocked.returncode, 0)
            self.assertIn("Timed out waiting for install lock", blocked.stderr)
            self.assertFalse((install_root / "design-craft").exists())

            shutil.rmtree(lock)
            lock.mkdir()
            (lock / "pid").write_text("999999999\n", encoding="utf-8")
            recovered = self._run_installer(install_root, backup_root)
            self.assertEqual(recovered.returncode, 0, recovered.stderr)
            self.assertTrue((install_root / "design-craft/SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
