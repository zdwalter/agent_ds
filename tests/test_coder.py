"""Unit tests for coder server."""

import os
import sys
import tempfile
from pathlib import Path

# Add servers to path
sys.path.insert(0, str(Path(__file__).parent.parent / "servers"))

from coder.server import _analyze_python_file, investigate_and_save_report


def test_analyze_python_file():
    """Test parsing a Python file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write('''"""Module docstring."""
CONST = 42

def foo():
    """Foo function."""
    pass

class MyClass:
    def method(self):
        pass
''')
        f.flush()
        try:
            result = _analyze_python_file(Path(f.name))
            assert "Docstring:" in result
            assert "Constant: CONST" in result
            assert "Function: foo" in result
            assert "Class: MyClass (method)" in result
        finally:
            os.unlink(f.name)


def test_investigate_and_save_report(tmp_path):
    """Test folder investigation."""
    # Create a dummy folder with a Python file
    sub = tmp_path / "subdir"
    sub.mkdir()
    (sub / "test.py").write_text('print("hello")')
    (tmp_path / "README.md").write_text("# Project")

    result = investigate_and_save_report(str(tmp_path))
    # Expect a success message
    assert "complete" in result.lower() or "saved" in result.lower()
    # Check that report file exists
    report = tmp_path / ".test.Agent.md"
    assert report.exists()
    content = report.read_text()
    assert "Project Context Report" in content
