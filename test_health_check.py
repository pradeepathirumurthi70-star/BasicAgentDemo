import tempfile
import unittest
from pathlib import Path

from health_check import check_python_files, check_readme


class HealthCheckTests(unittest.TestCase):
    def test_readme_check_passes_for_non_empty_readme(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = Path(folder)
            (repository / "README.md").write_text("# Example", encoding="utf-8")

            passed, message = check_readme(repository)

            self.assertTrue(passed)
            self.assertIn("present", message)

    def test_readme_check_fails_when_readme_is_missing(self):
        with tempfile.TemporaryDirectory() as folder:
            passed, message = check_readme(Path(folder))

            self.assertFalse(passed)
            self.assertIn("missing", message)

    def test_python_check_fails_for_invalid_python(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = Path(folder)
            (repository / "broken.py").write_text("def broken(:\n", encoding="utf-8")

            passed, message = check_python_files(repository)

            self.assertFalse(passed)
            self.assertIn("syntax errors", message)


if __name__ == "__main__":
    unittest.main()