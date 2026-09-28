"""A small, beginner-friendly repository health checker."""

from pathlib import Path
import ast
import subprocess
import sys


def check_readme(repository: Path) -> tuple[bool, str]:
    """Check whether the repository has a non-empty README file."""
    readme = repository / "README.md"

    if not readme.is_file():
        return False, "README.md is missing"
    if not readme.read_text(encoding="utf-8").strip():
        return False, "README.md is empty"
    return True, "README.md is present"


def check_python_files(repository: Path) -> tuple[bool, str]:
    """Check Python files for syntax errors."""
    python_files = sorted(repository.rglob("*.py"))
    errors = []

    for python_file in python_files:
        try:
            ast.parse(python_file.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError) as error:
            errors.append(f"{python_file.relative_to(repository)}: {error}")

    if errors:
        return False, "Python syntax errors found: " + "; ".join(errors)
    return True, f"Python files look good ({len(python_files)} checked)"


def check_git_status(repository: Path) -> tuple[bool, str]:
    """Check whether Git can inspect the repository and report its state."""
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=repository,
            capture_output=True,
            text=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False, "Git repository could not be inspected"

    if result.stdout.strip():
        return True, "Git has uncommitted changes"
    return True, "Git working tree is clean"


def run_health_check(repository: Path) -> int:
    """Run all checks and return a process exit code."""
    checks = [
        ("README", check_readme(repository)),
        ("Python syntax", check_python_files(repository)),
        ("Git status", check_git_status(repository)),
    ]

    print(f"Repository health check: {repository.resolve()}")
    print("-" * 50)

    all_checks_passed = True
    for name, (passed, message) in checks:
        label = "PASS" if passed else "FAIL"
        print(f"[{label}] {name}: {message}")
        all_checks_passed = all_checks_passed and passed

    print("-" * 50)
    print("Overall: healthy" if all_checks_passed else "Overall: needs attention")
    return 0 if all_checks_passed else 1


def main() -> None:
    """Read the optional repository path and start the check."""
    repository = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()

    if not repository.is_dir():
        print(f"Error: '{repository}' is not a directory.")
        raise SystemExit(1)

    raise SystemExit(run_health_check(repository))


if __name__ == "__main__":
    main()