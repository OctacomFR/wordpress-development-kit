"""Exercise comparison generation and refusal cases with real ImageMagick images."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from compare_visuals import compare_visuals, inspect_png, sha256


class VisualComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.magick = shutil.which("magick")
        if cls.magick is None:
            raise RuntimeError("ImageMagick est requis pour ces tests réels")

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="octacom-visual-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.figma = self.root / "figma reference.png"
        self.front = self.root / "front capture.png"
        self.output = self.root / "comparison"
        self.make_image(self.figma)
        self.make_image(self.front)

    def make_image(self, path: Path, *, size: str = "64x48", rectangle: str = "8,8 24,24") -> None:
        subprocess.run(
            [self.magick, "-size", size, "xc:white", "-fill", "#254b75",
             "-draw", f"rectangle {rectangle}", str(path)],
            capture_output=True, text=True, check=True,
        )

    def test_identical_inputs_produce_native_size_evidence_without_certification(self) -> None:
        hashes = sha256(self.figma), sha256(self.front)
        result = compare_visuals(self.figma, self.front, self.output)
        self.assertEqual(result["rmse"]["normalized"], 0)
        self.assertEqual(inspect_png(self.magick, self.output / "side-by-side.png"), (128, 48))
        self.assertEqual(inspect_png(self.magick, self.output / "overlay.png"), (64, 48))
        self.assertEqual(inspect_png(self.magick, self.output / "difference.png"), (64, 48))
        self.assertEqual((sha256(self.figma), sha256(self.front)), hashes)
        self.assertEqual(result["inputs"]["figma"]["sha256"], hashes[0])
        self.assertTrue(result["visual_review_required"])
        self.assertEqual(json.loads((self.output / "comparison.json").read_text(encoding="utf-8")), result)

    def test_one_pixel_shift_is_reported_without_a_passing_threshold(self) -> None:
        self.make_image(self.front, rectangle="9,8 25,24")
        result = compare_visuals(self.figma, self.front, self.output)
        self.assertGreater(result["rmse"]["normalized"], 0)
        self.assertTrue(result["visual_review_required"])
        self.assertNotIn("pass", result)
        self.assertNotIn("threshold", result)

    def test_different_dimensions_are_refused_without_outputs(self) -> None:
        self.make_image(self.front, size="64x49")
        with self.assertRaisesRegex(ValueError, "Dimensions différentes"):
            compare_visuals(self.figma, self.front, self.output)
        self.assertFalse(self.output.exists())

    def test_previous_evidence_is_preserved(self) -> None:
        compare_visuals(self.figma, self.front, self.output)
        evidence_hash = sha256(self.output / "comparison.json")
        with self.assertRaisesRegex(ValueError, "dossier de sortie doit être nouveau"):
            compare_visuals(self.figma, self.front, self.output)
        self.assertEqual(sha256(self.output / "comparison.json"), evidence_hash)

    def test_missing_capture_is_refused_without_outputs(self) -> None:
        with self.assertRaisesRegex(ValueError, "Capture PNG absente"):
            compare_visuals(self.figma, self.root / "missing.png", self.output)
        self.assertFalse(self.output.exists())

    def test_same_input_path_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "captures distinctes"):
            compare_visuals(self.figma, self.figma, self.output)
        self.assertFalse(self.output.exists())

    def test_missing_imagemagick_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "magick introuvable"):
            compare_visuals(self.figma, self.front, self.output, magick="octacom-missing-magick")
        self.assertFalse(self.output.exists())

    def test_provenance_is_preserved_without_a_visual_verdict(self) -> None:
        provenance = {"mission_digest": "m1", "resource": "post:42", "observed_revision": "r1", "epoch": 3,
            "figma_reference": "home", "figma_version": "f1", "state": "rest-1440", "front_url": "https://fixture.invalid/",
            "viewport": {"width": 1440, "height": 900, "dpr": 1, "zoom": 100}}
        result = compare_visuals(self.figma, self.front, self.output, provenance=provenance)
        self.assertEqual(result["provenance"], provenance)
        self.assertTrue(result["visual_review_required"])

    def test_incomplete_provenance_is_refused_before_generation(self) -> None:
        with self.assertRaisesRegex(ValueError, "Provenance complète"):
            compare_visuals(self.figma, self.front, self.output, provenance={"mission_digest": "m1"})
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
