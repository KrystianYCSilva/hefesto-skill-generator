---
description: "Extract Agent Skill from existing code file by wrapping with skill metadata"
command: "/hefesto.extract"
category: "skill-management"
user_story: "US1"
priority: "P1"
version: "1.0.0"
---

# /hefesto.extract - Extract Skill Command

**Command**: `/hefesto.extract`  
**Purpose**: Extract Agent Skill from existing code file  
**User Story**: US1 - Core Skill Creation & Extraction (P1)

---

## Overview

The `/hefesto.extract` command wraps existing code files with Agent Skills specification metadata, creating executable skills. Features:

1. **Code Analysis**: Auto-detect language, framework, and purpose
2. **Wizard Mode**: Interactive prompts when file path missing
3. **Human Gate**: Mandatory approval before persistence (T0-HEFESTO-02)
4. **Security Scan**: Detect secrets and credentials (T0-HEFESTO-11)
5. **Multi-CLI**: Generate for all detected CLIs

**Target Performance**: < 7s (excluding Human Gate wait)

---

## Command Signature

```text
/hefesto.extract [file_path] [--target <cli>] [--name <skill-name>]

Arguments:
  file_path      Path to code file to extract (optional)
                 If missing: Enter Wizard Mode
                 Supports: .py, .js, .ts, .sh, .java, .go, etc.

Options:
  --target <cli>     Target specific CLI (default: all detected)
  --name <name>      Override auto-generated skill name
```

---

## Execution Workflow

### Phase 0: Pre-Execution Validation

```markdown
1. Validate CONSTITUTION
   (see: helpers/constitution-validator.md)
   IF invalid → ABORT

2. Check Hefesto initialization
   IF NOT file_exists("MEMORY.md"):
     DISPLAY: "❌ Hefesto not initialized. Run /hefesto.init first."
     ABORT (exit code 1)

3. Load context
   - Read T0 rules from CONSTITUTION.md
   - Load CLI detection from MEMORY.md
   - Load extraction template
```

**Performance Target**: < 500ms

---

### Phase 1: Argument Parsing & Wizard Mode

```markdown
1. Parse arguments
   file_path = args.positional[0] OR null
   target_cli = args.flags.get("target") OR null
   custom_name = args.flags.get("name") OR null

2. Check Wizard Mode
   IF file_path IS null:
     TRIGGER wizard_mode()

3. Validate file existence
   IF NOT file_exists(file_path):
     ERROR E-EXTRACT-001: "File not found: {file_path}"
     SUGGEST: "Check path and try again"
     
     IF similar_files exist:
       DISPLAY: "Did you mean:"
       FOR EACH similar IN similar_files:
         DISPLAY: "  - {similar}"
     
     ABORT

4. Check file readability
   TRY:
     test_read(file_path)
   CATCH PermissionError:
     ERROR E-EXTRACT-002: "File not readable: {file_path}"
     SUGGEST: "Check permissions (chmod +r {file_path})"
     ABORT
```

**Performance Target**: < 200ms  
**References**: FR-003, FR-010

---

### Wizard Mode Flow

```markdown
WIZARD MODE ACTIVATED
═══════════════════════════════════════════════════

Step 1: Code File Path
  PROMPT: "Path to code file:"
  EXAMPLE: "./utils/email-validator.py"
  
  INPUT: file_path
  VALIDATE:
    - File exists (E-EXTRACT-001)
    - File readable (E-EXTRACT-002)
    - File size < 100KB (E-EXTRACT-006 warning if larger)
  
  IF invalid: RETRY (max 3 attempts)

Step 2: Skill Name (Auto-Generated)
  detected_name = basename(file_path, remove_extension=true)
  DISPLAY: "Suggested name: {detected_name}"
  PROMPT: "Press Enter to accept, or type custom name:"
  
  INPUT: custom_name OR accept_default
  VALIDATE:
    - Lowercase only (T0-HEFESTO-07)
    - Hyphens for separators
    - Max 64 characters
  
  AUTO-SANITIZE: Convert to valid format

Step 3: Target CLIs
  DISPLAY: "Detected CLIs: <cli-list>"
  PROMPT: "Target CLIs (comma-separated or 'all') [all]:"
  
  INPUT: target_selection OR default_all

Step 4: Confirmation
  DISPLAY: "Preview:"
  DISPLAY: "  Source: {file_path}"
  DISPLAY: "  Name: {skill_name}"
  DISPLAY: "  Target CLIs: {targets}"
  PROMPT: "[continue] [edit] [cancel]"
  
  CASE input:
    "continue" → PROCEED to Phase 2
    "edit" → GOTO Step 1
    "cancel" → ABORT gracefully
```

**Timeout**: 300 seconds of inactivity triggers cleanup

---

### Phase 2: Code Analysis

```markdown
1. Read source file
   TRY:
     source_content = read_file(file_path)
     file_size = get_file_size(file_path)
   CATCH IOError:
     ERROR E-EXTRACT-002: "Cannot read file"
     ABORT

2. Check file size
   IF file_size > 100KB:
     WARN E-EXTRACT-006: "File is large ({file_size} KB)"
     PROMPT: "Continue? [yes/no]"
     IF no → ABORT

3. Detect language and framework
   (see: helpers/code-analyzer.md)
   
   analysis = analyze_code(source_content, file_path)
   
   DETECT:
     - language: python, javascript, typescript, bash, etc.
     - framework: jest, pytest, express, etc.
     - purpose: testing, validation, deployment, etc.
     - entry_point: main function or command
     - dependencies: imports, requires

4. Security scan
   (see: helpers/secret-detector.md)
   
   secrets = detect_secrets(source_content)
   
   IF secrets NOT empty:
     ERROR E-EXTRACT-005: "Code contains potential secrets"
     DISPLAY: "Found in lines: {secret_lines}"
     DISPLAY: "This violates T0-HEFESTO-11 (Security by Default)"
     SUGGEST: "Remove secrets, use environment variables"
     ABORT (security violation)

5. Generate description
   IF custom_description NOT provided:
     description = infer_description(analysis)
     EXAMPLE: "Execute {language} {framework} {purpose} script"
```

**Performance Target**: < 3s  
**References**: T0-HEFESTO-11

---

### Phase 3: Skill Generation

```markdown
1. Generate skill name
   skill_name = custom_name OR sanitize_name(basename(file_path))

2. Detect collision
   FOR EACH target_cli IN targets:
     skill_path = ".{cli}/skills/{skill_name}/SKILL.md"
     IF file_exists(skill_path):
       TRIGGER collision_gate()  # FR-008

3. Generate skill wrapper
   (see: templates/extract/SKILL.md.template)
   
   skill_content = template.render({
     name: skill_name,
     description: description,
     language: analysis.language,
     framework: analysis.framework,
     source_file: basename(file_path),
     entry_point: analysis.entry_point,
     dependencies: analysis.dependencies,
     usage_example: generate_usage(analysis),
     created: current_timestamp(),
     version: "1.0.0"
   })

4. Prepare file copy
   target_filename = basename(file_path)
   script_path = "scripts/{target_filename}"

5. Generate metadata
   metadata = {
     name: skill_name,
     description: description,
     type: "extracted",
     source: file_path,
     language: analysis.language,
     created: current_timestamp()
   }
```

**Performance Target**: < 2s  
**References**: T0-HEFESTO-01, T0-HEFESTO-07

---

### Phase 4: Validation

```markdown
1. Validate against Agent Skills spec
   (see: helpers/template-validator.md)
   
   validation_errors = validate_skill(skill_content)
   
   CHECK:
     - Valid frontmatter
     - Name format correct
     - Description not empty
     - SKILL.md < 500 lines
     - No secrets in wrapper

2. Block persistence if invalid
   IF validation_errors NOT empty:
     DISPLAY: "❌ Validation Failed:"
     FOR EACH error IN validation_errors:
       DISPLAY: "  - {error.code}: {error.message}"
     ABORT
```

**Performance Target**: < 500ms  
**References**: T0-HEFESTO-06

---

### Phase 5: Human Gate

```markdown
1. Display preview
   (see: helpers/human-gate.md)
   
   DISPLAY:
   ═══════════════════════════════════════════════════
   ✅ Skill Extracted: {skill_name}
   ═══════════════════════════════════════════════════
   
   Source Analysis:
   -----------------------------------------
   File: {file_path}
   Language: {analysis.language}
   Framework: {analysis.framework}
   Purpose: {analysis.purpose}
   Size: {file_size} KB
   -----------------------------------------
   
   Generated Skill:
   -----------------------------------------
   name: {skill_name}
   description: {description}
   type: extracted
   -----------------------------------------
   
   [First 20 lines of SKILL.md...]
   
   Validation: PASS ✅
   
   Files to create:
     {FOR EACH cli}
     - .{cli}/skills/{skill_name}/SKILL.md
     - .{cli}/skills/{skill_name}/metadata.yaml
     - .{cli}/skills/{skill_name}/scripts/{filename}
   
   ═══════════════════════════════════════════════════

2. Prompt for approval
   PROMPT: "Actions: [approve] [expand] [edit] [reject]"
   
   INPUT: action
   
   CASE action:
     "approve" → PROCEED to Phase 6
     "expand"  → DISPLAY full content, re-prompt
     "edit"    → Allow edits, re-validate
     "reject"  → ABORT "Operation cancelled"
     timeout   → ABORT after 120s
```

**References**: T0-HEFESTO-02, FR-002

---

### Phase 6: Persistence

```markdown
1. Create directories
   FOR EACH target_cli IN targets:
     skill_dir = ".{target_cli}/skills/{skill_name}/"
     scripts_dir = "{skill_dir}/scripts/"
     
     create_directory(skill_dir)
     create_directory(scripts_dir)

2. Copy source file
   FOR EACH target_cli IN targets:
     source_dest = ".{target_cli}/skills/{skill_name}/scripts/{filename}"
     copy_file(file_path, source_dest)
     
     # Preserve permissions if executable
     IF is_executable(file_path):
       set_executable(source_dest)

3. Write skill files
   FOR EACH target_cli IN targets:
     skill_path = ".{target_cli}/skills/{skill_name}/SKILL.md"
     metadata_path = ".{target_cli}/skills/{skill_name}/metadata.yaml"
     
     write_file(skill_path, skill_content)
     write_file(metadata_path, metadata)

4. Update MEMORY.md
   state = read_memory_md()
   state.skills_created.append({
     name: skill_name,
     created: current_timestamp(),
     source: file_path,
     type: "extracted",
     clis: targets,
     status: "active"
   })
   write_memory_md(state)

5. Success message
   DISPLAY:
   ✅ Skill extracted successfully!
   
   Name: {skill_name}
   Source: {file_path}
   Location(s):
     {FOR EACH cli IN targets}
     - .{cli}/skills/{skill_name}/SKILL.md
   
   Next steps:
   - Validate: /hefesto.validate {skill_name}
   - View: /hefesto.show {skill_name}
   - Test: Use the skill with your AI CLI
```

**Performance Target**: < 1s

---

### Phase 7: Collision Handling

```markdown
collision_gate():
  DISPLAY:
  ⚠️  Skill already exists: {skill_name}
  
  Existing location(s):
    {FOR EACH existing_path}
    - {existing_path}
  
  Actions:
  [overwrite] - Replace existing (creates backup)
  [rename]    - Choose different name
  [cancel]    - Abort operation
  
  INPUT: action
  
  CASE action:
    "overwrite":
      create_backup(existing_path)
      RETURN continue_with_overwrite
    
    "rename":
      PROMPT: "New skill name:"
      INPUT: new_name
      skill_name = sanitize_name(new_name)
      RETRY collision check
    
    "cancel":
      ABORT
```

**References**: FR-008, T0-HEFESTO-08

---

## Error Cases

| Code | Condition | Handler |
|------|-----------|---------|
| **E-EXTRACT-001** | File not found | Error + suggest similar files |
| **E-EXTRACT-002** | File not readable | Permission error + suggest chmod |
| **E-EXTRACT-003** | Unsupported file type | Warning + generic wrapper |
| **E-EXTRACT-004** | Skill name collision | Trigger collision Human Gate |
| **E-EXTRACT-005** | Code contains secrets | Reject + security warning (T0-HEFESTO-11) |
| **E-EXTRACT-006** | File too large (>100KB) | Warning + confirmation |
| **E-EXTRACT-007** | Empty file | Error + suggest non-empty file |

**Error Format**:
```
ERROR [E-EXTRACT-XXX]: {Description}
Suggestion: {Remediation}
Usage: /hefesto.extract [file_path] [--name <skill-name>]
```

---

## Usage Examples

### Example 1: Basic Extraction

```bash
> /hefesto.extract ./utils/email-validator.py

Analyzing code from ./utils/email-validator.py...
Detected: Python, No framework, Validation
Suggested name: email-validator

═══════════════════════════════════════════════════
✅ Skill Extracted: email-validator
═══════════════════════════════════════════════════

[Preview shown...]

Actions: [approve] [expand] [edit] [reject]
> approve

✅ Skill extracted successfully!

Name: email-validator
Source: ./utils/email-validator.py
Location(s):
  - .claude/skills/email-validator/SKILL.md
  - .gemini/skills/email-validator/SKILL.md
```

### Example 2: Wizard Mode

```bash
> /hefesto.extract

🧙 Wizard Mode: Extract Skill
═══════════════════════════════════════════════════

Path to code file:
> ./scripts/deploy.sh

Suggested name: deploy
Press Enter to accept, or type custom name:
> deploy-aws

Detected CLIs: claude, opencode
Target CLIs (comma-separated or 'all') [all]:
> [Enter]

[Proceeds to analysis and Human Gate...]
```

### Example 3: Custom Name

```bash
> /hefesto.extract ./legacy-validator.js --name modernized-validator

Analyzing code from ./legacy-validator.js...
Using custom name: modernized-validator

[Proceeds with specified name...]
```

### Example 4: Security Rejection

```bash
> /hefesto.extract ./deploy-with-keys.sh

Analyzing code...

❌ ERROR [E-EXTRACT-005]: Code contains potential secrets

Found in lines: 15, 23, 45
Detected patterns:
  - AWS_ACCESS_KEY (line 15)
  - API_TOKEN (line 23)
  - PASSWORD (line 45)

This violates T0-HEFESTO-11 (Security by Default)

Suggestion: Remove secrets, use environment variables
Usage: /hefesto.extract [file_path] [--name <skill-name>]

Operation aborted.
```

---

## Success Criteria

- ✅ **SC-001**: Command implemented
- ✅ **SC-003**: Human Gate enforced
- ✅ **SC-004**: Wizard mode for missing file_path
- ✅ **US-001 Scenario 2**: Code extraction

---

## Performance Targets

| Operation | Target | Typical |
|-----------|--------|---------|
| File read | < 100ms | 50ms |
| Code analysis | < 3s | 1s |
| Template generation | < 2s | 1s |
| Validation | < 500ms | 200ms |
| Human Gate wait | unbounded | N/A |
| Persistence | < 1s | 500ms |
| **Total (excl. Human Gate)** | **< 7s** | **~3s** |

---

## Dependencies

**Required Helpers:**
- `helpers/human-gate.md` - Approval workflow
- `helpers/template-validator.md` - T0 compliance
- `helpers/code-analyzer.md` - Language/framework detection
- `helpers/secret-detector.md` - Security scan

**Required Templates:**
- `templates/extract/SKILL.md.template`
- `templates/base/metadata.yaml.template`

**State Files:**
- `MEMORY.md` - Skill registry

---

## See Also

- **Related Commands**: `/hefesto.create`, `/hefesto.validate`, `/hefesto.show`
- **Specification**: `specs/003-hefesto-commands/contracts/extract.contract.md`
- **T0 Rules**: `CONSTITUTION.md` (T0-HEFESTO-02, 06, 11)
- **User Story**: `specs/003-hefesto-commands/spec.md` US1
