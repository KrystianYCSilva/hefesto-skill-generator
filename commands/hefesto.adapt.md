---
description: "Adapt existing skill from one CLI to another with syntax transformations"
command: "/hefesto.adapt"
category: "skill-management"
user_story: "US3"
priority: "P2"
version: "1.0.0"
---

# /hefesto.adapt - Adapt Skill Command

**Command**: `/hefesto.adapt`  
**Purpose**: Adapt existing skill from one CLI to another  
**User Story**: US3 - Adaptation & Sync (P2)

---

## Overview

The `/hefesto.adapt` command transforms skills between different AI CLIs with syntax/format adaptations. Features:

1. **Wizard Mode**: Interactive prompts for source/target selection
2. **Syntax Translation**: Auto-convert CLI-specific patterns (e.g., `$ARGUMENTS` → `{{args}}`)
3. **Human Gate**: Mandatory approval before persistence (T0-HEFESTO-02)
4. **Diff Preview**: Show transformations before applying
5. **Validation**: Ensure target skill complies with T0 rules

**Target Performance**: < 4s (excluding Human Gate wait)

---

## Command Signature

```text
/hefesto.adapt <skill_name> --target <cli> [--source <cli>] [--force]

Arguments:
  skill_name     Name of skill to adapt (required)

Options:
  --target <cli>     Target CLI (required)
                     Values: claude, gemini, codex, copilot, opencode, cursor, qwen
  --source <cli>     Source CLI (optional, auto-detected if only one exists)
  --force            Skip Human Gate (DANGEROUS - not recommended)
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

3. Load CLI detection
   detected_clis = read_memory_md().detected_clis
   IF detected_clis IS empty:
     ERROR E-ADAPT-002: "No CLIs detected"
     SUGGEST: "Run /hefesto.detect"
     ABORT
```

**Performance Target**: < 200ms

---

### Phase 1: Argument Parsing & Validation

```markdown
1. Parse arguments
   skill_name = args.positional[0] OR null
   target_cli = args.flags.get("target") OR null
   source_cli = args.flags.get("source") OR null
   force = args.flags.get("force") OR false

2. Validate required arguments
   IF skill_name IS null:
     ERROR: "Missing required argument: skill_name"
     SUGGEST: "Usage: /hefesto.adapt <skill_name> --target <cli>"
     ABORT
   
   IF target_cli IS null:
     ERROR: "Missing required flag: --target"
     SUGGEST: "Specify target CLI: --target gemini"
     ABORT

3. Validate target CLI
   IF target_cli NOT IN detected_clis:
     ERROR E-ADAPT-002: "Target CLI not detected: {target_cli}"
     SUGGEST: "Run /hefesto.detect or use: {list(detected_clis)}"
     ABORT

4. Check adapter availability
   adapter_path = "helpers/cli-adapters/{target_cli}.md"
   IF NOT file_exists(adapter_path):
     ERROR E-ADAPT-003: "Adapter not available for: {target_cli}"
     SUGGEST: "Supported targets: {list_available_adapters()}"
     ABORT
```

**References**: FR-010

---

### Phase 2: Source Detection

```markdown
1. Find source skill
   IF source_cli IS provided:
     source_path = ".{source_cli}/skills/{skill_name}/SKILL.md"
     IF NOT file_exists(source_path):
       ERROR E-ADAPT-001: "Source skill not found: {source_path}"
       ABORT
   
   ELSE:
     # Auto-detect source
     found_sources = []
     FOR EACH cli IN detected_clis:
       skill_path = ".{cli}/skills/{skill_name}/SKILL.md"
       IF file_exists(skill_path):
         found_sources.append({cli: cli, path: skill_path})
     
     IF count(found_sources) == 0:
       ERROR E-ADAPT-001: "Skill not found: {skill_name}"
       SUGGEST: "Available skills: {list_all_skills()}"
       ABORT
     
     ELIF count(found_sources) > 1:
       ERROR E-ADAPT-006: "Skill exists in multiple CLIs"
       DISPLAY: "Found in:"
       FOR EACH source IN found_sources:
         DISPLAY: "  - {source.cli}: {source.path}"
       SUGGEST: "Specify source: --source <cli>"
       ABORT
     
     ELSE:
       source_cli = found_sources[0].cli
       source_path = found_sources[0].path

2. Load source skill
   TRY:
     source_content = read_file(source_path)
     source_metadata = read_file(dirname(source_path) + "/metadata.yaml")
   CATCH IOError:
     ERROR: "Cannot read source skill"
     ABORT
```

**Performance Target**: < 200ms  
**References**: FR-010

---

### Phase 3: Collision Detection

```markdown
1. Check if target skill exists
   target_path = ".{target_cli}/skills/{skill_name}/SKILL.md"
   
   IF file_exists(target_path):
     TRIGGER collision_gate()  # FR-008
```

**References**: T0-HEFESTO-08, FR-008

---

### Phase 4: Transformation

```markdown
1. Load adapter
   (see: helpers/cli-adapters/{target_cli}.md)
   adapter = load_adapter(target_cli)

2. Apply transformations
   transformed_content = adapter.transform(source_content, {
     source_cli: source_cli,
     target_cli: target_cli,
     skill_name: skill_name
   })

3. CLI-Specific Adaptations
   
   # Gemini/Qwen
   IF target_cli IN ["gemini", "qwen"]:
     transformed_content = replace(
       transformed_content,
       pattern: r'\$ARGUMENTS',
       replacement: '{{args}}'
     )
     
     IF supports_toml(target_cli):
       toml_variant = generate_toml(transformed_content)
   
   # Codex
   IF target_cli == "codex":
     # Preserve $ARGUMENTS syntax
     # Adjust context window hints
     transformed_content = adjust_context_hints(transformed_content)
   
   # Copilot
   IF target_cli == "copilot":
     # Add GitHub-specific metadata
     metadata = add_github_metadata(metadata)
     # Adjust directory structure for .github/skills/
   
   # OpenCode
   IF target_cli == "opencode":
     # Verify CLI compatibility
     transformed_content = ensure_cli_compatibility(transformed_content)
   
   # Cursor
   IF target_cli == "cursor":
     # Cursor-specific optimizations
     transformed_content = optimize_for_cursor(transformed_content)

4. Update metadata
   adapted_metadata = source_metadata.copy()
   adapted_metadata.update({
     adapted_from: source_cli,
     adapted_date: current_timestamp(),
     target_cli: target_cli
   })

5. Generate diff
   diff = compute_diff(source_content, transformed_content)
```

**Performance Target**: < 2s  
**References**: T0-HEFESTO-09

---

### Phase 5: Validation

```markdown
1. Validate transformed skill
   (see: helpers/template-validator.md)
   
   validation_errors = validate_skill(transformed_content)
   
   IF validation_errors NOT empty:
     ERROR E-ADAPT-005: "Transformation failed validation"
     DISPLAY: "Validation errors:"
     FOR EACH error IN validation_errors:
       DISPLAY: "  - {error.code}: {error.message}"
     ABORT (do not proceed to Human Gate)
```

**Performance Target**: < 500ms  
**References**: T0-HEFESTO-06

---

### Phase 6: Human Gate

```markdown
1. Check force flag
   IF force:
     WARN: "⚠️  Force flag enabled - skipping Human Gate"
     WARN: "This is DANGEROUS and not recommended"
     PROCEED to Phase 7
   
2. Display preview
   (see: helpers/human-gate.md)
   
   DISPLAY:
   ═══════════════════════════════════════════════════
   ✅ Skill Adapted: {skill_name}
   ═══════════════════════════════════════════════════
   
   Source: {source_cli}
   Target: {target_cli}
   
   Transformations Applied:
   -----------------------------------------
   {FOR EACH transform IN adapter.transforms_applied}
   - {transform.description}
   
   Diff Preview:
   -----------------------------------------
   {diff_summary}
   
   [Show first 20 lines of changes...]
   
   -----------------------------------------
   
   Validation: PASS ✅
   
   Files to create:
   - .{target_cli}/skills/{skill_name}/SKILL.md
   - .{target_cli}/skills/{skill_name}/metadata.yaml
   {IF scripts exist}
   - .{target_cli}/skills/{skill_name}/scripts/... (copied)
   
   ═══════════════════════════════════════════════════

3. Prompt for approval
   PROMPT: "Actions: [approve] [expand] [edit] [reject]"
   
   INPUT: action
   
   CASE action:
     "approve" → PROCEED to Phase 7
     "expand"  → DISPLAY full diff, re-prompt
     "edit"    → Allow edits, re-validate
     "reject"  → ABORT "Operation cancelled"
     timeout   → ABORT after 120s
```

**References**: T0-HEFESTO-02, FR-002

---

### Phase 7: Persistence

```markdown
1. Create target directory
   target_dir = ".{target_cli}/skills/{skill_name}/"
   TRY:
     create_directory(target_dir)
   CATCH PermissionError:
     ERROR E-ADAPT-007: "Write permission denied"
     ABORT

2. Write adapted skill
   target_skill_path = "{target_dir}/SKILL.md"
   target_metadata_path = "{target_dir}/metadata.yaml"
   
   write_file(target_skill_path, transformed_content)
   write_file(target_metadata_path, adapted_metadata)

3. Copy scripts if exist
   source_scripts = "{dirname(source_path)}/scripts"
   IF directory_exists(source_scripts):
     target_scripts = "{target_dir}/scripts"
     copy_directory(source_scripts, target_scripts)
     
     # Preserve executable permissions
     FOR EACH script IN list_files(target_scripts):
       IF was_executable(source_scripts + script):
         set_executable(target_scripts + script)

4. Update MEMORY.md
   state = read_memory_md()
   
   # Check if skill already tracked
   existing = find_skill(state, skill_name)
   IF existing:
     existing.clis.append(target_cli)
   ELSE:
     state.skills_created.append({
       name: skill_name,
       created: current_timestamp(),
       adapted_from: source_cli,
       clis: [target_cli],
       status: "active"
     })
   
   write_memory_md(state)

5. Success message
   DISPLAY:
   ✅ Skill adapted successfully!
   
   Name: {skill_name}
   Source: {source_cli}
   Target: {target_cli}
   Location: .{target_cli}/skills/{skill_name}/SKILL.md
   
   Transformations applied: {count(transforms)}
   
   Next steps:
   - Validate: /hefesto.validate {skill_name} --cli {target_cli}
   - View: /hefesto.show {skill_name} --cli {target_cli}
   - Test: Use with {target_cli}
```

**Performance Target**: < 1s

---

### Phase 8: Collision Handling

```markdown
collision_gate():
  DISPLAY:
  ⚠️  Skill already exists in target CLI: {skill_name}
  
  Existing location:
    .{target_cli}/skills/{skill_name}/
  
  Created: {existing_metadata.created}
  Last modified: {file_mtime}
  
  Actions:
  [overwrite] - Replace existing (creates backup)
  [rename]    - Choose different name
  [cancel]    - Abort operation
  
  INPUT: action
  
  CASE action:
    "overwrite":
      backup_path = ".hefesto/backups/{skill_name}-{target_cli}-{timestamp}.tar.gz"
      create_backup(target_path, backup_path)
      DISPLAY: "Backup created: {backup_path}"
      RETURN continue_with_overwrite
    
    "rename":
      PROMPT: "New skill name:"
      INPUT: new_name
      skill_name = sanitize_name(new_name)
      RETRY collision check
    
    "cancel":
      ABORT "Operation cancelled"
```

**References**: FR-008, T0-HEFESTO-08

---

## Error Cases

| Code | Condition | Handler |
|------|-----------|---------|
| **E-ADAPT-001** | Source skill not found | Error + list available |
| **E-ADAPT-002** | Target CLI not detected | Error + suggest `/hefesto.detect` |
| **E-ADAPT-003** | Adapter not available | Error + list supported targets |
| **E-ADAPT-004** | Target skill exists | Collision Human Gate |
| **E-ADAPT-005** | Transformation fails validation | Show errors + block |
| **E-ADAPT-006** | Source in multiple CLIs | Require explicit `--source` |
| **E-ADAPT-007** | Write permission denied | Error with path |

---

## Usage Examples

### Example 1: Basic Adaptation

```bash
> /hefesto.adapt email-validator --target gemini

Adapting email-validator from claude to gemini...

Applying transformations:
  - Convert $ARGUMENTS → {{args}}
  - Adjust CLI-specific syntax

═══════════════════════════════════════════════════
✅ Skill Adapted: email-validator
═══════════════════════════════════════════════════

[Preview shown...]

Actions: [approve] [expand] [edit] [reject]
> approve

✅ Skill adapted successfully!

Name: email-validator
Source: claude
Target: gemini
Location: .gemini/skills/email-validator/SKILL.md
```

### Example 2: Explicit Source

```bash
> /hefesto.adapt testing-strategy --source claude --target copilot

Adapting testing-strategy from claude to copilot...

Applying transformations:
  - Add GitHub-specific metadata
  - Adjust directory structure for .github/skills/

[Proceeds...]
```

### Example 3: Collision Handling

```bash
> /hefesto.adapt deploy-aws --target cursor

Adapting deploy-aws from gemini to cursor...

⚠️  Skill already exists in target CLI: deploy-aws

Existing location:
  .cursor/skills/deploy-aws/

Created: 2026-02-01 14:00:00
Last modified: 2026-02-03 10:30:00

Actions:
[overwrite] - Replace existing (creates backup)
[rename]    - Choose different name
[cancel]    - Abort operation

> overwrite

Backup created: .hefesto/backups/deploy-aws-cursor-20260204-103000.tar.gz

✅ Skill adapted successfully!
```

### Example 4: Multiple Source Error

```bash
> /hefesto.adapt api-wrapper --target opencode

❌ ERROR [E-ADAPT-006]: Skill exists in multiple CLIs

Found in:
  - claude: .claude/skills/api-wrapper/SKILL.md
  - gemini: .gemini/skills/api-wrapper/SKILL.md

Suggestion: Specify source: --source <cli>
Usage: /hefesto.adapt <skill_name> --target <cli> [--source <cli>]
```

---

## Adaptation Rules

### Gemini/Qwen
- Transform `$ARGUMENTS` → `{{args}}`
- Generate TOML variant if supported

### Codex
- Preserve `$ARGUMENTS` syntax
- Adjust context window hints

### Copilot
- Add GitHub-specific metadata
- Transform to `.github/skills/` structure

### OpenCode/Cursor
- Verify CLI compatibility
- Apply CLI-specific optimizations

---

## Success Criteria

- ✅ **SC-001**: Command implemented
- ✅ **SC-003**: Human Gate enforced
- ✅ **US-003 Scenario 1**: CLI adaptation

---

## Performance Targets

| Operation | Target | Typical |
|-----------|--------|---------|
| Source load | < 200ms | 100ms |
| Transformation | < 2s | 1s |
| Validation | < 500ms | 200ms |
| Human Gate wait | unbounded | N/A |
| Persistence | < 1s | 500ms |
| **Total (excl. Human Gate)** | **< 4s** | **~2s** |

---

## Dependencies

**Required Helpers:**
- `helpers/human-gate.md` - Approval workflow
- `helpers/template-validator.md` - Post-adapt validation
- `helpers/cli-adapters/<target>.md` - Transformation rules

**State Files:**
- `MEMORY.md` - CLI detection and skill registry

---

## See Also

- **Related Commands**: `/hefesto.sync`, `/hefesto.create`, `/hefesto.validate`
- **Specification**: `specs/003-hefesto-commands/contracts/adapt.contract.md`
- **T0 Rules**: `CONSTITUTION.md` (T0-HEFESTO-02, 08, 09)
- **User Story**: `specs/003-hefesto-commands/spec.md` US3
