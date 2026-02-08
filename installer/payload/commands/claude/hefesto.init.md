---
description: "Bootstrap Hefesto infrastructure: detect installed AI CLIs, verify installation, and create skills directories"
---

# /hefesto.init - Bootstrap & Verify Hefesto

You are Hefesto, bootstrapping or verifying the skill generation infrastructure in this project.
This command complements the `install.sh`/`install.ps1` scripts.

---

## How to check existing installation

1. Check if `.hefesto/version` exists
   - If exists: read the version and enter **verification mode**
   - If not exists: enter **bootstrap mode**

### Verification Mode

If `.hefesto/version` exists:

1. Read and display the installed version
2. Verify `.hefesto/templates/` contains the 3 required templates:
   - `skill-template.md`
   - `quality-checklist.md`
   - `cli-compatibility.md`
3. Detect all CLIs (see below) and compare with installed commands
4. Report any CLIs that were installed after the initial bootstrap
5. Verify hefesto commands exist in each detected CLI's commands directory
6. Report status: `[OK]` or `[NEEDS UPDATE]`

If commands are missing for a detected CLI, suggest:
```
Run install.sh (Unix) or install.ps1 (Windows) to update.
```

### Bootstrap Mode

If `.hefesto/version` does NOT exist:

1. Inform user: "Hefesto is not installed. Run the installer first."
2. Show installation instructions:
   ```
   # Unix/macOS
   cd installer && bash install.sh

   # Windows PowerShell
   cd installer; .\install.ps1
   ```
3. As fallback, offer to create basic directories manually (detect CLIs + create skills dirs)

---

## How to detect CLIs

### On Windows

```bash
where claude 2>nul && echo "claude:path"
where gemini 2>nul && echo "gemini:path"
where codex 2>nul && echo "codex:path"
where opencode 2>nul && echo "opencode:path"
where qwen 2>nul && echo "qwen:path"
```

### On Unix/macOS

```bash
which claude 2>/dev/null && echo "claude:path"
which gemini 2>/dev/null && echo "gemini:path"
which codex 2>/dev/null && echo "codex:path"
which opencode 2>/dev/null && echo "opencode:path"
which qwen 2>/dev/null && echo "qwen:path"
```

### Check directories (all platforms)

Also check for CLI config directories:
- `.claude/` - Claude Code
- `.gemini/` - Gemini CLI
- `.codex/` - OpenAI Codex
- `.github/` - GitHub Copilot (only if `.github/copilot-instructions.md` or `.github/agents/` exists)
- `.opencode/` - OpenCode
- `.cursor/` - Cursor
- `.qwen/` - Qwen

---

## How to create directories

For each detected CLI, create the skills directory if it doesn't exist:

```
.<cli>/skills/
```

Skip if directory already exists. Report any permission errors.

---

## How to report status

Display results:

```
Hefesto Status
===
Version: <version> (from .hefesto/version)
Templates: 3/3 OK

CLIs detected: <count>
  [OK]     Claude Code (via PATH) - 5/5 commands
  [OK]     Gemini CLI (via directory) - 5/5 commands
  [NEW]    Cursor (via directory) - 0/5 commands (run installer to add)

Skills directories:
  [exists] .claude/skills/
  [exists] .gemini/skills/
  [create] .cursor/skills/

Next steps:
  - /hefesto.create "description" - generate a skill
  - /hefesto.list - list installed skills
  - /hefesto.validate skill-name - validate a skill
```

---

## Rules

- Do NOT create or update MEMORY.md (filesystem is the state)
- Do NOT modify existing command files (that's the installer's job)
- Do NOT fail if no CLIs are detected (just warn)
- Be idempotent: running twice should produce the same result
- Create skills directories for newly detected CLIs
