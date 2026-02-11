# Hefesto CLI - Installation Guide

**Hefesto CLI** is a Python package that provides a command-line interface for the Hefesto Skill Generator system.

---

## Quick Install

```bash
uv tool install hefesto-cli --from git+https://github.com/KrystianYCSilva/hefesto-skill-generator.git
```

This will:
- Install `hefesto` command globally
- Make it available in your PATH
- Include all templates and slash commands

---

## Installation Options

### Option 1: Install from Git (Recommended)

```bash
# Using uv (recommended)
uv tool install hefesto-cli --from git+https://github.com/KrystianYCSilva/hefesto-skill-generator.git

# Using pipx
pipx install git+https://github.com/KrystianYCSilva/hefesto-skill-generator.git

# Using pip (global)
pip install git+https://github.com/KrystianYCSilva/hefesto-skill-generator.git
```

### Option 2: Install from Local Clone

```bash
# Clone repository
git clone https://github.com/KrystianYCSilva/hefesto-skill-generator.git
cd hefesto-skill-generator

# Install with uv
uv tool install .

# Or with pipx
pipx install .

# Or with pip
pip install .
```

### Option 3: Development Mode

For contributors or development:

```bash
git clone https://github.com/KrystianYCSilva/hefesto-skill-generator.git
cd hefesto-skill-generator

# Install in editable mode
pip install -e .
```

---

## Verify Installation

```bash
# Check version
hefesto version

# Initialize in a project
cd your-project/
hefesto init

# Check status
hefesto check
```

---

## Usage

### 1. Initialize Hefesto in Your Project

```bash
cd your-project/
hefesto init
```

This will:
- Detect installed AI CLIs (Claude Code, Gemini, Cursor, etc.)
- Create `.hefesto/` directory with templates
- Install slash commands in each detected CLI
- Create `skills/` directories

### 2. Check Installation Status

```bash
hefesto check
```

Shows:
- Installed version
- Detected CLIs
- Template files
- Command counts per CLI
- Skill counts

### 3. List Installed Skills

```bash
hefesto list
```

Displays all skills across all detected CLIs.

---

## Slash Commands (Inside AI CLIs)

After running `hefesto init`, you'll have these commands available:

| Command | Description |
|---------|-------------|
| `/hefesto.create "description"` | Create new skill from natural language |
| `/hefesto.validate skill-name` | Validate skill against quality checklist |
| `/hefesto.update skill-name` | Modify existing skill |
| `/hefesto.extract path/to/file` | Extract skill from code/docs |
| `/hefesto.agent "description"` | Generate specialized agent |
| `/hefesto.init` | Verify Hefesto installation |
| `/hefesto.list` | List all skills |

---

## Requirements

- **Python:** 3.11 or higher
- **Dependencies:** `typer`, `rich` (auto-installed)
- **Optional:** `uv` or `pipx` for isolated installs

---

## Supported AI CLIs

Hefesto auto-detects and installs to:

| CLI | Directory | Skills Path |
|-----|-----------|-------------|
| Claude Code | `.claude/` | `.claude/skills/` |
| Gemini CLI | `.gemini/` | `.gemini/skills/` |
| Codex | `.codex/` | `.codex/skills/` |
| Cursor | `.cursor/` | `.cursor/skills/` |
| OpenCode | `.opencode/` | `.opencode/skills/` |
| Qwen | `.qwen/` | `.qwen/skills/` |
| GitHub Copilot | `.github/` | `.github/skills/` |

---

## Uninstallation

```bash
# If installed with uv
uv tool uninstall hefesto-cli

# If installed with pipx
pipx uninstall hefesto-cli

# If installed with pip
pip uninstall hefesto-cli
```

---

## Troubleshooting

### Command not found

If `hefesto` is not found after installation:

1. Check if the install location is in your PATH:
   ```bash
   # For uv
   echo $PATH | grep .local/bin
   
   # For pipx
   pipx ensurepath
   ```

2. Reinstall with explicit PATH update:
   ```bash
   uv tool install hefesto-cli --from git+...
   ```

### Templates not found

If you get "templates directory not found" error:

1. Reinstall the package:
   ```bash
   uv tool uninstall hefesto-cli
   uv tool install hefesto-cli --from git+...
   ```

2. Verify templates are included:
   ```bash
   python -c "from hefesto_cli import get_templates_dir; print(get_templates_dir())"
   ```

### Permission errors

On Unix/macOS, if you get permission errors:

```bash
# Don't use sudo with uv/pipx (they manage isolation)
# If using pip globally, either:
pip install --user git+...

# Or use a virtual environment:
python -m venv venv
source venv/bin/activate
pip install git+...
```

---

## Next Steps

After installation:

1. **Initialize in project:** `hefesto init`
2. **Check status:** `hefesto check`
3. **Create first skill:** `/hefesto.create "your skill description"`
4. **List skills:** `hefesto list`

---

## Links

- [Repository](https://github.com/KrystianYCSilva/hefesto-skill-generator)
- [Agent Skills Spec](https://agentskills.io)
- [Hefesto README](README.md)

---

**Hefesto CLI** | Template-driven Agent Skill Generator | 2026
