---
description: "Logic for variable substitution in templates"
version: "1.0.0"
---

# Variable Substitution

This helper handles the substitution of variables in templates, including escape sequences.

## Features

*   **Standard Substitution**: Replaces `{{VAR}}` with the value.
*   **Escape Mechanism**: Replaces `{{{{VAR}}}}` with `{{VAR}}` (literal).
*   **Safety**: Only substitutes known variables.

## Logic

```python
def substitute_variables(content, variables):
    """
    Substitutes variables in the content.
    
    1. Handle Escapes: {{{{VAR}}}} -> __LITERAL_VAR__
    2. Substitute: {{VAR}} -> value
    3. Restore Escapes: __LITERAL_VAR__ -> {{VAR}}
    """
    
    # 1. Protect escaped variables
    # We use a temporary placeholder that is unlikely to exist in text
    protected_content = content.replace("{{{{", "__OPEN_BRACE__").replace("}}}}", "__CLOSE_BRACE__")
    
    # 2. Substitute real variables
    for name, value in variables.items():
        placeholder = f"{{{{{name}}}}}"
        if placeholder in protected_content:
            protected_content = protected_content.replace(placeholder, str(value))
            
    # 3. Restore escaped variables to literal {{VAR}}
    final_content = protected_content.replace("__OPEN_BRACE__", "{{").replace("__CLOSE_BRACE__", "}}")
    
    # Metadata substitution (US4)
    # If we have a metadata dict, we could handle it here or in a separate function
    # For now, we assume flattened variables for simplicity
    
    return final_content
```
