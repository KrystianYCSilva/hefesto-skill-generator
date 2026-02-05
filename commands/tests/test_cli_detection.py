#!/usr/bin/env python3
"""Test script to verify CLI detection functionality"""

import sys
from pathlib import Path
import re

def detect_installed_clis():
    """Detect installed CLIs from MEMORY.md or system"""
    memory_path = Path("MEMORY.md")
    if not memory_path.exists():
        return []

    content = memory_path.read_text(encoding='utf-8')
    # Look for CLIs in the "CLIs Detectados" section
    detected_clis = []

    # Look for the CLIs Detectados section
    lines = content.split('\n')

    for line in lines:
        # Look for lines that contain CLI names and detection status
        # Match patterns like: "| **OpenCode** | ✅ Detectado |" or "| **Qwen Code** | ✅ Detectado |"
        match = re.search(r'\|\s*\*\*(.*?)\*\*\s*\|\s*✅', line)
        if match:
            cli_full_name = match.group(1).lower()
            
            # Map full names to canonical IDs
            if "claude" in cli_full_name:
                detected_clis.append("claude")
            elif "gemini" in cli_full_name:
                detected_clis.append("gemini")
            elif "codex" in cli_full_name:
                detected_clis.append("codex")
            elif "copilot" in cli_full_name:
                detected_clis.append("copilot")
            elif "opencode" in cli_full_name:
                detected_clis.append("opencode")
            elif "cursor" in cli_full_name:
                detected_clis.append("cursor")
            elif "qwen" in cli_full_name:
                detected_clis.append("qwen")

    # Remove duplicates and return
    return list(set(detected_clis))

if __name__ == "__main__":
    print("Testing CLI detection...")
    detected = detect_installed_clis()
    print(f"Detected CLIs: {detected}")
    
    # Also print raw MEMORY.md content around the CLIs section for debugging
    with open("MEMORY.md", "r", encoding="utf-8") as f:
        content = f.read()
        
    # Find the CLIs Detectados section
    start_idx = content.find("## CLIs Detectados")
    if start_idx != -1:
        # Get the section (next 20 lines)
        lines = content[start_idx:].split('\n')[:20]
        print("\nContent around CLIs Detectados section:")
        for i, line in enumerate(lines):
            # Replace Unicode characters to prevent encoding errors
            safe_line = line.encode('ascii', errors='replace').decode('ascii')
            print(f"{i}: {safe_line}")