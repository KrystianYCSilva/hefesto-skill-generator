# Contract: Collision Module

**Module**: `commands/lib/collision.py`  
**Purpose**: Collision detection and resolution for existing skills (FR-020 to FR-025)  
**Phase**: 1 (Design)

---

## Public API

### `detect_collisions(skill_name: str, target_clis: List[str]) -> Dict[str, CollisionInfo]`

**Description**: Detect if skill with same name exists in any target CLI directory

**Parameters**:
- `skill_name`: str - Sanitized skill name to check
- `target_clis`: List[str] - List of CLI identifiers (e.g., ['claude', 'gemini', 'opencode'])

**Returns**: Dictionary mapping CLI name to CollisionInfo for each collision detected

**Behavior**:
1. For each CLI in target_clis:
   - Check if `.{cli}/skills/{skill_name}/SKILL.md` exists
   - If exists, extract metadata (created_date, modified_date, author, version)
   - Build CollisionInfo object
2. Return dictionary of collisions (empty dict if none)

**Example**:
```python
collisions = detect_collisions('code-review', ['claude', 'gemini', 'opencode'])
# Returns: {
#   'claude': CollisionInfo(skill_name='code-review', created='2026-01-15', ...),
#   'gemini': CollisionInfo(skill_name='code-review', created='2026-01-20', ...)
# }
```

---

### `prompt_collision_resolution(collisions: Dict[str, CollisionInfo]) -> CollisionDecision`

**Description**: Prompt user to resolve collision with overwrite/merge/cancel options (FR-022)

**Parameters**:
- `collisions`: Dict[str, CollisionInfo] - Detected collisions from detect_collisions()

**Returns**: CollisionDecision with user's choice

**Behavior**:
1. Display collision warning with skill name
2. For each collision, display metadata (FR-021):
   - Existing location (file path)
   - Created date
   - Last modified date
   - Author (if available in frontmatter)
   - Version (if available)
3. Show 3 options: `[overwrite]` `[merge]` `[cancel]` (FR-022)
4. Await user input
5. Return CollisionDecision

**Example Output**:
```
⚠️  COLLISION DETECTED: Skill 'code-review' already exists

Existing skill locations:
  .claude/skills/code-review/SKILL.md
    Created: 2026-01-15
    Modified: 2026-02-01
    Version: 1.0.0
  
  .gemini/skills/code-review/SKILL.md
    Created: 2026-01-20
    Modified: 2026-01-25
    Version: 1.1.0

Resolution options:
  [overwrite] - Replace existing skill (creates backup)
  [merge]     - Selectively merge changes
  [cancel]    - Abort operation

Choose action: 
```

---

### `handle_overwrite(collisions: Dict[str, CollisionInfo], new_content: str) -> BackupResult`

**Description**: Create backups and prepare for overwrite (FR-023)

**Parameters**:
- `collisions`: Dict[str, CollisionInfo] - Skills to be overwritten
- `new_content`: str - New skill content (for validation)

**Returns**: BackupResult with backup paths

**Raises**:
- `BackupError`: If backup creation fails (Edge Case #5)

**Behavior**:
1. For each collision:
   - Create `.tar.gz` backup of entire skill directory
   - Backup path: `.hefesto/backups/{skill-name}-{ISO8601-timestamp}.tar.gz`
   - Use atomic temp file + rename pattern
2. If ANY backup fails:
   - Cleanup partial backups
   - Raise BackupError (abort overwrite, preserve originals)
3. If all succeed:
   - Return BackupResult with all backup paths
   - Log backup creation to audit trail (FR-033)

**Example**:
```python
try:
    backup_result = handle_overwrite(collisions, new_skill_content)
    print(f"✓ Backups created: {backup_result.paths}")
    # Safe to proceed with overwrite
except BackupError as e:
    print(f"✗ Backup failed: {e}. Original skills preserved.")
```

---

### `handle_merge(existing_path: Path, new_content: str) -> str`

**Description**: Guide user through section-by-section merge (FR-024)

**Parameters**:
- `existing_path`: Path - Path to existing SKILL.md
- `new_content`: str - New skill content to merge

**Returns**: Merged skill content as string

**Behavior**:
1. Load existing skill content from file
2. Extract sections from both existing and new content:
   - Frontmatter (between `---`)
   - Each heading section (# or ##)
3. For each section that differs:
   - Display unified diff for that section
   - Prompt user: `Keep [existing] or use [new]?`
   - Collect user choice
4. Reconstruct merged skill from user choices
5. Return merged content string

**Example Flow**:
```
=== Section: frontmatter ===
- version: 1.0.0
+ version: 1.1.0

Keep [existing] or use [new]? new

=== Section: Usage ===
- Old usage instructions...
+ Updated usage instructions...

Keep [existing] or use [new]? existing

[Continues for all changed sections...]
```

---

### `get_skill_metadata(skill_path: Path) -> Dict[str, Any]`

**Description**: Extract metadata from existing skill frontmatter (FR-021)

**Parameters**:
- `skill_path`: Path - Path to SKILL.md file

**Returns**: Dictionary with metadata keys

**Behavior**:
1. Read SKILL.md file
2. Parse YAML frontmatter (between `---`)
3. Extract fields:
   - `created`: Created date (from frontmatter or file stat)
   - `modified`: Last modified date (file stat)
   - `author`: Author name (from frontmatter metadata)
   - `version`: Version string (from frontmatter)
4. Return dict with available metadata (missing keys have None)

**Example**:
```python
metadata = get_skill_metadata(Path('.claude/skills/code-review/SKILL.md'))
# Returns: {
#   'created': '2026-01-15',
#   'modified': '2026-02-01',
#   'author': 'Hefesto Skill Generator',
#   'version': '1.0.0'
# }
```

---

## Data Classes

### `CollisionInfo`

**Attributes**:
- `skill_name`: str - Name of colliding skill
- `cli_name`: str - CLI where collision detected
- `skill_path`: Path - Full path to existing SKILL.md
- `created_date`: str | None - Created date (ISO8601 or human-readable)
- `modified_date`: str - Last modified date (ISO8601)
- `author`: str | None - Author from frontmatter
- `version`: str | None - Version from frontmatter
- `file_size`: int - Size of SKILL.md in bytes

**Example**:
```python
@dataclass
class CollisionInfo:
    skill_name: str
    cli_name: str
    skill_path: Path
    created_date: str | None
    modified_date: str
    author: str | None
    version: str | None
    file_size: int
```

---

### `CollisionDecision`

**Attributes**:
- `decision`: str - One of: 'overwrite', 'merge', 'cancel'
- `timestamp`: str - Decision timestamp (ISO8601)
- `affected_clis`: List[str] - List of CLIs involved

**Example**:
```python
@dataclass
class CollisionDecision:
    decision: str  # 'overwrite' | 'merge' | 'cancel'
    timestamp: str
    affected_clis: List[str]
```

---

### `BackupResult`

**Attributes**:
- `success`: bool - Whether all backups succeeded
- `backup_paths`: Dict[str, Path] - Mapping CLI name → backup file path
- `timestamp`: str - Backup timestamp (ISO8601)
- `total_size`: int - Total size of all backups in bytes

**Example**:
```python
@dataclass
class BackupResult:
    success: bool
    backup_paths: Dict[str, Path]
    timestamp: str
    total_size: int
```

---

## Internal Functions

### `_create_backup_tarfile(skill_dir: Path, backup_path: Path) -> None`

**Description**: Create .tar.gz backup of skill directory

**Behavior**:
1. Create temp file: `backup_path.with_suffix('.tar.gz.tmp')`
2. Use tarfile.open() in 'w:gz' mode
3. Add entire skill directory to archive
4. Atomic rename: temp → final backup path
5. If any step fails, cleanup temp file and raise BackupError

---

### `_extract_sections(markdown_content: str) -> List[Tuple[str, str]]`

**Description**: Split markdown into sections for diffing

**Returns**: List of (section_name, content) tuples

**Behavior**:
1. Extract frontmatter as first section (between `---`)
2. Split remaining content by heading markers (# or ##)
3. Return ordered list of sections

---

### `_display_section_diff(section_name: str, existing: str, new: str) -> None`

**Description**: Display unified diff for one section

**Behavior**:
1. Use difflib.unified_diff() to generate diff
2. Print section name header
3. Print diff lines (+ for additions, - for deletions)
4. Format for terminal readability

---

### `_reconstruct_markdown(sections: Dict[str, str]) -> str`

**Description**: Rebuild markdown from section dictionary

**Behavior**:
1. Start with frontmatter section
2. Append body sections in original order
3. Preserve spacing between sections
4. Return complete markdown string

---

## Error Handling

| Error | Condition | Recovery |
|-------|-----------|----------|
| `BackupError` | Backup creation fails | Abort overwrite, preserve original (FR-023, Edge Case #5) |
| `FileNotFoundError` | Existing skill path invalid | Log warning, skip that CLI in collision check |
| `YAMLError` | Frontmatter parse fails | Use file stat dates, set author/version to None |

---

## Integration Points

### With Human Gate (`commands/lib/human_gate.py`)

Before presenting Human Gate:
```python
# In hefesto_create_impl.py, before Human Gate
collisions = detect_collisions(skill_name, target_clis)

if collisions:
    decision = prompt_collision_resolution(collisions)
    
    if decision.decision == 'cancel':
        print("Operation cancelled. Original skill preserved.")
        return 1
    
    elif decision.decision == 'overwrite':
        backup_result = handle_overwrite(collisions, skill_content)
        # Proceed to Human Gate with original content
    
    elif decision.decision == 'merge':
        # Merge each collision
        for cli, collision_info in collisions.items():
            merged_content = handle_merge(collision_info.skill_path, skill_content)
        skill_content = merged_content  # Update content
        # Proceed to Human Gate with merged content

# Continue to Human Gate
decision = present_human_gate(preview)
```

---

## Testing Contract

### Unit Tests

- `test_detect_collisions_none()`: No existing skills → empty dict
- `test_detect_collisions_single()`: One CLI has collision → dict with 1 entry
- `test_detect_collisions_multiple()`: Multiple CLIs → dict with N entries
- `test_get_skill_metadata_full()`: Frontmatter with all fields
- `test_get_skill_metadata_minimal()`: Missing fields → None values
- `test_create_backup_success()`: Backup created, atomic rename
- `test_create_backup_failure()`: Backup fails → BackupError raised, temp cleanup
- `test_extract_sections()`: Markdown → [(name, content), ...]
- `test_reconstruct_markdown()`: Sections → valid markdown

### Integration Tests

- `test_collision_overwrite_flow()`: Detect → prompt overwrite → backup → persist
- `test_collision_merge_flow()`: Detect → prompt merge → diff → merge → persist
- `test_collision_cancel_flow()`: Detect → prompt cancel → abort, original preserved
- `test_backup_rollback()`: Multi-CLI write fails → backups restored (Edge Case #4)

---

**Contract Status**: ✅ COMPLETE  
**Version**: 1.0.0
