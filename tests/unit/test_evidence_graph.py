from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.design_craft.evaluation.evidence_graph import (
    binding_domain,
    domain_fingerprint,
    git_domain_fingerprint,
    git_projected_skill_tree_sha256,
    graph_errors,
    project_skill_domain,
    projected_skill_tree_sha256,
    repository_graph_errors,
)
from tools.design_craft.repo import REPO_ROOT
from scripts.design_craft_evidence_common import tree_sha256
from scripts.design_craft_evidence_common import git_head


class EvidenceGraphTests(unittest.TestCase):
    def test_repository_graph_is_complete(self) -> None:
        self.assertEqual(repository_graph_errors(), [])

    def test_version_metadata_does_not_change_behavior_fingerprint(self) -> None:
        domain = binding_domain("cross_agent", "same-prompt-motion-review")
        before = domain_fingerprint(REPO_ROOT, domain)
        version_path = REPO_ROOT / "skills/design-craft/VERSION"
        original = version_path.read_bytes()
        try:
            version_path.write_bytes(b"999.999.999\n")
            self.assertEqual(domain_fingerprint(REPO_ROOT, domain), before)
        finally:
            version_path.write_bytes(original)

    def test_motion_reference_only_changes_motion_domain(self) -> None:
        motion = binding_domain("comparative", "emil-motion-ablation")
        visual = binding_domain("comparative", "taste-visual-critique-ablation")
        motion_before = domain_fingerprint(REPO_ROOT, motion)
        visual_before = domain_fingerprint(REPO_ROOT, visual)
        path = REPO_ROOT / "skills/design-craft/references/motion-quality.md"
        original = path.read_bytes()
        try:
            path.write_bytes(original + b"\n<!-- domain fixture -->\n")
            self.assertNotEqual(domain_fingerprint(REPO_ROOT, motion), motion_before)
            self.assertEqual(domain_fingerprint(REPO_ROOT, visual), visual_before)
        finally:
            path.write_bytes(original)

    def test_visual_reference_does_not_change_motion_domain(self) -> None:
        motion = binding_domain("comparative", "emil-motion-ablation")
        visual = binding_domain("comparative", "taste-visual-critique-ablation")
        motion_before = domain_fingerprint(REPO_ROOT, motion)
        visual_before = domain_fingerprint(REPO_ROOT, visual)
        path = REPO_ROOT / "skills/design-craft/references/visual-judgment.md"
        original = path.read_bytes()
        try:
            path.write_bytes(original + b"\n<!-- domain fixture -->\n")
            self.assertEqual(domain_fingerprint(REPO_ROOT, motion), motion_before)
            self.assertNotEqual(domain_fingerprint(REPO_ROOT, visual), visual_before)
        finally:
            path.write_bytes(original)

    def test_projection_contains_only_domain_files(self) -> None:
        domain = binding_domain("cross_agent", "same-prompt-motion-review")
        with tempfile.TemporaryDirectory() as raw:
            destination = Path(raw) / "design-craft"
            project_skill_domain(
                REPO_ROOT,
                REPO_ROOT / "skills/design-craft",
                domain,
                destination,
            )
            self.assertTrue((destination / "SKILL.md").is_file())
            self.assertTrue((destination / "references/motion-quality.md").is_file())
            self.assertFalse((destination / "VERSION").exists())
            self.assertFalse((destination / "references/visual-judgment.md").exists())
            self.assertEqual(
                projected_skill_tree_sha256(
                    REPO_ROOT, REPO_ROOT / "skills/design-craft", domain
                ),
                tree_sha256(destination),
            )

    def test_git_fingerprint_matches_clean_checkout(self) -> None:
        domain = binding_domain("cross_agent", "same-prompt-motion-review")
        commit = git_head(REPO_ROOT)
        self.assertEqual(
            git_domain_fingerprint(REPO_ROOT, domain, commit),
            domain_fingerprint(REPO_ROOT, domain),
        )
        self.assertEqual(
            git_projected_skill_tree_sha256(
                REPO_ROOT,
                REPO_ROOT / "skills/design-craft",
                domain,
                commit,
            ),
            projected_skill_tree_sha256(
                REPO_ROOT, REPO_ROOT / "skills/design-craft", domain
            ),
        )

    def test_graph_rejects_cycles(self) -> None:
        payload = {
            "schema": "design-craft.evidence-graph.v2",
            "domains": {
                "one": {"extends": ["two"], "include": []},
                "two": {"extends": ["one"], "include": []},
            },
            "bindings": {
                "cross_agent": {"task": "one"},
                "comparative": {"case": "one"},
                "operational": {"release": "two"},
            },
        }
        self.assertTrue(any("cycle" in error for error in graph_errors(payload)))


if __name__ == "__main__":
    unittest.main()
