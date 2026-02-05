# Parallel Generator Orchestrator

**Purpose**: Orchestrate simultaneous skill generation for multiple AI CLIs  
**Contract**: [parallel-generator.md](../../specs/004-multi-cli-generator/contracts/parallel-generator.md)  
**Feature**: 004-multi-cli-generator

---

## Overview

The Parallel Generator manages concurrent skill generation with:
- **Parallel Execution**: Generate for multiple CLIs simultaneously (3x faster)
- **Temp Directory Staging**: All-or-nothing atomic operations
- **Progress Tracking**: Real-time status updates
- **Atomic Rollback**: Clean up all changes if any CLI fails

**Performance Target**: 3x faster than sequential for 3+ CLIs

---

## Operations

### `generate_all(request: GenerationRequest) -> GenerationReport`

**Description**: Generate skill for all target CLIs in parallel (or sequential based on mode).

**Algorithm (Parallel Mode)**:
```
1. Create temporary staging directory: /tmp/hefesto-{timestamp}/
2. Initialize Generation Report
3. For each target CLI:
   a. Load CLI adapter
   b. Create GenerationTask with status=pending
   c. Add task to report
4. Launch all generation tasks in parallel:
   a. Execute generate_single_cli() for each task
   b. Monitor progress and update task status
5. Wait for all tasks to complete (or first failure)
6. If ALL tasks successful:
   a. Validate all generated skills
   b. If all valid, move from temp dir to target dirs (atomic)
   c. Delete temp directory
   d. Mark all tasks as success
   e. Return report with rollback_occurred=false
7. If ANY task failed:
   a. Trigger rollback_all()
   b. Mark failed task appropriately
   c. Mark other tasks as rolled_back
   d. Return report with rollback_occurred=true
```

**Algorithm (Sequential Mode)**:
```
1-3. Same as parallel mode
4. Execute tasks sequentially (no parallelization)
5-7. Same as parallel mode
```

**Performance Target**:
- Parallel mode: 3x faster than sequential for 3+ CLIs
- Sequential mode: Baseline performance

---

### `generate_single_cli(task: GenerationTask, adapter: CLIAdapter, temp_dir: string) -> GenerationTask`

**Description**: Generate skill for a single CLI in temp directory.

**Algorithm**:
```
1. Update task.status = in_progress
2. Set task.start_time = now()
3. Apply adapter transformations:
   a. adapted_skill = adapter.adapt(task.skill_content, task.target_cli)
4. Construct output paths in temp directory:
   a. temp_skill_dir = temp_dir / cli_name / skills / skill_name /
   b. Create directory structure
5. Write files to temp directory:
   a. Write SKILL.md
   b. Write references/ (if present)
   c. Write scripts/ (if present)
   d. Write assets/ (if present)
6. Validate adapted skill:
   a. validation_result = adapter.validate(adapted_skill)
   b. If validation_result.valid = false:
      - Set task.status = failed
      - Set task.error_message = validation errors
      - Return task
7. Set task.status = success
8. Set task.end_time = now()
9. Set task.output_paths = list of created files
10. Return task
```

**Performance Target**: <2 seconds per CLI for typical skill

---

### `validate_all_generated(tasks: list[GenerationTask], temp_dir: string) -> boolean`

**Description**: Validate all generated skills before committing to target directories.

**Algorithm**:
```
1. For each task with status=success:
   a. Read generated files from temp directory
   b. Run Agent Skills spec validator
   c. Run CLI-specific validators
   d. If any validation fails:
      - Update task.status = failed
      - Update task.error_message
      - Return false
2. If all validations pass: return true
```

**Validators Used**:
- Existing `/hefesto.validate` command (Agent Skills spec)
- CLI adapter validation rules
- T0-HEFESTO-03 (SKILL.md < 500 lines)
- T0-HEFESTO-11 (No secrets)

**Performance Target**: <500ms for 7 CLIs (run in parallel)

---

### `commit_to_targets(tasks: list[GenerationTask], temp_dir: string) -> CommitResult`

**Description**: Atomically move validated skills from temp directory to target CLI directories.

**Algorithm**:
```
1. For each task with status=success:
   a. Construct target path: ./{cli_config_dir}/skills/{skill_name}/
   b. Check if target directory exists:
      - If exists: trigger idempotence check (T0-HEFESTO-08)
      - User action: [overwrite], [skip], [cancel]
      - If cancel: return CommitResult with aborted=true
   c. Create target directory if not exists
   d. Move files from temp_dir/{cli_name}/ to target directory
   e. Verify all files moved successfully
2. If ANY move operation fails:
   a. Return CommitResult with success=false, error=details
3. If all moves successful:
   a. Delete temp directory
   b. Return CommitResult with success=true
```

**Atomicity**: All moves succeed or all fail (via rollback)

---

### `rollback_all(tasks: list[GenerationTask], temp_dir: string) -> void`

**Description**: Clean up temporary directory and mark all tasks as rolled back.

**Algorithm**:
```
1. For each task in tasks:
   a. If task.status = success or in_progress:
      - Set task.status = rolled_back
      - Set task.error_message = "Rolled back due to sibling failure"
2. Delete temp directory recursively
3. Verify temp directory deleted (retry up to 3 times if needed)
4. Log rollback completion
```

**Performance**: <100ms cleanup time

---

## Parallel Execution Strategies

### Unix/Linux/macOS (Bash Background Jobs)

```bash
#!/bin/bash
temp_dir="/tmp/hefesto-$(date +%s)"
mkdir -p "$temp_dir"

# Launch parallel generation tasks
generate_cli "claude" "$temp_dir" &
pid_claude=$!

generate_cli "gemini" "$temp_dir" &
pid_gemini=$!

generate_cli "opencode" "$temp_dir" &
pid_opencode=$!

# Wait for all background jobs
wait $pid_claude
status_claude=$?

wait $pid_gemini
status_gemini=$?

wait $pid_opencode
status_opencode=$?

# Check for failures
if [ $status_claude -ne 0 ] || [ $status_gemini -ne 0 ] || [ $status_opencode -ne 0 ]; then
  echo "Generation failed, rolling back..."
  rm -rf "$temp_dir"
  exit 1
fi

# Commit to targets
commit_all "$temp_dir"
```

---

### Windows (PowerShell Jobs)

```powershell
$tempDir = "C:\Temp\hefesto-$(Get-Date -Format 'yyyyMMddHHmmss')"
New-Item -ItemType Directory -Path $tempDir -Force

# Launch parallel generation jobs
$jobs = @()
$jobs += Start-Job -ScriptBlock { param($cli, $dir) Generate-CLI $cli $dir } -ArgumentList "claude", $tempDir
$jobs += Start-Job -ScriptBlock { param($cli, $dir) Generate-CLI $cli $dir } -ArgumentList "gemini", $tempDir
$jobs += Start-Job -ScriptBlock { param($cli, $dir) Generate-CLI $cli $dir } -ArgumentList "opencode", $tempDir

# Wait for all jobs
$results = $jobs | Wait-Job | Receive-Job

# Check for failures
$failed = $results | Where-Object { $_.Success -eq $false }
if ($failed) {
    Write-Host "Generation failed, rolling back..."
    Remove-Item -Recurse -Force $tempDir
    exit 1
}

# Commit to targets
Commit-All $tempDir
```

---

## Progress Tracking

### Output Format (Parallel Mode)

```
Detecting CLIs... ✓ (3 found: claude, gemini, opencode)
Generating skills for 3 CLIs...
  [claude] ⏳ In progress...
  [gemini] ⏳ In progress...
  [opencode] ⏳ In progress...

Validating...
  [claude] ✓ Success
  [gemini] ✓ Success
  [opencode] ✓ Success

Committing to target directories...
  ✓ .claude/skills/code-review/
  ✓ .gemini/skills/code-review/
  ✓ .opencode/skills/code-review/

Success! Skill 'code-review' generated for 3 CLIs in 2.1s
```

### Output Format (Failure with Rollback)

```
Detecting CLIs... ✓ (3 found: claude, gemini, opencode)
Generating skills for 3 CLIs...
  [claude] ⏳ In progress...
  [gemini] ⏳ In progress...
  [opencode] ⏳ In progress...

Validating...
  [claude] ✓ Success
  [gemini] ✗ Failed: Validation error - $ARGUMENTS found instead of {{args}}
  [opencode] ⏳ Rolling back...

Rolling back all changes...
  [claude] ⚠️  Rolled back
  [gemini] ✗ Failed
  [opencode] ⚠️  Rolled back

Error: Generation failed for gemini. All changes rolled back.
```

---

## Error Scenarios

| Scenario | Response | Rollback |
|----------|----------|----------|
| One CLI fails validation | Rollback all CLIs | Yes |
| Permission error on one CLI | Rollback all CLIs | Yes |
| Disk full during generation | Rollback all CLIs | Yes |
| User cancels mid-generation | Immediate stop, rollback all | Yes |
| Temp directory creation fails | Fail fast, no rollback needed | No |
| Commit to target fails | Rollback all CLIs | Yes |
| Idempotence conflict (user cancels) | Abort operation, temp dir cleanup | Yes |

---

## Configuration

### Execution Mode Selection

**Default**: Parallel mode (if supported by environment)

**Override**: `--sequential` flag forces sequential execution

**Auto-Detection**:
```
If bash or PowerShell available:
  execution_mode = parallel
Else:
  execution_mode = sequential
```

---

## Performance Targets

| Metric | Target | Measured How |
|--------|--------|--------------|
| Parallel speedup | 3x faster than sequential (3+ CLIs) | Time start to finish |
| Single CLI generation | <2 seconds | Per-task timing |
| Validation phase | <500ms for 7 CLIs | Parallel validation timing |
| Rollback cleanup | <100ms | Temp directory deletion |
| Commit to targets | <200ms for 7 CLIs | File move operations |

---

## Usage Example

```markdown
# Generate for detected CLIs
generation_request = {
  skill_content: skill,
  target_clis: ["claude", "gemini", "opencode"],
  execution_mode: "parallel",
  temp_directory: "/tmp/hefesto-12345"
}

generation_report = generate_all(generation_request)

if generation_report.rollback_occurred:
  display_error(generation_report)
else:
  display_success(generation_report)
```

---

## Related Files

- **Contract**: [parallel-generator.md](../../specs/004-multi-cli-generator/contracts/parallel-generator.md)
- **Data Model**: [data-model.md](../../specs/004-multi-cli-generator/data-model.md) §3, §5
- **Helpers**: `cli-detector.md`, `cli-adapter.md`, `rollback-handler.md`
- **Templates**: `generation-report.md`
- **Commands**: `hefesto.create.md`, `hefesto.extract.md`

---

**Version**: 1.0.0 | **Date**: 2026-02-05 | **Feature**: 004-multi-cli-generator
