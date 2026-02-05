---
description: "Logic for Human Gate blocking before persistence"
version: "1.0.0"
---

# Human Gate

This helper implements the T0-HEFESTO-02 rule: "NUNCA persistir sem Human Gate aprovado".

## Workflow

1.  **Generate**: The skill is generated in memory.
2.  **Validate**: The system runs `template-validator.md`.
    *   If invalid: Show errors and **BLOCK**.
3.  **Preview**: Show the generated content (or a summary) to the user.
4.  **Prompt**: Ask for explicit confirmation.
    *   `[approve]`: Proceed to write to disk.
    *   `[reject]`: Discard.
    *   `[edit]`: Allow modification (advanced).

## Interface

```text
✅ Skill Generated: {{SKILL_NAME}}

Preview:
-----------------------------------------
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}}
...
-----------------------------------------

Validation: PASS ✅

Actions:
[approve] - Save to disk
[reject]  - Discard
```

## Logic

```python
def human_gate(skill_content, validation_errors):
    if validation_errors:
        print("❌ Validation Failed:")
        for err in validation_errors:
            print(f"  - {err}")
        print("Persistence BLOCKED.")
        return False

    print_preview(skill_content)
    
    response = input("Action [approve/reject]: ").strip().lower()
    
    if response == "approve":
        return True
    else:
        print("Operation cancelled by user.")
        return False
```
