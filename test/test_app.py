import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from app import check_repository


class AppTests(unittest.TestCase):
    def test_healthy_repository_passes_all_checks(self):
        with tempfile.TemporaryDirectory() as folder:
            repository = Path(folder)
            (repository / "README.md").touch()
            (repository / "test").mkdir()
            (repository / "requirements.txt").touch()

            output = io.StringIO()
            with redirect_stdout(output):
                result = check_repository(repository)

            self.assertTrue(result)
            self.assertIn("Repository is healthy.", output.getvalue())

    def test_incomplete_repository_needs_attention(self):
        with tempfile.TemporaryDirectory() as folder:
            output = io.StringIO()
            with redirect_stdout(output):
                result = check_repository(Path(folder))

            report = output.getvalue()
            self.assertFalse(result)
            self.assertIn("[FAIL] README.md file", report)
            self.assertIn("[FAIL] test folder", report)
            self.assertIn("[FAIL] requirements.txt file", report)
            self.assertIn("Repository needs attention.", report)


if __name__ == "__main__":
    unittest.main()