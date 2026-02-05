# Contract: Preview Module

**Module**: `commands/lib/preview.py`  
**Purpose**: Preview generation and formatting for Human Gate display (FR-003)  
**Phase**: 1 (Design)

---

## Public API

### `create_preview(skill_content: str, metadata: str, target_clis: List[str], validation_errors: List[str] = None) -> PreviewObject`

**Description**: Create PreviewObject from validated skill content

**Parameters**:
- `skill_content`: str - Complete SKILL.md content (with frontmatter)
- `metadata`: str - metadata.yaml content
- `target_clis`: List[str] - Target CLI identifiers (e.g., ['claude', 'gemini'])
- `validation_errors`: List[str] | None - Validation errors (empty list if valid)

**Returns**: PreviewObject ready for Human Gate display

**Behavior**:
1. Calculate file sizes:
   - SKILL.md size (bytes)
   - metadata.yaml size (bytes)
   - Total size per CLI
2. Generate file paths for each target CLI:
   - `.{cli}/skills/{skill_name}/SKILL.md`
   - `.{cli}/skills/{skill_name}/metadata.yaml`
3. Determine validation status:
   - 'valid' if validation_errors is empty
   - 'invalid' if validation_errors has items
4. Create PreviewObject with all data
5. Return preview

**Example**:
```python
preview = create_preview(
    skill_content="---\nname: code-review\n...",
    metadata="author: Hefesto...",
    target_clis=['claude', 'gemini'],
    validation_errors=[]
)
# Returns: PreviewObject(skill_name='code-review', validation_status='valid', ...)
```

---

### `format_preview(preview: PreviewObject) -> str`

**Description**: Format preview for terminal display with ANSI colors (FR-003)

**Parameters**:
- `preview`: PreviewObject - Preview to format

**Returns**: Formatted string ready for terminal output

**Behavior**:
1. Detect ANSI support (check `sys.stdout.isatty()` and `TERM` env var)
2. Build formatted output:
   - Header: "=== HUMAN GATE: Skill Preview ===" (bold cyan)
   - Validation status: "✓ Valid" (green) or "✗ Invalid" (red)
   - For each target CLI:
     - File path (blue): `.{cli}/skills/{skill_name}/SKILL.md`
     - File size (green): "{size} bytes" (human-readable)
   - Content section: "--- Content Preview ---" (bold)
   - Truncated content (first 50 lines - FR-003 clarification)
   - Truncation indicator if needed: "... [{X} more lines]" (yellow)
   - Options: "[approve] [expand] [edit] [reject]" (bold white)
3. If ANSI not supported, return plain text version
4. Return formatted string

**Example Output**:
```
=== HUMAN GATE: Skill Preview ===

Status: ✓ Valid

Files to create:
  .claude/skills/code-review/SKILL.md (1.2 KB)
  .claude/skills/code-review/metadata.yaml (345 bytes)
  
  .gemini/skills/code-review/SKILL.md (1.2 KB)
  .gemini/skills/code-review/metadata.yaml (345 bytes)

Total: 2 CLIs, 4 files, 3.5 KB

--- Content Preview ---
---
name: code-review
description: Standardize code reviews following best practices
---

# Code Review Skill

## Purpose
[content continues...]

... [127 more lines]

--- End of Preview ---

Options: [approve] [expand] [edit] [reject]
> 
```

---

### `truncate_content(content: str, max_lines: int = 50) -> Tuple[str, int, bool]`

**Description**: Truncate skill content to first N lines with metadata (FR-003)

**Parameters**:
- `content`: str - Full skill content
- `max_lines`: int - Maximum lines to display (default: 50)

**Returns**: Tuple of (truncated_content, total_lines, was_truncated)

**Behavior**:
1. Split content into lines
2. Count total lines
3. If total <= max_lines:
   - Return (original_content, total_lines, False)
4. If total > max_lines:
   - Take first max_lines
   - Calculate remaining: total_lines - max_lines
   - Return (truncated_content, total_lines, True)

**Example**:
```python
truncated, total, was_truncated = truncate_content(skill_content, max_lines=50)
# Returns: ("---\nname: code-review\n...[50 lines]", 177, True)

if was_truncated:
    print(f"... [{total - 50} more lines]")
```

---

### `calculate_file_size(content: str) -> int`

**Description**: Calculate file size in bytes for preview display

**Parameters**:
- `content`: str - File content

**Returns**: Size in bytes

**Behavior**:
1. Encode content as UTF-8
2. Return byte length

---

### `format_file_size(size_bytes: int) -> str`

**Description**: Format file size for human-readable display

**Parameters**:
- `size_bytes`: int - Size in bytes

**Returns**: Formatted string (e.g., "1.2 KB", "345 bytes")

**Behavior**:
1. If < 1024 bytes: "{size} bytes"
2. If < 1024*1024 bytes: "{size/1024:.1f} KB"
3. If >= 1024*1024 bytes: "{size/(1024*1024):.1f} MB"
4. Return formatted string

**Example**:
```python
format_file_size(345) → "345 bytes"
format_file_size(1234) → "1.2 KB"
format_file_size(1234567) → "1.2 MB"
```

---

## Data Classes

### `PreviewObject`

**Attributes**:
- `skill_name`: str - Sanitized skill name
- `skill_content`: str - Full SKILL.md content
- `metadata_content`: str - Full metadata.yaml content
- `target_clis`: List[str] - List of target CLI identifiers
- `validation_status`: str - 'valid' or 'invalid'
- `validation_errors`: List[str] - Validation error messages (empty if valid)
- `file_paths`: Dict[str, List[Path]] - Mapping CLI → list of file paths
- `file_sizes`: Dict[str, int] - Mapping file path → size in bytes
- `timestamp`: str - Preview creation timestamp (ISO8601)
- `resources`: List[ResourceInfo] - Optional JIT resources (scripts, references, assets)

**Example**:
```python
@dataclass
class PreviewObject:
    skill_name: str
    skill_content: str
    metadata_content: str
    target_clis: List[str]
    validation_status: str  # 'valid' | 'invalid'
    validation_errors: List[str]
    file_paths: Dict[str, List[Path]]
    file_sizes: Dict[str, int]
    timestamp: str
    resources: List[ResourceInfo] = field(default_factory=list)
    
    def total_size(self) -> int:
        """Calculate total size across all files"""
        return sum(self.file_sizes.values())
    
    def total_files(self) -> int:
        """Count total files to be created"""
        return sum(len(paths) for paths in self.file_paths.values())
```

---

### `ResourceInfo`

**Attributes**:
- `resource_type`: str - One of: 'scripts', 'references', 'assets'
- `filename`: str - Resource filename
- `content`: str | None - Resource content (for scripts/references)
- `path`: Path | None - Resource path (for assets)
- `size`: int - Resource size in bytes

**Example**:
```python
@dataclass
class ResourceInfo:
    resource_type: str  # 'scripts' | 'references' | 'assets'
    filename: str
    content: str | None
    path: Path | None
    size: int
```

---

## Internal Functions

### `_detect_ansi_support() -> bool`

**Description**: Detect if terminal supports ANSI color codes

**Behavior**:
1. Check if stdout is TTY (`sys.stdout.isatty()`)
2. Check TERM environment variable != 'dumb'
3. On Windows: Check if Windows 10+ with ANSI enabled
4. Return True if supported, False otherwise

---

### `_apply_color(text: str, color_code: str, supports_ansi: bool) -> str`

**Description**: Apply ANSI color code if supported

**Parameters**:
- `text`: str - Text to colorize
- `color_code`: str - ANSI escape code (e.g., '\033[32m' for green)
- `supports_ansi`: bool - Whether terminal supports ANSI

**Returns**: Colored text or plain text

**Behavior**:
- If supports_ansi: `{color_code}{text}\033[0m`
- Else: `text`

---

### `_extract_skill_name(skill_content: str) -> str`

**Description**: Extract skill name from frontmatter

**Behavior**:
1. Parse YAML frontmatter (between `---`)
2. Extract `name` field
3. Return skill name or raise error if missing

---

## ANSI Color Codes Reference

```python
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'
```

**Usage**:
- Success indicators: GREEN
- Error indicators: RED
- File paths: BLUE
- File sizes: GREEN
- Section headers: BOLD + CYAN
- Truncation indicator: YELLOW
- Options prompt: BOLD + WHITE

---

## Error Handling

| Error | Condition | Recovery |
|-------|-----------|----------|
| `ValueError` | Missing skill name in frontmatter | Raise with clear message |
| `UnicodeError` | Content encoding issues | Try multiple encodings, fallback to 'utf-8' with errors='replace' |

---

## Integration Points

### With Human Gate (`commands/lib/human_gate.py`)

```python
# Create preview before Human Gate
preview = create_preview(
    skill_content=generated_skill,
    metadata=generated_metadata,
    target_clis=['claude', 'gemini', 'opencode'],
    validation_errors=validation_result
)

# Format and display in Human Gate
formatted = format_preview(preview)
print(formatted)

# Present to user
decision = present_human_gate(preview)
```

### With Expansion (`commands/lib/expansion.py`)

```python
# After resources added via [expand]
preview.resources.append(ResourceInfo(
    resource_type='scripts',
    filename='validate.sh',
    content=script_content,
    path=None,
    size=len(script_content.encode('utf-8'))
))

# Update file_paths and file_sizes
for cli in preview.target_clis:
    resource_path = Path(f".{cli}/skills/{preview.skill_name}/scripts/validate.sh")
    preview.file_paths[cli].append(resource_path)
    preview.file_sizes[str(resource_path)] = preview.resources[-1].size

# Re-display preview
formatted = format_preview(preview)
print(formatted)
```

---

## Testing Contract

### Unit Tests

- `test_create_preview_valid()`: Valid content → validation_status='valid'
- `test_create_preview_invalid()`: With errors → validation_status='invalid', errors list populated
- `test_truncate_content_short()`: 30 lines → not truncated, was_truncated=False
- `test_truncate_content_long()`: 177 lines → truncated to 50, was_truncated=True
- `test_format_file_size_bytes()`: 345 → "345 bytes"
- `test_format_file_size_kb()`: 1234 → "1.2 KB"
- `test_format_file_size_mb()`: 1234567 → "1.2 MB"
- `test_detect_ansi_support_tty()`: TTY terminal → True
- `test_detect_ansi_support_pipe()`: Piped output → False
- `test_format_preview_ansi()`: ANSI enabled → colored output
- `test_format_preview_plain()`: ANSI disabled → plain text

### Integration Tests

- `test_preview_to_human_gate()`: create_preview → format_preview → present_human_gate
- `test_preview_with_resources()`: Add resources → preview updates → formatted correctly
- `test_multi_cli_preview()`: 3 CLIs → all file paths shown, total size correct

---

**Contract Status**: ✅ COMPLETE  
**Version**: 1.0.0
