---
description: "Logic for selecting and applying CLI adapters"
version: "1.0.0"
---

# Adapter Selector

This helper selects and applies the correct adapter based on the target CLI.

## Adapter Map

| CLI | Adapter File |
|-----|--------------|
| Claude Code | `claude.adapter.md` |
| Gemini CLI | `gemini.adapter.md` |
| OpenAI Codex | `codex.adapter.md` |
| VS Code/Copilot | `copilot.adapter.md` |
| OpenCode | `opencode.adapter.md` |
| Cursor | `cursor.adapter.md` |
| Qwen Code | `qwen.adapter.md` |
| MCP | `mcp.adapter.md` |

## Logic

```python
import os

def apply_adapter(content, target_cli, adapters_dir="commands/templates/adapters"):
    """
    Applies the adapter for the target CLI to the content.
    """
    adapter_file = f"{target_cli}.adapter.md"
    adapter_path = os.path.join(adapters_dir, adapter_file)
    
    if not os.path.exists(adapter_path):
        # Fallback or error?
        # For now, return content as is (base template)
        return content, f"Warning: Adapter for {target_cli} not found."

    # Load adapter rules (simplified parsing)
    with open(adapter_path, 'r', encoding='utf-8') as f:
        adapter_rules = f.read()
        
    # Apply substitutions defined in adapter
    # This is a basic implementation - a real one would parse the rules more robustly
    if "{{ARGUMENTS}} → $ARGUMENTS" in adapter_rules:
        content = content.replace("{{ARGUMENTS}}", "$ARGUMENTS")
    elif "{{ARGUMENTS}} → {{args}}" in adapter_rules:
        content = content.replace("{{ARGUMENTS}}", "{{args}}")
        
    # Relative Path Adjustment (FR-019)
    # If target directory structure differs, adjust paths here
    # Example: if generating to .claude/skills/name/ but referencing ../scripts/
    # Not fully implemented in this MVP helper, but placeholder logic:
    # content = adjust_relative_paths(content, target_cli)

    return content, None
```
