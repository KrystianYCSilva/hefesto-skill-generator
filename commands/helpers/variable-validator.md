---
description: "Logic for validating variables against official rules"
version: "1.0.0"
---

# Variable Validator

This helper validates variable values against the official rules defined in `variables.md`.

## Validation Logic

```python
import re
from datetime import datetime

def validate_variable(name, value):
    """
    Validates a single variable value.
    Returns (True, None) if valid, (False, error_message) if invalid.
    """
    if name == "SKILL_NAME":
        if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', value):
            return False, f"Invalid SKILL_NAME '{value}'. Must be lowercase, alphanumeric, with hyphens (max 64 chars). Example: 'code-review'"
        if len(value) > 64:
            return False, f"SKILL_NAME '{value}' exceeds 64 characters."
            
    elif name == "SKILL_DESCRIPTION":
        if not value or not value.strip():
            return False, "SKILL_DESCRIPTION cannot be empty."
        if len(value) > 1024:
            return False, "SKILL_DESCRIPTION exceeds 1024 characters."
            
    elif name == "CREATED_DATE":
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            return False, f"Invalid CREATED_DATE '{value}'. Must be ISO 8601 format (YYYY-MM-DD)."
            
    elif name == "VERSION":
        # Basic SemVer regex
        if not re.match(r'^\d+\.\d+\.\d+$', value):
             return False, f"Invalid VERSION '{value}'. Must be SemVer format (e.g., 1.0.0)."

    return True, None

def validate_all_variables(variables_map):
    """
    Validates a dictionary of variables.
    Returns list of errors (empty if all valid).
    """
    errors = []
    for name, value in variables_map.items():
        is_valid, error = validate_variable(name, value)
        if not is_valid:
            errors.append(error)
    return errors
```
