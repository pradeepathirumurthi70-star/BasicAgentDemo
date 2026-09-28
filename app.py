from pathlib import Path
import sys


def check_repository(repository):
    """Check for the basic files and folder in a repository."""
    checks = {
        "README.md file": (repository / "README.md").is_file(),
        "test folder": (repository / "test").is_dir(),
        "requirements.txt file": (repository / "requirements.txt").is_file(),
    }

    print("Repository Health Report")
    print("-" * 25)

    all_checks_passed = True
    for name, passed in checks.items():
        result = "PASS" if passed else "FAIL"
        print(f"[{result}] {name}")
        all_checks_passed = all_checks_passed and passed

    print("-" * 25)
    if all_checks_passed:
        print("Repository is healthy.")
    else:
        print("Repository needs attention.")

    return all_checks_passed


def main():
    """Check the current repository or a path provided by the user."""
    repository_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    check_repository(repository_path)


if __name__ == "__main__":
    main()