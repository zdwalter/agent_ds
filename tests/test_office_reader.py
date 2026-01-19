"""Unit tests for office_reader server."""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add servers to path
sys.path.insert(0, str(Path(__file__).parent.parent / "servers"))

from office_reader.server import list_supported_formats, read_office_file


def test_list_supported_formats():
    """Test listing supported formats."""
    result = list_supported_formats()
    # Should return a string with supported formats
    assert "pdf" in result.lower()
    assert "docx" in result.lower()


def test_read_office_file_success():
    """Test reading an office file successfully."""
    # Mock markitdown
    mock_markitdown = Mock()
    mock_markitdown.convert.return_value.text_content = "# Mocked content"
    with patch("office_reader.server.MarkItDown", return_value=mock_markitdown), patch(
        "office_reader.server.os.path.exists", return_value=True
    ), patch("office_reader.server.os.path.isfile", return_value=True):
        result = read_office_file("/fake/path/document.docx")
        assert "Mocked content" in result
        # Ensure convert was called with correct path
        mock_markitdown.convert.assert_called_once_with("/fake/path/document.docx")


def test_read_office_file_error():
    """Test reading a non-existent file."""
    # Mock markitdown to raise an exception
    mock_markitdown = Mock()
    mock_markitdown.convert.side_effect = Exception("File not found")
    with patch("office_reader.server.MarkItDown", return_value=mock_markitdown):
        # Note: os.path.exists will return False for non-existent file,
        # so we don't need to mock it; the error will be "File not found at ..."
        result = read_office_file("/fake/path/nonexistent.docx")
        assert "Error" in result
        assert "File not found" in result or "not found at" in result


def test_read_office_file_unsupported_format():
    """Test reading an unsupported format."""
    # Mock markitdown to raise an exception about unsupported format
    mock_markitdown = Mock()
    mock_markitdown.convert.side_effect = Exception("Unsupported file type")
    with patch("office_reader.server.MarkItDown", return_value=mock_markitdown), patch(
        "office_reader.server.os.path.exists", return_value=True
    ), patch("office_reader.server.os.path.isfile", return_value=True):
        result = read_office_file("/fake/path/file.xyz")
        assert "Error" in result
        assert "Unsupported file type" in result
