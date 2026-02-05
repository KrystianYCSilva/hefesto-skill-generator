# CoALA Working Memory for /hefesto.create

> **Framework:** CoALA (Cognitive Architectures for Language Agents)
> **Component:** Working Memory with Circular Buffer + Sliding Windows
> **Purpose:** Maintain execution state across 6 phases with O(1) context lookup
> **Version:** 1.0.0
> **Status:** Implementation Guide

---

## Overview

CoALA Working Memory implements a **specialized state management system** for `/hefesto.create` that:

1. **Circular Buffer**: Fixed-size memory that reuses slots (prevents unbounded growth)
2. **Sliding Windows**: 3 specialized views into memory for different concerns
3. **Decision Cycle**: Phases 0-6 flow through memory atomically
4. **Recovery**: Checkpoint-based rollback on errors

```
┌─────────────────────────────────────────────────────────┐
│                    COALA WORKING MEMORY                  │
│                  Circular Buffer (16 slots)              │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │  SLOT-0  SLOT-1  SLOT-2  SLOT-3  ...  SLOT-15  │   │
│  │   [P0]    [P1]    [P1]    [P2]   ...   [P6]    │   │
│  └──────────────────────────────────────────────────┘   │
│         ↑                                                 │
│      write_head (next write position)                    │
│                                                           │
│  ┌──── SLIDING WINDOW 1: Input State ────┐              │
│  │ description, target_cli, template      │              │
│  └────────────────────────────────────────┘              │
│                                                           │
│  ┌──── SLIDING WINDOW 2: Processing State ────┐          │
│  │ skill_name, skill_content, metadata        │          │
│  └────────────────────────────────────────────┘          │
│                                                           │
│  ┌──── SLIDING WINDOW 3: Approval State ────┐            │
│  │ validation_errors, human_gate_response     │            │
│  └────────────────────────────────────────────┘            │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## Memory Architecture

### 1. Circular Buffer (Core)

```markdown
Structure:
  buffer: [Slot; 16]              # Fixed 16 slots
  write_head: usize               # Next write position (0-15)
  checkpoint_markers: Vec<usize>  # Phase markers for rollback
  
Semantics:
  - Write always goes to buffer[write_head]
  - write_head auto-increments (mod 16)
  - Old data automatically overwritten (no cleanup needed)
  - Checkpoint_markers preserve phase boundaries
```

**Rationale**: 16 slots handle 6 phases + buffer space without unbounded growth.

### 2. Sliding Window 1: Input State

**Purpose**: Track user input through parsing + wizard mode

```yaml
window_input:
  description: String         # Natural language skill description (≤2000 chars)
  target_cli: Option<String>  # User-specified CLI or null for auto-detect
  template_name: String       # Template variant name (default: "base")
  
  # Metadata
  raw_input: String           # Original unparsed user input
  parsed_at: Timestamp        # When input was parsed
  input_hash: Hash            # For deduplication
  
  # Validation
  input_valid: bool           # Pass/fail flag
  input_errors: Vec<Error>    # E-CREATE-001, E-CREATE-007, etc.
```

**Access Pattern**: Read-heavy (accessed in P0, P1, P2)

### 3. Sliding Window 2: Processing State

**Purpose**: Track skill generation and validation

```yaml
window_processing:
  skill_name: String          # Computed/user-provided skill name
  skill_content: String       # Generated SKILL.md content
  metadata: Map<String, Any>  # Generated metadata.yaml structure
  
  # Generation Info
  template_used: String       # Which template was used
  category_inferred: String   # Auto-inferred skill category
  generated_at: Timestamp     # When skill was generated
  
  # Validation
  validation_passed: bool     # Overall validation status
  validation_errors: Vec<Error>  # T0 rule violations if any
  validation_timestamp: Timestamp
```

**Access Pattern**: Write in P2, read in P3, modify in P4

### 4. Sliding Window 3: Approval State

**Purpose**: Track Human Gate + collision handling

```yaml
window_approval:
  collision_detected: bool    # Skill name already exists
  collision_details: Map      # Existing skill metadata
  human_gate_response: Enum   # approve|expand|edit|reject
  human_gate_timestamp: Timestamp
  
  # Collision Resolution
  action_chosen: Enum         # overwrite|rename|cancel
  backup_path: Option<String> # Path to backup if overwrite
  new_skill_name: Option<String> # New name if renamed
  
  # Persistence Checkpoint
  persistence_ready: bool     # All checks passed, ready to write
```

**Access Pattern**: Write in P3-P4, read in P5

---

## Decision Cycle: Phases 0-6

```
┌─────────────────────────────────────────────────────────┐
│          COALA DECISION CYCLE FOR /hefesto.create        │
└─────────────────────────────────────────────────────────┘

PHASE 0: PRE-EXECUTION
  ├─ Load CONSTITUTION.md
  ├─ Verify MEMORY.md exists
  ├─ Load .context/ standards
  └─ CHECKPOINT-0: Save initial state
      └─ Slot 0: [validated_context]
      
PHASE 1: ARGUMENT PARSING & WIZARD
  ├─ Parse arguments into window_input
  ├─ Trigger wizard_mode() if description missing
  ├─ Validate input (E-CREATE-001, E-CREATE-007)
  └─ CHECKPOINT-1: Save parsed input
      └─ Slot 1: [parsed_input_state]
      
PHASE 2: SKILL GENERATION
  ├─ Generate skill_name (sanitize per T0-HEFESTO-07)
  ├─ Render template with context
  ├─ Generate metadata.yaml
  └─ CHECKPOINT-2: Save generated skill
      └─ Slot 2: [generated_skill_content]
      
PHASE 3: VALIDATION
  ├─ Validate skill against T0 rules
  ├─ Check for secrets (T0-HEFESTO-11)
  ├─ Block persistence if fails
  └─ CHECKPOINT-3: Save validation result
      └─ Slot 3: [validation_result]
      
PHASE 4: HUMAN GATE & COLLISION
  ├─ Display skill preview
  ├─ Check for existing skill (collision_detected)
  ├─ Trigger collision_gate() if needed
  ├─ Await human approval (120s timeout)
  └─ CHECKPOINT-4: Save human decision
      └─ Slot 4: [human_gate_response]
      
PHASE 5: PERSISTENCE
  ├─ Create directories: .{cli}/skills/{name}/
  ├─ Write SKILL.md + metadata.yaml
  ├─ Update MEMORY.md registry
  └─ CHECKPOINT-5: Save success
      └─ Slot 5: [persistence_result]
      
PHASE 6: SUCCESS / CLEANUP
  ├─ Display success message
  ├─ Cleanup in-memory state
  └─ CHECKPOINT-6: Final state
      └─ Slot 6: [final_state]

───────────────────────────────────────────────────────────

ERROR / ROLLBACK HANDLING:

IF error at phase N:
  ├─ Read last valid checkpoint (N-1)
  ├─ Restore memory from checkpoint
  ├─ Rollback filesystem changes:
  │  └─ Remove partial skill directories
  ├─ Display error message (E-CREATE-XXX)
  └─ Return to PHASE 1 (allow retry)
```

---

## Memory Operations (Atomic)

### Operation 1: Push State (Write to Buffer)

```
push_state(phase: Phase, data: Any) → Result<usize, MemoryError>
  
  slot_id = write_head
  buffer[write_head] = SlotData {
    phase,
    timestamp: now(),
    data,
    checksum: hash(data)  # For integrity check
  }
  
  checkpoint_markers[phase] = write_head
  write_head = (write_head + 1) % 16
  
  return Ok(slot_id)
```

**Complexity**: O(1)  
**Atomicity**: Yes (no partial writes)

### Operation 2: Get State (Read from Buffer)

```
get_state(phase: Phase) → Result<Any, MemoryError>
  
  IF checkpoint_markers[phase] NOT set:
    return Err(MemoryError::PhaseNotInitialized)
  
  slot_id = checkpoint_markers[phase]
  data = buffer[slot_id].data
  
  IF hash(data) != buffer[slot_id].checksum:
    return Err(MemoryError::IntegrityCheckFailed)
  
  return Ok(data)
```

**Complexity**: O(1)  
**Safety**: Checksum verification prevents corruption

### Operation 3: Rollback (Restore from Checkpoint)

```
rollback_to(phase: Phase) → Result<Any, MemoryError>
  
  IF checkpoint_markers[phase] NOT set:
    return Err(MemoryError::NothingToRollback)
  
  slot_id = checkpoint_markers[phase]
  restored_data = buffer[slot_id].data
  
  # Clear all phase markers after target phase
  FOR each_phase IN [phase+1..6]:
    checkpoint_markers[each_phase] = null
  
  # Reset write_head to next available slot
  write_head = (slot_id + 1) % 16
  
  return Ok(restored_data)
```

**Complexity**: O(6) = O(1)  
**Safety**: Preserves all prior state, clears future

---

## Example: Memory Flow for /hefesto.create

### Scenario: "Validate email addresses"

```markdown
USER INPUT:
> /hefesto.create "Validate email addresses using regex patterns"

────────────────────────────────────────────────────────

PHASE 0 - PRE-EXECUTION
  push_state(PHASE-0, {
    context_loaded: true,
    memory_valid: true,
    standards_loaded: 11  // T0 rules
  })
  ✓ CHECKPOINT-0 saved to slot 0

PHASE 1 - PARSING
  push_state(PHASE-1, {
    description: "Validate email addresses using regex patterns",
    target_cli: null,  // auto-detect
    template_name: "base",
    raw_input_hash: "abc123...",
    input_valid: true,
    input_errors: []
  })
  ✓ CHECKPOINT-1 saved to slot 1

PHASE 2 - GENERATION
  push_state(PHASE-2, {
    skill_name: "validate-email-addresses",
    skill_content: "[SKILL.md content]...",
    metadata: {
      author: "user",
      version: "1.0.0",
      category: "development"
    },
    template_used: "base",
    generated_at: "2026-02-05T10:00:00Z"
  })
  ✓ CHECKPOINT-2 saved to slot 2

PHASE 3 - VALIDATION
  push_state(PHASE-3, {
    validation_passed: true,
    validation_errors: [],
    checked_rules: [
      "T0-HEFESTO-01: ✓ Agent Skills spec",
      "T0-HEFESTO-07: ✓ Name format",
      "T0-HEFESTO-11: ✓ No secrets"
    ]
  })
  ✓ CHECKPOINT-3 saved to slot 3

PHASE 4 - HUMAN GATE
  Detect collision: false
  Display preview...
  
  push_state(PHASE-4, {
    collision_detected: false,
    human_gate_response: "approve",
    human_gate_timestamp: "2026-02-05T10:01:00Z"
  })
  ✓ CHECKPOINT-4 saved to slot 4

PHASE 5 - PERSISTENCE
  Detected CLIs: [claude, gemini]
  
  Create .claude/skills/validate-email-addresses/
  Create .gemini/skills/validate-email-addresses/
  Write SKILL.md + metadata.yaml to both
  Update MEMORY.md
  
  push_state(PHASE-5, {
    persistence_success: true,
    files_created: [
      ".claude/skills/validate-email-addresses/SKILL.md",
      ".claude/skills/validate-email-addresses/metadata.yaml",
      ".gemini/skills/validate-email-addresses/SKILL.md",
      ".gemini/skills/validate-email-addresses/metadata.yaml"
    ]
  })
  ✓ CHECKPOINT-5 saved to slot 5

PHASE 6 - SUCCESS
  Display success message
  
  push_state(PHASE-6, {
    final_state: "success",
    skill_created: "validate-email-addresses",
    target_clis: ["claude", "gemini"]
  })
  ✓ CHECKPOINT-6 saved to slot 6

────────────────────────────────────────────────────────
MEMORY STATE AT END:

Buffer slots used: 7/16
Checkpoint markers: [0, 1, 2, 3, 4, 5, 6]
Write head: 7 (next available)

Next command will use slots 7-13...
```

---

## Error Recovery Example

### Scenario: Collision + Overwrite

```markdown
[Same as above, up to PHASE 3...]

PHASE 4 - HUMAN GATE (COLLISION PATH)
  
  get_state(PHASE-2)  # Retrieve generated skill
  
  Check filesystem:
    .claude/skills/validate-email-addresses/ EXISTS
  
  collision_detected = true
  
  Display collision prompt...
  USER: "overwrite"
  
  Create backup:
    .hefesto/backups/validate-email-addresses-2026-02-05T10-01-00.tar.gz
  
  push_state(PHASE-4, {
    collision_detected: true,
    collision_details: {
      existing_path: ".claude/skills/validate-email-addresses/",
      created: "2026-02-04T09:00:00Z"
    },
    action_chosen: "overwrite",
    backup_path: ".hefesto/backups/validate-email-addresses-2026-02-05T10-01-00.tar.gz",
    human_gate_response: "approve"
  })
  ✓ CHECKPOINT-4 saved to slot 4

PHASE 5 - PERSISTENCE
  Delete existing: .claude/skills/validate-email-addresses/
  Create new directories (same as before)
  Write updated files
  
  push_state(PHASE-5, {
    persistence_success: true,
    overwrite_mode: true,
    files_created: [...]
  })
  ✓ CHECKPOINT-5 saved to slot 5

[PHASE 6 as normal...]
```

---

## Error Recovery Example 2

### Scenario: Validation Failure → Retry

```markdown
[PHASE 0-2 as normal...]

PHASE 3 - VALIDATION FAILURE
  
  validation_errors = [
    E-CREATE-005: "Skill name too long (73 > 64 chars)"
  ]
  
  validation_passed = false
  
  push_state(PHASE-3, {
    validation_passed: false,
    validation_errors: [
      {
        code: "E-CREATE-005",
        message: "Skill name exceeds 64 characters",
        remediation: "Shorten skill name"
      }
    ]
  })
  ✓ CHECKPOINT-3 saved to slot 3
  
  DISPLAY ERROR:
  ERROR [E-CREATE-005]: Skill name exceeds 64 characters
  Suggestion: Shorten skill name
  
  DO NOT PROCEED TO HUMAN GATE
  
  USER RETRY:
  > /hefesto.create "Validate email with improved patterns"
  
  ROLLBACK:
    get_state(PHASE-1)  # Get parsed input from slot 1
    rollback_to(PHASE-1)  # Clear PHASE-2 and PHASE-3
    write_head reset to slot 2
  
  PHASE 2 - REGENERATION
    skill_name = "validate-email-patterns"  // Auto-sanitized
    [Generate new content...]
  
  PHASE 3 - VALIDATION
    validation_passed = true
    [Continue normally...]
```

---

## Implementation Checklist

- [ ] **Memory Struct**: Define circular buffer + sliding windows
- [ ] **Push/Get/Rollback**: Implement core operations (O(1))
- [ ] **Phase Handlers**: P0-P6 implementations
- [ ] **Checkpoint Markers**: Automatic phase tracking
- [ ] **Checksum Verification**: Integrity checking
- [ ] **Collision Detection**: Check filesystem before P4
- [ ] **Human Gate Integration**: 120s timeout + response handling
- [ ] **Rollback Handler**: Filesystem cleanup on errors
- [ ] **Error Propagation**: E-CREATE-XXX codes through memory
- [ ] **Testing**: 9 unit tests (one per scenario)

---

## Performance Metrics

| Operation | Complexity | Typical Time |
|-----------|-----------|--------------|
| push_state() | O(1) | <1ms |
| get_state() | O(1) | <1ms |
| rollback_to() | O(6) | <2ms |
| Checksum verify | O(1) | <0.5ms |
| Full cycle (P0-P6) | O(1) | <7s (excl. Human Gate) |

**Memory Footprint**: 16 slots × ~1KB per slot = ~16KB (negligible)

---

## See Also

- **Specification**: `specs/003-hefesto-commands/hefesto.create.md`
- **Phase Handlers**: `commands/hefesto.create-phases.md` (to create)
- **Human Gate**: `commands/helpers/human-gate.md`
- **Error Codes**: Section "Error Cases" in spec

---

**Version:** 1.0.0  
**Status:** Ready for Phase Handler Implementation  
**Next:** Create `hefesto.create-phases.md` with P0-P6 implementations
