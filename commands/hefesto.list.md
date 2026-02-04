---
description: "List command to display all detected CLIs and generated skills from project state"
command: "/hefesto.list"
category: "information"
user_story: "US3"
priority: "P2"
version: "1.0.0"
---

# /hefesto.list - List Skills and CLIs Command

**Command**: `/hefesto.list`  
**Purpose**: Display all detected CLIs and generated skills from project state  
**User Story**: US3 - Persist Project State Across Sessions (P2)

---

## Overview

The `/hefesto.list` command reads and displays the current project state from MEMORY.md:

1. Validates CONSTITUTION.md
2. Parses MEMORY.md (with corruption recovery)
3. Displays detected CLIs with status
4. Displays skill registry (if any skills exist)
5. Shows state metadata (totals, timestamps)
6. Performs filesystem synchronization check

**Target Performance**: < 100ms for state reading and display

---

## Command Signature

```text
/hefesto.list [--clis] [--skills] [--verbose] [--check-sync]

Options:
  --clis        Show only CLI list (skip skills)
  --skills      Show only skills list (skip CLIs)
  --verbose     Show detailed state including paths and timestamps
  --check-sync  Perform filesystem synchronization check
```

---

## Execution Workflow

### Phase 0: Pre-Execution Validation

```markdown
1. Run CONSTITUTION validation
   (see: helpers/constitution-validator.md)
   IF invalid → Block execution

2. Check if Hefesto is initialized
   IF NOT file_exists("MEMORY.md"):
     DISPLAY: "❌ Hefesto not initialized. Run /hefesto.init first."
     ABORT (exit code 1)
```

**References**: FR-010, constitution-validator.md

---

### Phase 1: State Parsing

```markdown
1. Attempt to parse MEMORY.md
   
   TRY:
     state = parse_memory_md("MEMORY.md")
   CATCH ParseError:
     TRIGGER corruption recovery (ERR-002)
     state = recover_corrupted_memory()
     DISPLAY recovery message
     IF recovery_failed:
       ABORT with error

2. Extract state components
   
   detected_clis = state.detected_clis
   skill_registry = state.skill_registry
   metadata = {
     hefesto_version: state.hefesto_version,
     initialized: state.initialized,
     last_updated: state.last_updated,
     total_skills: COUNT(skill_registry),
     active_clis: COUNT(detected_clis WHERE status = "active")
   }
```

**Performance Target**: < 50ms  
**References**: FR-011, memory-template.md

---

### Phase 2: CLI Listing

```markdown
1. Display CLI section header
   DISPLAY: "## Detected CLIs"

2. Group CLIs by status
   
   active_clis = detected_clis WHERE status = "active"
   warning_clis = detected_clis WHERE status = "warning_no_path"
   error_clis = detected_clis WHERE status = "error_permission"
   manual_clis = detected_clis WHERE status = "manual"

3. Display active CLIs
   
   IF active_clis.length > 0:
     DISPLAY: "### Active ({count})"
     FOR EACH cli IN active_clis:
       IF --verbose:
         DISPLAY:
           - **{cli.display_name}** v{cli.version}
             - Detection: {cli.detection_method}
             - Path: {cli.executable_path}
             - Skills Directory: {cli.skills_directory_path}
       ELSE:
         DISPLAY: "- {cli.display_name} (v{cli.version}) → {cli.skills_directory_path}"

4. Display warning CLIs
   
   IF warning_clis.length > 0:
     DISPLAY: "### Warnings ({count})"
     FOR EACH cli IN warning_clis:
       DISPLAY: "- {cli.display_name} ⚠️ Config only, not in PATH"

5. Display error CLIs
   
   IF error_clis.length > 0:
     DISPLAY: "### Errors ({count})"
     FOR EACH cli IN error_clis:
       DISPLAY: "- {cli.display_name} ❌ {cli.error_message}"
```

**References**: FR-035, data-model.md (CLI Detection Result)

---

### Phase 3: Skill Registry Display

```markdown
1. Check if skills exist
   
   IF skill_registry.length == 0:
     DISPLAY: "## Skills\n\nNo skills generated yet. Run /hefesto.create to generate your first skill."
     SKIP to Phase 4

2. Display skill section header
   DISPLAY: "## Skills ({count})"

3. Display skills table
   
   IF --verbose:
     DISPLAY table with all columns:
       | Skill Name | CLIs | Created | Last Modified | Status |
       |------------|------|---------|---------------|--------|
       {FOR EACH skill}
       | {skill.name} | {skill.clis.join(", ")} | {skill.created} | {skill.last_modified} | {sync_status} |
   ELSE:
     DISPLAY compact list:
       - {skill.name} (for {skill.clis.join(", ")})

4. Group by CLI (if multiple CLIs)
   
   IF detected_clis.length > 1:
     DISPLAY: "\n### Skills by CLI"
     FOR EACH cli IN detected_clis:
       cli_skills = skill_registry WHERE cli IN skill.clis
       IF cli_skills.length > 0:
         DISPLAY: "**{cli.display_name}**: {cli_skills.length} skill(s)"
         FOR EACH skill IN cli_skills:
           DISPLAY: "  - {skill.name}"
```

**References**: FR-036, data-model.md (Skill Registry Entry)

---

### Phase 4: State Metadata Display

```markdown
1. Display metadata section
   DISPLAY: "## Project State"

2. Display summary statistics
   
   DISPLAY:
     - **Hefesto Version**: {metadata.hefesto_version}
     - **Initialized**: {format_date(metadata.initialized)}
     - **Last Updated**: {format_date(metadata.last_updated)}
     - **Total Skills**: {metadata.total_skills}
     - **Active CLIs**: {metadata.active_clis}
     - **Total CLIs**: {detected_clis.length}

3. Display storage information
   
   IF --verbose:
     total_disk_usage = calculate_disk_usage()
     DISPLAY:
       - **Disk Usage**: {total_disk_usage} KB
       - **MEMORY.md Size**: {file_size("MEMORY.md")} bytes
       - **Skills Directories**: {list_skill_directories()}
```

**References**: FR-037, data-model.md (Project State)

---

### Phase 5: Filesystem Synchronization Check

```markdown
IF --check-sync OR detected inconsistency:
  
  1. Scan filesystem for skill directories
     
     FOR EACH cli IN detected_clis:
       filesystem_skills = list_directories(cli.skills_directory_path)
       registry_skills = skill_registry WHERE cli IN skill.clis
       
       # Check for orphaned skills (in filesystem, not in registry)
       orphaned = filesystem_skills NOT IN registry_skills
       IF orphaned.length > 0:
         inconsistencies.append({
           type: "orphaned",
           cli: cli.name,
           skills: orphaned
         })
       
       # Check for missing skills (in registry, not in filesystem)
       missing = registry_skills NOT IN filesystem_skills
       IF missing.length > 0:
         inconsistencies.append({
           type: "missing",
           cli: cli.name,
           skills: missing
         })
  
  2. Display synchronization status
     
     IF inconsistencies.length == 0:
       DISPLAY: "✅ Filesystem synchronized with MEMORY.md"
     ELSE:
       DISPLAY: "⚠️ Filesystem inconsistencies detected:"
       FOR EACH issue IN inconsistencies:
         IF issue.type == "orphaned":
           DISPLAY: "- {issue.cli}: {issue.skills.length} orphaned skill(s) (in filesystem, not tracked)"
         ELIF issue.type == "missing":
           DISPLAY: "- {issue.cli}: {issue.skills.length} missing skill(s) (tracked but not in filesystem)"
       
       DISPLAY: "\nRun /hefesto.sync to fix inconsistencies"
```

**References**: FR-038, data-model.md (filesystem synchronization)

---

## MEMORY.md Parsing Logic

### Parse YAML Frontmatter

```markdown
FUNCTION parse_memory_md(file_path):
  
  1. Read file content
     content = read_file(file_path)
  
  2. Extract YAML frontmatter
     yaml_match = regex_match(content, /^---\n(.*?)\n---/s)
     IF NOT yaml_match:
       THROW ParseError("Missing YAML frontmatter")
     
     yaml_content = yaml_match.group(1)
  
  3. Parse YAML
     TRY:
       frontmatter = parse_yaml(yaml_content)
     CATCH YAMLError:
       THROW ParseError("Invalid YAML frontmatter")
  
  4. Validate required fields
     REQUIRED_FIELDS = ["hefesto_version", "initialized", "last_updated"]
     FOR EACH field IN REQUIRED_FIELDS:
       IF field NOT IN frontmatter:
         THROW ParseError("Missing required field: {field}")
  
  RETURN frontmatter
```

### Parse Markdown Tables

```markdown
FUNCTION parse_cli_table(content):
  
  1. Extract CLI table section
     table_section = extract_section(content, "## Detected CLIs")
  
  2. Parse table rows
     rows = []
     FOR EACH line IN table_section.lines:
       IF line.starts_with("|") AND NOT line.contains("---"):
         cells = line.split("|").trim()
         IF cells.length >= 5:
           rows.append({
             cli: cells[0],
             detection_method: cells[1],
             skills_directory: cells[2],
             version: cells[3],
             status: cells[4]
           })
  
  RETURN rows

FUNCTION parse_skill_table(content):
  
  1. Extract skill table section
     table_section = extract_section(content, "## Skill Registry")
  
  2. Parse table rows
     rows = []
     FOR EACH line IN table_section.lines:
       IF line.starts_with("|") AND NOT line.contains("---"):
         cells = line.split("|").trim()
         IF cells.length >= 4:
           rows.append({
             name: cells[0],
             clis: cells[1].split(",").trim(),
             created: cells[2],
             last_modified: cells[3]
           })
  
  RETURN rows
```

**References**: memory-template.md, data-model.md

---

## Usage Examples

### Example 1: List All (Default)

```text
> /hefesto.list

## Detected CLIs

### Active (3)

- Claude Code (v1.2.0) → .claude/skills/
- OpenCode (v0.2.1) → .opencode/skills/
- Cursor (v1.0.5) → .cursor/skills/

### Warnings (1)

- Gemini CLI ⚠️ Config only, not in PATH

## Skills (2)

- code-review (for claude, opencode)
- api-docs (for claude, cursor)

### Skills by CLI

**Claude Code**: 2 skills
  - code-review
  - api-docs

**OpenCode**: 1 skill
  - code-review

**Cursor**: 1 skill
  - api-docs

**Gemini CLI**: 0 skills

## Project State

- **Hefesto Version**: 1.0.0
- **Initialized**: 2026-02-04 14:30:00 UTC
- **Last Updated**: 2026-02-04 16:45:00 UTC
- **Total Skills**: 2
- **Active CLIs**: 3
- **Total CLIs**: 4
```

### Example 2: List Only CLIs

```text
> /hefesto.list --clis

## Detected CLIs

### Active (3)

- Claude Code (v1.2.0) → .claude/skills/
- OpenCode (v0.2.1) → .opencode/skills/
- Cursor (v1.0.5) → .cursor/skills/

### Warnings (1)

- Gemini CLI ⚠️ Config only, not in PATH
```

### Example 3: List Only Skills

```text
> /hefesto.list --skills

## Skills (2)

- code-review (for claude, opencode)
- api-docs (for claude, cursor)
```

### Example 4: Verbose Output

```text
> /hefesto.list --verbose

## Detected CLIs

### Active (3)

- **Claude Code** v1.2.0
  - Detection: PATH
  - Path: /usr/local/bin/claude
  - Skills Directory: .claude/skills/

- **OpenCode** v0.2.1
  - Detection: PATH
  - Path: /usr/local/bin/opencode
  - Skills Directory: .opencode/skills/

- **Cursor** v1.0.5
  - Detection: PATH
  - Path: /Applications/Cursor.app/Contents/MacOS/cursor
  - Skills Directory: .cursor/skills/

## Skills (2)

| Skill Name | CLIs | Created | Last Modified | Status |
|------------|------|---------|---------------|--------|
| code-review | claude, opencode | 2026-02-04T10:00:00Z | 2026-02-04T11:30:00Z | ✅ Synced |
| api-docs | claude, cursor | 2026-02-04T12:00:00Z | 2026-02-04T12:00:00Z | ✅ Synced |

## Project State

- **Hefesto Version**: 1.0.0
- **Initialized**: 2026-02-04 14:30:00 UTC
- **Last Updated**: 2026-02-04 16:45:00 UTC
- **Total Skills**: 2
- **Active CLIs**: 3
- **Total CLIs**: 4
- **Disk Usage**: 124.5 KB
- **MEMORY.md Size**: 2,048 bytes
```

### Example 5: Filesystem Sync Check

```text
> /hefesto.list --check-sync

## Detected CLIs

...

## Skills (2)

...

## Filesystem Synchronization

⚠️ Inconsistencies detected:

- Claude Code: 1 orphaned skill (in filesystem, not tracked)
  - legacy-formatter
- Cursor: 1 missing skill (tracked but not in filesystem)
  - api-docs

Run /hefesto.sync to fix inconsistencies
```

### Example 6: No Skills Yet

```text
> /hefesto.list

## Detected CLIs

### Active (3)

- Claude Code (v1.2.0) → .claude/skills/
- Gemini CLI → .gemini/skills/
- OpenCode (v0.2.1) → .opencode/skills/

## Skills

No skills generated yet. Run /hefesto.create to generate your first skill.

## Project State

- **Hefesto Version**: 1.0.0
- **Initialized**: 2026-02-04 14:30:00 UTC
- **Last Updated**: 2026-02-04 14:30:00 UTC
- **Total Skills**: 0
- **Active CLIs**: 3
- **Total CLIs**: 3
```

---

## Error Scenarios

### ERR-002: Corrupted MEMORY.md

```text
> /hefesto.list

⚠️ State Recovery: MEMORY.md corrupted

Attempting to parse YAML frontmatter... ❌ Failed
Backup created: MEMORY.md.backup.2026-02-04T16-00-00Z
Rebuilding state from filesystem...

Scanned directories:
- .claude/skills/ (2 skills found)
- .gemini/skills/ (0 skills found)
- .opencode/skills/ (1 skill found)

✅ State rebuilt successfully

## Detected CLIs

### Active (3)

- Claude Code → .claude/skills/
- Gemini CLI → .gemini/skills/
- OpenCode → .opencode/skills/

...
```

**References**: error-handling.md (ERR-002), FR-016

### Filesystem Inconsistency

```text
⚠️ Filesystem inconsistencies detected:

Orphaned skills (in filesystem, not tracked):
- .claude/skills/old-skill/

Missing skills (tracked but deleted from filesystem):
- api-docs (expected in .cursor/skills/)

Recommendation: Run /hefesto.sync to reconcile state
```

**References**: FR-038

---

## Performance Benchmarks

| Operation | Target | Typical |
|-----------|--------|---------|
| CONSTITUTION validation (cached) | < 5ms | 2-5ms |
| MEMORY.md file read | < 20ms | 10-15ms |
| YAML frontmatter parsing | < 10ms | 5-8ms |
| Markdown table parsing | < 20ms | 10-15ms |
| Display formatting | < 30ms | 15-25ms |
| Filesystem sync check (optional) | < 100ms | 50-80ms |
| **Total List (no sync)** | **< 100ms** | **40-70ms** |
| **Total List (with sync)** | **< 200ms** | **100-150ms** |

**References**: Performance goals from plan.md

---

## Testing

### Manual Testing (Quickstart Scenarios)

- **Test 6**: List CLIs and skills across sessions - quickstart.md

### Validation Checks

```markdown
AFTER /hefesto.list completes:

CHECK: All CLIs from MEMORY.md displayed
CHECK: All skills from MEMORY.md displayed  
CHECK: State metadata accurate (counts, timestamps)
CHECK: Execution time < 100ms (without --check-sync)
CHECK: Corrupted MEMORY.md triggers recovery
CHECK: Filesystem sync detects inconsistencies
```

---

## References

- **Specification**: specs/001-hefesto-foundation/spec.md (User Story 3)
- **Plan**: specs/001-hefesto-foundation/plan.md
- **Data Model**: specs/001-hefesto-foundation/data-model.md (Project State, Skill Registry Entry)
- **Helpers**:
  - `helpers/memory-validator.md` (to be created)
  - `helpers/memory-recovery.md` (to be created)
  - `helpers/state-sync.md` (to be created)
  - `helpers/constitution-validator.md`
  - `helpers/error-handling.md`
- **Templates**:
  - `templates/memory-template.md`
- **Related Commands**:
  - `hefesto.init.md` (creates MEMORY.md)
  - `hefesto.detect.md` (updates MEMORY.md)
- **Requirements**: FR-011, FR-016, FR-035, FR-036, FR-037, FR-038
- **Success Criteria**: SC-005 (state consistency across 100+ executions)
