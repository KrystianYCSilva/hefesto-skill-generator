<!--
  SYNC IMPACT REPORT
  ==================
  Version Change: 1.0.0 → 2.0.0
  
  Modified Principles:
  - [Spec-First Development] → VIII. Spec-First Development (Retained as Process Rule)
  - [Human Gate Protocol] → II. Human Gate Protocol (Aligned with T0-HEFESTO-02)
  - [Test-Driven Implementation] → III. Quality-Driven & Auto-Critique (Aligned with T0-HEFESTO-12 & T0-HEFESTO-06)
  - [Progressive Documentation] → IV. Progressive Disclosure (Aligned with T0-HEFESTO-03)
  - [Constitution Compliance] → IX. Constitution Compliance
  
  Added Principles (from Root Constitution):
  - I. Agent Skills Standard (T0-HEFESTO-01, T0-HEFESTO-07)
  - V. Multi-CLI Support (T0-HEFESTO-04, T0-HEFESTO-09)
  - VI. Local Storage (T0-HEFESTO-05)
  - VII. Template Authority (T0-HEFESTO-13)
  - X. Safety & Security (T0-HEFESTO-11)
  
  Added Sections:
  - Runtime Guidance (Reference to Root Constitution)
  
  Templates Requiring Updates:
  ✅ .specify/templates/plan-template.md - Constitution Check aligned with new T0 rules
  ✅ .specify/templates/spec-template.md - Requirements aligned with T0 constraints
  ✅ .specify/templates/tasks-template.md - "Test-Driven" steps interpreted as "Quality/Validation" steps
  
  Follow-up TODOs: None
  
  Rationale for v2.0.0:
  - Synchronization with project-root CONSTITUTION.md (v2.0.0)
  - Adoption of T0-HEFESTO Absolute Rules as governing principles
  - Adjustment of "Test-Driven" to "Quality-Driven" to reflect Template-Driven architecture (Zero Python)
-->

# Hefesto Skill Generator Constitution

## Core Principles

### I. Agent Skills Standard (T0-01, T0-07)

All generated skills MUST strictly adhere to the [agentskills.io](https://agentskills.io) specification.
- **Naming**: Lowercase, hyphens only, max 64 chars (`^[a-z0-9]+(-[a-z0-9]+)*$`).
- **Structure**: Valid frontmatter (name, description) and Markdown body.
- **Description**: Actionable, max 1024 chars, with "Use when:" trigger.

**Rationale**: Ensures interoperability and standard compliance across the ecosystem.

### II. Human Gate Protocol (T0-02)

NUNCA persistir skill ou artefato sem aprovação humana explícita.
The system MUST offer `[approve]`, `[edit]`, `[reject]` options and MUST NOT assume implicit approval.

**Rationale**: Maintains human authority over project direction and prevents unwanted modifications.

### III. Quality-Driven & Auto-Critique (T0-06, T0-12)

Every generated artifact MUST undergo automatic validation before presentation to the user.
- **Skills**: Must pass the 13-point Quality Checklist (valid spec, token economy, security).
- **Process**: Generate -> Auto-Critique -> Fix -> Human Gate.

**Rationale**: Reduces human cognitive load by ensuring only high-quality, valid artifacts are presented for review.

### IV. Progressive Disclosure (T0-03)

Skills and documentation MUST follow Progressive Disclosure limits.
- **SKILL.md**: < 500 lines, < ~5000 tokens.
- **Context**: Detailed resources MUST be in `references/`, `scripts/`, or `assets/` subdirectories, loaded Just-In-Time.

**Rationale**: Optimizes context window usage and maintains readability.

### V. Multi-CLI Support (T0-04, T0-09)

Hefesto is CLI-agnostic. Features MUST support ALL 7 target CLIs (Claude, Gemini, Codex, Copilot, OpenCode, Cursor, Qwen).
- **Detection**: Detect installed CLIs automatically (T0-04).
- **Compatibility**: Adapt syntax (`$ARGUMENTS` vs `{{args}}`) for each target (T0-09).

**Rationale**: Ensures universality and prevents vendor lock-in.

### VI. Local Storage (T0-05)

Skills MUST be stored in the project's local directories by default (e.g., `.claude/skills/`, `.gemini/skills/`). Global storage is prohibited without explicit user request.

**Rationale**: Respects project boundaries and portability.

### VII. Template Authority (T0-13)

**Zero Code Policy**: All Hefesto logic LIVES in Markdown templates.
- NO Python/Node.js logic for core skill generation.
- Commands (`hefesto.*.md`) are the source of truth.

**Rationale**: Ensures zero dependencies and maximum portability (run anywhere with an LLM).

### VIII. Spec-First Development

Every feature begins with a complete specification before implementation.
- **Inputs**: User intent -> `spec.md` -> `plan.md`.
- **Constraint**: No template changes until the specification is approved.

**Rationale**: Prevents scope creep and ensures alignment with T0 rules.

### IX. Constitution Compliance

All generated artifacts MUST pass Constitution Check (T0 Validation) before research and implementation. Violations of T0 rules are **FORBIDDEN** (T0 is Absolute).

**Rationale**: Enforces the "Inviolable" nature of the T0 rules defined in the root `CONSTITUTION.md`.

### X. Safety & Security (T0-11)

Skills MUST be secure by default.
- NO credentials, tokens, or PII in generated files.
- NO internal/private URLs unless explicitly verified.

**Rationale**: Prevents accidental leakage of sensitive information.

## Development Workflow

### Phase 0: Research (plan command)
- Load feature requirement
- Verify against **T0 Rules** (Constitution Check)
- Generate `plan.md` adhering to **Template Authority** (VII)
- Present for Human Gate approval

### Phase 1: Design (plan command)
- Generate `data-model.md` or Template Specs
- Define **Multi-CLI** adaptation strategy (V)
- Re-validate against **Agent Skills Standard** (I)
- Present for Human Gate approval

### Phase 2: Task Breakdown (tasks command)
- Generate `tasks.md` organized by user story
- Ensure tasks include **Quality-Driven** validation steps (III)
- Group tasks to maintain **Idempotency** (T0-08)
- Present for Human Gate approval

### Phase 3: Implementation
- Execute tasks obeying **Template Authority** (logic in MD)
- Verify **Progressive Disclosure** (IV) limits are met
- Perform **Auto-Critique** (III) on outputs
- **Human Gate** (II) before final persistence

## Quality Gates

### Pre-Research Gate (Before Phase 0)
- [ ] Feature request does not violate **T0 Rules** (e.g., no request for Python logic)
- [ ] Constitution Check passes

### Pre-Design Gate (Before Phase 1)
- [ ] Plan respects **Template Authority** (Zero Code)
- [ ] **Multi-CLI** strategy defined

### Pre-Implementation Gate (Before Phase 2)
- [ ] Design artifacts comply with **Agent Skills Standard**
- [ ] **Safety & Security** review passed (no PII/Secrets in spec)

### Artifact Gate (During Phase 3)
- [ ] **Auto-Critique** Checklist (13 points) PASS
- [ ] **Progressive Disclosure** limits respected (<500 lines)
- [ ] **Human Gate** approval obtained

## Governance

### Amendment Procedure

1. **Proposal**: Changes to this constitution must be reflected in the root `CONSTITUTION.md` first.
2. **Sync**: This file (`.specify/memory/constitution.md`) tracks the root `CONSTITUTION.md`.
3. **Approval**: Explicit human approval required for T0 rule changes.
4. **Version**: Follows Semantic Versioning.

### Versioning Policy

- **MAJOR**: Changes to T0 (Absolute) rules.
- **MINOR**: New T1 (Normative) rules or workflow adjustments.
- **PATCH**: Clarifications and typos.

### Compliance Review

All `/speckit` commands MUST verify compliance with this constitution. **T0 violations are blocking errors** and cannot be overridden.

### Runtime Guidance

This document governs the **development process** of Hefesto.
For the **product rules** (the supreme law of the generated skills), refer to `CONSTITUTION.md` at the repository root.
In case of conflict, the root `CONSTITUTION.md` (T0 Rules) prevails.

**Version**: 2.0.0 | **Ratified**: 2026-02-07 | **Last Amended**: 2026-02-08