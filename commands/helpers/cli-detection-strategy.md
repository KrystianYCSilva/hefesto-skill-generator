---
description: "Multi-strategy approach for detecting installed AI CLI tools via PATH and config directories"
category: "helper"
type: "strategy"
used_by: ["/hefesto.init", "/hefesto.detect"]
version: "1.0.0"
---

# CLI Detection Strategy

**Purpose**: Multi-strategy approach for detecting installed AI CLI tools  
**Used by**: `/hefesto.init`, `/hefesto.detect`

---

## Supported CLIs

| CLI Name | Canonical ID | PATH Command | Config Directory |
|----------|-------------|--------------|------------------|
| Claude Code | `claude` | `claude` | `~/.claude/` |
| Gemini CLI | `gemini` | `gemini` | `~/.gemini/` |
| OpenAI Codex | `codex` | `codex` | `~/.codex/` |
| VS Code/Copilot | `copilot` | `code` (+ extension check) | `~/.vscode/` or `~/.github/` |
| OpenCode | `opencode` | `opencode` | `~/.opencode/` |
| Cursor | `cursor` | `cursor` | `~/.cursor/` |
| Qwen Code | `qwen` | `qwen` | `~/.qwen/` |

---

## Detection Order (Priority)

1. **PRIMARY**: PATH Environment Variable
   - Highest reliability (CLI actively installed and executable)
   - Use: `which {command}` (Unix) or `where.exe {command}` (Windows)
   - Status: `active` if found

2. **SECONDARY**: Config Directory Existence
   - Medium reliability (previous installation or manual config)
   - Check: `$HOME/.{cli-name}/` or `%USERPROFILE%\.{cli-name}\`
   - Status: `warning_no_path` if found but not in PATH

3. **FALLBACK**: Manual Specification
   - User prompt when no CLIs detected
   - Present list of supported CLIs
   - Status: `manual`

---

## Detection Algorithm

### Phase 1: PATH Scanning (Parallel)

```markdown
FOR EACH cli IN supported_clis:
  PARALLEL:
    IF platform = Windows:
      result = Execute("where.exe {cli.path_command}")
    ELSE:
      result = Execute("which {cli.path_command}")
    
    IF result.exit_code = 0:
      version = TryGetVersion(cli.path_command)
      RECORD(cli.canonical_id, "PATH", result.path, version, "active")
```

**Performance**: All 7 CLIs checked in parallel → ~300-500ms total

### Phase 2: Config Directory Scanning (Parallel)

```markdown
FOR EACH cli IN (supported_clis WHERE NOT detected_via_path):
  PARALLEL:
    config_path = GetConfigPath(cli.canonical_id)
    
    IF filesystem.exists(config_path):
      RECORD(cli.canonical_id, "config_directory", config_path, null, "warning_no_path")
      WARN("CLI '{cli.canonical_id}' config found but executable not in PATH")
```

**Performance**: Fast directory existence checks → ~100-200ms total

### Phase 3: Manual Fallback (Sequential)

```markdown
IF COUNT(detected_clis) = 0:
  PROMPT user:
    "No AI CLIs detected automatically. Which CLI do you use?"
    OPTIONS: [Claude Code, Gemini CLI, OpenAI Codex, ...]
    
  FOR EACH selected_cli:
    RECORD(selected_cli, "manual", ".{selected_cli}/skills/", null, "manual")
```

---

## Platform-Specific Commands

### Windows (PowerShell)

```powershell
# PATH check
$result = where.exe claude 2>$null
if ($LASTEXITCODE -eq 0) { Write-Output "FOUND: $result" }

# Config directory check
$configPath = "$env:USERPROFILE\.claude"
if (Test-Path $configPath) { Write-Output "CONFIG_FOUND: $configPath" }

# Version detection
$version = claude --version 2>$null | Select-String -Pattern '\d+\.\d+\.\d+' | ForEach-Object { $_.Matches.Value }
```

### Unix/Linux (Bash)

```bash
# PATH check
if command -v claude &> /dev/null; then
  path=$(which claude)
  echo "FOUND: $path"
fi

# Config directory check
if [ -d "$HOME/.claude" ]; then
  echo "CONFIG_FOUND: $HOME/.claude"
fi

# Version detection
version=$(claude --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
```

### macOS (Zsh/Bash)

```zsh
# Same as Unix/Linux, with special case for Homebrew installations
if command -v claude &> /dev/null; then
  path=$(which claude)
  echo "FOUND: $path"
elif [ -f "/opt/homebrew/bin/claude" ]; then
  echo "FOUND: /opt/homebrew/bin/claude (Homebrew)"
fi
```

---

## Version Detection

### Strategies by CLI

| CLI | Version Command | Parse Pattern |
|-----|----------------|---------------|
| Claude Code | `claude --version` | `\d+\.\d+\.\d+` |
| Gemini CLI | `gemini --version` | `\d+\.\d+\.\d+` |
| OpenAI Codex | `codex --version` | `\d+\.\d+\.\d+` |
| VS Code/Copilot | `code --version` | First line (VS Code version) |
| OpenCode | `opencode --version` | `\d+\.\d+\.\d+` |
| Cursor | `cursor --version` | `\d+\.\d+\.\d+` |
| Qwen Code | `qwen --version` | `\d+\.\d+\.\d+` |

**Note**: Version detection is best-effort. If detection fails, record `null` and continue (non-blocking).

---

## Special Cases

### VS Code/Copilot Detection

```markdown
1. Check for `code` command in PATH
2. If found, verify Copilot extension:
   a. Execute: `code --list-extensions | grep copilot`
   b. If Copilot found → record as "copilot"
   c. If not found → skip (VS Code without Copilot not supported)
```

### Cursor Detection

```markdown
Cursor often installs in non-standard locations:
- Windows: `%LOCALAPPDATA%\Programs\cursor\`
- macOS: `/Applications/Cursor.app/Contents/MacOS/cursor`
- Linux: `~/.local/share/cursor/`

CHECK these paths in addition to PATH scanning
```

---

## Error Handling

### Permission Errors

```markdown
IF execute(command) returns PermissionError:
  LOG("Permission denied checking {cli}")
  CONTINUE to next CLI
  
IF create_directory(skills_dir) returns PermissionError:
  RECORD(cli, detection_method, skills_dir, version, "error_permission")
  ADD to error report
  CONTINUE to next CLI
```

### Timeout Handling

```markdown
SET timeout = 5 seconds per CLI command
IF command exceeds timeout:
  LOG("Timeout checking {cli}")
  CONTINUE to next CLI
```

### Network Dependency

```markdown
CRITICAL: Detection MUST work offline
- No network calls to check versions
- No API requests to verify CLI status
- All checks based on local filesystem and PATH
```

---

## Detection Report Format

### Successful Detection

```markdown
## CLI Detection Summary

✅ Detected 5 AI CLIs

### Active (in PATH)
- Claude Code v1.2.0 → .claude/skills/
- OpenAI Codex v2.1.0 → .codex/skills/
- OpenCode v0.2.1 → .opencode/skills/

### Warnings
- Gemini CLI → .gemini/skills/ ⚠️ Config found but not in PATH

### Errors
- VS Code/Copilot: Permission denied creating .github/skills/
  Fix: Run with appropriate permissions

**Next Steps**: Run `/hefesto.list` to verify initialization
```

### No CLIs Detected

```markdown
## CLI Detection Summary

⚠️ No AI CLIs detected automatically

### Manual Specification Required

Which AI CLI do you use?
1. Claude Code
2. Gemini CLI
3. OpenAI Codex
4. VS Code/Copilot
5. OpenCode
6. Cursor
7. Qwen Code

Enter numbers (comma-separated): _
```

---

## Performance Targets

| Phase | Target | Strategy |
|-------|--------|----------|
| PATH scanning (7 CLIs) | < 500ms | Parallel execution |
| Config scanning (remaining) | < 200ms | Parallel directory checks |
| Version detection | < 1s | Parallel, timeout after 5s |
| **Total Detection** | **< 2s** | Combined parallel operations |

---

## References

- Research: CLI Detection Methodology (research.md #1)
- Contract: `/detect` operation (contracts/cli-detection.schema.yaml)
- FR-001: Automatic detection via PATH and config directories
- FR-006: Detection order for 7 CLIs
- FR-012: Detection report showing method and warnings
- FR-013: Manual specification fallback
- T0-HEFESTO-04: Multi-CLI automatic detection
