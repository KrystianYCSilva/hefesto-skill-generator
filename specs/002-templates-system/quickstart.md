# Quickstart Guide: Templates System

**Feature**: 002-templates-system  
**Date**: 2026-02-04  
**Audience**: AI Agents implementing Hefesto template commands

## Template Locations

```
.hefesto/templates/
├── skill-template.md           # Base Agent Skills template
├── metadata-template.yaml      # Expanded metadata template  
└── adapters/
    ├── claude.adapter.md       
    ├── gemini.adapter.md       
    ├── codex.adapter.md        
    ├── copilot.adapter.md      
    ├── opencode.adapter.md     
    ├── cursor.adapter.md       
    ├── qwen.adapter.md         
    └── mcp.adapter.md          
```

## Official Variables

| Variable | Example | Validation |
|----------|---------|------------|
| `{{SKILL_NAME}}` | code-review | T0-HEFESTO-07 naming |
| `{{SKILL_DESCRIPTION}}` | Analyzes code... | ≤1024 chars |
| `{{SKILL_BODY}}` | # Instructions\n... | Markdown |
| `{{CREATED_DATE}}` | 2026-02-04 | ISO 8601 |
| `{{VERSION}}` | 1.0.0 | SemVer |
| `{{ARGUMENTS}}` | $ARGUMENTS or {{args}} | CLI-specific |

## Basic Workflow

1. **Load** base template from `.hefesto/templates/skill-template.md`
2. **Gather** variable values from user request
3. **Validate** variables against rules (T0-HEFESTO-07, FR-007, FR-008)
4. **Substitute** variables in template
5. **Apply** CLI adapter (claude.adapter.md, gemini.adapter.md, etc.)
6. **Validate** output against Agent Skills spec (FR-012, FR-021)
7. **Present** via Human Gate (T0-HEFESTO-02)
8. **Persist** if approved

## Example: Basic Skill

**Input**: "Create code-review skill"

**After substitution**:
```markdown
---
name: code-review
description: |
  Analyzes code for quality issues.
  Use when: reviewing PRs
license: MIT
---

# code-review

Analyze code for quality, conventions, security.

## Usage
Invoke: `/skill code-review {{ARGUMENTS}}`
```

**After Claude adapter**: `{{ARGUMENTS}}` → `$ARGUMENTS`  
**After Gemini adapter**: `{{ARGUMENTS}}` → `{{args}}`

## Validation Errors

Example failure:
```
❌ Validation Failed:

[T0-HEFESTO-07] name: "Code Review"
Expected: lowercase, hyphens only
Suggestion: Use "code-review"
```

## Template Versioning

Templates version matches Hefesto version.  
Update via `/hefesto.init` after Hefesto upgrade.

---

**Quickstart Status**: ✅ Complete  
**Next**: Run `/speckit.tasks` to generate task breakdown
