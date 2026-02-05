# CLI Detector Helper

**Purpose**: Detect installed AI CLIs via PATH and config directory scanning  
**Contract**: [cli-detector.md](../../specs/004-multi-cli-generator/contracts/cli-detector.md)  
**Feature**: 004-multi-cli-generator

---

## Overview

The CLI Detector discovers installed AI CLIs using two methods:
1. **PATH Scanning**: Check system PATH for CLI executables
2. **Config Directory Detection**: Check for `.{cli}/` directories in project root

Results are merged with priority-based conflict resolution.

**Performance Target**: <500ms for 7 CLIs

---

## Supported CLIs

| Priority | CLI Name | Executable | Config Dir | Variable Syntax |
|----------|----------|------------|------------|-----------------|
| 1 | Claude Code | `claude` | `.claude/` | `$ARGUMENTS` |
| 2 | Gemini CLI | `gemini` | `.gemini/` | `{{args}}` |
| 3 | OpenAI Codex | `codex` | `.codex/` | `$ARGUMENTS` |
| 4 | VS Code/Copilot | `code` | `.github/` | `$ARGUMENTS` |
| 5 | OpenCode | `opencode` | `.opencode/` | `$ARGUMENTS` |
| 6 | Cursor | `cursor` | `.cursor/` | `$ARGUMENTS` |
| 7 | Qwen Code | `qwen` | `.qwen/` | `{{args}}` |

---

## Operations

### `detect_all_clis(config: DetectionConfig) -> DetectionReport`

**Description**: Detect all supported CLIs using configured detection methods.

**Algorithm**:
```
1. Initialize empty results list
2. Launch parallel detection:
   a. PATH detection (async if enabled)
   b. Config directory check (async if enabled)
   c. Version extraction (async if enabled)
3. Wait for all async operations (max timeout_ms)
4. Merge results:
   - Both found: status=detected, method=both
   - PATH only: status=detected, method=path
   - Config only: status=detected_config_only, method=config_dir
   - Neither: status=not_found
   - Error: status=error, capture error_message
5. Construct Detection Report
6. Return Detection Report
```

**Implementation** (Bash/PowerShell):
```bash
# Bash (Unix/Linux/macOS)
detect_all_clis() {
  local -a detected_clis=()
  local timeout_ms=${1:-500}
  
  # PATH detection (parallel)
  for cli in claude gemini codex code opencode cursor qwen; do
    (
      if command -v "$cli" &>/dev/null; then
        path=$(which "$cli" 2>/dev/null)
        version=$(timeout 0.2s "$cli" --version 2>/dev/null || echo "unknown")
        echo "$cli|path|$path|$version"
      fi
    ) &
  done
  
  # Config directory detection (parallel)
  for config_dir in .claude .gemini .codex .github .opencode .cursor .qwen; do
    (
      if [ -d "$config_dir" ]; then
        cli_name="${config_dir#.}"
        [ "$cli_name" = "github" ] && cli_name="copilot"
        echo "$cli_name|config|$config_dir|null"
      fi
    ) &
  done
  
  # Wait for all background jobs
  wait
  
  # Merge results (omitted for brevity - see contract)
}
```

```powershell
# PowerShell (Windows)
function Detect-AllCLIs {
    param(
        [int]$TimeoutMs = 500
    )
    
    $detectedCLIs = @()
    $jobs = @()
    
    # PATH detection (parallel jobs)
    $clis = @('claude', 'gemini', 'codex', 'code', 'opencode', 'cursor', 'qwen')
    foreach ($cli in $clis) {
        $jobs += Start-Job -ScriptBlock {
            param($cliName)
            $path = (Get-Command $cliName -ErrorAction SilentlyContinue).Source
            if ($path) {
                $version = & $cliName --version 2>$null
                [PSCustomObject]@{
                    CLI = $cliName
                    Method = 'path'
                    Path = $path
                    Version = $version
                }
            }
        } -ArgumentList $cli
    }
    
    # Config directory detection (parallel jobs)
    $configDirs = @('.claude', '.gemini', '.codex', '.github', '.opencode', '.cursor', '.qwen')
    foreach ($dir in $configDirs) {
        $jobs += Start-Job -ScriptBlock {
            param($configDir)
            if (Test-Path $configDir -PathType Container) {
                $cliName = $configDir.TrimStart('.')
                if ($cliName -eq 'github') { $cliName = 'copilot' }
                [PSCustomObject]@{
                    CLI = $cliName
                    Method = 'config'
                    Path = $configDir
                    Version = $null
                }
            }
        } -ArgumentList $dir
    }
    
    # Wait for all jobs
    $results = $jobs | Wait-Job | Receive-Job
    
    # Merge results (omitted for brevity - see contract)
}
```

---

### `check_path(cli_name: string) -> PathCheckResult`

**Description**: Check if CLI executable exists in system PATH.

**Algorithm**:
```
# Unix/Linux/macOS
1. Execute: which {cli_name}
2. If exit code 0: return { found: true, path: stdout }
3. If exit code != 0: return { found: false, path: null }

# Windows
1. Execute: where.exe {cli_name}.exe
2. If exit code 0: return { found: true, path: stdout }
3. If exit code != 0: return { found: false, path: null }
```

**Timeout**: 100ms per CLI

---

### `check_config_directory(cli_name: string) -> ConfigDirCheckResult`

**Description**: Check if CLI config directory exists in project root.

**Config Directory Mapping**:
- `claude` → `.claude/`
- `gemini` → `.gemini/`
- `codex` → `.codex/`
- `copilot` → `.github/`
- `opencode` → `.opencode/`
- `cursor` → `.cursor/`
- `qwen` → `.qwen/`

**Algorithm**:
```
1. Construct config directory path: ./{config_dir_name}/
2. Check if directory exists using filesystem API
3. Return { exists: boolean, path: string }
```

**Performance**: <10ms per CLI

---

### `extract_version(executable_path: string, cli_name: string) -> VersionExtractionResult`

**Description**: Extract version information from CLI executable.

**Algorithm**:
```
1. Try: {executable_path} --version (timeout 200ms)
2. If exit code 0: parse stdout for version string
3. If failed, try: {executable_path} -v (timeout 200ms)
4. If failed, try: {executable_path} version (timeout 200ms)
5. If all fail: return { success: false, version: "unknown" }
```

**Return Type**:
```yaml
success: boolean
version: string | null
error: string | null
```

**Note**: Failure is acceptable - version becomes "unknown"

---

### `persist_detection_results(report: DetectionReport) -> void`

**Description**: Save detection results to MEMORY.md.

**Format**:
```markdown
## CLIs Detectados

| CLI | Método | Status | Versão | Skills Dir | Skills |
|-----|--------|--------|--------|------------|--------|
| **Claude Code** | PATH + Config | ✅ active | 2.1.31 | .claude/skills/ | java-fundamentals |
| **Gemini CLI** | PATH + Config | ✅ active | 0.27.0 | .gemini/skills/ | java-fundamentals |
...

**Última detecção**: 2026-02-04 (hefesto.init re-scan)
**Total AI CLIs**: 7 (6 active, 1 warning_no_path)
```

**Algorithm**:
```
1. Load existing MEMORY.md
2. Find "## CLIs Detectados" section
3. Replace with new detection table
4. Update "Última detecção" timestamp
5. Write back to MEMORY.md
```

---

### `load_cached_detection() -> DetectionReport | null`

**Description**: Load previously cached detection results from MEMORY.md.

**Algorithm**:
```
1. Parse MEMORY.md
2. Extract "## CLIs Detectados" section
3. Parse table rows into CLIDetectionResult objects
4. Construct DetectionReport
5. Return report or null if not found
```

**Cache Invalidation**: Manual only - user runs `/hefesto.detect` to refresh

---

## Detection Config

### Default Config

```yaml
detection_config:
  check_path: true
  check_config_dirs: true
  timeout_ms: 500
  version_extraction: true
  target_clis: null  # All 7 CLIs
```

### Minimal Config (Fast)

```yaml
detection_config:
  check_path: true
  check_config_dirs: true
  timeout_ms: 300
  version_extraction: false  # Skip version extraction for speed
  target_clis: null
```

### Single CLI Config

```yaml
detection_config:
  check_path: true
  check_config_dirs: true
  timeout_ms: 100
  version_extraction: true
  target_clis: ["claude"]  # Only detect Claude
```

---

## Error Handling

| Scenario | Response | Status Code |
|----------|----------|-------------|
| Timeout exceeded | Return partial results with error for timed-out CLIs | Partial success |
| Permission denied | Mark CLI as error, continue with others | Partial success |
| Invalid CLI name | Return error immediately | Fail fast |
| No CLIs detected | Return empty report, trigger fallback mode | Success (empty) |
| Shell execution failed | Mark affected CLIs as error | Partial success |

---

## Cross-Platform Considerations

### Unix/Linux/macOS
- Use `which` command for PATH detection
- Executable: `{cli_name}` (no .exe extension)
- Shell: bash or zsh

### Windows
- Use `where.exe` command for PATH detection
- Executable: `{cli_name}.exe` (with extension)
- Shell: PowerShell

### Path Separators
- Use forward slashes in templates
- CLI runtime handles conversion

---

## Performance

| Operation | Target | Typical |
|-----------|--------|---------|
| PATH scan (7 CLIs parallel) | <300ms | 200-250ms |
| Config directory scan (7 dirs) | <50ms | 20-30ms |
| Version extraction (per CLI) | <200ms | 100-150ms |
| Merge results | <50ms | 20-30ms |
| **Total Detection** | **<500ms** | **300-400ms** |

---

## Usage Example

```bash
# Bash usage
source commands/helpers/cli-detector.md

# Detect all CLIs
detection_report=$(detect_all_clis 500)
echo "$detection_report"

# Check specific CLI
path_result=$(check_path "claude")
echo "$path_result"

# Check config directory
config_result=$(check_config_directory "claude")
echo "$config_result"
```

---

## Related Files

- **Contract**: [cli-detector.md](../../specs/004-multi-cli-generator/contracts/cli-detector.md)
- **Data Model**: [data-model.md](../../specs/004-multi-cli-generator/data-model.md) §1
- **Commands**: `hefesto.detect.md`, `hefesto.create.md`
- **Templates**: `detection-report.md`

---

**Version**: 1.0.0 | **Date**: 2026-02-05 | **Feature**: 004-multi-cli-generator
