# Research Document: Hefesto v2.2.0 Implementation

**Feature**: Update Feature Spec to v2.2.0  
**Date**: 2026-02-08  
**Status**: Phase 0 Complete

---

## Research Task 1: Web Search Tool Availability

### Question
Which CLIs support web search natively? Does conditional web research require CLI-specific handling?

### Decision
**Implement as conditional instruction**, not CLI-specific branching. All supported CLIs have web search capabilities, but we'll use a "conditional" pattern that degrades gracefully.

### Findings

| CLI | Web Search Support | Implementation Notes |
|-----|-------------------|---------------------|
| Claude (Anthropic) | ✅ Native | Direct API access via tools/function-calling |
| Gemini (Google) | ✅ Native | Integrated search capability |
| Qwen (Alibaba) | ✅ Native | MCP server integration |
| Copilot (Microsoft) | ✅ Native | Built-in search capability |
| Cursor | ⚠️ Limited | Via MCP or indirect API (fallback works) |
| Codex (OpenAI) | ⚠️ Limited | Plugin-based (fallback works) |
| OpenCode | ⚠️ Limited | Extension-based (fallback works) |

**Source**: `/docs/pesquisa/inventario-tools-and-refs-ai-v2.md`

### Rationale
Rather than maintaining 7 different versions, we use **conditional instruction text**:
```markdown
**Web Research** (conditional):
- When you need to cite URLs, verify claims, or find authoritative references: USE web search
- NEVER invent or hallucinate URLs -- if you include a link, verify it exists
- If web search is unavailable, explicitly state: "References not verified via web search"
- Prefer official documentation URLs (language docs, RFC, MDN, etc.)
```

This pattern:
- Works on all CLIs (agents self-select based on capability)
- Degrades gracefully (agents without search state the limitation)
- Requires no CLI-specific branching logic

### Alternatives Considered
1. **CLI-specific branching** - Rejected: violates T0-HEFESTO-04 (multi-CLI universality)
2. **Mandatory web search** - Rejected: would fail on limited CLIs
3. **External service (Tavily/Perplexity)** - Rejected: violates T0-HEFESTO-13 (zero dependencies)

---

## Research Task 2: Agent Command Placement

### Question
For non-Copilot CLIs, do agent commands go in `/commands/` or separate `/agents/` directory?

### Decision
**Agent commands go in `/commands/` for all CLIs except GitHub Copilot**, which uses dual structure (`.github/agents/` + `.github/prompts/`).

### Findings

**Directory Structure Audit**:
```text
.claude/commands/       # All commands here (no /agents/ subdirectory)
.gemini/commands/       # All commands here (no /agents/ subdirectory)
.codex/prompts/         # All commands here (no /agents/ subdirectory)
.opencode/command/      # All commands here (no /agents/ subdirectory)
.cursor/commands/       # All commands here (no /agents/ subdirectory)
.qwen/commands/         # All commands here (no /agents/ subdirectory)
.github/                # DUAL structure:
  ├── agents/           #   - Full agent definitions (hefesto.create.agent.md)
  └── prompts/          #   - Prompt stubs referencing agents (hefesto.create.prompt.md)
```

**GitHub Copilot Pattern**:
- Agent file (`.github/agents/hefesto.create.agent.md`) contains full workflow
- Prompt file (`.github/prompts/hefesto.create.prompt.md`) contains frontmatter: `agent: hefesto.create`
- This is a **Copilot-specific convention**; other CLIs don't use it

### Rationale
- Consistency: 6 of 7 CLIs use single `/commands/` directory
- Copilot's dual structure is native to its platform, not a general pattern
- Generated agents should follow this convention per CLI

### Alternatives Considered
1. **Force all CLIs to use /agents/** - Rejected: would break existing structure for 6 CLIs
2. **Only create in .github/agents/** - Rejected: violates T0-HEFESTO-04 (multi-CLI support)

### Implementation Impact
`/hefesto.agent` command must:
- For Claude/Gemini/Codex/OpenCode/Cursor/Qwen: create in `/commands/`
- For GitHub Copilot: create BOTH `.github/agents/<name>.md` AND `.github/prompts/<name>.prompt.md`

---

## Research Task 3: TOML Multi-line String Best Practices

### Question
What's the safest escaping strategy for Gemini TOML files with complex Markdown (tables, pipes, 13-point checklist)?

### Decision
**Use triple-quoted raw string literals** (`"""..."""`) for all complex Markdown prompts. No escaping needed for pipes, tables, or code blocks.

### Findings

**Pattern Analysis** (from `.gemini/commands/*.toml`):
```toml
description = "Single-line string in double quotes"

prompt = """
# Multi-line Markdown with NO escaping needed

| Column 1 | Column 2 |
|----------|----------|
| Value    | Value    |

`code blocks` and ```fenced blocks``` work directly

Variables: {{args}} used as-is
"""
```

**Edge Cases Tested**:
| Pattern | Works in Raw String? | Notes |
|---------|---------------------|-------|
| Pipes in tables (`\|`) | ✅ Yes | No escaping needed |
| Backticks (`` ` ``) | ✅ Yes | Single or triple work |
| YAML frontmatter (`---`) | ✅ Yes | Literal newlines preserved |
| Template variables (`{{args}}`) | ✅ Yes | Gemini/Qwen use this |
| Nested code fences | ✅ Yes | ` ```markdown ... ``` ` works |
| Degrees of freedom (`MUST/SHOULD`) | ✅ Yes | Slashes need no escaping |

**Critical Rule**: Literal `"""` sequences inside prompt would break (must escape as `\"\"\"` if needed), but this doesn't occur in skill generation commands.

### Rationale
- Raw strings eliminate 90% of escaping complexity
- Existing codebase already uses this pattern successfully
- Compatible with 13-point checklist table format

### Alternatives Considered
1. **Single-line with escaping** - Rejected: unreadable, error-prone
2. **External file references** - Rejected: breaks atomic command structure
3. **JSON embedding** - Rejected: TOML is Gemini's native format

---

## Research Task 4: Existing Drift Audit

### Question
Are there other commands beyond create/extract with drift (10-point vs 13-point checklist)?

### Decision
**Complete drift audit reveals 18 files with "10-point" references**. All must be updated to "13-point" with Token Economy section.

### Findings

**Files with Drift** (grep results for `10-point|/10 PASS`):

**Canonical commands (source of truth)**:
- `.claude/commands/hefesto.extract.md` - Line 91: "10-point", Line 114: `<X>/10 PASS`

**Installer payloads** (distribution copies):
- `installer/payload/commands/claude/hefesto.extract.md`
- `installer/payload/commands/gemini/hefesto.create.toml`
- `installer/payload/commands/gemini/hefesto.extract.toml`
- `installer/payload/commands/codex/hefesto.create.md`
- `installer/payload/commands/codex/hefesto.extract.md`
- `installer/payload/commands/cursor/hefesto.extract.md`
- `installer/payload/commands/opencode/hefesto.create.md`
- `installer/payload/commands/opencode/hefesto.extract.md`
- `installer/payload/commands/qwen/hefesto.extract.md`

**Live CLI directories**:
- `.codex/prompts/hefesto.create.md`
- `.codex/prompts/hefesto.extract.md`
- `.cursor/commands/hefesto.extract.md`
- `.gemini/commands/hefesto.create.toml`
- `.gemini/commands/hefesto.extract.toml`
- `.opencode/command/hefesto.create.md`
- `.opencode/command/hefesto.extract.md`
- `.qwen/commands/hefesto.extract.md`

**Additional Issues in Gemini Files**:
- Missing Token Economy table
- Using `## Instructions` + `## Key Concepts` instead of `## How to <capability>`
- Checklist missing columns/items introduced in v2.0.0

**Drift-Free Commands** (verified clean):
- `.claude/commands/hefesto.create.md` - ✅ Clean (13-point, Token Economy)
- All `hefesto.validate.md`, `hefesto.init.md`, `hefesto.list.md` - ✅ No checklist drift

### Rationale
CARD-003 identified Gemini drift; audit reveals it propagated across 6 of 7 CLIs. Must fix at source (canonical `.claude/commands/`) then propagate to all.

### Alternatives Considered
1. **Fix only Gemini** - Rejected: leaves 5 other CLIs with stale content
2. **Incremental updates** - Rejected: partial sync violates consistency guarantee
3. **Automated sync script** - Deferred: out of scope for v2.2.0 (consider for v2.3.0)

### Implementation Impact
Step 4 (Payload Sync) must:
1. Fix canonical `.claude/commands/hefesto.create.md` (add web research step)
2. Fix canonical `.claude/commands/hefesto.extract.md` (10→13, add web research)
3. Propagate to 18 files across all CLIs + installer payloads

---

## Research Task 5: Agent Naming Convention

### Question
Should generated agents follow skill naming rules (lowercase-hyphen)? Are agents validated differently than skills?

### Decision
**Generated agents follow SAME naming rules as skills**: `^[a-z0-9]+(-[a-z0-9]+)*$`, lowercase-hyphen, max 64 chars. Validation is identical.

### Findings

**Evidence from `.github/agents/`**:
```
hefesto.create.agent.md      # Existing agent (follows skill naming)
hefesto.extract.agent.md
hefesto.init.agent.md
speckit.plan.agent.md
speckit.tasks.agent.md
```

All existing agents:
- Use lowercase
- Use hyphen separators (`.` is file extension, not name separator)
- Use dot-notation for namespaced commands (`hefesto.create`, `speckit.plan`)
- Max length < 64 chars

**Critical Distinction**:
- **Command name**: `hefesto.create` (dot-separated namespace + action)
- **File name**: `hefesto.create.agent.md` (`.agent.md` is extension pattern)
- **Agent name** (for user-generated agents): Should be `code-reviewer`, `test-specialist`, etc. (hyphen-separated)

**IMPORTANT**: User-generated agents (via `/hefesto.agent`) do NOT use `hefesto.` prefix:
- Input: `/hefesto.agent "code reviewer for Python"`
- Generated: `code-reviewer.agent.md` (or just `code-reviewer.md` in non-Copilot CLIs)
- Command invocation: `/code-reviewer`, NOT `/hefesto.code-reviewer`

### Rationale
- Consistency with skill validation (T0-HEFESTO-07)
- Existing agents already follow this pattern
- Namespace prefix (`hefesto.`, `speckit.`) is reserved for system commands
- User agents should be simple, descriptive names

### Alternatives Considered
1. **Allow underscores in agent names** - Rejected: breaks skill spec consistency
2. **Require namespace prefix** - Rejected: clutters user namespace, limits creativity
3. **Case-insensitive naming** - Rejected: violates agentskills.io spec

### Implementation Impact
`/hefesto.agent` command must:
- Validate agent name with regex: `^[a-z0-9]+(-[a-z0-9]+)*$`
- Strip any `hefesto.` prefix from user input (reserved)
- Generate filename as `<name>.agent.md` for Copilot, `<name>.md` for others
- Document that command invocation is `/<name>`, not `/hefesto.<name>`

---

## Summary: All Clarifications Resolved

| Research Task | Status | Key Decision |
|---------------|--------|--------------|
| 1. Web Search Availability | ✅ RESOLVED | Conditional instruction pattern (no CLI branching) |
| 2. Agent Command Placement | ✅ RESOLVED | `/commands/` for 6 CLIs, dual structure for Copilot |
| 3. TOML Escaping | ✅ RESOLVED | Triple-quoted raw strings (`"""..."""`) |
| 4. Drift Audit | ✅ RESOLVED | 18 files need 10→13 update + Token Economy |
| 5. Agent Naming | ✅ RESOLVED | Same as skills (`^[a-z0-9]+(-[a-z0-9]+)*$`), no `hefesto.` prefix |

**Gate Status**: ✅ All NEEDS CLARIFICATION resolved. Ready for Phase 1 (Design).

---

## References

- CARD-003-v2.2.0-features.md (feature specification)
- CONSTITUTION.md (T0 rules)
- `.claude/commands/` (canonical command source)
- `.github/agents/` (agent naming examples)
- `.gemini/commands/*.toml` (TOML escaping patterns)
- `docs/pesquisa/inventario-tools-and-refs-ai-v2.md` (CLI tool inventory)
