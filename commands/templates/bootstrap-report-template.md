---
description: "Standard format template for reporting bootstrap and detection operation results"
category: "template"
type: "report"
used_by: ["/hefesto.init", "/hefesto.detect"]
format: "Markdown"
version: "1.0.0"
---

# Bootstrap Report Template

**Purpose**: Standard format for reporting bootstrap operation results  
**Used by**: `/hefesto.init`, `/hefesto.detect`

---

## Template Structure

```markdown
# Hefesto Bootstrap Report

**Operation**: {init | re-detect}
**Date**: {ISO8601_TIMESTAMP}
**Duration**: {seconds}s

---

## Summary

✅ **Successful**: {success_count}/{total_count} CLIs
{warnings_section}
{errors_section}

---

## Detected CLIs

### Active (in PATH)

{FOR EACH cli WHERE status='active'}
- **{CLI Display Name}** v{version}
  - Detection: PATH (`{executable_path}`)
  - Skills Directory: `{skills_dir}`
  - Status: ✅ Ready
{END FOR}

### Detected (Config Only)

{FOR EACH cli WHERE status='warning_no_path'}
- **{CLI Display Name}**
  - Detection: Config directory (`{config_path}`)
  - Skills Directory: `{skills_dir}`
  - Status: ⚠️  Executable not in PATH
  - Note: CLI was previously installed or configured
{END FOR}

### Manual Specification

{FOR EACH cli WHERE status='manual'}
- **{CLI Display Name}**
  - Detection: Manual specification
  - Skills Directory: `{skills_dir}`
  - Status: ℹ️  Created manually
{END FOR}

---

## Errors

{IF errors_count > 0}
{FOR EACH error}
### {CLI Display Name}

**Error**: {error_type}  
**Details**: {error_message}

**Fix**:
{fix_instructions}

{END FOR}
{ELSE}
No errors occurred during bootstrap.
{END IF}

---

## Created Directories

{FOR EACH created_dir}
- `{relative_path}` ({size} bytes)
{END FOR}

**Total Disk Usage**: {total_size_kb} KB

---

## Next Steps

1. **Verify initialization**: Run `/hefesto.list` to see detected CLIs and skills
2. **Create your first skill**: Run `/hefesto.create` with a skill description
3. **Review documentation**: Check `CONSTITUTION.md` for governance rules

{IF warnings_count > 0}
**Warnings to Address**:
{FOR EACH warning}
- {warning_message}
{END FOR}
{END IF}

{IF errors_count > 0}
**Errors to Fix**:
{FOR EACH error}
- {error_summary} → See "Errors" section above for details
{END FOR}
{END IF}

---

## State Persisted

- **MEMORY.md**: ✅ Created/Updated
- **CONSTITUTION.md**: {created | verified | restored}
- **CLI Directories**: {created_count} created, {verified_count} verified
- **Hefesto Version**: {version}

**Initialization Complete** 🎉
```

---

## Field Definitions

### Summary Fields

| Field | Type | Description |
|-------|------|-------------|
| `operation` | enum | "init" or "re-detect" |
| `timestamp` | ISO8601 | When operation started |
| `duration` | number | Seconds elapsed |
| `success_count` | number | CLIs successfully initialized |
| `total_count` | number | Total CLIs attempted |
| `warnings_count` | number | Non-blocking issues |
| `errors_count` | number | Blocking failures |

### CLI Fields

| Field | Type | Description |
|-------|------|-------------|
| `CLI Display Name` | string | Human-readable name (e.g., "Claude Code") |
| `version` | string | SemVer or "unknown" |
| `executable_path` | string | Full path to CLI executable |
| `config_path` | string | Path to config directory |
| `skills_dir` | string | Relative path to skills directory |
| `status` | enum | "active", "warning_no_path", "error_permission", "manual" |

### Error Fields

| Field | Type | Description |
|-------|------|-------------|
| `error_type` | enum | "permission_denied", "disk_full", "invalid_path", "timeout" |
| `error_message` | string | Detailed error description |
| `fix_instructions` | markdown | Step-by-step resolution guide |

---

## Examples

### Example 1: Successful Bootstrap (5 CLIs)

```markdown
# Hefesto Bootstrap Report

**Operation**: init
**Date**: 2026-02-04T14:30:00Z
**Duration**: 3.2s

---

## Summary

✅ **Successful**: 5/5 CLIs

---

## Detected CLIs

### Active (in PATH)

- **Claude Code** v1.2.0
  - Detection: PATH (`/usr/local/bin/claude`)
  - Skills Directory: `.claude/skills/`
  - Status: ✅ Ready

- **OpenAI Codex** v2.1.0
  - Detection: PATH (`/usr/local/bin/codex`)
  - Skills Directory: `.codex/skills/`
  - Status: ✅ Ready

- **OpenCode** v0.2.1
  - Detection: PATH (`/usr/local/bin/opencode`)
  - Skills Directory: `.opencode/skills/`
  - Status: ✅ Ready

- **Cursor** v1.0.5
  - Detection: PATH (`/Applications/Cursor.app/Contents/MacOS/cursor`)
  - Skills Directory: `.cursor/skills/`
  - Status: ✅ Ready

### Detected (Config Only)

- **Gemini CLI**
  - Detection: Config directory (`/Users/dev/.gemini/`)
  - Skills Directory: `.gemini/skills/`
  - Status: ⚠️  Executable not in PATH
  - Note: CLI was previously installed or configured

---

## Errors

No errors occurred during bootstrap.

---

## Created Directories

- `.claude/skills/` (0 bytes)
- `.codex/skills/` (0 bytes)
- `.opencode/skills/` (0 bytes)
- `.cursor/skills/` (0 bytes)
- `.gemini/skills/` (0 bytes)

**Total Disk Usage**: 2.1 KB

---

## Next Steps

1. **Verify initialization**: Run `/hefesto.list` to see detected CLIs and skills
2. **Create your first skill**: Run `/hefesto.create` with a skill description
3. **Review documentation**: Check `CONSTITUTION.md` for governance rules

**Warnings to Address**:
- Gemini CLI config found but executable not in PATH. Skills can be generated but may not work until Gemini CLI is reinstalled.

---

## State Persisted

- **MEMORY.md**: ✅ Created
- **CONSTITUTION.md**: ✅ Verified
- **CLI Directories**: 5 created, 0 verified
- **Hefesto Version**: 1.0.0

**Initialization Complete** 🎉
```

### Example 2: Bootstrap with Errors (2 failures)

```markdown
# Hefesto Bootstrap Report

**Operation**: init
**Date**: 2026-02-04T14:30:00Z
**Duration**: 4.1s

---

## Summary

✅ **Successful**: 3/5 CLIs
⚠️  **Warnings**: 1
❌ **Errors**: 1

---

## Detected CLIs

### Active (in PATH)

- **Claude Code** v1.2.0
  - Detection: PATH (`/usr/local/bin/claude`)
  - Skills Directory: `.claude/skills/`
  - Status: ✅ Ready

- **OpenCode** v0.2.1
  - Detection: PATH (`/usr/local/bin/opencode`)
  - Skills Directory: `.opencode/skills/`
  - Status: ✅ Ready

### Detected (Config Only)

- **Gemini CLI**
  - Detection: Config directory (`/Users/dev/.gemini/`)
  - Skills Directory: `.gemini/skills/`
  - Status: ⚠️  Executable not in PATH

---

## Errors

### VS Code/Copilot

**Error**: permission_denied  
**Details**: Cannot create directory `.github/skills/` (parent directory read-only)

**Fix**:
1. Check permissions: `ls -la . | grep .github`
2. Fix permissions: `chmod +w .github` (if directory exists)
3. Or run: `sudo /hefesto.init` (use with caution)
4. Or manually create: `mkdir -p .github/skills && chmod +w .github/skills`

### Cursor

**Error**: timeout  
**Details**: Version detection timed out after 5 seconds

**Fix**:
1. Check if Cursor is running properly: `cursor --version`
2. If hung, restart Cursor application
3. Re-run detection: `/hefesto.detect`

---

## Created Directories

- `.claude/skills/` (0 bytes)
- `.opencode/skills/` (0 bytes)
- `.gemini/skills/` (0 bytes)

**Total Disk Usage**: 1.3 KB

---

## Next Steps

1. **Verify initialization**: Run `/hefesto.list` to see detected CLIs and skills
2. **Create your first skill**: Run `/hefesto.create` with a skill description
3. **Review documentation**: Check `CONSTITUTION.md` for governance rules

**Warnings to Address**:
- Gemini CLI config found but executable not in PATH

**Errors to Fix**:
- VS Code/Copilot: Permission denied → See "Errors" section for fix instructions
- Cursor: Version detection timeout → See "Errors" section for fix instructions

---

## State Persisted

- **MEMORY.md**: ✅ Created
- **CONSTITUTION.md**: ✅ Verified
- **CLI Directories**: 3 created, 0 verified
- **Hefesto Version**: 1.0.0

**Initialization Complete (with warnings)** ⚠️
```

---

## Usage in Commands

### In /hefesto.init

```markdown
1. Start timer
2. Run CLI detection
3. Create directories
4. Handle errors
5. Stop timer
6. Generate report using this template
7. Display report to user
8. Persist state to MEMORY.md
```

### In /hefesto.detect

```markdown
1. Start timer
2. Run CLI re-detection (only new CLIs)
3. Create new directories
4. Handle errors
5. Stop timer
6. Generate report showing new vs. existing CLIs
7. Display report to user
8. Update MEMORY.md
```

---

## Customization Points

### Emoji Usage

```markdown
SUCCESS: ✅
WARNING: ⚠️
ERROR: ❌
INFO: ℹ️
COMPLETE: 🎉
```

**Note**: Can be disabled with `--no-emoji` flag if terminal doesn't support Unicode

### Verbosity Levels

| Level | Content |
|-------|---------|
| `--quiet` | Summary only (success/failure counts) |
| `--normal` (default) | Full report as shown above |
| `--verbose` | Include debug information (detection timings, cache hits, etc.) |

---

## References

- Error Handling: error-handling.md for error message formats
- CLI Detection: cli-detection-strategy.md for detection details
- FR-012: Detection report showing method and warnings
- SC-001: Bootstrap completion under 10 seconds (report included in timing)
