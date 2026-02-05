# Data Model - Hefesto Commands (Feature 003)

**Feature:** 003-hefesto-commands  
**Phase:** 1 (Command Execution)  
**Version:** 1.0.0  
**Last Updated:** 2026-02-04

---

## Overview

This document defines the data model for Hefesto command system. Entities represent commands, wizards, human gates, skills, arguments, and errors. The model ensures consistency between command execution, validation, and state management in MEMORY.md.

---

## Command Entity

```yaml
Command:
  name:
    type: string
    description: Command identifier without slash prefix
    constraints:
      - required: true
      - pattern: ^hefesto\.(init|create|extract|validate|adapt|sync|list|detect)$
      - max_length: 50
    example: "hefesto.create"

  alias:
    type: string[]
    description: Alternative command names
    constraints:
      - required: false
      - pattern: ^[a-z\.]+$
    example: ["hf.create", "create"]

  description:
    type: string
    description: Human-readable command purpose
    constraints:
      - required: true
      - max_length: 200
    example: "Create skill from description"

  phase:
    type: integer
    description: Implementation phase number
    constraints:
      - required: true
      - min: 1
      - max: 4
    default: 1

  requires_human_gate:
    type: boolean
    description: Whether command needs approval before persistence
    constraints:
      - required: true
    default: false

  wizard_id:
    type: string
    description: Reference to associated Wizard entity
    constraints:
      - required: false
      - references: Wizard.id
    example: "wizard_create_skill"

  arguments:
    type: Argument[]
    description: Command arguments and flags
    constraints:
      - required: false
    relationship: one-to-many with Argument

  execution_steps:
    type: string[]
    description: Ordered list of execution steps
    constraints:
      - required: true
      - min_items: 1
    example:
      - "Load context from /.context/"
      - "Start wizard if configured"
      - "Generate skill in memory"
      - "Trigger human gate"
      - "Persist on approval"

  state_updates:
    type: object
    description: MEMORY.md state changes on success
    constraints:
      - required: true
    properties:
      section: string
      operation: enum[append, update, create]
    example:
      section: "last_skill_generated"
      operation: "update"

  tier:
    type: integer
    description: Authority tier (0-3)
    constraints:
      - required: true
      - min: 0
      - max: 3
    default: 0
```

---

## Wizard Entity

```yaml
Wizard:
  id:
    type: string
    description: Unique wizard identifier
    constraints:
      - required: true
      - pattern: ^wizard_[a-z_]+$
      - max_length: 50
    example: "wizard_create_skill"

  command_name:
    type: string
    description: Associated command
    constraints:
      - required: true
      - references: Command.name
    example: "hefesto.create"

  questions:
    type: Question[]
    description: Ordered wizard questions
    constraints:
      - required: true
      - min_items: 1
    relationship: one-to-many with Question

  Question:
    id:
      type: string
      description: Question identifier
      constraints:
        - required: true
        - pattern: ^q_[a-z_]+$
      example: "q_skill_description"

    prompt:
      type: string
      description: Question text shown to user
      constraints:
        - required: true
        - max_length: 500
      example: "Describe the skill in 1-2 sentences"

    type:
      type: enum
      description: Question type
      constraints:
        - required: true
        - values: [text, select, multiselect, confirm, path]
      example: "text"

    validation:
      type: ValidationRule[]
      description: Input validation rules
      constraints:
        - required: false

    ValidationRule:
      rule:
        type: enum
        values: [required, min_length, max_length, pattern, file_exists]
        example: "max_length"
      
      value:
        type: any
        description: Rule parameter
        example: 200

      error_code:
        type: string
        description: Error to throw on validation failure
        references: Error.code
        example: "ERR_DESCRIPTION_TOO_LONG"

    default_value:
      type: any
      description: Default answer
      constraints:
        - required: false
      example: "Skill description here"

    depends_on:
      type: object
      description: Conditional question display
      constraints:
        - required: false
      properties:
        question_id: string
        expected_value: any
      example:
        question_id: "q_cli_detected"
        expected_value: false

  flow_control:
    type: object
    description: Wizard flow logic
    properties:
      allow_skip: boolean
      allow_back: boolean
      timeout_seconds: integer
    default:
      allow_skip: false
      allow_back: true
      timeout_seconds: 300
```

---

## Human Gate Entity

```yaml
HumanGate:
  id:
    type: string
    description: Unique gate identifier
    constraints:
      - required: true
      - pattern: ^gate_[a-z_]+$
    example: "gate_skill_approval"

  trigger:
    type: object
    description: When gate is triggered
    constraints:
      - required: true
    properties:
      command_name:
        type: string
        references: Command.name
        example: "hefesto.create"
      
      stage:
        type: enum
        values: [before_persistence, after_generation, before_deletion]
        example: "before_persistence"

  preview_data:
    type: object
    description: Data to show user for approval
    constraints:
      - required: true
    properties:
      skill_path:
        type: string
        example: "/.skills/hefesto-git-commit.skill.md"
      
      validation_results:
        type: ValidationResult[]
        relationship: references ValidationResult

      content_preview:
        type: string
        description: First N lines of generated content
        constraints:
          - max_length: 2000

  actions:
    type: Action[]
    description: Available user actions
    constraints:
      - required: true
      - min_items: 1

  Action:
    name:
      type: enum
      values: [approve, expand, edit, reject]
      example: "approve"

    label:
      type: string
      description: Button/option label
      example: "[approve] - Save skill"

    consequence:
      type: string
      description: What happens on selection
      example: "Persist skill to disk and update MEMORY.md"

    next_state:
      type: enum
      values: [persist, show_full, request_edits, abort]
      example: "persist"

  timeout:
    type: integer
    description: Seconds before auto-abort
    constraints:
      - required: false
      - min: 30
      - max: 600
    default: 120

  ValidationResult:
    check_name:
      type: string
      example: "Agent Skills Spec Compliance"

    status:
      type: enum
      values: [pass, fail, warn]
      example: "pass"

    message:
      type: string
      example: "All required sections present"

    error_code:
      type: string
      references: Error.code
      required: false
```

---

## Skill Entity

```yaml
Skill:
  description: Reference to Feature 002 skill definition
  reference: "specs/002-skill-structure/skill-entity.md"
  
  properties_used_by_commands:
    - id
    - name
    - path
    - status
    - created_at
    - last_validated
```

---

## Argument Entity

```yaml
Argument:
  name:
    type: string
    description: Argument name
    constraints:
      - required: true
      - pattern: ^[a-z_]+$
    example: "description"

  type:
    type: enum
    description: Argument type
    constraints:
      - required: true
      - values: [positional, flag, option]
    example: "positional"

  value_type:
    type: enum
    description: Expected value type
    constraints:
      - required: true
      - values: [string, integer, boolean, path, enum]
    example: "string"

  position:
    type: integer
    description: Position for positional args
    constraints:
      - required_if: type == "positional"
      - min: 0
    example: 0

  flag:
    type: string
    description: Flag syntax for flags/options
    constraints:
      - required_if: type in ["flag", "option"]
      - pattern: ^--[a-z-]+$
    example: "--cli"

  short_flag:
    type: string
    description: Short flag syntax
    constraints:
      - required: false
      - pattern: ^-[a-z]$
    example: "-c"

  required:
    type: boolean
    constraints:
      - required: true
    default: false

  default_value:
    type: any
    description: Default if not provided
    constraints:
      - required: false
    example: "."

  description:
    type: string
    constraints:
      - required: true
      - max_length: 200
    example: "Target CLI name"

  validation:
    type: ValidationRule[]
    description: Argument validation rules
    constraints:
      - required: false
```

---

## Error Entity

```yaml
Error:
  code:
    type: string
    description: Unique error code
    constraints:
      - required: true
      - pattern: ^ERR_[A-Z_]+$
    example: "ERR_DESCRIPTION_TOO_LONG"

  message:
    type: string
    description: Human-readable error message
    constraints:
      - required: true
      - max_length: 500
    example: "Skill description must be under 200 characters"

  severity:
    type: enum
    description: Error severity level
    constraints:
      - required: true
      - values: [fatal, error, warning, info]
    example: "error"

  category:
    type: enum
    description: Error category
    constraints:
      - required: true
      - values: [validation, execution, persistence, user_input, context]
    example: "validation"

  recovery_action:
    type: string
    description: Suggested recovery step
    constraints:
      - required: false
      - max_length: 300
    example: "Shorten the description and try again"

  related_entity:
    type: string
    description: Entity type that caused error
    constraints:
      - required: false
      - values: [Command, Wizard, Skill, Argument, HumanGate]
    example: "Wizard"

  tier:
    type: integer
    description: Authority tier of error source
    constraints:
      - required: true
      - min: 0
      - max: 3
    default: 1
```

---

## Entity Relationships

```
Command 1---* Argument
Command 1---? Wizard
Command 1---* HumanGate
Command *---* Skill (operates on)

Wizard 1---* Question
Question *---* ValidationRule
Question *---? Error (on validation failure)

HumanGate 1---* Action
HumanGate 1---* ValidationResult
ValidationResult *---? Error

Skill 1---* (defined in Feature 002)

Argument *---* ValidationRule
Argument *---? Error (on validation failure)
```

**Legend:**
- `1---*` : one-to-many
- `1---?` : one-to-optional
- `*---*` : many-to-many

---

## State Management

### MEMORY.md Integration

```yaml
StateUpdate:
  trigger:
    type: enum
    values: [command_start, command_success, command_failure, skill_created]

  section:
    type: string
    description: MEMORY.md section to update
    example: "skills_generated"

  operation:
    type: enum
    values: [append, update, create, delete]
    example: "append"

  data:
    type: object
    description: Data to write
    example:
      skill_name: "hefesto-git-commit"
      created_at: "2026-02-04T10:30:00Z"
      command: "hefesto.create"

  rollback:
    type: object
    description: How to revert on failure
    properties:
      enabled: boolean
      previous_state: object
```

---

## Example Instances

### Command Instance

```yaml
name: "hefesto.create"
alias: ["hf.create", "create"]
description: "Create skill from description"
phase: 1
requires_human_gate: true
wizard_id: "wizard_create_skill"
arguments:
  - name: "description"
    type: "positional"
    value_type: "string"
    position: 0
    required: false
    description: "Skill description"
  - name: "cli"
    type: "option"
    value_type: "string"
    flag: "--cli"
    short_flag: "-c"
    required: false
    description: "Target CLI"
execution_steps:
  - "Load context from /.context/"
  - "Start wizard_create_skill"
  - "Generate skill in memory"
  - "Validate against Agent Skills spec"
  - "Trigger gate_skill_approval"
  - "Persist on approval"
state_updates:
  section: "skills_generated"
  operation: "append"
tier: 0
```

### Wizard Instance

```yaml
id: "wizard_create_skill"
command_name: "hefesto.create"
questions:
  - id: "q_skill_description"
    prompt: "Describe the skill in 1-2 sentences:"
    type: "text"
    validation:
      - rule: "required"
        error_code: "ERR_DESCRIPTION_REQUIRED"
      - rule: "max_length"
        value: 200
        error_code: "ERR_DESCRIPTION_TOO_LONG"
    default_value: null
  - id: "q_target_cli"
    prompt: "Target CLI (auto-detected):"
    type: "select"
    validation:
      - rule: "required"
        error_code: "ERR_CLI_REQUIRED"
    default_value: "git"
flow_control:
  allow_skip: false
  allow_back: true
  timeout_seconds: 300
```

### Human Gate Instance

```yaml
id: "gate_skill_approval"
trigger:
  command_name: "hefesto.create"
  stage: "before_persistence"
preview_data:
  skill_path: "/.skills/hefesto-git-commit.skill.md"
  validation_results:
    - check_name: "Agent Skills Spec"
      status: "pass"
      message: "All sections present"
  content_preview: "# Git Commit Skill\n\n## Capability\nCreate commits..."
actions:
  - name: "approve"
    label: "[approve] - Save skill"
    consequence: "Persist skill to disk and update MEMORY.md"
    next_state: "persist"
  - name: "reject"
    label: "[reject] - Discard"
    consequence: "Abort without saving"
    next_state: "abort"
timeout: 120
```

### Error Instance

```yaml
code: "ERR_DESCRIPTION_TOO_LONG"
message: "Skill description must be under 200 characters (got 245)"
severity: "error"
category: "validation"
recovery_action: "Shorten the description and try again"
related_entity: "Wizard"
tier: 1
```

---

**END OF DATA MODEL**
