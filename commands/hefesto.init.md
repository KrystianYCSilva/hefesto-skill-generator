---
description: "Bootstrap command to initialize Hefesto Foundation Infrastructure in a project"
command: "/hefesto.init"
category: "initialization"
user_story: "US1"
priority: "P1"
version: "1.0.0"
---

# /hefesto.init - Bootstrap Command

**Command**: `/hefesto.init`
**Purpose**: Initialize Hefesto Foundation Infrastructure in a project
**User Story**: US1 - Bootstrap Hefesto in Existing Project (P1)

---

## Overview

The `/hefesto.init` command performs the complete bootstrap process for Hefesto:

1. Validates CONSTITUTION.md (auto-restore if missing)
2. Detects installed AI CLIs (PATH + config directories)
3. Creates skill directory structures for detected CLIs
4. Initializes MEMORY.md with project state
5. Generates bootstrap report

**Target Performance**: < 5 seconds total execution time

---

## Command Signature

```text
/hefesto.init [--force] [--verbose] [--no-emoji]

Options:
  --force       Re-run bootstrap even if already initialized (re-detect CLIs)
  --verbose     Show detailed detection logs
  --no-emoji    Disable emoji in output (for terminals without Unicode support)
```

---

## Execution Workflow

### Phase 0: Pre-Execution Validation

```markdown
1. Run CONSTITUTION validation (see: helpers/constitution-validator.md)
   - If missing → Auto-restore from bundle
   - If invalid → Block execution with ERR-004
   - If valid → Continue

2. Check if already initialized
   IF MEMORY.md exists AND --force NOT provided:
     READ existing state
     DISPLAY: "Hefesto already initialized. Use --force to re-initialize."
     ABORT (exit code 0)
```

**References**: FR-010, constitution-validator.md

---

### Phase 1: CLI Detection

```markdown
START timer

1. Display: "🔍 Detecting installed AI CLIs..."

2. Run parallel PATH detection (see: helpers/cli-detection-strategy.md)
   FOR EACH cli IN supported_clis (7 CLIs):
     PARALLEL:
       path_result = check_command_in_path(cli.executable)
       IF path_result.found:
         version = try_get_version(cli.executable)
         RECORD(cli.id, "PATH", path_result.path, version, "active")

3. Run parallel config directory detection
   FOR EACH cli IN (supported_clis WHERE NOT detected_via_path):
     PARALLEL:
       config_path = get_config_path(cli.id)
       IF directory_exists(config_path):
         RECORD(cli.id, "config_directory", config_path, null, "warning_no_path")

4. Check if any CLIs detected
   IF detected_count == 0:
     PROMPT manual specification (ERR-005)
     FOR EACH user_selected_cli:
       RECORD(cli.id, "manual", ".{cli.id}/skills/", null, "manual")

5. Display detection results
   ✅ Detected {count} CLIs:
   - {CLI Name} (v{version}) → {skills_dir}
   - {CLI Name} (config only, ⚠️ not in PATH) → {skills_dir}
```

**Performance Target**: < 2 seconds
**References**: FR-001, FR-006, FR-012, FR-013, cli-detection-strategy.md

---

### Phase 2: Directory Creation

```markdown
1. Display: "📁 Creating directory structures..."

2. Create skill directories for each detected CLI
   FOR EACH detected_cli:
     TRY:
       create_directory(detected_cli.skills_directory_path)
       DISPLAY: "✅ Created {skills_directory_path}"
     CATCH PermissionError:
       LOG error (ERR-001)
       RECORD(cli.id, ..., status="error_permission")
       DISPLAY: "❌ Permission denied: {skills_directory_path}"
       CONTINUE to next CLI

3. Collect creation results
   successful_count = COUNT(CLIs WHERE status IN ["active", "warning_no_path", "manual"])
   error_count = COUNT(CLIs WHERE status = "error_permission")
```

**Performance Target**: < 1 second
**References**: FR-002, FR-009, FR-014, FR-017, platform-detection.md

---

### Phase 3: State Initialization

```markdown
1. Display: "📄 Initializing MEMORY.md..."

2. Generate MEMORY.md from template (see: templates/memory-template.md)

   frontmatter:
     hefesto_version: "{current_version}"
     initialized: "{current_timestamp_iso8601}"
     last_updated: "{current_timestamp_iso8601}"

   detected_clis_table:
     FOR EACH detected_cli:
       | {cli.id} | {cli.detection_method} | {cli.skills_dir} | {cli.version} | {cli.status} |

   skill_registry_table:
     (empty - no skills generated yet)

   state_metadata:
     Total Skills: 0
     Active CLIs: {count_active}
     Last Validation: {current_timestamp_iso8601}

3. Write MEMORY.md to project root
   TRY:
     write_file("MEMORY.md", memory_content)
     DISPLAY: "✅ State file created"
   CATCH IOError:
     ABORT with error message (disk full, permission denied)

4. Verify MEMORY.md readable
   TRY:
     parse_memory_md("MEMORY.md")
   CATCH ParseError:
     LOG: "Warning: MEMORY.md created but failed validation"
```

**Performance Target**: < 100ms
**References**: FR-004, FR-011, memory-template.md, data-model.md

---

### Phase 4: Report Generation

```markdown
STOP timer
duration = timer.elapsed_seconds()

1. Display: "📜 Generating bootstrap report..."

2. Generate report (see: templates/bootstrap-report-template.md)

   report = generate_bootstrap_report({
     operation: "init",
     timestamp: current_timestamp,
     duration: duration,
     detected_clis: detected_clis_list,
     successful_count: successful_count,
     error_count: error_count,
     warnings: warnings_list,
     created_directories: created_dirs_list
   })

3. Display full report to user

4. Display summary
   IF error_count == 0 AND warning_count == 0:
     DISPLAY: "✅ Bootstrap completed in {duration}s"
   ELIF error_count > 0:
     DISPLAY: "⚠️ Bootstrap completed with {error_count} errors in {duration}s"
   ELSE:
     DISPLAY: "⚠️ Bootstrap completed with {warning_count} warnings in {duration}s"
```

**Performance Target**: < 500ms
**References**: FR-012, bootstrap-report-template.md

---

## CLI Detection Logic

### Supported CLIs

| CLI ID | Display Name | PATH Command | Config Directory |
|--------|-------------|--------------|------------------|
| `claude` | Claude Code | `claude` | `~/.claude/` |
| `gemini` | Gemini CLI | `gemini` | `~/.gemini/` |
| `codex` | OpenAI Codex | `codex` | `~/.codex/` |
| `copilot` | VS Code/Copilot | `code` + extension check | `~/.vscode/` or `~/.github/` |
| `opencode` | OpenCode | `opencode` | `~/.opencode/` |
| `cursor` | Cursor | `cursor` | `~/.cursor/` |
| `qwen` | Qwen Code | `qwen` | `~/.qwen/` |

### Detection Priority

1. **PRIMARY**: PATH environment variable (highest reliability)
2. **SECONDARY**: Config directory existence (medium reliability)
3. **FALLBACK**: Manual user specification (explicit)

### Platform-Specific Detection

**Windows (PowerShell)**:
```powershell
# PATH check
where.exe claude 2>$null
if ($?) {
  $version = claude --version 2>$null | Select-String -Pattern '\d+\.\d+\.\d+' | ForEach-Object { $_.Matches.Value }
  Write-Output "DETECTED:PATH:$version"
}

# Config check
if (Test-Path "$Env:USERPROFILE\.claude") {
  Write-Output "DETECTED:CONFIG"
}
```

**Unix/macOS (Bash/Zsh)**:
```bash
# PATH check
if command -v claude &> /dev/null; then
  version=$(claude --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
  echo "DETECTED:PATH:$version"
fi

# Config check
if [ -d "$HOME/.claude" ]; then
  echo "DETECTED:CONFIG"
fi
```

---

## Directory Creation

### Directory Structure

For each detected CLI with ID `{cli-id}`, create:

```text
.{cli-id}/
└── skills/          # Initially empty directory
```

**Examples**:
- `.claude/skills/`
- `.gemini/skills/`
- `.opencode/skills/`

### Idempotency

```markdown
IF directory already exists:
  LOG: "Directory {path} already exists, skipping creation"
  VERIFY directory is writable
  IF NOT writable:
    RECORD status="error_permission"
  CONTINUE
```

### Permissions

- **Unix/macOS**: Inherit parent directory permissions (typically `drwxr-xr-x`)
- **Windows**: Current user read/write (default for `New-Item`)

**Verification**:
```markdown
AFTER creating directory:
  TRY:
    write_test_file("{skills_dir}/.hefesto-test")
    delete_file("{skills_dir}/.hefesto-test")
    RECORD status="active" or "warning_no_path"
  CATCH PermissionError:
    RECORD status="error_permission"
```

---

## State Initialization

### MEMORY.md Format

```markdown
---
hefesto_version: "1.0.0"
initialized: 2026-02-04T14:30:00Z
last_updated: 2026-02-04T14:30:00Z
---

# Hefesto Project State

## Detected CLIs

| CLI | Detection Method | Skills Directory | Version | Status |
|-----|------------------|------------------|---------|--------|
| claude | PATH | .claude/skills/ | 1.2.0 | active |
| gemini | config_directory | .gemini/skills/ | null | warning_no_path |
| opencode | PATH | .opencode/skills/ | 0.2.1 | active |

## Skill Registry

| Skill Name | CLIs | Created | Last Modified |
|------------|------|---------|---------------|

## State Metadata

- **Total Skills**: 0
- **Active CLIs**: 3
- **Last Validation**: 2026-02-04T14:30:00Z
```

**References**: memory-template.md, data-model.md (Project State entity)

---

## Constitution Setup

### Validation Process

```markdown
1. Check if CONSTITUTION.md exists at project root
   IF NOT exists:
     DISPLAY: "⚠️ CONSTITUTION.md missing, restoring from bundle..."
     COPY bundled CONSTITUTION.md to project root
     DISPLAY: "✅ Constitution restored (v{version})"

2. Validate CONSTITUTION.md structure
   (see: helpers/constitution-validator.md)

   IF validation fails:
     DISPLAY: "❌ CONSTITUTION.md invalid"
     ABORT with ERR-004

3. Extract and verify T0 rules
   REQUIRED_RULES = [
     "T0-HEFESTO-01", "T0-HEFESTO-02", ..., "T0-HEFESTO-11"
   ]

   FOR EACH rule_id:
     IF NOT constitution_contains(rule_id):
       ABORT with ERR-004 (missing T0 rule)

4. Display validation result
   DISPLAY: "✅ Constitution validated (v{version}, {rule_count} T0 rules)"
```

**References**: FR-003, FR-010, constitution-validator.md

---

## Report Generation

### Report Sections

1. **Summary**: Success/warning/error counts, duration
2. **Detected CLIs**: Organized by detection method and status
3. **Errors**: Detailed error messages with fix instructions
4. **Created Directories**: List of paths and sizes
5. **Next Steps**: Actionable recommendations
6. **State Persisted**: Confirmation of MEMORY.md and CONSTITUTION.md

**Template**: `templates/bootstrap-report-template.md`

### Error Reporting

```markdown
IF errors occurred:
  FOR EACH error:
    DISPLAY:
      ❌ {CLI Name}: {error_type}
         Details: {error_message}
         Fix: {fix_instructions}
```

---

## Usage Examples

### Example 1: First-Time Bootstrap

```text
> /hefesto.init

🔍 Detecting installed AI CLIs...
✅ Detected 3 CLIs:
- Claude Code (v1.2.0) → .claude/skills/
- Gemini CLI (config only, ⚠️ not in PATH) → .gemini/skills/
- OpenCode (v0.2.1) → .opencode/skills/

📁 Creating directory structures...
✅ Created .claude/skills/
✅ Created .gemini/skills/
✅ Created .opencode/skills/

📄 Initializing MEMORY.md...
✅ State file created

📜 Verifying CONSTITUTION.md...
✅ Constitution validated (v1.1.0, 11 T0 rules)

✅ Bootstrap completed in 3.2 seconds

Next Steps:
1. Run `/hefesto.list` to verify initialization
2. Run `/hefesto.create` to generate your first skill
```

### Example 2: Re-Bootstrap with --force

```text
> /hefesto.init --force

⚠️ Hefesto already initialized, re-running detection...

🔍 Detecting installed AI CLIs...
✅ Detected 4 CLIs (1 new):
- Claude Code (v1.2.0) → .claude/skills/ [existing]
- Gemini CLI (config only) → .gemini/skills/ [existing]
- OpenCode (v0.2.1) → .opencode/skills/ [existing]
- Cursor (v1.0.5) → .cursor/skills/ [NEW]

📁 Creating directory structures...
✅ Created .cursor/skills/

📄 Updating MEMORY.md...
✅ Added 1 new CLI to state

✅ Re-bootstrap completed in 2.1 seconds
```

### Example 3: No CLIs Detected

```text
> /hefesto.init

🔍 Detecting installed AI CLIs...
⚠️ No AI CLIs detected automatically

Which AI CLI do you use? (Select numbers, comma-separated)
1. Claude Code
2. Gemini CLI
3. OpenAI Codex
4. VS Code/Copilot
5. OpenCode
6. Cursor
7. Qwen Code

Enter selection: 1,5

✅ Manual specification: Claude Code, OpenCode

📁 Creating directory structures...
✅ Created .claude/skills/
✅ Created .opencode/skills/

📄 Initializing MEMORY.md...
✅ State file created

✅ Bootstrap completed in 1.8 seconds
```

---

## Error Scenarios

### ERR-001: Permission Denied

```text
📁 Creating directory structures...
✅ Created .claude/skills/
❌ Permission denied: .github/skills/
✅ Created .opencode/skills/

⚠️ Bootstrap completed with 1 error in 2.5 seconds

Errors:
- VS Code/Copilot: Cannot create .github/skills/ (permission denied)
  Fix: Run `chmod +w .github` or manually create directory
```

### ERR-003: Missing CONSTITUTION.md

```text
📜 Verifying CONSTITUTION.md...
⚠️ CONSTITUTION.md missing, restoring from bundle...
✅ Constitution restored (v1.1.0)
✅ Bootstrap completed in 3.5 seconds
```

### ERR-004: Invalid CONSTITUTION.md

```text
📜 Verifying CONSTITUTION.md...
❌ CONSTITUTION.md invalid: Missing T0 rules

Missing rules: T0-HEFESTO-01, T0-HEFESTO-03

Action Required:
1. Review CONSTITUTION.md for unauthorized changes
2. Restore from backup: git restore CONSTITUTION.md
3. Or force restore: /hefesto.restore-constitution

Bootstrap aborted.
```

---

## Performance Benchmarks

| Phase | Target | Typical |
|-------|--------|---------|
| CONSTITUTION validation | < 500ms | 200-300ms |
| CLI detection (7 CLIs parallel) | < 2s | 1-2s |
| Directory creation (3 CLIs) | < 1s | 100-500ms |
| MEMORY.md initialization | < 100ms | 50-80ms |
| Report generation | < 500ms | 100-200ms |
| **Total Bootstrap** | **< 5s** | **2-4s** |

**References**: FR-008, SC-001

---

## Implementation

The implementation of `/hefesto.init` is contained in the Python script `hefesto_init_impl.py` which handles all phases of the initialization process:

1. **Constitution Validation**: Ensures CONSTITUTION.md exists and contains all required T0 rules
2. **Initialization Check**: Verifies if Hefesto is already initialized (unless --force is used)
3. **CLI Detection**: Scans PATH and config directories to detect installed AI CLIs
4. **Directory Creation**: Creates skill directories for each detected CLI
5. **State Initialization**: Generates and writes MEMORY.md with detected CLIs
6. **Report Generation**: Produces a comprehensive bootstrap report

The script follows all specified requirements and performance targets, with proper error handling and user feedback.

---

## Testing

### Manual Testing (Quickstart Scenarios)

- **Test 1**: Successful bootstrap (happy path) - quickstart.md
- **Test 4**: No CLIs detected (manual fallback) - quickstart.md
- **Test 5**: Idempotent bootstrap (run twice) - quickstart.md

### Validation Checks

```markdown
AFTER /hefesto.init completes:

CHECK: MEMORY.md exists and is parseable
CHECK: All detected CLIs have corresponding directories
CHECK: CONSTITUTION.md exists and is valid
CHECK: Execution time < 5 seconds (or < 10 seconds including user read time)
CHECK: Re-running /hefesto.init reports "already initialized"
```

---

## References

- **Specification**: specs/001-hefesto-foundation/spec.md (User Story 1)
- **Plan**: specs/001-hefesto-foundation/plan.md
- **Data Model**: specs/001-hefesto-foundation/data-model.md (Project State, CLI Detection Result)
- **Helpers**:
  - `helpers/cli-detection-strategy.md`
  - `helpers/error-handling.md`
  - `helpers/constitution-validator.md`
  - `helpers/platform-detection.md`
- **Templates**:
  - `templates/memory-template.md`
  - `templates/bootstrap-report-template.md`
- **Requirements**: FR-001, FR-002, FR-003, FR-004, FR-008, FR-009, FR-010
- **Success Criteria**: SC-001, SC-003, SC-008, SC-009
