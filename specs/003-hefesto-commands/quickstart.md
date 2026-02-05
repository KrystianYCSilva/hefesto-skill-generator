# Quickstart: Implementing Hefesto Commands

**Feature:** 003-hefesto-commands  
**Audience:** Developers and AI agents implementing Phase 1 commands  
**Version:** 1.0.0  
**Last Updated:** 2026-02-04

---

## 1. Purpose

This guide provides a practical, step-by-step approach to implementing Hefesto commands as Markdown-based prompt definitions. Follow this when building commands like `/hefesto.create`, `/hefesto.extract`, etc.

---

## 2. Prerequisites

**What You Need to Know:**

- Agent Skills spec: [agentskills.io](https://agentskills.io)
- T0 rules: `CONSTITUTION.md`
- Templates system: Feature 002 (commands/templates/)
- Helpers: commands/helpers/ (human-gate, template-validator, etc.)
- MEMORY.md structure and state management

**Files You'll Reference:**

- `CONSTITUTION.md` - T0 absolute rules
- `.context/standards/architectural-rules.md` - Enforcement logic
- `commands/templates/skill-template.md` - Base template
- `commands/helpers/human-gate.md` - Approval workflow
- `commands/helpers/template-validator.md` - Validation logic
- `MEMORY.md` - State tracking

---

## 3. Command Definition Structure

**Anatomy of a Command File:**

```markdown
---
name: hefesto.<command>
description: Brief purpose (max 200 chars)
version: 1.0.0
phase: 1
requires_human_gate: true|false
wizard_id: wizard_<command>_skill
tier: 0
---

# Command: /hefesto.<command>

## Purpose
[1-2 sentences describing the command's goal]

## Arguments
[Positional args and flags specification]

## Execution Flow
[Step-by-step logic]

## Wizard Mode
[Interactive prompts when args missing]

## Human Gate Integration
[When and how to trigger approval]

## Helper Invocation
[Which helpers to call and when]

## Error Handling
[Expected error cases and recovery]

## State Updates
[MEMORY.md changes on success]

## Examples
[Usage examples]
```

---

## 4. Implementing a New Command

**5-Step Process:**

### Step 1: Define Command Metadata

```yaml
---
name: hefesto.create
description: Create skill from description
version: 1.0.0
phase: 1
requires_human_gate: true
wizard_id: wizard_create_skill
tier: 0
---
```

### Step 2: Specify Arguments

```markdown
## Arguments

**Positional:**
- `description` (string, optional): Skill description. If missing, triggers Wizard Mode.

**Flags:**
- `--cli`, `-c` (string, optional): Target CLI name. Auto-detected if omitted.
- `--output`, `-o` (path, optional): Output directory. Defaults to `./<cli>/skills/`.

**Examples:**
- `/hefesto.create "Validate email regex"`
- `/hefesto.create --cli gemini`
- `/hefesto.create` (enters Wizard Mode)
```

### Step 3: Write Execution Flow

```markdown
## Execution Flow

1. **Load Context**: Read `/.context/` (T0 rules, standards)
2. **Parse Arguments**: Extract positional args and flags
3. **Trigger Wizard**: If required args missing, invoke wizard_create_skill
4. **Detect CLIs**: Use MEMORY.md `clis_detected` section
5. **Generate Skill**: Apply skill-template.md with variable substitution
6. **Validate**: Call helpers/template-validator.md
7. **Human Gate**: Call helpers/human-gate.md (BLOCKING)
8. **Persist**: Write to `./<cli>/skills/<name>/SKILL.md` on approval
9. **Update State**: Append to MEMORY.md `skills_generated` section
```

### Step 4: Implement Wizard Mode

```markdown
## Wizard Mode

**Trigger Condition:** Missing required positional arg `description`

**Questions (in order):**

1. **Q1: Skill Description**
   - Prompt: "Describe the skill in 1-2 sentences:"
   - Type: text
   - Validation: required, max_length: 200
   - Error: ERR_DESCRIPTION_REQUIRED, ERR_DESCRIPTION_TOO_LONG

2. **Q2: Target CLI**
   - Prompt: "Select target CLI (auto-detected: {{DETECTED_CLIS}}):"
   - Type: select
   - Options: Load from MEMORY.md `clis_detected`
   - Default: First detected CLI
   - Validation: required
   - Error: ERR_CLI_REQUIRED

3. **Q3: Add Sources**
   - Prompt: "Add reference sources (comma-separated URLs):"
   - Type: text
   - Required: false (T1 rule, not T0)
   - Validation: valid_url

**Flow Control:**
- Allow back: yes
- Allow skip: no (all questions required or have defaults)
- Timeout: 300 seconds
```

### Step 5: Integrate Human Gate

```markdown
## Human Gate Integration

**When:** After validation, before persistence (T0-HEFESTO-02)

**Preview Data:**
- Skill path: `./<cli>/skills/<name>/SKILL.md`
- Validation results from template-validator.md
- Content preview (first 50 lines or full if < 100 lines)

**Actions:**
- `[approve]` → Persist to disk, update MEMORY.md
- `[expand]` → Show full content, re-prompt
- `[edit]` → Allow inline edits (advanced, optional)
- `[reject]` → Abort, no persistence

**Invocation:**
```markdown
Call: helpers/human-gate.md
Input: skill_content, validation_results
Output: approval_status (boolean)
```

**Blocking Logic:**
```text
IF approval_status == false:
  ABORT persistence
  LOG rejection to MEMORY.md (optional)
  RETURN error message to user
ELSE:
  PROCEED to persistence
```
```

---

## 5. Wizard Mode Implementation

**Pattern:**

```markdown
## Wizard Mode

**Entry Condition:** [Define when wizard activates]

**Question Sequence:**

### Question 1: <Field Name>
- **Prompt:** "<User-facing question>"
- **Type:** text|select|multiselect|confirm|path
- **Validation Rules:**
  - required: true|false
  - min_length: <int>
  - max_length: <int>
  - pattern: <regex>
  - file_exists: true
- **Error Codes:** ERR_<CODE>
- **Default Value:** <value>
- **Depends On:** <question_id> == <value> (conditional)

**Flow Control:**
- Allow back navigation: yes|no
- Allow skip: yes|no
- Timeout: <seconds>
```

**Common Question Types:**

| Type | Use Case | Example |
|------|----------|---------|
| text | Free-form input | "Describe the skill:" |
| select | Single choice | "Choose CLI: [claude, gemini]" |
| multiselect | Multiple choices | "Select adapters: [claude, gemini, opencode]" |
| confirm | Yes/no | "Add metadata file? (y/n)" |
| path | File/directory | "Path to code file:" |

---

## 6. Human Gate Integration

**When to Use:**

- ALL write operations (create, extract, adapt, sync, delete)
- NEVER for read operations (list, show, validate, help)

**How to Call:**

```markdown
## Human Gate Integration

**Stage:** before_persistence

**Call Pattern:**
1. Generate skill in memory
2. Validate using helpers/template-validator.md
3. IF validation fails:
     SHOW errors
     BLOCK persistence
     RETURN error
4. IF validation passes:
     CALL helpers/human-gate.md
     PASS: skill_content, validation_results
5. AWAIT user action: [approve|expand|edit|reject]
6. IF approved:
     PROCEED to persistence
   ELSE:
     ABORT
```

**Preview Format:**

```text
✅ Skill Generated: <skill-name>

Preview:
-----------------------------------------
name: <skill-name>
description: <description>
[... first 50 lines ...]
-----------------------------------------

Validation: PASS ✅
  ✓ Frontmatter valid
  ✓ Name conforms to spec
  ✓ < 500 lines (actual: <count>)

Actions:
[approve] - Save to disk and update MEMORY.md
[expand]  - Show full content
[reject]  - Discard without saving
```

---

## 7. Helper Invocation

**Common Helpers:**

| Helper | When to Use | Input | Output |
|--------|-------------|-------|--------|
| template-validator.md | Before Human Gate | skill_content | errors[] |
| human-gate.md | Before persistence | skill_content, validation_results | approval_status |
| adapter-selector.md | CLI adaptation | cli_name | adapter_path |
| variable-substitution.md | Template generation | template, variables | filled_content |
| error-handling.md | On failures | error_code, context | formatted_error |
| state-sync.md | MEMORY.md updates | section, operation, data | success |

**Invocation Pattern:**

```markdown
## Helper: <helper-name>

**Purpose:** [Why calling this helper]

**Invocation:**
```text
CALL: commands/helpers/<helper-name>.md
INPUT:
  - param1: <value>
  - param2: <value>
OUTPUT:
  - result: <description>
```

**Error Handling:**
IF helper returns error:
  LOG error code
  ABORT operation
  RETURN user-friendly message
```
```

---

## 8. Testing Commands

**Manual Validation Approach:**

### Test Checklist

- [ ] **T0 Compliance**: Verify all T0 rules (CONSTITUTION.md)
- [ ] **Argument Parsing**: Test with/without args, valid/invalid flags
- [ ] **Wizard Mode**: Test interactive flow, validation, defaults
- [ ] **Human Gate**: Verify blocking before persistence, all actions work
- [ ] **Validation**: Test invalid inputs (uppercase name, long description, etc.)
- [ ] **Persistence**: Verify file created in correct location
- [ ] **State Updates**: Check MEMORY.md updated correctly
- [ ] **Error Handling**: Test failure paths (permission denied, invalid path, etc.)
- [ ] **Idempotency**: Test creating existing skill (collision handling)

### Test Scenarios

**Scenario 1: Happy Path**
```bash
/hefesto.create "Validate email regex"
# Expected: Wizard → Generate → Validate → Human Gate → Persist → Success
```

**Scenario 2: Wizard Mode**
```bash
/hefesto.create
# Expected: Interactive prompts → Collect inputs → Generate → Human Gate → Persist
```

**Scenario 3: Validation Failure**
```bash
/hefesto.create "UPPERCASE-NAME"
# Expected: Validation fails → Human Gate shows errors → Persistence blocked
```

**Scenario 4: Human Gate Rejection**
```bash
/hefesto.create "Valid skill"
# User action: [reject]
# Expected: No files created, MEMORY.md unchanged
```

**Scenario 5: Name Collision**
```bash
/hefesto.create "existing-skill"
# Expected: Detect collision → Prompt [overwrite|rename|cancel]
```

---

## 9. Common Patterns

### Pattern 1: CLI Detection

```markdown
## CLI Detection

**Load from MEMORY.md:**
```text
READ: MEMORY.md section "clis_detected"
PARSE: Extract cli names (claude, gemini, etc.)
IF empty:
  FALLBACK: Run helpers/platform-detection.md
  UPDATE: MEMORY.md with detected CLIs
```

**Usage:**
- Default to first detected CLI
- Offer as select options in Wizard
- Validate --cli flag against detected list
```

### Pattern 2: Skill Name Generation

```markdown
## Skill Name Generation

**From Description:**
```text
INPUT: "Validate email using regex"
STEPS:
  1. Lowercase: "validate email using regex"
  2. Remove stopwords: "validate email regex"
  3. Replace spaces with hyphens: "validate-email-regex"
  4. Validate: Match ^[a-z0-9]+(-[a-z0-9]+)*$
OUTPUT: "validate-email-regex"
```

**Collision Handling:**
```text
IF skill exists at `./<cli>/skills/<name>/`:
  PROMPT: "Skill '<name>' exists. [overwrite|rename|cancel]"
  IF overwrite:
    BACKUP: Move existing to <name>.backup/
    PROCEED
  IF rename:
    PROMPT: "New name:"
    VALIDATE: New name not in use
    PROCEED with new name
  IF cancel:
    ABORT
```
```

### Pattern 3: State Update

```markdown
## MEMORY.md Update

**After Successful Persistence:**

```text
CALL: helpers/state-sync.md
INPUT:
  section: "skills_generated"
  operation: "append"
  data:
    skill_name: "<name>"
    created_at: "<ISO 8601 timestamp>"
    command: "hefesto.create"
    cli: "<cli-name>"
    path: "./<cli>/skills/<name>/SKILL.md"

VERIFY: MEMORY.md updated
LOG: Success message
```
```

---

## 10. Common Pitfalls

**Avoid These Mistakes:**

| Pitfall | Problem | Solution |
|---------|---------|----------|
| **Skipping Human Gate** | Violates T0-HEFESTO-02 | ALWAYS call human-gate.md before writes |
| **Missing Validation** | Invalid skills persist | ALWAYS call template-validator.md first |
| **Hardcoded CLI Paths** | Breaks multi-CLI support | ALWAYS use MEMORY.md `clis_detected` |
| **No Wizard Fallback** | Command fails with no args | ALWAYS implement Wizard for missing args |
| **Ignoring Collision** | Overwrites existing skills | ALWAYS check existence, prompt action |
| **Exceeding 500 Lines** | Violates T0-HEFESTO-03 | Keep command definitions concise, reference helpers |
| **Forgetting State Update** | MEMORY.md desync | ALWAYS update MEMORY.md on success |
| **Unclear Error Messages** | Users confused | Use error-handling.md, provide recovery steps |

---

## 11. Checklist

**Pre-Flight Before Completing a Command:**

- [ ] **Metadata Complete**: name, description, version, phase, tier, requires_human_gate
- [ ] **Arguments Documented**: All positional args and flags with types, defaults, examples
- [ ] **Execution Flow Defined**: Clear step-by-step logic
- [ ] **Wizard Implemented**: Questions, validation, defaults, flow control
- [ ] **Human Gate Integrated**: For writes, blocking, with preview
- [ ] **Helpers Invoked**: template-validator, human-gate, state-sync at minimum
- [ ] **Error Handling**: All failure paths addressed with error codes
- [ ] **State Updates**: MEMORY.md section, operation, data defined
- [ ] **Examples Provided**: At least 2 usage examples
- [ ] **T0 Compliance**: Verified against CONSTITUTION.md
- [ ] **< 500 Lines**: Command file within limit
- [ ] **Testing Notes**: Manual test scenarios documented

---

## 12. References

**Core Documents:**
- Constitution: [CONSTITUTION.md](../../CONSTITUTION.md)
- Architectural Rules: [.context/standards/architectural-rules.md](../../.context/standards/architectural-rules.md)
- Data Model: [data-model.md](./data-model.md)
- Implementation Plan: [plan.md](./plan.md)

**Templates:**
- Skill Template: [commands/templates/skill-template.md](../../commands/templates/skill-template.md)
- MEMORY Template: [commands/templates/memory-template.md](../../commands/templates/memory-template.md)

**Helpers:**
- Human Gate: [commands/helpers/human-gate.md](../../commands/helpers/human-gate.md)
- Template Validator: [commands/helpers/template-validator.md](../../commands/helpers/template-validator.md)
- Adapter Selector: [commands/helpers/adapter-selector.md](../../commands/helpers/adapter-selector.md)
- Variable Substitution: [commands/helpers/variable-substitution.md](../../commands/helpers/variable-substitution.md)
- Error Handling: [commands/helpers/error-handling.md](../../commands/helpers/error-handling.md)
- State Sync: [commands/helpers/state-sync.md](../../commands/helpers/state-sync.md)

**Specification:**
- Feature Spec: [spec.md](./spec.md)
- Requirements: [checklists/requirements.md](./checklists/requirements.md)

---

**END OF QUICKSTART**
