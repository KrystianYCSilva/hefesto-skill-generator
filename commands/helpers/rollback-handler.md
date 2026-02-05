# Rollback Handler

**Purpose**: Atomic cleanup logic for failed multi-CLI generation  
**Feature**: 004-multi-cli-generator

---

## Overview

The Rollback Handler ensures atomic operations by cleaning up all generated files when any CLI fails. This implements the all-or-nothing guarantee required by FR-011.

**Performance Target**: <100ms cleanup time

---

## Operations

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

**Bash Implementation**:
```bash
rollback_all() {
  local temp_dir="$1"
  
  echo "Rolling back all changes..."
  
  # Delete temp directory
  if [ -d "$temp_dir" ]; then
    rm -rf "$temp_dir"
    echo "✓ Temp directory cleaned up: $temp_dir"
  fi
  
  # Verify deletion
  if [ -d "$temp_dir" ]; then
    echo "⚠️ Warning: Failed to delete temp directory"
    return 1
  fi
  
  echo "✓ Rollback completed"
  return 0
}
```

**PowerShell Implementation**:
```powershell
function Rollback-All {
    param(
        [string]$TempDir
    )
    
    Write-Host "Rolling back all changes..."
    
    # Delete temp directory
    if (Test-Path $TempDir) {
        Remove-Item -Recurse -Force $TempDir
        Write-Host "✓ Temp directory cleaned up: $TempDir"
    }
    
    # Verify deletion
    if (Test-Path $TempDir) {
        Write-Warning "Failed to delete temp directory"
        return $false
    }
    
    Write-Host "✓ Rollback completed"
    return $true
}
```

---

### `verify_no_partial_files(target_clis: list[string], skill_name: string) -> boolean`

**Description**: Verify no partial files exist in target CLI directories after rollback.

**Algorithm**:
```
1. For each target CLI:
   a. Check if skill directory exists: .{cli}/skills/{skill_name}/
   b. If exists: return false (partial files found)
2. Return true (clean state)
```

**Usage**: Called after rollback to verify atomicity

---

### `create_rollback_report(tasks: list[GenerationTask], reason: string) -> RollbackReport`

**Description**: Generate rollback report for user.

**Format**:
```markdown
## Rollback Report

**Reason**: {reason}
**Affected CLIs**: {count}

### Rolled Back
- claude: {status} → rolled_back
- gemini: {status} → rolled_back
- opencode: {status} → rolled_back

### Failed CLI
- gemini: Validation error - $ARGUMENTS found instead of {{args}}

**Action Required**: Fix validation errors and retry generation.
```

---

## Error Handling

### Failed Temp Directory Deletion

```markdown
IF delete_temp_dir() fails:
  1. Log warning
  2. Retry up to 3 times (100ms delay between attempts)
  3. If still fails:
     a. Log temp directory path for manual cleanup
     b. Continue with rollback (mark tasks as rolled_back)
     c. Display warning to user
```

**Rationale**: Rollback should not fail catastrophically - partial cleanup is acceptable

---

### Permission Errors

```markdown
IF permission_denied when deleting temp_dir:
  1. Log error with details
  2. Attempt recursive permission fix (chmod -R +w on Unix)
  3. Retry deletion
  4. If still fails, log path for manual cleanup
```

---

## Performance

| Operation | Target | Typical |
|-----------|--------|---------|
| Temp directory deletion | <100ms | 50-80ms |
| Task status updates | <10ms | 5ms |
| Verification | <50ms | 20-30ms |
| **Total Rollback** | **<200ms** | **100-150ms** |

---

## Usage Example

```bash
# Bash
if [ $validation_failed -eq 1 ]; then
  rollback_all "/tmp/hefesto-12345"
  exit 1
fi
```

```powershell
# PowerShell
if ($validationFailed) {
    Rollback-All "C:\Temp\hefesto-12345"
    exit 1
}
```

---

## Related Files

- **Helpers**: `parallel-generator.md` (calls rollback_all)
- **Data Model**: [data-model.md](../../specs/004-multi-cli-generator/data-model.md) §3
- **Templates**: `generation-report.md`

---

**Version**: 1.0.0 | **Date**: 2026-02-05 | **Feature**: 004-multi-cli-generator
