# Generation Report Template

**Purpose**: Template for multi-CLI skill generation output  
**Feature**: 004-multi-cli-generator

---

## Template

```markdown
## Skill Generation Report

**Skill Name**: {skill_name}  
**Generated**: {timestamp}  
**Duration**: {duration}s  
**Target CLIs**: {total_tasks}  
**Execution Mode**: {execution_mode}

---

### Summary

{IF rollback_occurred}
❌ Generation failed. All changes rolled back.
{ELSE}
✅ Successfully generated skill for {successful} CLI(s)
{END IF}

---

### Generation Results

{FOR EACH task}
- **{task.target_cli}**: {task.status_icon} {task.status}
  {IF task.status == "success"}
  - Output: {task.output_paths[0]}
  - Duration: {task.end_time - task.start_time}s
  {ELSE IF task.status == "failed"}
  - Error: {task.error_message}
  {ELSE IF task.status == "rolled_back"}
  - Rolled back due to sibling failure
  {END IF}
{END FOR}

---

### Performance

| Metric | Value |
|--------|-------|
| Total Time | {duration}s |
| Per-CLI Average | {duration / total_tasks}s |
| Parallel Speedup | {sequential_time / duration}x |

---

### Next Steps

{IF rollback_occurred}
1. Review error messages above
2. Fix validation errors
3. Retry skill generation: `/hefesto.create "{skill_name}"`
{ELSE}
1. View generated skill: `/hefesto.show {skill_name}`
2. Validate all CLIs: `/hefesto.validate {skill_name}`
3. Test skill with your AI CLI
{END IF}
```

---

## Variables

| Variable | Type | Description |
|----------|------|-------------|
| `skill_name` | string | Name of generated skill |
| `timestamp` | datetime | ISO 8601 timestamp |
| `duration` | float | Total time in seconds |
| `total_tasks` | integer | Number of target CLIs |
| `successful` | integer | Number of successful tasks |
| `failed` | integer | Number of failed tasks |
| `rollback_occurred` | boolean | Whether rollback was triggered |
| `execution_mode` | string | "parallel" or "sequential" |

---

## Status Icons

| Status | Icon | Description |
|--------|------|-------------|
| success | ✅ | Generation completed successfully |
| failed | ❌ | Generation failed |
| rolled_back | ⚠️ | Rolled back due to sibling failure |
| in_progress | ⏳ | Currently generating |

---

## Example Output (Success)

```markdown
## Skill Generation Report

**Skill Name**: code-review  
**Generated**: 2026-02-05T10:30:00Z  
**Duration**: 2.1s  
**Target CLIs**: 3  
**Execution Mode**: parallel

---

### Summary

✅ Successfully generated skill for 3 CLI(s)

---

### Generation Results

- **claude**: ✅ success
  - Output: .claude/skills/code-review/SKILL.md
  - Duration: 0.8s

- **gemini**: ✅ success
  - Output: .gemini/skills/code-review/SKILL.md
  - Duration: 0.9s

- **opencode**: ✅ success
  - Output: .opencode/skills/code-review/SKILL.md
  - Duration: 0.7s

---

### Performance

| Metric | Value |
|--------|-------|
| Total Time | 2.1s |
| Per-CLI Average | 0.7s |
| Parallel Speedup | 3.2x |

---

### Next Steps

1. View generated skill: `/hefesto.show code-review`
2. Validate all CLIs: `/hefesto.validate code-review`
3. Test skill with your AI CLI
```

---

## Example Output (Failure with Rollback)

```markdown
## Skill Generation Report

**Skill Name**: code-review  
**Generated**: 2026-02-05T10:30:00Z  
**Duration**: 2.3s  
**Target CLIs**: 3  
**Execution Mode**: parallel

---

### Summary

❌ Generation failed. All changes rolled back.

---

### Generation Results

- **claude**: ⚠️ rolled_back
  - Rolled back due to sibling failure

- **gemini**: ❌ failed
  - Error: Validation error - $ARGUMENTS found instead of {{args}}

- **opencode**: ⚠️ rolled_back
  - Rolled back due to sibling failure

---

### Performance

| Metric | Value |
|--------|-------|
| Total Time | 2.3s |
| Per-CLI Average | 0.8s |
| Parallel Speedup | N/A (failed) |

---

### Next Steps

1. Review error messages above
2. Fix validation errors
3. Retry skill generation: `/hefesto.create "code-review"`
```

---

## Related Files

- **Helpers**: `parallel-generator.md`, `rollback-handler.md`
- **Data Model**: [data-model.md](../../specs/004-multi-cli-generator/data-model.md) §5
- **Commands**: `hefesto.create.md`, `hefesto.extract.md`

---

**Version**: 1.0.0 | **Date**: 2026-02-05 | **Feature**: 004-multi-cli-generator
