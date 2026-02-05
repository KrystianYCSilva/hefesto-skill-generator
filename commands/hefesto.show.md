---
description: "Display full content and metadata of a specific skill (read-only)"
command: "/hefesto.show"
category: "information"
user_story: "US4"
priority: "P2"
version: "1.0.0"
---

# /hefesto.show - Show Skill Command

**Command**: `/hefesto.show`  
**Purpose**: Display full content and metadata of a skill (read-only)  
**User Story**: US4 - Management & Help (P2)

---

## Overview

The `/hefesto.show` command displays complete skill content in formatted output. Features:

1. **Read-Only**: No filesystem modifications
2. **Formatted Display**: Pretty-printed metadata and content
3. **Multi-CLI Support**: Show from specific CLI when skill exists in multiple
4. **Flexible Output**: Full content, metadata-only, or body-only
5. **Fast**: < 200ms for typical skill (SC-002)

**Target Performance**: < 200ms (< 2s requirement)

---

## Command Signature

```text
/hefesto.show <skill_name> [--cli <name>] [--metadata-only] [--body-only]

Arguments:
  skill_name      Name of skill to display (required)

Options:
  --cli <name>         Show from specific CLI directory
  --metadata-only      Show only metadata.yaml
  --body-only          Show only SKILL.md body (skip metadata)
```

---

## Execution Workflow

### Phase 0: Pre-Execution Validation

```markdown
1. Validate CONSTITUTION
   (see: helpers/constitution-validator.md)
   IF invalid → ABORT

2. Check Hefesto initialization
   IF NOT file_exists("MEMORY.md"):
     DISPLAY: "❌ Hefesto not initialized. Run /hefesto.init first."
     ABORT (exit code 1)

3. Parse arguments
   skill_name = args.positional[0] OR null
   
   IF skill_name IS null:
     ERROR: "Missing required argument: skill_name"
     SUGGEST: "Usage: /hefesto.show <skill_name>"
     ABORT
```

**Performance Target**: < 50ms

---

### Phase 1: Skill Discovery

```markdown
1. Load CLI detection
   detected_clis = read_memory_md().detected_clis
   cli_filter = args.flags.get("cli") OR null

2. Search for skill
   found_locations = []
   
   IF cli_filter IS provided:
     # Search in specific CLI only
     skill_path = ".{cli_filter}/skills/{skill_name}/SKILL.md"
     IF file_exists(skill_path):
       found_locations.append({
         cli: cli_filter,
         path: skill_path
       })
   
   ELSE:
     # Search in all detected CLIs
     FOR EACH cli IN detected_clis:
       skill_path = ".{cli}/skills/{skill_name}/SKILL.md"
       IF file_exists(skill_path):
         found_locations.append({
           cli: cli,
           path: skill_path
         })

3. Handle results
   IF found_locations IS empty:
     ERROR E-SHOW-001: "Skill not found: {skill_name}"
     
     # Fuzzy search
     similar = fuzzy_search(skill_name, all_skills)
     IF similar NOT empty:
       DISPLAY: "Did you mean:"
       FOR EACH suggestion IN similar:
         DISPLAY: "  - {suggestion}"
     
     ABORT (exit code 1)
   
   ELIF count(found_locations) > 1:
     ERROR E-SHOW-002: "Skill exists in multiple CLIs"
     DISPLAY: "Found in:"
     FOR EACH location IN found_locations:
       DISPLAY: "  - {location.cli}: {location.path}"
     SUGGEST: "Specify CLI: --cli <name>"
     ABORT
   
   ELSE:
     selected_location = found_locations[0]
```

**Performance Target**: < 100ms  
**References**: FR-011

---

### Phase 2: Load Content

```markdown
1. Read skill file
   skill_path = selected_location.path
   
   TRY:
     skill_content = read_file(skill_path)
   CATCH IOError:
     ERROR E-SHOW-003: "File not readable: {skill_path}"
     SUGGEST: "Check permissions"
     ABORT

2. Parse frontmatter
   TRY:
     frontmatter = parse_yaml_frontmatter(skill_content)
     body = extract_body(skill_content)
   CATCH YAMLError:
     WARN E-SHOW-004: "Invalid SKILL.md format"
     DISPLAY: "Showing raw content..."
     frontmatter = {}
     body = skill_content

3. Load metadata.yaml if exists
   metadata_path = dirname(skill_path) + "/metadata.yaml"
   
   IF file_exists(metadata_path):
     TRY:
       metadata = read_yaml(metadata_path)
     CATCH YAMLError:
       WARN E-SHOW-005: "metadata.yaml referenced but invalid"
       metadata = null
   ELSE:
     metadata = null

4. Get file stats
   file_stats = {
     size: get_file_size_kb(skill_path),
     modified: get_file_mtime(skill_path),
     created: metadata.created OR frontmatter.created OR "unknown"
   }
```

**Performance Target**: < 50ms

---

### Phase 3: Format & Display

```markdown
1. Display header
   DISPLAY:
   ═══════════════════════════════════════════════════
   Skill: {skill_name} ({selected_location.cli})
   ═══════════════════════════════════════════════════

2. Display metadata section
   IF NOT args.has_flag("--body-only"):
     DISPLAY: ""
     DISPLAY: "METADATA"
     DISPLAY: "--------"
     
     # Frontmatter fields
     IF frontmatter:
       FOR EACH key, value IN frontmatter:
         DISPLAY: "{key}: {format_value(value)}"
     
     # metadata.yaml fields (if different)
     IF metadata:
       DISPLAY: ""
       DISPLAY: "Extended metadata (metadata.yaml):"
       FOR EACH key, value IN metadata:
         IF NOT IN frontmatter:
           DISPLAY: "{key}: {format_value(value)}"
     
     DISPLAY: ""

3. Display content section
   IF NOT args.has_flag("--metadata-only"):
     DISPLAY: "CONTENT"
     DISPLAY: "-------"
     DISPLAY: body
     DISPLAY: ""

4. Display footer
   DISPLAY: "═══════════════════════════════════════════════════"
   DISPLAY: "Location: {skill_path}"
   DISPLAY: "Size: {file_stats.size} KB"
   DISPLAY: "Last modified: {format_timestamp(file_stats.modified)}"
   IF file_stats.created != "unknown":
     DISPLAY: "Created: {format_timestamp(file_stats.created)}"
   DISPLAY: "═══════════════════════════════════════════════════"

5. Format helpers
   format_value(value):
     IF is_list(value):
       RETURN "[{', '.join(value)}]"
     ELIF is_dict(value):
       RETURN pretty_print_yaml(value, indent=2)
     ELIF is_multiline_string(value):
       RETURN indent(value, 2)
     ELSE:
       RETURN str(value)
   
   format_timestamp(ts):
     RETURN format(ts, "YYYY-MM-DD HH:mm:ss")
```

**Performance Target**: < 50ms  
**References**: FR-011

---

## Error Cases

| Code | Condition | Handler |
|------|-----------|---------|
| **E-SHOW-001** | Skill not found | Error + fuzzy search suggestions |
| **E-SHOW-002** | Skill in multiple CLIs | Require explicit `--cli` |
| **E-SHOW-003** | File not readable | Permission error |
| **E-SHOW-004** | Invalid SKILL.md format | Show raw + warning |
| **E-SHOW-005** | metadata.yaml invalid | Skip + warning |

---

## Usage Examples

### Example 1: Basic Usage

```bash
> /hefesto.show email-validator

═══════════════════════════════════════════════════
Skill: email-validator (claude)
═══════════════════════════════════════════════════

METADATA
--------
name: email-validator
description: Validates email addresses using regex patterns. Use when: validating user input, checking email format.
version: 1.0.0
created: 2026-02-04
category: validation
tags: [email, regex, validation]

CONTENT
-------
# Email Validator Skill

## Capability

This skill validates email addresses using industry-standard regex patterns.

## Usage

Invoke with:
```
/email-validator user@example.com
```

## Parameters

- `email`: Email address to validate (required)

## Output

- Valid: "✅ Valid email"
- Invalid: "❌ Invalid email format"

## References

- RFC 5322: https://tools.ietf.org/html/rfc5322

═══════════════════════════════════════════════════
Location: .claude/skills/email-validator/SKILL.md
Size: 2.3 KB
Last modified: 2026-02-04 10:30:00
Created: 2026-02-04
═══════════════════════════════════════════════════
```

### Example 2: Metadata Only

```bash
> /hefesto.show email-validator --metadata-only

═══════════════════════════════════════════════════
Skill: email-validator (claude)
═══════════════════════════════════════════════════

METADATA
--------
name: email-validator
description: Validates email addresses using regex patterns
version: 1.0.0
created: 2026-02-04
category: validation
tags: [email, regex, validation]

Extended metadata (metadata.yaml):
template_version: 1.2.0
last_validated: 2026-02-04
type: created

═══════════════════════════════════════════════════
Location: .claude/skills/email-validator/SKILL.md
Size: 2.3 KB
Last modified: 2026-02-04 10:30:00
═══════════════════════════════════════════════════
```

### Example 3: Body Only

```bash
> /hefesto.show email-validator --body-only

═══════════════════════════════════════════════════
Skill: email-validator (claude)
═══════════════════════════════════════════════════

CONTENT
-------
# Email Validator Skill

## Capability

This skill validates email addresses using industry-standard regex patterns.

[... full content ...]

═══════════════════════════════════════════════════
```

### Example 4: Specific CLI

```bash
> /hefesto.show testing-strategy --cli gemini

═══════════════════════════════════════════════════
Skill: testing-strategy (gemini)
═══════════════════════════════════════════════════

[... content from gemini directory ...]
```

### Example 5: Not Found with Suggestions

```bash
> /hefesto.show email-val

❌ ERROR [E-SHOW-001]: Skill not found: email-val

Did you mean:
  - email-validator
  - email-sender
  - data-validator

Usage: /hefesto.show <skill_name>
```

### Example 6: Multiple CLIs

```bash
> /hefesto.show api-wrapper

❌ ERROR [E-SHOW-002]: Skill exists in multiple CLIs

Found in:
  - claude: .claude/skills/api-wrapper/SKILL.md
  - gemini: .gemini/skills/api-wrapper/SKILL.md
  - opencode: .opencode/skills/api-wrapper/SKILL.md

Suggestion: Specify CLI: --cli <name>
Usage: /hefesto.show <skill_name> [--cli <name>]
```

---

## Output Format

### Default (Full)

```
═══════════════════════════════════════════════════
Skill: <name> (<cli>)
═══════════════════════════════════════════════════

METADATA
--------
<key>: <value>
...

CONTENT
-------
<skill markdown body>

═══════════════════════════════════════════════════
Location: <path>
Size: <size> KB
Last modified: <timestamp>
Created: <timestamp>
═══════════════════════════════════════════════════
```

### Metadata Only

```
═══════════════════════════════════════════════════
Skill: <name> (<cli>)
═══════════════════════════════════════════════════

METADATA
--------
<key>: <value>
...

═══════════════════════════════════════════════════
Location: <path>
Size: <size> KB
Last modified: <timestamp>
═══════════════════════════════════════════════════
```

### Body Only

```
═══════════════════════════════════════════════════
Skill: <name> (<cli>)
═══════════════════════════════════════════════════

CONTENT
-------
<skill markdown body>

═══════════════════════════════════════════════════
```

---

## Success Criteria

- ✅ **SC-001**: Command implemented
- ✅ **SC-002**: Executes in < 2s (target < 200ms)
- ✅ **SC-005**: Help documentation embedded
- ✅ **US-004 Scenario 1**: Content display
- ✅ **FR-011**: Skill name + full content display

---

## Performance Targets

| Operation | Target | Typical |
|-----------|--------|---------|
| Discovery | < 100ms | 50ms |
| File read | < 50ms | 20ms |
| Formatting | < 50ms | 10ms |
| **Total** | **< 200ms** | **~100ms** |

---

## Dependencies

**Required Helpers:**
- `helpers/cli-detector.md` - Skill location

**State Files:**
- `MEMORY.md` - CLI detection results (read-only)

---

## See Also

- **Related Commands**: `/hefesto.list`, `/hefesto.validate`, `/hefesto.delete`
- **Specification**: `specs/003-hefesto-commands/contracts/show.contract.md`
- **T0 Rules**: `CONSTITUTION.md` (no T0 violations, read-only)
- **User Story**: `specs/003-hefesto-commands/spec.md` US4
