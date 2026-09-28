# Repository Health Check

## Project purpose

This beginner-friendly Python application checks whether a repository contains three common project files:

- `README.md`
- `test/`
- `requirements.txt`

It prints a short health report showing which checks pass and whether the repository is healthy.

## Setup

The application uses only Python's standard library. No third-party packages are required.

1. Install Python 3.
2. Clone or download this repository.
3. Open a terminal in the project folder.

The `requirements.txt` file is included for standard project structure, but it does not need any packages installed.

## Usage

Check the current folder:

```bash
python3 app.py
```

Check another repository by providing its path:

```bash
python3 app.py /path/to/repository
```

## Run the tests

Run all tests with Python's built-in test runner:

```bash
python3 -m unittest discover -v
```