# Research: Hefesto Command Architecture

**Feature**: 003 - Hefesto Commands  
**Phase**: 0 - Research  
**Date**: 2026-02-04  
**Status**: Complete

---

## Research Questions

**R-001**: What is the optimal structure for a Markdown command definition?  
**R-002**: How should Wizard Mode be triggered and managed?  
**R-003**: What patterns exist for argument parsing in prompt-based systems?  
**R-004**: How do commands call helpers (e.g., human-gate.md)?  
**R-005**: What should the command header/frontmatter contain?  
**R-006**: How should error states be handled and reported?

---

## Findings

### R-001: Command Structure

**Pattern from existing commands**:
- YAML frontmatter with metadata (description, command, category, version)
- Clear section hierarchy: Overview → Command Signature → Workflow → Examples → References
- Workflow broken into numbered phases (Phase 0, Phase 1, etc.)
- Pseudocode blocks for logic using markdown code blocks
- Performance targets explicitly stated
- Cross-references to helpers, templates, and specs

**Example** (from `hefesto.list.md:1-65`):
```yaml
---
description: "List command to display all detected CLIs and generated skills from project state"
command: "/hefesto.list"
category: "information"
version: "1.0.0"
---
```

**Key insight**: Commands are self-contained documentation that doubles as implementation specification.

### R-002: Wizard Mode Triggering

**Current pattern**: Not explicitly defined in existing commands, but implied through argument parsing.

**Inference from `hefesto.help.md:26-33`**:
```
/hefesto.help [command] [--verbose]

Arguments:
  command       Show detailed help for specific command (optional)
  
Options:
  --verbose     Show extended help with examples
```

**Recommendation**: Wizard Mode should activate when:
1. Command invoked without required arguments
2. User explicitly passes `--wizard` flag
3. Command detects ambiguity in provided arguments

### R-003: Argument Parsing Patterns

**From `hefesto.list.md:35-43`**:
```
/hefesto.list [--clis] [--skills] [--verbose] [--check-sync]

Options:
  --clis        Show only CLI list (skip skills)
  --skills      Show only skills list (skip CLIs)
  --verbose     Show detailed state including paths and timestamps
  --check-sync  Perform filesystem synchronization check
```

**Pattern identified**:
- Positional arguments in brackets: `[argument]`
- Boolean flags with double-dash: `--flag`
- Mutually exclusive options: `--clis` vs `--skills`
- Modifier flags: `--verbose`, `--force`

**Parsing logic** (inferred from `hefesto.help.md:469-482`):
```python
def parse_args(args):
    command_name = args.command OR null
    verbose = args.has_flag("--verbose")
    
    if command_name:
        display_command_help(command_name, verbose)
    elif verbose:
        display_verbose_help()
    else:
        display_general_help()
```

### R-004: Helper Integration

**Pattern from `human-gate.md:1-61`**:

Helpers are referenced inline in command workflows:
```markdown
1. Run CONSTITUTION validation
   (see: helpers/constitution-validator.md)
   IF invalid → Block execution
```

**Helper call pattern** (from `hefesto.list.md:51-60`):
```markdown
### Phase 0: Pre-Execution Validation

1. Run CONSTITUTION validation
   (see: helpers/constitution-validator.md)
   IF invalid → Block execution

2. Check if Hefesto is initialized
   IF NOT file_exists("MEMORY.md"):
     DISPLAY: "❌ Hefesto not initialized."
     ABORT (exit code 1)
```

**Key insight**: Helpers are declarative modules that commands reference by name. The AI agent reads the helper file and executes its logic inline.

### R-005: Header/Frontmatter Content

**Standard fields** (from all command files):
```yaml
---
description: "Brief description of command purpose"
command: "/hefesto.command"
category: "information" | "initialization" | "skill-management"
version: "1.0.0"
user_story: "US3"        # Optional
priority: "P2"           # Optional
phase: "polish"          # Optional
---
```

**Additional metadata for helpers** (from `template-validator.md:1-4`):
```yaml
---
description: "Logic for validating templates against Agent Skills spec"
version: "1.0.0"
---
```

### R-006: Error Handling

**Pattern from `hefesto.list.md:519-548`**:
```markdown
### ERR-002: Corrupted MEMORY.md

⚠️ State Recovery: MEMORY.md corrupted

Attempting to parse YAML frontmatter... ❌ Failed
Backup created: MEMORY.md.backup.2026-02-04T16-00-00Z
Rebuilding state from filesystem...

✅ State rebuilt successfully
```

**Error handling strategy**:
1. Named error codes (ERR-001, ERR-002, etc.)
2. Recovery procedures inline in error messages
3. User-friendly display with emojis (unless `--no-emoji`)
4. Graceful degradation with backups
5. Clear next steps for user

**From `human-gate.md:42-49`**:
```python
if validation_errors:
    print("❌ Validation Failed:")
    for err in validation_errors:
        print(f"  - {err}")
    print("Persistence BLOCKED.")
    return False
```

**Key insight**: Errors block execution explicitly and provide actionable feedback.

---

## Recommendations

### 1. Command Structure Template
- Use consistent YAML frontmatter
- Organize workflow into phases (0-N)
- Include performance targets
- Provide multiple usage examples
- Reference helpers by file path

### 2. Wizard Mode Design
- Trigger on missing required arguments OR `--wizard` flag
- Use interactive prompts with clear options
- Validate input at each step before proceeding
- Allow escape/cancel at any step

### 3. Argument Parsing Strategy
- Support both positional and flag-based arguments
- Use `--flag` for booleans, `--key=value` for parameters
- Implement `--help` for every command
- Support `--verbose` for detailed output
- Allow `--force` for overrides

### 4. Helper Integration
- Reference helpers by file path: `(see: helpers/helper-name.md)`
- Helpers return structured data or boolean success
- Commands orchestrate helper calls
- Helpers are reusable across commands

### 5. Error Protocol
- Use error codes: `ERR-XXX`
- Display user-friendly messages
- Provide recovery steps
- Create backups before destructive operations
- Log errors for debugging

---

## Command Structure Template

```markdown
---
description: "One-line description of command purpose"
command: "/hefesto.command-name"
category: "information" | "initialization" | "skill-management"
version: "1.0.0"
---

# /hefesto.command-name - Command Title

**Command**: `/hefesto.command-name`  
**Purpose**: Detailed purpose statement  
**Category**: Category name

---

## Overview

Brief description of what this command does (2-3 sentences).

---

## Command Signature

\```text
/hefesto.command-name [arg1] [arg2] [--flag1] [--flag2]

Arguments:
  arg1          Description (required/optional)
  arg2          Description (required/optional)
  
Options:
  --flag1       Description
  --flag2       Description
\```

---

## Execution Workflow

### Phase 0: Pre-Execution Validation

\```markdown
1. Validate prerequisites
   (see: helpers/prerequisite-validator.md)
   IF invalid → ABORT

2. Parse arguments
   args = parse_arguments()
   IF missing_required → TRIGGER wizard_mode OR ABORT
\```

### Phase 1: Main Execution

\```markdown
1. Execute primary logic
   result = do_work(args)
   
2. Validate result
   IF errors → Handle errors (see Phase 3)
\```

### Phase 2: Post-Execution

\```markdown
1. Display results
2. Update state if needed
3. Show next steps
\```

### Phase 3: Error Handling

\```markdown
1. Identify error type
2. Display user-friendly message
3. Provide recovery steps
4. Log for debugging
\```

---

## Usage Examples

### Example 1: Basic Usage

\```text
> /hefesto.command-name arg1

Expected output...
\```

### Example 2: With Flags

\```text
> /hefesto.command-name arg1 --flag1

Expected output...
\```

---

## Error Scenarios

### ERR-XXX: Error Name

\```text
❌ Error message

Recovery steps...
\```

---

## Performance Targets

| Operation | Target | Typical |
|-----------|--------|---------|
| Main operation | < Xms | Yms |

---

## References

- **Specification**: Link to spec
- **Helpers**: List of helper files
- **Related Commands**: List of related commands
```

---

## Wizard Mode Flow

```markdown
### Wizard Mode Activation

TRIGGER when:
1. Required arguments missing
2. User passes --wizard flag
3. Ambiguous input detected

### Wizard Flow

STEP 1: Welcome
  DISPLAY: "🧙 Wizard Mode: [Command Name]"
  DISPLAY: Brief description
  DISPLAY: "[continue] or [exit]"
  
  INPUT: user_choice
  IF user_choice == "exit" → ABORT

STEP 2: Gather Required Arguments
  FOR EACH required_arg IN command.required_args:
    DISPLAY: "Enter {arg.name}: {arg.description}"
    DISPLAY: "Example: {arg.example}"
    
    INPUT: arg_value
    VALIDATE: arg_value against arg.validation_rules
    
    IF invalid:
      DISPLAY: "❌ Invalid: {validation_error}"
      RETRY (max 3 attempts)
    
    args[arg.name] = arg_value

STEP 3: Optional Arguments
  DISPLAY: "Configure optional settings? [yes/no]"
  
  INPUT: configure_optional
  IF configure_optional == "yes":
    FOR EACH optional_arg IN command.optional_args:
      DISPLAY: "{arg.name} (default: {arg.default})"
      INPUT: arg_value OR SKIP
      IF arg_value:
        args[arg.name] = arg_value

STEP 4: Confirmation
  DISPLAY: "Preview:"
  DISPLAY: format_args(args)
  DISPLAY: "[confirm] [edit] [cancel]"
  
  INPUT: action
  CASE action:
    "confirm" → PROCEED to execution
    "edit" → GOTO STEP 2
    "cancel" → ABORT

STEP 5: Execution
  EXECUTE command with args
  DISPLAY results

### Wizard State Management

- Store partial input in memory
- Allow resume if interrupted
- Clear state after completion or cancellation
```

---

## Argument Parsing Strategy

```python
def parse_command_input(raw_input):
    """
    Parse command input into structured arguments.
    
    Input format: /command [positional] [--flag] [--key=value]
    """
    parts = raw_input.strip().split()
    command = parts[0]
    
    positional = []
    flags = {}
    
    for part in parts[1:]:
        if part.startswith("--"):
            if "=" in part:
                # Key-value: --output=file.txt
                key, value = part[2:].split("=", 1)
                flags[key] = value
            else:
                # Boolean flag: --verbose
                flags[part[2:]] = True
        else:
            # Positional argument
            positional.append(part)
    
    return {
        "command": command,
        "positional": positional,
        "flags": flags
    }

def validate_args(parsed, command_spec):
    """
    Validate parsed arguments against command specification.
    """
    errors = []
    
    # Check required positional arguments
    required = command_spec.required_args
    if len(parsed["positional"]) < len(required):
        errors.append(f"Missing required arguments: {required[len(parsed['positional']):]}")
    
    # Check flag types
    for flag, value in parsed["flags"].items():
        if flag not in command_spec.valid_flags:
            errors.append(f"Unknown flag: --{flag}")
    
    return errors

def should_trigger_wizard(parsed, command_spec):
    """
    Determine if wizard mode should activate.
    """
    # Explicit wizard flag
    if parsed["flags"].get("wizard"):
        return True
    
    # Missing required arguments
    if len(parsed["positional"]) < len(command_spec.required_args):
        return True
    
    # Ambiguous input (command-specific logic)
    if command_spec.check_ambiguity(parsed):
        return True
    
    return False
```

---

## Helper Integration Examples

### Example 1: Validation Helper

**Command file**: `hefesto.create.md`
```markdown
### Phase 0: Pre-Execution

1. Validate CONSTITUTION
   (see: helpers/constitution-validator.md)
   IF invalid → ABORT with ERR-004
```

**Helper file**: `helpers/constitution-validator.md`
```python
def validate_constitution():
    if not file_exists("CONSTITUTION.md"):
        return {"valid": False, "error": "ERR-003", "message": "Missing CONSTITUTION.md"}
    
    content = read_file("CONSTITUTION.md")
    checksum = compute_sha256(content)
    
    if checksum != EXPECTED_CHECKSUM:
        return {"valid": False, "error": "ERR-004", "message": "Invalid CONSTITUTION.md"}
    
    return {"valid": True}
```

### Example 2: Human Gate Helper

**Command file**: `hefesto.create.md`
```markdown
### Phase 4: Human Gate

1. Show preview to user
2. Request approval
   (see: helpers/human-gate.md)
   IF rejected → ABORT
   IF approved → PROCEED to Phase 5
```

**Helper usage**:
```python
# In command execution
skill_content = generate_skill(description)
validation = validate_template(skill_content)

approved = human_gate(skill_content, validation.errors)
if approved:
    write_file(skill_path, skill_content)
```

### Example 3: Chained Helpers

```markdown
### Phase 1: Setup

1. Validate environment
   (see: helpers/environment-validator.md)
   
2. Detect CLIs
   (see: helpers/cli-detection-strategy.md)
   
3. Validate each CLI
   FOR EACH detected_cli:
     (see: helpers/cli-specific-validator.md)
```

---

## Error Handling Patterns

### Pattern 1: Blocking Errors

```markdown
ERR-XXX: Critical Error

Display:
❌ Critical Error: {error_message}

This is a blocking error. Operation cannot continue.

Recovery steps:
1. Step one to fix
2. Step two to fix
3. Retry command

ABORT execution (exit code 1)
```

### Pattern 2: Recoverable Errors

```markdown
ERR-YYY: Recoverable Error

Display:
⚠️ Warning: {error_message}

Attempting automatic recovery...
✅ Recovery successful

OR

❌ Recovery failed. Manual intervention required:
1. Recovery step one
2. Recovery step two
3. Retry command
```

### Pattern 3: Graceful Degradation

```markdown
WARN-ZZZ: Non-Critical Warning

Display:
⚠️ Warning: {warning_message}

Impact: {what_features_affected}
Recommendation: {how_to_fix}

Continue execution with reduced functionality? [yes/no]
```

### Error Code Registry

**Location**: `commands/helpers/error-codes.md`

```markdown
| Code | Type | Description | Recovery |
|------|------|-------------|----------|
| ERR-001 | Permission | Permission denied | Fix permissions |
| ERR-002 | Corruption | Corrupted state file | Auto-recovery with backup |
| ERR-003 | Missing File | Missing CONSTITUTION.md | Auto-restore |
| ERR-004 | Validation | Invalid CONSTITUTION.md | Restore from backup |
| ERR-005 | Detection | No CLIs detected | Install CLI or manual spec |
```

---

## Conclusion and Next Steps

### Summary

Analysis of existing command files reveals:
1. **Consistent structure**: YAML frontmatter + phased workflows + examples
2. **Clear separation**: Commands orchestrate, helpers execute
3. **User-centric design**: Examples, errors, and recovery steps prominent
4. **Performance-aware**: Explicit targets for critical operations
5. **Self-documenting**: Commands serve as both spec and documentation

### Next Steps

**Phase 1: Architecture Design**
- Define command execution engine requirements
- Design wizard mode state machine
- Create argument parser specification
- Document helper contract interface

**Phase 2: Implementation**
- Implement argument parser (R-003)
- Implement wizard mode framework (R-002)
- Create helper execution engine (R-004)
- Build error handler with code registry (R-006)

**Phase 3: Command Rollout**
- `/hefesto.create` with wizard mode
- `/hefesto.extract` with wizard mode
- `/hefesto.validate`
- `/hefesto.adapt` (advanced)
- `/hefesto.sync` (advanced)

### Open Questions

1. Should wizard mode be default or opt-in?
2. How to handle partial execution in wizard mode (interruptions)?
3. Should helpers be executable (Python) or declarative (Markdown)?
4. What level of undo/redo support is needed?

---

**Research Complete** | Phase 0 | 2026-02-04
