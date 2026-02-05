# Multi-CLI Integration Guide

**Purpose**: Integration guide for multi-CLI parallel generation in Hefesto commands  
**Feature**: 004-multi-cli-generator

---

## Overview

This guide shows how to integrate multi-CLI parallel generation into Hefesto commands (`/hefesto.create`, `/hefesto.extract`, `/hefesto.adapt`).

**Core Components**:
- `cli-detector.md` - Detect installed CLIs
- `cli-adapter.md` - Transform skills for each CLI
- `parallel-generator.md` - Generate skills in parallel
- `rollback-handler.md` - Atomic cleanup on failure

---

## Integration Pattern for `/hefesto.create`

### Phase 1: CLI Detection (Before Generation)

```markdown
## Phase 1.5: CLI Detection

1. Load cached detection from MEMORY.md
   cached_detection = load_cached_detection()  # from cli-detector.md
   
2. If cache valid (recent) and --cli flag not provided:
   target_clis = cached_detection.detected_clis
   
3. If cache missing/stale or --cli flag provided:
   detection_config = {
     check_path: true,
     check_config_dirs: true,
     timeout_ms: 500,
     version_extraction: true,
     target_clis: parse_cli_flag(args.cli) OR null
   }
   
   detection_report = detect_all_clis(detection_config)  # from cli-detector.md
   target_clis = detection_report.clis WHERE status IN [detected, detected_config_only]
   
   persist_detection_results(detection_report)  # Save to MEMORY.md

4. Filter target CLIs based on --cli flag (if provided)
   IF args.cli:
     target_clis = target_clis WHERE name IN args.cli
     
5. If no CLIs detected:
   TRIGGER fallback mode (prompt user to specify manually)
   
6. Display detection summary
   DISPLAY: "Detected {count} CLI(s): {cli_names}"
```

**Performance**: <500ms

---

### Phase 2: Parallel Generation (Replace Sequential)

```markdown
## Phase 5: Parallel Skill Generation

1. Create generation request
   generation_request = {
     skill_content: {
       skill_name: skill_name,
       skill_md: skill_content,
       references: references,
       scripts: scripts,
       assets: assets,
       metadata: metadata
     },
     target_clis: target_clis.map(cli => cli.name),
     execution_mode: "parallel",  # or "sequential" if --sequential flag
     temp_directory: "/tmp/hefesto-" + timestamp()
   }

2. Generate for all CLIs in parallel
   generation_report = generate_all(generation_request)  # from parallel-generator.md

3. Check for rollback
   IF generation_report.rollback_occurred:
     DISPLAY: "❌ Generation failed. All changes rolled back."
     
     # Display detailed error report
     FOR EACH task IN generation_report.tasks WHERE status = "failed":
       DISPLAY: "  [{task.target_cli}] ✗ {task.error_message}"
     
     ABORT with error
   
4. Display success report
   DISPLAY: "✅ Skill '{skill_name}' generated for {successful} CLI(s)"
   
   FOR EACH task IN generation_report.tasks WHERE status = "success":
     DISPLAY: "  [{task.target_cli}] ✓ {task.output_paths[0]}"
   
   # Show performance metrics
   DISPLAY: "Duration: {duration}s (parallel speedup: {speedup}x)"
```

**Performance**: 3x faster than sequential for 3+ CLIs

---

### Phase 3: Progress Indicators (During Generation)

```markdown
## Progress Tracking

1. Display detection progress
   DISPLAY: "🔍 Detecting CLIs..."
   # ... detection runs ...
   DISPLAY: "✓ (3 found: claude, gemini, opencode)"

2. Display generation progress
   DISPLAY: "Generating skills for 3 CLIs..."
   DISPLAY: "  [claude] ⏳ In progress..."
   DISPLAY: "  [gemini] ⏳ In progress..."
   DISPLAY: "  [opencode] ⏳ In progress..."

3. Display validation progress
   DISPLAY: "Validating..."
   DISPLAY: "  [claude] ✓ Success"
   DISPLAY: "  [gemini] ✓ Success"
   DISPLAY: "  [opencode] ✓ Success"

4. Display commit progress
   DISPLAY: "Committing to target directories..."
   DISPLAY: "  ✓ .claude/skills/code-review/"
   DISPLAY: "  ✓ .gemini/skills/code-review/"
   DISPLAY: "  ✓ .opencode/skills/code-review/"

5. Display final status
   DISPLAY: "Success! Skill 'code-review' generated for 3 CLIs in 2.1s"
```

---

### Phase 4: Idempotence Check (Multi-CLI)

```markdown
## Multi-CLI Collision Detection

1. Check for existing skills across all target CLIs
   collisions = []
   
   FOR EACH target_cli IN target_clis:
     skill_path = ".{target_cli.name}/skills/{skill_name}/SKILL.md"
     IF file_exists(skill_path):
       collisions.append(target_cli.name)

2. Prompt based on collision count
   IF collisions.length == target_clis.length:
     # Skill exists in ALL target CLIs
     PROMPT: "Skill '{skill_name}' already exists in all detected CLIs."
     OPTIONS: [overwrite_all], [cancel]
     
   ELSE IF collisions.length > 0:
     # Skill exists in SOME CLIs
     PROMPT: "Skill '{skill_name}' exists in {collisions.join(', ')}."
     OPTIONS: [overwrite_all], [skip_existing], [cancel]
     
   ELSE:
     # No collisions, proceed
     CONTINUE

3. Handle user action
   CASE user_action:
     "overwrite_all":
       # Generate for all CLIs (overwrite existing)
       CONTINUE with generation
       
     "skip_existing":
       # Generate only for CLIs without skill
       target_clis = target_clis WHERE name NOT IN collisions
       IF target_clis.length == 0:
         DISPLAY: "No new CLIs to generate for."
         ABORT
       CONTINUE with generation
       
     "cancel":
       DISPLAY: "Operation cancelled. No changes made."
       ABORT
```

---

## Integration Pattern for `/hefesto.extract`

```markdown
Same pattern as /hefesto.create:

1. Detect CLIs (or use cached detection)
2. Extract skill from existing code
3. Generate for all detected CLIs in parallel
4. Handle collisions with multi-CLI idempotence check
5. Display generation report
```

---

## Integration Pattern for `/hefesto.adapt`

```markdown
Same pattern as /hefesto.create:

1. Detect CLIs (or use cached detection)
2. Load source skill
3. Apply adaptations
4. Generate adapted skill for all CLIs in parallel
5. Handle collisions
6. Display generation report
```

---

## CLI Flag Handling

### `--cli` Flag Syntax

```bash
# Single CLI
/hefesto.create "skill description" --cli claude

# Multiple CLIs (comma-separated)
/hefesto.create "skill description" --cli claude,gemini,opencode

# All detected CLIs (default, no flag)
/hefesto.create "skill description"
```

### Validation Rules

```markdown
1. Parse --cli flag
   cli_names = args.cli.split(',')

2. Validate CLI names
   FOR EACH cli_name IN cli_names:
     IF cli_name NOT IN supported_clis:
       ERROR: "Unknown CLI: {cli_name}"
       DISPLAY: "Supported CLIs: claude, gemini, codex, copilot, opencode, cursor, qwen"
       ABORT

3. Check if CLI is detected
   FOR EACH cli_name IN cli_names:
     IF cli_name NOT IN detected_clis:
       WARNING: "{cli_name} not detected"
       PROMPT: "CLI '{cli_name}' not detected. Create directory anyway? (y/n)"
       
       IF user = "n":
         REMOVE cli_name from target_clis
       ELSE:
         CREATE directory .{cli_name}/skills/
         ADD cli_name to target_clis
```

---

## Error Handling

### Validation Failure

```markdown
IF generation_report.rollback_occurred:
  # Find which CLI failed
  failed_task = generation_report.tasks WHERE status = "failed"
  
  DISPLAY:
  ❌ Generation failed for {failed_task.target_cli}
  
  Error: {failed_task.error_message}
  
  All changes have been rolled back.
  
  Fix the issue and retry: /hefesto.create "{skill_name}"
```

### Permission Error

```markdown
IF error_type = "permission_denied":
  DISPLAY:
  ❌ Permission denied: {error_path}
  
  Fix:
  1. Check permissions: ls -la {parent_dir}
  2. Fix permissions: chmod +w {parent_dir}
  3. Retry: /hefesto.create "{skill_name}"
```

### Disk Full Error

```markdown
IF error_type = "disk_full":
  DISPLAY:
  ❌ Disk full during generation
  
  All changes have been rolled back.
  
  Free up disk space and retry.
```

---

## Performance Monitoring

```markdown
## Log Performance Metrics

1. Detection phase
   detection_start = now()
   # ... detection runs ...
   detection_duration = now() - detection_start
   LOG: "Detection: {detection_duration}ms"

2. Generation phase
   generation_start = now()
   # ... parallel generation runs ...
   generation_duration = now() - generation_start
   LOG: "Generation: {generation_duration}ms"

3. Validation phase
   validation_start = now()
   # ... validation runs ...
   validation_duration = now() - validation_start
   LOG: "Validation: {validation_duration}ms"

4. Calculate speedup
   sequential_time = generation_duration * target_clis.length
   parallel_speedup = sequential_time / generation_duration
   LOG: "Parallel speedup: {parallel_speedup}x"
```

---

## Testing Checklist

### Manual Testing

- [ ] Detect 0 CLIs: Verify fallback prompt
- [ ] Detect 1 CLI: Verify single generation
- [ ] Detect 3 CLIs: Verify parallel generation with 3x speedup
- [ ] Detect 7 CLIs: Verify all CLIs generate correctly
- [ ] --cli flag with single CLI: Verify only that CLI gets skill
- [ ] --cli flag with multiple CLIs: Verify only specified CLIs get skill
- [ ] Collision in all CLIs: Verify overwrite_all prompt
- [ ] Collision in some CLIs: Verify skip_existing option
- [ ] Validation failure: Verify atomic rollback
- [ ] Permission error: Verify error message and rollback

---

## Related Files

- **Helpers**: `cli-detector.md`, `cli-adapter.md`, `parallel-generator.md`, `rollback-handler.md`
- **Templates**: `detection-report.md`, `generation-report.md`
- **Commands**: `hefesto.create.md`, `hefesto.extract.md`, `hefesto.adapt.md`
- **Contracts**: See `specs/004-multi-cli-generator/contracts/`

---

**Version**: 1.0.0 | **Date**: 2026-02-05 | **Feature**: 004-multi-cli-generator
