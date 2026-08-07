import tokenize
from pathlib import Path

import pytest

# Adjust path relative to your project root if necessary
COMPONENTS_DIR = Path(__file__).parent.parent / "components"


def get_file_comments(file_path: Path) -> list[tuple[int, str]]:
    """Scan a python file and return a list of (line_number, comment_text)."""
    comments = []
    with open(file_path, "rb") as f:
        try:
            tokens = tokenize.tokenize(f.readline)
            for token in tokens:
                if token.type == tokenize.COMMENT:
                    line_num = token.start[0]
                    comments.append((line_num, token.string.strip()))
        except tokenize.TokenError:
            pass  # Handles unclosed strings/multi-line syntax edge cases safely
    return comments


def test_no_comments_in_components():
    assert COMPONENTS_DIR.exists(), f"Target directory not found: {COMPONENTS_DIR}"

    # Recursively find all .py files, ignoring __pycache__ directories
    py_files = [
        path for path in COMPONENTS_DIR.rglob("*.py") if "__pycache__" not in path.parts
    ]

    violations = []
    for py_file in py_files:
        comments = get_file_comments(py_file)
        for line_num, comment_text in comments:
            # Format cleanly: relative_path:line -> comment
            relative_path = py_file.relative_to(COMPONENTS_DIR.parent)
            violations.append(f"{relative_path}:{line_num} -> {comment_text}")

    if violations:
        error_msg = (
            f"\nFound {len(violations)} comment(s) in './components/':\n\n"
            + "\n".join(violations)
        )
        pytest.fail(error_msg, pytrace=False)
