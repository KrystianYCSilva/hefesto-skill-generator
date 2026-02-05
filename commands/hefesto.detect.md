---
description: "CLI re-detection command to discover and add newly installed AI CLIs"
command: "/hefesto.detect"
category: "detection"
user_story: "US2"
priority: "P1"
version: "1.0.0"
---

# /hefesto.detect - CLI Re-Detection Command

**Command**: `/hefesto.detect`  
**Purpose**: Re-detect installed AI CLIs and add newly installed ones  
**User Story**: US2 - Detect Installed AI CLIs Automatically (P1)

---

## Overview

The `/hefesto.detect` command performs incremental CLI detection to discover newly installed CLIs after initial bootstrap:

1. Validates CONSTITUTION.md
2. Checks if Hefesto is initialized (MEMORY.md exists)
3. Runs CLI detection (reuses logic from `/hefesto.init`)
4. Identifies new CLIs vs. existing ones
5. Creates directories only for new CLIs
6. Updates MEMORY.md with new CLI entries
7. Generates detection report

**Target Performance**: < 2 seconds for detection phase

---

## Command Signature

```text
/hefesto.detect [--force] [--verbose] [--no-emoji]

Options:
  --force       Re-detect all CLIs (including already detected ones)
  --verbose     Show detailed detection logs
  --no-emoji    Disable emoji in output
```

---

## Execution Workflow

### Phase 0: Pre-Execution Validation

```markdown
1. Run CONSTITUTION validation
   (see: helpers/constitution-validator.md)
   IF invalid → Block execution

2. Check if Hefesto is initialized
   IF NOT file_exists("MEMORY.md"):
     DISPLAY: "❌ Hefesto not initialized. Run /hefesto.init first."
     ABORT (exit code 1)

3. Parse existing MEMORY.md
   existing_state = parse_memory_md("MEMORY.md")
   existing_clis = existing_state.detected_clis
   
   IF parse_fails:
     TRIGGER corrupted MEMORY.md recovery (ERR-002)
     existing_clis = []
```

**References**: FR-010, FR-018, constitution-validator.md, error-handling.md

---

### Phase 1: Re-Detection Logic

```markdown
START timer

1. Display: "🔍 Re-detecting AI CLIs..."

2. Run parallel CLI detection
   (REUSE detection logic from /hefesto.init)
   
   detected_clis = run_cli_detection()
   # Returns list of CLI Detection Results

3. Compare with existing state
   new_clis = []
   existing_clis_found = []
   
   FOR EACH detected IN detected_clis:
     IF detected.id IN existing_clis:
       existing_clis_found.append(detected)
       IF --force:
         # Update version/status if changed
         update_cli_entry(detected)
     ELSE:
       new_clis.append(detected)

4. Display comparison results
   IF new_clis.length > 0:
     DISPLAY: "✅ Found {new_clis.length} new CLI(s)"
     FOR EACH cli IN new_clis:
       DISPLAY: "  + {cli.display_name} (v{cli.version}) → {cli.skills_dir}"
   ELSE:
     DISPLAY: "ℹ️  No new CLIs detected"
   
   IF existing_clis_found.length > 0:
     DISPLAY: "ℹ️  {existing_clis_found.length} CLI(s) already configured"
```

**Performance Target**: < 2 seconds  
**References**: FR-018, cli-detection-strategy.md

---

### Phase 2: Incremental Addition

```markdown
IF new_clis.length == 0 AND NOT --force:
  DISPLAY: "No changes needed. All CLIs already detected."
  STOP timer
  EXIT (exit code 0)

1. Display: "📁 Creating directory structures for new CLIs..."

2. Create directories only for new CLIs
   successful_additions = []
   failed_additions = []
   
   FOR EACH cli IN new_clis:
     TRY:
       create_directory(cli.skills_directory_path)
       successful_additions.append(cli)
       DISPLAY: "✅ Created {cli.skills_directory_path}"
     CATCH PermissionError:
       failed_additions.append({
         cli: cli,
         error: "permission_denied",
         message: error.message
       })
       DISPLAY: "❌ Permission denied: {cli.skills_directory_path}"
       CONTINUE

3. Collect addition results
   success_count = successful_additions.length
   error_count = failed_additions.length
```

**Performance Target**: < 1 second  
**References**: FR-017, FR-018, platform-detection.md

---

### Phase 3: Detection Report

```markdown
1. Generate report showing new vs. existing
   
   report_sections:
     - New CLIs detected and added
     - Existing CLIs (unchanged)
     - Warnings (config-only CLIs, permission errors)
     - Errors (if any)

2. Display structured report
   
   ## CLI Detection Report
   
   **Operation**: re-detect
   **Date**: {timestamp}
   **Duration**: {duration}s
   
   ### New CLIs ({new_count})
   
   {IF new_count > 0}
   - {CLI Name} (v{version})
     - Detection: {method}
     - Skills Directory: {path}
     - Status: {status}
   {ELSE}
   No new CLIs detected
   {END IF}
   
   ### Existing CLIs ({existing_count})
   
   {FOR EACH existing_cli}
   - {CLI Name} (v{version}) → {path} [no changes]
   {END FOR}
   
   ### Warnings ({warning_count})
   
   {FOR EACH warning}
   - {warning_message}
   {END FOR}
   
   ### Errors ({error_count})
   
   {FOR EACH error}
   - {CLI Name}: {error_type}
     Details: {error_message}
     Fix: {fix_instructions}
   {END FOR}
```

**References**: FR-012, bootstrap-report-template.md

---

### Phase 4: Error Handling

```markdown
1. Handle permission errors gracefully
   
   FOR EACH failed_addition:
     LOG error with details (ERR-001)
     ADD to error report
     CONTINUE with next CLI
   
   # Do NOT abort - partial success allowed

2. Handle warnings
   
   FOR EACH cli WHERE status = "warning_no_path":
     WARNING: "{cli.name} config found but not in PATH"
     ADD to warning report

3. Display error summary
   
   IF error_count > 0:
     DISPLAY:
       ⚠️ Detection completed with {error_count} error(s)
       See "Errors" section above for details
```

**References**: FR-017, FR-024, error-handling.md (ERR-001)

---

### Phase 5: Warning Generation

```markdown
1. Identify config-only CLIs
   
   FOR EACH cli WHERE detection_method = "config_directory":
     IF status = "warning_no_path":
       warnings.append({
         cli: cli,
         type: "config_only",
         message: "{cli.name} config exists but executable not in PATH"
       })

2. Display warnings clearly
   
   ### Warnings
   
   - **{CLI Name}**: Config directory found but executable not in PATH
     - Config Location: {config_path}
     - Impact: Skills can be generated but may not work until CLI is reinstalled
     - Fix: Install {CLI Name} and ensure it's in PATH, then run /hefesto.detect
```

**References**: FR-025, Edge case clarification #5

---

### Phase 6: Manual Fallback

```markdown
IF detected_clis.length == 0 AND new_clis.length == 0:
  DISPLAY: "⚠️ No CLIs detected (new or existing)"
  
  PROMPT: "Would you like to manually specify a CLI? (y/n)"
  
  IF user = "y":
    DISPLAY CLI selection menu:
      1. Claude Code
      2. Gemini CLI
      3. OpenAI Codex
      4. VS Code/Copilot
      5. OpenCode
      6. Cursor
      7. Qwen Code
    
    user_selection = GET_INPUT()
    
    FOR EACH selected_cli:
      manual_cli = create_manual_cli_entry(selected_cli)
      new_clis.append(manual_cli)
    
    CONTINUE to Phase 2 (directory creation)
  ELSE:
    DISPLAY: "Detection aborted by user"
    EXIT (exit code 0)
```

**References**: FR-013, ERR-005

---

### Phase 7: State Update

```markdown
1. Update MEMORY.md with new CLI entries
   
   existing_memory = parse_memory_md("MEMORY.md")
   
   FOR EACH new_cli IN successful_additions:
     existing_memory.detected_clis.append({
       cli: new_cli.id,
       detection_method: new_cli.detection_method,
       skills_directory: new_cli.skills_directory_path,
       version: new_cli.version,
       status: new_cli.status
     })
   
   existing_memory.last_updated = current_timestamp()

2. Recalculate state metadata
   
   existing_memory.active_cli_count = COUNT(
     CLIs WHERE status = "active"
   )

3. Write updated MEMORY.md
   
   TRY:
     write_memory_md(existing_memory)
     DISPLAY: "✅ MEMORY.md updated with {new_clis.length} new CLI(s)"
   CATCH IOError:
     DISPLAY: "❌ Failed to update MEMORY.md"
     ABORT with error

4. Verify updated state
   
   TRY:
     validate_memory = parse_memory_md("MEMORY.md")
   CATCH ParseError:
     DISPLAY: "⚠️ Warning: MEMORY.md updated but validation failed"
```

**Performance Target**: < 100ms  
**References**: FR-027, memory-template.md, data-model.md

---

## Re-Detection Logic (Reuse from /hefesto.init)

### Shared Detection Function

```markdown
FUNCTION run_cli_detection():
  # This function is shared between /hefesto.init and /hefesto.detect
  
  detected_clis = []
  
  # Phase 1: PATH scanning (parallel)
  FOR EACH cli IN supported_clis:
    PARALLEL:
      IF command_exists(cli.executable):
        path = get_command_path(cli.executable)
        version = try_get_version(cli.executable)
        detected_clis.append({
          id: cli.id,
          name: cli.display_name,
          detection_method: "PATH",
          executable_path: path,
          version: version,
          skills_directory_path: ".{cli.id}/skills/",
          status: "active"
        })
  
  # Phase 2: Config directory scanning (parallel)
  FOR EACH cli IN (supported_clis WHERE NOT detected_via_path):
    PARALLEL:
      config_path = get_config_path(cli.id)
      IF directory_exists(config_path):
        detected_clis.append({
          id: cli.id,
          name: cli.display_name,
          detection_method: "config_directory",
          config_path: config_path,
          version: null,
          skills_directory_path: ".{cli.id}/skills/",
          status: "warning_no_path"
        })
  
  RETURN detected_clis
```

**References**: cli-detection-strategy.md

---

## Usage Examples

### Example 1: Detect New CLI

```text
> /hefesto.detect

🔍 Re-detecting AI CLIs...

✅ Found 1 new CLI:
  + Cursor (v1.0.5) → .cursor/skills/

ℹ️  3 CLIs already configured:
  - Claude Code
  - Gemini CLI
  - OpenCode

📁 Creating directory structures for new CLIs...
✅ Created .cursor/skills/

✅ MEMORY.md updated with 1 new CLI

## CLI Detection Report

**Operation**: re-detect
**Date**: 2026-02-04T15:00:00Z
**Duration**: 1.8s

### New CLIs (1)

- **Cursor** (v1.0.5)
  - Detection: PATH
  - Skills Directory: .cursor/skills/
  - Status: ✅ Active

### Existing CLIs (3)

- Claude Code (v1.2.0) → .claude/skills/ [no changes]
- Gemini CLI → .gemini/skills/ [no changes]
- OpenCode (v0.2.1) → .opencode/skills/ [no changes]

✅ Detection completed successfully
```

### Example 2: No New CLIs

```text
> /hefesto.detect

🔍 Re-detecting AI CLIs...

ℹ️  No new CLIs detected

ℹ️  3 CLIs already configured:
  - Claude Code
  - Gemini CLI  
  - OpenCode

No changes needed. All CLIs already detected.

Duration: 1.2s
```

### Example 3: Permission Error

```text
> /hefesto.detect

🔍 Re-detecting AI CLIs...

✅ Found 2 new CLIs:
  + Cursor (v1.0.5) → .cursor/skills/
  + Qwen Code (v0.1.0) → .qwen/skills/

📁 Creating directory structures for new CLIs...
✅ Created .cursor/skills/
❌ Permission denied: .qwen/skills/

⚠️ Detection completed with 1 error

## CLI Detection Report

### New CLIs (1 successful, 1 failed)

- **Cursor** (v1.0.5) → .cursor/skills/ ✅
- **Qwen Code** (v0.1.0) → .qwen/skills/ ❌

### Errors (1)

- **Qwen Code**: Permission denied
  Details: Cannot create directory .qwen/skills/
  Fix: Run `chmod +w .` or manually create: `mkdir -p .qwen/skills`

✅ MEMORY.md updated with 1 new CLI
```

### Example 4: Force Re-Detection

```text
> /hefesto.detect --force

🔍 Re-detecting AI CLIs (force mode)...

✅ Detected 4 CLIs:
  - Claude Code (v1.2.0) → .claude/skills/ [updated version: 1.1.0 → 1.2.0]
  - Gemini CLI → .gemini/skills/ [no changes]
  - OpenCode (v0.2.1) → .opencode/skills/ [no changes]
  - Cursor (v1.0.5) → .cursor/skills/ [NEW]

📁 Creating directory structures for new CLIs...
✅ Created .cursor/skills/

✅ MEMORY.md updated (1 new CLI, 1 version update)

Duration: 2.3s
```

---

## Error Scenarios

### ERR-001: Permission Denied

```text
❌ Permission denied: .qwen/skills/

Error: Cannot create directory
Reason: Parent directory is read-only

Fix:
1. Check permissions: ls -la . | grep .qwen
2. Fix permissions: chmod +w .qwen
3. Or manually create: mkdir -p .qwen/skills && chmod +w .qwen/skills
4. Then re-run: /hefesto.detect
```

**References**: error-handling.md (ERR-001)

### ERR-002: Corrupted MEMORY.md

```text
⚠️ State Recovery: MEMORY.md corrupted

Backup created: MEMORY.md.backup.2026-02-04T15-00-00Z
Rebuilt state from filesystem:
- Detected 3 CLI directories
- Found 5 skills

Continuing with CLI detection...
```

**References**: error-handling.md (ERR-002), FR-016

### Warning: Config-Only CLI

```text
### Warnings (1)

- **Gemini CLI**: Config directory found but executable not in PATH
  - Config Location: /Users/dev/.gemini/
  - Impact: Skills can be generated but may not work until Gemini CLI is reinstalled
  - Fix: Install Gemini CLI and ensure it's in PATH, then run /hefesto.detect
```

**References**: FR-025, Edge case clarification #5

---

## Performance Benchmarks

| Phase | Target | Typical |
|-------|--------|---------|
| CONSTITUTION validation (cached) | < 5ms | 2-5ms |
| MEMORY.md parsing | < 50ms | 20-30ms |
| CLI detection (7 CLIs parallel) | < 2s | 1-2s |
| Directory creation (per CLI) | < 100ms | 50-100ms |
| MEMORY.md update | < 100ms | 50-80ms |
| Report generation | < 200ms | 100-150ms |
| **Total Re-Detection** | **< 3s** | **1.5-2.5s** |

**References**: FR-008, performance goals from plan.md

---

## Testing

### Manual Testing (Quickstart Scenarios)

- **Test 2**: Multiple CLIs with mix of new/existing - quickstart.md
- **Test 3**: Permission error on one CLI - quickstart.md
- **Test 8**: Re-detection after installing new CLI - quickstart.md

### Validation Checks

```markdown
AFTER /hefesto.detect completes:

CHECK: MEMORY.md contains all new CLI entries
CHECK: New CLI directories exist on filesystem
CHECK: Existing CLIs remain unchanged (unless --force)
CHECK: Execution time < 3 seconds
CHECK: Partial success on permission errors
CHECK: Warnings displayed for config-only CLIs
```

---

## Integration with /hefesto.init

### Shared Components

Both commands share:
- CLI detection logic (`run_cli_detection()`)
- Directory creation logic
- Error handling patterns
- Report generation templates

### Key Differences

| Aspect | /hefesto.init | /hefesto.detect |
|--------|--------------|-----------------|
| **Precondition** | No MEMORY.md | MEMORY.md exists |
| **Behavior** | Initialize all detected CLIs | Add only new CLIs |
| **MEMORY.md** | Create new | Update existing |
| **Idempotency** | Reports "already initialized" | Always runs detection |
| **Use Case** | First-time setup | Post-installation detection |

---

## References

- **Specification**: specs/001-hefesto-foundation/spec.md (User Story 2)
- **Plan**: specs/001-hefesto-foundation/plan.md
- **Data Model**: specs/001-hefesto-foundation/data-model.md (CLI Detection Result)
- **Helpers**:
  - `helpers/cli-detection-strategy.md`
  - `helpers/error-handling.md`
  - `helpers/constitution-validator.md`
  - `helpers/platform-detection.md`
- **Templates**:
  - `templates/memory-template.md`
  - `templates/bootstrap-report-template.md`
- **Related Commands**:
  - `hefesto.init.md` (shares detection logic)
- **Requirements**: FR-001, FR-012, FR-013, FR-017, FR-018, FR-025
- **Success Criteria**: SC-002 (100% CLI detection accuracy)
