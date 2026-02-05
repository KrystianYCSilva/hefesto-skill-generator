---
description: "Official list of supported variables for Templates System"
version: "1.0.0"
---

# Official Variable List

This document defines the official variables supported by the Templates System. All templates MUST only use these variables.

## Core Variables

| Variable | Description | Required | Validation Rule |
|----------|-------------|----------|-----------------|
| `{{SKILL_NAME}}` | The unique identifier for the skill | Yes | `^[a-z0-9]+(-[a-z0-9]+)*$` (max 64 chars) |
| `{{SKILL_DESCRIPTION}}` | A clear description of what the skill does | Yes | Non-empty, max 1024 chars |
| `{{SKILL_BODY}}` | The main content/instructions of the skill | Yes | Valid Markdown content |
| `{{CREATED_DATE}}` | The creation date of the skill | No | ISO 8601 format (YYYY-MM-DD) |
| `{{VERSION}}` | The semantic version of the skill | No | SemVer format (e.g., 1.0.0) |
| `{{ARGUMENTS}}` | Placeholder for CLI arguments | No | Transformed by adapters |

## Usage

Variables are substituted during skill generation. Use the format `{{VARIABLE_NAME}}`.
To escape a variable (treat as literal text), use double braces: `{{{{VARIABLE_NAME}}}}`.

## Validation

- Unknown variables in templates cause a validation error.
- Variable values must meet the validation rules specified above.
