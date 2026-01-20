import json
import os
import tempfile
from pathlib import Path

from servers.yaml_skill.server import read_yaml, validate_yaml, write_yaml


def test_read_yaml():
    """Test reading a YAML file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_path = Path(tmpdir) / "test.yaml"
        yaml_path.write_text("""
name: John
age: 30
hobbies:
  - reading
  - hiking
""")
        result = read_yaml(str(yaml_path))
        # result is a JSON string
        data = json.loads(result)
        assert data["name"] == "John"
        assert data["age"] == 30
        assert "reading" in data["hobbies"]


def test_write_yaml():
    """Test writing a YAML file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_path = Path(tmpdir) / "out.yaml"
        data = {"foo": "bar", "nested": {"key": 42}}
        result = write_yaml(json.dumps(data), str(yaml_path))
        assert "Successfully" in result
        assert yaml_path.exists()
        # read it back
        with open(yaml_path, "r") as f:
            import yaml

            loaded = yaml.safe_load(f)
        assert loaded["foo"] == "bar"
        assert loaded["nested"]["key"] == 42


def test_validate_yaml():
    """Test validating YAML strings."""
    # valid YAML
    result = validate_yaml("key: value")
    assert "valid" in result.lower()
    # invalid YAML
    result = validate_yaml("key: [unclosed")
    assert "invalid" in result.lower()
