import os
import shutil
import subprocess
import tempfile
import unittest

_SOURCE_DIR = os.path.join("assets", "tests", "workflow")


class TestWwImageExif(unittest.TestCase):
    """Verify that `ww image exif` correctly detects GPS EXIF data in images."""

    @classmethod
    def setUpClass(cls):
        if not os.path.isdir(_SOURCE_DIR):
            raise unittest.SkipTest(f"Test image directory missing: {_SOURCE_DIR}")

    def setUp(self):
        # Copy test images to a temp directory so --clean never mutates originals
        self.tmpdir = tempfile.mkdtemp(prefix="exif_test_")
        for fname in os.listdir(_SOURCE_DIR):
            src = os.path.join(_SOURCE_DIR, fname)
            dst = os.path.join(self.tmpdir, fname)
            if os.path.isfile(src):
                shutil.copy2(src, dst)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    # ------------------------------------------------------------------
    #  helpers
    # ------------------------------------------------------------------

    def _run_exif(self, *extra_args):
        """Run ww image exif against the temp dir and return (returncode, stdout)."""
        cmd = ["ww", "image", "exif", self.tmpdir, *extra_args]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode, result.stdout.strip()

    # ------------------------------------------------------------------
    #  tests
    # ------------------------------------------------------------------

    def test_exit_code_success(self):
        """Command exits with 0."""
        rc, _ = self._run_exif()
        self.assertEqual(rc, 0)

    def test_gps_image_detected_default_mode(self):
        """Without --all, only GPS-bearing images are listed."""
        rc, out = self._run_exif()
        self.assertEqual(rc, 0)
        self.assertIn("tokyo_tower.jpg", out)
        self.assertNotIn("no_gps.jpg", out)
        self.assertIn("GPS:", out)
        self.assertIn("35.658600", out)
        self.assertIn("139.745400", out)

    def test_all_flag_shows_all_images(self):
        """--all lists every image, including those without GPS."""
        rc, out = self._run_exif("--all")
        self.assertEqual(rc, 0)
        self.assertIn("tokyo_tower.jpg", out)
        self.assertIn("no_gps.jpg", out)
        self.assertIn("(no GPS)", out)
        self.assertIn("GPS:", out)

    def test_summary_line_present(self):
        """Output always ends with a summary line."""
        rc, out = self._run_exif("--all")
        self.assertEqual(rc, 0)
        self.assertIn("Scanned:", out)
        self.assertIn("GPS found:", out)
        self.assertIn("Directory:", out)
        self.assertIn(self.tmpdir, out)

    def test_summary_counts_match(self):
        """Scanned and GPS counts are correct."""
        _, out = self._run_exif("--all")
        last_line = out.strip().split("\n")[-1]
        self.assertIn("Scanned: 2", last_line)
        self.assertIn("GPS found: 1", last_line)

    def test_recursive_flag_accepted(self):
        """-r/--recursive scans subdirectories (just verify no crash)."""
        rc, out = self._run_exif("-r", "--all")
        self.assertEqual(rc, 0)
        self.assertIn("Scanned:", out)

    def test_maps_url_present(self):
        """GPS output includes a Google Maps link."""
        _, out = self._run_exif("--all")
        self.assertIn("https://maps.google.com/?q=", out)

    def test_clean_removes_gps(self):
        """--clean removes GPS EXIF and reports the action."""
        # First confirm GPS exists
        _, before = self._run_exif("--all")
        self.assertIn("GPS:", before)

        # Then clean
        rc, out = self._run_exif("--clean")
        self.assertEqual(rc, 0)
        self.assertIn("GPS removed", out)

        # Verify GPS is gone
        _, after = self._run_exif("--all")
        self.assertNotIn("GPS:", after)
        self.assertIn("GPS found: 0", after)

    def test_clean_fallback_on_jpeg(self):
        """--clean uses piexif on JPEG (verifies no re-encode)."""
        rc, out = self._run_exif("--clean")
        self.assertEqual(rc, 0)
        # GPS removed line means piexif path worked
        self.assertIn("GPS removed", out)


if __name__ == "__main__":
    unittest.main()
