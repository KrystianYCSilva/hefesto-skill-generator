"""
Hefesto Skill Generator - Shared Library Modules

This package contains shared utilities for the Human Gate + Wizard Mode feature.

Modules:
- audit: Operation logging and audit trail
- sanitizer: Input sanitization and security validation
- colors: ANSI color utilities for terminal output
- timeout: Cross-platform timeout wrappers
- preview: Preview generation and formatting
- atomic: Atomic file operations with rollback
- human_gate: Human Gate approval workflow
- wizard: Wizard Mode for guided skill creation
- expansion: JIT resource expansion
- collision: Collision detection and resolution
- backup: Skill backup creation
- diff: Markdown section diffing
- editor: External editor integration
"""

__version__ = "1.0.0"
__all__ = [
    "audit",
    "sanitizer",
    "colors",
    "timeout",
    "preview",
    "atomic",
    "human_gate",
    "wizard",
    "expansion",
    "collision",
    "backup",
    "diff",
    "editor",
]
