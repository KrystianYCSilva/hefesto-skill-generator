# Data Model: Hefesto v2.2.0

**Feature**: Update Feature Spec to v2.2.0  
**Date**: 2026-02-08  
**Status**: Phase 1 Design

---

## Overview

Hefesto is a **template-driven system** with no traditional database or ORM. All entities are represented as **Markdown files** on the filesystem with YAML frontmatter. This document defines the logical entities and their relationships.

---

## Core Entities

### 1. Skill (Existing)

**Purpose**: Represents an Agent Skill following agentskills.io specification.

**Attributes**:
| Attribute | Type | Constraints | Example |
|-----------|------|-------------|---------|
| `name` | string | Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`, max 64 chars | `"python-error-handling"` |
| `description` | string | Max 1024 chars, must include "Use when:" | `"Handle Python exceptions... Use when: debugging..."` |
| `body` | markdown | < 500 lines, ~5000 tokens (T0-HEFESTO-03) | Full skill content |
| `frontmatter` | YAML | Required: `name`, `description` only | `---\nname: foo\n---` |
| `references/` | directory | Optional, loaded JIT | Extended documentation |
| `scripts/` | directory | Optional | Executable helpers |
| `assets/` | directory | Optional | Images, data files |

**Location**: `.<cli>/skills/<name>/SKILL.md`

**Validation Rules**:
- Frontmatter MUST contain ONLY `name` and `description` (no extra fields)
- Name MUST match filename directory
- Description MUST start with action verb
- Body MUST use `## How to <capability>` sections (not `## Instructions`)

**State Transitions**: None (skills are immutable after creation; updates handled via `/hefesto.update`)

---

### 2. Agent (New)

**Purpose**: Represents a composed command that orchestrates multiple skills into a specialized workflow.

**Attributes**:
| Attribute | Type | Constraints | Example |
|-----------|------|-------------|---------|
| `name` | string | Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`, max 64 chars | `"code-reviewer"` |
| `description` | string | Max 1024 chars | `"Reviews code for anti-patterns. Composes: code-reviewer, testing-expert."` |
| `persona` | string | Required, specific role | `"You are a senior code reviewer specializing in Python."` |
| `skills` | list[SkillReference] | 1+ skill paths | `[".<cli>/skills/code-reviewer/SKILL.md"]` |
| `workflow` | list[Step] | Sequential steps | `["1. Load code", "2. Review", "3. Report"]` |
| `rules` | list[Constraint] | Behavioral constraints | `["Never suggest complete rewrites"]` |
| `target_cli` | CLI | Enum of 7 CLIs | `claude`, `gemini`, etc. |

**Location**: 
- For Claude/Gemini/Codex/OpenCode/Cursor/Qwen: `.<cli>/commands/<name>.md`
- For GitHub Copilot: `.github/agents/<name>.agent.md` + `.github/prompts/<name>.prompt.md`

**Validation Rules** (7-point checklist):
1. All referenced skills exist (CRITICAL)
2. Frontmatter has description (CRITICAL)
3. Persona is specific, not generic (WARNING)
4. Workflow has sequential steps (CRITICAL)
5. Skill paths use correct CLI pattern (CRITICAL)
6. Agent is concise < 200 lines (WARNING)
7. No credentials/secrets/PII (CRITICAL)

**Relationships**:
- Agent **COMPOSES** 1+ Skill (read-only references via file paths)
- Agent **TARGETS** 1 CLI (files stored per CLI)

**State Transitions**: None (agents are immutable after creation)

**Key Distinction from Skills**:
- **Skills** teach capabilities (knowledge/patterns)
- **Agents** orchestrate skills into workflows (execution/process)
- **Agents** are invoked as commands (`/code-reviewer`)
- **Skills** are loaded by agents (`Read .<cli>/skills/code-reviewer/SKILL.md`)

---

### 3. CLI (Existing)

**Purpose**: Represents a target AI CLI environment.

**Attributes**:
| Attribute | Type | Constraints | Example |
|-----------|------|-------------|---------|
| `name` | string | One of 7 supported CLIs | `"claude"`, `"gemini"`, `"copilot"` |
| `config_dir` | path | Dot-prefixed directory | `.claude/` |
| `command_dir` | path | CLI-specific command storage | `.claude/commands/` |
| `agent_dir` | optional[path] | Only Copilot has this | `.github/agents/` |
| `prompt_dir` | optional[path] | Only Copilot/Codex have this | `.github/prompts/` |
| `syntax_variant` | enum | Variable syntax for arguments | `$ARGUMENTS` or `{{args}}` |
| `file_format` | enum | Command file format | `markdown` or `toml` |
| `web_search_support` | enum | Native/limited/none | `native`, `limited` |

**Enum Values**:

**CLI Names**:
1. `claude` (Anthropic Claude CLI)
2. `gemini` (Google Gemini CLI)
3. `codex` (OpenAI Codex CLI)
4. `github` (GitHub Copilot CLI)
5. `opencode` (OpenCode CLI)
6. `cursor` (Cursor CLI)
7. `qwen` (Alibaba Qwen CLI)

**Syntax Variants**:
- `$ARGUMENTS` - Used by Claude, Codex, Copilot, OpenCode, Cursor
- `{{args}}` - Used by Gemini, Qwen

**File Formats**:
- `markdown` - Used by Claude, Codex, Copilot, OpenCode, Cursor, Qwen
- `toml` - Used by Gemini (wraps markdown in `prompt = """..."""`)

**Web Search Support**:
- `native` - Claude, Gemini, Qwen, Copilot
- `limited` - Codex, Cursor, OpenCode (via MCP/plugins)

**Relationships**:
- CLI **HAS_MANY** Command
- CLI **HAS_MANY** Skill (in `.<cli>/skills/`)

---

### 4. Command (Existing)

**Purpose**: Represents a Hefesto or SpecKit command that agents can invoke.

**Attributes**:
| Attribute | Type | Constraints | Example |
|-----------|------|-------------|---------|
| `name` | string | Namespaced: `<prefix>.<action>` | `"hefesto.create"` |
| `description` | string | Single-line summary | `"Create Agent Skill from description"` |
| `phases` | list[Phase] | Sequential workflow steps | `["Understanding", "Research", "Generation", ...]` |
| `input_format` | string | How user provides input | `"{{args}}"` or `"$ARGUMENTS"` |
| `output_artifacts` | list[path] | Files generated | `[".<cli>/skills/<name>/SKILL.md"]` |
| `human_gate` | boolean | Requires approval? | `true` (all Hefesto commands) |

**Location**: 
- Canonical: `.claude/commands/<prefix>.<action>.md`
- Distributed: `.<cli>/commands/` (or `prompts/` for some CLIs)
- Installer: `installer/payload/commands/<cli>/`

**Namespaces**:
- `hefesto.*` - Skill/agent generation commands
- `speckit.*` - Specification workflow commands

**Existing Commands** (pre-v2.2.0):
- `hefesto.create` - Create new skill
- `hefesto.extract` - Extract skill from source
- `hefesto.validate` - Validate/fix skill
- `hefesto.init` - Bootstrap environment
- `hefesto.list` - List installed skills

**New Commands** (v2.2.0):
- `hefesto.update` - Modify existing skill content
- `hefesto.agent` - Generate agent from skill composition

---

### 5. Template (Existing)

**Purpose**: Blueprint for generating skills, agents, or other artifacts.

**Attributes**:
| Attribute | Type | Constraints | Example |
|-----------|------|-------------|---------|
| `name` | string | Descriptive filename | `"skill-template.md"` |
| `path` | path | Source location | `templates/skill-template.md` |
| `type` | enum | Template category | `skill`, `agent`, `command` |
| `locations` | list[path] | All copies | `[templates/, .hefesto/templates/, installer/payload/hefesto/templates/]` |
| `variables` | list[string] | Placeholders | `["<skill-name>", "{{args}}"]` |

**Location Replication**:
1. **Source**: `templates/` (canonical, version-controlled)
2. **Installed**: `.hefesto/templates/` (copied during init)
3. **Payload**: `installer/payload/hefesto/templates/` (for distribution)

**Existing Templates**:
- `skill-template.md` - Blueprint for SKILL.md structure
- `quality-checklist.md` - 13-point validation checklist
- `cli-compatibility.md` - CLI syntax adaptation rules

**New Template** (v2.2.0):
- `agent-template.md` - Blueprint for agent command structure

**Relationships**:
- Template **IS_COPIED_TO** 3 locations (sync required)
- Command **USES** Template during generation

---

### 6. UpdateChange (New)

**Purpose**: Represents a modification request to an existing skill.

**Attributes**:
| Attribute | Type | Constraints | Example |
|-----------|------|-------------|---------|
| `skill_name` | string | Must match existing skill | `"python-error-handling"` |
| `change_description` | string | Natural language change request | `"Add section on asyncio exceptions"` |
| `sections_to_modify` | list[string] | Markdown headers affected | `["## How to handle async exceptions"]` |
| `web_research_needed` | boolean | Requires URL verification? | `true` |
| `before_content` | markdown | Original SKILL.md | Full original content |
| `after_content` | markdown | Modified SKILL.md | Full modified content |
| `auto_critique_score` | string | Validation result | `"13/13 PASS"` |

**Lifecycle**:
1. **Input** - User provides: `skill_name` + `change_description`
2. **Analysis** - System reads current skill, identifies sections
3. **Planning** - Determines `sections_to_modify`, `web_research_needed`
4. **Generation** - Creates `after_content`
5. **Validation** - Runs 13-point checklist, generates `auto_critique_score`
6. **Human Gate** - Shows diff (`before_content` vs `after_content`)
7. **Persistence** - Overwrites SKILL.md in ALL detected CLI directories

**Validation**: Same 13-point checklist as skill creation

**State**: Transient (not persisted; exists only during `/hefesto.update` execution)

---

## Relationships Diagram

```
CLI (7 instances)
 ├── HAS_MANY Command
 │   ├── hefesto.create
 │   ├── hefesto.extract
 │   ├── hefesto.update (NEW)
 │   └── hefesto.agent (NEW)
 ├── HAS_MANY Skill
 │   └── <skill-name>/SKILL.md
 └── HAS_MANY Agent (NEW)
     └── <agent-name>.md (or .agent.md for Copilot)

Agent (NEW)
 └── COMPOSES Skill (1+)
     └── References: .<cli>/skills/<name>/SKILL.md

Command
 └── USES Template
     └── Templates: skill-template, agent-template (NEW), quality-checklist

Template
 └── IS_COPIED_TO Locations (3)
     ├── templates/ (source)
     ├── .hefesto/templates/ (installed)
     └── installer/payload/hefesto/templates/ (distribution)

UpdateChange (NEW, transient)
 └── MODIFIES Skill
     └── before_content → after_content
```

---

## File System Mapping

### Skill Storage Pattern
```
.<cli>/skills/<skill-name>/
├── SKILL.md              # Required (core content)
├── references/           # Optional (JIT resources)
│   └── *.md
├── scripts/              # Optional (executable helpers)
│   └── *.sh, *.ps1
└── assets/               # Optional (images, data)
    └── *.png, *.json
```

### Agent Storage Pattern (Non-Copilot CLIs)
```
.<cli>/commands/<agent-name>.md
```

### Agent Storage Pattern (GitHub Copilot)
```
.github/
├── agents/<agent-name>.agent.md     # Full agent definition
└── prompts/<agent-name>.prompt.md   # Stub with frontmatter: agent: <name>
```

### Template Storage Pattern
```
templates/<template-name>.md          # Source (canonical)
.hefesto/templates/<template-name>.md # Installed (copied)
installer/payload/hefesto/templates/
  └── <template-name>.md              # Distribution (copied)
```

### Command Storage Pattern
```
.claude/commands/<prefix>.<action>.md             # Canonical source
.<cli>/commands/<prefix>.<action>.{md,toml}       # Live CLI copies
installer/payload/commands/<cli>/
  └── <prefix>.<action>.{md,toml}                 # Distribution payloads
```

---

## Validation Rules Summary

### Skill Validation (13-point checklist)
1. Frontmatter valid? (CRITICAL)
2. Frontmatter strict (name + description only)? (CRITICAL)
3. Size limits (< 500 lines, ~5000 tokens)? (CRITICAL)
4. Description quality (action verb, "Use when:", specific)? (CRITICAL)
5. No "When to Use" section in body? (WARNING)
6. Task-oriented sections ("How to [task]")? (WARNING)
7. Token Economy applied? (WARNING)
8. Concise (no filler)? (WARNING)
9. Examples only for non-obvious patterns? (WARNING)
10. Terminology consistent? (WARNING)
11. Degrees of freedom appropriate? (INFO)
12. Progressive disclosure (references/ if > 200 lines)? (WARNING)
13. No credentials/secrets/PII? (CRITICAL)

### Agent Validation (7-point checklist)
1. All referenced skills exist? (CRITICAL)
2. Frontmatter has description? (CRITICAL)
3. Persona is specific (not generic)? (WARNING)
4. Workflow has sequential steps? (CRITICAL)
5. Skill paths use correct CLI pattern? (CRITICAL)
6. Agent is concise (< 200 lines)? (WARNING)
7. No credentials/secrets/PII? (CRITICAL)

### Name Validation (Skills & Agents)
- Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`
- Max length: 64 characters
- Lowercase only
- Hyphens allowed, no underscores
- No leading/trailing hyphens

---

## State Management

**Immutable Artifacts**:
- Skills (after creation)
- Agents (after creation)
- Templates (between versions)

**Mutable Artifacts**:
- Skills (via `/hefesto.update`)
- Configuration (`.hefesto/version`)

**Transient State**:
- `UpdateChange` (exists only during update workflow)
- Human Gate approval state (in-memory during command execution)

**No Database**: All state is filesystem-based. No SQLite, no ORM, no migrations.

---

## References

- agentskills.io specification
- CONSTITUTION.md (T0 rules)
- research.md (Phase 0 findings)
- CARD-003-v2.2.0-features.md
