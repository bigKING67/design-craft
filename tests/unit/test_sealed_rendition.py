from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from tools.design_craft.repo import REPO_ROOT


LIB_DIR = REPO_ROOT / "skills/design-craft/lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

import design_craft.sealed_rendition as gate_module
from design_craft.comp_fidelity import PngImage, write_png
from design_craft.sealed_rendition import (
    REPORT_SCHEMA,
    SPEC_SCHEMA,
    SealedRenditionError,
    closeout_gate,
    prepare_gate,
    validate_gate_report,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class GateFixture:
    def __init__(self, root: Path, *, dimensions: tuple[int, int] = (4, 4)) -> None:
        self.root = root
        self.sealed = root / "密封 source with spaces"
        self.sealed.mkdir()
        self.source = self.sealed / "report page.html"
        self.reference = self.sealed / "reference image.png"
        self.manifest = self.sealed / "RENDER.json"
        self.comparison_spec = root / "comparison spec.json"
        self.gate_spec = root / "gate spec.json"
        self.output = root / "repo external evidence"
        self.width, self.height = dimensions
        self.source.write_bytes(b"<!doctype html>\r\n<title>money</title>\x1a")
        pixels = bytearray()
        for y in range(self.height):
            for x in range(self.width):
                value = 32 if x == 1 else 224
                pixels.extend((value, value, value, 255))
        self.reference_image = PngImage(self.width, self.height, bytes(pixels))
        write_png(self.reference, self.reference_image)
        self.write_manifest()
        self.write_comparison_spec(dimensions=["content", "geometry"])
        self.write_gate_spec()

    def write_manifest(self) -> None:
        files = [
            {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in (self.source, self.reference)
        ]
        self.manifest.write_text(
            json.dumps({"schema": "fixture.sealed-rendition.v1", "files": files}),
            encoding="utf-8",
        )

    def write_comparison_spec(self, *, dimensions: list[str]) -> None:
        self.comparison_spec.write_text(
            json.dumps(
                {
                    "schema": "design-craft.comp-fidelity-spec.v1",
                    "case_id": "sealed-fixture",
                    "coordinate_space": {"width": self.width, "height": self.height},
                    "changed_pixel_delta": 0.02,
                    "regions": [
                        {
                            "id": "canvas",
                            "box": [0, 0, self.width, self.height],
                            "salience": "primary",
                            "dimensions": dimensions,
                            "note": "fixture canvas",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )

    def capture(self, capture_id: str = "desktop") -> dict[str, object]:
        return {
            "id": capture_id,
            "kind": "browser_viewport",
            "source": self.source.name,
            "reference": self.reference.name,
            "comparison_spec": str(self.comparison_spec),
            "contract": {
                "runtime": "browser67",
                "viewport": {"width": self.width, "height": self.height},
                "device_scale_factor": 1,
                "theme": "light",
                "network": "offline",
                "wait_for": "document_complete",
            },
        }

    def write_gate_spec(self, captures: list[dict[str, object]] | None = None) -> None:
        self.gate_spec.write_text(
            json.dumps(
                {
                    "schema": SPEC_SCHEMA,
                    "gate_id": "sealed-fixture",
                    "authority": {
                        "kind": "sealed_manifest",
                        "root": str(self.sealed),
                        "manifest": str(self.manifest),
                        "expected_schema": "fixture.sealed-rendition.v1",
                        "inventory_key": "files",
                        "anchors": [],
                    },
                    "captures": captures or [self.capture()],
                }
            ),
            encoding="utf-8",
        )

    def prepare(self) -> dict[str, object]:
        return prepare_gate(
            spec_path=self.gate_spec,
            output_root=self.output,
            prepared_at="2026-08-29T00:00:00Z",
        )

    def rendered_path(self, plan: dict[str, object], index: int = 0) -> Path:
        captures = plan["captures"]
        assert isinstance(captures, list)
        return Path(captures[index]["rendered_path"])

    def closeout(
        self,
        *,
        decision: str = "pending",
        reviewer: str | None = None,
        note: str = "Fixture remains pending human visual review.",
    ) -> dict[str, object]:
        return closeout_gate(
            plan_path=self.output / "capture-plan.json",
            visual_decision=decision,
            visual_note=note,
            reviewer=reviewer,
            observed_at="2026-08-29T00:00:01Z",
        )


class SealedRenditionGateTests(unittest.TestCase):
    def test_exact_positive_path_and_strict_validation(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            fixture = GateFixture(Path(raw))
            plan = fixture.prepare()
            shutil.copyfile(fixture.reference, fixture.rendered_path(plan))

            report = fixture.closeout(
                decision="pass",
                reviewer="fixture-reviewer",
                note="Exact fixture inspected at its planned coordinate space.",
            )
            validation = validate_gate_report(
                fixture.output / "gate-report.json", strict=True
            )

            self.assertEqual(report["schema"], REPORT_SCHEMA)
            self.assertEqual(report["verdict"], "pass")
            self.assertEqual(
                set(report["comparisons"][0]["strict_validation"]),
                {"schema", "ok", "artifact_count", "strict"},
            )
            self.assertNotIn(
                ".closeout-",
                json.dumps(report["comparisons"][0]["strict_validation"]),
            )
            self.assertEqual(
                report["statuses"],
                {
                    "input_integrity": "pass",
                    "capture_integrity": "pass",
                    "comparison_integrity": "pass",
                    "source_mutation_audit": "pass",
                    "visual_decision": "pass",
                },
            )
            self.assertTrue(validation["ok"])
            self.assertIsNone(validation["global_pixel_pass_threshold"])

    def test_input_mismatch_fails_before_capture_plan_exists(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            fixture = GateFixture(Path(raw))
            fixture.source.write_bytes(b"changed after sealing")

            with self.assertRaisesRegex(SealedRenditionError, "size mismatch|hash mismatch"):
                fixture.prepare()

            self.assertFalse(fixture.output.exists())

    def test_ordered_capture_contract_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            fixture = GateFixture(Path(raw))
            fixture.write_gate_spec([fixture.capture("mobile"), fixture.capture("desktop")])

            plan = fixture.prepare()

            self.assertEqual(plan["capture_order"], ["mobile", "desktop"])
            self.assertEqual(
                [capture["ordinal"] for capture in plan["captures"]], [1, 2]
            )

    def test_content_drift_is_measured_but_not_auto_failed_or_passed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            fixture = GateFixture(Path(raw))
            fixture.write_comparison_spec(dimensions=["content"])
            plan = fixture.prepare()
            changed = bytearray(fixture.reference_image.rgba)
            changed[0:4] = bytes((0, 0, 0, 255))
            write_png(
                fixture.rendered_path(plan),
                PngImage(fixture.width, fixture.height, bytes(changed)),
            )

            report = fixture.closeout()

            self.assertEqual(report["verdict"], "pending")
            self.assertGreater(
                report["comparisons"][0]["overall_metrics"]["changed_pixel_ratio"],
                0,
            )
            self.assertIsNone(report["decision_boundary"]["global_pixel_pass_threshold"])

    def test_geometry_drift_is_localized_without_a_global_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            fixture = GateFixture(Path(raw))
            fixture.write_comparison_spec(dimensions=["geometry"])
            plan = fixture.prepare()
            shifted = bytearray()
            for _y in range(fixture.height):
                for x in range(fixture.width):
                    value = 32 if x == 2 else 224
                    shifted.extend((value, value, value, 255))
            write_png(
                fixture.rendered_path(plan),
                PngImage(fixture.width, fixture.height, bytes(shifted)),
            )

            report = fixture.closeout()

            self.assertEqual(report["statuses"]["comparison_integrity"], "pass")
            self.assertEqual(report["statuses"]["visual_decision"], "pending")
            self.assertGreater(
                report["comparisons"][0]["regions"][0]["metrics"]["changed_pixel_ratio"],
                0,
            )

    def test_benign_raster_variance_stays_pending(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            fixture = GateFixture(Path(raw))
            plan = fixture.prepare()
            changed = bytearray(fixture.reference_image.rgba)
            changed[0] = min(255, changed[0] + 1)
            write_png(
                fixture.rendered_path(plan),
                PngImage(fixture.width, fixture.height, bytes(changed)),
            )

            report = fixture.closeout()

            self.assertEqual(report["verdict"], "pending")
            self.assertEqual(
                report["comparisons"][0]["overall_metrics"]["changed_pixel_ratio"],
                0,
            )

    def test_strict_validation_rejects_comp_artifact_tamper(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            fixture = GateFixture(Path(raw))
            plan = fixture.prepare()
            shutil.copyfile(fixture.reference, fixture.rendered_path(plan))
            report = fixture.closeout()
            comparison_report_path = fixture.output / report["comparisons"][0]["report"]["path"]
            comparison = json.loads(comparison_report_path.read_text(encoding="utf-8"))
            heatmap = comparison_report_path.parent / comparison["artifacts"]["heatmap"]["path"]
            write_png(
                heatmap,
                PngImage(fixture.width, fixture.height, bytes((0, 0, 0, 255)) * 16),
            )

            with self.assertRaisesRegex(SealedRenditionError, "hash or size mismatch"):
                validate_gate_report(fixture.output / "gate-report.json", strict=True)

    def test_source_mutation_audit_fails_before_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            fixture = GateFixture(Path(raw))
            plan = fixture.prepare()
            shutil.copyfile(fixture.reference, fixture.rendered_path(plan))
            fixture.source.write_bytes(b"mutated after capture preflight")

            with self.assertRaisesRegex(SealedRenditionError, "size mismatch|hash mismatch"):
                fixture.closeout()

            self.assertFalse((fixture.output / "comparisons").exists())
            self.assertFalse((fixture.output / "gate-report.json").exists())

    def test_output_must_be_disjoint_from_sealed_authority(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            fixture = GateFixture(Path(raw))

            with self.assertRaisesRegex(SealedRenditionError, "disjoint"):
                prepare_gate(
                    spec_path=fixture.gate_spec,
                    output_root=fixture.sealed / "evidence",
                )

    @unittest.skipIf(os.name == "nt", "Windows symlink creation may require elevation")
    def test_rendered_path_must_not_escape_through_a_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            fixture = GateFixture(Path(raw))
            plan = fixture.prepare()
            capture_dir = fixture.rendered_path(plan).parent
            capture_dir.rmdir()
            escaped = fixture.root / "escaped capture"
            escaped.mkdir()
            shutil.copyfile(fixture.reference, escaped / "rendered.png")
            capture_dir.symlink_to(escaped, target_is_directory=True)

            with self.assertRaisesRegex(SealedRenditionError, "traverse a symlink"):
                fixture.closeout()

    def test_unicode_spaces_and_binary_snapshot_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            fixture = GateFixture(Path(raw))

            plan = fixture.prepare()

            source_record = plan["captures"][0]["source"]
            self.assertEqual(source_record["sha256"], sha256(fixture.source))
            self.assertIn("密封 source with spaces", source_record["path"])
            self.assertEqual(
                gate_module.BINARY_READ_FLAGS & getattr(os, "O_BINARY", 0),
                getattr(os, "O_BINARY", 0),
            )

    def test_git_commit_authority_delegates_to_shadow_lab_verifier(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            fixture = GateFixture(root)
            shadow_manifest = root / ".design-craft-shadow-lab.json"
            shadow_manifest.write_text('{"schema":"fixture"}', encoding="utf-8")
            source_repo = root / "source-repo"
            source_repo.mkdir()
            fixture.write_gate_spec()
            payload = json.loads(fixture.gate_spec.read_text(encoding="utf-8"))
            payload["authority"] = {
                "kind": "git_commit",
                "shadow_lab_manifest": str(shadow_manifest),
            }
            payload["captures"][0]["source"] = fixture.source.name
            payload["captures"][0]["reference"] = fixture.reference.name
            fixture.gate_spec.write_text(json.dumps(payload), encoding="utf-8")
            calls: list[Path] = []

            def verify(path: Path) -> dict[str, object]:
                calls.append(path)
                return {
                    "ok": True,
                    "source": {
                        "source_unchanged": True,
                        "repo_path": str(source_repo),
                        "commit": "1" * 40,
                    },
                    "boundary": {
                        "source_writes_allowed": False,
                        "source_and_output_disjoint": True,
                    },
                    "lab": {"worktree": str(fixture.sealed)},
                }

            plan = prepare_gate(
                spec_path=fixture.gate_spec,
                output_root=fixture.output,
                shadow_lab_verifier=verify,
            )
            shutil.copyfile(fixture.reference, fixture.rendered_path(plan))
            report = closeout_gate(
                plan_path=fixture.output / "capture-plan.json",
                visual_decision="pending",
                visual_note="Git authority fixture remains pending.",
                shadow_lab_verifier=verify,
            )

            self.assertEqual(report["authority"]["preflight"]["kind"], "git_commit")
            self.assertGreaterEqual(len(calls), 3)

    def test_pass_visual_decision_requires_named_reviewer(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            fixture = GateFixture(Path(raw))
            plan = fixture.prepare()
            shutil.copyfile(fixture.reference, fixture.rendered_path(plan))

            with self.assertRaisesRegex(SealedRenditionError, "require a reviewer"):
                fixture.closeout(decision="pass")


if __name__ == "__main__":
    unittest.main()
