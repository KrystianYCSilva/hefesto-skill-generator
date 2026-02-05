# Quickstart: Multi-CLI Detection and Generation

**Feature**: 004-multi-cli-generator  
**Audience**: AI Agents implementing this feature  
**Time to Complete**: 10 minutes (reading) + implementation time

---

## Overview

This feature adds automatic CLI detection and parallel skill generation to Hefesto. When a user creates a skill, the system automatically detects which AI CLIs are installed and generates the skill for all of them simultaneously.

**Core Concepts**:
- **CLI Detection**: Find installed CLIs via PATH and config directory scanning
- **CLI Adapters**: Transform skills for CLI-specific syntax (e.g., `$ARGUMENTS` → `{{args}}`)
- **Parallel Generation**: Generate skills concurrently for 3x performance gain
- **Atomic Rollback**: All-or-nothing approach - if one CLI fails, all roll back

---

## Quick Reference

### Supported CLIs (Priority Order)

1. Claude Code (`.claude/`)
2. Gemini CLI (`.gemini/`)
3. OpenAI Codex (`.codex/`)
4. VS Code/Copilot (`.github/`)
5. OpenCode (`.opencode/`)
6. Cursor (`.cursor/`)
7. Qwen Code (`.qwen/`)

### Key Files to Create

```
commands/
├── hefesto.detect.md           # NEW - standalone detection command
├── hefesto.create.md            # MODIFIED - integrate detection
├── helpers/
│   ├── cli-detector.md          # NEW - detection logic
│   ├── cli-adapter.md           # NEW - transformation registry
│   ├── parallel-generator.md    # NEW - orchestration
│   └── rollback-handler.md      # NEW - cleanup logic
└── templates/
    ├── detection-report.md      # NEW - detection output
    └── generation-report.md     # NEW - generation output
```

### MEMORY.md Extension

Add new section:
```yaml
## Detected CLIs

last_detection: 2026-02-04T10:30:00Z

clis:
  - name: claude
    status: detected
    version: 2.1.31
    path: /usr/local/bin/claude
    config_dir: .claude
    method: both
```

---

## Implementation Workflow

### Phase 1: CLI Detection (FR-001 to FR-006)

**Goal**: Detect installed CLIs in <500ms

**Steps**:

1. **Create `cli-detector.md` helper**
   - Implement PATH scanning (Unix: `which`, Windows: `where.exe`)
   - Implement config directory checking (check for `.{cli}/` directories)
   - Combine results with priority-based conflict resolution
   - Extract version info (best-effort, timeout 200ms)
   - Return Detection Report

2. **Create `detection-report.md` template**
   - Format: List detected CLIs with status, version, paths
   - Summary: "X out of 7 supported CLIs detected"

3. **Create `/hefesto.detect` command**
   - Call cli-detector helper
   - Display detection report
   - Persist results to MEMORY.md

4. **Test detection**
   - Manual test with 0, 1, 3, 7 CLIs installed
   - Verify <500ms performance target
   - Verify accuracy (no false positives)

---

### Phase 2: CLI Adapters (FR-009, FR-026-028)

**Goal**: Transform skills for CLI-specific syntax

**Steps**:

1. **Create `cli-adapter.md` registry**
   - Define adapter for each CLI (7 total)
   - Specify variable syntax mappings:
     - Claude, Codex, Copilot, OpenCode, Cursor: `$ARGUMENTS` (no change)
     - Gemini, Qwen: `$ARGUMENTS` → `{{args}}`
   - Specify directory structures (all use `.{cli}/skills/{name}/`)
   - Specify frontmatter additions (Copilot adds `github_integration: true`)
   - Define validation rules per CLI

2. **Implement transformation logic**
   - `transform_variables()`: String replacement for variable syntax
   - `transform_structure()`: Directory path construction
   - `add_frontmatter()`: Merge CLI-specific fields
   - `validate()`: Run Agent Skills validator + CLI-specific checks

3. **Test adapters**
   - Test Gemini adapter: verify `$ARGUMENTS` → `{{args}}`
   - Test Copilot adapter: verify `github_integration` field added
   - Test validation: inject error, verify detection

---

### Phase 3: Parallel Generation (FR-007 to FR-011)

**Goal**: Generate skills for all CLIs simultaneously with atomic rollback

**Steps**:

1. **Create `parallel-generator.md` orchestrator**
   - Implement `generate_all()`: Main entry point
   - Implement `generate_single_cli()`: Per-CLI generation
   - Use temp directory for staging: `/tmp/hefesto-{timestamp}/`
   - Launch tasks in parallel (bash background jobs or PowerShell jobs)
   - Wait for all completions
   - Validate all generated skills
   - If all valid: commit to target directories
   - If any invalid: trigger rollback

2. **Create `rollback-handler.md` cleanup logic**
   - Delete temp directory
   - Mark all tasks as `rolled_back`
   - Report which CLI failed and why

3. **Integrate with existing commands**
   - Modify `/hefesto.create` to call cli-detector before generation
   - Modify `/hefesto.create` to call parallel-generator instead of single generation
   - Maintain existing Human Gate (approval happens before parallel generation)

4. **Test parallel generation**
   - Test success case: 3 CLIs, all succeed
   - Test failure case: inject validation error in one CLI, verify rollback
   - Test performance: verify 3x speedup vs sequential
   - Test atomic rollback: verify no partial files after failure

---

### Phase 4: CLI Targeting (FR-012 to FR-015)

**Goal**: Allow users to restrict generation to specific CLIs

**Steps**:

1. **Add `--cli` flag support to `/hefesto.create`**
   - Parse comma-separated CLI names: `--cli claude,gemini`
   - Validate CLI names against detected CLIs
   - Filter target CLIs based on flag
   - Default: all detected CLIs (when flag omitted)

2. **Test CLI targeting**
   - Test `--cli claude`: verify only Claude gets skill
   - Test `--cli claude,gemini,opencode`: verify exactly 3 CLIs get skill
   - Test invalid CLI name: verify error message with available CLIs
   - Test non-detected CLI: verify warning and prompt

---

### Phase 5: Reporting and UX (FR-016 to FR-019)

**Goal**: Provide clear progress and status feedback

**Steps**:

1. **Create `generation-report.md` template**
   - Format: List each CLI with status (success/failed/rolled_back)
   - Summary: "Successfully generated for X CLIs" or "Failed for Y, rolled back"
   - Performance metrics: Total time, per-CLI time

2. **Add progress indicators**
   - Detection: "Detecting CLIs... ✓ (3 found)"
   - Generation: "[claude] ⏳ In progress... ✓ Success"
   - Validation: "Validating... ✓ All passed"
   - Commit: "Committing... ✓ 3 directories updated"

3. **Test reporting**
   - Verify output clarity for success case
   - Verify error messages point to specific CLI and reason
   - Verify rollback messages clearly indicate atomic cleanup

---

### Phase 6: Error Handling (FR-020 to FR-023)

**Goal**: Graceful degradation and collision handling

**Steps**:

1. **Implement fallback for no CLIs detected**
   - If detection report shows 0 CLIs: prompt user to specify `--cli` manually
   - Offer to create directory for specified CLI even if not detected

2. **Implement permission error handling**
   - Catch filesystem errors during generation
   - Mark that CLI as failed, continue with others
   - Trigger rollback if rollback is required (atomic constraint)

3. **Extend idempotence check for multi-CLI**
   - Check if skill exists in ANY target CLI directory
   - Prompt: "Skill exists in claude, gemini. [overwrite_all], [skip_existing], [cancel]"
   - Apply user choice to all CLIs

4. **Test error handling**
   - Test no CLIs detected: verify fallback prompt
   - Test permission error: verify graceful handling and rollback
   - Test skill collision: verify multi-CLI idempotence prompt

---

## Testing Checklist

### Detection Tests

- [ ] 0 CLIs detected: verify fallback mode
- [ ] 1 CLI detected: verify correct identification
- [ ] 3 CLIs detected: verify all found
- [ ] 7 CLIs detected: verify complete coverage
- [ ] PATH-only detection: verify executable found, config missing warning
- [ ] Config-only detection: verify config found, executable missing warning
- [ ] Both methods: verify status=detected, method=both
- [ ] Detection <500ms: measure with 7 CLIs installed
- [ ] Version extraction: verify versions captured or "unknown"
- [ ] MEMORY.md persistence: verify detection results saved

### Adapter Tests

- [ ] Claude adapter: no transformations, `.claude/skills/{name}/`
- [ ] Gemini adapter: `$ARGUMENTS` → `{{args}}`, `.gemini/skills/{name}/`
- [ ] Codex adapter: no transformations, `.codex/skills/{name}/`
- [ ] Copilot adapter: `github_integration` added, `.github/skills/{name}/`
- [ ] OpenCode adapter: no transformations, `.opencode/skills/{name}/`
- [ ] Cursor adapter: no transformations, `.cursor/skills/{name}/`
- [ ] Qwen adapter: `$ARGUMENTS` → `{{args}}`, `.qwen/skills/{name}/`
- [ ] Validation: Gemini skill with `$ARGUMENTS` fails validation

### Parallel Generation Tests

- [ ] 3 CLIs, all succeed: verify 3 directories created
- [ ] 3 CLIs, one fails: verify rollback, no directories created
- [ ] Performance: parallel 3x faster than sequential (3+ CLIs)
- [ ] Atomic rollback: no partial files after failure
- [ ] User cancellation: temp directory cleaned up
- [ ] Disk full error: graceful failure and rollback
- [ ] Permission error: failure and rollback with clear message

### CLI Targeting Tests

- [ ] Default (no flag): all detected CLIs get skill
- [ ] `--cli claude`: only Claude gets skill
- [ ] `--cli claude,gemini`: exactly those 2 get skill
- [ ] `--cli invalid`: error message with available CLIs
- [ ] `--cli cursor` (not detected): warning and prompt

### Reporting Tests

- [ ] Success output: clear summary with CLI list
- [ ] Failure output: clear error with failing CLI identified
- [ ] Progress indicators: status updates during generation
- [ ] Generation report: accurate task counts and statuses

### Error Handling Tests

- [ ] No CLIs detected: fallback prompt shown
- [ ] Permission error: non-blocking for other CLIs, rollback triggered
- [ ] Skill collision: multi-CLI idempotence prompt
- [ ] Validation error: specific error message, rollback triggered

---

## Common Patterns

### Pattern 1: Detection Before Generation

**Every generation command should**:
```
1. Load cached detection from MEMORY.md (if exists and recent)
   OR
   Run detection if cache missing/stale
2. Filter target CLIs based on user flags (--cli)
3. Proceed with generation for filtered list
```

### Pattern 2: Adapter Selection

**For each target CLI**:
```
1. Load adapter from registry by CLI name
2. Apply transformations in order:
   a. Variables
   b. Structure
   c. Frontmatter
3. Validate adapted content
4. Return adapted skill or validation error
```

### Pattern 3: Atomic Rollback

**On any failure**:
```
1. Stop all in-progress tasks immediately
2. Delete temp directory (all generated files)
3. Mark all tasks as rolled_back
4. Report failure with specific CLI and reason
5. DO NOT leave partial files in any CLI directory
```

---

## Troubleshooting

### Detection Takes >500ms

**Diagnosis**: Version extraction timing out on slow executables

**Solution**: Disable version extraction or reduce timeout:
```yaml
detection_config:
  version_extraction: false  # Skip version checks
```

---

### Gemini Skills Fail Validation

**Diagnosis**: `$ARGUMENTS` not replaced with `{{args}}`

**Solution**: Check adapter transformation:
- Verify `cli-adapter.md` has `ARGUMENTS: "{{args}}"` for Gemini
- Verify `transform_variables()` is called before validation

---

### Parallel Generation Not Working

**Diagnosis**: Shell doesn't support background jobs

**Solution**: Fall back to sequential mode:
```bash
# In parallel-generator.md
if ! command -v bash &> /dev/null && ! command -v pwsh &> /dev/null; then
  execution_mode=sequential
fi
```

---

### Rollback Leaves Partial Files

**Diagnosis**: Atomic rollback not triggered properly

**Solution**: Verify failure detection:
- Check that ANY task failure triggers `rollback_all()`
- Verify temp directory deletion in `rollback_all()`
- Check that target directories are NOT written to until validation passes

---

## Performance Optimization Tips

1. **Cache Detection Results**: Don't re-detect on every command, use MEMORY.md cache
2. **Parallel Validation**: Run validators in parallel, not sequentially
3. **Skip Version Extraction**: Saves 200ms × 7 = 1400ms if not needed
4. **Lazy Adapter Loading**: Only load adapters for detected CLIs
5. **Batch Filesystem Operations**: Group mkdir/write operations when possible

---

## References

### Specification Documents

- **spec.md**: Complete feature specification (236 lines)
- **research.md**: Research decisions and trade-offs
- **data-model.md**: Entity schemas and relationships
- **contracts/**: Interface definitions for all components

### Constitution Rules

- **T0-HEFESTO-04**: Multi-CLI Detection (PRIMARY FEATURE)
- **T0-HEFESTO-09**: CLI Compatibility Matrix (PRIMARY FEATURE)
- **T0-HEFESTO-02**: Human Gate (maintained in multi-CLI flow)
- **T0-HEFESTO-08**: Idempotence (extended for multi-CLI)

### Related ADRs

- **ADR-001**: Use Agent Skills as primary format
- **ADR-003**: Lightweight frontmatter with JIT metadata

---

## Next Steps After Implementation

1. **Manual Testing**: Execute all test cases in Testing Checklist
2. **Constitution Validation**: Re-run constitution check against implementation
3. **Documentation Updates**: Update main README with multi-CLI examples
4. **User Communication**: Announce feature in project changelog

---

## Getting Help

**If you encounter ambiguities during implementation**:
1. Refer to spec.md §User Scenarios for intended behavior
2. Check research.md §Alternatives for decision rationale
3. Review data-model.md for entity structure
4. Consult contracts/ for interface expectations
5. Validate against CONSTITUTION.md T0 rules

**If specifications conflict**:
1. T0 rules (CONSTITUTION.md) always win
2. Spec.md requirements override implementation suggestions
3. Research decisions are context, not requirements
4. Quickstart is guidance, not mandate

---

**Quickstart Complete** | Ready for Implementation | Good luck!
