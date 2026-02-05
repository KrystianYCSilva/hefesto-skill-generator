# Copilot instructions for Hefesto Skill Generator

Purpose: Provide concise, repository-specific guidance for Copilot/Copilot CLI sessions working in this repository.

1) Build, test, and lint commands
- No standard build/test/lint toolchain detected in repository root (no package.json, no pytest, no Maven/Gradle project). Primary workflows are spec-driven and run via PowerShell scripts and repository commands.
- Create/new-feature helper (referenced in repo docs): `.specify/scripts/powershell/create-new-feature.ps1` (run from repo root with PowerShell when available). Also available workflows in `.specify/` templates and `commands/` directory for agent-driven commands.
- Single-test note: no unit test runner was found; see `.context/standards/testing-strategy.md` for the project testing guidance and add test scripts there if you introduce a test framework.

2) High-level architecture (brief)
- Spec-driven generator: primary source-of-truth are files under `specs/` and `commands/` which drive generation flows.
- Four-phase generation flow used by agents and scripts: Template-first -> Human Gate (explicit approval) -> Wizard interactive expansion -> Multi-CLI generation & persistence.
- Progressive Disclosure: skills use a small SKILL.md core + JIT sub-resources (metadata.yaml, scripts/, references/, assets/) to keep context small.
- Multi-CLI distribution: generated skill artifacts are stored per CLI under top-level dot-folders (examples: `.claude/skills/`, `.gemini/skills/`, `.codex/skills/`, `.opencode/skills/`, `.cursor/skills/`, `.qwen/skills/`, `.github/skills/` for Copilot/VS Code).

3) Key conventions Copilot must follow
- T0 rules from CONSTITUTION.md are authoritative. Always load/validate against CONSTITUTION.md before proposing or persisting changes.
- Human Gate: never persist a generated skill file without explicit human approval; agents/actions must present `[approve]`, `[expand]`, `[edit]`, `[reject]` options.
- SKILL.md constraints: keep core SKILL.md < 500 lines and < 5000 tokens; heavy docs belong in references/ or metadata JIT files.
- Frontmatter: each SKILL.md must include YAML frontmatter with at least `name` and `description`. `name` must be lowercase, hyphen-separated, max 64 chars; `description` max 1024 chars.
- Metadata JIT: extended metadata should live in `metadata.yaml` or similar and be loaded on demand; prefer small frontmatter in SKILL.md.
- CLI detection: check PATH and config dirs before asking user which CLIs to target; generate for all detected CLIs (priority: PATH -> config dirs).
- Idempotency: if a skill already exists, present options `[overwrite]`, `[merge]`, `[cancel]` and maintain backups; do not overwrite silently.
- Security: sanitize inputs (size limits, shell escaping), never write secrets into skill files, follow T0-HEFESTO-11 rules.
- Placement conventions: specs in `specs/`; command docs in `commands/`; helper templates in `commands/templates/`; context and standards in `.context/`.

4) AI assistant / agent integrations to be aware of
- Important repo files for agent behavior: `CONSTITUTION.md`, `AGENTS.md`, `MEMORY.md`, `.context/ai-assistant-guide.md` and `.context/standards/architectural-rules.md` (these contain T0 rules and required context-loading steps).
- There are existing agent definitions and prompts under `.github/agents/` and `.github/prompts/` and many per-CLI copies under `.<cli>/commands` and `.<cli>/skills/` — reuse those templates when generating CLI-specific artifacts.

5) Quick actionable checklist for Copilot sessions
- Load `.context/` files and CONSTITUTION.md first (T0 priority).
- Validate any generated SKILL.md against the Agent Skills spec checklist in CONSTITUTION.md before proposing persistence.
- Detect CLIs automatically; if none are detected, ask which target CLI(s) to generate for.
- Keep generated SKILL.md minimal and offer JIT resources for expansion.

References and pointers: README.md, CONSTITUTION.md, AGENTS.md, MEMORY.md, `.context/` and `commands/`.

---

If any of this should be adjusted or expanded (for example to add explicit test/run commands for a chosen test framework), say so and Copilot sessions will update this file accordingly.