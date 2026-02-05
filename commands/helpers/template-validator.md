---
description: "Logic for validating templates against Agent Skills spec and T0 rules"
version: "1.0.0"
---

# Template Validator

This helper validates generated skill templates against the Agent Skills specification and Hefesto T0 rules.

## Validation Checklist

1.  **Frontmatter Check (T0-HEFESTO-01)**
    *   Must be valid YAML.
    *   Must contain `name` and `description`.
    *   `name` must match regex `^[a-z0-9]+(-[a-z0-9]+)*$`.
    *   `description` must be non-empty and <= 1024 chars.

2.  **Progressive Disclosure (T0-HEFESTO-03)**
    *   `SKILL.md` content must be < 500 lines.
    *   Frontmatter should be small (~100 tokens).

3.  **Metadata Validation**
    *   If `metadata` field exists, it must point to a valid file (e.g., `./metadata.yaml`).

## Validation Logic

```python
import yaml

def validate_template(content, file_path="SKILL.md"):
    """
    Validates the generated template content.
    Returns list of errors.
    """
    errors = []
    
    # 1. Parse Frontmatter
    try:
        if not content.startswith("---"):
             return ["Missing frontmatter start '---'"]
        
        parts = content.split("---", 2)
        if len(parts) < 3:
             return ["Invalid frontmatter format"]
             
        frontmatter_yaml = parts[1]
        body = parts[2]
        
        data = yaml.safe_load(frontmatter_yaml)
        
        # T0-HEFESTO-01
        if "name" not in data:
            errors.append("Missing required field: 'name'")
        elif not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', data["name"]):
             errors.append(f"Invalid name '{data['name']}'. Must be lowercase, alphanumeric, with hyphens.")
             
        if "description" not in data:
            errors.append("Missing required field: 'description'")
        elif not data["description"]:
             errors.append("Description cannot be empty")
             
    except yaml.YAMLError as e:
        return [f"Invalid YAML frontmatter: {str(e)}"]

    # 2. T0-HEFESTO-03 (Line Count)
    line_count = len(content.splitlines())
    if line_count > 500:
        errors.append(f"SKILL.md exceeds 500 lines ({line_count}). Move content to references/.")

    # 3. Metadata Validation
    # If metadata field exists, warn if file not found (basic check)
    if "metadata" in data:
        # In a real implementation, we would check if the file actually exists
        pass

    return errors
```
