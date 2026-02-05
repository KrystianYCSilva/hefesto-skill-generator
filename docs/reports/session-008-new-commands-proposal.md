# New Commands Proposal - Session 008 Learnings

**Date**: 2026-02-04  
**Based on**: Session 008 Execution Report  
**Priority**: High

---

## Overview

This document proposes 3 new commands identified as critical needs during Session 008:
1. `/hefesto.distribute` - Multi-CLI skill distribution
2. `/hefesto.extend` - Incremental skill enhancement
3. `/hefesto.edit` - Interactive skill editor

---

## 1. `/hefesto.distribute` Command

### Problem Statement

During Session 008, user attempted to use `/hefesto.sync java-fundamentals --all` to distribute a skill to all detected CLIs. This is semantically incorrect as `/hefesto.sync` is designed for template synchronization, not multi-CLI distribution.

**Current Gap**: No dedicated command for distributing existing skills across multiple CLIs.

### Command Specification

```markdown
---
description: "Distribute existing skill to multiple AI CLI platforms"
command: "/hefesto.distribute"
category: "skill-management"
priority: "P1"
version: "1.0.0"
---

# /hefesto.distribute - Skill Distribution Command

**Purpose**: Copy existing skill from source CLI to target CLI(s)

## Signature

/hefesto.distribute <skill_name> --to <cli1,cli2,...> | --all [--adapt] [--dry-run]

Arguments:
  skill_name          Name of existing skill to distribute

Options:
  --to <clis>         Target CLIs (comma-separated: claude,gemini,cursor)
  --all               Distribute to all detected CLIs
  --adapt             Auto-adapt CLI-specific syntax (e.g., Gemini {{args}})
  --dry-run           Preview changes without applying
  --force             Overwrite if skill already exists in target

## Examples

# Distribute to specific CLIs
/hefesto.distribute java-fundamentals --to claude,gemini,cursor

# Distribute to all CLIs
/hefesto.distribute java-fundamentals --all

# Distribute with auto-adaptation
/hefesto.distribute java-fundamentals --all --adapt

# Preview distribution
/hefesto.distribute java-fundamentals --all --dry-run
```

### Execution Workflow

```markdown
Phase 0: Validation
1. Check CONSTITUTION.md
2. Check MEMORY.md exists
3. Verify skill exists in source CLI
4. Detect target CLIs

Phase 1: Planning
1. List target CLIs
2. Check for conflicts (skill already exists)
3. Identify adaptations needed (Gemini {{args}}, etc.)
4. Display plan to user

Phase 2: Distribution
1. Create skill directories in target CLIs
2. Copy SKILL.md, metadata.yaml, references/
3. Apply CLI-specific adaptations if --adapt flag
4. Validate T0 compliance in each target
5. Update MEMORY.md with new locations

Phase 3: Verification
1. Verify file checksums match source
2. Validate SKILL.md < 500 lines in all targets
3. Display success report
```

### T0 Compliance

- **T0-HEFESTO-05**: Skills stored locally in each CLI directory
- **T0-HEFESTO-09**: CLI-specific adaptations maintained
- **T0-HEFESTO-03**: Progressive Disclosure verified in targets

### Estimated Effort

**8 hours** (extends CARD-004: Multi-CLI Generator)

---

## 2. `/hefesto.extend` Command

### Problem Statement

User expressed need: *"agora que temos o java-fundamentals eu poderia criar uma sessão para falar de como refatorar aplicações java ou algo criar complementos por versão explicando o que cada uma tem (6/7/8 ...) e não posso fazer isso via comando"*

**Current Gap**: No way to incrementally add content to existing skills without manual file editing.

### Command Specification

```markdown
---
description: "Extend existing skill with additional content (sections, references, guides)"
command: "/hefesto.extend"
category: "skill-management"
priority: "P1"
version: "1.0.0"
---

# /hefesto.extend - Skill Extension Command

**Purpose**: Add new content to existing skills while maintaining T0 compliance

## Signature

/hefesto.extend <skill_name> --section <name> | --reference <file> | --version-guide [--cli <name>]

Arguments:
  skill_name          Name of existing skill to extend

Options:
  --section <name>    Add new section to SKILL.md (interactive wizard)
  --reference <file>  Add new reference file to references/
  --version-guide     Create version-specific guide (e.g., Java 6/7/8 features)
  --cli <name>        Target specific CLI (default: all CLIs where skill exists)
  --dry-run           Preview changes without applying

## Examples

# Add new section about refactoring
/hefesto.extend java-fundamentals --section "Refactoring Patterns"

# Add new reference file
/hefesto.extend java-fundamentals --reference "java-version-roadmap.md"

# Create version-specific guide
/hefesto.extend java-fundamentals --version-guide

# Preview extension
/hefesto.extend java-fundamentals --section "Testing" --dry-run
```

### Execution Workflow

```markdown
Phase 0: Validation
1. Check CONSTITUTION.md
2. Verify skill exists
3. Load current SKILL.md content
4. Check current line count

Phase 1: Content Creation (Wizard Mode)

FOR --section:
  1. PROMPT: "Section title?"
  2. PROMPT: "Section content (use 'reference' to create JIT file)?"
  3. Check if adding to SKILL.md exceeds 500 lines
  4. IF exceeds: Auto-suggest creating reference file instead
  5. Generate content with AI assistance

FOR --reference:
  1. PROMPT: "Reference file topic?"
  2. Load reference template
  3. Generate content structure
  4. Create file in references/

FOR --version-guide:
  1. Detect skill domain (Java, Python, etc.)
  2. PROMPT: "Which versions to cover?"
  3. Generate version comparison matrix
  4. Create structured guide

Phase 2: Integration
1. IF --section AND within limits:
   - Insert section in SKILL.md at appropriate location
   - Update table of contents
2. IF --reference:
   - Create file in references/
   - Add link in "Advanced Topics" section
3. Update metadata.yaml (updated timestamp, version bump)

Phase 3: Validation
1. Validate SKILL.md still < 500 lines (T0-HEFESTO-03)
2. Validate Agent Skills spec compliance
3. Display preview

Phase 4: Human Gate
1. Show diff of changes
2. PROMPT: [approve] [edit] [reject]
3. IF approve: Apply to all CLIs where skill exists
4. Update MEMORY.md

Phase 5: Multi-CLI Sync
1. Apply changes to all CLIs with this skill
2. Verify integrity
3. Display success report
```

### Example: Adding Version Guide to java-fundamentals

```bash
$ /hefesto.extend java-fundamentals --version-guide

🔧 Hefesto Extend: Version Guide Creation

Detected skill domain: Java
Current versions in metadata: 6-25

Which versions to detail?
[1] All versions (6, 7, 8, 11, 17, 21, 25)
[2] LTS only (8, 11, 17, 21)
[3] Custom selection

> 2

Generating Java LTS Version Guide...

Section 1: Java 8 LTS (2014)
  - Lambdas & Streams ✅
  - Optional ✅
  - Default methods ✅

Section 2: Java 11 LTS (2018)
  - var keyword ✅
  - HTTP Client ✅
  - String methods ✅

[... continues ...]

Preview:
  New file: references/java-version-lts-guide.md (480 lines)
  Updated: SKILL.md (added link in Advanced Topics)
  Updated: metadata.yaml (version 1.0.0 → 1.1.0)

Total SKILL.md size: 430 lines ✅ (< 500)

[approve] [edit] [reject]
> approve

✅ Extended java-fundamentals in 6 CLIs:
   .opencode/skills/java-fundamentals/
   .claude/skills/java-fundamentals/
   .gemini/skills/java-fundamentals/
   .codex/skills/java-fundamentals/
   .cursor/skills/java-fundamentals/
   .qwen/skills/java-fundamentals/

Done! Version guide added successfully.
```

### T0 Compliance

- **T0-HEFESTO-02**: Human Gate before persistence
- **T0-HEFESTO-03**: Validates SKILL.md < 500 lines, creates JIT files if needed
- **T0-HEFESTO-08**: Idempotent operations
- **T0-HEFESTO-09**: Syncs across all CLIs

### Estimated Effort

**12 hours** (new CARD-008)

---

## 3. `/hefesto.edit` Command

### Problem Statement

**Current Gap**: No interactive way to edit existing skill content. Users must manually open files and edit, risking T0 violations.

### Command Specification

```markdown
---
description: "Interactive editor for existing skills with live validation"
command: "/hefesto.edit"
category: "skill-management"
priority: "P2"
version: "1.0.0"
---

# /hefesto.edit - Interactive Skill Editor

**Purpose**: Edit existing skills interactively with AI assist
