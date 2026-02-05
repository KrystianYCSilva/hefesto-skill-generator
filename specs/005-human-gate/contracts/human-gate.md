# Contract: Human Gate Module

**Module**: `commands/lib/human_gate.py`  
**Purpose**: Core Human Gate approval workflow (FR-001 to FR-007)  
**Phase**: 1 (Design)

---

## Public API

### `present_human_gate(preview: PreviewObject) -> HumanGateDecision`

**Description**: Display preview and await user decision with timeout

**Parameters**:
- `preview`: PreviewObject - Validated skill preview to display

**Returns**: HumanGateDecision with user's choice

**Raises**:
- `TimeoutError`: If 5 minutes elapse without response (FR-005)
- `ValidationError`: If preview.validation_status != 'valid'

**Behavior**:
1. Display formatted preview (FR-003):
   - File paths for all target CLIs
   - File contents (first 50 lines per clarification)
   - File sizes
   - Validation status
2. Show 4 options: [approve] [expand] [edit] [reject] (FR-004)
3. Start 5-minute timeout timer (FR-005)
4. Await user input
5. Return decision or raise TimeoutError

**Example**:
```python
preview = create_preview(skill_content, target_clis)
decision = present_human_gate(preview)

if decision.decision == 'approve':
    persist_skills(preview)
elif decision.decision == 'reject':
    print("Operation cancelled")
```

---

### `persist_skills(preview: PreviewObject) -> bool`

**Description**: Atomically write skills to all target CLI directories (FR-006)

**Parameters**:
- `preview`: PreviewObject - Approved preview to persist

**Returns**: `True` if all writes succeed

**Raises**:
- `AtomicWriteError`: If any write fails (triggers rollback)
- `BackupError`: If backup creation fails during overwrite

**Behavior**:
1. For each target CLI:
   - Check if skill exists (collision detection)
   - If exists, create backup (FR-023)
   - Write SKILL.md + any resources
2. If ANY write fails:
   - Rollback all writes (Edge Case #4)
   - Restore backups if created
   - Raise AtomicWriteError
3. If all succeed:
   - Log to audit trail (FR-033)
   - Display confirmation with paths (FR-007)
   - Return True

**Example**:
```python
try:
    success = persist_skills(preview)
    print(f"✓ Created skills in {len(preview.target_clis)} CLI directories")
except AtomicWriteError as e:
    print(f"✗ Rollback complete: {e}")
```

---

### `format_preview(preview: PreviewObject) -> str`

**Description**: Format preview for terminal display with ANSI colors

**Parameters**:
- `preview`: PreviewObject - Preview to format

**Returns**: Formatted string with ANSI codes (or plain text if not supported)

**Behavior**:
1. Detect ANSI support (research.md decision #2)
2. Format header with skill name and validation status
3. For each target CLI:
   - Show file path (colored blue)
   - Show file size (colored green)
4. Show content (first 50 lines - clarification)
5. If > 50 lines, add "... [X more lines]" indicator
6. Show options (colored bold)
7. Return formatted string

**Example Output**:
```
=== HUMAN GATE: Skill Preview ===

File: .claude/skills/code-review/SKILL.md
Size: 1234 bytes

File: .gemini/skills/code-review/SKILL.md
Size: 1234 bytes

--- Content ---
---
name: code-review
description: Standardize code reviews
---
...
[truncated after 50 lines]

--- End of Preview ---

Options: [approve] [expand] [edit] [reject]
> 
```

---

## Internal Functions

### `_start_timeout(seconds: int) -> threading.Timer | signal.alarm`

**Description**: Platform-specific timeout mechanism

**Behavior**:
- Unix: Use `signal.alarm(seconds)`
- Windows: Use `threading.Timer(seconds, timeout_handler)`

---

### `_cancel_timeout(timer)`

**Description**: Cancel active timeout

**Behavior**:
- Unix: `signal.alarm(0)`
- Windows: `timer.cancel()`

---

### `_validate_preview(preview: PreviewObject) -> None`

**Description**: Ensure preview is ready for Human Gate

**Raises**:
- `ValidationError`: If preview.validation_status != 'valid'
- `ValidationError`: If preview.target_clis is empty

---

## Error Handling

| Error | Condition | Recovery |
|-------|-----------|----------|
| `TimeoutError` | 5 minutes elapsed | Save wizard state, abort operation |
| `ValidationError` | Invalid preview | Abort, show validation errors |
| `AtomicWriteError` | Persistence failed | Rollback, restore backups, show error |
| `BackupError` | Backup creation failed | Abort overwrite, preserve original |

---

## State Management

Human Gate is **stateless** - state is managed by caller (Wizard or command).

- Preview Object passed in
- Decision returned
- No internal state persisted

---

## Testing Contract

### Unit Tests

- `test_present_human_gate_approve()`: User chooses [approve]
- `test_present_human_gate_reject()`: User chooses [reject]
- `test_present_human_gate_timeout()`: 5 minutes elapse → TimeoutError
- `test_format_preview_ansi()`: ANSI codes applied when supported
- `test_format_preview_plain()`: Plain text when ANSI not supported
- `test_format_preview_truncation()`: 50-line limit enforced

### Integration Tests

- `test_full_approval_flow()`: Preview → approve → persist → confirm
- `test_atomic_rollback()`: Multi-CLI write failure triggers rollback

---

**Contract Status**: ✅ COMPLETE  
**Version**: 1.0.0
