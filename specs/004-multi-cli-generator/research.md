# Research: Multi-CLI Detection and Parallel Generation

**Feature**: 004-multi-cli-generator  
**Phase**: 0 (Research & Outline)  
**Date**: 2026-02-04

---

## 1. CLI Detection Strategies

### 1.1 PATH-Based Detection

**Approach**: Execute `which` (Unix) or `where` (Windows) to locate CLI executables.

**Pros**:
- Fast (<100ms per CLI)
- Reliable for properly installed CLIs
- Cross-platform with appropriate shell detection

**Cons**:
- Requires CLI to be in PATH
- May miss portable installations
- Version extraction requires separate execution

**Implementation Pattern**:
```bash
# Unix/Linux/macOS
which claude gemini codex code cursor qwen

# Windows PowerShell
where.exe claude.exe gemini.exe codex.exe code.exe cursor.exe qwen.exe
```

**Decision**: PRIMARY detection method - fast and reliable for 90% of installations.

---

### 1.2 Config Directory Detection

**Approach**: Check for existence of `.cli-name/` directories in project root.

**Pros**:
- Catches manual installations
- No execution required
- Works offline
- Fast filesystem check

**Cons**:
- Doesn't verify CLI is functional
- May detect abandoned installations
- Doesn't provide version info

**Implementation Pattern**:
```bash
# Check all 7 config directories
[ -d ".claude" ] && echo "Claude detected"
[ -d ".gemini" ] && echo "Gemini detected"
[ -d ".codex" ] && echo "Codex detected"
[ -d ".github" ] && echo "Copilot detected"
[ -d ".opencode" ] && echo "OpenCode detected"
[ -d ".cursor" ] && echo "Cursor detected"
[ -d ".qwen" ] && echo "Qwen detected"
```

**Decision**: SECONDARY detection method - complements PATH detection, catches edge cases.

---

### 1.3 Combined Detection Strategy (CHOSEN)

**Approach**: Run both methods in parallel, merge results with priority ordering.

**Algorithm**:
```
1. Launch PATH detection (async)
2. Launch config directory scan (async)
3. Wait for both completions (max 500ms combined)
4. Merge results:
   - If CLI found in BOTH: status="detected", method="both"
   - If CLI found in PATH only: status="detected", method="path"
   - If CLI found in config only: status="detected_config_only", method="config_dir"
   - If CLI not found: status="not_found"
5. Return combined detection result
```

**Rationale**: Maximizes coverage while maintaining <500ms performance target. Config-only detection warns user that executable may be missing.

---

## 2. Version Extraction Strategies

### 2.1 Standard `--version` Flag

**Approach**: Execute `{cli} --version` and parse output.

**Challenges**:
- Non-standard output formats
- Some CLIs use `-v` instead
- Parsing inconsistencies

**Fallback Strategy**:
```
1. Try `{cli} --version`
2. If fails, try `{cli} -v`
3. If fails, try `{cli} version`
4. If all fail, mark as "unknown"
```

**Timeout**: 200ms per CLI (prevents hanging on broken installations).

**Decision**: Best-effort extraction - "unknown" is acceptable per FR-022.

---

### 2.2 Alternative: Skip Version Extraction

**Rationale**: Version info is informational only (T2), not required for functionality. Skipping saves 200ms × 7 CLIs = 1400ms overhead.

**Trade-off**: Reduces detection report quality but guarantees <500ms performance.

**Decision**: DEFER - Implement version extraction with timeout, disable if performance target missed during testing.

---

## 3. Parallel Execution Patterns

### 3.1 Bash Background Jobs (Unix)

**Pattern**:
```bash
generate_for_claude &
generate_for_gemini &
generate_for_codex &
wait  # Wait for all background jobs
```

**Pros**:
- Native to shell
- No dependencies
- Simple implementation

**Cons**:
- Error handling complex
- No progress tracking
- Difficult rollback coordination

**Decision**: CHOSEN for Unix systems - simplest cross-platform approach.

---

### 3.2 PowerShell Jobs (Windows)

**Pattern**:
```powershell
$jobs = @()
$jobs += Start-Job -ScriptBlock { Generate-ForClaude }
$jobs += Start-Job -ScriptBlock { Generate-ForGemini }
$jobs | Wait-Job
```

**Pros**:
- Built-in error handling
- Progress tracking available
- Job control (cancel, retry)

**Cons**:
- PowerShell-specific
- Overhead higher than bash jobs

**Decision**: CHOSEN for Windows systems - PowerShell is standard on modern Windows.

---

### 3.3 Sequential Execution (Fallback)

**When**: Parallel execution unavailable or disabled via flag.

**Performance**: ~3x slower, but guaranteed to work.

**Decision**: FALLBACK ONLY - use when parallel execution fails or `--sequential` flag provided.

---

## 4. CLI Adapter Architecture

### 4.1 Strategy Pattern

**Approach**: Each CLI has an adapter with standard interface:

```
CLIAdapter {
  - target_cli: string
  - transform_variables(content): string
  - transform_structure(files): FileTree
  - validate(skill): Result
}
```

**Adapters**:
- `ClaudeAdapter`: No transformations (reference implementation)
- `GeminiAdapter`: `$ARGUMENTS` → `{{args}}`
- `CodexAdapter`: No transformations
- `CopilotAdapter`: Structure adjustment for `.github/skills/`
- `OpenCodeAdapter`: No transformations
- `CursorAdapter`: No transformations
- `QwenAdapter`: `$ARGUMENTS` → `{{args}}`, optional TOML generation

**Decision**: CHOSEN - clean separation, extensible, testable.

---

### 4.2 Adapter Registry

**Pattern**:
```yaml
adapters:
  claude:
    class: ClaudeAdapter
    priority: 1
    config_dir: .claude
  gemini:
    class: GeminiAdapter
    priority: 2
    config_dir: .gemini
  # ... etc
```

**Benefits**:
- Single source of truth
- Easy to add new CLIs
- Priority-based conflict resolution

**Decision**: Store registry in `commands/helpers/cli-adapter.md`.

---

## 5. Atomic Rollback Mechanism

### 5.1 Transaction Log Approach

**Approach**: Log all filesystem operations before execution, rollback from log on failure.

**Pattern**:
```
TRANSACTION START
  LOG: mkdir .claude/skills/skill-name/
  LOG: write .claude/skills/skill-name/SKILL.md
  LOG: mkdir .gemini/skills/skill-name/
  LOG: write .gemini/skills/skill-name/SKILL.md
  ERROR at step 4
  ROLLBACK: delete all logged operations in reverse order
TRANSACTION END
```

**Pros**:
- Complete audit trail
- Precise rollback
- Can resume from failure point

**Cons**:
- Complexity
- Log persistence required

**Decision**: NOT CHOSEN - too complex for prompt-based system.

---

### 5.2 Staged Filesystem Operations (CHOSEN)

**Approach**: Generate all skills to temporary directory first, then move atomically on success.

**Pattern**:
```
1. Create temp dir: /tmp/hefesto-{timestamp}/
2. Generate all skills to temp dir
3. Validate all skills
4. If ALL valid:
   - Move temp dir contents to target directories
   - Delete temp dir
5. If ANY invalid:
   - Delete temp dir
   - Report failure
```

**Pros**:
- Simple implementation
- Automatic cleanup
- No persistent state required

**Cons**:
- Requires sufficient disk space for double storage
- Move operation could fail (rare)

**Decision**: CHOSEN - simplicity wins for Hefesto's use case.

---

### 5.3 Idempotence Check Integration

**Current Behavior**: `/hefesto.create` checks if skill exists and prompts `[overwrite]`, `[merge]`, `[cancel]`.

**Multi-CLI Extension**:
- Check ALL target CLI directories
- If skill exists in SOME but not ALL:
  - Prompt: "Skill exists in Claude, Gemini. Options: [overwrite_all], [skip_existing], [cancel]"
- If skill exists in ALL:
  - Prompt: "Skill exists in all detected CLIs. [overwrite_all], [cancel]"

**Decision**: Extend existing idempotence logic per T0-HEFESTO-08.

---

## 6. Cross-Platform Considerations

### 6.1 Path Resolution

**Challenge**: Different path separators (`/` vs `\`), executable extensions (`.exe` on Windows).

**Solution**: Let AI CLI handle path normalization - Hefesto operates at directory level only.

**Decision**: Use forward slashes in templates, rely on CLI runtime for conversion.

---

### 6.2 Shell Detection

**Pattern**:
```bash
# Detect shell environment
if [ -n "$BASH_VERSION" ]; then
  # Bash detected
elif [ -n "$ZSH_VERSION" ]; then
  # Zsh detected
elif command -v pwsh > /dev/null; then
  # PowerShell detected
fi
```

**Decision**: Detection scripts adapt to detected shell automatically.

---

### 6.3 Filesystem Permissions

**Windows**: Typically permissive in user directories.  
**Unix**: May encounter permission errors in system directories.

**Handling**: Per FR-021, log permission errors and continue with other CLIs. Report failures at end.

**Decision**: Non-blocking error handling - partial success is acceptable.

---

## 7. Performance Optimization

### 7.1 Detection Caching

**Approach**: Cache detection results in MEMORY.md, refresh only when user runs `/hefesto.detect` explicitly.

**Cache Validity**: Until next explicit detection run (no automatic invalidation).

**Benefits**:
- Eliminates 500ms overhead on every command
- User controls refresh timing

**Decision**: CHOSEN - aligns with MEMORY.md as source of truth.

---

### 7.2 Lazy Adapter Loading

**Approach**: Only load adapters for detected CLIs.

**Example**: If only Claude and Gemini detected, only load ClaudeAdapter and GeminiAdapter.

**Benefits**: Reduces memory footprint (negligible for prompt system).

**Decision**: IMPLEMENT - simple conditional loading.

---

### 7.3 Parallel Validation

**Approach**: After generating skills in parallel, validate them in parallel too.

**Pattern**:
```bash
validate_claude &
validate_gemini &
validate_codex &
wait
```

**Benefits**: Maintains 3x performance gain through entire pipeline.

**Decision**: IMPLEMENT - extends parallel pattern to validation phase.

---

## 8. Testing Strategy

### 8.1 Manual Validation Matrix

**Requirement**: Test all combinations (7 CLIs × 2 detection methods × 3 skill types).

**Approach**: Create test matrix spreadsheet, manually execute each case.

**Rationale**: No automated test requirement (Principle III N/A), prompt-based system difficult to unit test.

**Decision**: Manual testing with documented matrix (to be created in Phase 1).

---

### 8.2 Constitution Compliance

**Validation**: Existing `/hefesto.validate` command checks Agent Skills spec compliance.

**Extension**: Run validation for ALL generated CLIs, not just one.

**Decision**: Integrate existing validator into multi-CLI pipeline.

---

## 9. Edge Cases and Error Handling

### 9.1 No CLIs Detected

**Response**: Fall back to interactive mode - prompt user to select target CLI(s) manually.

**Prompt**: "No AI CLIs detected. Install CLIs or specify manually with --cli flag."

**Decision**: Graceful degradation per FR-020.

---

### 9.2 Partial Generation Failure

**Example**: 3 CLIs detected, generation succeeds for 2, fails for 1.

**Response**: Rollback ALL (atomic requirement per FR-011), report which CLI failed and why.

**Decision**: All-or-nothing approach - prevents inconsistent state.

---

### 9.3 User Cancellation Mid-Generation

**Response**: Immediate termination of all parallel jobs, cleanup temp directory, report cancellation.

**Implementation**: Trap SIGINT/SIGTERM signals, execute cleanup handler.

**Decision**: Clean cancellation with no partial artifacts.

---

### 9.4 Conflicting CLI Installations

**Example**: Both `claude` and `claude-beta` in PATH.

**Response**: Use priority ordering from adapter registry, select highest priority.

**Decision**: Deterministic selection prevents ambiguity.

---

## 10. Integration Points

### 10.1 Existing Commands

**Modified Commands**:
- `/hefesto.create` - call detector before generation
- `/hefesto.extract` - call detector before extraction
- `/hefesto.adapt` - call detector to find target CLIs

**New Commands**:
- `/hefesto.detect` - standalone detection and reporting

**Decision**: Minimal changes to existing commands, detector is reusable helper.

---

### 10.2 MEMORY.md Extensions

**New Section**:
```yaml
detected_clis:
  last_detection: 2026-02-04T10:30:00Z
  clis:
    - name: claude
      status: detected
      version: 2.1.31
      path: /usr/local/bin/claude
      config_dir: .claude
      method: both
    - name: gemini
      status: detected
      version: unknown
      path: null
      config_dir: .gemini
      method: config_dir
```

**Decision**: Extend existing MEMORY.md schema, maintain backward compatibility.

---

## 11. Alternatives Considered and Rejected

| Alternative | Why Rejected |
|-------------|--------------|
| **Sequential Generation Only** | Fails SC-003 (3x faster requirement) |
| **Cloud-Based Detection** | Violates offline constraint, adds dependency |
| **Package Manager Integration** | Non-portable (npm, pip, etc. not universal) |
| **Auto-Installation of Missing CLIs** | Out of scope, user responsibility |
| **Custom CLI Discovery Protocol** | Over-engineering, PATH is sufficient |
| **Database for Detection Cache** | Overkill, MEMORY.md is adequate |
| **Micro-Rollback (per-CLI)** | Violates atomic requirement (FR-011) |

---

## 12. Open Questions for Phase 1

1. **CLI Priority Order**: Should priority be user-configurable or hardcoded?
   - **Lean toward**: Hardcoded initially, add config later if requested
   
2. **Version Format Standardization**: How to normalize different version string formats?
   - **Lean toward**: Store as-is, no normalization (display-only field)
   
3. **Progress Indicator Detail Level**: Real-time per-CLI updates or single "Generating..." message?
   - **Lean toward**: Single message - parallel execution makes real-time tracking complex
   
4. **Adapter Extension Mechanism**: How should users add custom CLI adapters?
   - **Lean toward**: Out of scope for v1, support only 7 defined CLIs

---

## 13. Research Conclusions

**Key Decisions**:
1. **Detection**: Combined PATH + config directory scan (parallel, <500ms)
2. **Parallelization**: Shell-native (bash jobs on Unix, PowerShell jobs on Windows)
3. **Adapters**: Strategy pattern with registry in `cli-adapter.md`
4. **Rollback**: Staged filesystem operations (temp dir → atomic move)
5. **Caching**: MEMORY.md persistence, explicit refresh via `/hefesto.detect`
6. **Error Handling**: Non-blocking for permissions, blocking for validation failures

**Next Steps** (Phase 1):
- Define data models for CLI Detection Result, CLI Adapter, Generation Task
- Create contracts for detector, adapter, and generator interfaces
- Generate test matrix for manual validation
- Update quickstart.md with developer workflow

---

**Research Complete** | Ready for Human Gate Approval → Phase 1 Design
