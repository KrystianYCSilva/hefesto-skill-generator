---
description: "Quickstart guide with step-by-step instructions and test scenarios for Hefesto Foundation Infrastructure"
feature: "001-hefesto-foundation"
type: "quickstart"
audience: "developers"
status: "complete"
created: "2026-02-04"
version: "1.0.0"
---

# Quickstart: Hefesto Foundation Infrastructure

**Feature**: 001-hefesto-foundation  
**Audience**: Developers implementing or testing the Hefesto Foundation  
**Date**: 2026-02-04

## Overview

This guide provides step-by-step instructions for implementing, testing, and using the Hefesto Foundation Infrastructure. It covers bootstrap operations, CLI detection, state management, and constitutional governance validation.

---

## Prerequisites

### System Requirements

- **Operating System**: Windows 10+, macOS 10.15+, or Linux (any modern distribution)
- **Disk Space**: Minimum 100MB free space in project directory
- **Permissions**: Read/write access to project directory
- **Shell**: PowerShell (Windows) or Bash/Zsh (macOS/Linux)

### Recommended (Not Required)

- **Git**: For version control integration
- **At least one AI CLI installed**: Claude Code, Gemini CLI, OpenAI Codex, VS Code/Copilot, OpenCode, Cursor, or Qwen Code

---

## Installation

### Step 1: Clone or Initialize Hefesto

```bash
# If starting fresh
git clone https://github.com/your-org/hefesto-skill-generator.git
cd hefesto-skill-generator

# Or, if adding to existing project
cd your-existing-project
# Copy Hefesto files to project root
```

### Step 2: Verify Project Structure

Ensure the following key files exist:

```text
project-root/
├── CONSTITUTION.md        # Governance rules (bundled with Hefesto)
├── AGENTS.md             # AI agent bootstrap guide
└── .context/             # Context directory for AI agents
    ├── ai-assistant-guide.md
    └── standards/
        └── architectural-rules.md
```

---

## Bootstrap Process

### Step 3: Run Bootstrap Command

The bootstrap command initializes Hefesto in your project by detecting installed CLIs and creating necessary directory structures.

**Via AI Agent** (recommended):

```text
In your AI CLI (Claude Code, Gemini CLI, etc.):
> /hefesto.init

Or:
> Run Hefesto bootstrap to initialize project
```

**Expected Output**:

```markdown
## Hefesto Bootstrap

🔍 Detecting installed AI CLIs...

✅ Detected 3 CLIs:
- Claude Code (v1.2.0) → .claude/skills/
- Gemini CLI (config only, ⚠️ not in PATH) → .gemini/skills/
- OpenCode (v0.2.1) → .opencode/skills/

📁 Creating directory structures...
✅ Created .claude/skills/
✅ Created .gemini/skills/
✅ Created .opencode/skills/

📄 Initializing MEMORY.md...
✅ State file created

📜 Verifying CONSTITUTION.md...
✅ Constitution validated

✅ Bootstrap completed in 3.2 seconds

## Next Steps
1. Run `/hefesto.list` to verify installation
2. Run `/hefesto.create` to generate your first skill
```

### Step 4: Verify Installation

Check that files and directories were created:

```bash
# Verify MEMORY.md exists
ls -la MEMORY.md

# Verify CLI directories
ls -la .claude/ .gemini/ .opencode/

# View initial state
cat MEMORY.md
```

**Expected MEMORY.md Content**:

```markdown
---
hefesto_version: "1.0.0"
initialized: 2026-02-04T14:30:00Z
last_updated: 2026-02-04T14:30:00Z
---

# Hefesto Project State

## Detected CLIs

| CLI | Detection Method | Skills Directory | Version | Status |
|-----|------------------|------------------|---------|--------|
| claude | PATH | .claude/skills/ | 1.2.0 | active |
| gemini | config_directory | .gemini/skills/ | null | warning_no_path |
| opencode | PATH | .opencode/skills/ | 0.2.1 | active |

## Skill Registry

(No skills generated yet)

## State Metadata

- **Total Skills**: 0
- **Active CLIs**: 3
- **Last Validation**: 2026-02-04T14:30:00Z
```

---

## Testing Scenarios

### Test 1: Successful Bootstrap (Happy Path)

**Setup**: Fresh project with Claude Code installed in PATH

**Steps**:
1. Run `/hefesto.init`
2. Verify `.claude/skills/` directory created
3. Verify MEMORY.md shows Claude as "active"
4. Verify bootstrap completes in < 5 seconds

**Expected Result**: ✅ Bootstrap successful, Claude Code detected via PATH

---

### Test 2: Config-Only CLI Detection

**Setup**: Gemini CLI has `~/.gemini/` config directory but is not in PATH

**Steps**:
1. Remove Gemini from PATH: `export PATH=$(echo $PATH | tr ':' '\n' | grep -v gemini | tr '\n' ':')`
2. Ensure `~/.gemini/` directory exists
3. Run `/hefesto.init`
4. Check MEMORY.md for Gemini entry

**Expected Result**: 
- ✅ Gemini detected via config_directory
- ⚠️  Warning: "CLI detected via config directory but not found in PATH"
- ✅ `.gemini/skills/` directory created
- ✅ Status: "warning_no_path"

---

### Test 3: Permission Error Handling

**Setup**: `.github/` directory exists with read-only permissions

**Steps**:
1. Make `.github/` read-only: `chmod 444 .github/`
2. Run `/hefesto.init`
3. Check bootstrap output for error message

**Expected Result**:
- ❌ Error: "Permission denied creating .github/skills/"
- ✅ Other CLIs processed successfully
- ✅ Error reported in summary with resolution steps
- ✅ Bootstrap continues (does not abort)

---

### Test 4: No CLIs Detected (Fallback)

**Setup**: No AI CLIs installed, no config directories

**Steps**:
1. Ensure no CLIs in PATH
2. Ensure no CLI config directories exist
3. Run `/hefesto.init`

**Expected Result**:
- ℹ️  Prompt: "No AI CLIs detected. Specify manually:"
- ℹ️  List of supported CLIs presented
- ⏸️  Bootstrap pauses for user input
- After user selects CLI → directory created with status "manual"

---

### Test 5: Idempotent Bootstrap

**Setup**: Hefesto already initialized, CLI directories exist

**Steps**:
1. Run `/hefesto.init` (initial bootstrap)
2. Wait 5 seconds
3. Run `/hefesto.init` again

**Expected Result**:
- ✅ Second run completes without errors
- ✅ No duplicate directories created
- ✅ MEMORY.md `last_updated` timestamp updated
- ✅ Existing directories unchanged
- ℹ️  Message: "Hefesto already initialized. Re-validating..."

---

### Test 6: Corrupted MEMORY.md Recovery

**Setup**: MEMORY.md with invalid YAML

**Steps**:
1. Manually corrupt MEMORY.md (add invalid YAML syntax)
2. Run any `/hefesto.*` command

**Expected Result**:
- ⚠️  Warning: "MEMORY.md is corrupted"
- ✅ Backup created: `MEMORY.md.backup.2026-02-04T15-30-00`
- ✅ Fresh MEMORY.md created
- ✅ Filesystem scanned to rebuild state
- ✅ Command proceeds normally

---

### Test 7: Missing CONSTITUTION.md Recovery

**Setup**: CONSTITUTION.md deleted from project

**Steps**:
1. Delete `CONSTITUTION.md`: `rm CONSTITUTION.md`
2. Run any `/hefesto.*` command

**Expected Result**:
- ⚠️  Warning: "CONSTITUTION.md missing"
- ✅ Restored from bundled copy
- ✅ Validation passes
- ✅ Command proceeds normally

---

### Test 8: CLI Installed After Bootstrap

**Setup**: Hefesto initialized with Claude only, then Cursor installed

**Steps**:
1. Run `/hefesto.init` with only Claude installed
2. Install Cursor
3. Run `/hefesto.detect` (re-detection command)

**Expected Result**:
- ✅ Cursor detected and added to MEMORY.md
- ✅ `.cursor/skills/` directory created
- ✅ Existing Claude configuration unchanged
- ℹ️  Message: "Detected 1 new CLI: cursor"

---

## Common Commands

### Initialize Hefesto

```text
/hefesto.init
```

Detects CLIs, creates directories, initializes state.

---

### Re-detect CLIs

```text
/hefesto.detect
```

Scans for newly installed CLIs after initial bootstrap.

---

### List Detected CLIs

```text
/hefesto.list --clis
```

Displays all detected CLIs and their status.

---

### View Current State

```text
cat MEMORY.md
```

Shows raw state file (for debugging).

---

### Validate Constitution

```text
/hefesto.validate --constitution
```

Checks CONSTITUTION.md integrity and T0 rule presence.

---

## Troubleshooting

### Problem: "No CLIs detected"

**Symptoms**: Bootstrap fails to find any AI CLIs

**Solutions**:
1. Verify at least one CLI is installed:
   ```bash
   which claude gemini codex code opencode cursor qwen
   ```
2. If installed but not detected, check PATH:
   ```bash
   echo $PATH  # Unix/macOS
   echo %PATH%  # Windows
   ```
3. Manually specify CLI when prompted
4. Check for config directories:
   ```bash
   ls -la ~/.claude ~/.gemini ~/.codex ~/.opencode ~/.cursor ~/.qwen
   ```

---

### Problem: "Permission denied" creating directories

**Symptoms**: Error message about permissions during bootstrap

**Solutions**:
1. Check project directory permissions:
   ```bash
   ls -la .
   ```
2. Ensure you have write access to project directory
3. If directory is read-only, change permissions:
   ```bash
   chmod u+w .
   ```
4. On Windows, right-click project folder → Properties → Security → ensure your user has "Modify" permission

---

### Problem: MEMORY.md shows "warning_no_path"

**Symptoms**: CLI detected but status is "warning_no_path"

**Explanation**: CLI config directory exists but CLI is not in PATH

**Solutions**:
1. Add CLI to PATH:
   ```bash
   export PATH=$PATH:/path/to/cli/bin  # Unix/macOS
   set PATH=%PATH%;C:\path\to\cli\bin  # Windows
   ```
2. Or, accept warning and proceed (skill generation will still work if CLI is manually accessible)

---

### Problem: Bootstrap takes longer than 5 seconds

**Symptoms**: Slow detection or directory creation

**Possible Causes**:
- Network filesystem (NFS, SMB)
- Antivirus scanning new directories
- Slow disk I/O

**Solutions**:
1. Run on local filesystem
2. Temporarily disable antivirus for project directory
3. Check disk health: `df -h` (Unix) or `wmic diskdrive get status` (Windows)

---

### Problem: Git worktree has different MEMORY.md than main

**Symptoms**: State differs between worktrees

**Explanation**: Each worktree should have independent state

**Solutions**:
1. Run `/hefesto.init` in each worktree separately
2. Each worktree gets its own MEMORY.md
3. CONSTITUTION.md can be shared (symlink or copy)

---

## Performance Benchmarks

| Operation | Target | Typical |
|-----------|--------|---------|
| CLI detection (7 CLIs) | < 2s | 1.2s |
| Directory creation (3 CLIs) | < 1s | 0.4s |
| MEMORY.md write | < 100ms | 45ms |
| CONSTITUTION validation | < 500ms | 250ms |
| **Total Bootstrap** | **< 5s** | **3.2s** |

---

## Next Steps

After successful bootstrap, you can:

1. **Generate your first skill**: `/hefesto.create <description>`
2. **Extract from existing code**: `/hefesto.extract @file.ts`
3. **List available commands**: `/hefesto.help`
4. **Read the constitution**: `cat CONSTITUTION.md`

---

## Appendix: Directory Structure After Bootstrap

```text
your-project/
├── CONSTITUTION.md               # Governance (Tier 0)
├── MEMORY.md                     # Persistent state
├── AGENTS.md                     # AI agent guide
│
├── .claude/                      # Claude Code (if detected)
│   └── skills/                   # Empty initially
│
├── .gemini/                      # Gemini CLI (if detected)
│   └── skills/                   # Empty initially
│
├── .codex/                       # OpenAI Codex (if detected)
│   └── skills/                   # Empty initially
│
├── .github/                      # VS Code/Copilot (if detected)
│   └── skills/                   # Empty initially
│
├── .opencode/                    # OpenCode (if detected)
│   └── skills/                   # Empty initially
│
├── .cursor/                      # Cursor (if detected)
│   └── skills/                   # Empty initially
│
└── .qwen/                        # Qwen Code (if detected)
    └── skills/                   # Empty initially
```

---

## Support

For issues or questions:
1. Check `.context/troubleshooting/common-issues.md`
2. Review AGENTS.md for AI-specific guidance
3. Validate against CONSTITUTION.md for governance rules
4. File an issue at project repository

---

**Quickstart Guide** | Hefesto Foundation Infrastructure | v1.0.0
