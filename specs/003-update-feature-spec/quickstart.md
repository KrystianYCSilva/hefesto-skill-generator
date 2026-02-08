# Quickstart Guide: Hefesto v2.2.0 Features

**Feature**: Update Feature Spec to v2.2.0  
**Date**: 2026-02-08  
**Audience**: Developers using Hefesto CLI

---

## Overview

Hefesto v2.2.0 introduces **4 major features**:

1. **`/hefesto.update`** - Modify existing skills
2. **Web Research Integration** - Automatic URL verification
3. **`/hefesto.agent`** - Compose skills into specialized agents
4. **Payload Sync** - Fixed drift across all CLIs

This guide shows you how to use the new commands.

---

## Feature 1: Update Existing Skills

### What It Does
Modify the **content** of an existing skill while preserving agentskills.io compliance. Different from `/hefesto.validate` (which fixes spec violations).

### Basic Usage

```bash
/hefesto.update <skill-name> "<change-description>"
```

### Examples

#### Example 1: Add New Section
```bash
/hefesto.update python-error-handling "Add section on asyncio exception patterns"
```

**What happens:**
1. **Selection Phase** - Locates skill across all detected CLIs
2. **Understanding Phase** - Reads current SKILL.md + references + CONSTITUTION
3. **Change Planning** - Parses your request, identifies sections to modify
4. **Web Research** (conditional) - Verifies any new URLs or references
5. **Apply Changes** - Generates updated SKILL.md
6. **Auto-Critique** - Runs 13-point quality checklist
7. **Human Gate** - Shows you the diff before/after + full skill content

**Human Gate Prompt:**
```
Skill Updated: python-error-handling
Change: Added section on asyncio exception patterns
---
Name: python-error-handling
Description: Handle Python exceptions...
Lines: 287 → 342 | Tokens: ~3200 → ~3800
Auto-Critica: 13/13 PASS
---

DIFF:
+ ## How to Handle Async Exceptions
+ [new content...]

Actions: [approve] [edit: <what to change>] [reject]
```

#### Example 2: Update Without Change Description
```bash
/hefesto.update java-fundamentals
```

**What happens:**
Command will prompt you:
```
What changes do you want to make to java-fundamentals?
Describe in 1-2 sentences, or type [explore] to browse the skill first.
```

#### Example 3: Remove Outdated Information
```bash
/hefesto.update react-hooks "Remove references to class components, focus on function components only"
```

### Human Gate Actions

**[approve]** - Persist changes to ALL detected CLI directories:
```
✅ Updated: .claude/skills/python-error-handling/SKILL.md
✅ Updated: .gemini/skills/python-error-handling/SKILL.md
✅ Updated: .github/skills/python-error-handling/SKILL.md
... (all 7 CLIs if present)
```

**[edit: <instruction>]** - Revise before approval:
```
edit: Make the asyncio section more concise, under 50 lines
```

**[reject]** - Cancel without changes:
```
❌ Update cancelled. No files modified.
```

### When to Use `/hefesto.update`

✅ **Use when:**
- Adding new capabilities to existing skill
- Updating examples or references
- Removing outdated information
- Reorganizing content structure
- Fixing factual errors

❌ **Don't use when:**
- Skill has spec violations → use `/hefesto.validate`
- You want to create a new skill → use `/hefesto.create`
- You want to check skill quality → use `/hefesto.validate`

---

## Feature 2: Web Research Integration

### What It Does
Commands now **automatically verify URLs** and find authoritative references when you create, extract, or update skills.

### How It Works

**Automatic** - No explicit invocation needed. When you run:
- `/hefesto.create "mcp-server-development"`
- `/hefesto.extract docs/api-guide.md`
- `/hefesto.update python-error-handling "add PEP reference"`

The agent will:
1. Detect if URLs or references are needed
2. Use web search (if available) to verify links exist
3. Find official documentation (MDN, RFC, PEPs, etc.)
4. State explicitly if web search was unavailable

### Example: Creating Skill with Web Research

```bash
/hefesto.create "Model Context Protocol server development patterns"
```

**Agent output (Phase 2: Research):**
```
5. Research the skill's domain:
   - Official MCP specification: https://spec.modelcontextprotocol.io/
   - Python SDK: https://github.com/modelcontextprotocol/python-sdk
   - TypeScript SDK: https://github.com/modelcontextprotocol/typescript-sdk

6. Web Research (conditional):
   ✅ Verified: All URLs return 200 OK
   ✅ Found authoritative source: MCP spec (modelcontextprotocol.io)
   ℹ️ References include official GitHub repos and RFC-style specification
```

### If Web Search Is Unavailable

The agent will state:
```
6. Web Research (conditional):
   ⚠️ Web search unavailable in this environment
   ℹ️ References not verified via web search
   ℹ️ URLs included based on known authoritative sources
```

### Benefits

- **No hallucinated URLs** - All links are verified before inclusion
- **Up-to-date references** - Finds current documentation
- **Authoritative sources** - Prefers official docs over blog posts
- **Graceful degradation** - Works even if web search isn't available

---

## Feature 3: Generate Specialized Agents

### What It Does
Compose **multiple skills** into a specialized agent with a persona and workflow. The agent becomes a new command you can invoke.

### Basic Usage

```bash
/hefesto.agent "<agent description>"
```

### Examples

#### Example 1: Code Review Agent
```bash
/hefesto.agent "code reviewer that specializes in Python best practices, composes code-reviewer and python-fundamentals skills"
```

**What happens:**
1. **Understanding Phase** - Parses your description
2. **Skill Discovery** - Lists available skills, matches capabilities
3. **Generation** - Creates agent with:
   - Persona: "You are a senior Python code reviewer..."
   - Skills: References to code-reviewer + python-fundamentals
   - Workflow: Sequential steps (Load code → Review → Report)
   - Rules: Constraints like "Never suggest complete rewrites"
4. **Auto-Critique** - Runs 7-point agent checklist
5. **Human Gate** - Shows full agent definition
6. **Persistence** - Creates command in ALL detected CLI directories

**Generated Agent Structure:**
```markdown
---
description: "Reviews Python code for best practices. Composes: code-reviewer, python-fundamentals."
---

# code-reviewer-python

You are a senior Python code reviewer specializing in best practices, readability, and maintainability.

## Skills

Load these skills for context:
- Read `.claude/skills/code-reviewer/SKILL.md` for general review patterns
- Read `.claude/skills/python-fundamentals/SKILL.md` for Python-specific patterns

## Workflow

1. Load the code file(s) to review
2. Analyze against Python best practices (PEP 8, PEP 20)
3. Check for common anti-patterns
4. Review error handling and edge cases
5. Generate actionable feedback with severity levels

## Rules

- Never suggest complete rewrites; prefer incremental improvements
- Cite specific PEPs when referencing Python standards
- Prioritize readability over cleverness
- Flag security issues as CRITICAL
```

**Human Gate Prompt:**
```
Agent Generated: code-reviewer-python
Composes: code-reviewer, python-fundamentals
---
Description: Reviews Python code for best practices...
Lines: 87 | Auto-Critica: 7/7 PASS
---

[Full agent content shown]

Actions: [approve] [edit: <what to change>] [reject]
```

**After approval:**
```
✅ Created: .claude/commands/code-reviewer-python.md
✅ Created: .gemini/commands/code-reviewer-python.toml
✅ Created: .github/agents/code-reviewer-python.agent.md
✅ Created: .github/prompts/code-reviewer-python.prompt.md
... (all 7 CLIs)

To use: /code-reviewer-python <file-to-review>
```

#### Example 2: Documentation Specialist
```bash
/hefesto.agent "documentation specialist for API docs, uses markdown-fundamentals and java-fundamentals"
```

#### Example 3: Test Strategy Agent
```bash
/hefesto.agent "test strategist that composes testing-expert and architecture-patterns to design test suites"
```

### Agent vs Skill: Key Differences

| Aspect | Skill | Agent |
|--------|-------|-------|
| **Purpose** | Teaches knowledge/patterns | Executes workflow |
| **Invocation** | Loaded by agents | Invoked as command |
| **Structure** | `## How to` sections | Persona + Workflow + Rules |
| **Composition** | Standalone | Composes 1+ skills |
| **Command** | N/A | `/<agent-name>` |
| **Location** | `.<cli>/skills/` | `.<cli>/commands/` |

### When to Use `/hefesto.agent`

✅ **Use when:**
- You need a specialized workflow combining multiple skills
- You want a consistent persona for a task
- You're repeating the same multi-step process
- You want to compose existing skills without modifying them

❌ **Don't use when:**
- You need to teach a concept → use `/hefesto.create` (skill)
- You need a single-purpose command → use skill directly
- The workflow is too simple (< 3 steps) → just use skills manually

### Agent Naming Rules

**Generated agents do NOT use `hefesto.` prefix**:
- ✅ Good: `code-reviewer`, `test-strategist`, `doc-specialist`
- ❌ Bad: `hefesto.code-reviewer`, `my_agent`, `CodeReviewer`

**Invocation**:
```bash
/code-reviewer file.py        # Correct
/hefesto.code-reviewer file.py  # Wrong (command not found)
```

**Reserved prefixes**:
- `hefesto.*` - System commands only
- `speckit.*` - Specification workflow commands only

---

## Feature 4: Payload Sync (Background)

### What Changed

**Problem**: Installer payloads had **drift** from canonical commands:
- 10-point checklist instead of 13-point
- Missing Token Economy section
- Outdated section structure (`## Instructions` vs `## How to`)

**Solution**: v2.2.0 syncs ALL 18 drifted files across 7 CLIs.

**You don't need to do anything** - but if you're updating from v2.1.0 or earlier:

```bash
# Re-run installer to get synced payloads
./installer/install.ps1    # Windows
./installer/install.sh     # Linux/Mac
```

### What Was Fixed

| File | Fix |
|------|-----|
| All `hefesto.create.*` | Added Token Economy, "How to" sections, 13-point checklist |
| All `hefesto.extract.*` | Changed 10→13 points, added web research step |
| Gemini TOML files | Overhauled structure to match canonical |

**Result**: Zero drift between canonical (`.claude/commands/`) and payloads (`installer/payload/commands/*/`).

---

## Verification & Troubleshooting

### Check Installed Version
```bash
cat .hefesto/version
# Expected output: 2.2.0
```

### List All Commands
```bash
/hefesto.list
```

Expected to show **7 commands**:
- hefesto.create
- hefesto.extract
- hefesto.validate
- hefesto.init
- hefesto.list
- hefesto.update ← NEW
- hefesto.agent ← NEW (but generates user agents, not hefesto.agent itself)

### Test Web Research
```bash
/hefesto.create "test skill for URL verification"
```

Look for Phase 2 output mentioning web search.

### Test Agent Generation
```bash
/hefesto.agent "simple agent composing one skill"
```

Verify agent file is created in your CLI directory.

### Common Issues

**Issue**: `/hefesto.update` not found  
**Fix**: Re-run installer or check `.claude/commands/` for `hefesto.update.md`

**Issue**: Web research not working  
**Status**: Check if your CLI supports web search (see research.md). Conditional web research should state "unavailable" but continue anyway.

**Issue**: Agent command not working after creation  
**Fix**: Restart CLI or reload config. Check that file was created in correct directory (`.claude/commands/` not `.claude/agents/`).

---

## Examples Cheat Sheet

```bash
# Update a skill
/hefesto.update python-error-handling "add asyncio section"

# Create skill with web research
/hefesto.create "OAuth 2.0 authentication patterns"

# Generate code review agent
/hefesto.agent "code reviewer for Python using code-reviewer and python-fundamentals"

# List all skills and commands
/hefesto.list

# Validate a skill (not new, but useful)
/hefesto.validate python-error-handling
```

---

## What's Next?

After using these features:
1. **Feedback** - Report bugs or suggestions via GitHub issues
2. **Custom Agents** - Experiment with composing your project's skills
3. **Contribute** - Share useful agents with the community

**Version**: 2.2.0  
**License**: MIT  
**Support**: See CONTRIBUTING.md

---

## References

- [CARD-003 Feature Specification](../../docs/cards/CARD-003-v2.2.0-features.md)
- [CONSTITUTION.md](../../CONSTITUTION.md) (T0 rules)
- [agentskills.io](https://agentskills.io) (specification)
- [research.md](./research.md) (design research)
- [data-model.md](./data-model.md) (entities and relationships)
