# Detection Report Template

**Purpose**: Template for CLI detection output  
**Feature**: 004-multi-cli-generator

---

## Template

```markdown
## CLI Detection Report

**Operation**: {operation}  
**Date**: {timestamp}  
**Duration**: {duration}s

---

### Summary

{total_detected} out of {total_supported} supported CLIs detected

---

### Detected CLIs ({detected_count})

{FOR EACH detected_cli}
- **{cli.display_name}** (v{cli.version})
  - Detection: {cli.detection_method}
  - Skills Directory: {cli.skills_directory}
  - Status: {cli.status_icon} {cli.status}
{END FOR}

{IF detected_count == 0}
No CLIs detected
{END IF}

---

### Config-Only CLIs ({config_only_count})

{FOR EACH config_only_cli}
- **{cli.display_name}**
  - Config Location: {cli.config_path}
  - ⚠️ Executable not in PATH
  - Fix: Install {cli.display_name} and ensure it's in PATH
{END FOR}

{IF config_only_count == 0}
None
{END IF}

---

### Not Found ({not_found_count})

{FOR EACH not_found_cli}
- {cli.display_name}
{END FOR}

{IF not_found_count == total_supported}
No AI CLIs detected. Install at least one supported CLI to continue.
{END IF}

---

### Warnings ({warning_count})

{FOR EACH warning}
- {warning_message}
{END FOR}

{IF warning_count == 0}
None
{END IF}

---

### Errors ({error_count})

{FOR EACH error}
- **{error.cli_name}**: {error.type}
  Details: {error.message}
  Fix: {error.fix_instructions}
{END FOR}

{IF error_count == 0}
None
{END IF}

---

{IF error_count > 0}
⚠️ Detection completed with {error_count} error(s)
{ELSE IF warning_count > 0}
✅ Detection completed with {warning_count} warning(s)
{ELSE}
✅ Detection completed successfully
{END IF}
```

---

## Variables

| Variable | Type | Description |
|----------|------|-------------|
| `operation` | string | "detect" or "re-detect" |
| `timestamp` | datetime | ISO 8601 timestamp |
| `duration` | float | Time in seconds |
| `total_supported` | integer | Total CLIs checked (always 7) |
| `total_detected` | integer | CLIs with status=detected |
| `detected_count` | integer | Count of detected CLIs |
| `config_only_count` | integer | Count of config-only CLIs |
| `not_found_count` | integer | Count of not found CLIs |
| `warning_count` | integer | Number of warnings |
| `error_count` | integer | Number of errors |

---

## Status Icons

| Status | Icon | Description |
|--------|------|-------------|
| detected | ✅ | Fully detected |
| detected_config_only | ⚠️ | Config found, no executable |
| not_found | ❌ | Not detected |
| error | ❌ | Detection error |

---

## Example Output

```markdown
## CLI Detection Report

**Operation**: detect  
**Date**: 2026-02-05T10:30:00Z  
**Duration**: 0.42s

---

### Summary

3 out of 7 supported CLIs detected

---

### Detected CLIs (3)

- **Claude Code** (v2.1.31)
  - Detection: path + config
  - Skills Directory: .claude/skills/
  - Status: ✅ active

- **Gemini CLI** (v0.27.0)
  - Detection: path + config
  - Skills Directory: .gemini/skills/
  - Status: ✅ active

- **OpenCode** (v1.1.48)
  - Detection: path + config
  - Skills Directory: .opencode/skills/
  - Status: ✅ active

---

### Config-Only CLIs (1)

- **VS Code/Copilot**
  - Config Location: .github/
  - ⚠️ Executable not in PATH
  - Fix: Install VS Code with Copilot extension

---

### Not Found (3)

- OpenAI Codex
- Cursor
- Qwen Code

---

### Warnings (1)

- VS Code/Copilot: Config directory found but executable not in PATH. Skills may not work until CLI is installed.

---

### Errors (0)

None

---

✅ Detection completed with 1 warning(s)
```

---

## Related Files

- **Helpers**: `cli-detector.md`
- **Data Model**: [data-model.md](../../specs/004-multi-cli-generator/data-model.md) §4
- **Commands**: `hefesto.detect.md`

---

**Version**: 1.0.0 | **Date**: 2026-02-05 | **Feature**: 004-multi-cli-generator
