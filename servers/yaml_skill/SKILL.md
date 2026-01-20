---
name: yaml_skill
description: YAML file reading and writing capabilities.
allowed-tools:
  - read_yaml
  - write_yaml
  - validate_yaml
---

# YAML Skill

This skill enables the agent to read and write YAML files, as well as validate YAML strings.

## Tools

### read_yaml
Read a YAML file and return its parsed contents as a Python dictionary.
- `file_path`: Absolute path to the YAML file.

### write_yaml
Write a Python dictionary to a YAML file.
- `data`: The dictionary to serialize.
- `file_path`: Absolute path where the YAML file will be written.

### validate_yaml
Validate a YAML string for correctness.
- `yaml_string`: The YAML string to validate.
- Returns a boolean indicating validity.
