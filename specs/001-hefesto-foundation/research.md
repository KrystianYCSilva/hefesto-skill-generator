# Research: Hefesto Foundation Infrastructure

**Feature**: 001-hefesto-foundation  
**Date**: 2026-02-04  
**Phase**: 0 (Research & Technical Decisions)

## Overview

This document consolidates research findings and technical decisions for implementing the Hefesto Foundation Infrastructure. All unknowns from the Technical Context have been resolved through analysis of existing project documentation, ADRs, and industry best practices.

---

## 1. CLI Detection Methodology

### Decision: Multi-Strategy Detection (PATH + Config Directory)

**Rationale**: Maximum compatibility and reliability across different installation patterns.

**Detection Strategies**:

| Strategy | Method | Reliability | Use Case |
|----------|--------|-------------|----------|
| PATH Scanning | `which <cli>` (Unix) / `where <cli>` (Windows) | High | Active CLI installations |
| Config Directory | Check for `~/.{cli-name}/` or project `.{cli-name}/` | Medium | Previous installations or manual configs |
| Manual Specification | User prompt when no CLIs detected | Fallback | Edge cases, custom installations |

**Implementation Approach**:

1. **PRIMARY**: Scan PATH environment variable for known CLI executables:
   - Claude Code: `claude` command
   - Gemini CLI: `gemini` command
   - OpenAI Codex: `codex` command
   - VS Code/Copilot: `code` command (check for Copilot extension)
   - OpenCode: `opencode` command
   - Cursor: `cursor` command
   - Qwen Code: `qwen` command

2. **SECONDARY**: Check standard config directory locations:
   - Unix/macOS: `~/.{cli-name}/`
   - Windows: `%USERPROFILE%\.{cli-name}\`
   - Project-level: `./.{cli-name}/` (indicates project-specific config)

3. **FALLBACK**: If no CLIs detected, prompt user with supported CLI list

**Alternatives Considered**:

- **PATH-only detection**: Rejected - misses CLIs with config but not in PATH
- **Config-only detection**: Rejected - less reliable than active PATH presence
- **Registry scanning (Windows)**: Rejected - platform-specific, adds complexity
- **Package manager queries**: Rejected - not all CLIs installed via package managers

**References**:
- FR-001: System MUST automatically detect AI CLIs via PATH and config directory checks
- T0-HEFESTO-04: Multi-CLI Detection requirement
- Edge case: "When a CLI config directory exists but the CLI is not in PATH"

---

## 2. State Persistence Format (MEMORY.md)

### Decision: Markdown with YAML Frontmatter + Structured Sections

**Rationale**: Human-readable, version-control friendly, consistent with Agent Skills spec format, parseable by both humans and AI agents.

**Format Structure**:

```markdown
---
hefesto_version: "1.0.0"
initialized: 2026-02-04T14:30:00Z
last_updated: 2026-02-04T15:45:00Z
---

# Hefesto Project State

## Detected CLIs

| CLI | Detection Method | Skills Directory | Version | Status |
|-----|------------------|------------------|---------|--------|
| claude | PATH | .claude/skills/ | 1.2.0 | active |
| gemini | config_directory | .gemini/skills/ | null | warning_no_path |

## Skill Registry

| Skill Name | CLIs | Created | Last Modified |
|------------|------|---------|---------------|
| code-review | claude, gemini | 2026-02-04 | 2026-02-04 |

## State Metadata

- **Total Skills**: 1
- **Active CLIs**: 2
- **Last Validation**: 2026-02-04T15:45:00Z
```

**Alternatives Considered**:

- **JSON**: Rejected - less human-readable, harder to manually edit/debug
- **TOML**: Rejected - less familiar to target users, not aligned with skill format
- **SQLite**: Rejected - binary format, not version-control friendly, requires dependencies
- **Plain Markdown tables**: Rejected - harder to parse metadata like version/timestamp

**Key Design Points**:

- Frontmatter tracks global metadata (version, timestamps)
- Markdown tables for structured data (human-scannable)
- ISO 8601 timestamps for cross-platform compatibility
- Null values represented explicitly for missing data
- Status field enables warnings (e.g., "warning_no_path" for config-only CLIs)

**References**:
- FR-011: MEMORY.md MUST track detected CLIs, skill names, timestamp, Hefesto version
- ADR-003: Lightweight frontmatter with JIT metadata
- Entity: Project State with attributes (detected CLIs, timestamp, version, skill registry)

---

## 3. Directory Structure Creation Strategy

### Decision: Lazy Creation + Idempotent Operations

**Rationale**: Only create directories for detected CLIs, support re-running bootstrap safely, minimize disk usage.

**Creation Strategy**:

1. **Detection Phase**: Identify all installed CLIs
2. **Verification Phase**: Check if directories already exist
3. **Creation Phase**: Create missing directories with proper permissions
4. **Validation Phase**: Verify directory accessibility

**Directory Template**:

```text
.{cli-name}/
└── skills/          # Initially empty, populated by /hefesto.create
```

**Permission Strategy**:

- **Unix/macOS**: `mkdir -p .{cli-name}/skills` (inherits parent permissions)
- **Windows**: PowerShell `New-Item -Force -Type Directory` (current user read/write)
- **Validation**: Attempt write test file, remove immediately

**Idempotency Guarantees**:

| Scenario | Behavior |
|----------|----------|
| First run, no directories | Create all for detected CLIs |
| Second run, directories exist | No-op, report existing structures |
| New CLI installed, re-detect | Create only new CLI directories |
| Permission error on creation | Skip that CLI, continue with others, report in summary |

**Alternatives Considered**:

- **Eager creation (all 7 CLIs)**: Rejected - violates T0-HEFESTO-04 (detect before creating), creates clutter
- **Manual directory specification**: Rejected - increases friction, violates automatic detection principle
- **Symbolic links to shared location**: Rejected - complicates multi-CLI independence, not all platforms support

**References**:
- FR-002: System MUST create directory structures only for detected CLIs
- FR-009: System MUST be idempotent
- FR-014: System MUST create skill directories with appropriate permissions
- FR-017: System MUST handle permission errors gracefully

---

## 4. CONSTITUTION.md Management

### Decision: Bundled Copy + Integrity Validation on Every Command

**Rationale**: Ensures governance rules always available, prevents accidental corruption, supports recovery.

**Management Strategy**:

1. **Bootstrap**: Copy CONSTITUTION.md from Hefesto repository to project root (if not exists)
2. **Validation**: On every `/hefesto.*` command execution:
   - Check file exists
   - Validate structure (frontmatter, T0 sections present)
   - Verify T0 rules are intact
3. **Recovery**:
   - If missing → restore from bundled copy
   - If corrupted → validate and block if T0 violated
4. **Versioning**: Track CONSTITUTION version in MEMORY.md for migration detection

**Validation Criteria**:

| Check | Pass Condition | Fail Action |
|-------|---------------|-------------|
| File exists | CONSTITUTION.md present in project root | Restore from bundle |
| Valid frontmatter | YAML frontmatter with version, status, tier | Restore from bundle |
| T0 rules present | All 11 T0-HEFESTO-* sections exist | Block operations, notify user |
| Structure integrity | Heading hierarchy intact | Warn user, allow operations if T0 intact |

**Alternatives Considered**:

- **Remote fetch on missing**: Rejected - violates offline operation requirement (FR-007)
- **Allow customization**: Rejected - violates immutability principle for T0 rules
- **Validate only on bootstrap**: Rejected - user could delete/modify between commands
- **Lock file permissions**: Rejected - not cross-platform, can be bypassed

**References**:
- FR-003: System MUST copy CONSTITUTION.md to project root if not present
- FR-010: System MUST validate CONSTITUTION.md structure and T0 rules on every command
- Edge case: "When CONSTITUTION.md is manually deleted or modified outside Hefesto"
- User Story 4: Enforce Constitutional Governance from Start

---

## 5. Error Handling and Recovery Patterns

### Decision: Fail-Safe with Detailed Reporting

**Rationale**: Maximize successful partial completion, provide actionable error information, maintain system integrity.

**Error Categories and Handling**:

| Error Type | Recovery Strategy | User Impact |
|------------|-------------------|-------------|
| **Permission errors** | Skip problematic CLI, continue with others | Partial success |
| **Corrupted MEMORY.md** | Backup with timestamp, create fresh, rescan filesystem | Auto-recovery |
| **Missing CONSTITUTION.md** | Restore from bundle | Auto-recovery |
| **No CLIs detected** | Prompt for manual specification | User input required |
| **Disk full** | Abort, report required space | Abort with guidance |

**Reporting Format**:

```markdown
## Bootstrap Summary

✅ Successfully initialized: 5/7 CLIs
⚠️  Warnings: 1
❌ Errors: 1

### Successful

- Claude Code (PATH detection) → .claude/skills/
- Gemini CLI (config detection, ⚠️ not in PATH) → .gemini/skills/
- OpenAI Codex (PATH detection) → .codex/skills/
- OpenCode (PATH detection) → .opencode/skills/
- Cursor (PATH detection) → .cursor/skills/

### Errors

- VS Code/Copilot: Permission denied creating .github/skills/
  → Fix: Run with appropriate permissions or manually create directory

### Next Steps

1. Review warnings and errors above
2. Run `/hefesto.list` to verify initialization
3. Run `/hefesto.create` to generate your first skill
```

**References**:
- FR-016: Handle corrupted MEMORY.md
- FR-017: Handle permission errors gracefully
- Clarification: "Skip problematic CLI, log error, continue with others, report failures"
- SC-003: 95%+ success rate in standard environments

---

## 6. Cross-Platform Compatibility

### Decision: Shell Script Abstraction with Platform Detection

**Rationale**: Support Windows, macOS, and Linux without external dependencies.

**Platform Detection**:

```markdown
## Platform Identification

| Platform | Detection | Shell |
|----------|-----------|-------|
| Windows | `$Env:OS -eq "Windows_NT"` | PowerShell |
| macOS | `uname -s` = "Darwin" | Bash/Zsh |
| Linux | `uname -s` = "Linux" | Bash |
```

**Platform-Specific Commands**:

| Operation | Windows (PowerShell) | Unix (Bash) |
|-----------|----------------------|-------------|
| PATH check | `where.exe {cli}` | `which {cli}` |
| Create directory | `New-Item -Force -Type Directory` | `mkdir -p` |
| Check file exists | `Test-Path` | `[ -f ... ]` |
| Get timestamp | `Get-Date -Format "o"` | `date -u +"%Y-%m-%dT%H:%M:%SZ"` |

**Alternatives Considered**:

- **Python scripts**: Rejected - adds Python as dependency, violates zero-dependency principle
- **Node.js scripts**: Rejected - adds Node.js as dependency
- **Single platform only**: Rejected - violates cross-platform requirement (SC-003)
- **Platform-specific installers**: Rejected - increases maintenance burden

**References**:
- Assumptions: "Users are running on Windows, macOS, or Linux operating systems"
- SC-003: Bootstrap completes successfully in 95%+ environments across platforms
- FR-007: System MUST support offline operation (no external tools)

---

## 7. Performance Optimization

### Decision: Parallel Detection + Cached Results

**Rationale**: Meet <5 second bootstrap target, optimize repeated operations.

**Performance Targets**:

| Operation | Target | Strategy |
|-----------|--------|----------|
| CLI detection | < 2s | Parallel PATH checks |
| Directory creation | < 1s | Batch mkdir operations |
| State persistence | < 100ms | Single file write |
| CONSTITUTION validation | < 500ms | Cached parse results |
| **Total Bootstrap** | **< 5s** | Combined optimizations |

**Optimization Techniques**:

1. **Parallel CLI Detection**: Check all 7 CLIs simultaneously
2. **Lazy Validation**: Only validate CONSTITUTION on first command, cache until file modified
3. **Incremental Updates**: MEMORY.md updates append-only when possible
4. **Minimal Filesystem Ops**: Single `mkdir -p` call per CLI (creates parent dirs automatically)

**Alternatives Considered**:

- **Sequential detection**: Rejected - 7 CLIs × ~300ms = 2.1s just for detection
- **Background validation**: Rejected - complex, potential race conditions
- **In-memory state only**: Rejected - violates persistence requirement

**References**:
- FR-008: System MUST complete bootstrap in under 5 seconds
- SC-001: Developers can bootstrap in under 10 seconds (includes user read time)
- Performance Goals: Bootstrap completion < 5s, CLI detection < 2s

---

## 8. Git Integration

### Decision: .gitignore Suggestions + Commit Hooks (Future)

**Rationale**: Support version control best practices, avoid committing generated artifacts.

**.gitignore Recommendations**:

```gitignore
# Hefesto state (commit this - tracks project configuration)
MEMORY.md

# Hefesto constitution (commit this - governance rules)
CONSTITUTION.md

# CLI skill directories (commit skills, not infrastructure)
.claude/
.gemini/
.codex/
.github/
.opencode/
.cursor/
.qwen/

# Backup files (do not commit)
*.backup.*
```

**Git Worktree/Submodule Handling**:

- Each worktree gets independent MEMORY.md (separate state)
- CONSTITUTION.md shared from main repo (symlink or copy)
- Submodules can have their own Hefesto initialization

**Alternatives Considered**:

- **Automatic .gitignore modification**: Rejected - invasive, user may have custom setup
- **Ignore MEMORY.md**: Rejected - state should be tracked for team collaboration
- **Global gitignore**: Rejected - project-specific is clearer

**References**:
- FR-015: System MUST be compatible with Git repositories
- Assumption: "The project uses Git or another version control system"
- Edge case: "How does the system handle projects with multiple Git worktrees or submodules?"

---

## Summary of Decisions

| Research Area | Decision | Status |
|---------------|----------|--------|
| CLI Detection | Multi-strategy (PATH + Config) | ✅ Final |
| State Format | Markdown + YAML frontmatter | ✅ Final |
| Directory Creation | Lazy + Idempotent | ✅ Final |
| CONSTITUTION Management | Bundled + Validated | ✅ Final |
| Error Handling | Fail-safe with reporting | ✅ Final |
| Cross-Platform | Shell script abstraction | ✅ Final |
| Performance | Parallel + Caching | ✅ Final |
| Git Integration | .gitignore suggestions | ✅ Final |

**All unknowns from Technical Context have been resolved.**

---

**Next Phase**: Phase 1 (Design) - Generate data-model.md, contracts/, and quickstart.md based on these research findings.
