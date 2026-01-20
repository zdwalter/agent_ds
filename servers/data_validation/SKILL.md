---
name: data_validation
description: Data validation capabilities using Pydantic and JSON Schema.
allowed-tools:
  - validate_data
  - parse_model
  - validate_json_schema
---

# Data Validation Skill

This skill enables the agent to validate data structures using Pydantic models and JSON Schema.

## Tools

### validate_data
Validate a dictionary against a Pydantic schema.

Args:
- `data`: The data dictionary to validate.
- `schema`: A dictionary describing the schema, where keys are field names and values are type annotations as strings (e.g., "str", "int").

Returns:
Validation result message.

### parse_model
Create a Pydantic model dynamically and return its schema.

Args:
- `model_name`: Name of the model to create.
- `fields`: Dictionary mapping field names to type strings (e.g., "str").

Returns:
JSON schema of the created model.

### validate_json_schema
Validate data against a JSON Schema (draft-07). Requires jsonschema library.

Args:
- `json_schema`: JSON Schema as a string.
- `data`: Data dictionary to validate.

Returns:
Validation result.

## Dependencies
- pydantic (added to requirements.txt)
- jsonschema (optional, not installed by default)
