---
description: "Help command to display available commands, usage information, and quick reference"
command: "/hefesto.help"
category: "information"
phase: "polish"
version: "1.0.0"
---

# /hefesto.help - Help Command

**Command**: `/hefesto.help`  
**Purpose**: Display available commands, usage information, and quick reference  
**Phase**: Polish & Cross-Cutting

---

## Overview

The `/hefesto.help` command provides comprehensive help information about Hefesto commands, options, and troubleshooting.

---

## Command Signature

```text
/hefesto.help [command] [--verbose]

Arguments:
  command       Show detailed help for specific command (optional)
  
Options:
  --verbose     Show extended help with examples and troubleshooting
```

---

## Usage Examples

### Example 1: General Help

```text
> /hefesto.help

# Hefesto Skill Generator - Command Reference

**Version**: 1.0.0  
**Status**: Initialized ✅

## Available Commands

### Initialization & Detection
- `/hefesto.init` - Initialize Hefesto in project
- `/hefesto.detect` - Re-detect installed AI CLIs

### State & Information
- `/hefesto.list [--clis|--skills|--check-sync]` - List CLIs and skills
- `/hefesto.help [command]` - Show this help

### Skill Management (Future)
- `/hefesto.create` - Create new skill from description
- `/hefesto.extract` - Extract skill from existing code
- `/hefesto.validate` - Validate skill against spec
- `/hefesto.adapt` - Adapt skill for different CLI
- `/hefesto.sync` - Synchronize skills across CLIs

## Quick Start

1. Initialize Hefesto: `/hefesto.init`
2. List detected CLIs: `/hefesto.list --clis`
3. Create your first skill: `/hefesto.create`

## Get Help

- Command help: `/hefesto.help <command>`
- Troubleshooting: Check `.context/troubleshooting/foundation-issues.md`
- Full docs: `AGENTS.md` and `CONSTITUTION.md`

## Resources

- **Agent Skills Spec**: https://agentskills.io
- **Project State**: `MEMORY.md`
- **Governance Rules**: `CONSTITUTION.md` (11 T0 rules)
```

### Example 2: Command-Specific Help

```text
> /hefesto.help init

# /hefesto.init - Initialize Hefesto

**Purpose**: Bootstrap Hefesto infrastructure in your project

## Usage

```
/hefesto.init [--force] [--verbose] [--no-emoji]
```

## Options

- `--force` - Re-run initialization even if already initialized
- `--verbose` - Show detailed detection and creation logs
- `--no-emoji` - Disable emoji output (for terminals without Unicode)

## What It Does

1. ✅ Validates CONSTITUTION.md (auto-restores if missing)
2. 🔍 Detects installed AI CLIs via PATH and config directories
3. 📁 Creates skill directory structures (`.{cli}/skills/`)
4. 📄 Initializes MEMORY.md with project state
5. 📊 Generates bootstrap report

## Performance

- Target: < 5 seconds
- Typical: 2-4 seconds

## Examples

```bash
# First-time initialization
/hefesto.init

# Re-initialize with verbose output
/hefesto.init --force --verbose

# Initialize without emoji (for basic terminals)
/hefesto.init --no-emoji
```

## Troubleshooting

**No CLIs detected?**
- Ensure at least one AI CLI is installed
- Check PATH environment variable
- Use manual specification when prompted

**Permission errors?**
- Run with appropriate permissions
- Check directory write access
- See `.context/troubleshooting/foundation-issues.md`

## See Also

- `/hefesto.detect` - Re-detect CLIs after installation
- `/hefesto.list` - View initialization results
- `AGENTS.md` - Full documentation
```

### Example 3: Verbose Help

```text
> /hefesto.help --verbose

# Hefesto Skill Generator - Complete Reference

**Version**: 1.0.0  
**Documentation**: `AGENTS.md`, `CONSTITUTION.md`

---

## Command Categories

### 🚀 Initialization Commands

#### `/hefesto.init [--force] [--verbose] [--no-emoji]`
Initialize Hefesto infrastructure in project

**What it does**:
- Validates CONSTITUTION.md
- Detects installed AI CLIs (7 supported)
- Creates `.{cli}/skills/` directories
- Initializes MEMORY.md state file
- Generates bootstrap report

**When to use**:
- First time setting up Hefesto in project
- After cloning project without Hefesto files
- To re-detect CLIs with `--force`

**Performance**: < 5s (typical: 2-4s)

**Common issues**:
- No CLIs detected → Install an AI CLI first
- Permission errors → Check directory permissions
- Already initialized → Use `--force` to re-run

**Related**: `/hefesto.detect`

---

#### `/hefesto.detect [--force] [--verbose]`
Re-detect and add newly installed AI CLIs

**What it does**:
- Runs CLI detection (reuses init logic)
- Identifies new vs. existing CLIs
- Creates directories only for new CLIs
- Updates MEMORY.md with new entries
- Shows detection report

**When to use**:
- After installing a new AI CLI
- To update CLI versions
- To verify CLI detection

**Performance**: < 2s (typical: 1-2s)

**Common issues**:
- New CLI not detected → Ensure it's in PATH
- Permission errors → Check new CLI directory permissions

**Related**: `/hefesto.init`

---

### 📊 Information Commands

#### `/hefesto.list [--clis] [--skills] [--verbose] [--check-sync]`
Display detected CLIs and generated skills

**What it does**:
- Parses MEMORY.md (with corruption recovery)
- Lists detected CLIs with status
- Shows skill registry
- Displays state metadata
- Optionally checks filesystem sync

**Options**:
- `--clis` - Show only CLI list
- `--skills` - Show only skills
- `--verbose` - Show detailed info (paths, timestamps)
- `--check-sync` - Check filesystem consistency

**When to use**:
- To verify initialization
- To see what CLIs are detected
- To list generated skills
- To check for inconsistencies

**Performance**: < 100ms without sync, < 200ms with sync

**Common issues**:
- Corrupted MEMORY.md → Auto-recovers, creates backup
- Inconsistencies detected → Run `/hefesto.sync` (future)

**Related**: `/hefesto.init`, `/hefesto.detect`

---

#### `/hefesto.help [command] [--verbose]`
Show command help and reference

**What it does**:
- Displays available commands
- Shows command-specific help
- Provides troubleshooting tips
- Links to documentation

**Options**:
- `command` - Specific command name
- `--verbose` - Extended help with examples

**When to use**:
- To discover available commands
- To learn command syntax
- To troubleshoot issues

---

### 🔧 Skill Management Commands (Future)

These commands will be available in future releases:

- `/hefesto.create` - Create skill from description
- `/hefesto.extract` - Extract skill from code
- `/hefesto.validate` - Validate skill spec compliance
- `/hefesto.adapt` - Adapt skill for different CLI
- `/hefesto.sync` - Synchronize skills across CLIs

---

## Supported AI CLIs

Hefesto supports the following AI CLIs:

1. **Claude Code** - Anthropic's Claude CLI
   - Detection: `claude` command in PATH
   - Config: `~/.claude/`
   - Skills: `.claude/skills/`

2. **Gemini CLI** - Google's Gemini CLI
   - Detection: `gemini` command in PATH
   - Config: `~/.gemini/`
   - Skills: `.gemini/skills/`

3. **OpenAI Codex** - OpenAI's Codex CLI
   - Detection: `codex` command in PATH
   - Config: `~/.codex/`
   - Skills: `.codex/skills/`

4. **VS Code/Copilot** - GitHub Copilot in VS Code
   - Detection: `code` command + Copilot extension
   - Config: `~/.vscode/` or `~/.github/`
   - Skills: `.github/skills/`

5. **OpenCode** - OpenAI's OpenCode CLI
   - Detection: `opencode` command in PATH
   - Config: `~/.opencode/`
   - Skills: `.opencode/skills/`

6. **Cursor** - Cursor AI Editor
   - Detection: `cursor` command in PATH
   - Config: `~/.cursor/`
   - Skills: `.cursor/skills/`

7. **Qwen Code** - Alibaba's Qwen Code CLI
   - Detection: `qwen` command in PATH
   - Config: `~/.qwen/`
   - Skills: `.qwen/skills/`

---

## Key Files

### Project Root
- `CONSTITUTION.md` - T0 governance rules (11 rules, immutable)
- `MEMORY.md` - Project state (CLIs, skills, metadata)
- `AGENTS.md` - AI agent bootstrap guide
- `.gitignore` - Git ignore patterns

### CLI Directories (created by init)
- `.claude/skills/` - Claude Code skills
- `.gemini/skills/` - Gemini CLI skills
- `.opencode/skills/` - OpenCode skills
- `.cursor/skills/` - Cursor skills
- (etc.)

### Command Definitions
- `commands/hefesto.init.md` - Bootstrap logic
- `commands/hefesto.detect.md` - Detection logic
- `commands/hefesto.list.md` - Listing logic
- `commands/hefesto.help.md` - This file

### Helpers
- `commands/helpers/cli-detection-strategy.md`
- `commands/helpers/constitution-validator.md`
- `commands/helpers/memory-validator.md`
- `commands/helpers/error-handling.md`
- (see `commands/helpers/` for full list)

---

## Error Codes

Common error codes and resolutions:

- **ERR-001**: Permission denied → Fix directory permissions
- **ERR-002**: Corrupted MEMORY.md → Auto-recovers, creates backup
- **ERR-003**: Missing CONSTITUTION.md → Auto-restores from bundle
- **ERR-004**: Invalid CONSTITUTION.md → Restore from backup or use `/hefesto.restore-constitution`
- **ERR-005**: No CLIs detected → Install CLI or use manual specification

See `commands/helpers/error-codes.md` for complete list.

---

## Performance Targets

| Operation | Target | Typical |
|-----------|--------|---------|
| Bootstrap (`/hefesto.init`) | < 5s | 2-4s |
| CLI detection | < 2s | 1-2s |
| State listing | < 100ms | 40-70ms |
| Filesystem sync check | < 200ms | 100-150ms |
| CONSTITUTION validation (cached) | < 5ms | 2-5ms |

---

## Constitutional Governance

Hefesto enforces **11 T0 rules** from `CONSTITUTION.md`:

1. **T0-HEFESTO-01**: Agent Skills Standard compliance
2. **T0-HEFESTO-02**: Human Gate Protocol
3. **T0-HEFESTO-03**: Progressive Disclosure (< 500 lines)
4. **T0-HEFESTO-04**: Multi-CLI Detection
5. **T0-HEFESTO-05**: Local Storage
6. **T0-HEFESTO-06**: Validation
7. **T0-HEFESTO-07**: Skill Naming (lowercase, hyphens)
8. **T0-HEFESTO-08**: Idempotency
9. **T0-HEFESTO-09**: Metadata
10. **T0-HEFESTO-10**: Cross-CLI Consistency
11. **T0-HEFESTO-11**: Security

**T0 violations BLOCK all operations** until resolved.

---

## Troubleshooting

### Common Issues

**1. "Hefesto not initialized"**
- Solution: Run `/hefesto.init`

**2. "No CLIs detected"**
- Ensure at least one AI CLI installed
- Check PATH environment variable
- Use manual specification when prompted

**3. "Permission denied creating directory"**
- Check write permissions: `ls -la .`
- Fix permissions: `chmod +w .`
- Or run with appropriate privileges

**4. "MEMORY.md corrupted"**
- System auto-recovers (creates backup)
- Review backup if needed: `MEMORY.md.backup.*`

**5. "Constitutional violation"**
- Check `CONSTITUTION.md` for modifications
- Restore: `git restore CONSTITUTION.md`
- Or force restore: `/hefesto.restore-constitution --force`

**6. "CLI detected but executable not in PATH"**
- This is a warning (non-blocking)
- Skills generated but may not work
- Install CLI properly and run `/hefesto.detect`

For more troubleshooting, see `.context/troubleshooting/foundation-issues.md`

---

## Resources

- **Specification**: https://agentskills.io (Agent Skills Standard)
- **Documentation**: `AGENTS.md` (bootstrap guide)
- **Governance**: `CONSTITUTION.md` (T0 rules)
- **State**: `MEMORY.md` (current project state)
- **Context**: `.context/` directory (AI agent context)
- **Troubleshooting**: `.context/troubleshooting/`

---

## Getting Support

1. Check this help: `/hefesto.help <command>`
2. Review troubleshooting guide
3. Check project documentation in `.context/`
4. Review `AGENTS.md` and `CONSTITUTION.md`
5. Check error codes in `commands/helpers/error-codes.md`

---

**Hefesto Skill Generator v1.0.0** | Foundation Infrastructure
```

---

## Implementation

### Display Logic

```markdown
FUNCTION execute_help_command(args):
  
  1. Parse arguments
     command_name = args.command OR null
     verbose = args.has_flag("--verbose")
  
  2. Check if Hefesto initialized
     initialized = file_exists("MEMORY.md")
  
  3. Display appropriate help
     IF command_name:
       display_command_help(command_name, verbose)
     ELIF verbose:
       display_verbose_help(initialized)
     ELSE:
       display_general_help(initialized)
```

### Command-Specific Help

```markdown
AVAILABLE_COMMANDS = {
  "init": {
    name: "/hefesto.init",
    purpose: "Initialize Hefesto in project",
    syntax: "/hefesto.init [--force] [--verbose] [--no-emoji]",
    options: [...],
    examples: [...],
    troubleshooting: [...]
  },
  "detect": {...},
  "list": {...},
  "help": {...}
}

FUNCTION display_command_help(command_name, verbose):
  IF command_name NOT IN AVAILABLE_COMMANDS:
    DISPLAY: "Unknown command: {command_name}"
    DISPLAY: "Run /hefesto.help to see available commands"
    RETURN
  
  cmd = AVAILABLE_COMMANDS[command_name]
  
  DISPLAY: "# {cmd.name} - {cmd.title}"
  DISPLAY: "\n**Purpose**: {cmd.purpose}"
  DISPLAY: "\n## Usage\n\n```\n{cmd.syntax}\n```"
  
  IF cmd.options:
    DISPLAY: "\n## Options\n"
    FOR EACH option IN cmd.options:
      DISPLAY: "- `{option.flag}` - {option.description}"
  
  IF verbose:
    DISPLAY: "\n## What It Does\n"
    FOR EACH step IN cmd.workflow:
      DISPLAY: "{step}"
    
    DISPLAY: "\n## Examples\n"
    FOR EACH example IN cmd.examples:
      DISPLAY: example
    
    DISPLAY: "\n## Troubleshooting\n"
    FOR EACH issue IN cmd.troubleshooting:
      DISPLAY: issue
```

---

## References

- **Commands**: All `/hefesto.*` command definitions
- **Error Codes**: helpers/error-codes.md
- **Troubleshooting**: .context/troubleshooting/foundation-issues.md
- **AGENTS.md**: Complete documentation
