# Contract: CLI Detector

**Feature**: 004-multi-cli-generator  
**Component**: CLI Detection System  
**Type**: Interface Definition

---

## Purpose

The CLI Detector is responsible for discovering installed AI CLIs using both PATH scanning and config directory detection, then merging results into a Detection Report.

---

## Interface

### Input

```yaml
detection_config:
  check_path: boolean           # Whether to scan system PATH (default: true)
  check_config_dirs: boolean    # Whether to check config directories (default: true)
  timeout_ms: integer           # Max time for detection (default: 500)
  version_extraction: boolean   # Whether to extract versions (default: true)
  target_clis: list | null      # Specific CLIs to detect, or null for all 7
```

### Output

```yaml
detection_report:
  detection_timestamp: datetime
  total_supported: integer
  total_detected: integer
  total_config_only: integer
  clis: list[CLIDetectionResult]
```

**Output Type**: Detection Report (see data-model.md §4)

---

## Operations

### `detect_all_clis(config: DetectionConfig) -> DetectionReport`

**Description**: Detects all supported CLIs using configured detection methods.

**Algorithm**:
```
1. Initialize empty results list
2. For each supported CLI (claude, gemini, codex, copilot, opencode, cursor, qwen):
   a. Launch PATH detection (async if check_path=true)
   b. Launch config directory check (async if check_config_dirs=true)
   c. If version_extraction=true, launch version check (async)
3. Wait for all async operations (max timeout_ms)
4. For each CLI, merge PATH + config + version results:
   - Both found: status=detected, method=both
   - PATH only: status=detected, method=path
   - Config only: status=detected_config_only, method=config_dir
   - Neither: status=not_found
   - Error: status=error, capture error_message
5. Construct Detection Report with aggregated results
6. Return Detection Report
```

**Performance Target**: Complete within 500ms for 7 CLIs

**Error Handling**: Non-blocking - errors for individual CLIs don't fail entire detection

---

### `detect_specific_cli(cli_name: string, config: DetectionConfig) -> CLIDetectionResult`

**Description**: Detects a single CLI by name.

**Algorithm**:
```
1. Validate cli_name against supported CLI list
2. Execute PATH detection (if enabled)
3. Execute config directory check (if enabled)
4. Execute version extraction (if enabled)
5. Merge results into single CLIDetectionResult
6. Return CLIDetectionResult
```

**Performance Target**: Complete within 100ms for single CLI

**Error Handling**: Returns CLIDetectionResult with status=error if detection fails

---

### `check_path(cli_name: string) -> PathCheckResult`

**Description**: Checks if CLI executable exists in system PATH.

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

**Return Type**:
```yaml
found: boolean
path: string | null
```

**Timeout**: 100ms per CLI

---

### `check_config_directory(cli_name: string) -> ConfigDirCheckResult`

**Description**: Checks if CLI config directory exists in project root.

**Algorithm**:
```
1. Construct config directory path: ./{config_dir_name}/
   - claude → .claude/
   - gemini → .gemini/
   - codex → .codex/
   - copilot → .github/
   - opencode → .opencode/
   - cursor → .cursor/
   - qwen → .qwen/
2. Check if directory exists using filesystem API
3. Return { exists: boolean, path: string }
```

**Return Type**:
```yaml
exists: boolean
path: string
```

**Performance**: Filesystem check, <10ms

---

### `extract_version(executable_path: string, cli_name: string) -> VersionExtractionResult`

**Description**: Extracts version information from CLI executable.

**Algorithm**:
```
1. Try: {executable_path} --version
2. If exit code 0: parse stdout for version string, return { success: true, version: string }
3. If failed, try: {executable_path} -v
4. If exit code 0: parse stdout for version string, return { success: true, version: string }
5. If failed, try: {executable_path} version
6. If exit code 0: parse stdout for version string, return { success: true, version: string }
7. If all fail: return { success: false, version: null, error: string }
```

**Return Type**:
```yaml
success: boolean
version: string | null
error: string | null
```

**Timeout**: 200ms per CLI

**Error Handling**: Failure is acceptable - version becomes "unknown"

---

## Dependencies

### External
- Shell execution capability (bash, PowerShell, or equivalent)
- Filesystem access (read permissions for project root)
- System PATH access

### Internal
- CLI priority matrix (for conflict resolution)
- Config directory name mapping

---

## Persistence

### MEMORY.md Integration

**Write Operation**: `persist_detection_results(report: DetectionReport) -> void`

**Format**:
```markdown
## Detected CLIs

last_detection: {timestamp}

clis:
  - name: {cli_name}
    status: {status}
    version: {version}
    path: {executable_path}
    config_dir: {config_directory}
    method: {detection_method}
```

**Read Operation**: `load_cached_detection() -> DetectionReport | null`

**Cache Invalidation**: Manual only - user runs `/hefesto.detect` to refresh

---

## Error Scenarios

| Scenario | Response | Status Code |
|----------|----------|-------------|
| Timeout exceeded | Return partial results with error for timed-out CLIs | Partial success |
| Permission denied | Mark CLI as error, continue with others | Partial success |
| Invalid CLI name | Return error immediately | Fail fast |
| No CLIs detected | Return empty report, trigger fallback mode | Success (empty) |
| Shell execution failed | Mark affected CLIs as error | Partial success |

---

## Testing Contract

### Manual Test Cases

1. **All CLIs Detected**
   - **Setup**: Install all 7 CLIs, add to PATH, create config dirs
   - **Expected**: total_detected=7, all status=detected, method=both

2. **Partial Detection (PATH only)**
   - **Setup**: 3 CLIs in PATH, no config dirs
   - **Expected**: total_detected=3, status=detected, method=path

3. **Partial Detection (Config only)**
   - **Setup**: Create config dirs, no PATH executables
   - **Expected**: total_config_only=7, status=detected_config_only, method=config_dir

4. **No CLIs Detected**
   - **Setup**: Clean system, no CLIs or config dirs
   - **Expected**: total_detected=0, total_config_only=0, all status=not_found

5. **Version Extraction Failure**
   - **Setup**: CLI in PATH but --version flag broken
   - **Expected**: status=detected, version=null or "unknown"

6. **Performance Under 500ms**
   - **Setup**: All 7 CLIs installed
   - **Measure**: detection_timestamp to report completion
   - **Expected**: <500ms elapsed time

7. **Permission Error Handling**
   - **Setup**: CLI executable without execute permissions
   - **Expected**: status=error, error_message describes permission issue

---

## Configuration Reference

### Default Detection Config

```yaml
detection_config:
  check_path: true
  check_config_dirs: true
  timeout_ms: 500
  version_extraction: true
  target_clis: null  # All 7 CLIs
```

### Minimal Detection Config (Fast)

```yaml
detection_config:
  check_path: true
  check_config_dirs: true
  timeout_ms: 300
  version_extraction: false  # Skip version extraction for speed
  target_clis: null
```

### Single CLI Detection Config

```yaml
detection_config:
  check_path: true
  check_config_dirs: true
  timeout_ms: 100
  version_extraction: true
  target_clis: ["claude"]  # Only detect Claude
```

---

## Implementation Notes

### Cross-Platform Considerations

**Unix/Linux/macOS**:
- Use `which` command for PATH detection
- Executable: `{cli_name}` (no .exe extension)
- Shell: bash or zsh

**Windows**:
- Use `where.exe` command for PATH detection
- Executable: `{cli_name}.exe` (with extension)
- Shell: PowerShell

**Path Separators**: Use forward slashes in templates, CLI runtime handles conversion

---

## Related Contracts

- [CLI Adapter](./cli-adapter.md) - Uses detection results to select appropriate adapter
- [Parallel Generator](./parallel-generator.md) - Consumes detection report to determine targets
- [Rollback Handler](./rollback-handler.md) - N/A (detection doesn't modify filesystem)

---

**Contract Version**: 1.0.0 | **Status**: Draft | **Date**: 2026-02-04
