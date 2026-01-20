import json
from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ValidationError, create_model

mcp = FastMCP("data_validation", log_level="ERROR")


@mcp.tool()
def validate_data(data: Dict[str, Any], schema: Dict[str, Any]) -> str:
    """
    Validate a dictionary against a Pydantic schema.

    Args:
        data: The data dictionary to validate.
        schema: A dictionary describing the schema, where keys are field names
                and values are type annotations as strings (e.g., "str", "int").

    Returns:
        Validation result message.
    """
    try:
        # Convert string type annotations to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "list": list,
            "dict": dict,
        }
        fields = {}
        for field_name, type_str in schema.items():
            if isinstance(type_str, str):
                if type_str in type_mapping:
                    fields[field_name] = (type_mapping[type_str], ...)
                else:
                    # Assume it's a string literal, treat as str
                    fields[field_name] = (str, ...)
            else:
                # Assume it's already a type (e.g., from JSON)
                fields[field_name] = (type_str, ...)

        DynamicModel = create_model("DynamicModel", **fields)
        validated = DynamicModel(**data)
        return f"Validation successful: {validated.model_dump()}"
    except ValidationError as e:
        errors = e.errors()
        return f"Validation failed with {len(errors)} error(s):\n{json.dumps(errors, indent=2)}"
    except Exception as e:
        return f"Error during validation: {str(e)}"


@mcp.tool()
def parse_model(model_name: str, fields: Dict[str, str]) -> str:
    """
    Create a Pydantic model dynamically and return its schema.

    Args:
        model_name: Name of the model to create.
        fields: Dictionary mapping field names to type strings (e.g., "str").

    Returns:
        JSON schema of the created model.
    """
    try:
        type_mapping = {
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "list": list,
            "dict": dict,
        }
        model_fields = {}
        for field_name, type_str in fields.items():
            if type_str in type_mapping:
                model_fields[field_name] = (type_mapping[type_str], ...)
            else:
                model_fields[field_name] = (str, ...)

        DynamicModel = create_model(model_name, **model_fields)
        schema = DynamicModel.model_json_schema()
        return f"Model '{model_name}' created. Schema:\n{json.dumps(schema, indent=2)}"
    except Exception as e:
        return f"Error creating model: {str(e)}"


@mcp.tool()
def validate_json_schema(json_schema: str, data: Dict[str, Any]) -> str:
    """
    Validate data against a JSON Schema (draft-07).

    Args:
        json_schema: JSON Schema as a string.
        data: Data dictionary to validate.

    Returns:
        Validation result.
    """
    try:
        import jsonschema

        schema = json.loads(json_schema)
        jsonschema.validate(instance=data, schema=schema)
        return "Validation against JSON Schema succeeded."
    except ImportError:
        return "Error: jsonschema library not installed. Please add 'jsonschema' to requirements.txt."
    except json.JSONDecodeError as e:
        return f"Invalid JSON schema: {str(e)}"
    except jsonschema.ValidationError as e:
        return f"Validation failed: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"
