"""
Hefesto Skill Generator - Preview Module

Preview generation and formatting for Human Gate display (FR-003).
"""

import sys
import yaml
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

from .colors import Colors, colorize, bold, green, blue, cyan, yellow, gray


@dataclass
class ResourceInfo:
    """JIT resource metadata"""

    resource_type: str  # 'scripts' | 'references' | 'assets'
    filename: str
    content: str | None
    path: Path | None
    size: int


@dataclass
class PreviewObject:
    """
    Represents in-memory skill before persistence.

    Attributes match contract specification in contracts/preview.md
    """

    skill_name: str
    skill_content: str
    metadata_content: str
    target_clis: List[str]
    validation_status: str  # 'valid' | 'invalid'
    validation_errors: List[str]
    file_paths: Dict[str, List[Path]]
    file_sizes: Dict[str, int]
    timestamp: str
    resources: List[ResourceInfo] = field(default_factory=list)

    def total_size(self) -> int:
        """Calculate total size across all files"""
        return sum(self.file_sizes.values())

    def total_files(self) -> int:
        """Count total files to be created"""
        return sum(len(paths) for paths in self.file_paths.values())


def _extract_skill_name(skill_content: str) -> str:
    """
    Extract skill name from frontmatter.

    Args:
        skill_content: Full SKILL.md content with frontmatter

    Returns:
        Skill name

    Raises:
        ValueError: If frontmatter is invalid or name missing
    """
    if not skill_content.startswith("---"):
        raise ValueError("Missing frontmatter start '---'")

    parts = skill_content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Invalid frontmatter format")

    frontmatter_yaml = parts[1]

    try:
        data = yaml.safe_load(frontmatter_yaml)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML frontmatter: {e}")

    if "name" not in data:
        raise ValueError("Missing required field 'name' in frontmatter")

    return data["name"]


def calculate_file_size(content: str) -> int:
    """
    Calculate file size in bytes.

    Args:
        content: File content

    Returns:
        Size in bytes
    """
    return len(content.encode("utf-8"))


def format_file_size(size_bytes: int) -> str:
    """
    Format file size for human-readable display.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted string (e.g., "1.2 KB", "345 bytes")
    """
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def truncate_content(content: str, max_lines: int = 50) -> Tuple[str, int, bool]:
    """
    Truncate skill content to first N lines (FR-003 clarification).

    Args:
        content: Full skill content
        max_lines: Maximum lines to display (default: 50)

    Returns:
        Tuple of (truncated_content, total_lines, was_truncated)
    """
    lines = content.split("\n")
    total_lines = len(lines)

    if total_lines <= max_lines:
        return content, total_lines, False

    truncated = "\n".join(lines[:max_lines])
    return truncated, total_lines, True


def create_preview(
    skill_content: str,
    metadata: str,
    target_clis: List[str],
    validation_errors: List[str] = None,
) -> PreviewObject:
    """
    Create PreviewObject from validated skill content.

    Args:
        skill_content: Complete SKILL.md content (with frontmatter)
        metadata: metadata.yaml content
        target_clis: Target CLI identifiers
        validation_errors: Validation errors (empty list if valid)

    Returns:
        PreviewObject ready for Human Gate display
    """
    if validation_errors is None:
        validation_errors = []

    # Extract skill name
    skill_name = _extract_skill_name(skill_content)

    # Calculate file sizes
    skill_size = calculate_file_size(skill_content)
    metadata_size = calculate_file_size(metadata)

    # Generate file paths and sizes
    file_paths = {}
    file_sizes = {}

    for cli in target_clis:
        skill_path = Path(f".{cli}/skills/{skill_name}/SKILL.md")
        metadata_path = Path(f".{cli}/skills/{skill_name}/metadata.yaml")

        file_paths[cli] = [skill_path, metadata_path]
        file_sizes[str(skill_path)] = skill_size
        file_sizes[str(metadata_path)] = metadata_size

    # Determine validation status
    validation_status = "invalid" if validation_errors else "valid"

    # Create preview object
    return PreviewObject(
        skill_name=skill_name,
        skill_content=skill_content,
        metadata_content=metadata,
        target_clis=target_clis,
        validation_status=validation_status,
        validation_errors=validation_errors,
        file_paths=file_paths,
        file_sizes=file_sizes,
        timestamp=datetime.now().isoformat(),
        resources=[],
    )


def format_preview(preview: PreviewObject) -> str:
    """
    Format preview for terminal display with ANSI colors (FR-003).

    Args:
        preview: PreviewObject to format

    Returns:
        Formatted string ready for terminal output
    """
    c = Colors
    lines = []

    # Header
    lines.append(bold(cyan("=" * 60)))
    lines.append(bold(f"HUMAN GATE: Skill Preview - {preview.skill_name}"))
    lines.append(cyan("=" * 60))
    lines.append("")

    # Validation status
    if preview.validation_status == "valid":
        lines.append(colorize("✓ Valid", c.GREEN))
    else:
        lines.append(colorize("✗ Invalid", c.RED))
        for error in preview.validation_errors:
            lines.append(colorize(f"  - {error}", c.RED))
    lines.append("")

    # Files to create
    lines.append(bold("Files to create:"))
    for cli in preview.target_clis:
        for path in preview.file_paths[cli]:
            size = preview.file_sizes.get(str(path), 0)
            size_str = format_file_size(size)
            lines.append(f"  {blue(str(path))} {gray(f'({size_str})')}")
    lines.append("")

    # Summary
    total_size = preview.total_size()
    total_files = preview.total_files()
    lines.append(
        f"Total: {len(preview.target_clis)} CLIs, {total_files} files, {format_file_size(total_size)}"
    )
    lines.append("")

    # Content preview
    lines.append(bold("--- Content Preview ---"))
    lines.append(gray("-" * 60))

    truncated, total_lines, was_truncated = truncate_content(
        preview.skill_content, max_lines=50
    )
    lines.append(truncated)

    if was_truncated:
        remaining = total_lines - 50
        lines.append(yellow(f"... [{remaining} more lines]"))

    lines.append(gray("-" * 60))
    lines.append(bold("--- End of Preview ---"))
    lines.append("")

    # Resources (if any)
    if preview.resources:
        lines.append(bold("JIT Resources:"))
        for resource in preview.resources:
            size_str = format_file_size(resource.size)
            lines.append(
                f"  [{resource.resource_type}] {resource.filename} {gray(f'({size_str})')}"
            )
        lines.append("")

    # Options
    lines.append(cyan("=" * 60))
    lines.append(bold("Options: ") + "[approve] [expand] [edit] [reject]")
    lines.append(cyan("=" * 60))

    return "\n".join(lines)
