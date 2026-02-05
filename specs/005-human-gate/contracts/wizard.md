# Contract: Wizard Module

**Module**: `commands/lib/wizard.py`  
**Purpose**: Step-by-step wizard for skill creation (FR-008 to FR-014)  
**Phase**: 1 (Design)

---

## Public API

### `run_wizard(command: str) -> PreviewObject | None`

**Description**: Execute wizard flow for `/hefesto.create` or `/hefesto.extract`

**Parameters**:
- `command`: str - 'create' or 'extract'

**Returns**: 
- `PreviewObject` if wizard completes successfully
- `None` if user cancels or timeout occurs

**Raises**:
- `WizardTimeoutError`: If wizard times out (saves state to `.hefesto/temp/`)

**Behavior**:
1. Initialize Wizard State (FR-010)
2. Execute steps 1-4 in order:
   - Step 1: Collect skill name (FR-013 auto-sanitizes)
   - Step 2: Collect description
   - Step 3: Collect main instructions
   - Step 4: Collect optional JIT resources
3. Support 'back' command at any step (FR-012)
4. Validate each input before proceeding (FR-011)
5. Display final review (FR-014)
6. Generate Preview Object
7. Return preview or None

**Example**:
```python
# /hefesto.create invoked without description
preview = run_wizard('create')

if preview:
    # Continue to Human Gate
    decision = present_human_gate(preview)
else:
    print("Wizard cancelled")
```

---

### `resume_wizard(state_path: Path) -> PreviewObject | None`

**Description**: Resume wizard from saved state after timeout/interrupt

**Parameters**:
- `state_path`: Path - Path to `.hefesto/temp/wizard-state-{timestamp}.json`

**Returns**:
- `PreviewObject` if wizard completes
- `None` if user cancels

**Raises**:
- `FileNotFoundError`: If state file doesn't exist
- `InvalidStateError`: If state file is corrupted

**Behavior**:
1. Load Wizard State from JSON
2. Validate state integrity
3. Resume at `current_step`
4. Continue wizard flow
5. Return preview or None

**Example**:
```python
# /hefesto.resume .hefesto/temp/wizard-state-2026-02-05T14-30-00.json
state_path = Path('.hefesto/temp/wizard-state-2026-02-05T14-30-00.json')
preview = resume_wizard(state_path)
```

---

### `wizard_step(step_num: int, state: WizardState) -> str | None`

**Description**: Execute single wizard step with validation

**Parameters**:
- `step_num`: int - Step number (1-4)
- `state`: WizardState - Current wizard state

**Returns**:
- User input (validated) or None if 'back' command

**Raises**:
- `ValidationError`: If input fails validation after 3 attempts
- `TimeoutError`: If step times out (5 minutes)

**Behavior**:
1. Display step prompt
2. Collect user input with timeout
3. Check for 'back' command (FR-012)
4. Validate input (FR-011):
   - Step 1: Skill name → sanitize to T0-HEFESTO-07 format
   - Step 2: Description → max 1024 chars
   - Step 3: Instructions → security validation
   - Step 4: Resources → optional, validate filenames
5. Return validated input or None for 'back'

**Prompts**:
```
Step 1/4: Skill Name
Enter a descriptive name for your skill: 

Step 2/4: Description
Describe what your skill does (max 1024 chars): 

Step 3/4: Main Instructions
Enter the main instructions for using this skill:

Step 4/4: Optional Resources (optional)
Add JIT resources? [scripts/references/assets/done]: 
```

---

## Internal Functions

### `_save_wizard_state(state: WizardState) -> Path`

**Description**: Persist wizard state to `.hefesto/temp/` on timeout

**Returns**: Path to saved state file

**Behavior**:
1. Create `.hefesto/temp/` directory if not exists
2. Generate filename: `wizard-state-{ISO8601-timestamp}.json`
3. Serialize WizardState to JSON
4. Write to file
5. Return path

**Example State File**:
```json
{
  "current_step": 2,
  "collected_inputs": {
    "skill_name": "code-review",
    "description": "Standardize code reviews..."
  },
  "visited_steps": [1],
  "start_timestamp": "2026-02-05T14:30:00",
  "timeout_at": "2026-02-05T14:35:00"
}
```

---

### `_load_wizard_state(state_path: Path) -> WizardState`

**Description**: Load wizard state from JSON file

**Raises**:
- `FileNotFoundError`: If file doesn't exist
- `InvalidStateError`: If JSON is malformed or missing required fields

---

### `_sanitize_skill_name(name: str) -> str`

**Description**: Auto-sanitize skill name to T0-HEFESTO-07 format (FR-013)

**Behavior**:
1. Convert to lowercase
2. Replace non-alphanumeric (except hyphens) with hyphens
3. Remove leading/trailing hyphens
4. Truncate to 64 chars
5. Validate final format
6. Return sanitized name

**Example**:
```python
_sanitize_skill_name("Code Review!") → "code-review"
_sanitize_skill_name("API Docs v2") → "api-docs-v2"
_sanitize_skill_name("VERY_LONG_NAME...") → "very-long-name..." (truncated to 64)
```

---

### `_display_final_review(state: WizardState) -> None`

**Description**: Show collected inputs before generating preview (FR-014)

**Example Output**:
```
=== Wizard Review ===

Skill Name: code-review
Description: Standardize code reviews following best practices
Instructions: [250 chars...]
Resources: 2 scripts, 1 reference

Proceed to generation? [yes/no/back]: 
```

---

## State Machine

```
[Start Wizard]
      │
      ▼
 [Step 1: Name] ←──────┐
      │                │
      ▼                │
 [Step 2: Desc] ───back┘
      │                │
      ▼                │
 [Step 3: Instructions] ─back
      │                │
      ▼                │
 [Step 4: Resources] ──back
      │
      ▼
 [Final Review]
      │
      ├─yes──→ [Generate Preview] → [Return]
      ├─no───→ [Abort] → [Return None]
      └─back─→ [Step 4]
```

---

## Error Handling

| Error | Condition | Recovery |
|-------|-----------|----------|
| `ValidationError` | Input fails validation (3 attempts) | Abort wizard, show error |
| `TimeoutError` | 5 minutes elapsed | Save state, abort, show resume instructions |
| `InvalidStateError` | Corrupted resume file | Abort resume, start fresh wizard |

---

## Edge Cases

### Empty Input (Edge Case #2)
- Prompt again with error message
- Max 3 attempts per step
- After 3 attempts: abort wizard with guidance

### Timeout During Wizard (Edge Case #1)
- Save current state to `.hefesto/temp/wizard-state-{timestamp}.json`
- Display path and resume instructions
- User can resume via `/hefesto.resume {path}`

### Back from Step 1
- Can't go back from first step
- Display message: "Already at first step"

---

## Testing Contract

### Unit Tests

- `test_wizard_step_1_valid()`: Valid skill name sanitized correctly
- `test_wizard_step_1_invalid()`: Invalid name rejected after 3 attempts
- `test_wizard_back_command()`: 'back' returns None, state preserved
- `test_wizard_timeout()`: Timeout saves state and raises error
- `test_sanitize_skill_name()`: Various inputs sanitized to T0-07 format

### Integration Tests

- `test_full_wizard_flow()`: Steps 1-4 → final review → preview generated
- `test_wizard_resume()`: Save → load → continue from saved step
- `test_wizard_cancel()`: User types 'no' at final review

---

**Contract Status**: ✅ COMPLETE  
**Version**: 1.0.0
