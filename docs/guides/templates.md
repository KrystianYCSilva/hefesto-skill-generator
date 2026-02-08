# Using Templates

## Overview

Hefesto uses 3 Markdown templates as source of truth for skill generation and validation.

## Templates

| Template | Location | Purpose |
|----------|----------|---------|
| `skill-template.md` | `templates/` | Canonical skill structure (frontmatter + body) |
| `quality-checklist.md` | `templates/` | 13-point auto-critica checklist |
| `cli-compatibility.md` | `templates/` | Multi-CLI directory map and adaptations |

After installation, templates are also available in `.hefesto/templates/` within the user's project.

## CLI Adaptations

| CLI | Format | Variable Syntax |
|-----|--------|-----------------|
| Claude/Codex/OpenCode/Cursor | `.md` with YAML frontmatter | `$ARGUMENTS` |
| Gemini | `.toml` with `description` + `prompt` | `{{args}}` |
| Qwen | `.md` with YAML frontmatter | `{{args}}` |
| Copilot | `.md` in `.github/` namespace | `$ARGUMENTS` |

See `templates/cli-compatibility.md` for the full compatibility matrix.
